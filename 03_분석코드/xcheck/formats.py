"""Independent cross-check of team-format math for RPS (no empirical parameters needed)."""
from functools import lru_cache
from math import comb


def p_best_of(q, n_games):
    """P(win a best-of-n_games series) when each decisive game is won w.p. q (ties replayed)."""
    need = n_games // 2 + 1
    return sum(comb(n_games, k) * q**k * (1 - q) ** (n_games - k) for k in range(need, n_games + 1))


def p_relay(q, n):
    """Winner-stays relay, n vs n, iid matches: team that first collects n wins -> best-of-(2n-1)."""
    return p_best_of(q, 2 * n - 1)


def p_relay_bruteforce(q, n):
    @lru_cache(None)
    def f(a_left, b_left):
        if a_left == 0:
            return 0.0
        if b_left == 0:
            return 1.0
        return q * f(a_left, b_left - 1) + (1 - q) * f(a_left - 1, b_left)
    return f(n, n)


def p_team_majority(q_match, members=5):
    return p_best_of(q_match, members)


def decisive_multi(n):
    return 3 * (2**n - 2) / 3**n


@lru_cache(None)
def coord_A(m, k):
    """Rule A (only winners survive): best P(>=1 teammate survives k rounds) with coordinated splits."""
    if m == 0:
        return 0.0
    if k == 0:
        return 1.0
    best = 0.0
    for a in range(m + 1):
        for b in range(m - a + 1):
            c = m - a - b
            best = max(best, (coord_A(a, k - 1) + coord_A(b, k - 1) + coord_A(c, k - 1)) / 3)
    return best


@lru_cache(None)
def coord_B(m, k):
    """Rule B (winners+ties survive; the group whose hand loses is eliminated)."""
    if m == 0:
        return 0.0
    if k == 0:
        return 1.0
    best = 0.0
    for a in range(m + 1):
        for b in range(m - a + 1):
            c = m - a - b
            best = max(best, (coord_B(b + c, k - 1) + coord_B(a + c, k - 1) + coord_B(a + b, k - 1)) / 3)
    return best


def indep(m, k, p_survive_round):
    return 1 - (1 - p_survive_round**k) ** m


if __name__ == "__main__":
    print("== Series / relay amplification (q = P(win a decisive throw)) ==")
    for q in (0.50, 0.52, 0.55, 0.60):
        row = [p_best_of(q, 1), p_best_of(q, 3), p_best_of(q, 5)]
        relay = [p_relay(q, n) for n in (3, 5, 7)]
        assert all(abs(p_relay(q, n) - p_relay_bruteforce(q, n)) < 1e-12 for n in (3, 5, 7))
        maj_bo1 = p_team_majority(q, 5)
        maj_bo3 = p_team_majority(p_best_of(q, 3), 5)
        print(f"q={q:.2f} Bo1={row[0]:.3f} Bo3={row[1]:.3f} Bo5={row[2]:.3f} | relay3={relay[0]:.3f} relay5={relay[1]:.3f} relay7={relay[2]:.3f} | 5-member majority (Bo1 each)={maj_bo1:.3f} (Bo3 each)={maj_bo3:.3f}")

    print("\n== n-player simultaneous round decisive probability ==")
    for n in range(2, 11):
        print(f"n={n:2d}  P(decisive)={decisive_multi(n):.4f}  E[rounds]={1/decisive_multi(n):.2f}")

    print("\n== Everyone-vs-host: P(>=1 teammate survives k rounds) ==")
    for rule, coord, ps in (("A: only winners survive", coord_A, 1 / 3), ("B: winners+ties survive", coord_B, 2 / 3)):
        print(rule)
        for m in (3, 5, 10, 20):
            c = " ".join(f"{coord(m, k):.3f}" for k in range(1, 6))
            i = " ".join(f"{indep(m, k, ps):.3f}" for k in range(1, 6))
            print(f"  team={m:2d}  coordinated k1..5: {c}   independent: {i}")
