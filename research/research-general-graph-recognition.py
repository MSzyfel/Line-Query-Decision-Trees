"""Recognize and execute the canonical graph-gated product 2-approximation.

The public recognizer reads only the original response matrix. It receives no
coordinate labels, graph, semantic test orientations, or private-code labels.
There is no exact unrestricted UDT optimization in this file.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import prod
from pathlib import Path
import importlib.util
import json
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CONTEXT = load("graph_recognition_context", "research-general-factor-contexts.py")
GRAPH = load("graph_recognition_activation", "research-general-dependency-graph.py")
BACK = CONTEXT.BACK


@dataclass(frozen=True)
class QuestionRef:
    query: int
    positive_response: bool
    target_subset: int

    def actual_ones(self, full_values):
        return self.target_subset if self.positive_response else full_values ^ self.target_subset


@dataclass
class Representation:
    instance: object
    alphabet: int
    labels: tuple
    cells: tuple
    parents: tuple
    equalities: dict
    palettes: dict
    support_oracle_calls: int

    @property
    def dimension(self):
        return len(self.parents)


def _recognize_alphabet(instance, alphabet):
    """Return (certificate, diagnostic); recognition is deliberately strict."""
    if alphabet < 4 or alphabet & (alphabet - 1):
        return None, "alphabet is not a power of two at least four"
    width = alphabet.bit_length() - 1
    remainder, dimension = instance.n, 0
    while remainder > 1 and remainder % alphabet == 0:
        remainder //= alphabet
        dimension += 1
    if remainder != 1 or not dimension:
        return None, "hypothesis count is not a positive power of the alphabet"
    threshold = instance.n // alphabet
    retained = tuple(q for q, mask in enumerate(instance.tests)
                     if min((mask & instance.full).bit_count(),
                            (instance.full ^ (mask & instance.full)).bit_count()) >= threshold)
    factors = CONTEXT.ResponseFactors(instance, retained)
    if factors.quotient_size != instance.n:
        return None, "threshold quotient does not identify the hypotheses"
    if factors.alphabets != (alphabet,) * dimension:
        return None, "threshold factors do not have the proposed common alphabet"
    labels, cells = factors.labels, factors.cells
    all_values = (1 << alphabet) - 1
    equalities, palettes, parent_sets = {}, {}, {}

    def box(mask):
        projections = [0] * dimension
        for h, label in enumerate(labels):
            if mask >> h & 1:
                for i, value in enumerate(label):
                    projections[i] |= 1 << value
        if not mask or prod(values.bit_count() for values in projections) != mask.bit_count():
            return None
        # The selected points lie in their projection product. Because the
        # labels are a bijection onto the full product, equal sizes prove the
        # full Cartesian-box equality, not just projection compatibility.
        return tuple(projections)

    for q, original_mask in enumerate(instance.tests):
        original_mask &= instance.full
        if not original_mask or original_mask == instance.full:
            continue
        parsed = []
        for positive_response, mask in ((True, original_mask),
                                        (False, instance.full ^ original_mask)):
            projections = box(mask)
            if projections is None:
                continue
            singleton_axes = [i for i, values in enumerate(projections) if values.bit_count() == 1]
            if (len(singleton_axes) == 1
                    and all(values == all_values or i == singleton_axes[0]
                            for i, values in enumerate(projections))):
                i = singleton_axes[0]
                value = projections[i].bit_length() - 1
                parsed.append(("eq", i, value,
                               QuestionRef(q, positive_response, projections[i])))
                continue
            targets = [i for i, values in enumerate(projections)
                       if values.bit_count() == alphabet // 2]
            if len(targets) != 1:
                continue
            i = targets[0]
            if not all(j == i or values == all_values or values.bit_count() == 1
                       for j, values in enumerate(projections)):
                continue
            parents = tuple(singleton_axes)
            assert i not in parents
            context = tuple(projections[p].bit_length() - 1 for p in parents)
            parsed.append(("gate", i, parents, context,
                           QuestionRef(q, positive_response, projections[i])))
        if not parsed:
            return None, f"query {q} is neither a pure equality nor a permitted private box"
        # For root bits both response cells parse, but they give the same
        # target and complementary local partitions. Other permitted forms
        # have a unique semantic positive cell when alphabet >= 4.
        semantic = {(item[0], item[1], item[2]) for item in parsed}
        if len(semantic) != 1:
            return None, f"query {q} has incompatible permitted descriptions"
        item = parsed[0]
        if item[0] == "eq":
            _, i, value, ref = item
            equalities.setdefault((i, value), ref)
        else:
            _, i, parents, context, ref = item
            if i in parent_sets and parent_sets[i] != parents:
                return None, f"target {i} has mixed parent sets"
            parent_sets[i] = parents
            partition = min(ref.target_subset, all_values ^ ref.target_subset)
            palettes.setdefault((i, context), {}).setdefault(partition, ref)

    if len(equalities) != dimension * alphabet:
        return None, "some pure coordinate equality is missing"
    if len(parent_sets) != dimension:
        return None, "some coordinate has no private or root fast palette"
    for i in range(dimension):
        parents = parent_sets[i]
        expected_contexts = set(product(range(alphabet), repeat=len(parents)))
        actual_contexts = {context for target, context in palettes if target == i}
        if actual_contexts != expected_contexts:
            return None, f"target {i} is missing at least one parent context"
        for context in expected_contexts:
            rows = tuple(palettes[i, context].values())
            if len(rows) != width:
                return None, f"target {i}, context {context} does not have exactly b distinct local bits"
            words = {tuple(bool(ref.target_subset >> value & 1) for ref in rows)
                     for value in range(alphabet)}
            if len(words) != alphabet:
                return None, f"target {i}, context {context} has a noninjective local palette"
            palettes[i, context] = rows
    return Representation(instance, alphabet, labels, cells,
                          tuple(parent_sets[i] for i in range(dimension)),
                          equalities, palettes, factors.oracle_calls), "accepted"


def recognize(instance, alphabet=None):
    """Return (Representation or None, list of attempted-alphabet diagnostics)."""
    guesses = [alphabet] if alphabet is not None else [
        1 << exponent for exponent in range(2, instance.n.bit_length())
        if instance.n % (1 << exponent) == 0]
    diagnostics = []
    for guess in guesses:
        certificate, reason = _recognize_alphabet(instance, guess)
        diagnostics.append({"alphabet": guess, "reason": reason})
        if certificate is not None:
            return certificate, diagnostics
    return None, diagnostics


def execute_recognized(certificate):
    """Return an actual original-query Tree and exact charged-DP statistics."""
    instance, alphabet = certificate.instance, certificate.alphabet
    dimension = certificate.dimension
    width = alphabet.bit_length() - 1
    all_values = (1 << alphabet) - 1
    dp = GRAPH.ChargedActivationDP((alphabet,) * dimension,
                                   certificate.parents, (width,) * dimension)
    charged = dp.solve((alphabet,) * dimension)

    @lru_cache(None)
    def state(candidates):
        result = instance.full
        for i, selected in enumerate(candidates):
            result &= sum(certificate.cells[i][v] for v in range(alphabet)
                          if selected >> v & 1)
        return result

    @lru_cache(None)
    def build(candidates):
        ambient = state(candidates)
        if ambient.bit_count() == 1:
            return BACK.Tree(ambient)
        enabled = [i for i, parents in enumerate(certificate.parents)
                   if candidates[i].bit_count() > 1
                   and all(candidates[p].bit_count() == 1 for p in parents)]
        if enabled:
            i = enabled[0]
            context = tuple(candidates[p].bit_length() - 1 for p in certificate.parents[i])
            ref = next(ref for ref in certificate.palettes[i, context]
                       if 0 < (candidates[i] & ref.actual_ones(all_values)).bit_count()
                       < candidates[i].bit_count())
        else:
            counts = tuple(selected.bit_count() for selected in candidates)
            assert dp.close(counts) == counts
            dp.solve(counts)
            i = dp.actions[counts]
            value = (candidates[i] & -candidates[i]).bit_length() - 1
            ref = certificate.equalities[i, value]
        hit_values = candidates[i] & ref.actual_ones(all_values)
        assert hit_values and hit_values != candidates[i]
        updated = list(candidates)
        updated[i] = hit_values
        left = build(tuple(updated))
        updated[i] = candidates[i] ^ hit_values
        right = build(tuple(updated))
        assert left.state == ambient & instance.tests[ref.query]
        assert right.state == ambient ^ left.state
        return instance.branch(ambient, ref.query, left, right)

    tree = build((all_values,) * dimension)
    assert tree.cost <= instance.n * charged
    CONTEXT.execute(instance, tree)
    return tree, {"alphabet": alphabet, "dimension": dimension,
                  "parents": certificate.parents,
                  "palette_groups": len(certificate.palettes),
                  "count_states": len(dp.values), "charged_mean": str(charged),
                  "actual_work": tree.cost,
                  "support_oracle_calls": certificate.support_oracle_calls,
                  "complement_oriented_equalities": sum(not ref.positive_response
                                                        for ref in certificate.equalities.values()),
                  "complement_oriented_palette_rows": sum(not ref.positive_response
                        for rows in certificate.palettes.values() for ref in rows)}


def make_case(alphabet, parents, seed, orientations):
    rng = random.Random(seed)
    dimension, width = len(parents), alphabet.bit_length() - 1
    points = list(product(range(alphabet), repeat=dimension))
    rng.shuffle(points)
    n, rows, descriptions = len(points), [], []
    for i in range(dimension):
        for value in range(alphabet):
            rows.append(sum(1 << h for h, x in enumerate(points) if x[i] == value))
            descriptions.append(("eq", i, value))
    for i, pa in enumerate(parents):
        for context in product(range(alphabet), repeat=len(pa)):
            code = list(range(alphabet))
            rng.shuffle(code)
            for bit in range(width):
                rows.append(sum(1 << h for h, x in enumerate(points)
                                if all(x[p] == a for p, a in zip(pa, context))
                                and code[x[i]] >> bit & 1))
                descriptions.append(("gate", i, context, bit))
    full = (1 << n) - 1
    decorated = []
    for mask, desc in zip(rows, descriptions):
        flip = orientations == "all" or orientations == "mixed" and rng.randrange(2)
        decorated.append((full ^ mask if flip else mask, desc))
    rng.shuffle(decorated)
    instance = BACK.Instance(n, [mask for mask, _ in decorated])
    # Preserve physical-mask metadata only for generating negative tests;
    # recognize() and execute_recognized() never receive these descriptions.
    metadata = {mask: desc for mask, desc in decorated}
    return instance, metadata


def main():
    definitions = [
        (4, [()], "none"),
        (4, [(), (0,)], "none"),
        (4, [(), (0,)], "all"),
        (4, [(1,), (0,)], "mixed"),
        (4, [(), (0,), (0, 1)], "all"),
        (4, [(2,), (0,), (1,)], "mixed"),
        (4, [(1, 2), (0, 2), (0, 1)], "mixed"),
        (8, [(1,), (0,)], "mixed"),
    ]
    accepted = []
    for j, (alphabet, parents, orientations) in enumerate(definitions):
        instance, _ = make_case(alphabet, parents, 2026101909 + j, orientations)
        certificate, diagnostics = recognize(instance)
        assert certificate is not None, diagnostics
        tree, stats = execute_recognized(certificate)
        assert stats["count_states"] <= instance.n
        accepted.append({"n": instance.n, "queries": len(instance.tests),
                         "orientation_mode": orientations, **stats})

    # A cyclic two-axis model has no root bits, so all attempted bad matrices
    # below retain the original pure equalities at the proposed threshold.
    original, descriptions = make_case(4, [(1,), (0,)], 2026101999, "none")
    gate_query = next(q for q, mask in enumerate(original.tests)
                      if descriptions[mask][0] == "gate")
    gate_mask = original.tests[gate_query]
    negative = []

    def reject(name, rows, n=None):
        instance = BACK.Instance(original.n if n is None else n, rows)
        certificate, diagnostics = recognize(instance)
        assert certificate is None, (name, diagnostics)
        negative.append({"case": name, "diagnostics": diagnostics})

    # Moving one positive point to a different parent cell preserves size two
    # but makes the support a diagonal, not its projection-product box.
    positive = [h for h in range(original.n) if gate_mask >> h & 1]
    # Use recovered labels to ensure both coordinate projections change.
    certificate, _ = recognize(original, alphabet=4)
    anchor = certificate.labels[positive[1]]
    outside = next(h for h, label in enumerate(certificate.labels)
                   if not gate_mask >> h & 1 and all(a != b for a, b in zip(anchor, label)))
    altered = gate_mask ^ (1 << positive[0]) ^ (1 << outside)
    rows = list(original.tests)
    rows[gate_query] = altered
    reject("false Cartesian box", rows)

    reject("missing palette row", [mask for q, mask in enumerate(original.tests) if q != gate_query])
    chosen_description = descriptions[gate_mask]
    reject("missing entire parent context", [mask for mask in original.tests
            if not (descriptions[mask][0] == "gate"
                    and descriptions[mask][1:3] == chosen_description[1:3])])
    diagonal = sum(1 << h for h, label in enumerate(certificate.labels) if label[0] == label[1])
    reject("extra incompatible diagonal question", list(original.tests) + [diagonal])
    # Remove one required equality. Its one-hot relation stays prime from the
    # other values, so rejection tests the explicit coverage check as well.
    eq_query = next(q for q, mask in enumerate(original.tests) if descriptions[mask][0] == "eq")
    reject("missing pure equality", [mask for q, mask in enumerate(original.tests) if q != eq_query])

    # A disallowed second parent set on one target is a valid box but must not
    # be silently merged into the existing graph representation.
    half_global = sum(1 << h for h, label in enumerate(certificate.labels) if label[0] < 2)
    reject("mixed target parent sets", list(original.tests) + [half_global])

    # Three distinct balanced bits need not identify eight values: use two
    # independent bits and their XOR in one formerly complete local palette.
    larger, _ = make_case(8, [(1,), (0,)], 20261019101, "none")
    larger_certificate, _ = recognize(larger, alphabet=8)
    rows = list(larger.tests)
    refs = larger_certificate.palettes[0, (0,)]
    for bit, ref in enumerate(refs):
        rows[ref.query] = sum(1 << h for h, label in enumerate(larger_certificate.labels)
                              if label[1] == 0 and ((label[0] & 1) if bit == 0
                                  else (label[0] >> 1 & 1) if bit == 1
                                  else (label[0] & 1) ^ (label[0] >> 1 & 1)))
    reject("balanced but noninjective local palette", rows, n=larger.n)
    output = {"accepted_cases": len(accepted), "rejected_cases": len(negative),
              "accepted": accepted, "rejections": negative,
              "recognizer_input_is_only_original_response_matrix": True,
              "no_unrestricted_optimum_oracle": True,
              "structured_approximation_factor": 2}
    Path(__file__).with_suffix(".results.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
