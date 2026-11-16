**Seat A report: Lecomte, arXiv:2611.15068v1, §§1–4 as printed (pp. 1–11)**

## Verdict: HOLDS WITH FIXES

I found no MUST-level objection. Every proof in §§1–4 survives a line-by-line read, every cited result I could reach says what the paper uses it for, and none of more than 100,000 checks that could have failed did. The fixes needed are wording and rigor only. One point for the site's verdict: h(n) = T(n), the answer to Erdős #117, does not depend on the companion preprint [13]. The identity h(n) = 1 + √ζ(n) and the claim "these also attain ζ(n)" do depend on it.

## Per-lemma table

| Item (page) | Status | Basis |
|---|---|---|
| §1: ω ≤ a ≤ z; a = max{1, χ(Γ_G)} (p.1) | HOLDS | read |
| §1: reduction to finite groups via Zarrin [22, Thm 1.1(2)] (p.3) | CITATION OK | arXiv:1412.4349 states it verbatim: "There exists a finite group K such that K is isoclinic to G and ω(G)=ω(K)". |
| §1: isoclinism preserves z, ω, a (p.3) | HOLDS, infinite groups included | A·Z(G) is abelian exactly when its image in G/Z is a subgroup with trivial commutator, and an isoclinism carries such subgroups to each other. a ≤ z is finite by Neumann. |
| §1: "clique number two never occurs"; facts about B and T (p.2–3) | HOLDS | read |
| Lemma 2.1 and the I·ω(gH) remark (p.3) | HOLDS | 59,585 fibre checks of width = [R : C_R(g)] |
| §2.1, eq. (2) (p.4) | HOLDS | read |
| Lemma 2.2(i), (iii), and the averaging step (p.4) | HOLDS | (i) needs G finite, which the reduction supplies |
| Lemma 2.2(ii) (p.4) | GAP in wording only | see S1 |
| C_p(k) remark (p.4) | HOLDS | read |
| Lemma 2.3 (p.4–5) | HOLDS | brute force |
| Lemma 2.4, all five claims (p.5) | HOLDS | brute force, below |
| Eq. (3), Tomkinson [20] (p.5) | CITATION OK, via secondary source | Journal returns 403. arXiv:2111.13658 states "Tomkinson [21] proved that f(k) = k!", which is the bound used. |
| Lemma 3.1 (p.5–6) | HOLDS | computed |
| Lemma 3.2, Cor. 3.3 (p.6) | HOLDS | read; examples computed |
| §3.1 sharp examples, incl. the q=3 / F₉ case with clique number 7 (p.6–7) | HOLDS; [12] CITATION OK | Klein–Metsch Thm 3.3: a maximal partial spread of Q(4,q) is a spread or has at most q²−q+1 lines. Their §6: W(3,q) has no ovoid for odd q. Clique number 7 also computed directly. |
| §4.1, scalar radical R ⊇ P′P^pZ(P) (p.7) | HOLDS | read |
| Lemma 4.2 (p.8) | HOLDS | 4,068 instances, a = ω in every one |
| §4.2 averaging and eq. (4) (p.8) | HOLDS | 10,359 averaging checks and 6,433 checks of (4) |
| Lemma 4.3 (p.8) | HOLDS | printed recipe checked on every hyperplane |
| Lemma 4.4 (p.8–9) | HOLDS | see S3; exhaustive tests |
| Lemma 4.5(1) and (2) (p.9) | HOLDS | 4,387 instances of (1); 3,926 of (2); 13,013 per-fibre width checks |
| §4.3, abelian noncentral radical (p.9) | HOLDS | arithmetic checked |
| §4.3, central radical, one component, incl. Ceria et al. [4, Thm 3.7] (p.9–10) | HOLDS; CITATION OK | Ceria et al. Thm 3.7 is verbatim in arXiv:2203.04553. The 13-point clique and the identity Tr(x/y − y/x) = Nm(1 − y/x) recomputed in F₂₇. |
| Lemma 4.6 (p.10) | HOLDS | printed recipe checked on random pencils; 1,835 group instances |
| §4.3, j = 2, several components, citing [10, Lemma 3] (p.10) | HOLDS; citation unreachable | see N2 |
| §4.3, nonabelian radical (p.11) | HOLDS | every inequality checked in exact arithmetic |
| Prop 4.1 (p.7) | odd p: HOLDS | The p = 2 part and the assembly of Sylow factors are in §5 / §5.4, Seat B's scope. |

## Objections, ranked

**MUST:** none.

**SHOULD**
1. **Lemma 2.2(ii), p.4.** It says "If every point of X_i ⊆ Q fails to commute with every point of X_j ⊆ Q". In every application Q = P/R is elementary abelian, so taken literally the hypothesis never holds. What the proofs actually use is that all *lifts* fail to commute, which the scalar form certifies. This happens in Lemma 4.5 ("Summing the widths over a clique"), in §4.2, and in §5.1. The printed proof works unchanged for the lifts version. Restate (ii) in terms of lifts.
2. **p.10.** "For p ≥ 5 and j ≥ 3, … Since j ≥ 2 and p ≥ 5, p²(j−1) ≥ 2pj". The two ranges contradict each other. Harmless, because j = 2 is handled separately and also satisfies the inequality.
3. **Lemma 4.4, p.8–9.** The proof is correct but terse at two load-bearing points:
   - B₁ is not intersected with M, so the final chain silently uses [M∩B₁ : D] ≤ [B₁ : D].
   - The induction is applied to the restricted subcover on B_j y after translating it.

   This deserves a fuller write-up or a citation if it is known. For general groups Tomkinson's k! is sharp (arXiv:2111.13658), so a p^{t−1} bound for p-groups is a real statement. My exhaustive tests support it, and the bound is attained.

**NOTE**
1. The identity h(n) = 1 + √ζ(n) and the claim about maximizers of ζ rest on [13], the author's own preprint (arXiv:2611.00943, posted 31 Oct 2026, not refereed). I checked that its Theorems 1.1 and 1.2(v) state the values the paper uses.
2. [10, Lemma 3] (Gow–Quinlan, LMA 2006) returns 403, so I could not see what it says. The fact actually needed is that a space of 4×4 alternating forms over a finite field whose nonzero members are all nondegenerate has dimension ≤ 2. That is standard (Chevalley–Warning applied to the Pfaffian quadratic form). Give the argument inline. My own exhaustive computation of this was too slow and I killed it, so this rests on the theorem, not on a computation.
3. Not checked, because the sources are paywalled: the attributions to Chin [5] and to Isaacs via Bertram [3, p.40]. They are not load-bearing, since the paper includes proofs. The abstract's "confirming Pyber's prediction" is never cited or quoted in the text.
4. Zarrin's own proof of his Thm 1.1(2) cites Pyber for "centre-by-finite" in arbitrary groups. Neumann [15] is the right source. This does not affect the paper.

## What I tested that could have failed

Scripts are in `~/MathDyad/subs-1116/117/seatA/` and logs in `seatA/logs/`. The two cadical jobs were never touched, and every scratch process was killed by its own PID.

**Checker controls.** The exact solver for (ω, a), CP-SAT over the maximal abelian subgroups, reproduces known values:

| Group | (ω, a) |
|---|---|
| S₃ | (4, 4) |
| A₄ | (5, 5) |
| D₈ | (3, 3) |
| UT₃(F₄) | (5, 5) |
| 3^{1+4}, both exponents | (7, 10) |
| 2^{1+6} | (7, 9) |

Negative controls: a deliberately wrong profile T′(n) = n is flagged, and each lemma predicate (4.2, 4.5a, 4.5b, 4.5 widths, 4.6, the average, eq. (4), 2.1) fires when its data is mutated.

**Symplectic geometry (`symp.py`)**
- Clique number of W(3,3) is 7, proven optimal; a clique of size 8 is infeasible. Plane controls give p+1 for p = 2, 3, 5, 7.
- For p = 2, the maximum clique is 2r+1 for r ≤ 4. All 288 maximum cliques at r = 3 span V and sum to zero.
- Lemma 4.3's recipe works on every hyperplane for (p, r) ∈ {(2,1), (2,2), (2,3), (3,1), (3,2), (5,1), (5,2)}.
- The 13-point Ceria set in F₂₇² is a clique, and the trace form has rank 6.
- Lemma 4.6's recipe produces p²(r−1)+1 points on random pencils for p = 2, 3, 5.
- Side fact: the clique number of W(3,5) is 18, below Tallini's 21. The paper does not need this.

**Lemma 2.4 and eq. (3) (`lemma24.g`).** Every subgroup U, every coset gU and every maximum clique X, in all nonabelian groups of order 6, 8, 12, 16, 18, 24, 27, plus 30 of the groups of order 32 (stopped for time):
- 0 failures over 2,319 cosets and 21,103 maximum cliques through order 27.
- Negative controls fire: a width bound of p+2 fails in 4 cosets, the wrong formula U∩C(X) = Z(U) fails in 384 cliques, and (w−1)! in place of w! fails in 79 cosets.

**Lemma 4.4 (`lemma44.py`).** Exhaustive search over every t at which a violation is possible (t ≤ log_p|U|):
- Covered: all groups of order 8, 9, 16, 25, 27, 81, 125, and C₃₂. The remaining order-32 groups were stopped for time.
- 0 violations. 216,523 irredundant covers of C₂⁴ alone.
- The bound is attained (order 16, t = 4, index 8; C₃₂, t = 5, index 16), so the check could have gone red.

**p-group survey (`survey.g` + `analyze.py`)**
- Exact (ω, a) and every scalar commutator form for all 3,261 groups of order 16, 32, 64, 128, 81, 243, 729 and 625.
- 0 violations of a ≤ T(ω), 0 cases with a ≥ T(ω) at ω ≥ 9, and 0 lemma-prediction failures (counts in the table above).
- The only groups with ω = 7 and a = 10 are those isoclinic to 3^{1+4}.
- The SmallGroups data for 5⁵ and 7⁴ is not installed here, which is why `class2.py` covers those primes.

**Class-2 models beyond the library (`class2.py`).** 43 random alternating maps over F₃ (dimension 4–6), F₅ and F₇ (dimension 4), and F₂ (dimension 6–8). The run was stopped during the dimension-6 cases.
- No violations. My "ANISO-CLAIM-FAILS" flag fired on the two one-form cases, but that was a filter bug on my side: those are 3^{1+4}, with ω = 7, a = 10 = T(7) as the paper says.
- Every anisotropic pencil gave a = ω = p²+1: 10 for p = 3, 26 for p = 5, exactly as §4.3 claims.

**Arithmetic (`arith.py`).** Every §4.3 inequality chain was checked in exact rationals for p ≤ 13, j ≤ 8, m ≤ 30, including the special p = 3, j = 1 split. 0 failures; weakening the thresholds produces 43 failures.

**Global sanity check outside my scope.** All 3,826 nonabelian groups of the remaining orders ≤ 255 (nonnilpotent included): 0 violations. The maximum a for each ω from 3 to 6 equals T(ω). For ω = 7 and 8 the maximum a is 7 and 8, both below 10.