"""probe_control.py -- the probe's certification must flag a wrong table: with T'(7)=9 the F_9-type map
(p=3, d=4, e=1, full rank: a=10, omega=7) must come out UNcertified; with the paper's T it must be certified.
Also: a deliberately improper colouring must be rejected by check_colouring on a probe graph."""
import probe, graphlib
from graphlib import check_colouring
true_T = probe.T
for seed in range(1, 40):
    rec, Ms = probe.analyse_map(3, 4, 1, 'random', seed)
    if rec['z'] == 81:
        break
print('true table : p=3 d=4 e=1 seed=%d z=%d omega=%d(exact=%s) a in [%d,%d] cert_a=%s cert_z=%s' % (seed, rec['z'], rec['omega_lb'], rec['omega_proven'], rec['a_lb'], rec['a_ub'], rec['cert_a'], rec['cert_z']))
probe.T = lambda n: 9 if n == 7 else true_T(n)
rec2, _ = probe.analyse_map(3, 4, 1, 'random', seed)
print("wrong T'(7)=9: cert_a=%s cert_z=%s (must both be False)" % (rec2['cert_a'], rec2['cert_z']))
ok = rec['cert_a'] and rec['cert_z'] and (not rec2['cert_a']) and (not rec2['cert_z'])
z, k, adj, reps = probe.build_graph(3, 4, probe.make_map(3, 4, 1, 'random', seed)[0])
bad = [0] * k
print('constant colouring on probe graph rejected:', not check_colouring(k, adj, bad))
ok = ok and not check_colouring(k, adj, bad)
print('PROBE CONTROL', 'PASS' if ok else 'FAIL')
