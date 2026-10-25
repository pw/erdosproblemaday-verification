# Toy check of (5.14), the product-formula cancellation, and the flank support (5.15)
# in N = Q(i), using the ACTUAL state definitions of Section 4.4:
#   nonarch entry v: A-class  = classes of |z_x - z_x'|_v <= e^{-s}  (labels = first vertex in fixed order)
#                    B1-class = classes of |w_x - w_x'|_v <= e^{s}
#   arch entry sigma: A = half-open grid cell of sigma(z_x), side e^{-s}; B1 = cell of sigma(w_x), side e^{s};
#                     one fixed fractional shift per grid, scaled with the side at every level.
# Weighted places of Q(i) (d_N = 2): 2 archimedean entries (id, conj), weight 1/2 each;
#   split l=1 mod 4: two places, 1 copy each; l=2 ramified (pi=1+i): 2 copies; l=3 mod 4 inert: 2 copies.
#   normalisation |l|_p = 1/l.
import sys, math, random, itertools
from fractions import Fraction as F
from sympy import factorint
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
MODE = sys.argv[2] if len(sys.argv)>2 else "paper"   # paper | swapN | nolog2 | halflog2 | wrongscale

class G:
    __slots__=("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return G(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return G(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return G(s.a*o.a-s.b*o.b, s.a*o.b+s.b*o.a)
    def conj(s): return G(s.a,-s.b)
    def norm(s): return s.a*s.a+s.b*s.b
    def inv(s): n=s.norm(); return G(s.a/n,-s.b/n)
    def iszero(s): return s.a==0 and s.b==0
    def __eq__(s,o): return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return f"({s.a}+{s.b}i)"

def gauss_prime_over(l):
    if l==2: return [G(1,1)]
    if l%4==3: return [G(l,0)]
    for a in range(1,int(l**0.5)+1):
        b2=l-a*a; b=int(round(b2**0.5))
        if b*b==b2: return [G(a,b),G(a,-b)]
    raise ValueError(l)

def divides(pi,g):  # g Gaussian integer
    q=g*pi.conj(); n=pi.norm()
    return (q.a/n).denominator==1 and (q.b/n).denominator==1

def ord_int(pi,g):  # g nonzero Gaussian integer
    o=0
    while divides(pi,g):
        q=g*pi.conj(); g=G(q.a/pi.norm(),q.b/pi.norm()); o+=1
    return o

def ordpi(pi,x):
    n=math.lcm(x.a.denominator,x.b.denominator); g=G(x.a*n,x.b*n)
    return ord_int(pi,g)-ord_int(pi,G(n,0))

def primes_of(x):
    s=set()
    for num in (x.norm().numerator, x.norm().denominator):
        s|=set(factorint(num).keys())
    return s

def places_for(elts):
    ps=set()
    for x in elts: ps|=primes_of(x)
    out=[]
    for l in sorted(ps):
        for pi in gauss_prime_over(l):
            e=2 if l==2 else 1
            copies=2 if (l==2 or l%4==3) else 1
            out.append(("na",l,pi,e,copies))
    out.append(("arch","id",None,None,1)); out.append(("arch","conj",None,None,1))
    return out

def logabs_sym(x,pl):
    """log|x|_v as dict prime->Fraction coefficient of log(prime)"""
    if pl[0]=="na":
        _,l,pi,e,_=pl
        return {l: F(-ordpi(pi,x),e)}
    n=x.norm(); d={}
    for p,k in factorint(n.numerator).items(): d[p]=d.get(p,0)+F(k,2)
    for p,k in factorint(n.denominator).items(): d[p]=d.get(p,0)-F(k,2)
    return d
def sym_add(*ds):
    out={}
    for c,d in ds:
        for p,k in d.items(): out[p]=out.get(p,0)+c*k
    return {p:k for p,k in out.items() if k!=0}
def sym_val(d): return sum(float(k)*math.log(p) for p,k in d.items())

def emb(pl,x):
    return complex(float(x.a),float(x.b)) if pl[1]=="id" else complex(float(x.a),-float(x.b))

# --- unit Gaussian rationals (|d|=1): jumps of real unit edges
UNITS=[G(F(3,5),F(4,5)),G(F(4,5),F(3,5)),G(F(5,13),F(12,13)),G(F(12,13),F(5,13)),G(F(8,17),F(15,17)),
       G(F(-3,5),F(4,5)),G(F(3,5),F(-4,5)),G(0,1),G(-1,0),G(F(7,25),F(24,25)),G(F(20,29),F(21,29)),
       G(F(33,65),F(56,65)),G(F(63,65),F(16,65)),G(F(-5,13),F(12,13)),G(F(9,41),F(40,41))]
for u in UNITS: assert u.norm()==1

LOG2=math.log(2)
def cv_add(pl):
    if pl[0]=="na": return 0.0
    return {"paper":LOG2,"swapN":LOG2,"wrongscale":LOG2,"nolog2":0.0,"halflog2":0.5*LOG2}[MODE]

viol=0; checks=0; pf_fail=0; e514_fail=0; consist_fail=0; pairs=0; maxT=0
EXTRA=[G(F(5,3),F(2,7)),G(F(-2,9),F(5,4)),G(F(7,6),F(-1,10))]
NU=int(sys.argv[5]) if len(sys.argv)>5 else 6
PAIRS=list(itertools.permutations(UNITS[:NU],2))
for d,dp in PAIRS:
  for exper in ("Q","P"):
    pairs+=1
    if exper=="Q":
        base=G(F(1,3),F(2,7)); y1=base+d; y2=base+dp     # base centre q, points p=q+d, r=q+d'
    else:
        base=G(F(2,5),F(-1,11)); y1=base-d; y2=base-dp   # base point p, centres q=p-d, q'=p-d'
    Z={ 'x':base,'y1':y1,'y2':y2 }
    W={k:v.conj() for k,v in Z.items()}                   # real points: w = conj(z)
    # edge jump on edge (point,centre): d_e = z_point - z_centre ; w-jump = 1/d_e
    if exper=="Q": de1=Z['y1']-Z['x']; de2=Z['y2']-Z['x']
    else:          de1=Z['x']-Z['y1']; de2=Z['x']-Z['y2']
    assert de1==d and de2==dp
    assert (W['y1']-W['x'] if exper=="Q" else W['x']-W['y1'])==d.inv()
    verts=[('x',base),('y1',y1),('y2',y2)]+[(f"e{i}",z) for i,z in enumerate(EXTRA)]
    elts=[d,dp,d-dp,d.inv()-dp.inv()]+[a-b for (_,a),(_,b) in itertools.combinations(verts,2)]
    PL=places_for(elts)
    tot514=F(0); total={}
    for pl in PL:
        w=F(1,2)*pl[4]           # weight 1/d_N per copy
        n1=sym_add((-1,logabs_sym(d,pl))); n2=sym_add((-1,logabs_sym(dp,pl)))
        u=sym_add((-1,logabs_sym(d-dp,pl)))
        b,bp = (n1,n2) if sym_val(n1)<=sym_val(n2) else (n2,n1)
        alpha=sym_add((1,u),(-1,b))
        lhs=sym_add((-1,logabs_sym((d-dp)*(d.inv()-dp.inv()),pl)))
        rhs=sym_add((2,alpha),(-1,bp),(1,b))
        if lhs!=rhs: e514_fail+=1
        total=sym_add((1,total),(w,lhs))
        bv,bpv,av=sym_val(b),sym_val(bp),sym_val(alpha)
        cv=cv_add(pl); T=av+cv; maxT=max(maxT,T)
        if pl[0]=="arch": assert av>=-LOG2-1e-12
        # --- scan thresholds with the actual state definitions
        n1v,n2v=sym_val(n1),sym_val(n2)
        lo=min(bv-abs(T),bv)-4; hi=max(bpv+abs(T),bpv)+4
        NG=int(sys.argv[3]) if len(sys.argv)>3 else 600
        NS=int(sys.argv[4]) if len(sys.argv)>4 else 8
        grid=[lo+(hi-lo)*i/NG for i in range(NG+1)]
        breaks=[n1v,n2v]
        if pl[0]=="na":
            nv=len(verts); zc=[v for _,v in verts]; wc=[v.conj() for _,v in verts]
            LZ={(i,j):sym_val(logabs_sym(zc[i]-zc[j],pl)) for i,j in itertools.combinations(range(nv),2)}
            LW={(i,j):sym_val(logabs_sym(wc[i]-wc[j],pl)) for i,j in itertools.combinations(range(nv),2)}
            breaks+= [-x for x in LZ.values()]+list(LW.values())
            grid+= [t+e for t in breaks for e in (-1e-6,1e-6)]
            def cls(L,thr):
                par=list(range(nv))
                def f(i):
                    while par[i]!=i: i=par[i]
                    return i
                for (i,j),val in L.items():
                    if val<=thr+1e-12: par[f(j)]=f(i)
                # ultrametric => relation already transitive: verify
                for (i,j),val in L.items():
                    assert (f(i)==f(j))==(val<=thr+1e-12)
                return [min(k for k in range(nv) if f(k)==f(i)) for i in range(nv)]
            shifts=[None]
        else:
            zA=[emb(pl,v) for _,v in verts]; wB=[emb(pl,v.conj()) for _,v in verts]
            shifts=[((random.random(),random.random()),(random.random(),random.random())) for _ in range(NS)]+[((0.,0.),(0.,0.)),((.5,.5),(.5,.5))]
            def cell(c,side,shift): return (math.floor(c.real/side+shift[0]),math.floor(c.imag/side+shift[1]))
        for sh in shifts:
          for s in grid:
            if any(abs(s-t)<1e-9 for t in (n1v,n2v)): continue
            Y1=1 if n1v>s else 0; Y2=1 if n2v>s else 0
            if pl[0]=="na":
                Alab=cls(LZ,-s); Blab=cls(LW,-s if MODE=="wrongscale" else s)
                Am=Alab[1]==Alab[2]; Bm=Blab[1]==Blab[2]
                for j,Y in ((1,Y1),(2,Y2)):
                    Aj=Alab[0]==Alab[j]; Bj=Blab[0]==Blab[j]
                    ok=(Y==1 and Aj and not Bj) or (Y==0 and Bj and not Aj)
                    if MODE!="wrongscale" and not ok: consist_fail+=1
            else:
                sideA=math.exp(-s); sideB=math.exp(-s) if MODE=="wrongscale" else math.exp(s)
                Am=cell(zA[1],sideA,sh[0])==cell(zA[2],sideA,sh[0])
                Bm=cell(wB[1],sideB,sh[1])==cell(wB[2],sideB,sh[1])
            if MODE=="swapN": pos=(Y1==Y2==1 and Am) or (Y1==Y2==0 and Bm)
            else:             pos=(Y1==Y2==1 and Bm) or (Y1==Y2==0 and Am)
            if pos:
                checks+=1
                inside=(bv-T-1e-9<=s<=bv+1e-9) or (bpv-1e-9<=s<=bpv+T+1e-9)
                if not inside:
                    viol+=1
                    if viol<=3: print("  violation:",exper,d,dp,pl[0],pl[1],"s=%.4f b=%.4f b'=%.4f T=%.4f"%(s,bv,bpv,T))
    if total!={}: pf_fail+=1
print("MODE",MODE,"pairs",pairs,"(5.14) exact failures",e514_fail,"product-formula sum!=0:",pf_fail)
print("positive-eligible (s,place,shift) samples",checks,"outside (5.15):",viol,"max T_v",round(maxT,3))
if MODE in("paper","nolog2","halflog2","swapN"): print("Lemma 4.5 nonarch consistency failures:",consist_fail)
