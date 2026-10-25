# Summarise the second instrument (BFS) over the 154 sets of split primes < 400 with Q <= 4000, both step bounds, and compare
# with the first instrument (sieve_perc) on the same sets. Exit 1 on any disagreement or missing set.
import itertools, re, glob, subprocess, sys
ps=[p for p in range(5,400) if p%4==1 and all(p%d for d in range(2,int(p**.5)+1))]
sets=[]
for r in (1,2,3,4):
    for c in itertools.combinations(ps,r):
        q=1
        for p in c: q*=p
        if q<=4000: sets.append((q,c))
sets.sort()
bfs={2:{},4:{}}
for f in sorted(['bfs_all.log','bfs_R4.log']+glob.glob('bfs_R2_s*.log')+glob.glob('bfs_R4_s*.log')+glob.glob('bfs_R2_rest_*.log')):
    for line in open(f):
        m=re.match(r'^(\d) (\d+) (\(.*?\)) (INFINITE|FINITE)',line)
        if m: bfs[int(m.group(1))][(int(m.group(2)),eval(m.group(3)))]=m.group(4)
bad=0
for R2 in (2,4):
    miss=[x for x in sets if x not in bfs[R2]]
    dis=[]
    for q,c in sets:
        out=subprocess.run(['./sieve_perc',str(R2)]+[str(p) for p in c],capture_output=True,text=True).stdout
        cv='FINITE' if ' FINITE ' in out else 'INFINITE'
        if (q,c) in bfs[R2] and bfs[R2][(q,c)]!=cv: dis.append((q,c))
    fin=sum(1 for v in bfs[R2].values() if v=='FINITE')
    print(f"R2={R2}: BFS covered {len(sets)-len(miss)}/{len(sets)} sets, finite={fin}, disagreements with sieve_perc={len(dis)} {dis[:3]} missing={miss}")
    bad+=len(miss)+len(dis)
sys.exit(1 if bad else 0)
