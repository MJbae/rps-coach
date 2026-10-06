import random
def beats(a, b): return (a - b) % 3 == 1
def throw(m, strat, rng):
    if m == 1 or strat == 'indep':
        return [rng.randrange(3) for _ in range(m)]
    if strat == 'same':
        h = rng.randrange(3); return [h]*m
    x = rng.randrange(3); y = (x + rng.choice([1, 2])) % 3
    return [x if i % 2 == 0 else y for i in range(m)]
def game(m, n, sa, sb, rule, rng):
    while True:
        pa, pb = throw(m, sa, rng), throw(n, sb, rng)
        s = set(pa) | set(pb)
        if len(s) != 2:
            continue
        x, y = tuple(s); w = x if beats(x, y) else y
        wa, wb = pa.count(w), pb.count(w)
        if rule == 'II':
            if wb == 0: return 1
            if wa == 0: return 0
            m, n = wa, wb
        else:
            if wa > wb: return 1
            if wb > wa: return 0
            m, n = wa, wb
rng = random.Random(11)
T = 300000
for rule in ['II', 'I']:
    for (m, n) in [(2, 2), (3, 3)]:
        for sa in ['indep', 'same', 'diff']:
            r = sum(game(m, n, sa, 'indep', rule, rng) for _ in range(T)) / T
            print(f"rule {rule} {m}v{n} A={sa:5s} vs indep: {r:.4f}")
