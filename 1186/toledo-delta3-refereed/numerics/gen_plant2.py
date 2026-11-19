import json, numpy as np, qlib
from common import grid_S2, phistar_grid
N = 1096; S2 = grid_S2(N).astype(np.float64); PH = phistar_grid(N).astype(np.float64)
Q = lambda M, x: qlib.qv(M, x) / (8 * N * N)
psi = np.load("psi_plant.npy"); qpsi = Q(S2, psi); rho = float(psi @ PH) / N
margin = 1e-4
c = (qpsi + 5 / 137 + margin) / (1 - rho ** 2)
Mp = np.ascontiguousarray(S2 - 8 * c * np.outer(psi, psi))
np.save(f"M_plant2_N{N}.npy", Mp)
print(f"PLANT2: margin {margin}: c={c:.6f} Q'(phi*)={Q(Mp, PH):.9f} Q'(psi)={Q(Mp, psi):.9f} (psi better by {Q(Mp, PH)-Q(Mp, psi):.3e})")
json.dump(dict(c=c, rho=rho, Q_psi_true=qpsi, Qp_phistar=Q(Mp, PH), Qp_psi=Q(Mp, psi)), open("ctrl_plant2.json", "w"))
