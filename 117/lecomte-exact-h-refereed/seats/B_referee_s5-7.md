I found no false step in §§5–7 as printed. Every lemma holds except for one small unjustified step in Lemma 6.3, which is easy to fix. Separately, two of the paper's headline claims are not proved in this paper: the identity h(n) = 1 + √ζ(n) and "these are also the groups attaining ζ(n)". Both are taken from the author's own unrefereed companion preprint [13].

**Verdict for §§5–7: HOLDS WITH FIXES.**

h(n) = T(n) and the classification of maximizers for n ≥ 9 do not depend on [13]. They do depend on the §§1–4 lemmas the other referee covers: Lemmas 2.1–2.4, (2), (3), (4), Lemmas 4.2–4.5, and the strictness claim for odd primes in Proposition 4.1.

## Per-lemma table

| Item | Page | Verdict |
|---|---|---|
| §5 case map | 11 | HOLDS. The cases cover everything: some radical nonabelian; all abelian with a rank-two form; all ranks ≥ 4 with a noncentral radical; all radicals central (one or several commutator components). For ν = 2 only one component is possible. |
| Cyclic-lift row (N ≥ 2ν+1) | 12 | HOLDS |
| §5.1 nonabelian radical | 12 | HOLDS. I checked every step: Lemma 4.5 widths, ∩C_A(g_i) = Z(P), N ≥ ν+dm+2, N ≥ 4h, and the final comparison. |
| §5.2 opening (rank two; fibre average for N ≥ 2d+5) | 12 | HOLDS |
| Lemma 5.1, Steps 1–5 | 13–14 | HOLDS. The hypothesis "all nonzero scalar forms have rank ≥ 4" is never used in this proof (harmless). |
| "Covering each fibre separately" | 14 | HOLDS |
| Lemma 5.2, Steps 1–7 | 14–16 | HOLDS. I verified the class-two argument, the K⊕U model (common radical 0, every scalarization has rank 4, the 9-subspace partition), and the plane counting (45 incidences, 15 planes). |
| (6) N ≥ 3(ν−3) | 16 | HOLDS |
| Lemma 5.3 | 16–17 | HOLDS (standard Scharlau decomposition) |
| Lemma 5.4, Steps 1–5 | 17 | HOLDS. The [10, Lemma 3] bound e ≤ ν/2 is true over finite fields: apply Chevalley–Warning to the Pfaffian, a form of degree ν/2 in e variables. |
| §5.4 products of Sylow subgroups | 17–18 | HOLDS |
| Proposition 6.1 case map | 18 | HOLDS, complete. Solvable groups split by complement (cyclic or nonabelian) and kernel H (abelian or not); the nonabelian-complement case with N ≤ 44 forces H abelian. |
| §6.1 elementary facts and (7) | 18 | HOLDS |
| Lemma 6.2 | 19 | HOLDS. The proof is fully self-contained and uses no central-index bound from [13]. The nilpotent form of Baer–Suzuki is derived correctly. |
| Descent numerics (N ≥ 45) | 19 | HOLDS |
| §6.2 nonsolvable, N ≤ 44 | 19 | HOLDS. CITATION checked against the source (below). |
| §6.3 affine quotient, (8) | 19–20 | HOLDS |
| §6.4 | 20–21 | HOLDS |
| Lemma 6.3 | 21 | GAP (minor, r = 3) |
| §6.5 | 21–22 | HOLDS |
| §6.6 | 22–23 | HOLDS (one ordering issue, NOTE) |
| §7: h(n) = T(n) and the n ≥ 9 maximizers | 23 | HOLDS |
| §7: comparison with ζ | 23 | Not proved here; imported from [13] |
| §7: closing "tight/loose" remarks | 23 | Unproved |

## Objections, ranked

**MUST:** none in §§5–7.

**SHOULD 1 — Lemma 6.3, case r = 3 (p. 21).** The text says: "Some centralizer has index at most three by Lemma 2.4. Its index divides four and is at least two, hence equals two." Nothing justifies "at least two", and index 1 is not excluded by divisibility.
- Fix: if a vertex x of a maximum clique X in gH satisfied C_H(x) = H, then x would commute with every element of xH = gH. That forces |X| = 1, contradicting r = 3.

**SHOULD 2 — §7 relies on [13] (p. 23; also Theorem 1.1 and the abstract).** The text says: "The central-index theorem [13, Theorems 1.1 and 1.2(v)] gives ζ(n) = (n−1)² for 3 ≤ n ≤ 6, ζ(7) = ζ(8) = 81, and ζ(n) = 4^⌊(n−1)/2⌋…"
- These two headline claims are imported from [13], a preprint by the same author, not proved here: h(n) = 1 + √ζ(n), and "These are also the groups attaining ζ(n)".
- I checked that [13]'s Theorems 1.1 and 1.2(v) say what is quoted.
- I did not check [13]'s proofs. As a numerical sanity check, z(G) ≤ ζ(ω(G)) held on all 5,644 groups I computed.
- For Erdős #117 (estimate h(n)), h(n) = T(n) stands without [13].
- The paper's §6.1 credit line ("selection argument … [13, Proposition 4.3]") does not import anything; the proof is given in full.

**SHOULD 3 — §6.2 depends on the classification of finite simple groups (p. 19).** The author discloses this. [2] = arXiv:0903.0692, Theorem 1.1, says what is used:
- hypothesis: G finite, nonsolvable, ω ≤ 57;
- alternatives: (1) Z(G)×PSL(2,p); (2) Z(G)SL(2,p); (3) G″⟨a⟩S with G″ ∈ {A5, SL(2,5)}; (4) G″⟨a⟩Z(G) with G″ ∈ {PSL(2,7), SL(2,7)}.

The paper writes "all four alternatives give G = G″⟨a⟩S". That is correct because Z(G) ≤ S. The value ω(PSL(2,7)) = 57 matches AAHZ's account of [1, Lemma 4.4] (q² + q + 1), and I computed 57 directly. AAHZ's own Lemma 2.10 is terse ("it is easy to see … a² ∈ Z(G)"), but the paper only needs [G : G″S] ≤ 2, which follows from G/S ≅ S5. [1] itself was not fetched.

**NOTE 1 — §6.6 (p. 22).** "If one is zero, its full fibre gives m ≥ 2√m vertices" needs m ≥ 4. That only follows from "A nonabelian L requires d ≥ 2", which comes in the next paragraph. Reorder.

**NOTE 2 — §7 closing remarks (p. 23).** "The loose case occurs even for groups of class two with elementary abelian central quotient" comes with no example and no proof, and nothing else is proved in that paragraph. My random search of 300 class-two pencils on F₂⁶ with a totally isotropic 4-space found no example.

**NOTE 3 — Lemma 6.3.** The conclusion I ≤ 2^r is never used later.

**NOTE 4 — §5.4.** Two facts are stated without the one-line justification: ω(G₁×G₂) ≥ ω(G₁)ω(G₂) (a product of cliques is a clique) and a(G₁×G₂) ≤ a(G₁)a(G₂).

**NOTE 5 — notation.** Some symbols are reused: v = ms; D = max(c, ℓ) versus D for cliques; S for both the solvable radical and the set G∖F.

**NOTE 6 — references not fetched.** I did not fetch Doerk–Hawkes [6, A.15.6], Scharlau [17], Gow–Quinlan [10] or Gorenstein [9, 3.8.2]. The facts used from each are standard, and the [10] bound is independently justified above.

## What I tested that could have failed

Scripts are in `/home/exedev/MathDyad/subs-1116/117/seatB/`. GAP exports the commuting structure on G/Z(G); a solver then computes the exact cover number a and clique number ω. Every run was under `ulimit -v`; the cadical PIDs were never touched.

- **Controls.** Known values reproduced: D8 3/3, S3 4/4, A4 5/5, S4 ω=10, A5 21/21, S5 31, PSL(2,7) 57, 2^{1+4} 5/5, 3^{1+4} ω=7 and a=10.
  - Negative control: lowering the profile T by 1 flags every tight group.
  - An independent clique search agrees with the solver's ω on the small groups.
- **Exhaustive sweep: every nonabelian group of order ≤ 255**, including orders 128 and 192 (5,644 groups, all values exact).
  - a ≤ T(ω) in every case.
  - a > ω occurs only for 2^{1+6}_± (ω 7, a 9), 3^{1+4} (ω 7, a 10) and 192_1333/1334/1337/1338 (ω 24, a 27).
  - No equality at ω ≥ 9 (2^{1+8} has order 512, outside the range).
  - ω(SL(2,5)) = 31, not 21. §6.2 is safe because it covers by cyclic subgroups of A5.
- **§6.6 primitive groups V⋊L with L nonabelian nilpotent.** The bound ω(Q) ≥ m + 2(ω(L)−1)√m held in every case:

  | m | L | ω(Q) | bound |
  |---|---|---|---|
  | 9 | D8 | 21 | 21 (tight) |
  | 9 | Q8 | 28 | 21 |
  | 9 | SD16 | 39 | 33 |
  | 25 | D8 | 46 | 45 |
  | 25 | Q8 | 76 | 45 |
  | 49 | D8 | 78 | 77 |
  | 49 | Q8 | 148 | 77 |

  For m = 9, Σ|U_c| = 7, 15, 23, within 2|L| − 1.
- **Lemma 6.2.** On 832 nonnilpotent groups up to order 150: some x outside F(G) has class size r ≤ ω, with a conjugate pair giving [G : C_G(⟨x,y⟩)] ≤ r(r−1). The smallest slack is 1, at D10 and SmallGroup(100,1). The run was stopped at order 150.
- **Lemmas 5.1 and 5.2 on real 2-groups.**
  - Order 128: 37 groups satisfy the hypotheses. All have |G/Z| = 32, class 2, and ω = a = 9, exactly as Lemma 5.2 says.
  - Order 256 (partial scan, |Z| ≤ 4): groups with [R:Z] = 4 have ω = 11, which hits the "eleven-point clique" claim exactly. Those with [R:Z] = 8 have ω = 19.
  - Positive control for the radical scan: 64_226 (D8×D8) shows the nonabelian rank-two radicals described on p. 7.
- **Class-two test beds.**
  - Rank-4 pencils on F₂⁵: dim W = 2 always gives ω = a = 9; dim W = 3 gives ω = a = 9 or ω ≥ 14; dim W = 4 gives ω ≥ 21.
  - Lemma 5.1 sampler: 35 instances where the lemma applies, all with d = 4, N = 11 and fibre widths ≤ 2.
- **Arithmetic.** Every numerical inequality in §§5–6 was brute-forced over wide ranges, including worst-case optimisation over (u, s) in §6.4 and §6.5 and the direct §5.1 bound. Zero failures.