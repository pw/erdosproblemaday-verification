#!/bin/bash
# Lake-free kernel replay of OpenAI's Lean proof of the planar unit-distance POWER SAVING (OAI.PlanarUnitDistances.main,
# module OAI.Geometry.UnitDistances.Main, 40 modules / 28,113 lines, Mathlib d13f23b7 = tag v4.34.1, toolchain v4.34.1).
# ESTIMATE BEFORE CPU (06:00Z erdos seat, 2026-10-14): cache get ~6 GB / ~4 min (disk only); 40 dense modules (20–50 KB each)
# at ONE thread nice 19 ⇒ ~2–10 min each ⇒ 1.5–6 h wall, ≤ 8 GB RSS (one lean at a time); probes minutes; leanchecker --fresh
# over the Mathlib closure 2–4 h. MEMORY GUARD (cron/erdos.md 2026-10-13): every Lean step waits until MemAvailable ≥ 28 GB
# (20 GB headroom + 8 GB job) — with the interactive #789 solvers holding ~21 GB this will WAIT; never evicts a solver.
# Writes only under /tmp/oaimath/167/lean-build and /tmp/erdos0300/lean/mathlib4/.lake (the shared Mathlib cache).
set -u
L=/tmp/oaimath/167/lean-build; SRC=$L/repo/lean; OUT=$L/out; ML=/tmp/erdos0300/lean/mathlib4
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export PATH="$TB:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
diskfree_gb(){ df -BG / | awk 'NR==2{gsub("G","",$4); print $4}'; }
waitmem(){ local need=$1; while [ "$(memavail_gb)" -lt "$need" ] || pgrep -x lake >/dev/null 2>&1; do log "waiting(mem ≥ ${need}G, no other lake): memavail=$(memavail_gb)G lake=$(pgrep -c -x lake)"; sleep 120; done; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"
lean --version; log "openai/math rev: $(git -C $L/repo rev-parse HEAD)"; log "mathlib rev: $(git -C $ML rev-parse HEAD)"
# 1. Mathlib oleans (disk guard ≥ 30 GB; low RAM)
if [ "$(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l)" -lt 5000 ]; then
  [ "$(diskfree_gb)" -ge 30 ] || { log "disk guard: only $(diskfree_gb)G free, need 30"; echo "cache_get 2 0" >> "$L/steps.tsv"; exit 12; }
  while pgrep -x lake >/dev/null 2>&1; do log "waiting(other lake)"; sleep 120; done
  step cache_get bash -c "cd $ML && nice -n 19 lake exe cache get > $L/logs/cache_get.log 2>&1"
  log "oleans: $(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' 2>/dev/null | wc -l)"
else log "mathlib oleans already present: $(find $ML/.lake/build/lib/lean/Mathlib -name '*.olean' | wc -l)"; fi
LP="$ML/.lake/build/lib/lean"; for p in $ML/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$OUT:$LP"; echo "$LEAN_PATH" > $L/lean_path.txt
# 2. smoke (memory-gated like everything below)
waitmem 28
step smoke bash -c "cd $L/probe && nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "smoke failed: $(head -5 $L/logs/smoke.log)"; exit 11; }
# 3. comparator module (statement with sorry) compiled against Mathlib only — its pp.all block is the reference
mkdir -p $OUT/ComparatorChallenges
step comparator_module bash -c "cd $SRC && nice -n 19 lean -DautoImplicit=false ComparatorChallenges/PlanarUnitDistances.lean -o $OUT/ComparatorChallenges/PlanarUnitDistances.olean -i $OUT/ComparatorChallenges/PlanarUnitDistances.ilean > $L/logs/comparator_module.log 2>&1"
step comparator bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false Comparator.lean > $L/logs/comparator.log 2>&1"
# 4. the 40 solution modules in import order, one at a time
build_one(){ local m="$1"; local o="$OUT/${m//.//}"; mkdir -p "$(dirname "$o")"
  ( cd "$SRC" && nice -n 19 ionice -c2 -n7 lean -DautoImplicit=false "${m//.//}.lean" -o "$o.olean" -i "$o.ilean" ) > "$L/logs/mod_$m.txt" 2>&1; local rc=$?
  echo "$m rc=$rc errors=$(grep -c 'error' "$L/logs/mod_$m.txt") lines=$(wc -l < "$L/logs/mod_$m.txt") rss_kb=$(cat $L/.rss 2>/dev/null)" >> "$L/modules.tsv"; return $rc; }
t0=$SECONDS; n=0; total=$(grep -c . $L/order.txt)
while read -r m; do [ -z "$m" ] && continue; n=$((n+1)); ts=$SECONDS
  if [ -s "$OUT/${m//.//}.olean" ] && grep -q "^$m rc=0" $L/modules.tsv 2>/dev/null; then log "skip (built) $m"; continue; fi
  waitmem 28
  if build_one "$m"; then log "built $n/$total $m ($((SECONDS-ts))s)"; else log "FAILED $m — stopping (see logs/mod_$m.txt)"; echo "build 1 $((SECONDS-t0))" >> "$L/steps.tsv"; exit 1; fi
done < "$L/order.txt"
echo "build 0 $((SECONDS-t0))" >> "$L/steps.tsv"; log "all $total modules built; oleans: $(find $OUT/OAI -name '*.olean' | wc -l)"
# 5. probes (--trust=0 for the axiom print on the solution)
waitmem 28
step axioms bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms90.lean > $L/logs/axioms.log 2>&1"
step rightshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false RightShape.lean > $L/logs/rightshape.log 2>&1"
step wrongshape bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false WrongShape.lean > $L/logs/wrongshape.log 2>&1"
step negcontrol bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false NegControl.lean > $L/logs/negcontrol.log 2>&1"
python3 - "$L" <<'PY'
import re,sys
L=sys.argv[1]
a=open(f"{L}/logs/axioms.log").read(); c=open(f"{L}/logs/comparator.log").read()
def block(t,key):
    i=t.find(key)
    if i<0: return None
    j=t.find("\n\n",i); return re.sub(r"\s+"," ",t[i:j if j>0 else None]).strip()
def axset(t,name):
    m=re.search(r"'%s' depends on axioms: \[([^\]]*)\]"%re.escape(name),t)
    return None if not m else set(x.strip().split('.{')[0] for x in m.group(1).split(','))
st_a=block(a,"OAI.PlanarUnitDistances.main :"); st_c=block(c,"OAI.PlanarUnitDistances.main :")
defs=[]
for d in ("def OAI.PlanarUnitDistances.u","def OAI.PlanarUnitDistances.unitPairCount","def OAI.PlanarUnitDistances.IsUnitPair"):
    defs.append((d, block(a,d), block(c,d)))
ax_a=axset(a,"OAI.PlanarUnitDistances.main"); ax_c=axset(c,"OAI.PlanarUnitDistances.main")
print("MAIN statement:",st_a); print("CMP  statement:",st_c)
for d,x,y in defs: print(d,"MATCH" if (x is not None and x==y) else "MISMATCH", x, "|", y)
print("MAIN axioms:",ax_a); print("CMP axioms:",ax_c)
ok_st = st_a is not None and st_a==st_c
ok_defs = all(x is not None and x==y for _,x,y in defs)
std = ax_a is not None and ax_a=={"propext","Classical.choice","Quot.sound"}
cmp_sorry = ax_c is not None and "sorryAx" in ax_c
verdict=("MATCH" if ok_st and ok_defs else "MISMATCH")+"\n"+("STD_AXIOMS" if std else "NONSTD_AXIOMS")+"\n"+("CMP_SORRY_SEEN" if cmp_sorry else "CMP_SORRY_NOT_SEEN")+"\n"
open(f"{L}/statement_match.txt","w").write(verdict); print(verdict)
PY
echo "statement_match $([ "$(head -1 $L/statement_match.txt)" = MATCH ] && [ "$(sed -n 2p $L/statement_match.txt)" = STD_AXIOMS ] && echo 0 || echo 1) 0" >> "$L/steps.tsv"
log "wrongshape rc must be NONZERO: $(grep '^wrongshape ' $L/steps.tsv | tail -1); negcontrol axioms: $(grep -o "depends on axioms: \[[^]]*\]" $L/logs/negcontrol.log | head -1)"
# 6. leanchecker --fresh over the whole closure
while pgrep -x leanchecker >/dev/null 2>&1; do log "waiting(other leanchecker)"; sleep 120; done
waitmem 28
step leanchecker_fresh bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Geometry.UnitDistances.Main > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.Geometry.UnitDistances.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
log "DONE — next erdos tick: read steps.tsv (build 0 + axioms 0 + statement_match 0 + rightshape 0 + wrongshape ≠ 0 + leanchecker_fresh 0 ⇒ (d) label; bank logs into verification/90/openai-referee/replay/, then rm -rf $ML/.lake per the disk guard)"
