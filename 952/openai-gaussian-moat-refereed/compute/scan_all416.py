# First instrument (sieve_perc, union-find) over EVERY set of split primes with product <= 4000 (seat B's M2: scan.py only used p < 400).
import itertools, subprocess, sys
ps=[p for p in range(5,4001) if p%4==1 and all(p%d for d in range(2,int(p**.5)+1))]
sets=[]
for r in (1,2,3,4):
    for c in itertools.combinations(ps,r):
        q=1
        for p in c: q*=p
        if q<=4000: sets.append((q,c))
sets.sort(); print("sets",len(sets),"(primes < 400:",sum(1 for q,c in sets if max(c)<400),")",flush=True)
for R2 in (1,2,4):
    fin=[]; mind=1.0
    for q,c in sets:
        out=subprocess.run(['./sieve_perc',str(R2)]+[str(p) for p in c],capture_output=True,text=True).stdout.strip()
        assert out.startswith(f"R2={R2} P="), out
        d=float(out.split('density=')[1].split()[0]); mind=min(mind,d)
        if ' FINITE ' in out: fin.append(out)
        elif ' INFINITE ' not in out: print("BAD",out); sys.exit(2)
    print(f"R2={R2}: {len(sets)} sets, finite={len(fin)}, min density={mind:.4f}",flush=True)
    for f in fin[:12]: print("   ",f)
