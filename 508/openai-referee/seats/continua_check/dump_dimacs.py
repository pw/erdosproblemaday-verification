import sys
sys.path.insert(0, '.')
from planar_cover_sat import encode, disk_cells, rect_cells
for tag, cells, h, m in [('disk3_h05_m2', disk_cells(3.0, 0.5), 0.5, 2),
                         ('disk26_h033_m2', disk_cells(2.6, 1/3), 1/3, 2),
                         ('disk26_h033_m3', disk_cells(2.6, 1/3), 1/3, 3),
                         ('strip_h05_m2', rect_cells(6.0, 1.5, 0.5), 0.5, 2)]:
    D2 = round((2.0/h)**2)
    _, _, _, pool, cl = encode(cells, D2, m)
    nv = max(abs(l) for c in cl for l in c)
    with open(f'{tag}.cnf', 'w') as f:
        f.write(f'p cnf {nv} {len(cl)}\n')
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    print(tag, nv, len(cl))
