#!/bin/bash
# Kernel replay of Gessel's Erdos488.lean (gist d8e15e5f..., head 9bbb516). Logs to replay.log; steps to steps.tsv
cd /tmp/e488/lean
export PATH="$HOME/.elan/bin:$PATH"
step(){ echo -e "$(date -u +%FT%TZ)\t$1\t$2" >> steps.tsv; }
step start "sha256 $(sha256sum Erdos488.lean | cut -c1-16)"
elan toolchain install leanprover/lean4:v4.33.0 >> replay.log 2>&1; step toolchain $?
lake update >> replay.log 2>&1; step lake_update $?
git -C .lake/packages/mathlib rev-parse HEAD >> replay.log 2>&1
lake exe cache get Mathlib.NumberTheory.SmoothNumbers Mathlib.Data.Nat.Totient Mathlib.Algebra.Order.BigOperators.Group.Finset Mathlib.Tactic.NormNum Mathlib.Tactic.Linarith Mathlib.Data.Nat.Factorization.Basic Mathlib.Data.Fintype.Card Mathlib.Data.Fintype.BigOperators Mathlib.Order.Interval.Finset.Nat Mathlib.Tactic.ByContra Mathlib.Data.Nat.GCD.BigOperators Mathlib.Data.Finset.Max Mathlib.Tactic.Tauto >> replay.log 2>&1; step cache_get $?
/usr/bin/time -v lake env lean -o Erdos488.olean Erdos488.lean > lean_out.log 2> lean_time.log; step lean_compile $?
cat lean_out.log >> replay.log
step done "$(grep -c 'depends on axioms' lean_out.log) axiom lines"
