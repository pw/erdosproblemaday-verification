"""Lemma 1'' (CLAIMS.md): finite inequality  K*(A(N)-K) <= K*|M_R ∩ [1,N+a_K]| + (R-1)*(N+a_K),
where a_1<...<a_K are the K smallest elements of A and r(n) counts pairs a<b in A with a+b=n.
Also prints |M_R ∩ [1,N']|/N' against the density of A up to N (should approach >= delta)."""
import random
def build(name, L, rng):
    if name == 'random 0.3':   return [n for n in range(1, L+1) if rng.random() < 0.3]
    if name == 'random 0.05':  return [n for n in range(1, L+1) if rng.random() < 0.05]
    if name == 'multiples of 9': return list(range(9, L+1, 9))
    if name == '0,1 mod 7':    return [n for n in range(1, L+1) if n % 7 in (0, 1)]
    if name == '0,1 mod 40':   return [n for n in range(1, L+1) if n % 40 in (0, 1)]
    if name == 'Bateman {1} U 6N': return [1] + list(range(6, L+1, 6))
    if name == 'blocks [x,2x] x*=5':
        s = set(); x = 3
        while x <= L:
            s |= set(range(x, min(2*x, L)+1)); x *= 5
        return sorted(s)
    if name == '9N + squares': return sorted(set(range(9, L+1, 9)) | {k*k for k in range(1, int(L**0.5)+1)})
    if name == '{4,6} U 10q U 10q+3': return sorted({4, 6} | set(range(10, L+1, 10)) | set(range(13, L+1, 10)))
    raise ValueError(name)
names = ['random 0.3','random 0.05','multiples of 9','0,1 mod 7','0,1 mod 40','Bateman {1} U 6N','blocks [x,2x] x*=5','9N + squares','{4,6} U 10q U 10q+3']
rng = random.Random(7)
fails = 0
for N in (3000, 9000):
    for name in names:
        for K in (3, 10, 40):
            A = build(name, N + 10**5 if False else 2*N + 2000, rng)   # A generated well past N + a_K
            if len(A) < K + 5: continue
            aK = A[K-1]; Np = N + aK
            inA = bytearray(Np + 1)
            for a in A:
                if a <= Np: inA[a] = 1
            r = [0]*(Np+1)
            for a in A:
                if a > Np: break
                for b in range(a+1, Np - a + 1):
                    if inA[b]: r[a+b] += 1
            AN = sum(1 for a in A if a <= N)
            for R in (1, 3, 10):
                M = sum(1 for n in range(1, Np+1) if r[n] >= R)
                ok = K*(AN - K) <= K*M + (R-1)*Np
                if not ok:
                    fails += 1; print('FAIL', N, name, K, R)
                if K == 40 and R == 3:
                    print(f"N={N:5d} {name:22s} K={K:2d} R={R}: a_K={aK:5d}  A(N)/N={AN/N:.3f}  |M_R∩[1,N']|/N'={M/Np:.3f}  rhs-lhs={K*M + (R-1)*Np - K*(AN-K)}")
print('failures:', fails)
