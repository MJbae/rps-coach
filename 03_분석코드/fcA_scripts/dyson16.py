import sys, math
sys.path.insert(0, sys.argv[1])
import xlrd
wb = xlrd.open_workbook(sys.argv[2])
sh = wb.sheet_by_index(0)
rows = []
for r in range(5, sh.nrows):
    v = sh.cell_value(r, 0)
    if isinstance(v, float) and v >= 1:
        rows.append([sh.cell_value(r, c) for c in range(sh.ncols)])
print('n participants rows:', len(rows), 'ids', [int(x[0]) for x in rows])
def mean(xs): return sum(xs)/len(xs)
def sem(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))/math.sqrt(len(xs))
print('Item R P S:', [round(mean([x[c] for x in rows]),4) for c in (1,2,3)])
print('Outcome W D L (cols 6,7,8):', [round(mean([x[c] for x in rows]),4) for c in (6,7,8)])
# first-order: items R,P,S at base 12, 21, 30; outcomes W,L,D at offsets 0,3,6; strategies STAY,UP,DOWN offsets 0,1,2
items = {'R':12,'P':21,'S':30}
outs = {'W':0,'L':3,'D':6}
strat = {'stay':0,'up':1,'down':2}
for o, oo in outs.items():
    res = {}
    for s, so in strat.items():
        per = []
        for x in rows:
            vals = [x[b+oo+so] for b in items.values() if x[b+oo+so] != '']
            per.append(mean(vals))
        res[s] = (round(mean(per),4), round(sem(per),4))
    print('outcome', o, res)
# check blanks
blank = sum(1 for x in rows for c in range(12,39) if x[c] == '')
print('blank cells in first-order:', blank)
# second-order
sec = {}
for s1, b in (('stay',41),('up',44),('down',47)):
    for s2, o in (('stay',0),('up',1),('down',2)):
        per = [x[b+o] for x in rows if x[b+o] != '']
        sec[s1+'->'+s2] = (round(mean(per),4), round(sem(per),4), len(per))
print(sec)
# per item x outcome means
for it, b in items.items():
    for o, oo in outs.items():
        print(it, o, [round(mean([x[b+oo+so] for x in rows if x[b+oo+so] != '']),4) for so in (0,1,2)])
