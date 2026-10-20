"""Complete alternative activation witnesses and fixed-width cover compiler.

The prototype takes a verified full Cartesian labeling. The outer raw-matrix
threshold/factorization portfolio is described in the note, not rerun here.
All constructed codes use actual original query indices. No optimum oracle.
"""

from fractions import Fraction
from functools import lru_cache
import importlib.util
from itertools import product, combinations
import json
from math import prod
from pathlib import Path
import sys


def load_backend():
    spec = importlib.util.spec_from_file_location(
        "activation_certificate_backend", Path(__file__).with_name("research-general-algorithm-next.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BACK = load_backend()


class ChargedOR:
    def __init__(self, sizes, witnesses, charges):
        self.sizes, self.witnesses, self.charges = sizes, witnesses, charges
        self.values, self.actions = {}, {}

    def close(self, counts):
        current, charge = list(counts), 0
        changed = True
        while changed:
            changed = False
            for i, families in enumerate(self.witnesses):
                if current[i] > 1 and any(all(current[p] == 1 for p in w) for w in families):
                    current[i], charge, changed = 1, charge+self.charges[i], True
        return tuple(current), charge

    def solve(self, counts):
        if counts in self.values:
            return self.values[counts]
        closed, charge = self.close(counts)
        if closed != counts:
            result = charge+self.solve(closed)
        elif all(r == 1 for r in counts):
            result = Fraction(0)
        else:
            options = []
            for i, r in enumerate(counts):
                if r <= 1:
                    continue
                child = list(counts)
                child[i] = 1
                hit = self.solve(tuple(child))
                child[i] = r-1
                miss = self.solve(tuple(child))
                options.append((1+(hit+(r-1)*miss)/r, i))
            result, self.actions[counts] = min(options)
        self.values[counts] = result
        assert (prod(counts)*result).denominator == 1
        return result


class Compiler:
    def __init__(self, sizes, points, tests):
        self.sizes, self.points = tuple(sizes), tuple(points)
        assert len(set(points)) == prod(sizes) == len(points)
        assert set(points) == set(product(*(range(size) for size in sizes)))
        self.instance = BACK.Instance(len(points), tests)
        self.n, self.dimension = len(points), len(sizes)
        self.cells = tuple(tuple(sum(1 << h for h, point in enumerate(points) if point[i] == v)
                                 for v in range(size)) for i, size in enumerate(sizes))
        self.equalities = {}
        partitions = {mask: (q, True) for q, mask in enumerate(self.instance.tests)}
        for q, mask in enumerate(self.instance.tests):
            partitions.setdefault(self.instance.full ^ mask, (q, False))
        for i, cells in enumerate(self.cells):
            for v, cell in enumerate(cells):
                assert cell in partitions, "Original factor-value equality missing"
                self.equalities[i, v] = partitions[cell]
        self.contexts, self.codes, self.heights = {}, {}, {}
        for i in range(self.dimension):
            others = [p for p in range(self.dimension) if p != i]
            for pattern in product(*(range(-1, sizes[p]) for p in others)):
                witness = tuple(p for p, v in zip(others, pattern) if v >= 0)
                values = tuple(v for v in pattern if v >= 0)
                context = self.instance.full
                for p, v in zip(witness, values):
                    context &= self.cells[p][v]
                self.contexts[i, witness, values] = context
                local = {}
                for q, mask in enumerate(self.instance.tests):
                    ones, valid = 0, True
                    for v, cell in enumerate(self.cells[i]):
                        selected = context & cell
                        hit = selected & mask
                        if hit and hit != selected:
                            valid = False
                            break
                        if hit:
                            ones |= 1 << v
                    if valid and 0 < ones < (1 << sizes[i])-1:
                        local[q] = ones

                def build(selected):
                    if selected.bit_count() == 1:
                        return BACK.Tree(selected), 0
                    _, q = min((max((selected & ones).bit_count(),
                                    (selected & ~ones).bit_count()), q)
                               for q, ones in local.items()
                               if selected & ones and selected & ~ones)
                    hit = selected & local[q]
                    left, hl = build(hit)
                    right, hr = build(selected ^ hit)
                    return BACK.Tree(selected, q, left, right,
                                     selected.bit_count()+left.cost+right.cost), 1+max(hl, hr)
                code, height = build((1 << sizes[i])-1)
                self.codes[i, witness, values] = code, local
                self.heights[i, witness] = max(self.heights.get((i, witness), 0), height)

    def witness_family(self, charges):
        return tuple(tuple(w for (target, w), height in self.heights.items()
                           if target == i and height <= charges[i])
                     for i in range(self.dimension))

    def query_cover(self, response, witnesses, width):
        terms = {}
        for (i, w, a), context in self.contexts.items():
            if w not in witnesses[i]:
                continue
            target_values, term = 0, 0
            for v, cell in enumerate(self.cells[i]):
                selected = context & cell
                if selected & response == selected:
                    target_values |= 1 << v
                    term |= selected
            if term:
                assert term & response == term
                terms.setdefault(term, (i, w, a, target_values))
        if response in terms:
            return (terms[response],)
        if width == 2:
            rows = list(terms.items())
            for (first, ft), (second, st) in combinations(rows, 2):
                if first | second == response:
                    return ft, st
        return None

    def certify(self, charges, width=2):
        assert width in (1, 2), "Only fixed width one/two implemented"
        witnesses = self.witness_family(charges)
        covers = {}
        equality_masks = {self.cells[i][v] for i, v in self.equalities}
        equality_masks |= {self.instance.full ^ cell for cell in equality_masks}
        for q, mask in enumerate(self.instance.tests):
            if mask in equality_masks or mask in (0, self.instance.full):
                continue
            cover = self.query_cover(mask, witnesses, width)
            orientation = True
            if cover is None:
                cover = self.query_cover(self.instance.full ^ mask, witnesses, width)
                orientation = False
            if cover is None:
                return None
            desired = mask if orientation else self.instance.full ^ mask
            union = 0
            for i, w, a, values in cover:
                term = self.contexts[i, w, a] & sum(self.cells[i][v] for v in range(self.sizes[i])
                                                  if values >> v & 1)
                union |= term
            assert union == desired
            covers[q] = orientation, cover
        return witnesses, covers

    def physical_code(self, charges, witnesses):
        dp = ChargedOR(self.sizes, witnesses, charges)
        value = dp.solve(self.sizes)

        @lru_cache(None)
        def state(candidates):
            selected = self.instance.full
            for i, values in enumerate(candidates):
                selected &= sum(self.cells[i][v] for v in range(self.sizes[i]) if values >> v & 1)
            return selected

        def build(candidates):
            ambient = state(candidates)
            if ambient.bit_count() == 1:
                return BACK.Tree(ambient)
            enabled = [(i, w) for i, families in enumerate(witnesses)
                       if candidates[i].bit_count() > 1 for w in families
                       if all(candidates[p].bit_count() == 1 for p in w)]
            if enabled:
                i, w = enabled[0]
                a = tuple(candidates[p].bit_length()-1 for p in w)
                node, local = self.codes[i, w, a]
                while node.test >= 0:
                    hit = candidates[i] & local[node.test]
                    if hit and hit != candidates[i]:
                        q, actual_ones = node.test, local[node.test]
                        break
                    node = node.left if hit else node.right
                else:
                    raise AssertionError("Certified code did not separate candidates")
            else:
                counts = tuple(values.bit_count() for values in candidates)
                assert dp.close(counts) == (counts, 0)
                dp.solve(counts)
                i = dp.actions[counts]
                v = (candidates[i] & -candidates[i]).bit_length()-1
                q, orientation = self.equalities[i, v]
                actual_ones = 1 << v if orientation else ((1 << self.sizes[i])-1) ^ (1 << v)
            hit = candidates[i] & actual_ones
            updated = list(candidates)
            updated[i] = hit
            left = build(tuple(updated))
            updated[i] = candidates[i] ^ hit
            right = build(tuple(updated))
            assert left.state == ambient & self.instance.tests[q]
            assert right.state == ambient ^ left.state
            return self.instance.branch(ambient, q, left, right)
        tree = build(tuple((1 << size)-1 for size in self.sizes))
        assert tree.cost <= self.n*value
        for h in range(self.n):
            node = tree
            while node.test >= 0:
                node = node.left if self.instance.tests[node.test] >> h & 1 else node.right
            assert node.state == 1 << h
        return tree, value, len(dp.values)


def main():
    sizes = (4, 4, 4)
    points = tuple(product(*(range(size) for size in sizes)))
    tests = [sum(1 << h for h, point in enumerate(points) if point[i] == v)
             for i, size in enumerate(sizes) for v in range(size)]
    intended = (((2,),), ((2,),), ((0,), (1,)))
    for i, families in enumerate(intended):
        for w in families:
            for a in product(*(range(sizes[p]) for p in w)):
                for bit in range(2):
                    tests.append(sum(1 << h for h, point in enumerate(points)
                                     if all(point[p] == v for p, v in zip(w, a))
                                     and ((point[i]+sum(a)) % sizes[i]) >> bit & 1))
    # One physical test combines activation terms with distinct target/witness roles.
    tests.append(sum(1 << h for h, x in enumerate(points)
                     if x[0] == 0 and x[2] in (1, 3) or x[2] == 1 and x[0] in (2, 3)))
    full = (1 << len(points))-1
    tests = [mask if q % 3 else full ^ mask for q, mask in enumerate(tests)]
    compiler = Compiler(sizes, points, tests)
    cert = compiler.certify((2, 2, 2), 2)
    assert cert is not None
    witnesses, covers = cert
    assert (0,) in witnesses[2] and (1,) in witnesses[2]
    assert compiler.certify((2, 2, 2), 1) is None
    tree, charged, states = compiler.physical_code((2, 2, 2), witnesses)
    successful, best = 0, tree.cost
    for charges in product(*(range(1, size) for size in sizes)):
        candidate = compiler.certify(charges, 2)
        if candidate is not None:
            successful += 1
            code, value, visited = compiler.physical_code(charges, candidate[0])
            best = min(best, code.cost)
            assert visited <= compiler.n
    output = {"status": "passed", "n": compiler.n, "queries": len(compiler.instance.tests),
              "local_context_codes": len(compiler.codes),
              "target_witness_pairs": len(compiler.heights),
              "actual_multiple_witnesses_for_target_two": witnesses[2],
              "cover_width_one_rejected": True, "cover_width_two_accepted": True,
              "certified_non_equality_queries": len(covers),
              "charged_mean_at_two_per_factor": str(charged), "count_states": states,
              "actual_work_at_two_per_factor": tree.cost,
              "charge_vectors_tested": prod(size-1 for size in sizes),
              "successful_charge_vectors": successful, "best_portfolio_work": best,
              "all_codes_executed_on_every_hypothesis": True,
              "complemented_physical_questions_included": True,
              "full_factorization_supplied_in_this_checker": True,
              "no_unrestricted_OPT_oracle": True}
    Path(__file__).with_name("research-general-activation-certificates-results.json").write_text(
        json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
