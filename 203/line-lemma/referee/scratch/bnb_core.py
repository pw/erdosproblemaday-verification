S=E.denominator
for *_,w in lum: S=S*w.denominator//gcd(S,w.denominator)
lum.sort(key=lambda x:(-x[2], -x[1]))
wi=[int(w*S) for *_,w in lum]; ii=[i for _,i,_ in lum]
need=S-int(E*S)          # each cell needs lumpy mass >= need
tau=np.arange(Mp)
masks=[[ (tau%i==c) for c in range(i)] for i in ii]
suffix=[0]*(len(lum)+1)
for j in range(len(lum)-1,-1,-1): suffix[j]=suffix[j+1]+wi[j]
nodes=0; t0=time.time(); timed_out=False
def bound_ok(W,j):
    # return False if provably infeasible
    order=np.argsort(W, kind='stable')
    Ws=W[order]
    if Ws[0]+suffix[j] < need: return False
    # cell sets T = k lowest cells, k = 2..Mp (check a few sizes)
    for k in (2,3,4,6,8,12,16,24,32,48,Mp):
        if k>Mp: break
        T=order[:k]
        tot=int(Ws[:k].sum())
        for jj in range(j,len(lum)):
            i=ii[jj]
            cnt=np.bincount(T%i, minlength=i).max()
            tot+=wi[jj]*int(cnt)
            if tot>=need*k: break
        if tot < need*k: return False
    return True
def dfs(j,W):
    global nodes,timed_out
    nodes+=1
    if nodes%20000==0 and time.time()-t0>TL: timed_out=True; return True
    if j==len(lum): return bool((W>=need).all())
    if not bound_ok(W,j): return False
    rng=[0] if (sym and j==0) else range(ii[j])
    for c in rng:
        W2=W.copy(); W2[masks[j][c]]+=wi[j]
        if dfs(j+1,W2): return True
        if timed_out: return True
    return False
W0=np.zeros(Mp,dtype=np.int64)
found=dfs(0,W0)
print(json.dumps({'N':N,'dir':[a,b],'Mp':Mp,'lumpy':len(lum),'sym':sym,'result':('TIMEOUT' if timed_out else ('FEASIBLE' if found else 'INFEASIBLE (no class choice reaches 1 on every cell)')),'nodes':nodes,'secs':round(time.time()-t0,1)}),flush=True)
