import sys
sys.path.insert(0, sys.argv[1])
import xlrd
wb = xlrd.open_workbook(sys.argv[2])
for sh in wb.sheets():
    print("=== SHEET", sh.name, sh.nrows, sh.ncols)
    maxr = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    for r in range(min(sh.nrows, maxr)):
        print(r, [sh.cell_value(r, c) for c in range(sh.ncols)])
