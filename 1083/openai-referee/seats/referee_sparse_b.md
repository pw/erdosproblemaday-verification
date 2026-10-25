# Referee report: sparse_b, §6.3–6.5 and the proof of Theorem 6.1 (PDF pp. 51–61)

Paper: /tmp/oaimath/166/paper.pdf (sha256 37f6355365a18510e75d897dc9ab6d29305d7ff132cf148845b6f16d080ee1bf).
Scope: Prop 6.5 (projection depth, separated windows), Remark 6.6, §6.4 (Lemma 6.7 and the rank contradiction), §6.5 (final curve plateau for narrower centres), and the proof of Theorem 6.1 (p. 61).

What I read for context: §1.2–1.3 and §2 (pp. 2–13); §3 (pp. 14–26), reading the proofs of Lemmas 3.8, 3.10, 3.11, 3.12(i), and Cor. 3.13 and 3.14 closely, and Lemmas 3.3 and 3.6 at medium depth; §4 (pp. 27–33); §5 (pp. 33–42); §6 preamble, §6.1 and §6.2 (pp. 42–51).

I checked every displayed formula in my scope against the rendered PDF (pp. 51–61), not only against the text extraction. On p. 41 the extraction reads "D_{d−1} exp(o(s))", but the PDF has D_d^{−1} exp(o(s)), which is correct. That is an extraction artifact, not an error in the paper.

## Verdict for my scope

**HOLDS AS READ.** I found no mathematical gap and no hidden rate on δ in pp. 51–61. Every objection below is exposition (COSMETIC or UNCLEAR). The verdict depends on upstream results owned by other referees. These are the places where my scope could still fail:

- **Prop 5.1(3) and Prop 5.3.** I rely on their no-capture and individual-cut conclusions, including uniformity over all cuts of degree O(T_s(b)) and over sequences of pieces. They are used on every plateau of dimension ≥ 2 in Lemma 6.7, and for the centre piece in (6.16). (§5 referee.)
- **Lemma 4.2.** Its generic list bound is the only secant input to (6.16). (Secants referee.)
- **Prop 4.3.** I checked only that the objects it deletes are the objects §6.5 produces. Its o(N²) count is the secants referee's.
- **Prop 5.5.** The selection must exhaust the cases and must deliver a covered ordered product of fixed positive density α in one orientation. (Secants / sparse_a referees.)
- **Lemma 3.3 and Lemma 3.6.** Interpolation degree C·L independent of the number of points, and the lower bound (3.7). These are the engine of every Hilbert lower bound used here. (Algebra referee.)

### Brief items, one by one

**No rate on δ.** In my scope δ enters in exactly three places, and each needs only δ = O(1):
- §6.4 end: the ratio is ≥ δ^{−1} e^{cs/3}.
- §6.5, the h ≥ 2 exclusion: it reduces to e^{(c−O(ξ))s} ≲ δ (Objection 6).
- §6.5, the exceptional family: the ratio is O(δ e^{−(η−ε)s}).

So the separated-window case does not even use δ → 0. Inside §6, δ → 0 is needed only through Prop 4.3/5.5 and §6.1–6.2. The paper's warning on p. 61 ("One must not instead compare (N/A)exp(−o(s)) directly with δN/A") correctly identifies the one comparison that would need a rate. The argument avoids it by using the strict gap η − ε from Lemma 3.8 at degree T1 = T0·e^{ηs}.

**Where the zero margin sits.** It is (6.26), second entry, −Σ_{i>j+1} b_i, at j = d−1, where the sum is empty and equals 0. Equivalently R·D_d = A with R = B·exp(−b_d s). I checked the case analysis of Lemma 6.7 exhaustively (see Numerics). Every plateau with b_j < b_{j+1}, in either orientation, has a strict margin except the narrower-centre final one-dimensional plateau. That is exactly the case §6.5 treats.

**Either endpoint.** Inside my scope the orientation is fixed: p ∈ Px is the covering centre. Both v/s → 0 and v/s → ∞ are treated: (6.15) plus §6.5 for narrower centres, and (6.16) for wider ones. So whichever factor Prop 5.5 makes the centre, the argument applies.

**Prop 4.3 objects.**
- Prop 4.3 deletes ordered pairs (p, q) with q assigned to Y_i and π_p Y_i ⊆ C_p (p. 30).
- Prop 5.5 applies it to the global assignment of every non-core point to "one of its carrier curves after the (d−1)st cut" (p. 41).
- §6.3 uses exactly that assignment on the final plateau: "On the final one-dimensional plateau use its carrier from the global terminal assignment."
- §6.5 concludes π_p Y = γ ⊂ C_p for that Y.

These are the same objects.

**Positive fraction and constants.** The separated-window contradictions hold for any fixed covered density α > 0. All constants depend only on d and the limiting profile (b_i) (see the constant table). Dependence on the limiting profile is dependence on the (sub)sequence. That is legitimate, because Theorem 6.1 is a non-existence statement along one sequence. Prop 2.2 applies it to one diagonal sequence, and no uniformity over sequences is claimed or needed.

## Objections

**1. Narrower-centre isolation degree is asserted, not derived (§6.3, p. 53).**
- Quote: "The center piece can be simultaneously isolated as zero-dimensional components of equations of degree L = B exp(o(s)), |Px| = N exp(o(s)), where the second error is signed."
- Problem: no justification is given. The claim is true. Prop 5.1(2)–(3) gives the piece's own d proper cuts of degree ≤ D_i^{(x)}·exp(o(v)) ≤ B·exp((1+o(1))v), and the local dimension is 0 "automatic after the last cut". Since v = o(s), this gives L = B·exp(o(s)).
- Severity: COSMETIC, exposition. Fix: cite Prop 5.1(2)–(3).

**2. Isolatedness in the (6.20) count assumes non-dropping incidences (§6.3, p. 53).**
- Quote: "The generic ray has finite intersection with that component, so the fiber is locally finite. Thus the solution is isolated on the variety parametrized by (z, t)."
- Problem: this needs (p, Y′) not to be dimension-dropping. If Y contains the line through p and y, the roots on that line form a positive-dimensional set. Isolated Bézout does not count them, so the per-centre identity "number = depth − 1" fails at such centres.
- Why harmless: those incidences were already deleted ("Projection from p can drop the dimension of Y only if its generic fiber is a line…"). The Markov step needs the bound only at retained incidences.
- Severity: COSMETIC.

**3. First-cut bound: "path locus = unique first carrier" near a regular point is not argued (§6.3, p. 53).**
- Quote: "At an assigned regular point q the line would lie locally in its unique first carrier, so its direction would be tangent there."
- Problem: this needs the first path locus V(h_1, …, h_m) to coincide near q with the unique smooth first carrier W_q. That holds for the following reasons, none stated:
  - every component of the path locus through q passes through a piece point, so it is a carrier;
  - by Prop 5.1(3) each such component has the plateau's local dimension;
  - Prop 5.3's full-rank common equations then force all of them to equal W_q.
- If the first limiting cut time has multiplicity m ≥ 2, "the first plateau after a drop" has codimension m. All m cuts have degree ≤ D_1·exp(o(s)), so the bound R = D_1 is unchanged.
- Severity: UNCLEAR, exposition. True as written.

**4. Lemma 4.2's generic list bound is transferred to the generic point of an auxiliary curve (§6.3, (6.16), pp. 55–56).**
- Quotes: "choose an irreducible algebraic curve through p whose general point lies in the open set where the preceding generic properties, including the gcd degree, hold" and "The generic list bound permits at most q remaining distinct roots."
- Problem: Lemma 4.2 bounds generic map degrees over a general pair (x, y). The argument needs an open dense U ⊂ X, for the fixed y, on which the *actual* number of points of line(x, y) ∩ ⋃_{Z∈Y_X} Z \ {x} is ≤ q. Fibre cardinality is not semicontinuous in general, so a specific statement is needed: the root incidence over X×Y is generically finite, and étale over a dense open.
- Why it is true: generic finiteness holds because no l-dimensional listed target can contain line(x, y) for x in a dense subset of X. The cone from y over X has dimension k+1 > l, using k ≥ l, which itself comes from b_{j+1} > 0. Listed targets whose generic image differs from π_x Y contribute no roots over the general direction. The step is therefore correct.
- Consequence for distinguished roots: on targets whose image agrees with π_p Y only at the special centre p, distinguished roots are never in supp D_0. They count fully toward the rank deficit, which is exactly what the argument needs.
- Severity: UNCLEAR, exposition. True.

**5. Lemma 3.8 is applied in projective space (§6.5, p. 60).**
- Quote: "Lemma 3.8 gives equations of degree at most T1 vanishing on the whole family Fp, with generic full rank except on components of total degree O(ET0/T1)".
- Problem: Lemma 3.8 is stated in ℂ^n. F_p ⊂ P^{d−1} is pure one-dimensional, consisting of components of V_p = Env_{T0}(C_p), which is cut out by degree-T0 forms. The lower-bound hypotheses of Lemma 3.6 hold with L = T0. The projective version follows from the chart convention on p. 14 (a generic affine chart containing the finitely many labels and the generic points of the components). The paper accounts for the pullback ("proper rational test, with cleared numerator of degree O(T1)").
- Severity: COSMETIC.

**6. The h ≥ 2 exclusion cites (6.27), but the contradiction actually runs through the envelope bound (§6.5, pp. 59–60).**
- Quote: "The Hilbert bounds for the envelope group propagate this with exponent h ≥ 2, exactly the required exponent of σT on a one-dimensional plateau. At b0 sufficiently close to bd it contradicts (6.27)."
- The actual contradiction goes through H_{V_p}(T0) = H_{C_p}(T0) ≤ CE(T0+1) (stated just above). Explicit chain:
  1. The lower bound (Cor. 3.7) gives a_h ≤ C·E·T0^{1−h}.
  2. For S′ = covered targets with labels on the h-group: H_{π_p S′}(T′) ≤ C·a_h·(T′+1)^h ≤ C·E·T′²/T0.
  3. Lemma 6.7 at b′ ↑ b_{d−1}: H_{π_p S′}(T′) ≥ σ(b′)·T′·e^{cs}/A, with σ(b′) = e_{d−1}·T′·e^{O(ξs)}. This holds also when b_{d−2} = b_{d−1}, by continuity of σ.
  4. Combining: (T0/D_d)·e^{(c−O(ξ))s} ≲ δ. With b_d − b_0 < c/2 this is false for large s.
- I verified each step. The text compresses the chain into one sentence.
- Severity: COSMETIC.

**7. Order of choices in §6.5 (p. 59).**
- Quote: "Choose a fixed time b0 < bd sufficiently close to bd … Fix 0 < ε < η. Include this tolerance for the final plateau in the finite depth batch, and use the typical-center set for the combined batch. Its deletion is made before the envelopes below are chosen."
- Problem: b_0 depends on c (Lemma 6.7's margin); ε < η = b_eq − b_0 depends on b_0; and the typical-centre set on which Lemma 6.7 is re-run depends on ε. This looks circular but is not. The order is:
  1. profile margins (6.26);
  2. tolerances for the non-final plateaux;
  3. c;
  4. b_0, b_eq, b_test;
  5. η, then ε;
  6. the combined depth batch;
  7. the typical centres;
  8. the envelopes V_p.

  c does not depend on ε, because ε governs only the final plateau, where Lemma 6.7 is not used. The text says this only implicitly.
- Severity: UNCLEAR, exposition. No gap.

**8. "Uniformly in the center and the envelope" (Lemma 6.7, p. 58; §6.5, pp. 60–61).**
- Quotes: "The individual-cut conclusion of Proposition 5.3 therefore removes only o(|Py|) such targets, uniformly in the center and the envelope" and "…uniformly in p".
- This is inherited from Prop 5.1(3) ("Uniformly over polynomials of degree O(Ts(b))") through Prop 5.3's pooling (Lemma 3.9 plus (5.8)) and its sequence quantifier.
- On the final one-dimensional plateau it is elementary and independent of §5. A proper cut of degree T on the terminal curves captures ≤ e_{d−1}·e^{o(s)}·T = N·e^{(b−b_d)s+o(s)} = o(|Py|) points. So §6.5's three uses do not depend on §5's deep no-capture.
- Lemma 6.7 on plateaux of dimension ≥ 2, and (6.16) on the centre piece, *do* depend on it.
- Severity: COULD NOT CHECK in my scope, because the uniform no-capture is constructed in Prop 5.1's regularization. Statement-level match verified.

**9. The final §6.4 contradiction is stated without the row count (p. 59).**
- Quote: "This contradicts the positive density of covered rows."
- Implicit count: a covered product ≥ α|Px||Py| gives ≥ (α/2)|Px| rows with ≥ (α/2)|Py| covered targets. Typical centres are a 1 − o(1) fraction of Px, so some typical row is covered. Its covered remaining targets are a dense subset, so (6.25) applies at ρ = α/3. Then (6.25)/(6.27) ≥ δ^{−1}·e^{cs/3} → ∞.
- The (1+T)/T and constant factors are absorbed since σ(b)/N ≥ e^{−cs/2}.
- Severity: COSMETIC.

**10. The proof of Theorem 6.1 (p. 61) is a five-sentence summary.**
- Quote: "The profile-pair selection exhausts the possibilities. … For separated windows, strict row rank propagation contradicts coverage except on the final narrow-center curve plateau, which the preceding argument resolves by common regularity and terminal deletion."
- The case list matches Prop 5.5 (core / common window / separated windows / outermost pool). Theorem 6.1's hypotheses are verbatim Prop 5.5's hypotheses (curves spanning ≤ P², deg C_p ≤ δN/A, 1 − o(1) of pairs covered from either endpoint).
- The summary does not restate that each branch contradicts a fixed covered density α > 0 obtained after a subsequence, nor which constants are fixed where. For separated windows I verified this myself (constant table).
- Whether Prop 5.5 truly exhausts the cases is outside my scope.
- Severity: COSMETIC, exposition.

**Considered and dismissed (recorded so others need not re-check):**
- (6.16) "Because s = o(log B), we have q = o(r) and r = B^{1+o(1)}". Correct: q = B^{1/2}, r = ⌈B·e^{−2s}⌉ = B^{1−o(1)}.
- L²/r = B·e^{O(s)}. Correct: L ≤ B·e^{(2+o(1))s}, which gives ≤ B·e^{6s}. This is o(T_v(τ)) since s = o(v), so the compressed cut is a proper cut of admissible degree on the centre plateau.
- "If both forms vanish, S(p) = 0 and the rank decrease is ρ ≥ L ≥ r". Correct, because L ≥ B is chosen.
- The (6.15) exponent arithmetic e_j·B^{l+1}/N = B·exp(s·Σ_{i≤j} b_i) = B·exp(−s·Σ_{i>j} b_i). Correct. Prefix sums of a sorted zero-sum profile are ≤ 0, so R ≤ B.
- e_{d−1}/R = (N/D_d)/(B·e^{−b_d s}) = N/A on the narrow final plateau. Correct.
- (6.29): C·a·L/D with a = O(E), L = T0, D = T1, giving O(E·e^{−ηs}). Correct.

## Citation table (my scope)

| Cited result | What the paper claims it says | What the source says | Verdict |
|---|---|---|---|
| (none) | pp. 51–61 contain no bibliographic citation (grep for "[digit" finds only the binary-form parameter "[1 : 0]") | — | no external citation in scope |
| Fulton, Intersection Theory [14, Prop. 4.4, App. B.6], entering via Lemma 3.12(i) → (6.18) and the point-projection formula on p. 51 | degree formula for a linear system with base locus; t·deg Y = deg X − mult_p X | Book behind a paywall, no arXiv version. The paper gives its own blow-up proof on p. 24, which I checked: (H−E)^k = H^k + (−1)^k E^k, with E^k = (−1)^{k−1}·mult_p X, gives a − mult_p X. | COULD NOT FETCH; in-paper proof verified |

**Internal results my scope consumes, and their status:**
- **Verified at proof level:**
  - Lemma 3.8: the J-functional rank argument and the binomial ratio giving b ≤ C·a·L/D.
  - Lemma 3.10: the Frobenius decomposition, digit basis mod J_z, specialization.
  - Lemma 3.11.
  - Lemma 3.12(i).
  - Cor. 3.13: degree ≤ (n+1)·a/(⌊a/2⌋+1) ≤ 2(n+1).
  - (3.5) and Cor. 3.7 (statement).
- **Statement-level only:** Lemma 2.1 (flat cap), Lemma 3.3, Lemma 3.6 lower bound, Lemma 4.1, Lemma 4.2, Prop 4.3, Props 5.1–5.3, Prop 5.5.

## Constant-dependency table (my scope)

| Constant | Fixed where | Depends on | Used where | Claimed independent of |
|---|---|---|---|---|
| ε (Prop 6.5 tolerance; ε in §6.5) | Before the incidence deletions (p. 52); in §6.5, after b_0 (p. 59) | Profile margins (6.26) (non-final plateaux); η = b_eq − b_0 (final plateau) | (6.13), (6.21), §6.5 exceptional-mass comparison | N, δ, ρ, the subcollection. Checked. |
| η (Prop 6.5 internal slack) | In the proof, after ε | ε | (6.19), Markov in (6.15) | N, δ |
| α (deleted incidence mass) | Output of the deletions | Sequence (o(1)) | Row Markov √α (p. 53) | Choice of later subcollection. Checked. |
| ρ (density threshold) | After the typical-centre set | Arbitrary fixed > 0 | (6.13), Lemma 6.7, §6.5 | Deletions (only the large-index threshold depends on ρ). Checked. |
| c₀ (flat cap) | Lemma 2.1 | Absolute (1/2 works) | Dimension-drop and tangency deletions | Sequence |
| q = B^{1/2} | (6.16), p. 54 | Lemma 4.2 exponent 1/2 | Root count in the gcd specialization | δ |
| r = ⌈B·e^{−2s}⌉ | p. 55 | B, s | Depth cutoff, compression degree | δ; needs only s = o(log B) |
| L₀, L = B·e^{O(s)}, L ≥ B | p. 55 | Target cut degrees D_i·e^{o(s)} | Sylvester size, Q-minor degree ≤ 2L² | δ |
| C in B·e^{Cs} (C ≤ 6 suffices) | p. 54 | d | Centre no-capture (needs s = o(v)) | Sequence |
| τ (centre testing time) | p. 54 | Profile (0 < τ < min{b_i > 0}) | Admissibility of degree B·e^{O(s)} on the centre plateau | Sequence |
| L (narrow centre isolation) = B·e^{O(v)} | p. 53 | Centre path | (6.20) | — (= B·e^{o(s)} since v = o(s)) |
| R (three choices (6.14)–(6.16)) | p. 52 | Profile, s, B | (6.21), (6.26) | δ |
| c (Lemma 6.7 margin) | Lemma 6.7 | Profile margins (6.26), tolerances; decreased finitely often | §6.4 end, §6.5 h ≥ 2 exclusion | δ, N, ε of the final plateau. Checked, no cycle (Obj. 7). |
| b₀ < b_eq < b_test | p. 59 | c, profile | T₀, T₁ | δ |
| T₀ = T_s(b₀), T₁ = T₀·e^{ηs} | p. 59 | b₀, η | V_p, Lemma 3.8 | — |
| Hilbert / Bézout constants c_n, C_n | §3 | Dimension only | Everywhere | Sequence |
| E = δN/A | Hypothesis | δ (no rate) | (6.27), (6.28), (6.29) | Used only with δ = O(1) in my scope |

## Steps verified line by line vs skimmed

**Verified line by line:**
- Prop 6.5 bookkeeping: (6.17), (6.18), (6.19), and the √α row-Markov uniformity mechanism.
- Dimension-drop deletion (flat cap) and the multiplicity deletion (Cor. 3.13 plus bounded-degree centre no-capture; the inherited lower boundary B·e^{−v} is above any bounded degree).
- First-cut bound (6.14); see Obj. 3.
- Narrower bound (6.15): parametrization, degree 2L pullback, isolatedness (Obj. 2), Bézout (6.20), division by |Px|, exponent identity, Markov.
- Wider bound (6.16) in full:
  - Lemma 4.2 hypotheses for k = l: flat counts and weights B^{±(d−l)+o(1)}, n_x, n_y ≥ N·e^{−o(log B)};
  - choice of y;
  - base-locus homogenization;
  - line parametrization [U : Uy + V(x−y)];
  - gcd over ℂ(X) and constant generic combinations;
  - Sylvester rank ρ = 2L − g (numerically checked);
  - curve through p avoiding the bad set;
  - DVR/content specialization of the gcd;
  - ≤ q distinguished roots in supp D₀ (Obj. 4);
  - rank deficit ≥ r/2, including the one-zero and both-zero cases;
  - Lemma 3.11 order ≥ ⌈r/2⌉;
  - Lemma 3.10 degree O(L²/r);
  - properness and admissibility on the centre plateau;
  - uniformity in Y.
- Remark 6.6.
- Lemma 6.7:
  - initial interval (A/T² = e^{−2bs});
  - envelope containment via pulled-back proper cuts;
  - grouping;
  - h > l propagation, including continuity of σ across simultaneous cuts;
  - h = l via (6.21);
  - (6.26) arithmetic and the exhaustive case analysis.
- (6.27) and the §6.4 contradiction (Obj. 9).
- §6.5 in full:
  - order of choices (Obj. 7);
  - h ≥ 2 exclusion (Obj. 6);
  - (6.28);
  - placement of the projected terminal curve in F_p;
  - Lemma 3.8 exceptional bound (6.29) versus depth bound (N/A)·e^{−εs};
  - pullback of g_p and removal at b_test;
  - identification γ = π_p Y at a full-rank label;
  - the match with Prop 4.3/5.5's deleted incidences.
- Proof of Theorem 6.1: case list against Prop 5.5's alternatives.

**Skimmed or statement-level only:**
- Lemma 4.2's proof: the Szemerédi–Trotter slice for flats in common (k+1)-flats.
- Lemma 4.1's proof.
- Prop 4.3's proof: lines, d ≥ 4 stabilizer argument, d = 3 polar/Hölder.
- Prop 5.1's regularization and its uniform no-capture.
- Prop 5.3's pooling.
- Prop 5.5's selection and its proof that the cases are exhaustive.
- Lemma 3.3 and the lower bound of Lemma 3.6.
- §6.1–6.2 (sparse_a scope).

## Numerics (python at nice 19; scripts in /tmp/sb_scripts/)

- **sylv.py.** 300 random pairs of binary forms of degree L ≤ 5, with planted common factors including roots at [0:1] and occasional zero forms. Rank of the 2L-square Sylvester map (a, b) ↦ aF + bG equals 2L − deg gcd (L if exactly one form is 0, and 0 if both are): 0 mismatches. Negative control with a deliberately wrong formula: 146 mismatches, so the check can fail.
- **margins.py.** All limiting profiles on a 1/8-grid for d = 3…7 satisfying (5.7) and max|b_i| ≥ 1/2: 43,670 (plateau, orientation) cases. The best available depth choice in (6.26) (R = D₁ always; (6.15) narrower; (6.16) wider with b_{j+1} > 0 and l < d−1) gives a strictly negative normalized log of R·D_{j+1}/A in every case except narrower centres on the final one-dimensional plateau (2,751 such cases, where the second entry is exactly 0). That is exactly Lemma 6.7's exception and §6.5's case. Negative control with the narrower choice removed: 862 violations.

## Summary

In §6.3–6.5 and the proof of Theorem 6.1 (pp. 51–61), I found no false sentence, no hidden rate on δ, and no cycle among the constants. Every objection is exposition (COSMETIC or UNCLEAR): an unjustified-but-true isolation degree (Obj. 1), tacit restrictions to non-dropping incidences (Obj. 2), unstated local identification of the path locus (Obj. 3), the transfer of Lemma 4.2's generic bound to a curve's generic point (Obj. 4), Lemma 3.8 used projectively (Obj. 5), a compressed contradiction chain (Obj. 6), an implicit order of choices (Obj. 7), and a summary-only proof of Theorem 6.1 (Obj. 10).

The scope's correctness is conditional on: Prop 5.1(3)/5.3's uniform no-capture (the §6.5 uses are elementary, but Lemma 6.7 on plateaux of dimension ≥ 2 and (6.16) are not); Lemma 4.2; Prop 4.3; Prop 5.5's exhaustion; and Lemmas 3.3/3.6. All of these are owned by other referees.
