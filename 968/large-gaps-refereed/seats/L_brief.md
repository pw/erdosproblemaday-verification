# Seat L — OpenAI's Lean versus the paper.
Read COMMON.md first. The Lean is being kernel-replayed separately by the coordinator (results land in
/tmp/oaimath/026/lean-build/steps.tsv, statement_match.txt, logs/ax.log); you do NOT need to build anything. Your scope:
1. Map the paper's chain to Lean files/theorems: Theorem 1.1 (OAI.LargePrimeGaps.main in Main.lean), Corollary 1.2
   (RatioCorollary.lean / RatioDensity.lean), the weight proposition, the cancellation construction, the moment proposition, the
   mixed-moment proposition, the BV lemma, the singular-series average. A table: paper item → Lean name(s) → file:line.
2. The paper ASSUMES Bombieri–Vinogradov. The Lean appears to PROVE it: `bombieriVinogradov : BombieriVinogradov` from
   `siegelWalfisz : SiegelWalfisz` (Main.lean), `bombieriVinogradov_of_siegelWalfisz` (LogParameters.lean). Check that the Prop
   definitions `BombieriVinogradov` (MangoldtBounds.lean, with `endpointError`) and `SiegelWalfisz` (ConductorBounds.lean) are faithful
   to the standard theorems (ranges, max over residues coprime to q, ψ vs θ, primitive characters only?, conductor ≤ (log x)^B), and
   find where Siegel's theorem / the exceptional zero is handled (SiegelBounds.lean? ZeroFreeBounds.lean?) and where the large sieve
   is (AdditiveSieve / MultiplicativeSieve). Is anything there a hypothesis carried in a structure, a vacuous definition, or a
   `decide` on something nontrivial? (Source grep found 0 axiom/sorry/native_decide/set_option, 6 `decide`, 2 `Classical.`.)
3. Route differences: does the Lean use the same construction (τ = 1/8? alternating levels near k? r = ⌊√k⌋? the same profile g?) or a
   different one? Note any place the Lean proves something weaker/stronger/different from the paper.
4. Definitions in the comparator (ComparatorChallenges/PrimeGaps.lean): `prime`, `largeGapIndices`, `primeAt`, `initialCount`,
   `lowerAsymptoticDensity` (an sSup of eventually-valid lower bounds), `ratioIncreaseIndices`. Do they say what Theorem 1.1 and
   Corollary 1.2 say (1-based indexing, Nat.nth Nat.Prime (n−1), division by (n:ℝ) at n ≥ 1, strict inequalities)? Any degenerate way
   the statement could be true for a trivial reason?
5. Audit counts (lines, theorems) and anything odd (e.g. very long proofs, `maxRecDepth`, `simp` sets, `Classical.choice` uses).
Report as COMMON.md says. Cite file:line for everything.
