# N3: (8.18) exact orthogonality u*sum_e (m_e - m/u)^2 = sum_{a=1}^{u-1} |S(a/u)|^2, with controls;
# and the large-sieve step of (8.19): sum_{u in bin} sum_{a=1}^{u-1}|S(a/u)|^2 <= (J + 4U^2) m  (MV constant 1),
# on small-prime-sieved sets (the actual shape used), plus the derived bound on exceptional residues.
import cmath, math, random
def primes(n):
    return [p for p in range(2,n+1) if all(p%q for q in range(2,int(p**.5)+1))]
random.seed(7)
def sieved(J,w):
    ps=primes(w); cl={t:random.randrange(t) for t in ps}
    return [j for j in range(J) if all(j%t!=cl[t] for t in ps)]
def S(seq,th): return sum(cmath.exp(2j*math.pi*j*th) for j in seq)
seq=sieved(3000,13); m=len(seq)
for u in [17,19,23]:
    me=[0]*u
    for j in seq: me[j%u]+=1
    lhs=u*sum((x-m/u)**2 for x in me)
    rhs=sum(abs(S(seq,a/u))**2 for a in range(1,u))
    rhs_ctrl=sum(abs(S(seq,a/u))**2 for a in range(0,u))   # control: includes a=0 -> must FAIL
    print("u=%d lhs=%.6f rhs=%.6f |diff|=%.2e  control(a=0 incl) diff=%.1f"%(u,lhs,rhs,abs(lhs-rhs),rhs_ctrl-lhs))
# large sieve over a prime bin [U,(1+xi)U]
def isp(n): return n>1 and all(n%q for q in range(2,int(n**.5)+1))
for (J,U,xi) in [(3000,40,0.5),(3000,60,0.3),(800,30,0.5)]:
    seq=sieved(J,13); m=len(seq)
    bin_=[u for u in range(U+1,int((1+xi)*U)+1) if isp(u)]
    tot=sum(abs(S(seq,a/u))**2 for u in bin_ for a in range(1,u))
    bound=(J+4*U*U)*m
    print("J=%d U=%d bin=%s  sum=%.0f  (J+4U^2)m=%.0f  ratio=%.3f"%(J,U,bin_,tot,bound,tot/bound))
