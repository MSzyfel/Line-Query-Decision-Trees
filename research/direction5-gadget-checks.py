"""Finite checks for direction 5; the accompanying report supplies the proofs."""

from functools import lru_cache
from itertools import combinations
from random import Random


def matching_number(n, edges):
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        best = solve(rest)
        choices = adjacency[u] & rest
        while choices:
            v = choices & -choices
            choices ^= v
            best = max(best, 1 + solve(rest ^ v))
        return best

    return solve((1 << n) - 1)


def exact(n, queries, weights=None):
    total = (1 << n) - 1
    weights = weights or [1] * n

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0, 0
        cost = sum(weights[i] for i in range(n) if state >> i & 1)
        candidates = []
        for query in queries:
            left = state & query
            right = state ^ left
            if left and right:
                lw, le = solve(left)
                rw, re = solve(right)
                candidates.append((1 + max(lw, rw), cost + le + re))
        assert candidates, (n, queries, state)
        return min(w for w, e in candidates), min(e for w, e in candidates)

    return solve(total)


def check_pair_family(n, queries):
    codes = [tuple((q >> i) & 1 for q in queries) for i in range(n + 1)]
    if len(set(codes)) != n + 1:
        return False
    edges = [tuple(i for i in range(n) if q >> i & 1)
             for q in queries if q.bit_count() == 2]
    r = matching_number(n, edges)
    expected = n * (n + 3) // 2 - (n - 1) * r + r * r
    worst = max(n - r, r + 1)
    actual = exact(n + 1, queries)
    assert actual == (worst, expected), (n, queries, r, actual, worst, expected)
    return True


def pair_checks():
    checked = 0
    # Every singleton/pair family through four nonzero vertices.
    for n in range(1, 5):
        universe = [1 << i for i in range(n)]
        universe += [(1 << u) | (1 << v) for u, v in combinations(range(n), 2)]
        for mask in range(1 << len(universe)):
            queries = [q for j, q in enumerate(universe) if mask >> j & 1]
            checked += check_pair_family(n, queries)
    # Every graph on five vertices, with no singleton tests.
    n = 5
    universe = [(1 << u) | (1 << v) for u, v in combinations(range(n), 2)]
    for mask in range(1 << len(universe)):
        queries = [q for j, q in enumerate(universe) if mask >> j & 1]
        checked += check_pair_family(n, queries)
    rng = Random(5001)
    for _ in range(1000):
        n = rng.randrange(5, 8)
        universe = [1 << i for i in range(n)]
        universe += [(1 << u) | (1 << v) for u, v in combinations(range(n), 2)]
        queries = [q for q in universe if rng.random() < .5]
        checked += check_pair_family(n, queries)
    return checked


def make_tree(state, queries, rng):
    if state.bit_count() == 1:
        return state.bit_length() - 1
    useful = [q for q in queries if state & q and state & q != state]
    query = rng.choice(useful)
    left = state & query
    return query, make_tree(left, queries, rng), make_tree(state ^ left, queries, rng)


def restrict(tree, state):
    if isinstance(tree, int):
        assert state == 1 << tree
        return tree
    query, left, right = tree
    ls = state & query
    rs = state ^ ls
    if not ls:
        return restrict(right, rs)
    if not rs:
        return restrict(left, ls)
    return query, restrict(left, ls), restrict(right, rs)


def promote(tree, state, queries):
    if not queries:
        return restrict(tree, state)
    query = queries[0]
    ls = state & query
    rs = state ^ ls
    if not ls or not rs:
        return promote(tree, state, queries[1:])
    return query, promote(tree, ls, queries[1:]), promote(tree, rs, queries[1:])


def paths(tree, path=()):
    if isinstance(tree, int):
        return {tree: path}
    query, left, right = tree
    return paths(left, path + (query,)) | paths(right, path + (query,))


def promotion_checks():
    rng = Random(5002)
    for _ in range(1000):
        n = rng.randrange(2, 10)
        full = (1 << n) - 1
        queries = set(1 << i for i in range(n))
        queries.update(rng.randrange(1, full) for _ in range(n))
        queries = sorted(queries)
        weights = [rng.randrange(1, 31) for _ in range(n)]
        original = make_tree(full, queries, rng)
        old = paths(original)
        chosen = rng.sample(queries, rng.randrange(1, min(5, len(queries)) + 1))
        promoted = promote(original, full, chosen)
        new = paths(promoted)
        for h in range(n):
            assert len(new[h]) <= len(old[h]) + len(chosen) - len(set(chosen) & set(old[h]))
        old_cost = sum(weights[h] * len(old[h]) for h in range(n))
        new_cost = sum(weights[h] * len(new[h]) for h in range(n))
        bound = sum(weights[h] * (len(chosen) - len(set(chosen) & set(old[h])))
                    for h in range(n))
        assert new_cost <= old_cost + bound
        assert max(map(len, new.values())) <= max(map(len, old.values())) + len(chosen)
    return 1000


if __name__ == '__main__':
    print(f'Uniform singleton/pair families checked against exact subset DP: {pair_checks()}')
    print(f'Query-promotion trees checked: {promotion_checks()}')
    q = [(1 << j) - 1 for j in range(1, 6)]
    print('Six-point rational threshold example, (height, raw expected):',
          exact(6, q, [8, 1, 1, 1, 1, 8]))
