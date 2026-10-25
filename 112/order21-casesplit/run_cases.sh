#!/bin/bash
# Run every case CNF with cadical (DRAT proof), verify UNSAT proofs with drat-trim, keep SAT models.
# Usage: ./run_cases.sh <cases_dir> <parallel> <seconds_per_case>
set -u
D=${1:-cases}; P=${2:-16}; T=${3:-1800}
cd "$D" || exit 1
mkdir -p out
one() {
  f="$1"; n=$(basename "$f" .cnf); T="$2"
  [ -s "out/$n.status" ] && return 0
  start=$(date +%s)
  timeout "$T" cadical -q --binary=false "$f" "out/$n.drat" > "out/$n.out" 2>&1
  rc=$?; secs=$(( $(date +%s) - start ))
  if [ $rc -eq 10 ]; then
    echo "SAT $secs" > "out/$n.status"; rm -f "out/$n.drat"
  elif [ $rc -eq 20 ]; then
    if drat-trim "$f" "out/$n.drat" -t 20000 2>/dev/null | grep -q "s VERIFIED"; then echo "UNSAT-VERIFIED $secs" > "out/$n.status"; rm -f "out/$n.drat"
    else echo "UNSAT-UNVERIFIED $secs" > "out/$n.status"; fi
  else
    echo "UNKNOWN $secs rc=$rc" > "out/$n.status"; rm -f "out/$n.drat"
  fi
}
export -f one
ls *.cnf | xargs -P "$P" -I{} bash -c 'one "$@"' _ {} "$T"
echo "=== SUMMARY $(date -u +%FT%TZ)"; cat out/*.status | awk '{print $1}' | sort | uniq -c
grep -l "^SAT" out/*.status 2>/dev/null | head
