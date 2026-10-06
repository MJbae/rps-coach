# Conditional next-hand distributions of the OPPONENT given the opponent's own previous outcome.
# s = repeat own previous hand X; u = "upgrade" to X+ (hand that beats X); d = "downgrade" to X- (hand X beats).
data = {
 'Wang2014 a=1.1 (EPS)': {'W': (0.568, 0.181, 0.250), 'T': (0.602, 0.254, 0.144), 'L': (0.310, 0.364, 0.325)},
 'Wang2014 a=2 (EPS)':   {'W': (0.528, 0.226, 0.247), 'T': (0.432, 0.334, 0.234), 'L': (0.360, 0.276, 0.365)},
 'Wang2014 a=4 (EPS)':   {'W': (0.504, 0.205, 0.291), 'T': (0.388, 0.382, 0.230), 'L': (0.340, 0.280, 0.379)},
 'Wang2014 a=9 (EPS)':   {'W': (0.448, 0.258, 0.293), 'T': (0.358, 0.349, 0.292), 'L': (0.303, 0.283, 0.414)},
 'Wang2014 a=100 (EPS)': {'W': (0.453, 0.232, 0.315), 'T': (0.364, 0.367, 0.269), 'L': (0.343, 0.261, 0.397)},
 'Dyson2016 (xls, mean of item cells)': {'W': (0.357, 0.307, 0.336), 'T': (0.275, 0.401, 0.324), 'L': (0.223, 0.372, 0.405)},
 'Forder&Dyson2016 (text)': {'W': (0.4245, 0.2932, 0.2823), 'T': (0.2928, 0.3732, 0.3340), 'L': (0.2146, 0.3913, 0.3941)},
 'WangL2020 humans vs AI (raw, mean of players)': {'W': (0.469, 0.284, 0.248), 'T': (0.394, 0.303, 0.303), 'L': (0.375, 0.320, 0.305)},
}
def opts(s, u, d):
    return {'X+ (beat their last hand)': s - d, 'X- (beat their upgrade)': u - s, 'X (beat their downgrade)': d - u}
for name, D in data.items():
    print('==', name)
    best_tot = 0; rules = {'always X+ (Cournot BR to their last hand)': 0, 'self-downgrade rule': 0}
    for o in 'WTL':
        s, u, d = D[o]
        e = opts(s, u, d)
        b = max(e, key=e.get)
        best_tot += e[b] / 3
        rules['always X+ (Cournot BR to their last hand)'] += e['X+ (beat their last hand)'] / 3
        sd = {'W': e['X+ (beat their last hand)'], 'L': e['X (beat their downgrade)'], 'T': e['X- (beat their upgrade)']}[o]
        rules['self-downgrade rule'] += sd / 3
        print('  opp prev outcome %s: stay %.3f up %.3f down %.3f | edges: %s | best=%s (%+.3f)' % (
            o, s, u, d, ', '.join('%s %+.3f' % (k.split(' ')[0], v) for k, v in e.items()), b.split(' ')[0], e[b]))
    print('  equal-weight mean edge: per-outcome best %+.3f | %s' % (best_tot, ' | '.join('%s %+.3f' % (k, v) for k, v in rules.items())))
