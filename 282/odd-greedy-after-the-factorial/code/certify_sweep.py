"""Independent re-check of one sweep row (N, t) with certify.py: length, plus the climb's end from certify's OWN
recomputed (a_k, s_k, g_k).  Output: N t L_og L_cert rc R s_at_R g_at_R next where R = last numerator of the
initial climb 3,4,...,R.  s_at_R == R+1 iff R divides m at that point (Brown's ramp condition held at R)."""
import sys, math, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from certify import certify
N, t = int(sys.argv[1]), int(sys.argv[2])
tr = f"/dev/shm/cs_{N}_{t}.txt"
out = subprocess.run(["./og", "fact", "3", str(N), "1000000", tr, str(t)], capture_output=True, text=True, env={**os.environ, "OG_FAST": "1"}).stdout
L_og = int(out.split("length=")[1].split()[0])
claim = [int(x) for x in open(tr).read().split(",")]; os.remove(tr)
steps = []
rc, L = certify(3, t*math.factorial(N) - 1, claim, steps)
nums = [st[0] for st in steps] + [1]
k = 0
while k + 1 < len(nums) and nums[k+1] == nums[k] + 1: k += 1
R = nums[k]; s_R, g_R = (steps[k][1], steps[k][2]) if k < len(steps) else (0, 0)
print(N, t, L_og, L, rc, R, s_R, g_R, nums[k+1] if k + 1 < len(nums) else 0, flush=True)
