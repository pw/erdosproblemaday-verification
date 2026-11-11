#!/bin/bash
# wide-W refinement: L = q, T = round(10^(j/50)) for j in 550..620 (10^11 .. 10^12.4), W in [64q, min(1000q, q^2-1)] step 2q; stops at the first certified T per y
cd ~/MathDyad/erdos488/explicit
for y in "$@"; do
  read q Whi <<<"$(python3 -c "y=$y
k=y+1
while any(k%d==0 for d in range(2,int(k**.5)+1)): k+=1
print(k, min(1000*k, k*k-1))")"
  Ts=$(python3 -c "print(' '.join(str(round(10**(j/50))) for j in range(550,621)))")
  echo "### y=$y q=$q Whi=$Whi"
  STOP_AFTER_CERT=1 OMP_NUM_THREADS=4 nice -n 10 bash -c "ulimit -v 5000000; exec ./bracketsW3 20 50 weights_20.txt $y $q $((64*q)) $Whi $((2*q)) $Ts" | grep "^T=" | awk -v y=$y '{print "y="y, $0}'
done
