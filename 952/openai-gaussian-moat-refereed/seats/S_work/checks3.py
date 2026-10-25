# Seat S: explicit parameter checks for Sections 6.1-6.4, all in log space (no exp of huge args).
# Unknown O_D constants -> generous stand-ins (CD=1e3, deficit constant c=1/2, O(M^6) taken exactly
# from the construction). Reports, per M, which explicit inequalities fail.
from mpmath import mp, mpf, log, ceil
mp.dps = 30
CD = mpf(1000); LN2 = log(2); beta0 = mpf(1)/200
def lse(a, b):  # log(e^a + e^b)
    m = max(a, b); return m + log(1 + mp.e**(min(a, b) - m))
def check(M):
    fails = set(); Mf = mpf(M)
    g1log = Mf**3; g2log = 100*Mf**20; g0log = log(1000)
    X = lambda m: mpf(100)**m
    mlo = (M+1)//2; XM = X(M); logN = 10*mpf('1.05')*XM
    nops = sum(mpf('0.5')*X(m)/(2*g0log) + mpf('0.1')*X(m)/(2*g1log) + mpf('0.05')*X(m)/(2*g2log) + 3
               for m in range(mlo, M+1))
    for (lo, glog) in [(mpf('0.8'), g0log), (mpf('0.20'), g1log), (mpf('0.05'), g2log)]:
        if not (lo*X(mlo) - glog > log(logN + log(nops) + 1)): fails.add("L6.1 log(1+S_V)<=2gV")
    for m in range(mlo+1, M+1):
        if not (mpf('0.05')*X(m) - g2log > mpf('1.3')*X(m-1)): fails.add("L6.1 band domination")
    for m in range(mlo, M+1):
        if not ((ceil(200*Mf**20)+2)*2*g2log < mpf('0.05')*X(m)): fails.add("bottom band capacity")
    # terminal deficit 2^{-200M^20} + 3CD e^{-100M^20} <= e^{-90M^20}
    if not (lse(-ceil(200*Mf**20)*LN2, log(3*CD) - 100*Mf**20) <= -90*Mf**20): fails.add("terminal deficit")
    maxJ = 0
    for m in range(mlo, M+1):
        for frac in [mpf(1), mpf('1.025'), mpf('1.05')]:
            logT = frac*X(m)
            if not (beta0*logT > Mf**20): fails.add("beta0 logT > M^20"); continue
            J = 0
            while beta0/2**J*logT > Mf**20: J += 1
            maxJ = max(maxJ, J); bJ = beta0/2**J
            if not (Mf**20/2 < bJ*logT <= Mf**20): fails.add("J range")
            r = mpf(1)/4; logeta = log(mpf(1)/100)
            rs, logetas, betas, logdel = [], [], [], []
            for i in range(J+1):
                rs.append(r); betas.append(beta0/2**i); logdel.append(-(i+6)*LN2); logetas.append(logeta)
                logeta = logeta + logdel[-1] - log(100); r -= 2*betas[-1]
            for i in range(J+1):
                rl = rs[i]*logT
                if not (mpf('0.23')*X(m) < rl <= mpf('0.2625')*X(m)): fails.add("r_i log T band")
                if not (rl - 2*g1log > mpf('0.20')*X(m) and rl < mpf('0.30')*X(m)): fails.add("A_i in middle band")
            for i in range(J):
                if not (2*betas[i]*logT > (ceil(g1log)+2)*2*g1log): fails.add("M^3 iterations fit")
                logeps = lse(-g1log*LN2, log(3*CD) - g1log)          # 2^{-M^3} + 3CD e^{-M^3}
                logsL = rs[i]*logT - 2*g1log - 2*g1log*ceil(g1log) - LN2
                logkappa = log(CD) + (mpf(6)/5*betas[i]*logT + LN2) + rs[i+1]*logT - logsL
                logrhs = logetas[i] + logdel[i] + log(betas[i+1]) - log(16)
                if not (lse(logeps, logkappa) <= logrhs): fails.add("(5.4) eps+kappa budget")
                if not (logkappa <= -g1log): fails.add("(6.16) kappa<=e^{-M^3}")
                logp = logT + LN2
                lhs_log = 2*logdel[i] + mpf(6)/5*betas[i]*logT - betas[i]*logp - LN2
                if not (lhs_log > log(logp + log(100) - logdel[i])): fails.add("(5.5a)")
                if not (-logdel[i] < betas[i+1]/2*logT): fails.add("(5.5b)")
                if not (log(2*mp.e) - logdel[i] <= betas[i+1]/4*logT): fails.add("(5.6)")
            logTV = log(mpf(5)/8) - bJ*(logT + LN2)
            logfrac = -90*Mf**20 + log(logT + LN2) - LN2 - 2*logTV
            if not (logfrac < logetas[J]): fails.add("base case")
    return sorted(fails), maxJ
for M in [30, 40, 50, 60, 70, 80, 90, 100, 120, 160, 200]:
    f, J = check(M)
    print(f"M={M}: maxJ={J} (6.65M={6.65*M:.0f}) failures={f}", flush=True)
