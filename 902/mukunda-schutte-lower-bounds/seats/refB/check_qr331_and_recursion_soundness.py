"""Referee B: (a) nu_k of QR_331 (n=5) using arc-transitivity of Paley tournaments
(x -> c x + d, c a nonzero square, maps any arc u->v to 0->1, so every k-set, k>=2, is
equivalent to one containing {0,1}); confirms QR_331 has S_5 and checks Lemma 3.1 on orbit
representatives.  (b) Soundness test of Lemma 4.5: for every real S_n tournament T on N vertices we
have, L_s(N) <= nu_s(T); a mutated recursion (h = L_{s+1}+2) must FAIL on some real T (control)."""
import sys, time
from itertools import combinations
from math import comb
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refB')
import tb
from recursion import Ls, ruled_out

t0 = time.time()
p, n = 331, 5
out = tb.qr_tournament(p)
inm = tb.in_masks(out)
# sanity: automorphism x -> 3x+5 if 3 is a square mod 331
sq = {(x * x) % p for x in range(1, p)}
c = next(c for c in range(2, p) if c in sq)
for u in range(0, p, 37):
    for v in range(p):
        if u != v:
            assert ((out[u] >> v) & 1) == ((out[(c * u + 7) % p] >> ((c * v + 7) % p)) & 1)
nu, cnt = tb.nu_all(inm, p, n, fixed=(0, 1))
nu[1] = bin(inm[0]).count('1')
print(f'QR_331: nu_0..nu_5 = {nu} (sets enumerated per size {cnt}); S_5 holds: {nu[5] >= 1}; time {time.time()-t0:.1f}s')
sys.stdout.flush()
ok = True
nchk = 0
reps = {0: [()], 1: [(0,)], 2: [(0, 1)], 3: [(0, 1, x) for x in range(2, p)],
        4: [(0, 1) + c2 for c2 in combinations(range(2, p), 2)]}
for s in range(n):
    h = nu[s + 1]
    for A in reps[s]:
        R = tb.D(inm, A, p)
        m = R.bit_count()
        Aset = set(A)
        o = [(out[y] & R).bit_count() for y in range(p) if y not in Aset]
        for y in range(p):
            if y in Aset:
                continue
            oy = (out[y] & R).bit_count()
            if oy > (m - h - 1 if (R >> y) & 1 else m - h):
                ok = False
        for k in range(1, n + 1):
            mid = sum(comb(x, k) for x in o)
            lhs = nu[k] * comb(m, k)
            r1 = (p - s - m) * comb(m - h, k) + m * comb(m - h - 1, k)
            r2 = (p - s) * comb(m - h, k)
            nchk += 1
            if not (lhs <= mid <= r1 <= r2):
                ok = False
                print('FAIL', s, A, k, lhs, mid, r1, r2)
print(f'QR_331 Lemma 3.1 on orbit representatives: {nchk} (A,k) checks, all OK = {ok}; time {time.time()-t0:.1f}s')

# (b) recursion soundness on real tournaments
real = [('QR_7', 2, 7, [7, 3, 1]), ('QR_19', 3, 19, [19, 9, 4, 1]), ('QR_67', 4, 67, [67, 33, 16, 6, 1]),
        ('N70', 4, 70, [70, 33, 16, 5, 1]), ('QR_331', 5, 331, nu)]
for name, nn, N, nuv in real:
    L = Ls(nn, N)
    sound = all(L[s] <= nuv[s] for s in range(nn + 1))
    Lm = Ls(nn, N, hshift=2)
    mut_viol = [s for s in range(nn + 1) if Lm[s] > nuv[s]]
    print(f'{name}: L(N={N}) = {L}  nu = {nuv}  L_s<=nu_s all s: {sound};  '
          f'mutated (h=L+2) L = {Lm}, violates real nu at s={mut_viol}')
print('time', round(time.time() - t0, 1))
