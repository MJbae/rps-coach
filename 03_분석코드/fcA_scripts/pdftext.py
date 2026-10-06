import sys
sys.path.insert(0, sys.argv[1])
from pypdf import PdfReader
r = PdfReader(sys.argv[2])
out = []
for i, p in enumerate(r.pages):
    out.append('\n=== PAGE %d ===\n' % (i+1) + (p.extract_text() or ''))
open(sys.argv[3], 'w').write(''.join(out))
print(len(r.pages), 'pages')
