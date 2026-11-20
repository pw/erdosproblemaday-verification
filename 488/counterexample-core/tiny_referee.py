import sys
def smooth(s,y):
    for p in range(2,y+1):
        while s%p==0: s//=p
    return s==1
def run(y,L,T,W):
    A=[s for s in range(T+1,L*T+1) if smooth(s,y)]
    S=set(A); Amin=[s for s in A if not any(d in S for d in range(2,s) if s%d==0)]
    X=W*T
    def Mvec(G):
        b=bytearray(X+1)
        for a in G:
            for k in range(a,X+1,a): b[k]=1
        return b
    bA=Mvec(A); bm=Mvec(Amin)
    assert bA==bm, "B differs"
    M=lambda b,x: sum(b[1:x+1])
    psi=lambda x: sum(1 for s in range(1,x+1) if smooth(s,y))
    rough=[u for u in range(1,W) if u==1 or all(u%p for p in range(2,y+1))]
    formula=sum(psi(X//u)-psi(T) for u in rough)
    n=L*T
    print(f"y={y} L={L} T={T} W={W} |A|={len(A)} |Amin|={len(Amin)} max(Amin)={max(Amin)}<=n={n} M(n)={M(bA,n)} |A|={len(A)} M(WT)={M(bA,X)} formula={formula} ok={M(bA,X)==formula and M(bA,n)==len(A)}")
for args in [(7,11,50,200),(7,9,40,150),(5,7,30,60),(11,12,20,300),(3,5,100,40)]:
    run(*args)
