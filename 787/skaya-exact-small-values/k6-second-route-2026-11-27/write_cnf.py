"""Write a formula of part (b) as DIMACS for the kissat / cadical binaries (proof-logged runs).
Clauses: our base encoding (+ our order atoms if ORDER_ATOMS=1), archive cores certified by our checker, our extra cores,
then unit clauses for the case (and task, if given).  Prints the 1-based clause-id ranges (for mapping an LRAT proof).
Usage: write_cnf.py OUT.cnf [CASE [ULOW UHIGH]]     (CASE / ULOW / UHIGH = None or an index)"""
import sys, os, json
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/787/check')
from sat_close import base_clauses, load_cores, case_assumptions, NV, TRIP, TID, s
from sat_tasks import tasks_for_case

def order_atoms():
    def g(i, j, l): return NV + 1 + TID[(i, j, l)]
    oc = []
    for (i, j, l) in TRIP:
        oc.append([-s(i, j, l), -g(i, j, l)])
        succ = []
        if l - 1 > j: succ.append((i, j, l - 1))
        if i + 1 < j: succ.append((i + 1, j, l))
        if j + 1 < l: succ.append((i, j + 1, l))
        for t2 in succ:
            oc.append([-s(i, j, l), g(*t2)]); oc.append([-g(i, j, l), g(*t2)])
    return oc

def main():
    out = sys.argv[1]
    P = lambda a: None if a == 'None' else int(a)
    base, nb, no = base_clauses()
    nv = NV
    if os.environ.get('ORDER_ATOMS', '0') == '1':
        base = base + order_atoms(); nv = NV + len(TRIP)
    cores, extra = load_cores()
    units = []
    if len(sys.argv) > 2:
        c = P(sys.argv[2]); units = [[a] for a in case_assumptions(c)]
        if len(sys.argv) > 4:
            want = (P(sys.argv[3]), P(sys.argv[4]))
            TA = [A for key, A in tasks_for_case(c) if key == want]
            assert len(TA) == 1, 'no such task'
            units += [[a] for a in TA[0]]
    n = len(base) + len(cores) + len(extra) + len(units)
    with open(out, 'w') as f:
        f.write(f"p cnf {nv} {n}\n")
        for part in (base, cores, extra, units):
            for cl in part:
                f.write(' '.join(map(str, cl)) + ' 0\n')
    r1 = len(base); r2 = r1 + len(cores); r3 = r2 + len(extra)
    print(json.dumps({'cnf': out, 'vars': nv, 'clauses': n, 'base': [1, r1], 'archive_cores': [r1 + 1, r2],
                      'extra_cores': [r2 + 1, r3], 'units': [r3 + 1, n]}))

if __name__ == '__main__':
    main()
