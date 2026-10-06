"""Exact check: simultaneous team-vs-team RPS (Cho's rules) with team A using a fixed composition, team B random.
Hands: 0=Rock, 1=Paper, 2=Scissors. h beats (h-1)%3 ... i.e. Paper(1) beats Rock(0), Scissors(2) beats Paper(1), Rock(0) beats Scissors(2).
Rule I : decisive (exactly 2 hand types) -> team with more winners wins; equal -> the winners replay.
Rule II: decisive -> if all winners are from one team, that team wins; otherwise only the winners replay.
Non-decisive throws are replayed by the same players.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product

BEATS = {1: 0, 2: 1, 0: 2}  # key beats value


def winning_hand(types):
    a, b = sorted(types)
    return a if BEATS[a] == b else b


def comp(policy, n):
    """Team A's hands for n players (X = Rock w.l.o.g.; random X is symmetric)."""
    if policy == "random":
        return None
    X, beaten_by_X, beats_X = 0, 2, 1
    if n == 1:
        return None  # a lone player just randomizes
    if policy == "two_on_X_one_on_what_X_beats":
        return [X] * (n - 1) + [beaten_by_X]
    if policy == "reverse":
        return [X] * (n - 1) + [beats_X]
    if policy == "herd":
        return [X] * n
    if policy == "two_hands_split":
        return [X if i % 2 == 0 else beaten_by_X for i in range(n)]
    raise ValueError(policy)


def outcomes(a_hands_options, b):
    for a_hands, pa in a_hands_options:
        for b_hands in product(range(3), repeat=b):
            yield a_hands, list(b_hands), pa * Fraction(1, 3**b)


@lru_cache(None)
def V(a, b, rule, policy):
    fixed = comp(policy, a)
    a_opts = [(fixed, Fraction(1))] if fixed is not None else [(list(h), Fraction(1, 3**a)) for h in product(range(3), repeat=a)]
    p_replay, acc = Fraction(0), Fraction(0)
    for a_hands, b_hands, p in outcomes(a_opts, b):
        types = set(a_hands) | set(b_hands)
        if len(types) != 2:
            p_replay += p
            continue
        w = winning_hand(types)
        wa, wb = a_hands.count(w), b_hands.count(w)
        if rule == "I":
            if wa > wb:
                acc += p
            elif wa == wb:
                acc += p * V(wa, wb, rule, policy)
        else:
            if wb == 0:
                acc += p
            elif wa == 0:
                pass
            else:
                acc += p * V(wa, wb, rule, policy)
    return acc / (1 - p_replay)


if __name__ == "__main__":
    for n in (2, 3, 4):
        for rule in ("I", "II"):
            row = []
            for pol in ("random", "two_on_X_one_on_what_X_beats", "reverse", "herd", "two_hands_split"):
                row.append(f"{pol}={float(V(n, n, rule, pol)):.4f}")
            print(f"{n}v{n} rule {rule}: " + "  ".join(row))
