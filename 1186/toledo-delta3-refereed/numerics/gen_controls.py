import sys, json, numpy as np
sys.argv = ["csearch.py", "1096", "1.0", "true"]
import csearch as C
import qlib
from common import grid_K, grid_S2, phistar_grid
N = 1096
S2 = grid_S2(N).astype(np.float64); PH = phistar_grid(N).astype(np.float64)
Q = lambda M, x: qlib.qv(M, x) / (8 * N * N)
C.M = S2
# --- control 1: tilted kernel w(a) = 1 + eps (a - 1/2) on the a (endpoint) coordinate ---
eps = 0.2
K = grid_K(N).astype(np.float64)
a = (np.arange(N) + 0.5) / N
Kt = K * (1 + eps * (a - 0.5))[:, None]
Mt = np.ascontiguousarray(Kt + Kt.T)
np.save(f"M_tilt_N{N}.npy", Mt)
best = (Q(Mt, PH), "phi*")
for s in range(1, 13):        # local descent from phi* (and -phi*) = the 'planted' target
    x0 = PH * (1 if s % 2 else -1)
    x, _ = qlib.cd(Mt, x0, s)
    x, _ = qlib.tabu(Mt, x, s, 60 * N, 20, 20); x, _ = qlib.cd(Mt, x, s)
    x2, _ = qlib.sa(Mt, x0, s, 600 * N, 30.0, 0.5); x2, _ = qlib.cd(Mt, x2, s)
    for y in (x, x2):
        if Q(Mt, y) < best[0]: best = (Q(Mt, y), "local-from-phi*")
print(f"TILT eps={eps}: Q'(phi*) = {Q(Mt, PH):.12f}; local descent from phi* reaches {best[0]:.12f}  (improvement {Q(Mt, PH)-best[0]:.3e})")
json.dump(dict(eps=eps, Q_phistar=Q(Mt, PH), Q_target=best[0]), open("ctrl_tilt.json", "w"))
# --- control 2: plant a structurally different local optimum psi via a rank-one bump ---
rs = [json.loads(l) for l in open("csearch_N1096_true.jsonl")]
alt = sorted([r for r in rs if r["ham"] > 300 and r["nfrac"] == 0], key=lambda r: r["Q"])[0]
rec = C.job((alt["method"], alt["fam"], alt["k"], alt["seed"], 0, 0))
rng = np.random.default_rng(alt["seed"]); x0 = C.family_start(alt["fam"], alt["k"], rng)
psi, _ = qlib.cd(S2, x0, alt["seed"]); psi, _ = qlib.tabu(S2, psi, alt["seed"] + 1, 3 * N, 0, 1)
psi = np.sign(psi)
qpsi = Q(S2, psi); rho = float(psi @ PH) / N
margin = 5e-4
c = (qpsi + 5 / 137 + margin) / (1 - rho ** 2)
Mp = np.ascontiguousarray(S2 - 8 * c * np.outer(psi, psi))     # Q'(x) = Q(x) - c (psi.x/N)^2
np.save(f"M_plant_N{N}.npy", Mp); np.save("psi_plant.npy", psi)
print(f"PLANT: psi has {len(C.blocks_of(psi))} blocks, Q(psi)={qpsi:.9f} (gap {qpsi+5/137:.3e}), rho={rho:.4f}, c={c:.6f}")
print(f"       Q'(phi*)={Q(Mp, PH):.9f}  Q'(psi)={Q(Mp, psi):.9f}  (psi planted better by {Q(Mp, PH)-Q(Mp, psi):.3e})")
json.dump(dict(c=c, rho=rho, Q_psi_true=qpsi, Qp_phistar=Q(Mp, PH), Qp_psi=Q(Mp, psi)), open("ctrl_plant.json", "w"))
