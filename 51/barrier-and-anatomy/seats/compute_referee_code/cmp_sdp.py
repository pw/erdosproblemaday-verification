import pickle, numpy as np, sys
from fractions import Fraction
d=sys.argv[1]; tot=0
for P,X,f,npy in [((2,3),(120,80),'exact_2-3_120-80.pkl','R23.npy'),((2,3,5),(60,30,20),'exact_2-3-5_60-30-20.pkl','R235.npy')]:
    b=pickle.load(open('/tmp/refc51/'+f,'rb')); R=np.load(d+'/'+npy); bad=0
    for c,n in b.items():
        r=R[c]
        if n is None: bad+= (not np.isnan(r)); continue
        a=1
        for p,e in zip(P,c): a*=p**e
        if np.isnan(r) or abs(float(Fraction(n,a))-r)>1e-12*r: bad+=1
    print('   ',npy,'full-lattice cells disagreeing with referee exact DP:',bad); tot+=bad
print('   ->','CAUGHT' if tot else 'passes')
