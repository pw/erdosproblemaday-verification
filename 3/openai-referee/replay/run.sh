#!/bin/bash
# Independent kernel replay of OpenAI's OWN Lean proof of Erdős #3 (ReciprocalProgressionTheorem, family 159), on exe.dev.
# erdos cron tick 2026-10-12 06:00Z. Builds the solution module OAI.Combinatorics.Progressions.Main inside the #1083 replay
# workspace (/tmp/oaimath/166/lean-build/repo — OAI package pinned adc7f124, Mathlib d13f23b7, oleans for 2,100 of the 4,774
# Progressions modules already present), then #print axioms under --trust=0, a pp.all statement comparison against the
# Comparator challenge module, a sorry negative control, and leanchecker --fresh over the import closure.
set -u
S=/tmp/oaimath/159/lean-build
W=/tmp/oaimath/166/lean-build
cd "$S"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
# Gate: the #1083 leanchecker --fresh running in this same workspace must be gone (it mmaps oleans we might rebuild),
# and memory headroom for a 4-thread Lean build (~30 GB peak) must exist.
disk_gb(){ df --output=avail -BG /tmp | tail -1 | tr -dc 0-9; }
while pgrep -f 'leanchecker --fresh DistinctDistances' >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 36 ] || [ "$(disk_gb)" -lt 10 ]; do log "waiting: 1083-leanchecker alive=$(pgrep -c -f 'leanchecker --fresh DistinctDistances') memavail=$(memavail_gb)G disk=$(disk_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"; sleep 120; done
log "gates open: memavail=$(memavail_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"
cd "$W/repo" || exit 10
export HOME="$W/home" ELAN_HOME="$W/home/.elan"
export LEAN_NUM_THREADS=4 ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$W/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin"
which lake lean || { log "no lake under the toolchain bin"; exit 11; }
lake --version; lean --version
log "OAI package rev: $(git -C .lake/packages/OAI rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
log "Progressions oleans before: $(find .lake/packages/OAI/lean/.lake/build/lib/lean/OAI/Combinatorics/Progressions -name '*.olean' | wc -l)"
step build nice -n 19 ionice -c2 -n7 lake build OAI/+OAI.Combinatorics.Progressions.Main
log "Progressions oleans after: $(find .lake/packages/OAI/lean/.lake/build/lib/lean/OAI/Combinatorics/Progressions -name '*.olean' | wc -l)"
step axioms bash -c "nice -n 19 lake env lean --trust=0 $S/Erdos3Axioms.lean > $S/axioms.log 2>&1"
step challenge bash -c "nice -n 19 lake env lean --trust=0 $S/ChallengeStatement.lean > $S/challenge.log 2>&1"
step negcontrol bash -c "nice -n 19 lake env lean $S/NegControl.lean > $S/negcontrol.log 2>&1"
python3 - "$S" <<'PY'
import re,sys
S=sys.argv[1]
a=open(f"{S}/axioms.log").read(); c=open(f"{S}/challenge.log").read()
def blocks(t):
    out={}
    for m in re.finditer(r"(?ms)^(?:@\[[^\]]*\] )?(?:noncomputable )?def (OAI\.Erdos3\.\w+)(.*?)(?=^\S|\Z)", t):
        out[m.group(1)]=re.sub(r"\s+"," ",m.group(2)).strip()
    return out
A,C=blocks(a),blocks(c)
ok=True
for k in ["OAI.Erdos3.ReciprocalProgressionTheorem","OAI.Erdos3.HasAP","OAI.Erdos3.reciprocalTerm"]:
    same = A.get(k) is not None and A.get(k)==C.get(k)
    print(f"pp.all identical {k}: {same}"); ok = ok and same
print("STATEMENT MATCH:", ok)
open(f"{S}/statement_match.txt","w").write(("MATCH" if ok else "MISMATCH")+"\n")
PY
echo "statement_match $([ "$(cat $S/statement_match.txt)" = MATCH ] && echo 0 || echo 1) 0" >> "$S/steps.tsv"
step leanchecker_fresh bash -c "nice -n 19 lake env leanchecker --fresh OAI.Combinatorics.Progressions.Main > $S/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $S/leanchecker_fresh.log | tr '\n' ' ')"
log "DONE"; cat "$S/steps.tsv"
