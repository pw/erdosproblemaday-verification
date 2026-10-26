# Seat R1 — hostile referee of the whole paper (read COMMON.md first)

Scope: all of §§1–6 (9 pages). Read every lemma line by line from the TeX. You are refereeing the PAPER's argument as written; the
Lean exists, but a gap in the paper that the Lean closes some other way is still a finding about the paper (say so in one sentence
and, if you looked, where the Lean does it — `grep -rl` the Lean dir by a key word; file names track the paper's vocabulary).

Load-bearing places to attack (not exhaustive — find others):
- Lemma 2 / (2.3)–(2.4): the Hadamard/logarithmic-derivative inequality, its constants for both parities, the passage to (2.2)
  (Mertens, primes dividing q, primes ≤ H). Is anything non-uniform in q?
- Lemma 3 (the interpolation/zero estimate) and its proof: the dimension count, the nearest-point argument (existence of the
  minimiser, the face G, Carathéodory/"one coefficient ≥ 1/4", y − u ∈ 3P, the strict decrease (3.5)), the hyperplane H with
  r·c ≠ 0, the Lagrange polynomial Q and its separate degrees. Zero estimates are where transcendence proofs usually break. Try to
  build a counterexample (an A satisfying the hypotheses, and t satisfying (3.1), where evaluation is NOT surjective), or explain
  why none can exist.
- Corollary 4's arithmetic; §4's greedy weighted selection (well-defined? all retained weights ≤ 96H^{2/3}U?), Lemma 6's counting.
- Lemma 7: the Frobenius congruence (5.2) (Euler's criterion in Z[a,b]/pZ[a,b]; which primes; d vs D=4d), the replacement rows
  (5.4), the claim that the matrix of replacement rows is L × (retained rows) with L unit lower-triangular over K, and the closing
  remark that "no integrality of L is required". Is Δ ∈ p^{E_p} R really proved?
- (5.1) Hadamard/Archimedean bound (|ν(θ_n)| ≤ 8N√q for both signs of d); (5.6)–(5.7); the master inequality (6.2) and the ORDER
  of parameter choices (H, then γ, then q → ∞): does any "absolute" constant secretly depend on H, γ, the field, or d?
- §6's reduction to a sequence with q → ∞, δ → 0 (finitely many characters of bounded conductor; zeros not accumulating at 1), and
  the excluded field Q(√2).
- SANITY TEST (do at least one): an argument that excludes Siegel zeros must not also "prove" something false. Design a test —
  e.g. ask what the same determinant argument would prove about primes with a different Frobenius class, or for a different set
  of primes, and compare with what Chebotarev/PNT says is true. Report what the test shows, whichever way it goes.

Numerics are welcome (small cases, exact arithmetic) but a separate seat is doing the heavy computations; keep yours to quick checks.
Report: /tmp/oaimath/003/seats/R1_report.md ; scratch: /tmp/oaimath/003/seats/R1_work/
