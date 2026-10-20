"""Independent exact audit of weighted fixed-tree restriction potentials."""

from fractions import Fraction
import importlib.util
import random
import sys


spec = importlib.util.spec_from_file_location("tree_potential_source", "research-general-tree-potential.py")
source = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = source
spec.loader.exec_module(source)
library = source.library


def weighted_work(node, selected, weights):
    if selected.bit_count() <= 1 or node.test < 0:
        return Fraction(0)
    left = selected & node.left.state
    right = selected & node.right.state
    value = weights.get(node.state, Fraction(0)) * selected.bit_count() if left and right else 0
    return value + weighted_work(node.left, left, weights) + weighted_work(node.right, right, weights)


def weighted_drop(tree, selected, test, weights):
    return (weighted_work(tree, selected, weights)
            - weighted_work(tree, selected & test, weights)
            - weighted_work(tree, selected & ~test, weights))


def separate(tree, test, weights):
    def solve(node):
        if node.test < 0:
            color = (1, 0) if node.state & test else (0, 1)
            return {(0, 0): (Fraction(0), 0), color: (Fraction(0), node.state)}
        left, right = solve(node.left), solve(node.right)
        answer = {}
        for (rl, bl), (vl, sl) in left.items():
            for (rr, br), (vr, sr) in right.items():
                red, blue = rl + rr, bl + br
                increment = 0
                if rl + bl and rr + br:
                    if not (rl and rr):
                        increment += red
                    if not (bl and br):
                        increment += blue
                value = vl + vr + weights.get(node.state, Fraction(0)) * increment
                key = red, blue
                if key not in answer or value > answer[key][0]:
                    answer[key] = value, sl | sr
        return answer

    best = Fraction(0), 0
    for (red, blue), (value, selected) in solve(tree).items():
        if red + blue and value / (red + blue) > best[0]:
            best = value / (red + blue), selected
    assert weighted_drop(tree, best[1], test, weights) == best[0] * best[1].bit_count()
    return best


def internal_nodes(tree):
    if tree.test >= 0:
        yield tree
        yield from internal_nodes(tree.left)
        yield from internal_nodes(tree.right)


def coordinate_tree(dimension):
    n = 1 << dimension
    tests = [sum(1 << h for h in range(n) if (h >> b) & 1) for b in range(dimension)]
    instance = library.Instance(n, tests)

    def build(state, depth):
        if state.bit_count() <= 1:
            return library.Tree(state)
        red = state & tests[depth]
        blue = state ^ red
        return instance.branch(state, depth, build(red, depth + 1), build(blue, depth + 1))

    return instance, build(instance.full, 0)


def main():
    rng = random.Random(20261018)
    weighted_checks = 0
    for n in range(2, 9):
        for _ in range(10):
            tests = [rng.randrange(1, (1 << n) - 1) for _ in range(4)]
            tests += [sum(1 << h for h in range(n) if (h >> b) & 1)
                      for b in range((n - 1).bit_length())]
            instance = library.Instance(n, tests)
            tree = instance.greedy(instance.full)
            weights = {node.state: Fraction(rng.randrange(0, 8), rng.randrange(1, 9))
                       for node in internal_nodes(tree)}
            for test in instance.tests:
                found = separate(tree, test, weights)[0]
                brute = max(weighted_drop(tree, selected, test, weights) / selected.bit_count()
                            for selected in range(1, 1 << n))
                assert found == brute
                weighted_checks += 1

    witness_checks = 0
    average_checks = 0
    analytic_bounds = []
    for dimension in range(2, 11):
        instance, tree = coordinate_tree(dimension)
        n = instance.n
        final_test = instance.tests[-1]
        weights = {node.state: Fraction(rng.randrange(0, 8), 7)
                   for node in internal_nodes(tree)}
        level_nodes = {0: [(tree, [])]}
        for depth in range(dimension):
            level_nodes[depth + 1] = []
            for node, ancestors in level_nodes[depth]:
                level_nodes[depth + 1].append((node.left, ancestors + [(node, node.right)]))
                level_nodes[depth + 1].append((node.right, ancestors + [(node, node.left)]))

        for depth in range(dimension):
            total_path_weight = Fraction(0)
            total_deficit = Fraction(0)
            total_size = 0
            red_mass = 1 << (dimension - depth - 1)
            for node, ancestors in level_nodes[depth]:
                selected = node.state & final_test
                path_weight = Fraction(0)
                for ancestor, opposite in ancestors:
                    blue = opposite.state & ~final_test
                    assert blue
                    selected |= blue & -blue
                    path_weight += weights[ancestor.state]
                assert selected.bit_count() == red_mass + depth
                value = weighted_drop(tree, selected, final_test, weights)
                assert value >= red_mass * path_weight
                total_path_weight += path_weight
                total_deficit += value
                total_size += selected.bit_count()
                witness_checks += 1
            sum_averages = sum(sum(weights[node.state] for node, _ in level_nodes[i]) / (1 << i)
                               for i in range(depth))
            assert sum_averages == total_path_weight / (1 << depth)
            # This rearrangement is valid for arbitrary weights; capacity feasibility
            # would additionally bound the mean actual deficit by mean selected size.
            assert red_mass * total_path_weight <= total_deficit
            assert total_size == (1 << depth) * (red_mass + depth)
            average_checks += 1

        if dimension >= 4:
            ceil_log = (dimension - 1).bit_length()
            remaining = ceil_log + 1
            depth = dimension - remaining
            upper = Fraction(remaining + 1) + Fraction(depth, 1 << (remaining - 1))
            assert upper <= ceil_log + 3
            analytic_bounds.append((dimension, str(upper), str(Fraction(dimension, ceil_log + 3))))

    pair_capacity_checks = 0
    for dimension in range(1, 5):
        n = 1 << dimension
        for selected in range(1 << n):
            for bit in range(dimension):
                edges = sum(bool((selected >> h) & 1) and bool((selected >> (h ^ (1 << bit))) & 1)
                            for h in range(n) if not ((h >> bit) & 1))
                assert 2 * edges <= selected.bit_count()
                pair_capacity_checks += 1
        assert 2 * dimension * (n // 2) == n * dimension

    print("PASS rational weighted separation comparisons:", weighted_checks)
    print("PASS cube witness inequalities:", witness_checks)
    print("PASS averaged path identities:", average_checks)
    print("PASS exact pair matching capacities:", pair_capacity_checks)
    print("Analytic weighted-LP mean upper bounds (D, bound, guaranteed gap):", analytic_bounds)


if __name__ == "__main__":
    main()
