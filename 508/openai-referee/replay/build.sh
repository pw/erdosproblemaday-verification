#!/bin/bash
# Lake-free kernel replay of OpenAI's Lean proof that the Euclidean plane has NO proper five-colouring
# (OAI.EuclideanFiveColor.no_proper_five_coloring in OAI/Geometry/PlaneColoring/Five.lean; comparator
# ComparatorChallenges/EuclideanFiveColor.lean, permitted axioms propext/Quot.sound/Classical.choice).
# Closure: 70 OAI modules / 30,336 lines (37 PlaneColoring + 19 Analysis/PlaneSpectrum + 14 MeasureTheory/CompactFactors),
# only `import Mathlib` outside OAI; Mathlib d13f23b7 = v4.34.1 (the repo's lake-manifest pin), toolchain v4.34.1.
# ESTIMATE BEFORE CPU (21:00Z erdos seat, 2026-10-14): cache get ~6 GB / ~2–4 min; 70 modules at ONE thread nice 19:
# #90 did 28,113 lines in 1,275 s and #604 14,207 lines in 508 s ⇒ ~25 min nominal, 40–60 min with ~38 % steal and
# heavier measure theory; ≤ 8–13 GB RSS (one lean at a time); probes minutes; leanchecker --fresh over the Mathlib
# closure ~1–1.2 h (#90: 4,057 s, #604: 3,462 s). Disk: Mathlib cache ~7 GB (52 GB free at launch; guard ≥ 30).
# MEMORY GUARD (cron/erdos.md 2026-10-13): every Lean step waits until MemAvailable ≥ 28 GB; never evicts a solver.
# Writes only under /tmp/oaimath/158/lean-build and /tmp/erdos0300/lean/mathlib4/.lake (the Mathlib cache).
set -u
L=/tmp/oaimath/158/lean-build; SRC=$L/repo/lean; OUT=$L/out; ML=/tmp/erdos0300/lean/mathlib4
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export PATH="$TB:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
diskfree_gb(){ df -BG / | awk 'NR==2{gsub("G","",$4); print $4}'; }
waitmem(){ local need=$1; while [ "$(memavail_gb)" -lt "$need" ] || pgrep -x lake >/dev/null 2>&1; do log "waiting(mem ≥ ${need}G, no other lake): memavail=$(memavail_gb)G lake=$(pgrep -c -x lake)"; sleep 120; done; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"
for b in lean lake leanchecker; do [ -x "$TB/$b" ] || { log "missing $TB/$b"; echo "toolchain 2 0" >> $L/steps.tsv; exit 13; }; done
lean --version; log "openai/math rev: $(git -C $L/repo rev-parse HEAD)"; log "mathlib rev: $(git -C $ML rev-parse HEAD)"
git -C $L/repo rev-parse HEAD > $L/openai_math_rev.txt; git -C $ML rev-parse HEAD > $L/mathlib_rev.txt
# 1. Mathlib oleans
if [ "$(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l)" -lt 5000 ]; then
  [ "$(diskfree_gb)" -ge 30 ] || { log "disk guard: only $(diskfree_gb)G free, need 30"; echo "cache_get 2 0" >> "$L/steps.tsv"; exit 12; }
  while pgrep -x lake >/dev/null 2>&1; do log "waiting(other lake)"; sleep 120; done
  step cache_get bash -c "cd $ML && nice -n 19 lake exe cache get > $L/logs/cache_get.log 2>&1"
fi
NO=$(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' | wc -l); log "mathlib oleans present: $NO"
[ "$NO" -ge 5000 ] || { echo "cache_ready 1 0" >> "$L/steps.tsv"; exit 14; }; echo "cache_ready 0 0" >> "$L/steps.tsv"
LP="$ML/.lake/build/lib/lean"; for p in $ML/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$OUT:$LP"; echo "$LEAN_PATH" > $L/lean_path.txt
# 2. smoke
waitmem 28
step smoke bash -c "cd $L/probe && nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "smoke failed: $(head -5 $L/logs/smoke.log)"; exit 11; }
# 3. comparator module (statement with sorry) compiled against Mathlib only — its pp.all output is the reference
mkdir -p $OUT/ComparatorChallenges
step comparator_module bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/EuclideanFiveColor.lean -o $OUT/ComparatorChallenges/EuclideanFiveColor.olean -i $OUT/ComparatorChallenges/EuclideanFiveColor.ilean > $L/logs/comparator_module.log 2>&1"
step cmp_main bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false CmpMain.lean > $L/logs/cmp_main.log 2>&1"
step cmp_def bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false CmpDef.lean > $L/logs/cmp_def.log 2>&1"
step cmp_axioms bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false CmpAxioms.lean > $L/logs/cmp_axioms.log 2>&1"
# 4. the 70 solution modules in import order, one at a time
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
# 5. probes (--trust=0 for the axiom print on the solution)
waitmem 28
step axioms bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms158.lean > $L/logs/axioms.log 2>&1"
step sol_main bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false SolMain.lean > $L/logs/sol_main.log 2>&1"
step sol_def bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false SolDef.lean > $L/logs/sol_def.log 2>&1"
step rightshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false RightShape.lean > $L/logs/rightshape.log 2>&1"
step wrongshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false WrongShape.lean > $L/logs/wrongshape.log 2>&1"
step negcontrol bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false NegControl.lean > $L/logs/negcontrol.log 2>&1"
step statement_match python3 $L/statement_match.py $L
log "wrongshape rc must be NONZERO: $(grep '^wrongshape ' $L/steps.tsv | tail -1); negcontrol axioms: $(grep -o "depends on axioms: \[[^]]*\]" $L/logs/negcontrol.log | head -1)"
# 6. leanchecker --fresh over the whole closure
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 28
step leanchecker_fresh bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Geometry.PlaneColoring.Five > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Geometry.PlaneColoring.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE — read steps.tsv (build 0 + axioms 0 + statement_match 0 + rightshape 0 + wrongshape ≠ 0 + leanchecker_fresh 0 ⇒ (d)); bank into verification/508/openai-referee/replay/; then rm -rf $ML/.lake per the disk guard once no other replay needs it"
