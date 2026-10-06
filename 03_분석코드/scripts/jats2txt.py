import sys, re
import xml.etree.ElementTree as ET

def text_of(el):
    # Render element to text, handling inline math crudely
    parts = []
    def rec(e):
        tag = e.tag.split('}')[-1] if isinstance(e.tag, str) else ''
        if tag in ('xref',):
            parts.append((e.text or '') )
            for c in e:
                rec(c)
            if e.tail: parts.append(e.tail)
            return
        if tag == 'table-wrap':
            parts.append('\n[TABLE]\n')
        if e.text: parts.append(e.text)
        for c in e:
            rec(c)
        if tag in ('p','title','caption','label','tr','sec','table-wrap','fig','list-item','ref'):
            parts.append('\n')
        if tag in ('td','th'):
            parts.append(' | ')
        if e.tail: parts.append(e.tail)
    rec(el)
    return ''.join(parts)

def main(path):
    raw = open(path, encoding='utf-8').read()
    raw = re.sub(r'<!DOCTYPE[^>]*>', '', raw)
    root = ET.fromstring(raw)
    out = text_of(root)
    out = re.sub(r'[ \t]+', ' ', out)
    out = re.sub(r'\n\s*\n+', '\n\n', out)
    print(out)

if __name__ == '__main__':
    main(sys.argv[1])
