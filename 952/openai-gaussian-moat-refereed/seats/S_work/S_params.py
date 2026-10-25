# Seat S: precision-safe check of every explicit inequality in printed Lemma 6.1, (6.4)-(6.5), (6.7), (6.10),
# (6.11), (6.14)-(6.16) and the Theorem 5.2 hypotheses (5.4)-(5.6) at every invocation i<J, for every batch
# window m in [ceil(M/2), M] (log T sampled across [X_m, 1.05 X_m]).
# The inherited checks3.py subtracted r_i*logT - r_{i+1}*logT at 30 digits with logT ~ 10^(2M): catastrophic
# cancellation -> spurious "(5.4)"/"(6.16)" failures. Here every such difference is taken symbolically (= 2*beta_i*logT).
import sys
from mpmath import mp, mpf, log, ceil, floor, exp
mp.dps = 60
LN2 = log(2)

def lse(*xs):
    m = max(xs); return m + log(sum(mp.e**(x - m) for x in xs))

def run(M, g0=mpf('1e-3'), l0=15, a0=mpf(1)/4, C43=mpf(100), CD=mpf(1000), Cpnt=mpf(1),
        n_exp=mpf(6)/5, gap=2, g1log=None, g2log=None, verbose=False,
        fracs=('1','1.0001','1.013','1.025','1.037','1.0499','1.05')):
    fails = set()
    Mf = mpf(M)
    beta0 = mpf(1)/200; e0 = beta0/50
    g0log = -log(g0)
    g1log = Mf**3 if g1log is None else g1log(Mf)       # log(1/g1)
    g2log = 100*Mf**20 if g2log is None else g2log(Mf)  # log(1/g2)
    X = lambda m: mpf(100)**m
    mlo = (M + 1)//2
    XM = X(M); logN = 10*mpf('1.05')*XM + 1
    # c0 and B (printed 6.2): c0 < a0 g0^{2(l0+1)}; B-1 >= C/(e0 c0)
    logc0 = log(a0) + 2*(l0+1)*log(g0) - LN2
    logB = log(1 + Cpnt/(e0*mp.e**logc0))
    # number of operations (all windows, all bands) + 1
    nops = sum(mpf('0.5')*X(m)/(2*g0log) + mpf('0.1')*X(m)/(2*g1log) + mpf('0.05')*X(m)/(2*g2log) + 3
               for m in range(mlo, M + 1))
    lognops = log(nops)
    # ---- Lemma 6.1 ----
    bands = []   # in processing order: (window, lowEdge, highEdge, log(1/g))
    for m in range(M, mlo - 1, -1):
        bands += [(m, mpf('0.8'), mpf('1.3'), g0log), (m, mpf('0.20'), mpf('0.30'), g1log), (m, mpf('0.05'), mpf('0.10'), g2log)]
    for k, (m, lo, hi, gl) in enumerate(bands):
        log_gV_min = lo*X(m) - gl                       # smallest g*V in this band
        # (a) every later band's largest log-length g'U' is below the smallest gV here
        for (m2, lo2, hi2, gl2) in bands[k+1:]:
            if not (hi2*X(m2) - gl2 < log_gV_min): fails.add("L6.1 later bands dominated")
        # (b) log(1+S_V) <= 2gV : suffices gV >= logN + log(nops) + log 2
        if not (log_gV_min > log(logN + lognops + LN2)): fails.add("L6.1 log(1+S_V)<=2gV")
        # Lemma 4.3 regime g^5 U >= Lambda log T with margin: log(g^5 U) - log log T > 50
        logLT_max = log(mpf('1.05')*X(m) + 1)
        if not (lo*X(m) - 5*gl - logLT_max > 50): fails.add("L4.3 regime g^5U/logT")
    # windows nonempty given B
    if not (mpf('0.05')*X(mlo) > 2*logB): fails.add("windows contain >=2 batches")
    # ---- per window / per batch ----
    maxJ = 0
    for m in range(mlo, M + 1):
        Xm = X(m)
        # (6.4) placement: l0+1 top-band steps below a0*T stay in the top band; q<=k needs a0<1/2
        if not (mpf('0.2')*Xm > -log(a0) + 2*(l0 + 2)*g0log): fails.add("(6.4) top-band placement")
        # bottom band capacity for ceil(200 M^20) iterations + recording
        if not ((ceil(200*Mf**20) + 2)*2*g2log < mpf('0.05')*Xm): fails.add("(6.11) bottom band capacity")
        for frac in [mpf(x) for x in fracs]:
            LT = frac*Xm
            if not (beta0*LT > Mf**20): fails.add("(6.7) J>=1"); continue
            J = 0
            while beta0*LT/2**J > Mf**20: J += 1
            maxJ = max(maxJ, J)
            BJ = beta0*LT/2**J
            if not (Mf**20/2 < BJ <= Mf**20): fails.add("(6.7) range of beta_J logT")
            for i in range(J + 1):
                ri = mpf(1)/4 - 4*beta0*(1 - mpf(2)**(-i))
                # A_i in middle band with room for one middle step above 0.20 X_m
                if not ((ri*frac - mpf('0.20'))*Xm > 2*g1log + 1 and ri*frac < mpf('0.30')): fails.add("A_i in middle band")
            # base case (6.11) + Pinsker
            log_def_bottom = lse(-ceil(200*Mf**20)*LN2, log(2*C43 + 8) - g2log)
            if not (log_def_bottom <= -90*Mf**20): fails.add("(6.11) bottom deficit <= e^{-90M^20}")
            tauJ = mpf(3)/8 - mpf(2)**(-J - 3)
            logTV = log(1 - tauJ) - BJ - (beta0/2**J)*LN2
            log_frac_fail = -90*Mf**20 + log(LT + LN2) - LN2 - 2*logTV
            logetaJ = -(J + 1)*log(100) - (J*(J - 1)//2 + 6*J)*LN2
            if not (log_frac_fail < logetaJ): fails.add("base case fraction < eta_J")
            for i in range(J):
                Bi = beta0*LT/2**i              # beta_i log T
                bi1 = beta0/2**(i + 1)
                logdel = -(i + 6)*LN2
                logeta = -(i + 1)*log(100) - (i*(i - 1)//2 + 6*i)*LN2
                # M^3 iterations fit between A_i and A_{i+1}: gap*Bi > 2M^3(ceil(M^3)+2)
                if not (gap*Bi > 2*g1log*(ceil(Mf**3) + 2)): fails.add("(6.10) M^3 iterations fit")
                # eps_i = 2^{-ceil M^3} + (2 C43 + 8) g1   (iteration + preservation)
                logeps = lse(-ceil(Mf**3)*LN2, log(2*C43 + 8) - g1log)
                # kappa_i <= CD * 2 T^{n_exp beta_i} T^{r_{i+1}} / (T^{r_i} e^{-2M^3(ceil M^3 +1)} / 2)
                logkappa = log(CD) + 2*LN2 + n_exp*Bi - gap*Bi + 2*g1log*(ceil(Mf**3) + 1)
                if not (logkappa <= -Mf**3): fails.add("(6.16) kappa <= e^{-M^3}")
                if not (lse(logeps, logkappa) <= logeta + logdel + log(bi1) - log(16)): fails.add("(5.4) eps+kappa budget")
                # (5.4) first: eta' <= eta delta/100 holds with equality by (6.13) (checked exactly elsewhere)
                # (5.5a): p exp(-delta^2 n p^{-beta}/2) <= delta/100, p in [T,2T], n >= T^{n_exp beta_i}
                lhs = 2*logdel + (n_exp - 1)*Bi - (beta0/2**i)*LN2 - LN2
                if not (lhs > log(LT + LN2 + log(100) - logdel)): fails.add("(5.5a) concentration")
                # (5.5b): delta^{-1} < p^{beta'/2}, p >= T
                if not (-logdel < bi1*LT/2): fails.add("(5.5b)")
                # (5.6): log(2e/delta) <= (beta'/4) log T
                if not (log(2*mp.e) - logdel <= bi1*LT/4): fails.add("(5.6)")
    return sorted(fails), maxJ, float(logB)

if __name__ == "__main__":
    print("== actual parameters (g0=1e-3, l0=15, a0=1/4, C43=100, CD=1e3) ==")
    for M in [30, 34, 36, 40, 50, 60, 70, 80, 84, 86, 90, 100, 120, 160]:
        f, J, lB = run(M)
        print(f"M={M}: maxJ={J}  logB={lB:.1f}  fails={f}", flush=True)
    print("== heavier hidden constants (C43=1e6, CD=1e9, g0=1e-6) at M=90,120 ==")
    for M in [90, 120]:
        f, J, lB = run(M, C43=mpf('1e6'), CD=mpf('1e9'), g0=mpf('1e-6'))
        print(f"M={M}: maxJ={J}  logB={lB:.1f}  fails={f}", flush=True)
    print("== NEGATIVE CONTROLS (each must FAIL the named check) ==")
    f, _, _ = run(100, n_exp=mpf(1));                 print("NC1 n_i=T^{beta_i} (no 6/5):", f)
    f, _, _ = run(100, gap=1, n_exp=mpf(6)/5);        print("NC2 r_i-r_{i+1}=beta_i:", f)
    f, _, _ = run(100, g1log=lambda M: M);            print("NC3 g1=e^{-M}:", f)
    f, _, _ = run(100, g2log=lambda M: M**3);         print("NC4 g2=e^{-M^3}:", f)
