# APSSV's n = M_K - 1, M_K = prod_{p<=K} p^(floor(log_p K)+1): u(n,k) = 1 for every k <= K (carries by Kummer).
from sympy import primerange
def MK(K):
    m = 1
    for p in primerange(2, K + 1):
        e = 0
        while p ** (e + 1) <= K: e += 1
        m *= p ** (e + 1)
    return m
def logu_is_zero(n, k):          # u(n,k)=1  <=>  no carry [n]_q < [k]_q at any q = p^a, p <= k
    for p in primerange(2, k + 1):
        q = p
        while q <= n:
            if n % q < k % q: return False
            q *= p
    return True
for K in (30, 100, 300):
    n = MK(K) - 1
    ok = all(logu_is_zero(n, k) for k in range(1, K + 1))
    print(f"K={K}: n has {len(str(n))} digits; u(n,k)=1 for all 1<=k<=K: {ok}; Roy's bound needs log u >= k/4+O(k/log k), here log u = 0 at k = {K}")
