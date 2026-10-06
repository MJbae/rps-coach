import sys
sys.path.insert(0, sys.argv[1])
import xlrd
wb = xlrd.open_workbook(sys.argv[2])
sh = wb.sheet_by_index(0)
rows = []
for r in range(5, sh.nrows):
    v = [sh.cell_value(r, c) for c in range(sh.ncols)]
    if v[0] == '' or not isinstance(v[0], float):
        print("skip row", r, v[:5]); continue
    rows.append(v)
print("N participants:", len(rows))
items = ['ROCK','PAPER','SCISSORS']; outs = ['WIN','LOSE','DRAW']; strat = ['STAY','UP','DOWN']
def col(item, out, s):
    return 12 + items.index(item)*9 + outs.index(out)*3 + strat.index(s)
mean = lambda xs: sum(xs)/len(xs)
# item proportions
for k, nm in zip([1,2,3], items):
    print(nm, "mean prop %.4f" % mean([r[k] for r in rows]))
for k, nm in zip([6,7,8], ['WIN','DRAW','LOSE']):
    print(nm, "mean prop %.4f" % mean([r[k] for r in rows]))
# check blanks
blank = sum(1 for r in rows for c in range(12,39) if r[c]=='' )
print("blank cells in first-order:", blank)
# per tied hand, mean across participants
res = {}
for it in items:
    vals = {}
    for s in strat:
        xs = [r[col(it,'DRAW',s)] for r in rows if r[col(it,'DRAW',s)] != '']
        vals[s] = mean(xs)
    res[it] = vals
    print("after DRAW on", it, {k: round(100*v,1) for k,v in vals.items()}, "n=", len(xs))
# unweighted mean over the three hands
for s in strat:
    print("DRAW unweighted-hand mean", s, round(100*mean([res[it][s] for it in items]),1))
# weighted by each participant's item proportion (approx number of draw trials with that item ~ prop*225/3)
for s in strat:
    num = 0; den = 0
    for r in rows:
        for it, k in zip(items, [1,2,3]):
            c = r[col(it,'DRAW',s)]
            if c == '': continue
            w = r[k]
            num += w*c; den += w
    print("DRAW item-weighted pooled", s, round(100*num/den,1))
# same for WIN and LOSE
for out in ['WIN','LOSE']:
    for s in strat:
        num = 0; den = 0
        for r in rows:
            for it, k in zip(items, [1,2,3]):
                c = r[col(it,out,s)]
                if c == '': continue
                w = r[k]; num += w*c; den += w
        print(out, "item-weighted pooled", s, round(100*num/den,1))
# overall stay rate per participant, weighting cells by item prop * outcome prop (approx)
stays = []
for r in rows:
    num=0; den=0
    for it,k in zip(items,[1,2,3]):
        for out,ko in zip(['WIN','LOSE','DRAW'],[6,8,7]):
            c = r[col(it,out,'STAY')]
            if c=='': continue
            w = r[k]*r[ko]
            num += w*c; den += w
    stays.append(num/den)
print("overall stay mean %.3f, min %.3f, max %.3f, n<1/3: %d" % (mean(stays), min(stays), max(stays), sum(1 for x in stays if x<1/3)))
# second-order
so = {}
for i, s1 in enumerate(strat):
    for j, s2 in enumerate(strat):
        c = 41 + i*3 + j
        xs = [r[c] for r in rows if r[c] != '']
        so[(s1,s2)] = mean(xs)
for s1 in strat:
    print("after", s1, {s2: round(100*so[(s1,s2)],1) for s2 in strat})
