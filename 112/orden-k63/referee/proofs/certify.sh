#!/bin/bash
# sequential: solve with proof, then check. One solver/checker process at a time.
cd /tmp/e1122/seatO/proofs
DT=/home/exedev/MathDyad/tools/drat-trim/drat-trim
CL=/home/exedev/MathDyad/tools/cake_lpr/cake_lpr
ulimit -v 12000000
for base in lemmaB_32_B8fixed lemmaB_23_B8fixed lemmaB_32_Ifree lemmaB_23_Ifree; do
  cnf=../cnf/$base.cnf
  echo "=== $base"
  s=$(date +%s.%N); timeout 2400 nice -n 19 /home/exedev/MathDyad/tools/kissat/build/kissat -q --no-binary $cnf $base.drat > $base.kissat.out 2>&1; rc=$?; e=$(date +%s.%N)
  echo "kissat rc=$rc ($(grep '^s ' $base.kissat.out)) time=$(echo "$e - $s" | bc)s proof=$(stat -c %s $base.drat 2>/dev/null)B"
  if [ $rc = 20 ]; then
    s=$(date +%s.%N); timeout 3600 nice -n 19 $DT $cnf $base.drat -L $base.lrat > $base.dt.out 2>&1; e=$(date +%s.%N)
    echo "drat-trim: $(grep -E '^s ' $base.dt.out) time=$(echo "$e - $s" | bc)s"
    s=$(date +%s.%N); timeout 3600 nice -n 19 $CL $cnf $base.lrat > $base.cl.out 2>&1; e=$(date +%s.%N)
    echo "cake_lpr on drat-trim LRAT: $(grep -E '^s ' $base.cl.out | head -2 | tr '\n' ' ') time=$(echo "$e - $s" | bc)s"
    rm -f $base.drat
  fi
done
# negative controls for the checkers
echo "=== negative controls"
$DT ../cnf/control_n13_22_Ifree.cnf lemmaB_32_B8fixed.lrat > neg1.out 2>&1; echo "drat-trim on SAT control CNF with unrelated proof: $(grep -E '^s |ERROR|error' neg1.out | head -2 | tr '\n' ' ')"
$CL ../cnf/control_n13_22_Ifree.cnf lemmaB_32_B8fixed.lrat > neg2.out 2>&1; echo "cake_lpr on SAT control CNF with unrelated LRAT: $(head -c 300 neg2.out | tr '\n' ' ')"
[ -f lemmaB_32_B8fixed.lrat ] && head -c $(( $(stat -c %s lemmaB_32_B8fixed.lrat) / 2 )) lemmaB_32_B8fixed.lrat > trunc.lrat
$CL ../cnf/lemmaB_32_B8fixed.cnf trunc.lrat > neg3.out 2>&1; echo "cake_lpr on truncated LRAT: $(head -c 300 neg3.out | tr '\n' ' ')"
echo DONE
