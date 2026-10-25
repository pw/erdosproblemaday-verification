#!/bin/bash
# Kernel replay of LiAlreadyExists/Erdos-341 @ c1d9121 (Lean v4.33.0-rc1, Mathlib v4.33.0-rc1). Steps logged to steps.tsv.
set -u
export PATH="$HOME/.elan/bin:$PATH"
export ELAN_HOME="$HOME/.elan"
REPO=/tmp/erdos2100/li/repo
LB=/tmp/erdos2100/lean-build
STEPS=$LB/steps.tsv
cd "$REPO" || exit 9
step(){ local name=$1; shift; local t0=$(date +%s); "$@" > "$LB/$name.log" 2>&1; local rc=$?; local t1=$(date +%s); printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$((t1-t0))" "$(date -u +%FT%TZ)" >> "$STEPS"; return $rc; }
echo "start $(date -u +%FT%TZ) pid $$" >> "$STEPS"
step toolchain2 lean --version || exit 1
step cache_get lake exe cache get || exit 2
step build lake build || exit 3
# our audit file: axioms + pp.all statement of the final theorem; negative control with sorry
step audit lake env lean /tmp/erdos2100/scripts/Audit341.lean
step negcontrol lake env lean /tmp/erdos2100/scripts/NegControl341.lean
step source_scan bash -c 'grep -nE "sorry|admit|native_decide|implemented_by|@\[extern|unsafe|partial def|opaque|^axiom|\baxiom\b" LeanProject/*.lean LeanProject.lean; true'
echo "done $(date -u +%FT%TZ)" >> "$STEPS"
