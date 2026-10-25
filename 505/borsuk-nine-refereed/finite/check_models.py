#!/usr/bin/env python3
"""Validate SAT models of the drop-one controls with the independent set-logic checker in tensystem_cnf.check."""
import sys, glob, re
from tensystem_cnf import check
rc = 0
for out in sorted(glob.glob('runs/*.kissat.out')) + sorted(glob.glob('runs/*.cadical.out')):
    txt = open(out).read()
    if 's SATISFIABLE' not in txt: continue
    lits = [int(x) for l in txt.splitlines() if l.startswith('v ') for x in l[2:].split()]
    pos = {x for x in lits if x > 0}
    ok, nq, nt = check(pos)
    name = out.split('/')[-1]
    m = re.search(r'drop_(\w+?)\.(kissat|cadical)', name)
    dropped = m.group(1) if m else None
    viol = [k for k, v in ok.items() if not v]
    expect = {dropped} if dropped else set()
    # a SAT model must satisfy every encoded field; parity is not encoded in the lean variant, so ignore it
    enc_viol = [k for k in viol if k not in expect and k != 'parity']
    print(f'{name:45s} |Q|={nq:3d} |T|={nt:3d} violates={viol}  ' + ('OK' if not enc_viol else 'ENCODING DISAGREES'))
    if enc_viol: rc = 1
sys.exit(rc)
