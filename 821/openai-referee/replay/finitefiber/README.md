# Kernel check of OpenAI's partial formal artifact for family 011

`lean/OAI/NumberTheory/TotientFibers/FiniteFiber.lean` in github.com/openai/math (initial commit adc7f124, 2026-10-06; 312 lines,
imports only Mathlib) formalizes the CONDITIONAL §8 step of the paper: given a finite set P of primes p ≤ t^a with p−1 t-smooth and
|P| > t^{a−1}, some n has g(n) > n^{1−ε} (`finite_large_fiber_rpow`). It does NOT formalize Theorem 1.2 (the smooth-shifted-prime
count), which is the whole content of the paper; the release's formalization.yaml has no entry for the family.

What we did (2026-10-11, erdos cron seat): copied the file verbatim (sha256 of the original in ../../world/oai_FiniteFiber_2026-10-11.lean),
appended three `#print axioms` lines, and compiled it with the Lean 4.34.1 toolchain + the Mathlib build already produced for the
#172 replay (`/tmp/oai-math/lean-build/repo`, pinned mathlib rev as in that project's lake-manifest), `lake env lean --trust=0`,
scrubbed HOME/ELAN_HOME. Result (lean_trust0_out.log): compiles with no errors; all three theorems depend on
[propext, Classical.choice, Quot.sound]. Wall 1m55s. Caveat as for #172/#181: `--trust=0` does not re-check the cached Mathlib
oleans; this certifies the file as compiled from source against that build.
