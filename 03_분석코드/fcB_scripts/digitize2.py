import sys
sys.path.insert(0, sys.argv[1])
from PIL import Image
import numpy as np
im = np.asarray(Image.open(sys.argv[2]).convert('L')).astype(int)
panels = {'F(a=1.1)':(55,425,445,700),'G(a=2)':(495,425,850,700),'H(a=4)':(905,425,1260,700),'I(a=9)':(1315,425,1670,700),'J(a=100)':(1725,425,2080,700)}
labels = ['W-','W0','W+','T-','T0','T+','L-','L0','L+']
for name,(x0,y0,x1,y1) in panels.items():
    p = im[y0:y1, x0:x1]
    H,W = p.shape
    dark = p < 90
    xr = 258; step = 38.5
    row = p[xr-6, :]
    # bar fill is mid-gray (not white, not black); outline black. find runs of non-white
    nonwhite = row < 235
    segs=[]; inseg=False
    for x in range(8, W):
        if nonwhite[x] and not inseg: s=x; inseg=True
        elif (not nonwhite[x]) and inseg:
            if x-s > 15: segs.append((s,x-1))
            inseg=False
    if inseg and W-s>15: segs.append((s,W-1))
    out=[]
    for (s,e) in segs:
        cols = range(s+1, e)
        top=None
        for y in range(5, xr-2):
            frac = dark[y, s+1:e].mean()
            if frac > 0.9:
                top=y; break
        # refine: bar top outline thickness ~2px; use center of the dark run
        if top is not None:
            y2=top
            while y2+1<xr and dark[y2+1, s+1:e].mean()>0.9: y2+=1
            topc=(top+y2)/2
            out.append(round((xr-topc)/(step*10),3))
        else: out.append(None)
    print(name, 'segments', len(segs), dict(zip(labels, out)))
