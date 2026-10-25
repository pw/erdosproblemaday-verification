#!/bin/bash
# Independent replay of cadamcat/hypercube-ramsey-lean4 on exe.dev (erdos cron tick 2026-10-11 12Z).
# Waits for the #172 replay (same 43 pinned package revs) to finish, then reuses its built packages.
set -u
S=/tmp/oaimath/171/lean-build
P172=/tmp/oai-math/lean-build
cd "$S"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
echo "relaunch $(date -u +%FT%TZ) 0 0" >> "$S/steps.tsv"
while pgrep -x lake >/dev/null 2>&1 || [ -n "$(pgrep -f "$P172/run.sh" 2>/dev/null)" ]; do log "waiting for #172 replay (lake/run.sh alive)"; sleep 120; done
log "#172 replay finished: $(cat $P172/steps.tsv | tr '\n' ';')"
if [ ! -d repo/.git ]; then step clone git clone -q https://github.com/cadamcat/hypercube-ramsey-lean4 repo || exit 10; fi
cd repo
git checkout -q 35fa13445f3ab7a1934f0e293cb49f86b83d13da || log "checkout of pinned HEAD failed; staying on $(git rev-parse HEAD)"
log "repo HEAD $(git rev-parse HEAD) $(git log -1 --format=%ci)"; git tag -l | sed 's/^/tag: /'
export HOME="$S/home" ELAN_HOME="$S/home/.elan" PATH="$S/home/.elan/bin:/usr/local/bin:/usr/bin:/bin"
export LEAN_NUM_THREADS=4 ELAN_TOOLCHAIN_GC_DISABLE=1
mkdir -p "$S/home"
if [ -d "$S/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin" ]; then log "toolchain already copied"; else step copy_toolchain cp -a "$P172/home/.elan" "$S/home/.elan"; fi
which lake lean || { log "lake not found under scratch ELAN_HOME; falling back to proxies (as the #172 driver did)"; export PATH="/home/exedev/.elan/bin:$PATH"; }
which lake lean || { log "still no lake; using the toolchain bin directly"; export PATH="$S/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:$PATH"; }
which lake lean || { log "no lake anywhere"; exit 11; }
lake --version; lean --version
mkdir -p .lake
if [ -d .lake/packages/mathlib ]; then log "packages already copied"; else step copy_packages cp -a "$P172/repo/.lake/packages" .lake/packages; fi
log "OAI package rev: $(git -C .lake/packages/OAI rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
python3 - <<'PY'
import json
a=json.load(open('/tmp/oai-math/lean-build/repo/lake-manifest.json')); b=json.load(open('lake-manifest.json'))
ra={p['name']:p.get('rev') for p in a['packages']}; rb={p['name']:p.get('rev') for p in b['packages']}
bad=[(k,ra.get(k),rb[k]) for k in rb if ra.get(k)!=rb[k]]
print("manifest revs identical" if not bad else f"MANIFEST MISMATCH {bad}")
PY
step patches scripts/apply-oai-patches.sh
step cache_get lake exe cache get
step build lake build HypercubeRamsey.Main
step verify bash scripts/verify.sh
step axioms_copy cp .lake/verification-results/axioms.log "$S/axioms.log"
step audit_probes lake env lean --trust=0 Audit/TargetProbes.lean
step audit_restatement lake env lean --trust=0 Audit/IndependentRestatement.lean
mkdir -p .lake/verification-results
step leanchecker_fresh bash -c "lake env leanchecker --fresh HypercubeRamsey.Main > $S/leanchecker_fresh.log 2>&1"
log "leanchecker tail: $(tail -3 $S/leanchecker_fresh.log | tr '\n' ' ')"
# Also re-check the #172 project's whole import closure in a fresh kernel (its driver only ran #print axioms).
step leanchecker_fresh_172 bash -c "cd $P172/repo && HOME=$P172/home ELAN_HOME=$P172/home/.elan PATH=$P172/home/.elan/bin:/usr/local/bin:/usr/bin:/bin lake env leanchecker --fresh HindmanSumsProducts.Main > $P172/leanchecker_fresh.log 2>&1"
log "172 leanchecker tail: $(tail -3 $P172/leanchecker_fresh.log | tr '\n' ' ')"
log "DONE"; cat "$S/steps.tsv"
