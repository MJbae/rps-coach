import csv, collections, sys
# usage: python3 -I us_first_throws.py rps_v1_data.csv rps_v2_data.csv rps_v3_data.csv
def first_moves(path, has_bot):
    c=collections.Counter()
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            if row['round_index']!='1': continue
            if has_bot and row.get('is_bot')!='0': continue
            c[row['player_move']]+=1
    return c
tot=collections.Counter()
for label, path, hb in [('v1 dyads', sys.argv[1], False), ('v2 fixed bots', sys.argv[2], True), ('v3 adaptive bots', sys.argv[3], True)]:
    c=first_moves(path, hb); valid={m:c[m] for m in ('rock','paper','scissors')}; n=sum(valid.values()); tot.update(valid)
    print(label, 'n', n, {m: round(v/n,3) for m,v in valid.items()}, 'excluded', {m:v for m,v in c.items() if m not in valid})
n=sum(tot.values()); print('pooled n', n, {m: round(v/n,3) for m,v in tot.items()}, 'chi2', round(sum((v-n/3)**2/(n/3) for v in tot.values()),2))
