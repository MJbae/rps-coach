import re, sys, zlib
for path in sys.argv[1:]:
    data = open(path, 'rb').read()
    txt = ''
    for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
        try: txt += zlib.decompress(m.group(1)).decode('latin-1')
        except Exception: pass
    bars = re.findall(r'([\d.]+) 475 155 ([\d.]+) re', txt)
    # three colour groups in order: first 7 = '-', next 7 = '0', next 7 = '+'
    vals = [round(float(h)/3520.83, 3) for x, h in bars]
    labels = ['1', '1.1', '2', '4', '9', '100', 'inf']
    print(path.split('/')[-1])
    for i, lab in enumerate(labels):
        print('  a=%-4s  -: %.3f  0: %.3f  +: %.3f' % (lab, vals[i], vals[7+i], vals[14+i]))
