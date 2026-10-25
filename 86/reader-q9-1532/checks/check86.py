# Own C4-freeness check for a subgraph of Q_n (two methods): (A) every 2-face {v,v^a,v^b,v^ab} has <=3 edges;
# (B) every pair of vertices has <=1 common neighbour in the subgraph. Controls: add an edge closing a square -> both reject.
import sys, itertools
def load(path,n):
    E=set()
    for ln in open(path):
        ln=ln.strip()
        if not ln or ln.startswith('#'): continue
        a,b=map(int,ln.split()[:2])
        assert 0<=a<2**n and 0<=b<2**n, (a,b)
        d=a^b; assert d and d&(d-1)==0, ('not a hypercube edge',a,b)
        e=(min(a,b),max(a,b)); assert e not in E, ('duplicate',e)
        E.add(e)
    return E
def faces_ok(E,n):
    bad=0
    for v in range(2**n):
        for i,j in itertools.combinations(range(n),2):
            if v>>i&1 or v>>j&1: continue
            a,b,c=v|1<<i, v|1<<j, v|1<<i|1<<j
            es=[(v,a),(v,b),(a,c),(b,c)]
            if all(e in E for e in es): bad+=1
    return bad
def common_ok(E,n):
    N=[set() for _ in range(2**n)]
    for a,b in E: N[a].add(b); N[b].add(a)
    bad=0
    for u in range(2**n):
        for w in range(u+1,2**n):
            if len(N[u]&N[w])>=2: bad+=1
    return bad
if __name__=='__main__':
    n=int(sys.argv[2]); E=load(sys.argv[1],n)
    f=faces_ok(E,n); c=common_ok(E,n)
    print(sys.argv[1],'edges',len(E),'full squares',f,'pairs with >=2 common nbrs',c)
    # control: find a square with exactly 3 edges and add the 4th
    for v in range(2**n):
        done=False
        for i,j in itertools.combinations(range(n),2):
            if v>>i&1 or v>>j&1: continue
            a,b,c_=v|1<<i, v|1<<j, v|1<<i|1<<j
            es=[(v,a),(v,b),(a,c_),(b,c_)]; miss=[e for e in es if e not in E]
            if len(miss)==1:
                E2=E|{miss[0]}; print('control: +',miss[0],'-> squares',faces_ok(E2,n),'common',common_ok(E2,n)); done=True; break
        if done: break
