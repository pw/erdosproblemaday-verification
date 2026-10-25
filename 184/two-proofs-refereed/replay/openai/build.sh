#!/bin/bash
# Lake-free kernel replay of OpenAI's Lean proof of the Erdős–Gallai cycle decomposition bound (OAI.ErdosGallai.erdos_gallai = MainStatement,
# comparator ComparatorChallenges/CycleDecomposition), module tree OAI.Combinatorics.CycleDecomposition (34 modules / 21,451 lines), Mathlib d13f23b7
# = v4.34.1, toolchain v4.34.1 (scratch elan of /tmp/oaimath/166), openai/math rev 1581d4c (= adc7f12 on these paths). Recipe = #138's build.sh.
# GATES: waits for the #85 t1_rep0 Lean (pid in T1PID) to exit, MemAvailable ≥ 28 GB, and /tmp/oaimath/181/lean-build/GO (written by the seat after the
# source audit). Writes only under /tmp/oaimath/181/lean-build. ESTIMATE.md written before CPU.
set -u
L=/tmp/oaimath/181/lean-build; SRC=/tmp/oaimath/604/lean-build/repo/lean; OUT=$L/out; ML=/tmp/erdos0300/lean/mathlib4
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export PATH="$TB:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
waitmem(){ local need=$1; while [ "$(memavail_gb)" -lt "$need" ]; do log "waiting(mem ≥ ${need}G): memavail=$(memavail_gb)G"; sleep 120; done; }
T1PID=$(cat $L/T1PID 2>/dev/null)
while [ -n "$T1PID" ] && kill -0 "$T1PID" 2>/dev/null; do log "waiting(#85 t1_rep0 pid $T1PID still running; memavail=$(memavail_gb)G)"; sleep 120; done
while [ ! -e $L/GO ]; do log "waiting(GO file — source audit not yet read)"; sleep 120; done
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"
lean --version; log "openai/math rev: $(git -C $SRC/.. rev-parse HEAD)"; log "mathlib rev: $(git -C $ML rev-parse HEAD)"
n_ol=$(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l); log "mathlib oleans present: $n_ol"
[ "$n_ol" -ge 5000 ] || { log "cache short"; echo "cache_ready 2 0" >> "$L/steps.tsv"; exit 12; }
echo "cache_ready 0 0" >> "$L/steps.tsv"
LP="$ML/.lake/build/lib/lean"; for p in $ML/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$OUT:$LP"; echo "$LEAN_PATH" > $L/lean_path.txt
waitmem 28
step smoke bash -c "cd $L/probe && nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "smoke failed: $(head -5 $L/logs/smoke.log)"; exit 11; }
mkdir -p $OUT/ComparatorChallenges
step comparator_module bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/CycleDecomposition.lean -o $OUT/ComparatorChallenges/CycleDecomposition.olean -i $OUT/ComparatorChallenges/CycleDecomposition.ilean > $L/logs/comparator_module.log 2>&1"
step comparator bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false Comparator.lean > $L/logs/comparator.log 2>&1"
build_one(){ local m="$1"; local o="$OUT/${m//.//}"; mkdir -p "$(dirname "$o")"
  ( cd "$SRC" && /usr/bin/time -f "maxrss_kb=%M wall_s=%e" nice -n 19 ionice -c2 -n7 lean -DautoImplicit=false "${m//.//}.lean" -o "$o.olean" -i "$o.ilean" ) > "$L/logs/mod_$m.txt" 2>&1; local rc=$?
  echo "$m rc=$rc errors=$(grep -c 'error' "$L/logs/mod_$m.txt") $(grep -o 'maxrss_kb=[0-9]* wall_s=[0-9.]*' "$L/logs/mod_$m.txt" | tail -1) sha=$(sha256sum "$o.olean" 2>/dev/null | cut -c1-16)" >> "$L/modules.tsv"; return $rc; }
t0=$SECONDS; n=0; total=$(grep -c . $L/order.txt)
while read -r m; do [ -z "$m" ] && continue; n=$((n+1)); ts=$SECONDS
  if [ -s "$OUT/${m//.//}.olean" ] && grep -q "^$m rc=0" $L/modules.tsv 2>/dev/null; then log "skip (built) $m"; continue; fi
  waitmem 28
  if build_one "$m"; then log "built $n/$total $m ($((SECONDS-ts))s)"; else log "FAILED $m — stopping (see logs/mod_$m.txt)"; echo "build 1 $((SECONDS-t0))" >> "$L/steps.tsv"; exit 1; fi
done < "$L/order.txt"
echo "build 0 $((SECONDS-t0))" >> "$L/steps.tsv"; log "all $total modules built; oleans: $(find $OUT/OAI -name '*.olean' | wc -l)"
waitmem 28
step axioms bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms184.lean > $L/logs/axioms.log 2>&1"
step wrongshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false WrongShape.lean > $L/logs/wrongshape.log 2>&1"
step negcontrol bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false NegControl.lean > $L/logs/negcontrol.log 2>&1"
( cd $L && python3 statement_match.py > $L/logs/statement_match.log 2>&1 )
echo "statement_match $([ "$(head -1 $L/statement_match.txt)" = MATCH ] && [ "$(sed -n 2p $L/statement_match.txt)" = STD_AXIOMS ] && [ "$(sed -n 3p $L/statement_match.txt)" = CMP_SORRY_SEEN ] && echo 0 || echo 1) 0" >> "$L/steps.tsv"
log "wrongshape rc must be NONZERO: $(grep '^wrongshape ' $L/steps.tsv | tail -1); negcontrol axioms: $(grep -o "depends on axioms: \[[^]]*\]" $L/logs/negcontrol.log | head -1)"
touch $L/BUILD_DONE
[ -e $L/BRIDGE_READY ] && step bridge bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Bridge.lean > $L/logs/bridge.log 2>&1"
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 28
step leanchecker_fresh bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Combinatorics.CycleDecomposition.Main > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Combinatorics.CycleDecomposition.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE — read steps.tsv; bank into verification/184/; then rm -rf $ML/.lake per the disk guard"
