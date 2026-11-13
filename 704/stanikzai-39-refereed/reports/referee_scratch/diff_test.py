"""Differential test of clq2 (both the shipped binary and a fresh -O2 build) against cliquer (Ostergard).
Global graph g.col on Ng vertices; leaf = random subset (shuffled order) or all vertices. Reference omega of the
induced leaf graph by cliquer on a separately written induced DIMACS file."""
import random, subprocess, sys, os, itertools
seed = int(sys.argv[1]); trials = int(sys.argv[2])
rng = random.Random(seed)
D = f'/tmp/ref704/diff/w{seed}'; os.makedirs(D, exist_ok=True)
BIN = ['/home/exedev/MathDyad/erdos704/indep/clq2', '/tmp/ref704/clq2_mine']
SIZES = [40, 63, 64, 65, 66, 100, 127, 128, 129, 150, 191, 192, 193, 220, 255, 256, 257, 300, 320, 350]
bad = 0; done = 0; skipped = 0
def cliquer_omega(path):
    try:
        o = subprocess.run(['nice','-n','19','cliquer','-u','-q','-q',path], capture_output=True, text=True, timeout=60).stdout
    except subprocess.TimeoutExpired:
        return None
    return int(o.split('size=')[1].split(',')[0]) if 'size=' in o else 0
for t in range(trials):
    n = rng.choice(SIZES)
    # density chosen so cliquer stays feasible
    p = rng.choice([0.5, 0.6, 0.7] if n > 200 else [0.6, 0.7, 0.75, 0.8] if n > 120 else [0.7, 0.75, 0.8, 0.85])
    extra = rng.choice([0, 0, 20, 60])           # global graph has extra vertices not in the leaf
    Ng = n + extra
    A = [[False]*Ng for _ in range(Ng)]
    for i in range(Ng):
        for j in range(i+1, Ng):
            if rng.random() < p: A[i][j] = A[j][i] = True
    leaf = rng.sample(range(Ng), n)                 # shuffled order
    if rng.random() < 0.6:                            # plant a clique inside the leaf
        k = rng.randint(8, min(n, 40))
        S = rng.sample(leaf, k)
        for a in S:
            for b in S:
                if a != b: A[a][b] = True
    E = [(i, j) for i in range(Ng) for j in range(i+1, Ng) if A[i][j]]
    with open(D + '/g.col', 'w') as f:
        f.write(f'p edge {Ng} {len(E)}\n'); f.writelines(f'e {i+1} {j+1}\n' for i, j in E)
    pos = {v: i for i, v in enumerate(leaf)}
    Ei = [(pos[a]+1, pos[b]+1) for a, b in itertools.combinations(leaf, 2) if A[a][b]]
    with open(D + '/ind.col', 'w') as f:
        f.write(f'p edge {n} {len(Ei)}\n'); f.writelines(f'e {a} {b}\n' for a, b in Ei)
    w = cliquer_omega(D + '/ind.col')
    if w is None: skipped += 1; continue
    lines = ''.join(f'{100+tau} {tau} {n} ' + ' '.join(str(x+1) for x in leaf) + '\n' for tau in (w-2, w-1, w, w+1, w+2) if tau >= 1)
    open(D + '/lv.txt', 'w').write(lines)
    for b in BIN:
        try:
            o = subprocess.run(['nice','-n','19', b, D + '/g.col', D + '/lv.txt'], capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            print('TIMEOUT', b, n, p); skipped += 1; continue
        if o.returncode != 0: print('RC', o.returncode, o.stderr); bad += 1; continue
        for l in o.stdout.split('\n'):
            if not l: continue
            x = l.split(); tau = int(x[0]) - 100
            exp = tau <= w; got = x[1] == 'SAT'
            if got:
                C = [int(y)-1 for y in x[2:]]
                ok = len(C) == tau and len(set(C)) == tau and set(C) <= set(leaf) and all(A[a][b] for a, b in itertools.combinations(C, 2))
                if not ok: bad += 1; print('BAD WITNESS', seed, t, n, p, tau)
            if got != exp:
                bad += 1; print('MISMATCH', seed, t, b, 'n', n, 'p', p, 'tau', tau, 'omega', w, x[:2])
                open(D + f'/fail_{t}.txt', 'w').write(lines)
    done += 1; print('trial', t, 'n', n, 'p', p, 'omega', w, 'ok', flush=True)
print(f'seed {seed}: trials={trials} done={done} skipped={skipped} bad={bad}')
