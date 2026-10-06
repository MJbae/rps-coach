import sys
from PIL import Image
src, out, x0, y0, x1, y1, scale = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8])
im = Image.open(src).convert('RGB')
c = im.crop((x0, y0, x1, y1))
c = c.resize(((x1-x0)*scale, (y1-y0)*scale), Image.LANCZOS)
c.save(out)
print(im.size, c.size)
