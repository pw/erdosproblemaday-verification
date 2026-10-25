p='/tmp/oaimath/156/seats/w_scripts/cover10.py'
s=open(p).read()
old="    if cr<best[0]: best=(cr,C.copy())\n"
new="    if cr<best[0]:\n        best=(cr,C.copy()); np.save(f\"/tmp/oaimath/156/seats/w_scripts/best_K{K}_s{seed}.npy\",best[1])\n"
assert old in s
open(p,'w').write(s.replace(old,new))
