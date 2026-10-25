#!/bin/bash
# Symmetry-broken pass: for every case without an UNSAT-VERIFIED status, build <case>_sb.cnf (lex-leader over
# Aut(N+)xAut(N-)xAut(N0), see symbreak_case.py) and race cadical/kissat with a long cap; verify the DRAT; record the
# verdict in the PARENT's status as "UNSAT-VERIFIED <secs> sb" (so ship112.py and the monitor count it) or "SAT ... sb".
# Usage: ./rerun_sb.sh <cases_dir> <parallel> <seconds>
set -u
D=${1:-cases}; P=${2:-12}; T=${3:-7200}
cd "$(dirname "$0")" || exit 1
todo=$(for f in $D/p*_o*_i*_n*.cnf; do n=$(basename "$f" .cnf); case "$n" in *_c[012]|*_sb) continue;; esac; grep -q "^UNSAT-VERIFIED\|^SAT" "$D/out/$n.status" 2>/dev/null || echo "$n"; done)
echo "cases to run: $(echo "$todo" | wc -w)"
for n in $todo; do [ -f "$D/${n}_sb.cnf" ] || ~/.venv/bin/python symbreak_case.py "$n" "$D" | tail -1; done
cd "$D" || exit 1
one() {
  n="$1"; T="$2"; f="${n}_sb.cnf"
  start=$(date +%s)
  timeout "$T" cadical -q --binary=false "$f" "out/$n.sb.c.drat" > "out/$n.sb.c.out" 2>&1 & pc=$!
  timeout "$T" kissat -q --no-binary "$f" "out/$n.sb.k.drat" > "out/$n.sb.k.out" 2>&1 & pk=$!
  while kill -0 $pc 2>/dev/null && kill -0 $pk 2>/dev/null; do sleep 5; done
  if ! kill -0 $pc 2>/dev/null; then wait $pc; rc=$?; who=c; kill $pk 2>/dev/null; wait $pk 2>/dev/null; else wait $pk; rc=$?; who=k; kill $pc 2>/dev/null; wait $pc 2>/dev/null; fi
  secs=$(( $(date +%s) - start ))
  if [ $rc -eq 10 ]; then echo "SAT $secs sb-$who" > "out/$n.status"; cp "out/$n.sb.$who.out" "out/$n.sb.model"
  elif [ $rc -eq 20 ]; then
    if drat-trim "$f" "out/$n.sb.$who.drat" -t 40000 2>/dev/null | grep -q "s VERIFIED"; then echo "UNSAT-VERIFIED $secs sb-$who" > "out/$n.status"; rm -f out/$n.sb.c.drat out/$n.sb.k.drat
    else echo "UNSAT-UNVERIFIED $secs sb-$who" > "out/$n.status"; fi
  else echo "UNKNOWN $secs rc=$rc sb" > "out/$n.status"; rm -f out/$n.sb.c.drat out/$n.sb.k.drat; fi
}
export -f one
echo "$todo" | tr ' ' '\n' | grep -v '^$' | xargs -P "$P" -I{} bash -c 'one "$@"' _ {} "$T"
echo "=== SB PASS $(date -u +%FT%TZ)"; cat out/*.status | grep -v -E "_c[012]" | awk '{print $1}' | sort | uniq -c
