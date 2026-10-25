import itertools
K = 2921
opt = {}
for line in open('r3table.txt'):
    n, s = map(int, line.split()[:2]); el = list(map(int, line.split(':')[1].split()))
    if s not in opt: opt[s] = el
def bt(j):
    v,p=0,1
    while j: v+=(j&1)*p; j>>=1; p*=3
    return v
# full blocks: (size, M, elemfn, name)
leaves = [(len(e), max(e), (lambda e: (lambda j: e[j]))(e), f"O{s}") for s,e in opt.items() if s>=2]
def prod(top, low):
    ts,tM,tf,tn = top; ls,lM,lf,ln = low; b = 2*lM+1
    return (ts*ls, tM*b+lM, (lambda tf,lf,ls,b: (lambda j: tf(j//ls)*b + lf(j%ls)))(tf,lf,ls,b), f"{tn}.{ln}")
blocks = list(leaves)
lvl = list(leaves)
for depth in range(2):
    new = []
    for a in leaves:
        for b in lvl:
            p = prod(a, b)
            if p[0] <= 3000: new.append(p)
    # prune dominated: keep for each size the min M
    best = {}
    for p in new:
        if p[0] not in best or p[1] < best[p[0]][1]: best[p[0]] = p
    lvl = list(best.values()); blocks += lvl
best = {}
for p in blocks:
    if p[0] not in best or p[1] < best[p[0]][1]: best[p[0]] = p
blocks = sorted(best.values())
res = []
for low in blocks:
    ls, lM, lf, ln = low; b = 2*lM+1; q = -(-K//ls); j = K-1
    # top options: optimal prefix O_s for s >= q, or BT infinite
    for s,e in opt.items():
        if s >= q: res.append((e[j//ls]*b + lf(j%ls), f"O{s}[prefix].{ln}"))
    res.append((bt(j//ls)*b + lf(j%ls), f"BT*.{ln}"))
res.sort()
for r in res[:12]: print(r)
