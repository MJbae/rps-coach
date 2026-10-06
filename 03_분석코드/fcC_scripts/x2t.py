import sys, re
import xml.etree.ElementTree as ET
t = ET.parse(sys.argv[1]).getroot()
out=[]
def walk(e, depth=0):
    tag = e.tag.split('}')[-1]
    if tag in ('ref-list',): return
    txt = (e.text or '')
    if tag in ('p','title','caption','td','th','label','abstract','article-title'):
        s = ''.join(e.itertext())
        s = re.sub(r'\s+',' ', s).strip()
        if s: out.append(('## ' if tag=='title' else '')+s)
        return
    for c in e: walk(c, depth+1)
walk(t)
open(sys.argv[2],'w').write('\n'.join(out))
