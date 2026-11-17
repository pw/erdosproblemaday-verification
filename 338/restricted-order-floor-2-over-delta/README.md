# Erdős #338 at positive density: the restricted order is at most ⌊2/δ⌋ − 1, and that is sharp (17 Nov 2026)

Page: https://erdosproblemaday.com/day/338-restricted-order-at-density-delta-is-exactly-floor-2-over-delta-minus-1
Previous entry (15 Nov, bound 4⌈1/δ⌉ − 4): ../density-theorem-refereed-linear-bound-kelly-exceptions/

## Claim (label (b): rigorous modulo Kneser 1953 (integers and finite abelian groups), Olson 1984 and Varnavides 1959 / Roth)
A ⊆ ℕ, lower density δ ∈ (0, 1/2], and for every modulus g the residue classes mod g containing infinitely many
members of A generate ℤ/g. Then every large integer is a sum of at most ⌊2/δ⌋ − 1 DISTINCT members of A.
Sharp: {n ≡ 0, 1 mod ⌊2/δ⌋} has density ≥ δ and restricted order exactly ⌊2/δ⌋ − 1.
Full statement and proof, every case of the final count: CLAIMS.md.

## Chain
1. Good members B (middle of ≥ R three-term APs in A): A \ B has density 0 (Varnavides); repeats of good members are
   made distinct by (a−d)+(a+d) pairs.
2. Kneser iteration on B ∪ {0}: first k with no δ-increment; then X_{k+1} is cofinite in |P| + |S| − 1 classes mod g,
   |P| ≥ kδg, |S| ≥ δg.
3. Growth lemma in ℤ/g: 0 ∈ S′ generating, Z + S′ ≠ ℤ/g ⇒ |Z + S′| ≥ |Z| + ⌈|S′|/2⌉ (Kneser in finite groups);
   |S′| ≥ δg where S′ = infinite classes of A plus 0.
4. Count with m = ⌊2/δ⌋, δ(m+1) > 2: k + 1 + (filling steps) ≤ m − 1 in every case.

## Programs (all deterministic; outputs committed beside them)
- growth_lemma_check.c — exhaustive check of step 3 for every Z, every generating S′ ∋ 0, g ≤ 12 (1.6 M cases, 0 failures).
  Controls: non-generating S′ and the sharper |S′| − 1 gain both produce counterexamples (the latter only at composite g).
  gcc -O2 -o growth_lemma_check growth_lemma_check.c && ./growth_lemma_check 12
- proof_arith_check.py / proof_arith_check2.py — enumerate every integer configuration the proof allows; for all 551
  δ = p/q ≤ 1/2 (q ≤ 60), g ≤ 60/δ, the worst total is exactly ⌊2/δ⌋ − 1, never more. Control: with one class per
  filling step the bound fails at 30 of 35 sampled δ.  python3 proof_arith_check2.py
- model_census.c — exact restricted order of periodic-plus-sparse model sets (full classes D, sparse classes E usable any
  number of times, ≥ 1 summand from D), m ≤ 15, 13.0 M sets: none exceeds ⌊2m/|D|⌋ − 1; ⌈⌉ − 2 is exceeded (control);
  non-generating sets flagged unreachable.  gcc -O2 -o model_census model_census.c && ./model_census 15

## Seats
REFEREE.md (hostile referee, Opus 5.5 instance), WORLD.md (literature seat), BLIND.md (blind reader of the page).

## Reproduce
Everything above runs in under 2 minutes on one core (model_census m = 15 is the slowest, ~1 min).

## Corrections made before publishing (see BLIND.md, WORLD.md)
- Lemma 1 is Olson's lemma; the group version of the whole bound is Hamidoune–Rødseth 1996; Hegarty 2009 Lemma 3.3 gives
  4/d for integer (ordinary) bases. What is ours: the exact constant ⌊2/δ⌋ − 1 for integers, for distinct summands, under (H).
- The page uses the blind reader's four-line count (CLAIMS.md, last section) in place of the case analysis.
