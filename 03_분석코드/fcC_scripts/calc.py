import math, statistics as st
def bo(p_win, p_loss, need):
    # first to `need` decisive wins; ties replayed
    q = p_win/(p_win+p_loss)
    tot=0.0
    for k in range(need):  # opponent wins k before you get need
        tot += math.comb(need-1+k, k) * q**need * (1-q)**k
    return tot
cases = {
 'Paper vs Roshambull full (W=R 33.99, L=S 31.20)': (0.3399,0.3120),
 'Scissors vs experienced (W=P 34.56, L=R 32.60)': (0.3456,0.3260),
 'Paper vs 36/32/32': (0.36,0.32),
 'Experienced humans W34.66 L33.17': (0.3466,0.3317),
 'Best response W41.66 L27.37': (0.4166,0.2737),
}
for k,(w,l) in cases.items():
    print(f"{k}: Bo3={bo(w,l,2):.4f} Bo5={bo(w,l,3):.4f}")
# Poisson shares tau=1.5 and 1.55
for tau in (1.5,1.55):
    ps=[math.exp(-tau)*tau**k/math.factorial(k) for k in range(4)]
    print(tau, [round(x*100,1) for x in ps], round((1-sum(ps))*100,1))
# CHC Table II taus
taus=[0.10,0.00,4.90,3.70,2.40,2.00,0.20,0.00,0.10,0.10,0.50,1.00,1.00,1.10,1.10,1.60,2.30,1.50,2.80,3.00,3.00,0.80,1.80,3.70]
print('n',len(taus),'mean',round(st.mean(taus),3),'median',st.median(taus))
# C10 repeat-rate counter: opponent repeats r, other two (1-r)/2 each; you throw the hand their last throw beats
for r in (0,0.12,0.2,0.25,0.3):
    win=(1-r)/2; tie=(1-r)/2; loss=r
    print('r',r,'EV',round(win-loss,3),'win share among decisive',round(win/(win+loss),3))
# SE of r
for n in (9,20):
    print('SE n',n, round(math.sqrt((1/3)*(2/3)/n),3))
# Wang 2020 Table 4 means
R,P,S=106.6098,96.29268,97.09756
print('sum',R+P+S,'pct',[round(x/3,2) for x in (R,P,S)], 'x41', [round(x*41,2) for x in (R,P,S)], 'x52',[round(x*52,2) for x in (R,P,S)])
sc=[10,41,8,34,73,43,48,43,59,24,9]
print('multi10 mean',round(st.mean(sc),3), round(st.mean(sc)/300,4))
