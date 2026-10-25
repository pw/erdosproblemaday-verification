import json, sys
from fractions import Fraction as F
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
D='/home/exedev/MathDyad/erdos203'
N=int(sys.argv[1]); d=tuple(map(int,sys.argv[2].split(','))); Mps=[int(x) for x in sys.argv[3].split(',')]; tl=float(sys.argv[4])
pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
for Mp in Mps:
    E,lum,M,ev=LL.instance(pool,d,Mp)
    name,V,bd,t,wt=LL.cpsat(E,lum,M,tl,2)
    rc=LL.recount_np(E,lum,M,t) if t is not None else None
    print(json.dumps({'N':N,'dir':d,'Mp':Mp,'M':M,'lumpy':len(lum),'status':name,'V':str(V),'V_f':float(V) if V is not None else None,'bound':str(bd),'bound_f':float(bd) if bd is not None else None,'recount':str(rc),'wall':round(wt,1)}),flush=True)
