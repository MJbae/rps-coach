import re, sys, zlib
path = sys.argv[1]
data = open(path, 'rb').read()
out = []
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
    raw = m.group(1)
    try:
        dec = zlib.decompress(raw)
    except Exception:
        try:
            dec = zlib.decompressobj().decompress(raw)
        except Exception:
            dec = raw
    out.append(dec)
for i, d in enumerate(out):
    print('==== stream', i, len(d))
    print(d.decode('latin-1')[:int(sys.argv[2]) if len(sys.argv) > 2 else 20000])
