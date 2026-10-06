import sys
sys.path.insert(0, sys.argv[1])
from PIL import Image
im = Image.open(sys.argv[2])
x0,y0,x1,y1 = map(int, sys.argv[3:7])
scale = float(sys.argv[7])
c = im.crop((x0,y0,x1,y1))
c = c.resize((int((x1-x0)*scale), int((y1-y0)*scale)), Image.LANCZOS)
c.save(sys.argv[8])
print(c.size)
