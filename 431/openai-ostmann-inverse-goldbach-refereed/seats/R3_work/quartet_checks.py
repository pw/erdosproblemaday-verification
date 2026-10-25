# Check the quartet algebra of §6 (eqs. tree-difference-ratio, tree-held-square, tree-p-square) in F_q,
# the 4th-moment inequality (tree-fourth-moment) and the principal subtraction, with failing controls.
import random, itertools, math
random.seed(7)
q = 1000003
inv = lambda a: pow(a % q, q-2, q)
U = lambda: random.randrange(1, q)
bad = 0; checks = 0; ctrl_fail = 0
for trial in range(2000):
    sn, sp, sm = U(), U(), U()          # s_n, s_{n,+}, s_{n,-}
    s1, s2, s3, s4 = U(), U(), U(), U() # bottom frequencies s_{L,+}, s_{L,-}, s_{R,+}, s_{R,-}
    Dp, un, uL, uR = U(), U(), U(), U()
    A, B = U(), U()                     # current entries X_{n,+}, X_{n,-}
    Cp, Cm = U(), U()                   # C_{n,+}, C_{n,-}
    C1 = U(); C2 = un*Cp*inv(C1) % q    # consistency C1*C2 = u_n C_{n,+}
    C3 = U(); C4 = un*Cm*inv(C3) % q
    M1, M2, M3, M4 = U(), U(), U(), U()
    Hp = A*Cp*M1*M2 % q; Hm = B*Cm*M3*M4 % q
    pst = (sp*Hm - sm*Hp) * inv(sn*un) % q
    if pst == 0: continue
    y = sn*inv(Dp*Hp*Hm) % q
    d = sp*inv(Dp*pst*un*Hp) % q; e_ = sm*inv(Dp*pst*un*Hm) % q
    # child L: entries (p*, A); H_{L,+}=p* C1 M1, H_{L,-}=A C2 M2
    HL1, HL2 = pst*C1*M1 % q, A*C2*M2 % q
    HR1, HR2 = pst*C3*M3 % q, B*C4*M4 % q
    # child's own y formula must agree with parent display (consistency)
    checks += 1
    if d != s_L if False else False: pass
    sL, sR = sp, sm
    dL_own = sL*inv(Dp*HL1*HL2) % q
    eR_own = sR*inv(Dp*HR1*HR2) % q
    if dL_own != d or eR_own != e_: bad += 1
    if (d - e_) % q != y: bad += 1
    pL = (s1*HL2 - s2*HL1)*inv(sL*uL) % q
    if pL == 0: continue
    yL1 = s1*inv(Dp*pL*uL*HL1) % q; yL2 = s2*inv(Dp*pL*uL*HL2) % q
    if (yL1 - yL2) % q != d: bad += 1
    tL = yL1*inv(yL2) % q          # free = L+ (M1), held = L- (M2)  -> friendly (held uses residual A)
    lhs = tL*inv(d) % q
    rhs = Dp*s1*inv(s2*sL) % q * HL2 % q * HL2 % q
    if lhs != rhs: bad += 1
    # control: wrong exponent (H_held^1) must fail
    if lhs == Dp*s1*inv(s2*sL)*HL2 % q: ctrl_fail += 1
    # p*^2 formula
    if pst*pst % q != sp*sm*inv(sn*Dp*un*un) % q * y % q * inv(d*e_) % q: bad += 1
    if pst % q == sp*sm*inv(sn*Dp*un*un) % q * y % q * inv(d*e_) % q: ctrl_fail += 1
print("quartet algebra: trials", checks, "failures", bad, "| control coincidences (should be ~0):", ctrl_fail)

# 4th moment inequality: (1/(q-1)) sum_alpha sum_a |sum_b w(b) alpha(a-b)|^4 <= 2 q r_w^2 + J^4,
# and principal contribution >= J^4 - 3J^4/(q-1).
import cmath
for q2 in (11, 13, 17, 19):
    g = next(x for x in range(2,q2) if all(pow(x,(q2-1)//p,q2)!=1 for p in {p for p in range(2,q2) if (q2-1)%p==0 and all(p%r for r in range(2,p))}))
    dlog = {}; x = 1
    for k in range(q2-1): dlog[x] = k; x = x*g % q2
    ch = lambda j, x: 0 if x % q2 == 0 else cmath.exp(2j*math.pi*j*dlog[x % q2]/(q2-1))
    for rep in range(5):
        w = [random.random()**3 for _ in range(q2)]
        J = sum(w); r = sum(v*v for v in w)
        tot = 0; princ = 0
        for j in range(q2-1):
            for a in range(q2):
                v = abs(sum(w[b]*ch(j, a-b) for b in range(q2)))**4
                tot += v
                if j == 0: princ += v
        tot /= (q2-1); princ /= (q2-1)
        ok1 = tot <= 2*q2*r*r + J**4 + 1e-9
        ok2 = princ >= J**4 - 3*J**4/(q2-1) - 1e-9
        ctrl = tot <= q2*r*r + 0.5*J**4   # deliberately too-strong bound: expected to FAIL sometimes
        print(f"q={q2} 4th-moment ok={ok1} principal-lower ok={ok2} | control(too-strong) holds={ctrl}  ratio={tot/(2*q2*r*r+J**4):.3f}")
