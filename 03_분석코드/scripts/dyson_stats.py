import sys, statistics as st
sys.path.insert(0, sys.argv[1])
import xlrd
wb = xlrd.open_workbook(sys.argv[2])
sh = wb.sheet_by_index(0)
rows = []
for r in range(5, sh.nrows):
    v = sh.row_values(r)
    if v[0] == '' : continue
    rows.append(v)
print("N participants:", len(rows))
def m(col):
    vals=[r[col] for r in rows if r[col] != '']
    return st.mean(vals), len(vals)
print("Item n (R,P,S):", [round(m(c)[0]*100,2) for c in (1,2,3)])
print("Outcome n (WIN,DRAW,LOSE):", [round(m(c)[0]*100,2) for c in (6,7,8)])
items=['ROCK','PAPER','SCISSORS']; outs=['WIN','LOSE','DRAW']; strs=['STAY','UP','DOWN']
col=12
cell={}
for it in items:
    for o in outs:
        for s in strs:
            cell[(it,o,s)]=col; col+=1
print("last first-order col:", col-1)
# per-cell means across participants
for it in items:
    for o in outs:
        vals=[ (m(cell[(it,o,s)])) for s in strs]
        print(f"{it:8s} {o:4s} ->", "  ".join(f"{s}={v[0]*100:.1f}%(n={v[1]})" for s,v in zip(strs,vals)))
# collapsed by outcome: per participant mean over items, then mean over participants
print("--- collapsed over item (mean of per-participant item-averaged proportions) ---")
for o in outs:
    res=[]
    for s in strs:
        pp=[]
        for r in rows:
            vals=[r[cell[(it,o,s)]] for it in items if r[cell[(it,o,s)]] != '']
            if vals: pp.append(st.mean(vals))
        res.append((s, st.mean(pp)*100, st.stdev(pp)*100, len(pp)))
    print(o, "  ".join(f"{s}={mu:.1f}% (SD {sd:.1f}, n={n})" for s,mu,sd,n in res))
print("--- collapsed over outcome (by item) ---")
for it in items:
    res=[]
    for s in strs:
        pp=[]
        for r in rows:
            vals=[r[cell[(it,o,s)]] for o in outs if r[cell[(it,o,s)]] != '']
            if vals: pp.append(st.mean(vals))
        res.append((s, st.mean(pp)*100))
    print(it, "  ".join(f"{s}={mu:.1f}%" for s,mu in res))
print("--- overall (mean of 9 item x outcome cells) ---")
for s in strs:
    pp=[]
    for r in rows:
        vals=[r[cell[(it,o,s)]] for it in items for o in outs if r[cell[(it,o,s)]] != '']
        pp.append(st.mean(vals))
    print(s, f"{st.mean(pp)*100:.1f}%")
# second order
print("--- second-order (strategy n->n+1 x strategy n+1->n+2) ---")
c=41
for s1 in strs:
    vals=[m(c+i) for i in range(3)]
    print("prev", s1, "->", "  ".join(f"{s}={v[0]*100:.1f}%" for s,v in zip(strs,vals)))
    c+=3
