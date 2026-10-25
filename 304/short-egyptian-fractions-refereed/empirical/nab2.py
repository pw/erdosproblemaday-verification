#!/usr/bin/env python3
"""first b with N(b) >= k, and N(b-1,b) there, k<=6 (b<=110); plus N(732,733). Uses nab.py's exact N(a,b)."""
import importlib.util,sys
spec=importlib.util.spec_from_file_location('nab','nab.py'); 
src=open('nab.py').read().split('B=int(sys.argv[1])')[0]
ns={}; exec(src,ns); N=ns['N']
first={}
for b in range(2,111):
    Nb=max(N(a,b) for a in range(1,b))
    if Nb not in first: first[Nb]=(b,N(b-1,b),[a for a in range(1,b) if N(a,b)==Nb])
print('first b with N(b)=k: ',{k:v for k,v in sorted(first.items())})
print('N(732,733)=',N(732,733))
