import sys, statistics as st
sys.path.insert(0, sys.argv[1])
import xlrd
sh = xlrd.open_workbook(sys.argv[2]).sheet_by_index(0)
rows = [sh.row_values(r) for r in range(5, sh.nrows) if sh.row_values(r)[0] != '']
items=['ROCK','PAPER','SCISSORS']; outs=['WIN','LOSE','DRAW']; strs=['STAY','UP','DOWN']
cell={}; col=12
for it in items:
    for o in outs:
        for s in strs:
            cell[(it,o,s)]=col; col+=1
# outcome marginals per participant: cols 6,7,8 = WIN, DRAW, LOSE
ocol={'WIN':6,'DRAW':7,'LOSE':8}
icol={'ROCK':1,'PAPER':2,'SCISSORS':3}
stay_pp=[]; draw_pp={s:[] for s in strs}
for r in rows:
    tot=0; acc={s:0.0 for s in strs}
    for it in items:
        for o in outs:
            w = r[icol[it]] * r[ocol[o]]  # approx joint (independence), normalised later
            for s in strs:
                acc[s] += w * r[cell[(it,o,s)]]
            tot += w
    stay_pp.append(acc['STAY']/tot)
    # after draw, weighted by item freq
    tw=0; dacc={s:0.0 for s in strs}
    for it in items:
        w=r[icol[it]]
        for s in strs: dacc[s]+=w*r[cell[(it,'DRAW',s)]]
        tw+=w
    for s in strs: draw_pp[s].append(dacc[s]/tw)
print("weighted overall P(stay) mean across participants: %.1f%% (SD %.1f, min %.1f, max %.1f)" % (st.mean(stay_pp)*100, st.stdev(stay_pp)*100, min(stay_pp)*100, max(stay_pp)*100))
print("participants with P(stay) < 1/3:", sum(1 for x in stay_pp if x < 1/3), "of", len(stay_pp))
print("after DRAW (item-weighted): " + ", ".join("%s=%.1f%%" % (s, st.mean(draw_pp[s])*100) for s in strs))
# second-order: P(stay n+2 | stay n+1) col 41
ss=[r[41] for r in rows]
print("P(stay|prev stay) mean: %.1f%%" % (st.mean(ss)*100))
three=[a*b for a,b in zip(stay_pp, ss)]
print("approx P(three same in a row) = P(stay)*P(stay|stay), mean across participants: %.1f%% (random 11.1%%)" % (st.mean(three)*100))
