"""Exact finite checks of directly lifted and independently pruned core codes."""

from fractions import Fraction
import importlib.util
import math
import random
import sys


spec = importlib.util.spec_from_file_location("lifting_library", "research-general-algorithm-next.py")
library = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = library
spec.loader.exec_module(library)


def make_core(dimension, routes):
    core_n = 1 << dimension
    n = core_n + len(routes)
    labels = list(range(core_n)) + routes
    tests = [sum(1 << h for h in range(n) if (labels[h] >> bit) & 1)
             for bit in range(dimension)]
    instance = library.Instance(n, tests)

    def build(state, depth):
        if state.bit_count() == 1:
            return library.Tree(state)
        red = state & tests[depth]
        return instance.branch(state, depth, build(red, depth + 1), build(state ^ red, depth + 1))

    core = (1 << core_n) - 1
    return instance, build(core, 0), core


def evaluate(instance, tree, core, stop):
    """Return raw work, finished core mask, and outsider work."""
    def visit(node, population, depth):
        outsiders = population & ~core
        if stop(node, population, depth):
            return 0, 0, 0
        if node.test < 0:
            return (0, node.state if not outsiders else 0, 0)
        red = population & instance.tests[node.test]
        left = visit(node.left, red, depth + 1)
        right = visit(node.right, population ^ red, depth + 1)
        return (population.bit_count() + left[0] + right[0],
                left[1] | right[1],
                outsiders.bit_count() + left[2] + right[2])

    return visit(tree, instance.full, 0)


def all_prefix_profits(instance, tree, core, prizes):
    def visit(node, population):
        if node.test < 0:
            leaf_profit = sum(prizes[h] for h in range(instance.n) if node.state >> h & 1)
            return [leaf_profit] if population.bit_count() == 1 else [0]
        red = population & instance.tests[node.test]
        left = visit(node.left, red)
        right = visit(node.right, population ^ red)
        return [0] + [a + b - population.bit_count() for a in left for b in right]

    return visit(tree, instance.full)


def entropy_stops(tree, counts, prizes, eta):
    total = sum(prizes)
    occupied = [h for h, value in enumerate(counts) if value]
    bad_prize = sum(prizes[h] for h in occupied)
    u = sum(counts)
    slack = eta * total - bad_prize
    assert slack > 0
    stop_states = set()
    outside_bound = 0
    budget_sum = Fraction(0)
    for h in occupied:
        budget = prizes[h] + slack * Fraction(counts[h], u)
        budget_sum += budget
        node, depth = tree, 0
        while sum(prizes[g] for g in range(len(prizes)) if node.state >> g & 1) > budget:
            assert node.test >= 0
            node = node.left if node.left.state >> h & 1 else node.right
            depth += 1
        stop_states.add(node.state)
        outside_bound += counts[h] * depth
    assert budget_sum == eta * total
    return stop_states, outside_bound


def check_ternary_lifts(rng):
    """Exit depth j means response 2 at query j, otherwise binary routing."""
    checks = 0
    for dimension in range(2, 6):
        core_n = 1 << dimension
        _, tree, _ = make_core(dimension, [])
        for _ in range(12):
            routes = [(rng.randrange(core_n), rng.choice([None] + list(range(1, dimension + 1))))
                      for _ in range(rng.randrange(1, core_n * 4))]
            bins = {}
            for label, exit_depth in routes:
                key = ("core", label) if exit_depth is None else ("ghost", exit_depth, label & ((1 << (exit_depth - 1)) - 1))
                bins[key] = bins.get(key, 0) + 1
            contaminated = sum(key[0] == "core" for key in bins)
            if contaminated == core_n:
                continue
            eta = Fraction(core_n + contaminated, 2 * core_n)
            slack = eta * core_n - contaminated
            u = len(routes)
            stop_states = set()
            exposure_bound = 0
            for key, count in bins.items():
                leaf_prize = int(key[0] == "core")
                budget = leaf_prize + slack * Fraction(count, u)
                if key[0] == "core":
                    label, exit_depth = key[1], None
                else:
                    exit_depth, label = key[1], key[2]
                node, depth = tree, 0
                while node.state.bit_count() > budget:
                    if exit_depth is not None and depth + 1 == exit_depth:
                        node, depth = None, depth + 1
                        break
                    assert node.test >= 0
                    node = node.left if node.left.state >> label & 1 else node.right
                    depth += 1
                if node is not None:
                    stop_states.add(node.state)
                exposure_bound += count * depth

            def visit(node, routed, depth):
                if node.state in stop_states:
                    return 0, 0, 0
                if node.test < 0:
                    return 0, int(not routed), 0
                left, right = [], []
                for label, exit_depth in routed:
                    if exit_depth == depth + 1:
                        continue  # Missing response 2 stops unfinished.
                    (left if node.left.state >> label & 1 else right).append((label, exit_depth))
                red = visit(node.left, left, depth + 1)
                blue = visit(node.right, right, depth + 1)
                return (node.state.bit_count() + len(routed) + red[0] + blue[0],
                        red[1] + blue[1], len(routed) + red[2] + blue[2])

            work, completed, outside_work = visit(tree, routes, 0)
            assert completed >= (1 - eta) * core_n
            assert outside_work <= exposure_bound
            assert work <= tree.cost + exposure_bound
            entropy = sum(Fraction(count, u) * math.log2(Fraction(u, count)) for count in bins.values())
            analytic_bound = u * (float(entropy) + math.log2(float(Fraction(core_n, 1) / slack)) + 1)
            assert outside_work <= analytic_bound + 1e-8
            checks += 1
    return checks


def main():
    rng = random.Random(20261018)
    cuts = thresholds = prize_budgets = entropies = prefix_comparisons = 0
    families = []
    for dimension in range(2, 7):
        core_n = 1 << dimension
        route_lists = [[]]
        route_lists += [[0] * u for u in (1, core_n // 2, core_n * 8)]
        for _ in range(8):
            occupied = rng.sample(range(core_n), rng.randrange(1, core_n))
            route_lists.append([rng.choice(occupied) for _ in range(rng.randrange(1, core_n * 5))])
        for routes in route_lists:
            instance, tree, core = make_core(dimension, routes)
            u = len(routes)
            counts = [routes.count(h) for h in range(core_n)]
            occupied = [h for h in range(core_n) if counts[h]]
            c = len(occupied)
            full = evaluate(instance, tree, core, lambda node, pop, depth: False)
            assert full[0] == tree.cost + u * dimension
            assert full[1].bit_count() == core_n - c
            families.append((core_n, u, c))

            for depth_cut in range(dimension + 1):
                def cut(node, population, depth):
                    return depth >= depth_cut and bool(population & ~core)

                work, completed, outside_work = evaluate(instance, tree, core, cut)
                frontier_bad_mass = 0
                def scan(node, population, depth):
                    nonlocal frontier_bad_mass
                    if depth == depth_cut or node.test < 0:
                        if population & ~core:
                            frontier_bad_mass += node.state.bit_count()
                        return
                    red = population & instance.tests[node.test]
                    scan(node.left, red, depth + 1)
                    scan(node.right, population ^ red, depth + 1)
                scan(tree, instance.full, 0)
                assert completed.bit_count() >= core_n - frontier_bad_mass
                assert outside_work <= u * depth_cut
                assert work <= tree.cost + u * depth_cut
                cuts += 1

            for alpha in (Fraction(1), Fraction(1, 2), Fraction(1, 3)):
                def threshold(node, population, depth):
                    return (population & ~core).bit_count() >= alpha * node.state.bit_count()
                work, completed, _ = evaluate(instance, tree, core, threshold)
                assert completed.bit_count() >= core_n - Fraction(u, 1) / alpha
                assert work <= (1 + alpha) * tree.cost
                thresholds += 1

            if not u or c == core_n:
                continue
            # Uniform prizes, with half the uncontaminated core prize available
            # as extra slack for expanding contaminated cells.
            eta = Fraction(core_n + c, 2 * core_n)
            uniform = [1] * core_n
            stops, exact_outside_bound = entropy_stops(tree, counts, uniform, eta)
            work, completed, outside_work = evaluate(
                instance, tree, core, lambda node, pop, depth: node.state in stops)
            assert completed.bit_count() >= (1 - eta) * core_n
            assert outside_work <= exact_outside_bound
            assert work <= tree.cost + exact_outside_bound
            entropy = sum(Fraction(counts[h], u) * math.log2(Fraction(u, counts[h])) for h in occupied)
            bound = u * (float(entropy) + math.log2(float(Fraction(core_n, 1) / (eta * core_n - c))) + 1)
            assert outside_work <= bound + 1e-8
            entropies += 1

            # The rational budget/pruning theorem itself requires no balance.
            prizes = [rng.randrange(1, 20) for _ in range(core_n)]
            bad_prize = sum(prizes[h] for h in occupied)
            eta_weighted = Fraction(sum(prizes) + bad_prize, 2 * sum(prizes))
            stops, exact_outside_bound = entropy_stops(tree, counts, prizes, eta_weighted)
            work, completed, outside_work = evaluate(
                instance, tree, core, lambda node, pop, depth: node.state in stops)
            finished_prize = sum(prizes[h] for h in range(core_n) if completed >> h & 1)
            assert finished_prize >= (1 - eta_weighted) * sum(prizes)
            assert outside_work <= exact_outside_bound
            assert work <= tree.cost + exact_outside_bound
            prize_budgets += 1
            if dimension <= 3:
                optimum_profit = max(all_prefix_profits(instance, tree, core, prizes))
                assert optimum_profit >= finished_prize - work
                prefix_comparisons += 1

    # A simple gamma=1/2 case with many concentrated outsiders.
    instance, tree, core = make_core(6, [0] * 4096)
    counts = [4096] + [0] * 63
    stops, bound = entropy_stops(tree, counts, [1] * 64, Fraction(1, 2))
    work, completed, outside_work = evaluate(instance, tree, core, lambda node, pop, depth: node.state in stops)
    assert completed.bit_count() >= 32
    assert outside_work <= 3 * 4096
    assert work <= tree.cost + 3 * 4096

    ternary_checks = check_ternary_lifts(rng)

    print("PASS lifted code families:", len(families))
    print("PASS exact cut-depth profiles:", cuts)
    print("PASS load-threshold policies:", thresholds)
    print("PASS rational weighted prize-budget policies:", prize_budgets)
    print("PASS entropy exposure bounds:", entropies)
    print("PASS exact prefix-profit dominance:", prefix_comparisons)
    print("PASS ternary missing-response entropy lifts:", ternary_checks)
    print("Concentrated outside family (core, outsiders, completed, work):",
          (64, 4096, completed.bit_count(), work))


if __name__ == "__main__":
    main()
