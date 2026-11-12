from fractions import Fraction as F
from math import prod
def isp(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
for lo,hi,c in [(503,641,F(19,10)),(1049,1483,F(19,10))]:
    ps=[p for p in range(lo,hi+1) if isp(p)]
    r=len(ps); m=ps[-2]*ps[-1]; P=prod(ps)
    # left: sum_{k<=m} (w(k)-c)^+, w = sum v_p
    L=F(0)
    # only k with w>=2 matter: pairs p_i p_j<=m, squares p^2<=m, cubes etc
    cnt2=sum(1 for i in range(r) for j in range(i+1,r) if ps[i]*ps[j]<=m)+sum(1 for p in ps if p*p<=m)
    assert all(p**3>m for p in ps) and all(ps[0]**2*ps[1]>m for _ in [0])
    L=cnt2*(2-c)
    a=P-m//2; b=a+m-1
    sq=0
    for p in ps:
        q=p*p; first=(a+q-1)//q*q
        k=first
        while k<=b:
            assert k!=P; sq+=1; k+=q
    # P contributes r-1; any other element with two primes? pair products > m/2 radius
    assert ps[0]*ps[1] > m//2
    R=(r-1)+sq  # each p^2 multiple has w=2 exactly? check p^3 impossible within: p^3 multiples
    print(lo,hi,'r',r,'m',m,'L',L,float(L),'R',R,'fails' , L>R, 'Sform L', F(r*(r-1)//2)*(2-c),'Sform R',r-1)
