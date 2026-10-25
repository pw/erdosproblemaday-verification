# K_{m,k} with m = round(e^L), k = round(e L): a part-constant stationary point (a on m-side, b on k-side)
# violates (2.5) with C_4=256 by a wide margin, while the global maximizer (m-side ~ 1) does not.
# Shows Lemma 2.3 genuinely needs GLOBAL maximality (as the paper and the Lean IsOptimizer assume).
from mpmath import mp, mpf, exp, log, findroot, nint, e
mp.dps = 60
for L in [10, 100, 3000]:
    m = nint(exp(mpf(L))); k = nint(e * L)
    # unknowns: la = log a, lb = log b ; stationarity: -la = k b, -lb = m a
    f = lambda la, lb: [-la - k * exp(lb), -lb - m * exp(la)]
    la, lb = findroot(f, (mpf(-L), mpf(-1)))
    a, b = exp(la), exp(lb)
    wS, wD = m * a, k * b
    eSD = m * k * a * b
    x = max(mpf(1), log(wD)) if wD > 1 else mpf(1)
    g = wS * (x + max(0, log(1 / wS)))
    Fsad = m * a * (1 - la) + k * b * (1 - lb) - m * k * a * b
    Fq = m  # test vector q: 1 on the m-side, 0 on the k-side gives F(q) = m exactly
    print(f'L={L}: m=e^{L}, k={int(k)}: stationary point w(S)={mp.nstr(wS,6)} w(D)={mp.nstr(wD,6)} x=log w(D)={mp.nstr(x,6)} '
          f'ratio e_w(S,D)/g_x(w(S))={mp.nstr(eSD/g,6)} (vs 256)  residuals={mp.nstr(max(abs(v) for v in f(la,lb)),3)}  F(stat)={mp.nstr(Fsad,6)} < F(q)=m={mp.nstr(Fq,6)}')
