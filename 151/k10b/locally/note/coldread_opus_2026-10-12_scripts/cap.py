import sys, io, contextlib, time
sys.path.insert(0,"/home/exedev/MathDyad/erdos151/locally")
import locally
S=locally.Search(locally.make_X('M8'), 1000)
S.maxc=0; S.maxsurv=0; S.ncomplete=0
oc=S.complete; orec=S.rec
def complete(adj, non, closed, v, pos, assign, newcount):
    S.ncomplete+=1; S.maxc=max(S.maxc, len(adj)+newcount); return oc(adj, non, closed, v, pos, assign, newcount)
S.complete=complete
t=time.time()
with contextlib.redirect_stdout(io.StringIO()): S.run()
print("found",[G.number_of_nodes() for G in S.found],"nodes",S.nodes,"maxn(rec)",S.maxn,"max n+newcount in complete()",S.maxc,"refused",S.refused,"complete calls",S.ncomplete,f"{time.time()-t:.0f}s")
