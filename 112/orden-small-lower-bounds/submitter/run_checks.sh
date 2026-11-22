#!/bin/sh
# run_checks.sh: rebuilds the arc lists from the connection sets, then checks every
# witness with both checkers, plus negative and positive controls. A few seconds.
# Usage (from this folder): sh run_checks.sh > checks.out 2>&1
set -u
B=$(mktemp -d)
python3 -I build_witnesses.py "$B" > /dev/null
for f in witness_*.txt control_*.txt; do cmp -s "$f" "$B/$(basename "$f")" || echo "MISMATCH: $f differs from the rebuilt file"; done
echo "arc lists rebuilt from the connection sets and compared: done (any difference is printed above)"
cc -O2 -o "$B/knm_check" knm_check.c || exit 1
K() { echo "### knm_check $*"; "$B/knm_check" "$@"; echo "exit=$?"; }
P() { echo "### second_check.py $*"; python3 -I second_check.py "$@"; echo "exit=$?"; }
W=.
echo "== Witnesses (each must PASS) =="
K 38 7 3 $W/witness_k73_ge39_N38.txt
K 46 8 3 $W/witness_k83_ge47_N46.txt
K 77 6 4 $W/witness_k64_ge78_N77.txt
K 70 3 6 $W/witness_k36_ge71_N70.txt
K 69 3 6 $W/witness_k36_ge70_N69.txt
echo "== Negative controls (each must FAIL: the same graph tested for a smaller n or m) =="
K 38 6 3 $W/witness_k73_ge39_N38.txt
K 38 7 3 $W/witness_k73_ge39_N38.txt flip 0 1
K 46 7 3 $W/witness_k83_ge47_N46.txt
K 77 5 4 $W/witness_k64_ge78_N77.txt
K 77 6 3 $W/witness_k64_ge78_N77.txt
K 70 2 6 $W/witness_k36_ge71_N70.txt
K 70 3 5 $W/witness_k36_ge71_N70.txt
echo "== Positive controls (published graphs; each must PASS) =="
K 8 3 3 $W/control_B8_k33_ge9.txt
K 14 4 3 $W/control_Z14_k43_ge15.txt
K 28 6 3 $W/control_Z28_k63_ge29.txt
echo "== Second method: counts of independent sets and transitive tournaments =="
echo "== (the witness needs 0 independent n-sets and TT_m = 0) =="
P 38 7 3 $W/witness_k73_ge39_N38.txt
P 46 8 3 $W/witness_k83_ge47_N46.txt
P 77 6 4 $W/witness_k64_ge78_N77.txt
P 70 3 6 $W/witness_k36_ge71_N70.txt
P 69 3 6 $W/witness_k36_ge70_N69.txt
P 14 4 3 $W/control_Z14_k43_ge15.txt
P 28 6 3 $W/control_Z28_k63_ge29.txt
rm -rf "$B"
