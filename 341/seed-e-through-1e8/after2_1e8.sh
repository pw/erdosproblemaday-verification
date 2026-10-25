#!/bin/bash
# second post-10⁸ chain: the instruments written after the referee's report, on the 10⁸ output
cd ~/MathDyad/erdos341e
echo "=== spectrum v3 on [2e7,1e8] ==="; /usr/bin/time -f "spectrum wall %es" nice -n 19 python3 spectrum.py F_E_eq_1e8_elems.u32 6 50 > spectrum_F_E_eq_1e8_v3.log 2>&1; grep -E "RELATION|Z-rank|peaks on the|variance within|continued|convergent|variance in the" spectrum_F_E_eq_1e8_v3.log
G=$(grep -oE "g = [0-9]\.[0-9]+" spectrum_F_E_eq_1e8_v3.log | head -1 | awk '{print $3}'); [ -z "$G" ] && G=0.28459193622; echo "g used for phases: $G"
echo "=== phase_core on two 10⁸ windows ==="; { nice -n 19 python3 phase_core.py F_E_eq_1e8_elems.u32 $G 99000000 1000000 1000; nice -n 19 python3 phase_core.py F_E_eq_1e8_elems.u32 $G 50000000 1000000 1000; nice -n 19 python3 phase_core.py F_E_eq_1e8_elems.u32 $G 20000000 1000000 1000; } 2>&1 | tee phase_core_E_1e8.log
echo "=== phase_arcs on [9.9e7,1e8) ==="; nice -n 19 python3 phase_arcs.py F_E_eq_1e8_elems.u32 $G 99000000 1000000 1000 2>&1 | tee phase_arcs_E_1e8.log
echo "=== 31821 cross-window census (same classes empty in disjoint windows?) ==="; nice -n 19 python3 - <<'PY' 2>&1 | tee census_31821_1e8.log
import numpy as np
el=np.fromfile('F_E_eq_1e8_elems.u32',dtype='<u4').astype(np.int64)
for m in (31821,8528,27875):
    sets=[]
    for lo,hi in ((10**7,4*10**7),(4*10**7,7*10**7),(7*10**7,10**8)):
        c=np.bincount(el[(el>=lo)&(el<hi)]%m,minlength=m); sets.append(set(np.nonzero(c==0)[0].tolist())); print(f"m={m} [{lo},{hi}): empty classes {len(sets[-1])} ({len(sets[-1])/m*100:.1f}%)")
    print(f"m={m}: empty in all three windows {len(sets[0]&sets[1]&sets[2])}; union {len(sets[0]|sets[1]|sets[2])}; pairwise symmetric differences {len(sets[0]^sets[1])}, {len(sets[1]^sets[2])}")
PY
echo "ALL DONE 2 $(date -u +%FT%TZ)"
