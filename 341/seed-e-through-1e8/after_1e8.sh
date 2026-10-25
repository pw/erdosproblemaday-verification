#!/bin/bash
# waits for the 1e8 generator, then runs every post-hoc instrument on its output
cd ~/MathDyad/erdos341e
PID=$(cat F_E_eq_1e8.pid)
while kill -0 "$PID" 2>/dev/null; do sleep 20; done
echo "1e8 generator exited at $(date -u +%FT%TZ)"; cat F_E_eq_1e8.log
ls -la F_E_eq_1e8_elems.u32; sha256sum F_E_eq_1e8_elems.u32 | tee F_E_eq_1e8_elems.sha256
echo "=== analyze (maxshift 4e7) ==="; /usr/bin/time -f "analyze wall %es" nice -n 19 python3 analyze.py F_E_eq_1e8_elems.u32 40000000 > analyze_1e8.log 2>&1; tail -20 analyze_1e8.log
echo "=== verify341 windows on the 1e8 output ==="; { ./verify341 F_E_eq_1e8_elems.u32 0 12 13 200000; ./verify341 F_E_eq_1e8_elems.u32 0 12 50000000 200000; ./verify341 F_E_eq_1e8_elems.u32 0 12 99799000 200000; ./verify341 F_E_eq_1e8_elems.u32 0 12 50000000 200000 50000041; echo "rc=$? (negative control, expect 1)"; } 2>&1 | tee verify_1e8.log
echo "=== residue census m<=10000 on [1e7,1e8] ==="; nice -n 19 python3 - <<'PY' 2>&1 | tee census_mod_1e8.log
import numpy as np, time
el=np.fromfile('F_E_eq_1e8_elems.u32',dtype='<u4').astype(np.int64); w=el[el>=10**7]
t0=time.time(); worst=[]; empties=0
for m in range(2,10001):
    c=np.bincount(w%m,minlength=m); mu=c.mean(); worst.append((c.min()/mu,c.max()/mu,m)); empties+=(c.min()==0)
worst.sort(); print(f"[1e7,1e8], {len(w)} elements, m=2..10000: moduli with an EMPTY class: {empties}; most depleted (min/mean,m): {[(round(a,3),m) for a,b,m in worst[:5]]}; most over-full (max/mean,m): {[(round(b,3),m) for a,b,m in sorted(worst,key=lambda t:-t[1])[:5]]} ({time.time()-t0:.0f}s)")
PY
echo "ALL DONE $(date -u +%FT%TZ)"
