import sys, hashlib
sys.path.insert(0,'/home/exedev/MathDyad/erdos85/fs')
import fsenc
for h,T,f in [(3,[(0,1,2)],'h3_t1_rep0_r1b_all'),(5,[(0,1,2)],'h5_t1_rep0_r1b_all')]:
    H,fixed,target,n0,np_,ns=fsenc.stratum(h,T)
    cnf,var,F,adjS,st,cls=fsenc.build(49,H,fixed,target,highs=H,sb="all",r1=True,r1b=True)
    p=f'/tmp/fsref/{f}.cnf'; cnf.to_file(p)
    mine=hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
    theirs=hashlib.sha256(open(f'/tmp/erdos85-fs/cells/{f}.cnf','rb').read()).hexdigest()[:16]
    print(f,mine,theirs,st['sb_classes'],st['r1_clauses'],st['r1b_clauses'],len(var))
