#!/bin/bash
# Independent kernel replay of cadamcat/distinct-distances-lean4 (Erdős #1083, OpenAI family 166) on exe.dev.
# erdos cron tick 2026-10-11 21:00Z. Waits until the #181 replay's build is past `verify` AND the box has >30 GB
# MemAvailable, then reuses the #181 replay's built packages (manifest revs verified identical: OAI adc7f124, mathlib d13f23b7).
set -u
S=/tmp/oaimath/166/lean-build
P181=/tmp/oaimath/171/lean-build
cd "$S"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
echo "launch $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
memavail_gb(){ awk '/MemAvailable/{printf "%d", $2/1024/1024}' /proc/meminfo; }
# Gate 1: the #181 driver has logged its `verify` step (its lake build is over), or is gone entirely.
while ! grep -q '^verify ' "$P181/steps.tsv" 2>/dev/null && kill -0 "$(cat $P181/pid 2>/dev/null)" 2>/dev/null; do log "waiting: #181 replay still building (last step: $(tail -1 $P181/steps.tsv | tr -d '\n'))"; sleep 180; done
log "#181 past verify (or gone): $(tail -3 $P181/steps.tsv | tr '\n' ';')"
# Gate 2: no lake build of another project alive, and memory headroom for a 4-thread Lean build (~30 GB peak).
while pgrep -x lake >/dev/null 2>&1 || [ "$(memavail_gb)" -lt 30 ]; do log "waiting: lake alive=$(pgrep -c -x lake) memavail=$(memavail_gb)G"; sleep 120; done
log "gates open: memavail=$(memavail_gb)G load=$(cut -d' ' -f1 /proc/loadavg)"
if [ ! -d repo/.git ]; then step clone git clone -q https://github.com/cadamcat/distinct-distances-lean4 repo || exit 10; fi
cd repo
git fetch -q --tags origin 2>/dev/null; git checkout -q 88919b8137844c402935f0c6f2cb2ba082c054d7 2>/dev/null || log "checkout of pinned HEAD failed; staying on $(git rev-parse HEAD)"
log "repo HEAD $(git rev-parse HEAD) $(git log -1 --format=%ci)"; git tag -l | sed 's/^/tag: /'; log "v1.0.0 = $(git rev-parse v1.0.0 2>/dev/null)"
export HOME="$S/home" ELAN_HOME="$S/home/.elan"
export LEAN_NUM_THREADS=4 ELAN_TOOLCHAIN_GC_DISABLE=1
mkdir -p "$S/home"
if [ -d "$S/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin" ]; then log "toolchain already copied"; else step copy_toolchain cp -a "$P181/home/.elan" "$S/home/.elan"; fi
export PATH="$S/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin"
which lake lean || { log "no lake under the toolchain bin"; exit 11; }
lake --version; lean --version
mkdir -p .lake
if [ -d .lake/packages/mathlib ]; then log "packages already copied"; else step copy_packages cp -a "$P181/repo/.lake/packages" .lake/packages; fi
log "OAI package rev: $(git -C .lake/packages/OAI rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
python3 - <<'PY'
import json
a=json.load(open('/tmp/oaimath/171/lean-build/repo/lake-manifest.json')); b=json.load(open('lake-manifest.json'))
ra={p['name']:p.get('rev') for p in a['packages']}; rb={p['name']:p.get('rev') for p in b['packages']}
bad=[(k,ra.get(k),rb[k]) for k in rb if ra.get(k)!=rb[k]]
print("manifest revs identical" if not bad else f"MANIFEST MISMATCH {bad}")
PY
step patches scripts/apply-oai-patches.sh
step cache_get lake exe cache get
step build nice -n 19 ionice -c2 -n7 lake build DistinctDistances.Main
step verify nice -n 19 bash scripts/verify.sh
step axioms_copy cp .lake/verification-results/axioms.log "$S/axioms.log"
step audit_probes nice -n 19 lake env lean --trust=0 Audit/TargetProbes.lean
step audit_restatement nice -n 19 lake env lean --trust=0 Audit/IndependentRestatement.lean
step audit_nonvacuity nice -n 19 lake env lean --trust=0 Audit/NonVacuity.lean
mkdir -p .lake/verification-results
step leanchecker_fresh bash -c "nice -n 19 lake env leanchecker --fresh DistinctDistances.Main > $S/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $S/leanchecker_fresh.log | tr '\n' ' ')"
log "DONE"; cat "$S/steps.tsv"
