# NEGATIVE control for the CRT pipeline: corrupt one residue (Hc(111) mod p_3, +1) and confirm the
# 8th-modulus consistency check flags it (the reconstruction then lands ~2^216, failing both tests).
import json
from math import prod
rs = [json.load(open(f"/tmp/e488/referee_R/crt_R2048_J113_m{i}.json")) for i in range(8)]
ps = [r["p"] for r in rs]
def crt(vals, mods):
    x, M = 0, 1
    for v, m in zip(vals, mods):
        t = ((v - x) * pow(M, -1, m)) % m; x += M*t; M *= m
    return x
for tamper in (False, True):
    vals = [r["c"][111] for r in rs]
    if tamper: vals[3] = (vals[3] + 1) % ps[3]
    v = crt(vals[:7], ps[:7])
    print(f"tamper={tamper}: bits={v.bit_length()} 8th-modulus match={v % ps[7] == vals[7]}  -> check {'PASS' if (v % ps[7] == vals[7] and v.bit_length() <= 200) else 'FAIL'}")
