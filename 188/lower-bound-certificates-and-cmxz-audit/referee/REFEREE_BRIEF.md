# Hostile referee brief — Erdős #188 tick, 2026-10-14

You are refereeing, adversarially, a short write-up that will go on a public scoreboard. Your job is to BREAK it. Quote the
exact sentence or line you object to. Output a report with sections FATAL / GAP / NOTE, each item: quote → why → what would fix it.
If you find nothing fatal, say HOLDS AS READ and list what you checked.

Files (read them; run them if you want, Python at ~/.venv/bin/python has numpy/scipy/sympy/pysat; cadical is on PATH):
* ~/ErdosProblemADay-0014/verification/188/lower-bound-certificates-and-cmxz-audit/README.md  — the claims
* same dir: config188.py (builds instances), mus188.py (minimal core), verify_core.py (exact sympy check), describe_core.py,
  cmxz_audit.py, cores/*.core.json, cores/*.describe.json, logs/*, instances/*
* Primary sources (text): ~/MathDyad/erdos188/papers/tsaturian_1703.10723v2.txt, egmrss_1975_II.txt (Theorem 1′ around line 117),
  cmxz_2606.17194v2.txt (Section 3.1 = Theorem 1.2, the 6330 bound), conlon_fox_lines_1705.02166v4.txt, forum188.txt (live forum).

What to attack, in order:
1. The WLOG reductions W1 and W2 in README §1a. Is the unit clause "origin red" sound? Is "(5,0) blue" sound given only ONE
   rotation freedom is used, and is it used consistently (the certificate's other points are NOT assumed anything)? Does the
   argument really prove E² → (ℓ₂, ℓ₅) for ALL colourings of the plane (not just lattice colourings)? Check that every
   constraint in the core is a true constraint on an arbitrary plane colouring: a unit pair forbids red-red; a unit-spaced
   collinear 5-run forbids all-blue. Check the orientation of θ_d (does ±θ_d matter? both signs are sound; is the exact
   value cos θ_d = 1 − 1/(2d²) right for "a point at distance d moves by exactly 1"?).
2. verify_core.py: does it actually verify what the README says (exact reconstruction, exact distance 1, exact collinearity,
   second solver, minimality, negative control)? Look for a check that cannot fail. Run it on both cores.
3. The CMXZ audit (README §1b and cmxz_audit.py): is each recomputed constant actually the paper's? In particular
   |z(D)| = 18, the Janson form P(X=0) ≤ exp(−μ + Δe^{2δ}) and how Δ, δ are bounded (3 pairs per index with 2 ≤ |i−j| ≤ 4;
   E[X_i X_{i+1}] = 0), the 6329 vs 6330 crossover.
4. The REMARK k₁₈₈ ≤ 4920: is the degree-3/3-variable Milnor–Thom reparametrisation legitimate? (t = tan(θ/2) misses θ = π;
   does that lose any admissible collection the union bound needs? are the polynomials really of degree ≤ 3 in (x₁, y₁, t) after
   clearing the (1+t²) denominator — write one out; is Theorem 2.5's form (50DM/N)^N applicable with D = 3, N = 3, M = 100m² and
   M ≥ N?) Recompute the crossover yourself.
5. Statements about the literature: Conlon–Fox gives 2.15·10⁹ for n = 2 (check with their Theorem 1.1: R = m, |K| = m >
   10⁸ log₂ m); Tsaturian's Lemma 2.2 typo (√3 vs 3 — forum says side length 3); "θ₃ never used" in our 111-point core (check
   cores/ts_c3_k5.core.describe.json); the claim that the core lives in ℚ(√−3, √11).
6. Anything in README §3 that overclaims (it is meant to be a plan, not a result).
Do NOT rewrite the README. Report only.
