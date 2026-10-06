"""Leader-vs-everyone 'last one standing' with a crowd: our team (n coordinated or independent) + M independent others.
Host throws uniformly at random. Rule A: only those who beat the host survive. Rule B: beat or tie survive.
If a round would eliminate everyone still standing, the round is void (replayed).
Game ends when exactly one player remains. Estimate P(final survivor is from our team).
Symmetric baseline (everyone independent): n/(n+M).
"""
import random, sys

def play(n, M, rule, coordinated, rng):
    team, others = n, M
    while team + others > 1:
        h = rng.randrange(3)
        # team allocation
        if coordinated and team >= 1:
            q, r = divmod(team, 3)
            alloc = [q + (1 if i < r else 0) for i in range(3)]
            rng.shuffle(alloc)  # random labelling so the split is not predictable
        else:
            alloc = [0, 0, 0]
            for _ in range(team):
                alloc[rng.randrange(3)] += 1
        oth = [0, 0, 0]
        for _ in range(others):
            oth[rng.randrange(3)] += 1
        win_hand = (h + 1) % 3   # hand that beats host (Paper beats Rock if 0=R,1=P,2=S)
        lose_hand = (h + 2) % 3  # hand that loses to host
        if rule == 'A':
            nt, no = alloc[win_hand], oth[win_hand]
        else:
            nt, no = team - alloc[lose_hand], others - oth[lose_hand]
        if nt + no == 0:
            continue  # void round
        team, others = nt, no
    return team == 1

def est(n, M, rule, coordinated, trials=200000, seed=7):
    rng = random.Random(seed)
    return sum(play(n, M, rule, coordinated, rng) for _ in range(trials)) / trials

for (n, M) in [(3, 27), (5, 45), (10, 90), (10, 30)]:
    base = n / (n + M)
    for rule in ['A', 'B']:
        pi = est(n, M, rule, False)
        pc = est(n, M, rule, True)
        print(f"n={n:2d} M={M:3d} rule {rule}: baseline {base:.3f} | independent {pi:.3f} | coordinated-even-split {pc:.3f}")
