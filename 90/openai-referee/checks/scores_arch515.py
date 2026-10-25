# Abstract archimedean entry: at a non-identity embedding z and w are independent complex coordinates,
# only the edge relation w_y - w_x = 1/(z_y - z_x) holds. Random base (z0,w0), random jumps d1,d2 (any size),
# endpoints z=z0+d_j, w=w0+1/d_j. States: A = half-open grid cell of z at side e^{-s}, B1 = cell of w at side e^{s},
# one fixed fractional shift per grid. Check that every s with
#   (Y1=Y2=1 and B1 match) or (Y1=Y2=0 and A match)
# lies in [b-T,b] U [b',b'+T], T = alpha + c, alpha = u - b, u = -log|d1-d2|, for c = log 2 (paper),
# and that c = 0 (control) FAILS; c = (1/2) log 2 is reported (sharp constant).
import random, math, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 11)
def cell(c,side,sh): return (math.floor(c.real/side+sh[0]),math.floor(c.imag/side+sh[1]))
res={}
for cname,cval in (("log2",math.log(2)),("halflog2",0.5*math.log(2)),("zero",0.0)):
    viol=0; pos=0; negT=0
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 11)
    for it in range(3000):
        z0=complex(random.gauss(0,3),random.gauss(0,3)); w0=complex(random.gauss(0,3),random.gauss(0,3))
        def rj():
            r=math.exp(random.gauss(0,1.5)); th=random.uniform(0,2*math.pi); return r*complex(math.cos(th),math.sin(th))
        d1=rj()
        mode=random.random()
        if mode<0.3: d2=d1*complex(1+random.gauss(0,0.05),random.gauss(0,0.05))   # near-equal jumps
        elif mode<0.45: d2=-d1*(1+random.gauss(0,0.02))                             # near-opposite (alpha ~ -log 2)
        else: d2=rj()
        n1=-math.log(abs(d1)); n2=-math.log(abs(d2)); b,bp=min(n1,n2),max(n1,n2)
        u=-math.log(abs(d1-d2)); alpha=u-b
        assert alpha>=-math.log(2)-1e-9          # triangle inequality
        T=alpha+cval
        if T<0: negT+=1
        zs=[z0+d1,z0+d2]; ws=[w0+1/d1,w0+1/d2]
        shA=(random.random(),random.random()); shB=(random.random(),random.random())
        lo=b-abs(T)-4; hi=bp+abs(T)+4
        for i in range(1201):
            s=lo+(hi-lo)*i/1200
            Y1=n1>s; Y2=n2>s
            Am=cell(zs[0],math.exp(-s),shA)==cell(zs[1],math.exp(-s),shA)
            Bm=cell(ws[0],math.exp(s),shB)==cell(ws[1],math.exp(s),shB)
            if (Y1 and Y2 and Bm) or ((not Y1) and (not Y2) and Am):
                pos+=1
                if not ((b-T-1e-9<=s<=b+1e-9) or (bp-1e-9<=s<=bp+T+1e-9)): viol+=1
    res[cname]=(pos,viol,negT)
    print(f"c_v={cname:9s} positive-eligible samples={pos} outside flanks={viol} (cases with T<0: {negT})")
