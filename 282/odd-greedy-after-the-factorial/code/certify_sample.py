import random, subprocess, sys
from math import gcd
sys.path.insert(0, '.')
from certify import certify
random.seed(20261109)
# negative controls: corrupt one numerator of a true claim
for frac in ["3/179", "2086/2381", "5/5809", "881/937", "2/3"]:
    a0, b0 = map(int, frac.split('/'))
    out = subprocess.run(["./og","one",str(a0),str(b0)],capture_output=True,text=True).stdout.split("\n")
    claim = [int(x) for x in out[0].split(",")]
    acc = []
    for pos in range(len(claim)):
        bad = list(claim); bad[pos] += 2
        rc, L = certify(a0, b0, bad)
        if rc == 0: acc.append(pos)
    print(f"corrupted {frac} at every one of its {len(claim)} positions: accepted {len(acc)} {acc}", "(all rejected)" if not acc else "(BAD)")
# random sample across b < 10^4
n = ok = 0; bad = []
while n < 3000:
    b = random.randrange(3, 10000, 2); a = random.randrange(1, b)
    if gcd(a, b) != 1: continue
    out = subprocess.run(["./og","one",str(a),str(b)],capture_output=True,text=True).stdout.split("\n")
    claim = [int(x) for x in out[0].split(",")] if out[0] else []
    L_og = int(out[1].split("length=")[1].split()[0])
    rc, L = certify(a, b, claim); n += 1
    if rc == 0 and L == L_og: ok += 1
    else: bad.append((a, b, rc, L, L_og))
print(f"random sample: {n} fractions with odd b < 10^4, certified {ok}, problems {len(bad)}", bad[:5])
