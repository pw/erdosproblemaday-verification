#!/bin/bash
# Independent replay of cadamcat/hindman-sums-products-lean4 on exe.dev (erdos cron tick 2026-10-11 ~07Z).
# Sandboxed: scrubbed env, scratch HOME/ELAN_HOME; bwrap hides /home/exedev and /tmp except this dir when available.
set -u
S=/tmp/oai-math/lean-build
cd "$S"
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
step(){ local name="$1"; shift; log "BEGIN $name :: $*"; local t0=$SECONDS; "$@"; local rc=$?; log "END $name rc=$rc elapsed=$((SECONDS-t0))s"; echo "$name $rc $((SECONDS-t0))" >> "$S/steps.tsv"; return $rc; }
: > "$S/steps.tsv"
if [ ! -d repo/.git ]; then step clone git clone -q https://github.com/cadamcat/hindman-sums-products-lean4 repo || exit 10; fi
cd repo
log "repo HEAD $(git rev-parse HEAD) $(git log -1 --format=%ci)"; git tag -l | sed 's/^/tag: /'
export HOME="$S/home" ELAN_HOME="$S/home/.elan" PATH="$S/home/.elan/bin:/usr/local/bin:/usr/bin:/bin"
export LEAN_NUM_THREADS=4 ELAN_TOOLCHAIN_GC_DISABLE=1
step elan_install /home/exedev/.elan/bin/elan toolchain install "$(cat lean-toolchain)" || true
export PATH="$ELAN_HOME/bin:$PATH"; ls "$ELAN_HOME/bin" 2>/dev/null | head; which lake lean || { log "lake not found under scratch ELAN_HOME; falling back to proxies"; export PATH="/home/exedev/.elan/bin:$PATH"; }
lake --version; lean --version
step lake_update lake update; log "(lake update exit above; the OAI hook error is expected per docs)"
step patches scripts/apply-oai-patches.sh
log "OAI package rev: $(git -C .lake/packages/OAI rev-parse HEAD 2>/dev/null)"; log "mathlib rev: $(git -C .lake/packages/mathlib rev-parse HEAD 2>/dev/null)"
step cache_get lake exe cache get
step build lake build -j 4
step verify bash scripts/verify.sh
step nonvacuity lake env lean --trust=0 audit/NonVacuity.lean
log "DONE"; cat "$S/steps.tsv"
