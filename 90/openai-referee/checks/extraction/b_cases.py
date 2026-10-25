# Brute-force check of the pointwise combinatorics in Lemma 7.1 (7.3) and Lemma 7.3.
# Model of one good rare level: states (A,B1) with labels in {0,1,2}; dominant label ell=0 in the
# "relevant" coordinate (B1 if minority bit r=1, A if r=0).  Bits Y in {0,1} free; an edge is
# CONSISTENT iff (Y=1 and A agree and B1 differ) or (Y=0 and B1 agree and A differ)  [§4.4].
import itertools, sys
LAB = [0,1,2]
STATES = list(itertools.product(LAB, LAB))
def consistent(x, y, Y):
    Aeq, Beq = x[0]==y[0], x[1]==y[1]
    return (Y==1 and Aeq and not Beq) or (Y==0 and Beq and not Aeq)
def exc(x, r):           # exception indicator: relevant coordinate label != 0
    return int((x[1] if r==1 else x[0]) != 0)
def N_event(q, qq, Y1, Y2):   # nonshared-coordinate match of the two opposite endpoints
    if Y1==1 and Y2==1: return q[1]==qq[1]      # B1 match
    if Y1==0 and Y2==0: return q[0]==qq[0]      # A match
    return False

def check(sigma_sign=+1, residual_has_XX=True, verbose=False):
    bad = 0
    for r in (0,1):
        b = 1-r; sigma = (1 if r==1 else -1)*sigma_sign
        # --- Lemma 7.3 identity: |Y_pq - (b+sigma(Xp+Xq))| <= 2(XpXq + Ipq)
        for p, q in itertools.product(STATES, STATES):
            for Y in (0,1):
                Xp, Xq, I = exc(p,r), exc(q,r), int(not consistent(p,q,Y))
                res = abs(Y - (b + sigma*(Xp+Xq)))
                bound = 2*((Xp*Xq if residual_has_XX else 0) + I)
                if res > bound:
                    bad += 1
                    if verbose and bad<=3: print("  7.3-identity FAIL r=%d p=%s q=%s Y=%d res=%d bound=%d"%(r,p,q,Y,res,bound))
                if Xp*Xq==0 and I==0 and res!=0:
                    bad += 1
        # --- Lemma 7.1 (7.3): P+ >= 2X - 2(U+V+I+I'), N <= U+V+I+I'
        for p, q, qq in itertools.product(STATES, STATES, STATES):
            for Y1, Y2 in itertools.product((0,1),(0,1)):
                X, U, V = exc(p,r), exc(q,r), exc(qq,r)
                I, I2 = int(not consistent(p,q,Y1)), int(not consistent(p,qq,Y2))
                Pplus = 2*X*int(Y1==r and Y2==r and N_event(q,qq,Y1,Y2))
                Nn = abs(Y1-Y2)
                s = U+V+I+I2
                if not (Pplus >= 2*X - 2*s and Nn <= s): bad += 1
                if not (Pplus - Nn >= 2*X - 3*s): bad += 1
        # --- Lemma 7.3 (7.9) pointwise: |Ypq-Yrq| >= Xp+Xr-2(XpXr+XpXq+XrXq+Ipq+Irq)
        for p, q, rr in itertools.product(STATES, STATES, STATES):
            for Y1, Y2 in itertools.product((0,1),(0,1)):
                Xp, Xq, Xr = exc(p,r), exc(q,r), exc(rr,r)
                I1, I2 = int(not consistent(p,q,Y1)), int(not consistent(rr,q,Y2))
                lhs = abs(Y1-Y2)
                rhs = Xp+Xr-2*(Xp*Xr+Xp*Xq+Xr*Xq+I1+I2)
                if lhs < rhs: bad += 1
                # (7.8) integrand: |(Ypq-Yrq) - sigma(Xp-Xr)| <= 2(XpXq+XrXq+Ipq+Irq)
                lhs8 = abs((Y1-Y2) - sigma*(Xp-Xr))
                rhs8 = 2*((Xp*Xq + Xr*Xq) if residual_has_XX else 0) + 2*(I1+I2)
                if lhs8 > rhs8:
                    bad += 1
    return bad

print("paper's table (sigma=+1 iff minority bit 1, residual 2(XpXq+I)):  violations =", check())
print("CONTROL sigma sign flipped:                                       violations =", check(sigma_sign=-1))
print("CONTROL residual without the XpXq term:                           violations =", check(residual_has_XX=False, verbose=True))
