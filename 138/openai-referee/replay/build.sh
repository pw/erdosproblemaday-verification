#!/bin/bash
# Lake-free kernel replay of OpenAI's Lean proof of the superexponential van der Waerden bound (OAI.QuantitativeVanDerWaerden.uniform_lower_bound
# = Theorem 1.1, comparator ComparatorChallenges/QuantitativeVanDerWaerden), module tree OAI.Combinatorics.ProgressionColoring (115 modules / 14,837 lines),
# Mathlib d13f23b7 = v4.34.1, toolchain v4.34.1, openai/math rev 1581d4c (sparse clone shared with /tmp/oaimath/604). ESTIMATE in ESTIMATE.md (written before CPU).
# MEMORY GUARD (cron/erdos.md 2026-10-13): every Lean step waits until MemAvailable ≥ 28 GB; never evicts a solver. Writes only under /tmp/oaimath/160/lean-build.
set -u
L=/tmp/oaimath/160/lean-build; SRC=/tmp/oaimath/604/lean-build/repo/lean; OUT=$L/out; ML=/tmp/erdos0300/lean/mathlib4
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export PATH="$TB:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
waitmem(){ local need=$1; while [ "$(memavail_gb)" -lt "$need" ] || pgrep -x lake >/dev/null 2>&1; do log "waiting(mem ≥ ${need}G, no other lake): memavail=$(memavail_gb)G lake=$(pgrep -c -x lake)"; sleep 120; done; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"
lean --version; log "openai/math rev: $(git -C $SRC rev-parse HEAD)"; log "mathlib rev: $(git -C $ML rev-parse HEAD)"
n_ol=$(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l); log "mathlib oleans present: $n_ol"
[ "$n_ol" -ge 5000 ] || { log "cache short"; echo "cache_ready 2 0" >> "$L/steps.tsv"; exit 12; }
echo "cache_ready 0 0" >> "$L/steps.tsv"
LP="$ML/.lake/build/lib/lean"; for p in $ML/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$OUT:$LP"; echo "$LEAN_PATH" > $L/lean_path.txt
waitmem 28
step smoke bash -c "cd $L/probe && nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "smoke failed: $(head -5 $L/logs/smoke.log)"; exit 11; }
mkdir -p $OUT/ComparatorChallenges
step comparator_module bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/QuantitativeVanDerWaerden.lean -o $OUT/ComparatorChallenges/QuantitativeVanDerWaerden.olean -i $OUT/ComparatorChallenges/QuantitativeVanDerWaerden.ilean > $L/logs/comparator_module.log 2>&1"
step comparator bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false Comparator.lean > $L/logs/comparator.log 2>&1"
build_one(){ local m="$1"; local o="$OUT/${m//.//}"; mkdir -p "$(dirname "$o")"
  ( cd "$SRC" && nice -n 19 ionice -c2 -n7 lean -DautoImplicit=false "${m//.//}.lean" -o "$o.olean" -i "$o.ilean" ) > "$L/logs/mod_$m.txt" 2>&1; local rc=$?
  echo "$m rc=$rc errors=$(grep -c 'error' "$L/logs/mod_$m.txt") lines=$(wc -l < "$L/logs/mod_$m.txt")" >> "$L/modules.tsv"; return $rc; }
t0=$SECONDS; n=0; total=$(grep -c . $L/order.txt)
while read -r m; do [ -z "$m" ] && continue; n=$((n+1)); ts=$SECONDS
  if [ -s "$OUT/${m//.//}.olean" ] && grep -q "^$m rc=0" $L/modules.tsv 2>/dev/null; then log "skip (built) $m"; continue; fi
  waitmem 28
  if build_one "$m"; then log "built $n/$total $m ($((SECONDS-ts))s)"; else log "FAILED $m — stopping (see logs/mod_$m.txt)"; echo "build 1 $((SECONDS-t0))" >> "$L/steps.tsv"; exit 1; fi
done < "$L/order.txt"
echo "build 0 $((SECONDS-t0))" >> "$L/steps.tsv"; log "all $total modules built; oleans: $(find $OUT/OAI -name '*.olean' | wc -l)"
waitmem 28
step axioms bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms138.lean > $L/logs/axioms.log 2>&1"
step rightshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false RightShape.lean > $L/logs/rightshape.log 2>&1"
step wrongshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false WrongShape.lean > $L/logs/wrongshape.log 2>&1"
step negcontrol bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false NegControl.lean > $L/logs/negcontrol.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 )
echo "statement_match $([ "$(head -1 $L/statement_match.txt)" = MATCH ] && [ "$(sed -n 2p $L/statement_match.txt)" = STD_AXIOMS ] && [ "$(sed -n 4p $L/statement_match.txt)" = ALL_STD_AXIOMS ] && echo 0 || echo 1) 0" >> "$L/steps.tsv"
log "wrongshape rc must be NONZERO: $(grep '^wrongshape ' $L/steps.tsv | tail -1); negcontrol axioms: $(grep -o "depends on axioms: \[[^]]*\]" $L/logs/negcontrol.log | head -1)"
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 28
step leanchecker_fresh bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Combinatorics.ProgressionColoring.Main > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Combinatorics.ProgressionColoring.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE — read steps.tsv; bank into verification/138/openai-referee/replay/; then rm -rf $ML/.lake per the disk guard"
