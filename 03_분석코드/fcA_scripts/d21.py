# Dyson 2021 Table 2: per experiment, 3 credit conditions; each with Win/Lose/Draw columns; rows stay/up/down
T = {
 'Exp1': {'stay': [(0.376,0.234,0.294),(0.384,0.220,0.302),(0.357,0.246,0.294)],
          'up':   [(0.329,0.385,0.380),(0.316,0.390,0.372),(0.345,0.367,0.346)],
          'down': [(0.295,0.382,0.327),(0.300,0.390,0.326),(0.298,0.388,0.360)]},
 'Exp2': {'stay': [(0.295,0.220,0.276),(0.338,0.186,0.251),(0.271,0.189,0.262)],
          'up':   [(0.337,0.379,0.326),(0.341,0.382,0.384),(0.364,0.383,0.362)],
          'down': [(0.368,0.401,0.398),(0.321,0.433,0.366),(0.365,0.428,0.376)]},
 'Exp3': {'stay': [(0.463,0.225,0.350),(0.439,0.257,0.307),(0.415,0.302,0.360)],
          'up':   [(0.288,0.370,0.363),(0.285,0.343,0.365),(0.292,0.316,0.325)],
          'down': [(0.250,0.405,0.286),(0.376,0.400,0.327),(0.293,0.382,0.315)]},
}
for e, d in T.items():
    avg = {s: [sum(c[i] for c in d[s])/3 for i in range(3)] for s in d}  # i: 0 win,1 lose,2 draw
    W = (avg['stay'][0], avg['up'][0], avg['down'][0]); L = (avg['stay'][1], avg['up'][1], avg['down'][1]); D = (avg['stay'][2], avg['up'][2], avg['down'][2])
    eXp = lambda s,u,dn: s-dn; eX = lambda s,u,dn: dn-u; eXm = lambda s,u,dn: u-s
    print(e, 'W', [round(x,3) for x in W], 'L', [round(x,3) for x in L], 'D', [round(x,3) for x in D])
    print('   oppLost: repeat-winner X+ %+.3f | loser-hand X %+.3f | X- %+.3f' % (eXp(*L), eX(*L), eXm(*L)))
    print('   oppWon: beat-winner X+ %+.3f | tie: X+ %+.3f X- %+.3f | self-downgrade avg %+.3f' % (eXp(*W), eXp(*D), eXm(*D), (eXp(*W)+eX(*L)+eXm(*D))/3))
