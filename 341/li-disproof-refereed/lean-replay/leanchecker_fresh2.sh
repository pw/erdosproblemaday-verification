#!/bin/bash
set -u
export PATH="$HOME/.elan/bin:$PATH"
REPO=/tmp/erdos2100/li/repo; LB=/tmp/erdos2100/lean-build; STEPS=$LB/steps.tsv
cd "$REPO" || exit 9
step(){ local name=$1; shift; local t0=$(date +%s); "$@" > "$LB/$name.log" 2>&1; local rc=$?; local t1=$(date +%s); printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$((t1-t0))" "$(date -u +%FT%TZ)" >> "$STEPS"; return $rc; }
echo "leanchecker_fresh2 start $(date -u +%FT%TZ) pid $$ (single module LeanProject = closure of Erdos341 + Erdos341g + Shield + Mathlib)" >> "$STEPS"
step leanchecker_fresh_LeanProject lake env leanchecker --fresh LeanProject
echo "leanchecker_fresh2 done $(date -u +%FT%TZ)" >> "$STEPS"
