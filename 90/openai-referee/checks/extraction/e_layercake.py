# Lemma 7.2 bookkeeping on a random finite bipartite graph: layer-cake identity
#   E_E[min(H_p,H_q) 1{H_p > R}] = int_0^inf P_E(F_u, G_u) du,  F_u={H_p > max(u,R)}, G_u={H_q > u},
#   int_0^inf mu(F_u) du = E_mu[H_p 1{H_p>R}] = A,   int kappa(G_u) du = E_kappa H_q,
# the Cauchy-Schwarz step, and the distinctness factor (1 - 1/d(p)) for two uniform neighbours.
import random
from fractions import Fraction as Fr
random.seed(3)
P, Q = range(40), range(60)
E = [(p,q) for p in P for q in Q if random.random() < 0.15]
Hp = {p: Fr(random.choice([0,0,0,1,2,5,9,30])) for p in P}
Hq = {q: Fr(random.choice([0,0,1,3,4,7,12])) for q in Q}
R = Fr(4); nE = len(E)
deg = {p: sum(1 for e in E if e[0]==p) for p in P}; degq = {q: sum(1 for e in E if e[1]==q) for q in Q}
lhs = sum(min(Hp[p],Hq[q]) for (p,q) in E if Hp[p] > R) / nE
def PE(u): return Fr(sum(1 for (p,q) in E if Hp[p] > max(u,R) and Hq[q] > u), nE)
def mu(u): return Fr(sum(deg[p] for p in P if Hp[p] > max(u,R)), nE)
def ka(u): return Fr(sum(degq[q] for q in Q if Hq[q] > u), nE)
bps = sorted(set([Fr(0)] + list(Hp.values()) + list(Hq.values()) + [R]))
def integ(f):   # f is a right-continuous step function constant on [bps[i], bps[i+1]); f(u)=0 beyond max
    return sum(f(bps[i]) * (bps[i+1]-bps[i]) for i in range(len(bps)-1))
I_PE, I_mu, I_ka = integ(PE), integ(mu), integ(ka)
A = sum(Fr(deg[p], nE)*Hp[p] for p in P if Hp[p] > R)
Ekq = sum(Fr(degq[q], nE)*Hq[q] for q in Q)
print("layer cake:  E_E[min 1_T] =", lhs, " int P_E(F_u,G_u) du =", I_PE, " equal:", lhs == I_PE)
print("int mu(F_u) =", I_mu, "= A_t =", A, ":", I_mu == A, " ; int kappa(G_u) =", I_ka, "= E_kappa H_q =", Ekq, ":", I_ka == Ekq)
# Cauchy-Schwarz: int sqrt(h_P h_Q) <= sqrt(A * E H_q)
cs = sum(float(mu(bps[i])*ka(bps[i]))**0.5 * float(bps[i+1]-bps[i]) for i in range(len(bps)-1))
print("int sqrt(h_P h_Q) du = %.4f <= sqrt(A E_k H_q) = %.4f : %s" % (cs, float(A*Ekq)**0.5, cs <= float(A*Ekq)**0.5 + 1e-12))
# distinctness: P(q != q' | p) = 1 - 1/d(p) for two independent uniform neighbours
p0 = max(P, key=lambda p: deg[p]); d0 = deg[p0]
nb = [q for (p,q) in E if p == p0]
dist = Fr(sum(1 for a in nb for b in nb if a != b), d0*d0)
print("P(q != q' | p) =", dist, "= 1 - 1/d(p) =", 1 - Fr(1, d0), ":", dist == 1 - Fr(1, d0))
# CONTROL: dropping the max(u,R) (i.e. F_u = {H_p > u} intersect T computed WRONG as {H_p > u}) must disagree
def PEbad(u): return Fr(sum(1 for (p,q) in E if Hp[p] > u and Hq[q] > u), nE)
print("CONTROL F_u={H_p>u} (no tail restriction):", integ(PEbad), "!= lhs:", integ(PEbad) != lhs)
