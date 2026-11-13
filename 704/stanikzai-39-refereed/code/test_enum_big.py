"""clq3 (enumerate every clique of size tau = omega) vs cliquer 1.21 'all cliques of size exactly omega' on random
dense graphs of 65-160 vertices (multi-word bitsets)."""
import random, subprocess
random.seed(704); bad = 0; runs = 0
for t in range(50):
    n = random.randint(65, 160); p = random.choice([0.6, 0.7, 0.75])
    A = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p: A[i][j] = A[j][i] = True
    if random.random() < 0.6:
        for _ in range(random.randint(1, 3)):
            S = random.sample(range(n), random.randint(12, 20))
            for a in S:
                for b in S:
                    if a != b: A[a][b] = True
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if A[i][j]]
    open('/tmp/eb.col', 'w').write(f"p edge {n} {len(E)}\n" + ''.join(f"e {a+1} {b+1}\n" for a, b in E))
    o = subprocess.run(['cliquer', '-u', '-q', '/tmp/eb.col'], capture_output=True, text=True).stdout
    w = int(o.split('size=')[1].split(',')[0])
    o = subprocess.run(['cliquer', '-u', '-q', '-q', '-a', '-m', str(w), '-M', str(w), '/tmp/eb.col'], capture_output=True, text=True).stdout
    ref = {frozenset(map(int, l.split(':')[1].split())) for l in o.splitlines() if l.startswith('size=')}
    perm = list(range(1, n + 1)); random.shuffle(perm)
    open('/tmp/eb.txt', 'w').write(f"1 {w} {n} " + ' '.join(map(str, perm)) + "\n")
    r = subprocess.run(['./clq3', '/tmp/eb.col', '/tmp/eb.txt'], capture_output=True, text=True).stdout.splitlines()
    got = [frozenset(map(int, l.split()[2:])) for l in r if ' SOL ' in l]
    runs += 1
    print('graph', runs, 'n', n, 'omega', w, 'max cliques', len(ref), 'clq3', len(got), flush=True)
    if set(got) != ref or len(got) != len(set(got)): bad += 1; print('MISMATCH', n, w, len(ref), len(got))
print('clq3 vs cliquer -a: graphs', runs, 'bad', bad)
