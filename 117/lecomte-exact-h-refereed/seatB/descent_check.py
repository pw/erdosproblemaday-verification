# Lemma 6.2 consequences on all nonnilpotent groups with descent data:
#  (a) some x outside F(G) has class size r <= omega(G);  (b) min [G:C_G(<x,y>)] <= r(r-1) <= N(N-1).
import glob
om = {}
for f in glob.glob('scan_*.out'):
    for line in open(f):
        p = line.split('\t')
        if len(p) > 5 and p[3].startswith('omega='): om[p[0]] = int(p[3].split('=')[1])
n = bad = 0; slack = []
for line in open('descent.txt'):
    lab, r, idx = line.split(); r = int(r); idx = int(idx) if idx != 'infinity' else None
    if lab not in om: continue
    N = om[lab]; n += 1
    ok = idx is not None and r <= N and idx <= r * (r - 1) and idx <= N * (N - 1)
    if not ok: bad += 1; print('FAIL', lab, r, idx, N)
    slack.append((N - r, lab))
print('checked', n, 'failures', bad, 'min slack N-r', min(slack) if slack else None)
