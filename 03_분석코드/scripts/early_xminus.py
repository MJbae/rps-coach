import csv, sys, os, collections, math
# returns per-player sequences of hands (strings) for US v1 and AU Moerel
UP={'rock':'paper','paper':'scissors','scissors':'rock'}; DOWN={v:k for k,v in UP.items()}
def res(me, op):
    if me==op: return 0
    return 1 if DOWN[me]==op else -1
def summarize(label, seqs, lo, hi):
    per_minus=[]; per_plus=[]; per_rep=[]
    for s in seqs:
        pm=pp=n=rep=0
        for i in range(lo, min(hi, len(s))):
            a,b=s[i-1], s[i]
            if a not in UP or b not in UP: continue
            pm+=res(DOWN[a], b); pp+=res(UP[a], b); rep+=(a==b); n+=1
        if n: per_minus.append(pm/n); per_plus.append(pp/n); per_rep.append(rep/n)
    def ms(x):
        m=sum(x)/len(x); se=math.sqrt(sum((v-m)**2 for v in x)/(len(x)-1))/math.sqrt(len(x)); return m,se
    print(f'{label}: players {len(per_minus)}; repeat {ms(per_rep)[0]:.3f} ({ms(per_rep)[1]:.3f}); always X- {ms(per_minus)[0]:+.3f} ({ms(per_minus)[1]:.3f}); always X+ {ms(per_plus)[0]:+.3f} ({ms(per_plus)[1]:.3f})')
# US v1
rows=collections.defaultdict(lambda: collections.defaultdict(dict))
with open(sys.argv[1], newline='') as f:
    for r in csv.DictReader(f):
        rows[r['game_id']][r['player_id']][int(r['round_index'])]=r['player_move']
us=[]
for g,ps in rows.items():
    if len(ps)!=2: continue
    if not all(len(v)==300 for v in ps.values()): continue
    for p,d in ps.items(): us.append([d[i] for i in range(1,301)])
# AU Moerel
base=sys.argv[2]; NAME={'1':'rock','2':'paper','3':'scissors','0':'none'}
au=[]
for fn in sorted(os.listdir(os.path.join(base,'events'))):
    rr=list(csv.DictReader(open(os.path.join(base,'events',fn)), delimiter='\t'))
    for k in ['player1_resp','player2_resp']: au.append([NAME[x[k]] for x in rr])
for lab, seqs in [('US dyads (Brockbank & Vul 2020 raw)', us), ('AU pairs (Moerel 2025 raw)', au)]:
    summarize(lab+' rounds 2-10', seqs, 1, 10)
    summarize(lab+' all rounds', seqs, 1, 10**6)
