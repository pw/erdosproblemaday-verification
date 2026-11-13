"""Differential test of clq2 (multi-word bitsets, batch format) against cliquer 1.21 on random dense graphs n=60..400."""
import random, subprocess, os
random.seed(2026); bad = 0; runs = 0
for t in range(80):
    n = random.randint(64, 200); p = random.choice([0.6, 0.7, 0.75, 0.8])
    A = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p: A[i][j] = A[j][i] = True
    if random.random() < 0.5:
        S = random.sample(range(n), random.randint(10, 24))
        for a in S:
            for b in S:
                if a != b: A[a][b] = True
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if A[i][j]]
    open('/tmp/d.col', 'w').write(f"p edge {n} {len(E)}\n" + ''.join(f"e {a+1} {b+1}\n" for a, b in E))
    o = subprocess.run(['cliquer', '-u', '-q', '/tmp/d.col'], capture_output=True, text=True).stdout
    w = int(o.split('size=')[1].split(',')[0])
    perm = list(range(1, n + 1)); random.shuffle(perm)
    for tau in (w - 1, w, w + 1):
        open('/tmp/d.txt', 'w').write(f"1 {tau} {n} " + ' '.join(map(str, perm)) + "\n")
        r = subprocess.run(['./clq2', '/tmp/d.col', '/tmp/d.txt'], capture_output=True, text=True, timeout=600).stdout.split()
        runs += 1
        got = r[1] == 'SAT'; exp = tau <= w
        if got:
            C = [int(x) - 1 for x in r[2:]]
            if len(set(C)) != tau or not all(A[a][b] for a in C for b in C if a != b): bad += 1; print('BAD WITNESS', n, tau)
        if got != exp: bad += 1; print('MISMATCH', n, p, tau, w)
print('clq2 vs cliquer: runs', runs, 'bad', bad)
