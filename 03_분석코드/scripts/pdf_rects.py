import sys, re
sys.path.insert(0, '/private/tmp/claude-501/-Users-baemanjin-orca-projects-----/9282a235-4fc4-4c50-add0-37a1d5aaa853/scratchpad/pylib')
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
pg = r.pages[0]
data = pg.get_contents().get_data().decode('latin-1')
# print rectangles and text
rects = re.findall(r'(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) re', data)
print('n rects', len(rects))
for x in rects[:80]:
    print(x)
txt = re.findall(r'\((.*?)\) ?Tj|\[(.*?)\] ?TJ', data)
print('texts', [a or b for a, b in txt][:80])
print(data[:1500])
