#!/bin/bash
# usage: one_n.sh N mult  -> one line: N mult length maxnum rampend tail(after ramp, up to 30)
N=$1; M=$2; T=/dev/shm/og282_${N}_${M}.txt
out=$(OG_FAST=${OG_FAST:-1} /home/exedev/MathDyad/erdos282b/og fact 3 $N 1000000 $T $M)
python3 -I - "$N" "$M" "$out" "$T" <<'PY'
import sys
N,M,out,T=sys.argv[1:5]
t=list(map(int,open(T).read().split(',')))
k=0
while k+1<len(t) and t[k+1]==t[k]+1: k+=1
f=dict(x.split('=') for x in out.split() if '=' in x)
print(N,M,f['length'],f['maxnum'],t[k],len(t),'|',','.join(map(str,t[k+1:k+31])))
PY
rm -f $T
