# Independent (non-Monte-Carlo) computation of kappa = E Delta from the single-scale sharing formula
# Pr(Delta >= u) = E_{U,phi}[(1-|cos phi|/rho)_+ (1-|sin phi|/rho)_+],  rho = e^{-u} 2^{-U}, U~U[0,1), phi~U[0,pi/2)
# (paper p.10: "{Delta >= u} is sharing at the largest side l <= R e^{-u}"; law of l/R log-uniform on (e^{-u}/2, e^{-u}]).
import numpy as np
from scipy import integrate
def G(u, nU=400, nphi=400):
    U = (np.arange(nU) + 0.5) / nU
    phi = (np.arange(nphi) + 0.5) / nphi * (np.pi / 2)
    rho = np.exp(-u) * 2.0 ** (-U)[:, None]
    g = np.clip(1 - np.cos(phi)[None, :] / rho, 0, None) * np.clip(1 - np.sin(phi)[None, :] / rho, 0, None)
    return g.mean()
up = integrate.quad(G, 0, 0.5*np.log(2), limit=200)[0]
lo = integrate.quad(lambda u: 1 - G(-u), 0, 60, limit=400)[0]
print("int_0^inf P(Delta>=u) du =", up, "  int_0^inf P(Delta<-u) du =", lo, "  kappa =", up - lo)
for u in [1, 2, 4, 6, 10]:
    print(f"u={u}: P(Delta<-u)={1-G(-u):.6f}  e^u*P = {(1-G(-u))*np.exp(u):.5f}   (asymptote (4/pi)/ln2 = {4/np.pi/np.log(2):.5f})")
print("P(Delta >= 0) =", G(0.0), "  P(Delta >= 0.3) =", G(0.3), " P(Delta >= log sqrt2 - 1e-9) =", G(0.5*np.log(2) - 1e-9))
