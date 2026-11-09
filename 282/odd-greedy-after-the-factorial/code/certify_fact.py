"""Certify og's claimed trajectory for 3/(t*N!-1) with certify.py (claim read from og's trace file)."""
import sys, math, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from certify import certify
N, t = int(sys.argv[1]), int(sys.argv[2])
tr = f"/dev/shm/cf_{N}_{t}.txt"
out = subprocess.run(["./og", "fact", "3", str(N), "1000000", tr, str(t)], capture_output=True, text=True, env={**os.environ, "OG_FAST": "1"}).stdout
L_og = int(out.split("length=")[1].split()[0])
claim = [int(x) for x in open(tr).read().split(",")]
rc, L = certify(3, t*math.factorial(N) - 1, claim)
print(f"3/({t}*{N}!-1): og length {L_og}; certificate rc={rc} length {L} -> {'OK' if rc == 0 and L == L_og else 'PROBLEM'}", flush=True)
os.remove(tr)
