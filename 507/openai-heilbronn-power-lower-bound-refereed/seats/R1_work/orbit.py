# Lemma 4.2 check: BFS orbit of diag(1,B^b,B^e) under SL3(Z/h) (elementary generators), compare to c0*h^8/(D^3E^2)
import sys, math, itertools
def enc(M,h):
    x=0
    for v in M: x=x*h+v
    return x
def dec(x,h):
    M=[0]*9
    for i in range(8,-1,-1):
        M[i]=x%h; x//=h
    return M
def orbit_size(C,h,limit=8_000_000):
    seen={enc(C,h)}; frontier=[enc(C,h)]
    while frontier:
        nf=[]
        for x in frontier:
            M=dec(x,h)
            rows=[M[0:3],M[3:6],M[6:9]]
            for i in range(3):
                for j in range(3):
                    if i==j: continue
                    # E_ij(1) * M : row_i += row_j
                    nr=[list(r) for r in rows]
                    nr[i]=[(nr[i][c]+rows[j][c])%h for c in range(3)]
                    y=enc(nr[0]+nr[1]+nr[2],h)
                    if y not in seen:
                        seen.add(y); nf.append(y)
                        if len(seen)>limit: return None
        frontier=nf
    return len(seen)
def predicted(B,k,b,e):
    h=B**k; D=B**b; E=B**e
    G=h**9*(1-1/B)*(1-1/B**2)*(1-1/B**3)
    # exact stabilizer in GL: g with col1=e1, col2 in e2+Ann(D)^3, col3 in e3+Ann(E)^3, invertible
    return 21/64*h**8/(D**3*E**2)
def exact_formula(B,k,b,e):
    # enumerate stabilizer of Delta in GL3(Z/h) explicitly, compute |O| = |SL3|/|H cap SL3|
    h=B**k; D=B**b; E=B**e
    annD=[x for x in range(h) if (x*D)%h==0]
    annE=[x for x in range(h) if (x*E)%h==0]
    Hsize=0; Hsl=0; dets=set()
    for c2 in itertools.product(annD,repeat=3):
        for c3 in itertools.product(annE,repeat=3):
            g=[[1,c2[0],c3[0]],[0,(1+c2[1])%h,c3[1]],[0,c2[2],(1+c3[2])%h]]
            det=(g[0][0]*(g[1][1]*g[2][2]-g[1][2]*g[2][1])-g[0][1]*(g[1][0]*g[2][2]-g[1][2]*g[2][0])+g[0][2]*(g[1][0]*g[2][1]-g[1][1]*g[2][0]))%h
            if det%B==0: continue
            Hsize+=1; dets.add(det)
            if det==1: Hsl+=1
    G=round(h**9*(1-1/B)*(1-1/B**2)*(1-1/B**3))
    phi=h-h//B
    SL=G//phi
    return SL//Hsl, Hsize, len(dets), Hsl
cases=[(2,2),(3,2),(2,3),(5,2)]
for (B,k) in cases:
    h=B**k
    for b in range(k+1):
        for e in range(b,k+1):
            pred=predicted(B,k,b,e)
            ex,Hs,nd,Hsl=exact_formula(B,k,b,e)
            D=B**b;E=B**e
            C=[1,0,0,0,D%h,0,0,0,E%h]
            if ex<=3_000_000:
                o=orbit_size(C,h)
            else:
                o=None
            print(f"h={h} (B={B},k={k}) b={b} e={e}: BFS orbit={o} formula-orbit={ex} bound c0*h^8/(D^3E^2)={pred:.1f} ratio={ex/pred:.3f} |H|={Hs}<=D^3E^3={D**3*E**3} |detH|={nd}>=(1-1/B)E={(1-1/B)*E:.1f}",flush=True)
