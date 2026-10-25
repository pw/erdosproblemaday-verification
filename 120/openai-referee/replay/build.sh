#!/bin/bash
# Lake-free kernel replay of OpenAI's Lean proof of the DYADIC case of Erdős #120 (OAI.Problem310.dyadic_affine_avoidance,
# module OAI.MeasureTheory.DyadicAvoidance.Main, 75 modules / 8,455 lines, Mathlib d13f23b7, toolchain v4.34.1).
# Estimate before CPU: 75 small modules (≤ 12.5 KB each) ⇒ ~0.5–3 min each at 2 threads nice 19 ⇒ 40–150 min wall; ≤ 8 GB RSS
# (one lean at a time); then --trust=0 probes (minutes) and leanchecker --fresh over the Mathlib closure (~2–3.5 h on this box).
# erdos cron tick 2026-10-14 03:00Z (Fable 5.1). Writes only under /tmp/erdos0300/lean.
set -u
L=/tmp/erdos0300/lean; SRC=$L/repo/lean; OUT=$L/out
export HOME=/tmp/oaimath/166/lean-build/home ELAN_HOME=/tmp/oaimath/166/lean-build/home/.elan
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export LEAN_PATH="$OUT:$(cat $L/lean_path.txt)"
export LEAN_NUM_THREADS=2 PATH="$TB:/usr/bin:/bin"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$L/steps.tsv"
while [ "$(memavail_gb)" -lt 22 ]; do log "waiting(mem): memavail=$(memavail_gb)G"; sleep 60; done
lean --version; log "openai/math rev: $(git -C $L/repo rev-parse HEAD)"; log "mathlib rev: $(git -C $L/mathlib4 rev-parse HEAD)"
# LEAN_PATH smoke: a Mathlib import must compile against the cache
echo 'import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
example : (1:ℝ) + 1 = 2 := by norm_num' > $L/probe/Smoke.lean
step smoke bash -c "cd $L/probe && nice -n 19 lean Smoke.lean > $L/logs/smoke.log 2>&1"
[ "$(tail -1 $L/steps.tsv | cut -d' ' -f2)" = 0 ] || { log "smoke failed: $(cat $L/logs/smoke.log | head -5)"; exit 11; }
build_one(){ local m="$1"; local o="$OUT/${m//.//}"; mkdir -p "$(dirname "$o")"
  ( cd "$SRC" && nice -n 19 ionice -c2 -n7 lean -DautoImplicit=false "${m//.//}.lean" -o "$o.olean" -i "$o.ilean" ) > "$L/logs/mod_$m.txt" 2>&1; local rc=$?
  echo "$m rc=$rc errors=$(grep -c 'error' "$L/logs/mod_$m.txt") lines=$(wc -l < "$L/logs/mod_$m.txt")" >> "$L/modules.tsv"; return $rc; }
t0=$SECONDS; n=0; total=$(grep -c . $L/order.txt)
while read -r m; do [ -z "$m" ] && continue; n=$((n+1)); ts=$SECONDS
  while [ "$(memavail_gb)" -lt 18 ]; do log "waiting(mem mid-build): memavail=$(memavail_gb)G"; sleep 60; done
  if build_one "$m"; then log "built $n/$total $m ($((SECONDS-ts))s)"; else log "FAILED $m — stopping"; echo "build 1 $((SECONDS-t0))" >> "$L/steps.tsv"; exit 1; fi
done < "$L/order.txt"
echo "build 0 $((SECONDS-t0))" >> "$L/steps.tsv"; log "all $total modules built; oleans: $(find $OUT -name '*.olean' | wc -l)"
step axioms bash -c "cd $L/probe && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms120.lean > $L/logs/axioms.log 2>&1"
step comparator bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false Comparator.lean > $L/logs/comparator.log 2>&1"
step negcontrol bash -c "cd $L/probe && nice -n 19 lean -DautoImplicit=false NegControl.lean > $L/logs/negcontrol.log 2>&1"
python3 - "$L" <<'PY'
import re,sys
L=sys.argv[1]
a=open(f"{L}/logs/axioms.log").read(); c=open(f"{L}/logs/comparator.log").read()
def grab(t,key):
    i=t.find(key); 
    if i<0: return None
    j=t.find("\n\n",i); seg=t[i:j if j>0 else None]
    return re.sub(r"\s+"," ",seg).strip()
# statement = the #check line for the theorem; definition = #print of dyadicPoint
sa=grab(a,"@OAI.Problem310.dyadic_affine_avoidance :"); sc=grab(c,"@OAI.Problem310.dyadic_affine_avoidance :")
da=grab(a,"def OAI.Problem310.dyadicPoint"); dc=grab(c,"def OAI.Problem310.dyadicPoint")
ax_main=grab(a,"'OAI.Problem310.dyadic_affine_avoidance' depends on axioms"); ax_cmp=grab(c,"'OAI.Problem310.dyadic_affine_avoidance' depends on axioms")
print("MAIN statement:",sa); print("CMP  statement:",sc); print("MAIN dyadicPoint:",da); print("CMP  dyadicPoint:",dc)
print("MAIN axioms:",ax_main); print("CMP axioms (must mention sorryAx):",ax_cmp)
ok = sa is not None and sa==sc and da is not None and da==dc
std = ax_main is not None and set(re.findall(r"\[([^\]]*)\]",ax_main)[0].replace(" ","").split(","))=={"propext","Classical.choice","Quot.sound"}
cmp_sorry = ax_cmp is not None and "sorryAx" in ax_cmp
print("STATEMENT MATCH:",ok,"| MAIN standard axioms:",std,"| comparator shows sorryAx:",cmp_sorry)
open(f"{L}/statement_match.txt","w").write(("MATCH" if ok else "MISMATCH")+"\n"+("STD_AXIOMS" if std else "NONSTD_AXIOMS")+"\n"+("CMP_SORRY_SEEN" if cmp_sorry else "CMP_SORRY_NOT_SEEN")+"\n")
PY
echo "statement_match $([ "$(head -1 $L/statement_match.txt)" = MATCH ] && echo 0 || echo 1) 0" >> "$L/steps.tsv"
log "negcontrol log head: $(head -c 600 $L/logs/negcontrol.log | tr '\n' ' ')"
while pgrep -x leanchecker >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 18 ]; do log "waiting(leanchecker gate): other=$(pgrep -c -x leanchecker) memavail=$(memavail_gb)G"; sleep 120; done
step leanchecker_fresh bash -c "cd $L/probe && nice -n 19 leanchecker --fresh OAI.MeasureTheory.DyadicAvoidance.Main > $L/logs/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $L/logs/leanchecker_fresh.log | tr '\n' ' ')"
O=$L/logs/leanchecker_controls.log; : > $O
echo "== NEG: leanchecker OAI.MeasureTheory.DyadicAvoidance.DoesNotExist ==" >> $O; timeout 600 nice -n 19 leanchecker OAI.MeasureTheory.DyadicAvoidance.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker OAI.MeasureTheory.DyadicAvoidance.Model (non-fresh) ==" >> $O; timeout 1800 nice -n 19 leanchecker OAI.MeasureTheory.DyadicAvoidance.Model >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
log DONE; cat $L/steps.tsv
