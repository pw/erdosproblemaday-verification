"""Conditioned LP (level 1): class 1 = W. Is there z >= 0 on copies disjoint from W covering every other 5-set exactly once
(fractionally), optionally with the integrality cuts?  Column generation over the 1,410,555 distinct Aut(W)-feature columns.
  rows: 101 cover equalities | 69 four-set cuts (<=) | 135 six-set cuts (<=) | 4 point rows (>=)
Usage: lp.py [nocuts|cuts|planted]"""
import sys, json, numpy as np
from scipy.optimize import linprog
mode = sys.argv[1] if len(sys.argv) > 1 else 'cuts'
with open('lp_cols.bin', 'rb') as f:
    n = int(np.frombuffer(f.read(8), dtype=np.int64)[0]); D = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
    C = np.frombuffer(f.read(n * D), dtype=np.uint8).reshape(n, D)
    mult = np.frombuffer(f.read(4 * n), dtype=np.uint32)
O = json.load(open('orbits.json')); n5, n4, n6, npt = O['n5'], O['n4'], O['n6'], O['npt']
Wf = np.array(open('W_features.txt').read().split(), dtype=np.int64)
assert D == n5 + n4 + n6 + npt and int(mult.sum()) == 69046650 and Wf[:n5].sum() == 0
b_eq = np.array(O['size5'], dtype=float)
b_le = np.concatenate([4 * np.array(O['size4']) - Wf[n5:n5 + n4], 3 * np.array(O['size6']) - Wf[n5 + n4:n5 + n4 + n6]]).astype(float)
b_ge = (np.array(O['sizept']) - Wf[n5 + n4 + n6:]).astype(float)
assert (C[:, :n5].sum(axis=1) == 33).all()
if mode == 'planted': b_eq = b_eq.copy(); b_eq[0] *= 2          # control: an infeasible right-hand side must be detected
use_cuts = mode != 'nocuts'
Cf = C.astype(np.float32)
rng = np.random.default_rng(7)
active = list(rng.choice(n, size=4000, replace=False))
m_eq = n5; m_in = (n4 + n6 + npt) if use_cuts else 0
for it in range(200):
    A = C[active].astype(float)
    Aeq = np.hstack([A[:, :n5].T, np.eye(m_eq), -np.eye(m_eq)])
    cost = np.concatenate([np.zeros(len(active)), np.ones(2 * m_eq)])
    if use_cuts:
        Ain = np.vstack([A[:, n5:n5 + n4 + n6].T, -A[:, n5 + n4 + n6:].T])
        Ain = np.hstack([Ain, np.zeros((m_in, 2 * m_eq)), -np.eye(m_in)])
        Aeq = np.hstack([Aeq, np.zeros((m_eq, m_in))]); cost = np.concatenate([cost, np.ones(m_in)])
        res = linprog(cost, A_ub=Ain, b_ub=np.concatenate([b_le, -b_ge]), A_eq=Aeq, b_eq=b_eq, bounds=(0, None), method='highs')
        lam = np.concatenate([res.eqlin.marginals, res.ineqlin.marginals[:n4 + n6], -res.ineqlin.marginals[n4 + n6:]])
    else:
        res = linprog(cost, A_eq=Aeq, b_eq=b_eq, bounds=(0, None), method='highs')
        lam = np.concatenate([res.eqlin.marginals, np.zeros(n4 + n6 + npt)])
    assert res.status == 0, res.message
    red = -(Cf @ lam.astype(np.float32))            # reduced cost of each column (cost 0)
    worst = float(red.min()); nneg = int((red < -1e-6).sum())
    print(f'iter {it}: active {len(active)} infeasibility {res.fun:.6f} min reduced cost {worst:.3e} improving cols {nneg}', flush=True)
    if res.fun < 1e-7:
        z = res.x[:len(active)]; sup = [(int(active[i]), float(z[i])) for i in range(len(active)) if z[i] > 1e-9]
        print('FEASIBLE: fractional completion exists; support', len(sup), 'sum z', sum(v for _, v in sup))
        json.dump(dict(mode=mode, support=sup), open(f'lp_{mode}_feasible.json', 'w')); break
    if nneg == 0:
        print('INFEASIBLE at LP level: Farkas certificate found (float); writing lam'); np.save(f'lp_{mode}_farkas.npy', lam)
        print('lam.b =', float(lam[:n5] @ b_eq + (lam[n5:n5 + n4 + n6] @ b_le if use_cuts else 0) + (lam[n5 + n4 + n6:] @ b_ge if use_cuts else 0)))
        break
    order = np.argsort(red)[:3000]; aset = set(active)
    active += [int(i) for i in order if red[i] < -1e-6 and int(i) not in aset]
