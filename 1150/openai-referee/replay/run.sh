#!/bin/bash
# Independent kernel replay of OpenAI's OWN Lean proof behind Erdős #1150 (OAI.AsymptoticallyMinimalLittlewood.main,
# family 076) + the family's second formalized claim (FiniteFlatness), on exe.dev. erdos cron tick 2026-10-12 09:00Z.
# Estimate written BEFORE any CPU: joint import cone = 28 OAI modules / 9,712 lines (Mathlib only otherwise), 0 oleans
# present; comparable OAI modules built at 41 s CPU mean in the #172 log, analysis modules heavier ⇒ ~1–2 CPU-h,
# ~15–45 min wall at 4 threads nice 19, ≤ 30 GB RAM, < 200 MB disk. Then --trust=0 probes (seconds–minutes), then
# leanchecker --fresh over the import closure (Mathlib re-check dominates: 2–4 h on the #1083/#172 builds).
# Workspace = the #1083/#3 replay workspace (/tmp/oaimath/166/lean-build/repo, OAI adc7f124, Mathlib d13f23b7).
set -u
S=/tmp/oaimath/076/lean-build
W=/tmp/oaimath/166/lean-build
cd "$S"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
disk_gb(){ df --output=avail -BG /tmp | tail -1 | tr -dc 0-9; }
lake3_alive(){ pgrep -f 'lake build OAI/\+OAI\.Combinatorics\.Progressions' >/dev/null 2>&1; }
# Gate 1 (build): the #3 lake build in this same workspace must be gone (two lakes in one workspace fight over .lake);
# a concurrent leanchecker only READS oleans we do not touch, so it is tolerated at this step; RAM headroom for 4 lean threads.
while lake3_alive || [ "$(memavail_gb)" -lt 30 ] || [ "$(disk_gb)" -lt 5 ]; do log "waiting(build): lake3=$(lake3_alive && echo yes || echo no) memavail=$(memavail_gb)G disk=$(disk_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"; sleep 120; done
log "gate 1 open: memavail=$(memavail_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"
cd "$W/repo" || exit 10
export HOME="$W/home" ELAN_HOME="$W/home/.elan"
export LEAN_NUM_THREADS=4 ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$W/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin"
which lake lean || { log "no lake under the toolchain bin"; exit 11; }
lake --version; lean --version
log "OAI package rev: $(git -C .lake/packages/OAI rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
log "Littlewood oleans before: $(find .lake/packages/OAI/lean/.lake/build/lib/lean/OAI/Analysis/Littlewood -name '*.olean' 2>/dev/null | wc -l)"
step build nice -n 19 ionice -c2 -n7 lake build OAI/+OAI.Analysis.Littlewood.Main OAI/+OAI.Analysis.Littlewood.FiniteFlatness
log "Littlewood oleans after: $(find .lake/packages/OAI/lean/.lake/build/lib/lean/OAI/Analysis/Littlewood -name '*.olean' 2>/dev/null | wc -l)"
step axioms bash -c "nice -n 19 lake env lean --trust=0 $S/Axioms1150.lean > $S/axioms.log 2>&1"
step challenge bash -c "nice -n 19 lake env lean --trust=0 $S/ChallengeStatement.lean > $S/challenge.log 2>&1"
step negcontrol bash -c "nice -n 19 lake env lean $S/NegControl.lean > $S/negcontrol.log 2>&1"
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
# Gate 2 (leanchecker): no other leanchecker --fresh (each is ~8 GB and hours); then ours over the Main closure.
while pgrep -f 'leanchecker --fresh' >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 20 ]; do log "waiting(leanchecker): other=$(pgrep -c -f 'leanchecker --fresh') memavail=$(memavail_gb)G"; sleep 120; done
step leanchecker_fresh bash -c "nice -n 19 lake env leanchecker --fresh OAI.Analysis.Littlewood.Main > $S/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $S/leanchecker_fresh.log | tr '\n' ' ')"
# controls for reading leanchecker's silence (same shape as #181/#1083): NEG must fail loudly, POS (non-fresh, small real module) exit 0 silently
O=$S/leanchecker_controls.log; : > $O
echo "== NEG: leanchecker OAI.Analysis.Littlewood.DoesNotExist ==" >> $O; timeout 600 nice -n 19 lake env leanchecker OAI.Analysis.Littlewood.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker OAI.Analysis.Littlewood.Model (non-fresh) ==" >> $O; timeout 1800 nice -n 19 lake env leanchecker OAI.Analysis.Littlewood.Model >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
log "DONE"; cat "$S/steps.tsv"
