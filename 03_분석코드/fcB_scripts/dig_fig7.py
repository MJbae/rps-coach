import sys
sys.path.insert(0, sys.argv[1])
from PIL import Image
import numpy as np
im = Image.open(sys.argv[2]).convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
# page at 400 dpi: 612x792 pt -> 3400x4400 px. Figure 7 occupies roughly y 250..560 of the 150dpi render (1275x1650) -> scale 400/150
s = 400/150
y0,y1 = int(240*s), int(560*s); x0,x1 = int(420*s), int(900*s)
sub = a[y0:y1, x0:x1]
r,g,b = sub[...,0],sub[...,1],sub[...,2]
# axis: find black horizontal line (x-axis) = row with most near-black pixels
blk = (r<60)&(g<60)&(b<60)
rows = blk.sum(axis=1)
cand = [y for y in range(len(rows)) if rows[y] > 0.5*sub.shape[1]]; xaxis = max(cand)
# y-axis tick labels: find the top frame line (y=1) = first row from top with many black pixels
top = min(cand)
print('xaxis row', xaxis, 'top frame row', top)
scale = xaxis - top  # pixels per 1.0
# classify colors
darkgreen = (r<40)&(g>100)&(g<150)&(b>80)&(b<130)
lightgreen = (r>100)&(r<150)&(g>170)&(b<120)
yellow = (r>230)&(g>230)&(b<140)
def bars(mask, name):
    cols = mask.sum(axis=0)
    xs = np.where(cols>5)[0]
    segs=[]; 
    if len(xs)==0: return []
    s0=xs[0]; prev=xs[0]
    for x in xs[1:]:
        if x-prev>3: segs.append((s0,prev)); s0=x
        prev=x
    segs.append((s0,prev))
    out=[]
    for (u,v) in segs:
        if v-u < 10: continue
        c = (u+v)//2
        colmask = mask[:, u+3:v-3].any(axis=1)
        ys = np.where(colmask)[0]
        topy = ys.min()
        out.append(round((xaxis - topy)/scale,3))
    return out
print('T- (dark green):', bars(darkgreen,'T-'))
print('T0 (light green):', bars(lightgreen,'T0'))
print('T+ (yellow):', bars(yellow,'T+'))
