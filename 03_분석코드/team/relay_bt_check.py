import itertools, random
from functools import lru_cache
def relay(order_A, order_B, p):
    @lru_cache(None)
    def f(i, j):
        if i == len(order_A): return 0.0
        if j == len(order_B): return 1.0
        q = p(order_A[i], order_B[j])
        return q * f(i, j + 1) + (1 - q) * f(i + 1, j)
    return f(0, 0)
rng = random.Random(42)
maxspread_bt = 0.0
maxspread_gen = 0.0
for trial in range(200):
    n = rng.choice([3, 4, 5])
    sa = [rng.uniform(0.3, 3) for _ in range(n)]; sb = [rng.uniform(0.3, 3) for _ in range(n)]
    bt = lambda i, j: sa[i] / (sa[i] + sb[j])
    vals = [relay(o, tuple(range(n)), bt) for o in itertools.permutations(range(n))]
    vals_b = [relay(tuple(range(n)), ob, bt) for ob in itertools.permutations(range(n))]
    maxspread_bt = max(maxspread_bt, max(vals) - min(vals), max(vals_b) - min(vals_b))
    M = [[rng.uniform(0.2, 0.8) for _ in range(n)] for _ in range(n)]
    gen = lambda i, j: M[i][j]
    vals2 = [relay(o, tuple(range(n)), gen) for o in itertools.permutations(range(n))]
    maxspread_gen = max(maxspread_gen, max(vals2) - min(vals2))
print("max spread of team-win prob across orderings, Bradley-Terry:", maxspread_bt)
print("max spread across orderings, arbitrary matchup matrix:", round(maxspread_gen, 4))
