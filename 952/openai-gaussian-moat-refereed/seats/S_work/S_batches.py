# Seat S: sanity check of the constants behind (6.4)'s a_0 and (6.5)'s C on real primes (T up to 1e7),
# plus the geometric-sum step sum_{T'<T, T'=B^j'} k_T' log(2T') <= C T/(B-1).
import math
NMAX = 2*10**7 + 10
sieve = bytearray([1])*(NMAX+1); sieve[0]=sieve[1]=0
for i in range(2, int(NMAX**0.5)+1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(range(i*i, NMAX+1, i)))
pref_cnt = [0]*(NMAX+1); pref_log = [0.0]*(NMAX+1)
c=0; l=0.0
for n in range(NMAX+1):
    if sieve[n] and n % 4 == 1: c += 1; l += math.log(n)
    pref_cnt[n]=c; pref_log[n]=l
def batch(T):
    T = int(T); lo = T; hi = 2*T
    k = pref_cnt[hi]-pref_cnt[lo-1]; s = pref_log[hi]-pref_log[lo-1]
    return k, s
worstC = 0; worst_a0 = 9
for e in range(3, 8):
    for mant in [1, 2, 3, 5, 7]:
        T = mant*10**e
        if 2*T > NMAX: continue
        k, s = batch(T); L = s/k
        worstC = max(worstC, k*math.log(2*T)/T)
        worst_a0 = min(worst_a0, k*L/T)     # a_0 T/L <= k  <=>  a_0 <= k L / T
        print(f"T={T:>9}: k_T={k:>7} kL/T={k*L/T:.4f}  k log(2T)/T={k*math.log(2*T)/T:.4f}")
print("max k log(2T)/T =", round(worstC,4), " (so C=1 is safe here; asymptotically 1/2)")
print("min kL/T =", round(worst_a0,4), " (a_0=1/4 satisfies a_0 T/L <= k_T)")
# geometric sum with B=3: sum over T'=3^j < T
B=3; T=3**14
S=sum(batch(3**j)[0]*math.log(2*3**j) for j in range(2,14))
print(f"B=3, T=3^14: sum_(T'<T) k log 2T' = {S:.1f} <= C T/(B-1) with C={worstC:.3f}: {worstC*T/(B-1):.1f}")
