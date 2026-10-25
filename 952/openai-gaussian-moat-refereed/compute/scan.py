import itertools, subprocess, sys
R2s=[int(a) for a in sys.argv[1].split(',')]; QMAX=int(sys.argv[2])
ps=[p for p in range(5,400) if p%4==1 and all(p%d for d in range(2,int(p**.5)+1))]
sets=[]
for r in (1,2,3,4):
    for c in itertools.combinations(ps,r):
        q=1
        for p in c: q*=p
        if q<=QMAX: sets.append((q,c))
sets.sort()
for R2 in R2s:
    found=None
    for q,c in sets:
        out=subprocess.run(['./sieve_perc',str(R2)]+[str(p) for p in c],capture_output=True,text=True).stdout.strip()
        if ' FINITE max_component=' in out: found=out; break
    print(R2, found if found else f'none with Q<={QMAX} ({len(sets)} sets tried)', flush=True)
