import sys, time; sys.path.insert(0,'/tmp/e1125/787work')
from mis import *
out=[]
bad=0
for f in sys.argv[1:]:
    for line in open(f):
        p=line.split()
        if not p: continue
        n,al,ed,lab=int(p[0]),int(p[1]),int(p[2]),p[3]
        A=[int(x) for x in p[4:]]
        As,E=graph(A)
        t=time.time()
        a1,B1=alpha_cpsat(A)
        # SAT decision: alpha>=al SAT and alpha>=al+1 UNSAT
        s1,B=has_indep(A,al); s2,_=has_indep(A,al+1)
        ok = (len(A)==n==len(set(A)) and len(E)==ed and a1==al and s1 and not s2 and check_indep(A,B1))
        if not ok: bad+=1
        line_out=f"{f.split('/')[-1]} n={n} |A|={len(A)} distinct={len(set(A))} claimed_alpha={al} cpsat={a1} sat(>=al)={s1} sat(>=al+1)={s2} edges claimed={ed} mine={len(E)} int=yes {'OK' if ok else 'MISMATCH'} {time.time()-t:.1f}s"
        print(line_out, flush=True)
print("BAD", bad)
