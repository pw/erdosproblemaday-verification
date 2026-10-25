import sys, math, time
sys.path.insert(0,'/tmp/erdos295-referee')
from ref_search import S, small_primes
certs = {
 'Bae34': [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992],
 'ours35': [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,48,50,52,54,63,640,337280,1735650,68479214496],
 'k17': [17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,42,43,44,45,48,50,52,54,63,1735650,68479214496],
}
for name,C in certs.items():
    for m in range(2, 15):
        P=C[:len(C)-m]
        a,b=1,1
        for x in P:
            a,b=a*x-b,b*x; g=math.gcd(a,b); a//=g; b//=g
        primes=frozenset(p for x in P for p in small_primes(x))
        s=S(prime=True,quad=True); t0=time.time()
        ok=s.dfs(P[-1]+1, m, a, b, primes, tuple(P))
        el=time.time()-t0
        print(f"{name}: fixed first {len(P)}, search last {m}: witness={ok} first={list(s.sols[0][len(P):]) if s.sols else None} nodes={s.c['nodes']} pprunes={s.c['pprunes']} qprunes={s.c['two_prunes']} {el:.1f}s", flush=True)
        if el>60: break
