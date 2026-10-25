#!/bin/bash
# For every UNKNOWN case: split 3 ways (cube_case.py), race cadical/kissat on each child with a long budget,
# verify each child's DRAT; parent becomes UNSAT-VERIFIED only if all three children are. Any SAT child = witness.
# Usage: ./rerun_cubed.sh <cases_dir> <parallel_children> <seconds_per_child>
set -u
D=${1:-cases}; P=${2:-6}; T=${3:-10800}
cd "$(dirname "$0")" || exit 1
for s in $(grep -l "^UNKNOWN" "$D"/out/*.status); do n=$(basename "$s" .status); [ -f "$D/${n}_c0.cnf" ] || ~/.venv/bin/python cube_case.py "$n" "$D"; done
cd "$D" || exit 1
child() {
  c="$1"; T="$2"; f="$c.cnf"; [ -s "out/$c.status" ] && grep -q -E "^(SAT|UNSAT-VERIFIED)" "out/$c.status" && return 0
  start=$(date +%s)
  timeout "$T" cadical -q --binary=false "$f" "out/$c.c.drat" > "out/$c.c.out" 2>&1 & pc=$!
  timeout "$T" kissat -q --no-binary "$f" "out/$c.k.drat" > "out/$c.k.out" 2>&1 & pk=$!
  while kill -0 $pc 2>/dev/null && kill -0 $pk 2>/dev/null; do sleep 5; done
  if ! kill -0 $pc 2>/dev/null; then wait $pc; rc=$?; who=c; kill $pk 2>/dev/null; wait $pk 2>/dev/null; else wait $pk; rc=$?; who=k; kill $pc 2>/dev/null; wait $pc 2>/dev/null; fi
  secs=$(( $(date +%s) - start ))
  if [ $rc -eq 10 ]; then echo "SAT $secs $who" > "out/$c.status"; cp "out/$c.$who.out" "out/$c.model"
  elif [ $rc -eq 20 ]; then
    if drat-trim "$f" "out/$c.$who.drat" -t 40000 2>/dev/null | grep -q "s VERIFIED"; then echo "UNSAT-VERIFIED $secs $who" > "out/$c.status"; rm -f out/$c.c.drat out/$c.k.drat
    else echo "UNSAT-UNVERIFIED $secs $who" > "out/$c.status"; fi
  else echo "UNKNOWN $secs rc=$rc $who" > "out/$c.status"; rm -f out/$c.c.drat out/$c.k.drat; fi
}
export -f child
ls *_c[012].cnf | sed 's/\.cnf$//' | xargs -P "$P" -I{} bash -c 'child "$@"' _ {} "$T"
# roll children up into parents
for s in $(grep -l "^UNKNOWN" out/*.status | grep -v "_c[012].status"); do
  n=$(basename "$s" .status); v=$(for i in 0 1 2; do cut -d" " -f1 "out/${n}_c$i.status" 2>/dev/null || echo MISSING; done | sort -u | tr '\n' ',')
  case "$v" in "UNSAT-VERIFIED,") echo "UNSAT-VERIFIED cubed" > "out/$n.status";; *SAT,*) echo "SAT cubed" > "out/$n.status";; *) echo "UNKNOWN cubed $v" > "out/$n.status";; esac
done
echo "=== CUBED $(date -u +%FT%TZ)"; cat out/*.status | grep -v "^UNSAT-VERIFIED [0-9]" | sort | uniq -c | head; cat out/*.status | awk '{print $1}' | sort | uniq -c
