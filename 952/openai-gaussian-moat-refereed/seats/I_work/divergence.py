# Seat I: divergence arithmetic for the final assembly of Theorem 1.2 (printed §8, eq. (8.2)).
# Batches: T = B^j with X_m <= log T <= 1.05 X_m, X_m = 100^m, ceil(M/2) <= m <= M.
# Quantity: S(M) = sum over batches of 1/log T = sum_m sum_{j in window m} 1/(j log B).
import mpmath as mp
mp.mp.dps = 120

def window(m, logB):
    X = mp.mpf(100)**m
    a = int(mp.ceil(X/logB))
    b = int(mp.floor(mp.mpf('1.05')*X/logB))
    return X, a, b

def window_sum(m, logB):
    X, a, b = window(m, logB)
    if b < a:
        return 0, mp.mpf(0), X
    # sum_{j=a}^{b} 1/j = psi(b+1) - psi(a)
    s = (mp.digamma(b+1) - mp.digamma(a))/logB
    return b-a+1, s, X

print("Paper claim (§8 proof): each window [X_m,1.05X_m] holds >= c X_m/log B batches,")
print("contributes >= c/(1.05 log B); there are ~M/2 windows => sum -> infinity.\n")
print("limit per-window contribution = log(1.05)/log B =", mp.nstr(mp.log(mp.mpf('1.05')),8), "/ log B\n")

for label, logB in [("B=3", mp.log(3)), ("B=e^10", mp.mpf(10)), ("B=e^50", mp.mpf(50)),
                    ("B=10^30", 30*mp.log(10)), ("B=e^233 (~10^101)", mp.mpf(233))]:
    print("==", label, " log B =", mp.nstr(logB, 6))
    # windows disjoint?
    disjoint = all(mp.mpf('1.05')*mp.mpf(100)**m < mp.mpf(100)**(m+1) for m in range(1, 60))
    first_nonempty = None
    for m in range(1, 60):
        cnt, s, X = window_sum(m, logB)
        if cnt > 0 and first_nonempty is None:
            first_nonempty = m
    print("   windows pairwise disjoint (1.05 X_m < X_{m+1}):", disjoint,
          "| first m with a batch:", first_nonempty)
    for m in [first_nonempty, first_nonempty+1, first_nonempty+3, 20, 40]:
        cnt, s, X = window_sum(m, logB)
        ratio = s*logB/mp.log(mp.mpf('1.05'))
        print(f"   m={m:3d}: #batches={mp.nstr(mp.mpf(cnt),6):>12}  "
              f"(0.05X_m/logB={mp.nstr(mp.mpf('0.05')*X/logB,6):>12})  "
              f"contrib={mp.nstr(s,8)}  contrib/(log1.05/logB)={mp.nstr(ratio,8)}")
    for M in [10, 20, 40, 80]:
        tot = mp.mpf(0); nB = 0
        for m in range((M+1)//2, M+1):
            cnt, s, X = window_sum(m, logB)
            tot += s; nB += cnt
        approx = (M - (M+1)//2 + 1)*mp.log(mp.mpf('1.05'))/logB
        print(f"   M={M:3d}: S(M)=sum 1/log T = {mp.nstr(tot,8)}   "
              f"(#windows*log1.05/logB = {mp.nstr(approx,8)})   n_B={mp.nstr(mp.mpf(nB),6)}")
    print()

# Telescope error budget (Lemma 8.1): (n_B-1)*eps_M with eps_M = O(T_+^{-7}), n_B = O(log T_+).
# log T_+ = 1.05 X_M.  Show log10 of n_B*T_+^{-7} for M=10 with log B=233:
M = 10; logB = mp.mpf(233)
nB = sum(window_sum(m, logB)[0] for m in range((M+1)//2, M+1))
logTp = mp.mpf('1.05')*mp.mpf(100)**M
print("M=10, logB=233: n_B =", nB, "; log10(n_B * T_+^{-7}) =",
      mp.nstr(mp.log10(nB) - 7*logTp/mp.log(10), 8))

# Illustrative size of M needed (constants are nonexplicit; this is only a scale illustration).
# l0: 2^{-l0} < e0/3, e0 = beta0/50, beta0=1/200.
beta0 = mp.mpf(1)/200; e0 = beta0/50
l0 = int(mp.ceil(mp.log(3/e0)/mp.log(2)))+0
while not (mp.mpf(2)**(-l0) < e0/3): l0 += 1
print("\nl0 (2^-l0 < e0/3, e0=1/10000):", l0)
for g0 in [mp.mpf('1e-3'), mp.mpf('1e-6')]:
    a0 = mp.mpf('0.25')
    c0 = a0*g0**(2*(l0+1))/4      # 'any sufficiently small constant below a0 g0^{2(l0+1)}/2'
    K0 = 1                         # see report: K0 >= 1 suffices in (7.7)
    c1 = beta0*c0/(12*K0)
    C = 4                          # k_T log(2T) <= C T with margin; illustrative
    logB = mp.log(C/(e0*c0) + 1)
    KD = 5                         # D = 1
    # need c1 * (#windows) * log(1.05)/logB > log KD, #windows ~ M/2
    Mneed = 2*mp.log(KD)*logB/(c1*mp.log(mp.mpf('1.05')))
    print(f"g0={mp.nstr(g0,3)}: c0~{mp.nstr(c0,4)}, c1~{mp.nstr(c1,4)}, log B~{mp.nstr(logB,5)}, "
          f"M needed ~ {mp.nstr(Mneed,4)} (finite; depends only on D through g0, c0, K_D)")
