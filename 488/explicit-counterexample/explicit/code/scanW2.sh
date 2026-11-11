#!/bin/bash
# refined: L = q, T = round(10^(j/20)) for j in 220..300 (10^11 .. 10^17), W in [32q, min(320q, q^2-1)] step q
cd ~/MathDyad/erdos488/explicit
for y in "$@"; do
  read q Whi <<<"$(python3 -c "y=$y
k=y+1
while any(k%d==0 for d in range(2,int(k**.5)+1)): k+=1
print(k, min(320*k, k*k-1))")"
  Ts=$(python3 -c "print(' '.join(str(round(10**(j/20))) for j in range(220,341)))")
  echo "### y=$y q=$q Whi=$Whi"
  STOP_AFTER_CERT=1 OMP_NUM_THREADS=4 nice -n 10 bash -c "ulimit -v 5000000; exec ./bracketsW2 20 50 weights_20.txt $y $q $((32*q)) $Whi $q $Ts" | grep "^T=" | awk -v y=$y '{print "y="y, $0}'
done
