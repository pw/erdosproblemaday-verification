# Exact check of the §6 density bound for depth l=2 (r=4): the law of the 4 leaf arguments, over
# independent uniform leaf variables in U^4, has point masses <= 2^{r-1}/(q-1)^r on valid points.
import random, collections
random.seed(3)
def run(q):
    inv = lambda a: pow(a % q, q-2, q)
    U = lambda: random.randrange(1, q)
    worst = 0
    for rep in range(3):
        sn, sp, sm, s1, s2, s3, s4 = (U() for _ in range(7))
        Dp, un, uL, uR, A, B, Cp, Cm = (U() for _ in range(8))
        C1 = U(); C2 = un*Cp*inv(C1) % q; C3 = U(); C4 = un*Cm*inv(C3) % q
        cnt = collections.Counter()
        for M1 in range(1,q):
         for M2 in range(1,q):
          for M3 in range(1,q):
           for M4 in range(1,q):
            Hp = A*Cp*M1*M2 % q; Hm = B*Cm*M3*M4 % q
            pst = (sp*Hm - sm*Hp)*inv(sn*un) % q
            if pst == 0: continue
            HL1, HL2, HR1, HR2 = pst*C1*M1 % q, A*C2*M2 % q, pst*C3*M3 % q, B*C4*M4 % q
            pL = (s1*HL2 - s2*HL1)*inv(sp*uL) % q
            pR = (s3*HR2 - s4*HR1)*inv(sm*uR) % q
            if pL == 0 or pR == 0: continue
            args = (s1*inv(Dp*pL*uL*HL1) % q, s2*inv(Dp*pL*uL*HL2) % q,
                    s3*inv(Dp*pR*uR*HR1) % q, s4*inv(Dp*pR*uR*HR2) % q)
            cnt[args] += 1
        worst = max(worst, max(cnt.values()))
    return worst
for q in (7, 11, 13):
    w = run(q)
    print(f"q={q}: max multiplicity of a leaf-argument vector = {w}; claimed bound 2^(r-1) = 8; "
          f"CONTROL bound 2^(r-2)=4 violated: {w>4}")
