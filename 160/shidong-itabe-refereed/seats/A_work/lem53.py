# Shi-Dong Lemma 5.3. (a) carry consistency: for M = 2^j, every 4-AP y0..y3 in Z/MZ (step s in 0..M-1)
#     with tau(y0)=tau(y1), tau(y2)=tau(y3), tau(x)=floor(log2(M-x)), has constant carries 1{y_{i+1}<y_i}.
#     Also count how often the proof's "opposite sides of M/2" step meets the boundary x = M/2.
# (b) the full colouring psi_N on [N]: no nontrivial 4-AP with c(n0)=c(n1), c(n2)=c(n3)  (AABB incl. AAAA).
# Controls: drop tau / drop Psi / replace floor(log2(M-x)) by floor(log2(x+1)) -> AABB must appear.
import math, sys
def tau_f(M):
    return [ (M - x).bit_length() - 1 for x in range(M) ]   # floor(log2(M-x)) exactly
rc = 0
for j in range(1, 10):
    M = 2**j; tau = tau_f(M); bad = bdry = 0
    for s in range(M):
        for y0 in range(M):
            y = [(y0 + i*s) % M for i in range(4)]
            if tau[y[0]] == tau[y[1]] and tau[y[2]] == tau[y[3]]:
                e = [int(y[i+1] < y[i]) for i in range(3)]
                if len(set(e)) != 1: bad += 1
            # boundary bookkeeping: a carry in the first addition with s <= M/2 and y0 == M/2
            if 2*s <= M and y[1] < y[0] and 2*y[0] == M: bdry += 1
    print(f"M={M}: carry-consistency violations={bad}; first-addition carries starting AT x=M/2 (s<=M/2): {bdry}")
    rc |= bad > 0
def colour(N, use_tau=True, use_psi=True, alt_tau=False):
    M = 2**math.ceil(math.sqrt(math.log2(N))); m = math.ceil(math.log(N+1, M) - 1e-12)
    while M**m < N+1: m += 1
    col = [None]*(N+1)
    for n in range(1, N+1):
        xs = []; t = n
        for _ in range(m): xs.append(t % M); t //= M
        T = tuple(((x+1).bit_length()-1) if alt_tau else ((M-x).bit_length()-1) for x in xs) if use_tau else ()
        col[n] = T + ((sum(x*x for x in xs),) if use_psi else ())
    return col, M, m
def count_aabb(col, N, stop=False):
    c = 0
    for d in range(1, (N-1)//3 + 1):
        for a in range(1, N - 3*d + 1):
            if col[a] == col[a+d] and col[a+2*d] == col[a+3*d]:
                c += 1
                if stop: return c
    return c
for N in (300, 1000, 2500):
    col, M, m = colour(N)
    k = count_aabb(col, N)
    print(f"N={N} (M={M}, m={m}, palette={len(set(col[1:]))}): AABB-type 4-APs = {k}")
    rc |= k > 0
N = 1000
print("controls (expect >0):",
      "no tau ->", count_aabb(colour(N, use_tau=False)[0], N, True),
      "| no Psi ->", count_aabb(colour(N, use_psi=False)[0], N, True),
      "| tau=floor(log2(x+1)) ->", count_aabb(colour(N, alt_tau=True)[0], N, True))
sys.exit(rc)
