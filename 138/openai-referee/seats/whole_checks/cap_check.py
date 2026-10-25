#!/usr/bin/env python3
"""Which inequality caps c (brief item j)?  Rich case: log R_k <= log2 + 2D log q - (gamma/80) k log k
with D log q <= c k log k + D log(2k^2)  =>  needs 2c < gamma/80, i.e. c < gamma/160 = 6.25e-5.
Affine case: log T_aff ~ 6 log q ~ 6 (c k/D) log k = o(p k) for EVERY fixed c (D ~ k^{1/10} > k^{1/20}).
CONTROL (must FAIL): c = 7e-5 > gamma/160 -> rich bound positive at every large k."""
import math
gamma = 0.01
def logR(k_log10, c):
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return math.log(2) + 2 * D * logq - (gamma / 80) * k * lk
def logAff_main(k_log10, c):   # 6 log q - pk/4 (dominant c-dependent part of log A_k)
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return 6 * logq - math.exp(0.95 * lk) / 4
for c in (1e-5, 6e-5, 6.2e-5, 7e-5, 1e-3):
    row = [f"{logR(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    aff = [f"{logAff_main(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    print(f"c={c:g}: 2c-gamma/80={2*c-gamma/80:+.3e}; log R_k at k=10^6,10^10,10^50,10^100,10^300: {row}")
    print(f"        affine main term 6log q - pk/4 at same k: {aff}")
