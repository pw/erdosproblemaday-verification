import sys, math, random
sys.path.insert(0, '.')
from lemma61_check import build, delta_hyp
def lhs(parent, ln, al):
    N=len(parent); _,_,d=build(parent,ln)
    return sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(N) for xp in range(N) for y in range(N))
for dl in [0.4, 0.1, 0.01]:
    # path a-b-c, masses delta/2, 1-delta, delta/2
    parent=[0,0,1]; ln=[0,1.0,1.0]; al=[dl/2,1-dl,dl/2]   # root a=0, b=1, c=2
    print('path3 delta=%.2f  delta_hyp=%.3f  LHS/L=%.4e  LHS/(delta L)=%.3f' % (dl, delta_hyp(parent,ln,al), lhs(parent,ln,al)/2, lhs(parent,ln,al)/(2*dl)))
    # star: centre mass 0, k leaves; one heavy leaf mass 1-delta/2... edges each must separate >= delta/2
    k=int(round(2/dl)); parent=[0]+[0]*k; ln=[0]+[1.0]*k; al=[0]+[1.0/k]*k
    dh=delta_hyp(parent,ln,al)
    print('   uniform star k=%d delta_hyp=%.3f LHS/L=%.4e LHS/(delta_hyp L)=%.3f' % (k, dh, lhs(parent,ln,al)/k, lhs(parent,ln,al)/(dh*k)))
