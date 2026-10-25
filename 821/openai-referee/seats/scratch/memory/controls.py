# Negative controls: perturb ONE rule of the paper's memory evolution (RHS only) and check the identity breaks.
import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); C0 = frozenset({0})
P4 = [5, 7, 17, 19]; P5 = [5, 7, 17, 19, 29]; ID2 = [(0, 1)]
def case(name):
    if name == 'A1':
        return dict(P=P4, J=1, ell=1, patterns=[RAW], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=11)
    if name == 'C1':
        return dict(P=P4, J=1, ell=1, patterns=[RAW], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1,1,1], seed=31)
    if name == 'F1':   # two free labels forced EQUAL (path-data restriction applied to both sides)
        return dict(P=P5, J=2, ell=0, patterns=[RAW, frozenset({0,1})], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1,
                    kseq=[1,1], seed=61, edge_perms=[ID2]*2, flags=('free_equal_only',))
    if name == 'D1':
        return dict(P=P5, J=1, ell=1, patterns=[RAW, C0], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1,1,1],
                    seed=41, edge_patterns=[[0],[1],[0],[0]], edge_perms=[ID2]*4)
cname = sys.argv[1]
flagsets = sys.argv[2].split(',')
kw = case(cname)
bflags = tuple(kw.pop('flags', ()))
base = Toy(**kw, flags=bflags); L = base.lhs(); R0 = base.rhs_full()
print(f"case {cname}: paths={base._npaths} stats={base.stats}\n  LHS = {F.fmt(L)}\n  LHS ~ {F.approx(L):.12g}; unperturbed RHS equal: {L == R0}", flush=True)
for fl in flagsets:
    if fl.startswith('rho='):
        kw2 = dict(kw); kw2['rho'] = Fr(fl[4:]); t = Toy(**kw2, flags=bflags)
    else:
        t = Toy(**kw, flags=bflags + (fl,))
    R = t.rhs_full()
    d = F.sub(R, L)
    print(f"  control {fl:24s}: RHS ~ {F.approx(R):.12g}   equal={R == L}   RHS-LHS ~ {F.approx(d):.6g}", flush=True)
