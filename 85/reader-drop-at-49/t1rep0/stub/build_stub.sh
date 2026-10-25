#!/bin/bash
# Build the stub + the 9 downstream capstone modules over OUR replay oleans; print axioms.
S=$(cd "$(dirname "$0")" && pwd)
B=/tmp/erdos85-1019/build; P=/tmp/erdos85-1019/repo/proofs; T=$HOME/.elan/toolchains/leanprover--lean4---v4.31.0/bin
export PATH=$T:/usr/bin:/bin HOME=$B/home LANG=C.UTF-8
export LEAN_PATH=$S/lean:$B/lean:$(ls -d $P/.lake/packages/*/.lake/build/lib/lean | paste -sd:)
ulimit -v 40000000
m=Erdos85OrderFortyNineSevenHighT1Rep0Certificate
( cd $S/src && /usr/bin/time -f "MAXRSS_KB=%M %es" nice -n 19 lean -j1 Proofs/$m.lean -o $S/lean/Proofs/$m.olean ) > $S/logs/$m.log 2>&1; echo "$m rc=$?" | tee -a $S/build.tsv
for m in OrderFortyNineSevenHighCertificates OrderFortyNineSevenHighT0CanonicalTerminal OrderFortyNineSevenHighT0CanonicalEmptyCubeTerminal OrderFortyNineSevenHighT0CanonicalEmptyCubeSplitTerminal OrderFortyNineSevenHighT0CanonicalEmptyCubeMixedCapstone OrderFortyNineSevenHighT0CanonicalHsbStratumCapstone OrderFortyNineCapstone OrderFortyNineCapstoneH3 FiniteDropCapstone; do
  m=Erdos85$m
  ( cd $P && /usr/bin/time -f "MAXRSS_KB=%M %es" nice -n 19 lean -j1 Proofs/$m.lean -o $S/lean/Proofs/$m.olean ) > $S/logs/$m.log 2>&1; rc=$?; echo "$m rc=$rc" | tee -a $S/build.tsv
  [ $rc = 0 ] || exit 1
done
( cd $S/src && cat > PrintAxioms.lean <<'XX'
import Proofs.Erdos85FiniteDropCapstone
#print axioms Erdos85.not_c4FreeMinDegreeWitness_fortyNine_seven_of_h1_h7Evidence
#print axioms Erdos85.minDegreeForC4_fortyEight_fortyNine_exact_of_h1_h7Evidence
#print axioms Erdos85.minDegreeForC4_fortyNine_lt_fortyEight_of_h1_h7Evidence
XX
/usr/bin/time -f "MAXRSS_KB=%M %es" nice -n 19 lean -j1 PrintAxioms.lean ) > $S/axioms.out 2>&1; echo "axioms rc=$?" | tee -a $S/build.tsv
