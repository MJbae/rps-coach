import sys, csv, glob, os
from collections import Counter, defaultdict
beats = {'R':'S','P':'R','S':'P'}; beaten_by = {v:k for k,v in beats.items()}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'per_player_draw2.py')).read().split('def per(')[0])
def result(me, opp):
    if me==opp: return 0
    return 1 if beats[me]==opp else -1
def evaluate(players, name):
    # players: list of [(own, opp)] sequences; we evaluate rules as if we were the opponent of 'own' sequence
    rules = {
      'throw hand their last throw beats': lambda X: beats[X],
      'repeat their last throw': lambda X: X,
      'throw hand that beats their last throw': lambda X: beaten_by[X],
    }
    for cond in [None,'D']:
        for rn, f in rules.items():
            tot=0; n=0
            for p in players:
                for t in range(len(p)-1):
                    own,opp = p[t]; nxt = p[t+1][0]
                    if not own or not opp or not nxt: continue
                    if cond=='D' and own!=opp: continue
                    tot += result(f(own), nxt); n+=1
            print(name, 'cond', cond or 'ANY', '|', rn, ': net %.1f pp (n=%d)' % (100*tot/n, n))
evaluate(load_moerel(sys.argv[1]), 'Moerel')
evaluate(load_brock(sys.argv[2]), 'Brockbank')
