import sys
sys.path.insert(0, sys.argv[1])
from PIL import Image
import numpy as np
im = np.asarray(Image.open(sys.argv[2]).convert('L')).astype(int)
panels = {'F(a=1.1)':(55,425,445,700),'G(a=2)':(495,425,850,700),'H(a=4)':(905,425,1260,700),'I(a=9)':(1315,425,1670,700),'J(a=100)':(1725,425,2080,700)}
for name,(x0,y0,x1,y1) in panels.items():
    p = im[y0:y1, x0:x1]
    H,W = p.shape
    dark = p < 80
    # y-axis: column with longest dark vertical run
    colsum = dark.sum(axis=0)
    ax = int(np.argmax(colsum[:W//3]))
    # x-axis: row with most dark pixels
    rowsum = dark.sum(axis=1)
    xr = int(np.argmax(rowsum))
    # ticks: rows where pixels just right of axis are dark (ticks extend right)
    tick = [y for y in range(H) if dark[y, ax+4:ax+12].sum() >= 6 and y < xr-3]
    # group tick rows
    groups=[]
    for y in tick:
        if groups and y-groups[-1][-1] <= 2: groups[-1].append(y)
        else: groups.append([y])
    tickc = [np.mean(g) for g in groups]
    # bars: along a row 10px above x-axis, find segments of non-white columns between dark outlines
    row = p[xr-8, :]
    nonwhite = row < 235
    segs=[]; inseg=False
    for x in range(ax+3, W):
        if nonwhite[x] and not inseg: s=x; inseg=True
        elif not nonwhite[x] and inseg:
            if x-s > 15: segs.append((s,x-1))
            inseg=False
    if inseg and W-s>15: segs.append((s,W-1))
    print(name, 'axis_x', ax, 'xaxis_y', xr, 'ticks', [round(t,1) for t in tickc])
    # scale: assume ticks are at 0.1 steps; x-axis = 0
    if len(tickc) >= 2:
        steps = np.diff(tickc)
        step = float(np.median(steps))
    vals=[]
    for (s,e) in segs:
        xs = s+4  # just inside left edge
        col = dark[:, xs]
        # first dark pixel from top above x-axis
        top = next((y for y in range(0, xr-2) if col[y]), None)
        vals.append(round((xr - top)/ (step*10), 3) if top is not None else None)
    print('   bars(px step %.2f):' % step, vals)
