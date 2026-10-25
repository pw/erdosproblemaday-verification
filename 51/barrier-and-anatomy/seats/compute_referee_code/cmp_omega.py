import numpy as np, sys
d=sys.argv[1]
k=np.fromfile('/tmp/refc51/c4e7/knap_ell.bin',dtype=np.uint32); o=np.fromfile(d+'/omega_ell.bin',dtype=np.uint32)
oe=o[0::2][:len(k)]
mis=int((k[1:]!=oe[1:]).sum()); oddhits=int((o[1::2]!=0).sum())-1
out=open(d+'/out.txt').read().splitlines()
ntot=int(out[0].split()[-1])
print(d.split('/')[-1], '| count', ntot, 'V(4e7) knap 6208455 ->', 'CAUGHT' if ntot!=6208455 else 'passes',
      '| per-a ell mismatches', mis, '+ odd-a hits', oddhits, '->', 'CAUGHT' if mis or oddhits else 'passes')
base=open('/tmp/refc51/c4e7_base_out.txt').read()
print('   aggregate output (maxR/maxW/viol/histogram) identical to unmutated:', '\n'.join(out)==base.strip())
