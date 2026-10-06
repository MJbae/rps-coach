import sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-baemanjin-orca-projects-----/9282a235-4fc4-4c50-add0-37a1d5aaa853/scratchpad/pylib')
import xlrd
wb = xlrd.open_workbook(sys.argv[1])
maxrows = int(sys.argv[2]) if len(sys.argv) > 2 else 60
for sh in wb.sheets():
    print('=== SHEET', sh.name, sh.nrows, 'x', sh.ncols)
    for r in range(min(sh.nrows, maxrows)):
        vals = []
        for c in range(sh.ncols):
            v = sh.cell_value(r, c)
            if isinstance(v, float):
                v = f"{v:.4g}"
            vals.append(str(v))
        print(r, '\t'.join(vals))
