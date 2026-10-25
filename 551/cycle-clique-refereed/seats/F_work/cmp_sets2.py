import json, sys
sys.path.insert(0, '/tmp/oaimath/189/seats/F_work')
import orig_lib, indep_lib
exec(open('/tmp/oaimath/189/seats/F_work/enum_own.py').read().split("summ = json.load")[0])
cert = {}
for line in open(sys.argv[1]):
    r = json.loads(line)
    cert.setdefault((r['k'], r['t']), set()).add(tuple(tuple(c) for c in r['pattern']))
bad = 0
for k in range(5, 18):
    for t in range(max(3, k//2), min(8, k)+1):
        mine = count(t, k-t)
        o = list(orig_lib.forests(t, k-t)); so = set(o)
        i = indep_lib.patterns(t, k-t); si = set(i)
        ok = (mine == so == si == cert[(k,t)]) and len(o) == len(so)
        if not ok: bad += 1; print('MISMATCH', k, t, len(mine), len(so), len(si), len(cert[(k,t)]), len(o))
print('set mismatches:', bad)
