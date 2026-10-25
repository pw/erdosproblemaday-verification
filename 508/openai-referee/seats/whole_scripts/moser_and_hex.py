# Cross-check (numeric, 60 digits) of the final step (Lemma 8.8/8.9, eq. (8.4)-(8.6)) and the
# p.2 hexagon upper bound. The exact rational check is the cycles seat's (G); this is a
# whole-paper sanity pass with a control that must FAIL.
from decimal import Decimal as Dm, getcontext
getcontext().prec=60
s3,s11=Dm(3).sqrt(),Dm(11).sqrt()
def C(a,b): return (Dm(a),Dm(b))
def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def add(z,w): return (z[0]+w[0],z[1]+w[1])
def n2(z): return z[0]*z[0]+z[1]*z[1]
A=(s3/2,Dm(1)/2); B=(s3/2,-Dm(1)/2); T=(s3,Dm(0)); u=(Dm(5)/6,s11/6); O=(Dm(0),Dm(0))
G={'0':O,'A':A,'B':B,'T':T,'uA':mul(u,A),'uB':mul(u,B),'uT':mul(u,T)}
E=[('0','A'),('0','B'),('A','B'),('A','T'),('B','T'),('0','uA'),('0','uB'),('uA','uB'),('uA','uT'),('uB','uT'),('T','uT')]
rot=(Dm(35)/37,Dm(12)/37); sh=(Dm(-290)/250,Dm(149)/250)
Z={g:mul(rot,add(p,sh)) for g,p in G.items()}   # (8.6): z_g = rot*(g+shift)
def P(z): x,y=z; return y*y*(3*x*x-y*y)**2
def Pp(z): l=n2(z); return l**3*(1-l/4)*(l-1)**2
def check(Z,label):
    edge_err=max(abs(n2((Z[a][0]-Z[b][0],Z[a][1]-Z[b][1]))-1) for a,b in E)
    ok=True
    for g,z in Z.items():
        l=n2(z); good=(0<l<4) and P(z)<Pp(z); ok&=good
        print(f"  {label} {g:>2}: l={float(l):.6f}  P={float(P(z)):.6g}  P'={float(Pp(z)):.6g}  in-region={good}")
    print(f"  {label}: max |edge^2-1| = {float(edge_err):.2e}; all 7 in region: {ok}")
    return ok, edge_err
ok,err=check(Z,"placement")
assert ok and err<Dm(10)**-50
# CONTROL 1: misread (8.6) as rot*g+shift -> region membership must FAIL somewhere
Zc={g:add(mul(rot,p),sh) for g,p in G.items()}
okc,_=check(Zc,"CONTROL rot*g+shift")
# CONTROL 2: non-unit spindle (u with |u|=1.01) must break an edge
u2=(Dm(5)/6*Dm('1.01'),s11/6*Dm('1.01'))
Zb={**Z,'uT':mul(rot,add(mul(u2,T),sh))}
eb=max(abs(n2((Zb[a][0]-Zb[b][0],Zb[a][1]-Zb[b][1]))-1) for a,b in E)
print("  CONTROL non-unit u: max |edge^2-1| =",float(eb))
# Moser graph not 3-colourable (exhaustive)
import itertools
V=list(G); idx={v:i for i,v in enumerate(V)}
n3=sum(all(c[idx[a]]!=c[idx[b]] for a,b in E) for c in itertools.product(range(3),repeat=7))
n4=sum(all(c[idx[a]]!=c[idx[b]] for a,b in E) for c in itertools.product(range(4),repeat=7))
print("  proper 3-colourings of the 7-vertex graph:",n3,"| CONTROL proper 4-colourings:",n4)
# p.2 hexagon bound
r=Dm(2)/5
print("hexagon: 2r =",2*r,"<1 ;  (sqrt21-2) r =",(Dm(21).sqrt()-2)*r,">1 ; |2-omega|^2 = 4+2+1 =",4+2+1)
