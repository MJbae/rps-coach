import csv, sys, glob, os, math
from collections import defaultdict
sys.path.insert(0, sys.argv[1])
UP = {'R': 'P', 'P': 'S', 'S': 'R'}
DN = {'R': 'S', 'P': 'R', 'S': 'P'}
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
def res(a, b):
    if a == b: return 0
    return 1 if BEATS[a] == b else -1
def mean(xs): return sum(xs)/len(xs)
def sem(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))/math.sqrt(len(xs))
# pairs: list of (target_seq, me_seq); evaluate strategies predicting target's move at t+1
def evaluate(pairs, label):
    strat = {
     'other X- (lose to opp last)': lambda P, Q: DN[P],
     'Cournot X+ (beat opp last)': lambda P, Q: UP[P],
     'copy opp last X': lambda P, Q: P,
     'self-downgrade (my last beats)': lambda P, Q: DN[Q],
     'self-stay (repeat my last)': lambda P, Q: Q,
     'self-upgrade': lambda P, Q: UP[Q],
    }
    out = {}
    for name, f in strat.items():
        per = []
        for P, Q in pairs:
            s = []
            for t in range(len(P)-1):
                if P[t] and Q[t] and P[t+1]:
                    s.append(res(f(P[t], Q[t]), P[t+1]))
            per.append(mean(s))
        out[name] = (mean(per), sem(per), len(per))
    print('==', label)
    for k, v in out.items():
        print(f"   {k:32s} edge={v[0]:+.3f} (SEM {v[1]:.3f}, n={v[2]})")
# US dyads
M = {'rock': 'R', 'paper': 'P', 'scissors': 'S'}
rows = list(csv.DictReader(open(sys.argv[2])))
games = defaultdict(lambda: defaultdict(dict))
for r in rows: games[r['game_id']][r['player_id']][int(r['round_index'])] = M.get(r['player_move'])
pairs = []
for g, pl in games.items():
    ids = list(pl)
    if len(ids) != 2 or any(len(pl[i]) != 300 for i in ids): continue
    a = [pl[ids[0]][t] for t in range(1, 301)]; b = [pl[ids[1]][t] for t in range(1, 301)]
    pairs += [(a, b), (b, a)]
evaluate(pairs, 'US dyads (Brockbank & Vul 2020)')
# AU dyads
N = {'1': 'R', '2': 'P', '3': 'S'}
pairs = []
for f in sorted(glob.glob(os.path.join(sys.argv[3], '*_events.tsv'))):
    rr = list(csv.DictReader(open(f), delimiter='\t'))
    a = [N.get(r['player1_resp']) for r in rr]; b = [N.get(r['player2_resp']) for r in rr]
    pairs += [(a, b), (b, a)]
evaluate(pairs, 'AU dyads (Moerel et al. 2025)')
# Wang L 2020 humans vs AI: target = human, me = AI's actual move
import openpyxl
pairs = []
for path in sys.argv[4:]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        rws = list(ws.iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(rws) if r[0] and isinstance(r[0], str) and 'Round number' in r[0])
        mcol = next(j for j, h in enumerate(rws[hi]) if h and 'Multi AI played' in str(h))
        data = [r for r in rws[hi+1:] if isinstance(r[0], (int, float))]
        pairs.append(([str(r[1]).strip() for r in data], [str(r[mcol]).strip() for r in data]))
evaluate(pairs, 'Wang L 2020 humans (vs multi-AI)')
