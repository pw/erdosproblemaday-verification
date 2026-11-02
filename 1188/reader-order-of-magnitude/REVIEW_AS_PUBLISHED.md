**Verdict: VERIFIED.** log F(x) = Θ(x log x), so F(x) = x^{Θ(x)}, with the explicit bounds as stated. Reviewed 2 November 2026; the k(36) line was updated the same morning, when the last table runs finished. As the submission says, the constant is open: whether log F(x)/(x log x) converges is the preprint's Question 6.7. Its liminf is at least 0.0672 and its limsup at most 1 − log 2 ≈ 0.3069.

**The claim.** F(x) counts the minimal distinct covering systems with every modulus in [2, x], as erdosproblems.com/1188 defines F. Systems with the same moduli and different residues count separately. The preprint is Zenodo 10.5281/zenodo.23427851 (16 October 2026, 34 pp.; SHA-256 64039de9…5fe69d0d). It proves:

- (c₁ + o(1)) x log x ≤ log F(x) ≤ (1 − log 2) x log x + 1.5x, with c₁ = 0.0672 and the upper bound for every x ≥ 2;
- log F(x) ≥ x/2 − 3x/log x for every x ≥ 40, by an elementary construction.

Until now the bounds in print were exp((log x)^{3−o(1)}) ≤ F(x) ≤ exp(O(x log x)). Colin Snyder's July Lean claim, log F(x) ≥ x^{1−o(1)}, is discussed below.

**What we checked.** We used our own code throughout and ran none of the submitter's. The "verification supplement" in Section 8 is not in the Zenodo record, so the paper's exact certificates could not be run. Where they matter, we replaced them with our own computations.

The seats, all AI:

- Two referee seats with tools each took half of Sections 2–7 and were briefed to refute them.
- A third recomputed the Section 8 tables.
- A fourth searched the literature.
- The host model, also an AI, read the central constructions itself.

*Upper bound.*

- The local lemma (Thm 1.3) holds. In a minimal system, for every prime p dividing some modulus, the classes with p | n project onto all of ℤ/p^e, where p^e is the largest power of p dividing a modulus.
- So at least p classes have moduli divisible by p. With distinct moduli at most x, every modulus is therefore √x-smooth (Cor 1.4), and Theorem 1.5 bounds F(x) by the product of n + 1 over the √x-smooth n ≤ x.
- We checked the paper's explicit bound on the log of that product for every integer x from 2 to 10⁸ (the paper needs it up to 81,796). There are no violations. The largest excess over (1 − log 2) x log x is 0.5418x, at x = 50, against the allowance of 1.5x.
- 3,200 random certified-minimal coverings, most with repeated moduli, satisfy the local lemma at every prime. A non-minimal system breaks it.

*Explicit lower bound.*

- Construction 3.1 is correct. It covers, its moduli are distinct (read off from the largest prime-power component), and every class has a private integer.
- Different permutations give different systems, so F(x) ≥ ∏_{p<P}(p−1)!, where P is the largest prime with P(P+3) ≤ x.
- We built the construction literally and checked it exactly over ℤ/L. All 96 data at P = 5 and all 69,120 at P = 7 give valid systems, pairwise different.
- We checked log ∏_{p<P}(p−1)! ≥ x/2 − 3x/log x at the right end of every step up to x ≈ 10¹⁶, plus every integer up to 10⁷. The paper needs a numerical check only for e⁶ ≤ x < e²⁰. There are no violations. The tightest point is just below x = 928, where the margin is 0.06x.

*Order of magnitude.*

- The split construction (Construction 4.2, Prop 4.3) is correct. Covering works by walking the splitting tree with z mod c, and a leaf's private integer is excluded from its siblings by their last common node.
- Proposition 4.7 alone, with single splitters in (x^{1/5}, x^{1/4}], gives log F(x) ≥ (0.01267 + o(1)) x log x by an elementary argument. That is already enough for Θ(x log x).
- Exact checks over a full period pass on Examples 4.4 and 4.5, rebuilt from the construction rules (all 6,720 paddings of 4.4 are valid and pairwise different), and on 48 random instances with trees to depth 3, with periods up to 12,252,240.
- On two large instances (46,984 and 78,654 classes), the moduli are distinct and at most x, and every private integer lies in exactly its own class. Covering there was tested on 109,702 and 709,981 chosen points, not over a full period.
- Negative controls fail, as they must: a deleted leaf, a repeated padding, and a bad τ.

*The constant 0.0672.*

- Theorem 4.8's splitting trees and Dickman-ρ integrals hold as read.
- We computed ρ two independent ways, checked against ρ(2) = 1 − log 2 and ρ(3). The paper's C₁(0.225) ≈ 0.0672193558 and C₂(0.2175) ≈ 0.2128758404 agree with ours to every printed digit.
- Our own lower Riemann sums give C₁(0.225) > 0.0672 and C₂(0.2175) > 0.2128. They are in high-precision floating point, not the paper's exact integer arithmetic. A coarser mesh, run as a control, correctly fails to certify.
- Table 4 (through 10¹⁴) reproduces, as do the seven (C₁, C₂) rows of Table 5 and the values quoted in Section 8.5's text. We did not recompute Table 5's finite-x columns.
- Section 6 (the anchor lemma, Thm 1.8, Cor 1.9) checks line by line.

*Exact values.*

- F(x) = 0 for x ≤ 11, 24 for 12 ≤ x ≤ 23, and 216 at x = 24 reproduce exactly. Four implementations agree, including a plain enumeration of all 3,968,055,000 assignments at x = 24.
- The paper's five moduli sets at x = 24 come out with the same 24/48/48/48/48 split.
- A search over all moduli, without the √x-smoothness pruning, agrees for x ≤ 13. So Corollary 1.4 is not doing the work there.
- k(12) = 5, k(24) = 6 and k(30) = 10 reproduce, each with an explicit system and a proof that one more class is impossible. At x = 30 that proof holds under two different solvers.
- k(36) = 14 reproduces with CP-SAT only, the paper's own solver family, under our own model and symmetry breaking. The symmetry breaking was controlled: it still finds every known witness, and it confirms the x = 30 bound.
- For k(40) = 15 and k(48) = 18 we reproduced the lower bounds (found systems, and the paper's printed 18-class system), but not the optimality.
- Tables 2, 3 and 7 and the 14-class system on the divisors of 216 match.

**Notes for a revision.** None of these affects a theorem.

- Credit Colin Snyder's claim, formalized in Lean by his account (we have not built it), that log log F(x)/log x → 1. It has been on the #1188 proof-claims tab since 15 July 2026, and Formal Conjectures marks the problem "research solved" on that statement. Your Corollary 1.6 gives an independent, elementary and explicit proof of it. So the sentence after Theorem 1.2, "This improves the lower bound log F(x) ≥ (log x)^{3−o(1)}", should also say that it improves Snyder's log F(x) ≥ x^{1−o(1)}.
- Theorem 1.3's counting inequality is already in Jenkin and Simpson (Integers 3, 2003, A13), your reference [17]: it is the case j = 1 of Lemma 7 and its proof, by the same CRT argument. There it is stated for sets of distinct moduli and phrased as removability.
- Corollary 1.4 follows from the case a = 1 of Krukenberg's lemma, Corollary 8 in Dalton and Trifonov (your [7]), which gives the slightly sharper P⁺(n)(P⁺(n)+1) ≤ x.
- c₁ = 0.0672 comes with no explicit x₀, since Theorem 4.8 is a limit statement. Section 8.4 shows that at every tabulated x up to 10¹⁶, the Section 4.1 split construction still gives less than Λ(x) ≈ x/2. The abstract should say that the only explicit lower bound is x/2 − 3x/log x.
- The submission's "Erdős expected F(x) to grow very slowly", repeated from the problem page, is not what Er80 says. On p. 95, "very slowly" refers to j_x, the largest number of covering systems whose moduli are all distinct and less than x, even across systems.
- The introduction's "irreducible covering systems with largest modulus x" should read "with all moduli at most x".
- The abstract's local-lemma sentence needs "every prime p dividing some modulus".
- Construction 4.2's data need not exist for every (P, I): P = 13 with I = {5, 7, 11} fails. Proposition 4.3 is correctly conditional on them.
- Section 8.6's "for 30 ≤ x ≤ 48 the solver proved optimality" should say "at the tabulated x": Table 6 gives k at 30, 36, 40 and 48 only.

**Context.**

- Snyder's Lean, as we read it (unbuilt), gives log F(x) ≥ c·x/(log x)⁴. The constant c is so small that the bound is trivial until x is astronomically large, and its upper bound is the trivial one.
- So the order of magnitude log F(x) ≍ x log x is new as far as our searches of arXiv, the forum, GitHub and the Formal Conjectures history reach. So are the explicit x/2 bound, the constant 1 − log 2 and k(x) ≍ x. These are searches, not a proof of absence.
- The paper's exact counts agree with Agrawal et al. (Integers 24A, 2024) on {2, 3, 4, 6, 12}, and with chenhaoyu's five irreducible moduli sets on the #1188 thread.

**What "verified" means here.** Two AI seats read every proof in Sections 2–7, each briefed to refute. The numbers above were recomputed with our own code, the Dickman constants in floating point. No human has refereed it, and nothing here is in Lean. The verification files are at github.com/pw/erdosproblemaday-verification/tree/main/1188/reader-order-of-magnitude.
