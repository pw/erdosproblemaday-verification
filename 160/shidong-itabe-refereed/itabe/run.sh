#!/bin/bash
# Kernel replay of Rio Itabe's Lean 4 development for Erdős #160 (H(N) <= N^(1/3+eps) eventually), tag v0.2.1-review-candidate,
# commit fd426c9, Lean v4.30.0 + Mathlib v4.30.0 (TAGGED release => `lake exe cache get`, minutes). erdos cron 2026-10-13 18:00Z seat.
# Estimate BEFORE CPU: 20 first-party modules / ~200 KB; cache get ~4 min + ~6 GB disk; build ~10-40 min wall at 2 threads
# (one lean ~3-5 GB RSS each); then --trust=0 axiom/statement probes (minutes). leanchecker --fresh over the Mathlib closure
# afterwards (hours, ~8 GB) behind a memory gate. Memory guard (cron/erdos.md 10-13): need >= 20 GB available AFTER our RSS.
set -u
S=/tmp/erdos160/itabe/lean-build; R=/tmp/erdos160/itabe/repo
cd "$S"; log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
while [ "$(memavail_gb)" -lt 30 ]; do log "waiting(build): memavail=$(memavail_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"; sleep 120; done
cd "$R" || exit 10
export PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=2 ELAN_TOOLCHAIN_GC_DISABLE=1
lake --version; lean --version; git rev-parse HEAD; git describe --tags
step cache_get nice -n 19 lake exe cache get
step build nice -n 19 lake build ErdosProblems -j2
step their_audit bash -c "nice -n 19 lake env lean --trust=0 AxiomAudit.lean > $S/their_axioms.log 2>&1"
step our_audit bash -c "nice -n 19 lake env lean --trust=0 $S/Axioms160.lean > $S/axioms.log 2>&1"
step negcontrol bash -c "nice -n 19 lake env lean $S/NegControl.lean > $S/negcontrol.log 2>&1"
step their_check_release bash -c "nice -n 19 bash scripts/check_release.sh > $S/check_release.log 2>&1"
step source_scan bash -c "grep -RnE --include='*.lean' 'sorry|admit|native_decide|implemented_by|extern|unsafe|partial def|opaque|axiom ' ErdosProblems AxiomAudit.lean ErdosProblems.lean > $S/source_scan.log 2>&1; true"
log "axioms.log tail:"; tail -12 "$S/axioms.log"
# leanchecker --fresh (Mathlib closure rechecked; hours) behind a memory gate; one at a time on the box
while pgrep -x leanchecker >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 28 ]; do log "waiting(leanchecker): other=$(pgrep -c -x leanchecker) memavail=$(memavail_gb)G"; sleep 120; done
step leanchecker_fresh bash -c "nice -n 19 lake env leanchecker --fresh ErdosProblems.E160.RealAsymptotics > $S/leanchecker_fresh.log 2>&1"
O=$S/leanchecker_controls.log; : > $O
echo "== NEG: leanchecker ErdosProblems.E160.DoesNotExist ==" >> $O; timeout 600 nice -n 19 lake env leanchecker ErdosProblems.E160.DoesNotExist >> $O 2>&1; echo "neg rc=$?" >> $O
echo "== POS: leanchecker ErdosProblems.E160.Problem (non-fresh) ==" >> $O; timeout 1800 nice -n 19 lake env leanchecker ErdosProblems.E160.Problem >> $O 2>&1; echo "pos rc=$?" >> $O
echo DONE >> $O
log DONE; cat "$S/steps.tsv"
