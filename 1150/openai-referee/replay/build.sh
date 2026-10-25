#!/bin/bash
# Manual (lake-free) kernel replay of OpenAI's Lean proof behind Erdős #1150 — compiles the 28-module import cone of
# OAI.Analysis.Littlewood.{Main,FiniteFlatness} with the toolchain's `lean` directly, in topological order, writing oleans into
# OUR OWN directory; Mathlib and every other package olean is read from the #166 workspace via the exact LEAN_PATH Lake gave its
# own compiler processes (captured from /proc of a running #3 build job), plus the one option Lake passes (-DautoImplicit=false).
# Nothing in /tmp/oaimath/166 is written. Estimate before CPU: 28 modules / 9,712 lines; 1–5 min each at 2 threads ⇒ 30–90 min
# wall, ≤ ~8 GB RAM (one lean at a time). erdos cron tick 2026-10-12 09:00Z (Fable 5.1).
set -u
S=/tmp/oaimath/076/lean-build; M=$S/manual; OUT=$M/out
SRC=/tmp/oaimath/166/lean-build/repo/.lake/packages/OAI/lean
TB=/tmp/oaimath/166/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin
export LEAN_PATH="$OUT:$(cat $M/lake_lean_path.txt)"
export LEAN_NUM_THREADS=2 PATH="$TB:/usr/bin:/bin"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
echo "launch_manual $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
while [ "$(memavail_gb)" -lt 20 ]; do log "waiting(mem): memavail=$(memavail_gb)G"; sleep 60; done
lean --version; log "OAI package rev: $(git -C $SRC rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C /tmp/oaimath/166/lean-build/repo/.lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
log "LEAN_PATH entries: $(echo "$LEAN_PATH" | tr ':' '\n' | wc -l)"
build_one(){ local m="$1"; local src="$SRC/${m//.//}.lean"; local o="$OUT/${m//.//}"; mkdir -p "$(dirname "$o")"
  ( cd "$SRC" && nice -n 19 ionice -c2 -n7 lean -DautoImplicit=false "${m//.//}.lean" -o "$o.olean" -i "$o.ilean" ) > "$M/log_$m.txt" 2>&1; local rc=$?
  local errs=$(grep -c "error" "$M/log_$m.txt"); echo "$m rc=$rc errors=$errs lines=$(wc -l < "$M/log_$m.txt")" >> "$M/modules.tsv"; return $rc; }
t0=$SECONDS; n=0
while read -r m; do [ -z "$m" ] && continue; n=$((n+1)); ts=$SECONDS
  if build_one "$m"; then log "built $n/28 $m ($((SECONDS-ts))s)"; else log "FAILED $m rc — stopping"; echo "build 1 $((SECONDS-t0))" >> "$S/steps.tsv"; exit 1; fi
done < "$M/order.txt"
echo "build 0 $((SECONDS-t0))" >> "$S/steps.tsv"; log "all 28 modules built; oleans: $(find $OUT -name '*.olean' | wc -l)"
step axioms bash -c "cd $S && nice -n 19 lean --trust=0 -DautoImplicit=false Axioms1150.lean > $S/axioms.log 2>&1"
step challenge bash -c "cd $S && nice -n 19 lean --trust=0 -DautoImplicit=false ChallengeStatement.lean > $S/challenge.log 2>&1"
step negcontrol bash -c "cd $S && nice -n 19 lean NegControl.lean > $S/negcontrol.log 2>&1"
python3 - "$S" <<'PY'
import re,sys
S=sys.argv[1]
a=open(f"{S}/axioms.log").read(); c=open(f"{S}/challenge.log").read()
def blocks(t):
    out={}
    for m in re.finditer(r"(?ms)^(?:@\[[^\]]*\] )?(?:noncomputable )?def (OAI\.AsymptoticallyMinimalLittlewood\.\w+)(.*?)(?=^\S|\Z)", t):
        out[m.group(1)]=re.sub(r"\s+"," ",m.group(2)).strip()
    return out
A,C=blocks(a),blocks(c)
ok=True
for k in ["OAI.AsymptoticallyMinimalLittlewood.MainStatement","OAI.AsymptoticallyMinimalLittlewood.littlewoodValue","OAI.AsymptoticallyMinimalLittlewood.IsRealSigning"]:
    same = A.get(k) is not None and A.get(k)==C.get(k)
    print(f"pp.all identical {k}: {same}"); ok = ok and same
print("STATEMENT MATCH:", ok)
open(f"{S}/statement_match.txt","w").write(("MATCH" if ok else "MISMATCH")+"\n")
PY
echo "statement_match $([ "$(cat $S/statement_match.txt)" = MATCH ] && echo 0 || echo 1) 0" >> "$S/steps.tsv"
while pgrep -f 'leanchecker --fresh' >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 16 ]; do log "waiting(leanchecker): other=$(pgrep -c -f 'leanchecker --fresh') memavail=$(memavail_gb)G"; sleep 120; done
step leanchecker_fresh bash -c "nice -n 19 leanchecker --fresh OAI.Analysis.Littlewood.Main > $S/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $S/leanchecker_fresh.log | tr '\n' ' ')"
O=$S/leanchecker_controls.log; : > $O
echo "== NEG: leanchecker OAI.Analysis.Littlewood.DoesNotExist ==" >> $O; timeout 600 nice -n 19 leanchecker OAI.Analysis.Littlewood.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker OAI.Analysis.Littlewood.Model (non-fresh) ==" >> $O; timeout 1800 nice -n 19 leanchecker OAI.Analysis.Littlewood.Model >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
log "DONE"; cat "$S/steps.tsv"
