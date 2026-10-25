# Referee report, seat `memory`: Lemma 3.7 (exact memory identity, PDF p. 17) and §3.8 (equality-rank restoration, PDF pp. 23–25)

Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026), `/tmp/oaimath/011/paper.pdf`. I read PDF pp. 1–6 and 10–27 rendered, plus the text extraction for quotes. **I did not open any other seat's report (`referee_*.md`) or any other file in `/tmp/oaimath/011/` apart from the brief, the paper, and my own directory `scripts_memory/`.**

## Verdict for this scope

**HOLDS AS READ.**

- **Lemma 3.7 / (3.17).** I checked it as an exact identity in Q(√2, i) on toy instances of §§3.2–3.4. The left side is the physical path sum in the independent-residue model. The right side is Π b_p · ⟨1_∅, G_0E_0⋯G_N1_∅⟩_distinct, built from the paper's literal definitions (3.12), (3.15), (3.16) and (i)–(iv) on p. 16. The two sides are written as independent code: the left side never builds a memory. Results:
  - Exact equality in **all 19 non-degenerate tabulated settings**: one big group with 3–6 primes, M = 2 or 3, raw pattern and comparison patterns with free labels (including two coincident free labels), N = 2 and 4, q ∈ {1/2, 1/4, 4/9, 1/9}, four phases θ, varying shifts. Three of the 19 are genuine two-big-group instances.
  - Also exact equality in 6 preliminary runs on weaker-coverage toys.
  - Three settings were degenerate (both sides exactly 0, because no compatible physical path exists). I do not count them.
  - **Every non-vacuous negative control (10 kinds for (3.17), one more for (3.41)) breaks the equality**, and the right side does not depend on ρ.
- **No term of the paper's definitions had to be changed.** Two of the paper's rules are redundant for the identity. I proved this and confirmed it by controls; they matter only in the enlarged evolution.
- **§3.8.** I re-derived it line by line:
  - (3.41) and (3.42) are correct; I also checked them by computation.
  - (3.44) holds. I wrote the backward induction out explicitly (N = 3 edges, pivot dying at visit 1, dependent born at visit 3). It uses only pointwise weighted row bounds that are uniform in the retained pivot value. C_h = C_a + C_v works.
  - (3.45)–(3.47) and the final display are arithmetically correct under (3.37).
  - The "distinct performed birth values" of (3.41) is exactly Lemma 3.7's distinct-birth rule. Shared continuations, promotions and free draws are correctly not addresses.
- **All objections below are COSMETIC/UNCLEAR, exposition only.** None is a mathematical gap.

**What this verdict does not cover.**
- Lemma 3.6 (residue replacement), Lemmas 3.8–3.10 and (3.28) are outside my scope. I used them only as stated inputs (the row/column bounds L^{C_a}, L^{C_v}, the signed norm L^{−G} of (3.38), and the tail (3.28)). I re-derived (3.20)–(3.22) and (3.26) only far enough to see that the large-rank modification is legitimate.
- Small groups are not modelled. I argue below (§1.1, D11) that they are a common factor of both sides.
- Toy sizes: |P_g| ≤ 6, N ≤ 4 (N = 2 for two groups), at most 2 groups, ghost batches of size ≤ 2.

---

## Part 1: Lemma 3.7 by exact computation

### 1.1 What was modelled, and every interpretive decision (with the sentence quoted)

Code: `scripts_memory/field.py` (exact Q(√2,i)), `model.py` (left and right sides), `model2g.py` (two big groups). Verbatim in the Appendix.

**Left side.** This is the left side of (3.7) with the average over n replaced by the expectation over independent uniform residues at every group prime (Lemma 3.6), the return condition dropped, and e(θh_N) inserted (3.11). The path data are:
- an ordered initial list of distinct labels, mass V_g^{−M};
- at each edge i: a source permutation (weight 1/M!), a pattern ν, free labels with law μ_g and the ban from both lists, target labels with shared slots copied, unshared target labels ranging over P_g with the target list distinct, and normalization V_g^{−t_g};
- the multiplier K_ν·ψ(D) for forward edges, and conj(K_ν(T,S,·)ψ(D)) for backward edges;
- the step h_{i+1} − h_i = σ_i k_i D_i;
- finally E_y of (3.8), with q_0 = q_N = √q and q_i = q inside.

E_y factorizes over primes. I validated the per-prime shortcut against an honest Haar average over Π Z/pZ: equal on all 96 paths of a 3-prime case and on 16 sampled paths of a 4-prime case (`ey_control.py`).

**Right side.** Π_p b_p times the iterated row actions G_0, E_0, …, G_N, evaluated on the initial state (active list integrated against μ̃^{⊗M}, empty memory). The final state must have empty memory, with the distinct-birth indicator enforced incrementally along the expanded path through a set of "born" primes.

Decisions on ambiguous or underspecified sentences:

- **D1. Law of free draws.** Step (i) reads: *"Form D from shared source labels and the independent free draws."* The law is not restated there. I used μ_g, as in Def. 3.3 (*"in the C_g slots, independent labels of law μ_g"*). The Lemma 3.10 proof also lists only *"the measures of active labels and fresh target integrations are μ̃_g in place of μ_g"*. With μ̃_g for free draws the identity **fails** (control `free_mut`, §1.3). See Objection 1.
- **D2. Ghost batch.** (3.16) is an ordered integral over P_g^b with 1/b!. Under the distinct-birth rule (*"Distinct ghost births in an unordered batch are counted once by its factorial divisor"*, p. 17), I sum over b-subsets of unborn primes. This is the same quantity. Control `no_bfact` multiplies each batch by b! and breaks the identity.
- **D3. Pending residues.** Read as *"A pending particle (p, r) records displacement from its required hit, modulo p"*. A store appends (p,0) after the old-zero ρ factors; translation adds σ_i k_i D; "zero" means a hit.
- **D4. Dropped particles stay "born".** *"drop the other unshared source particles"* together with *"the rule that all prime values assigned at different births are distinct … This is a global rule, even if two births occur far apart."* So a dropped or terminated prime can never be reborn.
- **D5. Symmetrizations.** *"with independent source and target symmetrizations in all active lists"*. Since Sym² = Sym and G_i commutes with active-list symmetrization, I use one uniform permutation per edge at the source, identically on both sides.
- **D6. Adjoint orientation.** *"the adjoint moves by −kD, interchanges source and target labels in the coefficient, and conjugates the multiplier"* (p. 12), and (i) *"Multiply by the oriented coefficient K_νD^{iζ}, or its conjugate with roles interchanged"*.
- **D7. D^{iζ}.** It is not in any number field, so I replaced it by an arbitrary function ψ(D) with Gaussian-rational values, conjugated on backward edges. Since (3.17) must hold for every multiplier depending only on (σ, D), this is a stronger test. The phase e(θσkD) is exact: θ = a/8, and e(1/8) ∈ Q(√2,i).
- **D8. K_ν.** For comparison patterns, K_ν is an arbitrary Gaussian-rational function of (source labels, target labels, free labels) via a stable hash. The raw pattern has K = 1.
- **D9. q.** The brief suggested q = 1/2. I kept it, since √(1/2) = √2/2 ∈ Q(√2), and also used q ∈ {1/4, 4/9, 1/9}. For ρ I used ρ ∈ {9/10, 3/4, 5/6, 3/5, 19/20}, with ρ² > √q as required on p. 16.
- **D10. Group primes exceed |k|** (*"For large x every group prime exceeds |k|"*, p. 15). The code asserts this. I used k ∈ {1,2,3,4} with primes ≥ 5.
- **D11. Small groups are not modelled.**
  - In the memory model, small groups use *"the physical target sum, with normalization V_g^{−ℓ}, and the two small endpoint factors q^{(ω_g−M)/2}. These counts concern small states at y and y + Δ"* (p. 16). This is literally the physical independent-residue treatment, and residues are independent across primes.
  - So for each fixed small-list history, both sides carry the identical small factor. The small part's only influence on big primes is the factor D_S inside Δ = σkD_SD_B.
  - I emulate D_S by per-edge integer factors k_i coprime to the big primes ("kseq"). I also ran a genuine two-big-group instance (`model2g.py`).
- **D12. Toy sizes and structure.**
  - The algebra needs only distinct residue fields Z/pZ, so P_g consists of small primes.
  - The first toys (P = {5,7,11} and {5,7,11,13}) were **degenerate**. No prime divided a difference of shifts, so endpoint hits (√q) and h_N ≠ 0 never carried weight, and the comparison pattern was **physically unrealizable**: with M = 2 and both slots unshared, a target needs 2 primes outside the source and the free label, so at least 5 primes.
  - I therefore switched to P = {5,7,17,19} (7 | 19−5, 5 | 17−7) and P = {5,7,17,19,29,(31)}. I added path-type counters to every run (`stats`), so that each "EQUAL" carries its coverage.

### 1.2 Results (exact; left side = physical independent-residue path sum, right side = Π b_p ⟨1_∅, G_0E_0⋯G_N1_∅⟩_distinct)

| # | instance | N | q, ρ, θ, k_i | nonzero physical paths / coverage | result |
|---|---|---|---|---|---|
| 1 | P={5,7,11}, raw, M=2 | 2 | 1/4, 3/4, 1/8, (1,1) | 96 paths | LHS = RHS = 19395804505/14000333778 |
| 2 | P={5,7,17,19}, raw | 2 | 1/2, 9/10, 1/8, (1,1) | 152 nonzero; 56 with h_N≠0; 64 with endpoint (√q) hits; 56 multi-run (store+promote) | LHS = RHS = 11550819174788635/927766734962688 + (15892945173875/57985420935168)√2 |
| 3 | same | 2 | 1/4, 3/4, 3/8, (2,3) | 100 nonzero, all h_N≠0 | LHS = RHS = (−3372251795784655 + 4528564694107895 i)√2 / 133598409834627072 |
| 4 | same | 2 | 4/9, 5/6, 2/8, (1,4) | 100 | LHS = RHS = (950166951286105 − 320690737344845 i)/6262425460998144 |
| 5 | same | 2 | 1/9, 3/5, 1/8, (3,1) | 100 | LHS = RHS = −562032333876125/4174950307332096 + (481238379864935/5566600409776128) i |
| 6 | same, full Sym | 4 | 1/2, 9/10, 1/8, (1,1,1,1) | 636 nonzero; 228 h_N≠0; 256 endpoint hits; 80 hits while pending; 336 needing ghost birth/termination | LHS = RHS = 167047058786631979736402711915/3044844103186717240530567168 − (131709697146489965111525/1321546919785901580091392)√2 |
| 7 | same | 4 | 1/4, 3/4, 3/8, (1,2,1,2) | 32 | EQUAL (complex, see Appendix) |
| 8 | same | 4 | 4/9, 5/6, 1/8, (2,1,3,1) | 24 | EQUAL |
| 9 | P={5,7,17,19,29}, raw + comparison C={1}, full Sym | 2 | 1/2, 9/10, 1/8, (1,1) | 2916 nonzero, 2304 using a comparison edge | EQUAL, ≈ 8.139111723 |
| 10 | same | 2 | 1/4, 3/4, 3/8, (2,1) | 2034 / 1536 comparison | EQUAL, ≈ 0.26360434+0.35300851i |
| 11 | P5, pattern sequence (raw,cmp,raw,raw), fixed permutations | 4 | 1/2, 9/10, 1/8, (1,1,1,1) | 56, all with comparison edge | EQUAL, ≈ −0.0013789−0.0019382i |
| 12 | P5, (raw,raw,cmp,raw) | 4 | 1/2, 9/10, 1/8, (2,1,1,1) | 5 | EQUAL, ≈ −0.0037026−0.0070461i |
| 13 | M=3 (J=2, ℓ=1), P={5,7,17,19,29,31}, comparison C={1} on both edges (one shared + one free label in the same group) | 2 | 1/2, 9/10, 1/8, (1,1) | 1632 | EQUAL, ≈ 0.0088502483 |
| 14 | M=3, P5, raw+cmp | 2 | 1/4, 3/4, 3/8, (1,2) | 120 | EQUAL |
| 15 | J=2, ℓ=0, C={1,2} (two free labels; every nonzero path has them **coincident**, f1=f2), P5 | 2 | 1/2, 9/10, 1/8, (1,1) | 564 nonzero; 20 paths where two orphans can coexist | EQUAL, ≈ 2.057927131 |
| 16 | same, sequence (C12,raw,raw,C12) | 4 | 1/4, 3/4, 3/8 | 304; 24 hits while pending | EQUAL, ≈ 0.0272118998 |
| 17 | **two big groups** {5,7,17} ∪ {11,19,23}, raw, M=2 per group, D = k·s_1s_2 | 2 | 1/2, 9/10, 1/8, 1 | 144 | LHS = RHS = 47838947920237520898775/17049841958960727688328 |
| 18 | two big groups {5,7,17} ∪ {11,13,19} | 2 | 1/4, 3/4, 3/8, 2 | 144 | LHS = RHS = 112496611438713532815785/60486908118762618754704 |
| 19 | same | 2 | 4/9, 5/6, 1/8, 3 | 144 | LHS = RHS = 16559539870364223377645/20162302706254206251568 |
| (deg.) | P5 (cmp,raw,raw,cmp) k=(1,1,2,1); P={5,7,11} raw+cmp k=(1,2,3,1), θ ∈ {0, 1/8} | 4 | | 0 nonzero | 0 = 0, **not counted** |

Preliminary runs (Appendix, `out_prelim.txt`): P = {5,7,11} and {5,7,11,13}, raw and raw+cmp, N = 2 and 4, 6 non-degenerate settings, all exactly equal. The comparison pattern is physically unrealizable on these primes, and no endpoint hit carries weight there, so these runs have low coverage. A two-group N = 4 run was stopped after 11 minutes (right side state explosion); it is not reported.

Slot indices in this report are 1-based as in the paper (the code is 0-based: `frozenset({0})` = C_g = {1}).

The row-15 setting also holds with the free labels restricted to f1 = f2 on both sides (`controls.py F1`). The identity is claimed path by path, so restricting path data must preserve it, and it does.

### 1.3 Negative controls (each perturbs ONE rule on the right side only; left side fixed)

| control | rule perturbed | case | result |
|---|---|---|---|
| `fresh_repeat` | distinct-birth rule dropped for fresh target slots | row 2 | **DIFFER** (RHS−LHS ≈ 30.44+0.58i) |
| `ghost_repeat` | distinct-birth rule dropped for ghost births | row 2 | **DIFFER** (+0.2492) |
| `no_bfact` | 1/b! removed from the ghost batch | row 15 (two coexisting orphans) | **DIFFER** (+0.00035995) |
| `no_bfact` | same | rows 2, 6 (no batch of size ≥ 2 can carry weight) | equal, as expected |
| `mu_not_mut` | births weighted by μ_g instead of μ̃_g = 1/(V_g p b_p) | rows 2 / 6 | **DIFFER** (−4.673 / −34.35+0.025i) |
| `no_rho_iv` | ρ for remaining pending zeros in (iv) omitted | rows 2 / 6 | **DIFFER** (−0.01722 / −0.1311−0.0080i) |
| `q0_bulk` | q_0 = q_N = q instead of √q in G_0, G_N and b_p | rows 2 / 6 | **DIFFER** (−0.5868 / −2.406) |
| `baseline_internal_only` | b_p = 1 − (1/p)Σ_{0<i<N} η_i (endpoints omitted) | rows 2 / 6 | **DIFFER** (+0.6347 / +2.707) |
| `no_ban` | free-label ban from both active lists removed | row 15 | **DIFFER** (+0.04663) |
| `free_mut` | free draws with law μ̃_g instead of μ_g | row 15 | **DIFFER** (+0.005703) |
| `prom_new` | newly stored particles may be promoted across the same edge | rows 2, 6, 15 | equal (**vacuous; proved below**) |
| `no_pnotD` | "p ∤ D for stored or promoted" removed | rows 2, 6, 15 | equal (**vacuous; proved below**) |
| ρ = 19/20 vs 9/10 | — | rows 2, 6 | equal (ρ cancels, as the proof says) |
| `own_D` (two groups) | group-g memory translated by k·s_g (own shared label) instead of the full Δ = σkD | row 18 | **DIFFER** (−0.2099) |

Separately, I checked (3.41) on 420 random realized paths with up to 7 addresses (0 failures). Its control (drop (|B|−1)! in μ) fails on 80 of 200 (`incl_excl.py`).

**Why the two controls are vacuous.** Under the distinct-birth rule:
1. A stored source particle with p ∤ D has translated residue σkD mod p ≠ 0, because p > |k| and p ∤ D. So *"Newly stored particles cannot be promoted across this edge"* is implied by the residue check.
2. An active particle with p | D would have to be a shared label (the same value born twice) or a free label (banned). So *"Require p ∤ D for every stored or promoted particle"* is implied.

Both rules matter only in the enlarged evolution (equal births allowed) used for Lemmas 3.8–3.9, where the paper indeed re-invokes them (*"The exclusion p ∤ D is retained under reversal, even when numerical coincidences have been allowed"*, p. 21). Not an error; see Objection 2.

### 1.4 The identity by hand (what the computation confirms)

For one big prime p and a fixed compatible path:
- Its residue expectation is (1/p)Π_{i∉act}(1 − η_i H_i) if p is active somewhere, and (1/p)Σ_r Π_i(1 − η_i 1[r+h_i≡0]) otherwise.
- Telescoping (3.13) expands the pre-activity product as "born at a_p" plus Σ_{j<a_p} (−η_j H_j)·(internal damping). The post-activity product expands likewise.
- The inactive case gives b_p + (pb_p)^{−1}Σ_{j<i}… (3.14).

I re-derived (3.13) and (3.14): the partial products telescope; the empty and singleton terms of the inactive expansion give exactly b_p, and degree ≥ 2 terms group by their extreme indices.

Each lifespan term corresponds to exactly one memory history, with these weights:
- **Birth.** Initial or fresh: μ̃ = 1/(V_g p b_p), where the 1/V_g is the physical slot normalization. Ghost: (−η_jV_g/ρ)μ̃·ρ = −η_j/(pb_p).
- **Promotion.** V_g^{−1}, with the residue check by counting measure, so no 1/p.
- **Internal hit while pending.** ρ·(q_i/ρ²)·ρ = q_i.
- **Ghost termination.** ρ(−η_i/ρ).
- **Drop.** The constant "1" term of the post-activity expansion.
- **Shared continuation.** Free; the congruence is automatic because p | D.

The physical constraints that are not explicit in the memory model are implied:
- Distinct labels within a list follow from distinct births.
- An unshared label cannot persist across an edge: it would divide kD, hence D, so it would be shared (a duplicate) or free (banned).

So there is a bijection (physical path) × (one lifespan term per represented big prime) ↔ (memory path with distinct births), and it preserves coefficients. Removing any one of the weights listed above breaks the identity in the controls. **Lemma 3.7 is correct as stated.**

---

## Part 2: §3.8 by hand (PDF pp. 23–25)

### 2.1 Addresses and (3.41)

*"In the truncated evolution allocate potential birth addresses as follows: initial big slots; every possible big target slot at every edge, in its canonical order before final symmetrization; and indices 1, …, B in each group's ordered ghost batch at each visit. A target slot is performed as an address precisely when it is a fresh birth rather than shared or promoted. A ghost address is performed precisely when its batch is at least that large."*

Count: A_* ≤ M|B| + NM|B| + (N+1)|B|B ≤ M|B|(N+1) + (N+1)|B|B. This is O(J·T·L^{0.52} + T·L^{2.52}) ≤ L^{2.53} for x ≥ x_0(J), so the exponent C' can be absolute, as claimed in (3.39).

(3.41) is pathwise. For a realized path, Σ_π μ(π)1_{C_π} sums over blocks contained in the performed addresses, monochromatic within each block, with weight Π(−1)^{h−1}(h−1)!. Reading each block as a cycle, this equals the signed count of value-preserving permutations of the performed addresses. The count factors over equal-value classes and equals 1 iff every class is a singleton. **Correct; computationally confirmed** (`incl_excl.py`).

*Potential vs performed:* blocks are chosen among potential addresses and C_π demands performance, so non-performed addresses contribute 0. Fine.

### 2.2 (3.42)

Collections with weight |μ| ↔ permutations whose non-trivial cycles are the blocks, so Σ_{r(π)=r}|μ(π)| = [t^r]Π_{j<A_*}(1+jt) = e_r(0,…,A_*−1) ≤ (A_*²/2)^r/r! ≤ A_*^{2r}. Also Σ|B'| = r + #blocks ≤ 2r. **Correct; computationally confirmed for A_* ≤ 7** (the equality with e_r is exact).

### 2.3 Large rank: why each dependent birth saves O(P_*^{−1})

Absolute weighted row bounds (Lemma 3.8, (3.22)) factor over local choices. In the edge proof (*"fresh integrations have mass μ̃_g(P_g)^{t_g−a_g} ≤ 2^{t_g}"*, p. 20), the fresh mass of each fresh slot is a separate multiplicative factor. Constraining one fresh slot to a point p̂ replaces μ̃_g(P_g) ≍ 1 by μ̃_g(p̂) ≤ 1/(v_− P_* b_p) ≪ P_*^{−1}; this is (3.43).

The rest of the row sum is untouched, for three reasons:
- (a) The step Δ = σkD depends on shared labels (earlier births) and free draws (not births), never on this edge's fresh values.
- (b) The promotion count depends on old pending residues and Δ only. (3.26) is uniform in the number of zero residues.
- (c) The target weight w = v^{j_tot} depends on j_old + #stores − #promotions only.

The coefficient K_νD^{iζ}e(·) is bounded by sup|K_ν| (3.2). The ban and the p ∤ D exclusions only remove terms of an absolute sum, so *"exclusions may be discarded"* is valid for an upper bound.

For a ghost dependent at batch index h: Σ_{b≥h}(1/b!)(|C_i|v)^b ν(P_g)^{b−1}·sup μ̃ ≤ (sup μ̃/ν(P_g))·exp(|C_i|vν(P_g)). This is the same relative saving with constant |C_i|v ≤ v_+v/ρ. *"The birth coefficient V_g and the memory weight only give fixed constants per constrained coordinate"* is correct. Initial slots: ∫μ̃(x_a)μ̃(x_b)1[x_a=x_b] ≤ sup μ̃. Pivots and dependents inside one operation: integrate the pivot first and constrain the dependent; the canonical order makes this well defined.

A dependent in a different group than its pivot gives mass 0. Fine.

### 2.4 The backward induction, written out (N = 3 edges; one rank-1 collection {β_0, β_1}; pivot β_0 dies at visit 1; dependent β_1 born at visit 3)

**Setup.** Operations in order: G_0, E_0, G_1, E_1, G_2, E_2, G_3. Take β_0 = an initial big slot (value p̂ = x_{β_0}). Its particle is shared across E_0 to visit 1 and then dropped at E_1's departure, so it is absent from every later state. Take β_1 = a fresh target slot of E_2 (arrival at visit 3). A ghost birth in G_3 = G_N cannot be the dependent, since it leaves memory non-empty and is killed by 1_∅.

Write |X| for absolute kernels of the enlarged truncated evolution and |E_2|^{[p̂]} for E_2 restricted to choices in which slot β_1 is fresh, with its value fixed to p̂. The constrained absolute contribution is

∫ dμ̃^{⊗M|B|}(x) Φ_0((x, ∅); p̂ = x_{β_0}), where

- Φ_7 := 1_∅,
- Φ_6 := |G_3|Φ_7,
- Φ_5(·;p̂) := |E_2|^{[p̂]}Φ_6,
- Φ_4 := |G_2|Φ_5(·;p̂),
- Φ_3 := |E_1|Φ_4(·;p̂),
- Φ_2 := |G_1|Φ_3(·;p̂),
- Φ_1 := |E_0|Φ_2(·;p̂),
- Φ_0 := |G_0|Φ_1(·;p̂).

"Retain all pivot values in the conditioning" means exactly this: p̂ is a **parameter** of the functions Φ_5, …, Φ_0, not a coordinate of the state. Only the kernel of |E_2|^{[p̂]} depends on p̂. Pointwise bounds, for every state s and every p̂:

- Φ_7 ≤ w, since w = v^{j_tot} ≥ 1 for v > 1 and 1_∅ ≤ 1 (*"beginning with 1_∅ ≤ w"*).
- Φ_6 ≤ |G_3|w ≤ L^{C_v}w, by the (3.22) row bound.
- Φ_5 ≤ L^{C_v}|E_2|^{[p̂]}w ≤ L^{C_v}·(C/P_*)L^{C_a}w, by 2.3 above, uniformly in p̂.
- Φ_4 ≤ (C/P_*)L^{C_a+2C_v}w.
- Φ_3 ≤ (C/P_*)L^{2C_a+2C_v}w. The drop of the pivot particle at E_1 is irrelevant: the bound on Φ_4 is uniform over all states reached, whether or not they contain a particle of value p̂.
- Φ_2 ≤ (C/P_*)L^{2C_a+3C_v}w, then Φ_1 ≤ (C/P_*)L^{3C_a+3C_v}w, then Φ_0 ≤ (C/P_*)L^{3C_a+4C_v}w.

At the initial boundary, w(x, ∅) = 1 and ∫dμ̃^{⊗M|B|} = Π_gμ̃_g(P_g)^M = 1 + O(sN/P_*). Total ≤ (C/P_*)L^{(C_a+C_v)(N+1)}(1 + o(1)). This is (3.44) with C_h = C_a + C_v (plus ε).

Variant: if the pivot is a ghost birth (index h) in G_0, or is ghost-terminated in G_1, Φ_0 integrates the batch with Φ_1(·; p̂ = p'_h). The integrand bound is uniform in p'_h, so the same estimate follows.

Only **row** bounds are iterated, so no column bound or adjoint measure is needed here. **Correct**: the paper's three sentences beginning *"For completeness, these conditional row bounds can be iterated…"* say exactly this.

### 2.5 (3.45) and the r ≥ r_0 sum

r_0 = ⌈C''NT/L^c⌉. Since c < d < 0.47 < 0.52, r_0 → ∞ and r_0/N = O(T/L^c) + O(1/N) → 0. Then

L^{C_h(N+1)}Σ_{r≥r_0}(CL^{C'}/P_*)^r ≤ 2L^{C_h(N+1)}exp(−r_0(L^c − C'log L − log C)) ≤ L^{C_h(N+1) − C''N(1−o(1))}.

This uses r_0L^c ≥ C''NT = C''N log L, and r_0·C'log L = O(NT²/L^c) = o(N log L). With C'' > C_h + E (chosen after C_h, C, C', as stated), it is o(L^{−EN}). **Correct.**

### 2.6 Small rank: (3.46)–(3.47) and the final display

- (3.46) ∫_{[0,1]^{h−1}}e(Σ_jτ_j(p_{β_j} − p_{β_0}))dτ = Π_j1[p_{β_j} = p_{β_0}] for integers. **Exact.**
- For fixed τ, the factor e(τ_jp_{β_j}) attaches to the dependent's birth operation and e(−Σ_jτ_jp_{β_0}) to the pivot's. Together with the "performed" indicators, these are multipliers of modulus ≤ 1 on the local choices of single operations. The fresh slot's value and its fresh-vs-promoted status are local choices of that edge; batch size b ≥ h is a local choice of that G_i.
- Lemma 3.8's last sentence (*"These bounds and Equation (3.22) persist under arbitrary multipliers of modulus at most one on individual local transition choices, and under memory-size projections."*) then gives operator norms ≤ L^{C_a} (edges) and ≤ L^{C_v} (ghost operations) through (3.18), since |K_mult| ≤ |K| pointwise.
- Unaffected edges are literally the operators of (3.38), so ‖E_i‖ ≤ L^{−G}.
- All factors act on the same Hilbert space H, so submultiplicativity applies: |⟨v_0, G_0E_0⋯G_N1_∅⟩| ≤ ‖v_0‖‖1_∅‖Π‖G_i'‖Π‖E_i'‖. Here v_0 is the phase-modified initial vector, and the initial slots are always performed.

**Ghost-batch symmetrization.** Averaging ϕ_b over S_b inside (1/b!)∫Π dμ̃ does not change the integral, because the rest is symmetric in the batch variables. The average still has modulus ≤ 1, so the operator acts on symmetric memories. **Correct.**

**"At most 2r edges are affected."** The number of affected **operations** is at most the number of addresses in π, which is ≤ 2r.
- A block whose addresses lie in the same edge (for example two fresh slots of a comparison pattern with t_g ≥ 2) affects fewer edges.
- A ghost address affects a G_i, whose bound L^{C_v} is already paid by all N + 1 ghost operations.
- An initial address affects only v_0.

So "≤ 2r affected edges" is a valid upper bound. Hence:

|contribution| ≤ ‖v_0‖‖1_∅‖·L^{C_v(N+1)}·L^{−G(N−a)}·L^{C_aa} ≤ O(L^{(−G+C_v)N + C_v + 2r(G+C_a)}), with a ≤ 2r. This is (3.47), uniform in τ.

Integrating over τ ∈ [0,1]^r costs nothing. Summing with (3.42):

Σ_{r<r_0}L^{C'r}·O(L^{(−G+C_v)N+C_v+2r(G+C_a)}) ≤ O(r_0L^{C_v + r_0(C'+2G+2C_a)})·L^{(−G+C_v)N} = L^{(−G+C_v+o(1))N},

because r_0 = o(N). With (3.37), G > E + C_v + 3, this is ≤ L^{−(E+3−o(1))N} = o(L^{−EN}). **Correct.**

No circularity: C_a enters only through the o(N) term, so E_id depends only on E, C_v, C_s, as claimed. Every π falls in exactly one of the two ranges.

### 2.7 Is "distinct performed birth values" the paper's distinct-birth rule?

Lemma 3.7: *"Births comprise initial active slots, fresh active target slots, and ghost births."*
§3.8 addresses: initial big slots (always performed); big target slots *"performed … precisely when it is a fresh birth rather than shared or promoted"*; ghost batch indices *"performed precisely when its batch is at least that large"*.

The two sets coincide.
- Shared continuations and promotions are neither births nor performed addresses. This is correct: physically they are later uses of an earlier birth, and Lemma 3.7's bijection depends on promotions *not* being constrained against their own earlier value.
- Free draws are neither (*"Auxiliary free draws of D are not particle births"*). Small labels are physical and distinct by the definition of a small state.
- The ordered batch with 1/b! times the indicator on ordered tuples equals one count per distinct set (D2).

So Σ_π μ(π)·[truncated enlarged path sum with C_π] = the truncated path sum with the distinct-birth indicator. This is the right side of (3.17) up to the truncation tail (3.28), which the paper bounds *"even with the distinct-birth indicator"* (absolute value of a 0/1 indicator). **Yes.**

---

## Objections (numbered)

1. **p. 16, edge operation (i).** *"Form D from shared source labels and the independent free draws."*
   - **Problem:** The law of the free draws is not restated in the memory model. Only μ_g (Def. 3.3) makes (3.17) true; with μ̃_g it fails (control `free_mut`: RHS − LHS = +0.005703 on row 15). The proof of Lemma 3.10 (*"the measures of active labels and fresh target integrations are μ̃_g in place of μ_g"*) implies μ_g for auxiliary draws, so the intended reading is recoverable.
   - **Severity:** UNCLEAR, exposition.
   - **Fix:** "independent free draws of law μ_g".

2. **p. 16, (iii).** *"Newly stored particles cannot be promoted across this edge. Require p ∤ D for every stored or promoted particle."*
   - **Problem:** Both rules are implied by the distinct-birth rule (proof in §1.3), so they are vacuous for Lemma 3.7 (controls `prom_new`, `no_pnotD` are exactly equal on rows 2, 6, 15). They are needed only in the enlarged evolution (Lemma 3.9).
   - **Severity:** COSMETIC. Not an error; stating the redundancy would have shown that the identity does not depend on them.

3. **p. 17, proof of Lemma 3.7.** *"Thus these constructions are mutually inverse and preserve all coefficients."*
   - **Problem:** The bijection is given at sketch level. The drop alternative (the constant term of the post-activity telescoping), the free-label ban, the oriented multipliers and the permutation averaging are not mentioned, although each is carried identically on both sides.
   - **Severity:** COSMETIC, exposition. Verified by computation (§1.2–1.3) and by hand (§1.4).

4. **p. 24.** *"Thus the total absolute contribution for this fixed collection is at most L^{C_h(N+1)}(C/P_*)^{r(π)}, for fixed C_h, C; both may depend on m, C_1."*
   - **Problem:** C_h is never identified. The explicit induction (§2.4) gives C_h = C_a + C_v + ε, which is consistent with the claimed dependence.
   - **Severity:** COSMETIC.

5. **p. 25.** *"At most 2r edges are affected by a rank-r collection."*
   - **Problem:** What is bounded is the number of affected operations (edges, ghost operations, boundary), at most #addresses ≤ 2r. Same-edge blocks and ghost addresses only lower the edge count, and ghost operations are already charged L^{C_v}.
   - **Severity:** COSMETIC. The bound used in (3.47) is correct.

6. **p. 24.** *"A rank-r collection involves at most 2r addresses. More precisely its total absolute coefficient, summed over all collections of rank r, obeys (3.42)"*
   - **Problem:** "More precisely" joins two different statements. Both are true (§2.2).
   - **Severity:** COSMETIC.

7. **p. 24.** *"this improves the weighted absolute row bound by O(P_*^{−1}) per dependent birth."*
   - **Problem:** This is true because, in Lemma 3.8's row bound, each fresh slot contributes a separate mass factor. For ghost births the relative factor is sup μ̃/ν(P_g) times the constant |C_i|v (§2.3). The paper's next paragraph supplies this, tersely.
   - **Severity:** COSMETIC.

No FATAL and no GAP in this scope.

## Citation table (scope: Lemma 3.7, §3.8)

| cited result | paper's use | source | status |
|---|---|---|---|
| — | No external result is invoked in §3.2–§3.8 (the inputs are internal: (3.2), Lemma 3.4, Lemma 3.8, (3.22), (3.38), (3.28)). Helfgott–Radziwiłł [11, §1.5] and Pilatte [18, §§3, 5] are mentioned on p. 10 only as related work: *"The operators and ranges here differ; the memory identity and transference estimate below are proved for the present model."* | not fetched (not inputs) | N/A |

## Parameter-dependency table (scope)

| constant | fixed where | depends on | used where | claimed independent of |
|---|---|---|---|---|
| q, ℓ, v_±, c_0, C_0, a<b<c<d | Def. 3.1 | — | everywhere | x |
| ρ | p. 16, ρ² > √q | q | (3.16), (i)–(iv) | cancels in (3.17) (verified: ρ-independence) |
| v > 1 | (3.21) | q, ρ, v_+ | weight w = v^{j_tot}, (3.20), (3.44) | J, m, C_1 |
| C_v | (3.22) | q, ρ, v, v_±, C_0 | (3.37), (3.47), (3.44) | m, C_1, J (as claimed; consistent with (3.20)) |
| C_a | Lemma 3.8 | m, C_1, ℓ, q, ρ, v, fixed data | (3.30), (3.44), (3.47) | J |
| C_s | Lemma 3.10 | fixed data | (3.37) | m, C_1, J |
| G | (3.37) | E, C_v | (3.38), (3.47) | J |
| E_id | (3.37) | G, C_s (so E, C_v, C_s) | (3.6) | m, C_1, J, C_a ✓ (C_a enters (3.47) only through the o(N) term) |
| J | p. 23, after (3.37) | C_a, G, c_0, ℓ (so m, C_1) | (3.32) | — (last) |
| B = ⌈L²⌉ | (3.27) | x | (3.28), (3.39) | — |
| C' | (3.42) | absolute (A_* ≤ L^{2.53} for x ≥ x_0(J)) | (3.42), r ≥ r_0 sum, small-rank sum | J ✓ |
| C, C_h | (3.44) | C_a, C_v, v_±, ρ, v (so m, C_1) | (3.44) | J |
| C'' | (3.45) | C_h, C, C', E | r_0 | — |
| r_0 | (3.45) | x, C'' | split of the π-sum | r_0/N → 0 for fixed constants ✓ |
| N = 2⌈L^{0.52}⌉, P_* = exp(L^c) | Thm 3.5, (3.12) | x | all | — |

Order: E → G → E_id → (m, C_1 from Thm 4.1, outside scope) → C_a → J; C_h, C, C'' after C_a. No cycle inside the scope.

## Verified line by line vs skimmed

**Verified line by line (with computation where noted):**
- Def. 3.3 normalizations.
- (3.4) as used.
- (3.8).
- (3.11).
- (3.12).
- (3.13) and (3.14), re-derived and exercised in the toy.
- p. 15, the two compatibility consequences (persistence impossible; Vg^{−1} per run).
- (3.15) as used for the identity (the factorial measure does not enter the identity).
- (3.16).
- Edge operation (i)–(iv) and the following paragraph.
- Distinct-birth rule.
- Lemma 3.7 statement and proof: exact toy computations, 16 settings plus controls.
- (3.39)–(3.42): computation for (3.41) and (3.42).
- Large-rank paragraphs and (3.43)–(3.45): explicit induction.
- Small-rank paragraphs (3.46), ghost symmetrization, "≤ 2r", (3.47), and the final display.
- "Completion of Theorem 3.5".
- The quantifier order in (3.37) and (3.45).

**Skimmed / used as stated inputs (not verified by me):**
- Lemma 3.6, including the Bonferroni/CRT error.
- (3.18)–(3.22): only the ghost row ratio (3.20) re-derived.
- (3.23)–(3.26).
- Lemma 3.8: only its structure (fresh mass as a separate factor) checked.
- Lemma 3.9 and (3.32).
- Lemma 3.10 and the Fourier reduction to T(Θ).
- (3.28) truncation tail (the logic checked; the absolute path bound taken from Lemmas 3.4/3.8).
- Corollary 3.11.
- The small-group factor: argued (D11), not computed. A second big group was emulated (k_i) and genuinely computed at N = 2 (rows 17–19, plus the `own_D` control).

**Not checked:** anything outside §3.


---

## Appendix A — scripts (verbatim)

All scripts live in `/tmp/oaimath/011/scripts_memory/`. Run with `nice -n 19 python3`. Exploratory debugging scripts `dbg1.py`, `dbg2.py` (used only to diagnose why the first toys were degenerate) are in the directory but not reproduced.

### `field.py`

```python
# Exact arithmetic in Q(sqrt2, i): element = (a,b,c,d) meaning (a + b*s) + i*(c + d*s), s = sqrt(2).
from fractions import Fraction as Fr

def E(a=0, b=0, c=0, d=0):
    return (Fr(a), Fr(b), Fr(c), Fr(d))

ZERO = E(0); ONE = E(1)

def add(x, y): return (x[0]+y[0], x[1]+y[1], x[2]+y[2], x[3]+y[3])
def sub(x, y): return (x[0]-y[0], x[1]-y[1], x[2]-y[2], x[3]-y[3])
def neg(x): return (-x[0], -x[1], -x[2], -x[3])

def _m2(a, b, e, f):  # (a+b s)(e+f s)
    return (a*e + 2*b*f, a*f + b*e)

def mul(x, y):
    a, b, c, d = x; e, f, g, h = y
    xx = _m2(a, b, e, f); yy = _m2(c, d, g, h); xy = _m2(a, b, g, h); yx = _m2(c, d, e, f)
    return (xx[0]-yy[0], xx[1]-yy[1], xy[0]+yx[0], xy[1]+yx[1])

def conj(x): return (x[0], x[1], -x[2], -x[3])

def inv(x):
    a, b, c, d = x
    n0 = a*a + 2*b*b + c*c + 2*d*d
    n1 = 2*a*b + 2*c*d
    den = n0*n0 - 2*n1*n1
    if den == 0: raise ZeroDivisionError
    ninv = E(n0/den, -n1/den)
    return mul(conj(x), ninv)

def div(x, y): return mul(x, inv(y))

def powe(x, n):
    r = ONE
    if n < 0: x = inv(x); n = -n
    for _ in range(n): r = mul(r, x)
    return r

def scal(x, fr): fr = Fr(fr); return (x[0]*fr, x[1]*fr, x[2]*fr, x[3]*fr)

def sqrt_of_q(q):
    """exact sqrt of a rational q, returned in Q(sqrt2): q must be a rational square or 2*square"""
    q = Fr(q)
    from math import isqrt
    def issq(fr):
        n, d = fr.numerator, fr.denominator
        rn, rd = isqrt(n), isqrt(d)
        return (rn*rn == n and rd*rd == d), Fr(rn, rd)
    ok, r = issq(q)
    if ok: return E(r)
    ok, r = issq(q/2)   # q = 2 r^2 -> sqrt q = r*sqrt2
    if ok: return E(0, r)
    raise ValueError("sqrt(q) not in Q(sqrt2)")

# zeta8 = e(1/8) = (1+i)/sqrt2 = (sqrt2/2)(1+i)
ZETA8 = E(0, Fr(1, 2), 0, Fr(1, 2))
_Z8 = [ONE]
for _ in range(7): _Z8.append(mul(_Z8[-1], ZETA8))
assert mul(_Z8[7], ZETA8) == ONE

def e8(n):   # e(n/8)
    return _Z8[n % 8]

def fmt(x):
    a, b, c, d = x
    parts = []
    for coef, name in ((a, ''), (b, '*sqrt2'), (c, '*i'), (d, '*i*sqrt2')):
        if coef != 0: parts.append(f"({coef}){name}")
    return ' + '.join(parts) if parts else '0'

def approx(x):
    s = 2 ** 0.5
    return complex(float(x[0]) + float(x[1]) * s, float(x[2]) + float(x[3]) * s)
```

### `model.py`

```python
# Toy instance of OpenAI 011 paper, Sections 3.2-3.4: physical independent-residue path sum (LHS of (3.17))
# versus  prod_p b_p * <1_empty, G_0 E_0 G_1 ... E_{N-1} G_N 1_empty>_distinct  (RHS of (3.17)).
# One big group P (no small groups; small-group shifts emulated by per-edge integer factors kseq[i]).
import itertools, random, zlib
from fractions import Fraction as Fr
from math import factorial
import field as F

class Toy:
    def __init__(self, P, J, ell, patterns, N, q, rho, theta_num, kseq, seed=1, flags=(), sqrtq=None,
                 edge_patterns=None, edge_perms=None):
        self.P = sorted(P); self.J = J; self.ell = ell; self.M = J + ell
        self.patterns = patterns          # list of frozensets C (free slots among 0..J-1); C empty = raw (K=1)
        self.N = N; self.q = Fr(q); self.rho = Fr(rho); self.th = theta_num
        assert len(kseq) == N; self.kseq = kseq
        for p in self.P: assert all(p > abs(k) for k in kseq), "group primes must exceed |k| (paper p.15)"
        self.flags = set(flags)
        self.sq = F.sqrt_of_q(self.q) if sqrtq is None else sqrtq
        assert F.approx(self.sq).real < float(self.rho)**2, "need rho^2 > sqrt q"
        self.V = sum(Fr(1, p) for p in self.P)
        self.Ve = F.E(self.V)
        self.qv = [self.sq if i in (0, N) else F.E(self.q) for i in range(N + 1)]
        self.eta = [F.sub(F.ONE, x) for x in self.qv]
        # RHS-side copies (negative controls may perturb only the RHS)
        self.qvR = list(self.qv)
        if 'q0_bulk' in self.flags:
            self.qvR = [F.E(self.q) for i in range(N + 1)]
        self.etaR = [F.sub(F.ONE, x) for x in self.qvR]
        sum_eta = F.ZERO
        for x in self.etaR: sum_eta = F.add(sum_eta, x)
        if 'baseline_internal_only' in self.flags:
            sum_eta = F.ZERO
            for x in self.etaR[1:-1]: sum_eta = F.add(sum_eta, x)
        self.b = {p: F.sub(F.ONE, F.scal(sum_eta, Fr(1, p))) for p in self.P}
        self.mu = {p: F.E(1 / (self.V * p)) for p in self.P}
        self.mut = {p: F.inv(F.mul(F.E(self.V * p), self.b[p])) for p in self.P}
        self.seed = seed
        self._K = {}; self._psi = {}
        self.memo = {}
        # optional restriction to fixed pattern / permutation sequences (identity is claimed path by path)
        self.edge_patterns = edge_patterns if edge_patterns is not None else [list(range(len(patterns)))] * N
        allperms = list(itertools.permutations(range(self.M)))
        self.edge_perms = edge_perms if edge_perms is not None else [allperms] * N

    # ---- arbitrary coefficients (identical on both sides) ----
    def K(self, pi, S, T, free):
        if not self.patterns[pi]: return F.ONE        # raw pattern K_0 = 1
        key = (pi, S, T, free)
        if key not in self._K:
            r = random.Random(zlib.crc32(repr(('K', self.seed, key)).encode()))
            self._K[key] = F.E(Fr(r.randint(-9, 9), r.randint(1, 7)), 0,
                               Fr(r.randint(-9, 9), r.randint(1, 7)), 0)
        return self._K[key]

    def psi(self, D):          # stands in for D^{i zeta}; backward edges use the conjugate
        if D not in self._psi:
            r = random.Random(zlib.crc32(repr(('psi', self.seed, D)).encode()))
            self._psi[D] = F.E(Fr(r.randint(1, 9), r.randint(1, 5)), 0,
                               Fr(r.randint(-9, 9), r.randint(1, 5)), 0)
        return self._psi[D]

    def edge_mult(self, i, pi, S, T, free, D):
        sig = 1 if i % 2 == 0 else -1
        if sig == 1:
            return F.mul(self.K(pi, S, T, free), self.psi(D))
        else:   # adjoint: interchange source/target labels in the coefficient and conjugate
            return F.conj(F.mul(self.K(pi, T, S, free), self.psi(D)))

    def slots(self, C):
        shared = [s for s in range(self.J) if s not in C]
        unsh = sorted(C) + list(range(self.J, self.M))
        return shared, unsh

    def Dval(self, i, S, shared, free):
        D = self.kseq[i]
        for s in shared: D *= S[s]
        for f in free: D *= f
        return D

    # =================== LHS: physical path sum in the independent-residue model ===================
    def lhs(self, brute=False):
        P, M, N = self.P, self.M, self.N
        self._lhs_total = F.ZERO; self._npaths = 0
        w0 = F.E(self.V ** (-M))
        self.stats = dict(nonzero=0, hN_nonzero=0, cmp_edge=0, multirun=0, endpoint_hit=0, pending_hit=0,
                          ghost_needed=0, orphan_possible=0, two_orphans_possible=0)
        for L0 in itertools.permutations(P, M):
            self._lhs_rec(0, [L0], [0], w0, brute, [])
        return self._lhs_total

    def _lhs_rec(self, i, lists, hs, w, brute, pats):
        N, M, P = self.N, self.M, self.P
        if i == N:
            Efac = self._Ey_brute(lists, hs) if brute else self._Ey(lists, hs)
            ph = F.e8(self.th * hs[-1])             # e(theta h_N), theta = th/8   (3.11)
            c = F.mul(F.mul(w, Efac), ph)
            self._lhs_total = F.add(self._lhs_total, c)
            self._npaths += 1
            if Efac != F.ZERO: self._stat(lists, hs, pats)
            return
        sig = 1 if i % 2 == 0 else -1
        L = lists[-1]
        for perm in self.edge_perms[i]:
            S = tuple(L[j] for j in perm)
            wp = F.scal(w, Fr(1, factorial(M)))
            for pi in self.edge_patterns[i]:
                C = self.patterns[pi]
                shared, unsh = self.slots(C)
                t = len(unsh)
                for free in itertools.product(P, repeat=len(C)):
                    if 'free_equal_only' in self.flags and len(set(free)) > 1: continue
                    if any(f in S for f in free): continue          # ban: free labels not in source list
                    wf = wp
                    for f in free: wf = F.mul(wf, self.mu[f])          # free labels have law mu_g
                    D = self.Dval(i, S, shared, free)
                    for tl in itertools.product(P, repeat=t):
                        T = list(S)
                        for idx, s in enumerate(unsh): T[s] = tl[idx]
                        T = tuple(T)
                        if len(set(T)) < M: continue                 # physical lists: distinct labels
                        if any(f in T for f in free): continue      # ban: free labels not in target list
                        we = F.mul(wf, F.E(self.V ** (-t)))           # prod V_g^{-t_g}
                        we = F.mul(we, self.edge_mult(i, pi, S, T, free, D))
                        self._lhs_rec(i + 1, lists + [T], hs + [hs[-1] + sig * D], we, brute, pats + [pi])

    def _stat(self, lists, hs, pats):
        st = self.stats; st['nonzero'] += 1
        if hs[-1] != 0: st['hN_nonzero'] += 1
        if any(self.patterns[pi] for pi in pats): st['cmp_edge'] += 1
        N = len(lists) - 1
        mr = eh = ph = gh = False
        norph = 0
        for p in self.P:
            act = [i for i, L in enumerate(lists) if p in L]
            if not act:
                cls = {}
                for i in range(N + 1): cls[(-hs[i]) % p] = cls.get((-hs[i]) % p, 0) + 1
                if max(cls.values()) >= 2: norph += 1
            if act:
                runs = 1 + sum(1 for a, b in zip(act, act[1:]) if b > a + 1)
                if runs >= 2: mr = True
                r = (-hs[act[0]]) % p
                hits = [i for i in range(N + 1) if i not in act and (r + hs[i]) % p == 0]
                if any(i in (0, N) for i in hits): eh = True
                if any(act[0] < i < act[-1] for i in hits): ph = True
                if any(i < act[0] or i > act[-1] for i in hits): gh = True
        st['multirun'] += mr; st['endpoint_hit'] += eh; st['pending_hit'] += ph; st['ghost_needed'] += gh
        st['orphan_possible'] += (norph >= 1); st['two_orphans_possible'] += (norph >= 2)

    def _Ey(self, lists, hs):
        # expectation over independent uniform residues of (3.8); factorizes over primes
        tot = F.ONE
        for p in self.P:
            act = [i for i, L in enumerate(lists) if p in L]
            if act:
                rs = {(-hs[i]) % p for i in act}
                if len(rs) > 1: return F.ZERO
                r = rs.pop()
                v = F.E(Fr(1, p))
                for i in range(len(lists)):
                    if i not in act and (r + hs[i]) % p == 0: v = F.mul(v, self.qv[i])
            else:
                cls = {}
                for i in range(len(lists)):
                    c = (-hs[i]) % p
                    cls[c] = F.mul(cls.get(c, F.ONE), self.qv[i])
                v = F.E(p - len(cls))
                for x in cls.values(): v = F.add(v, x)
                v = F.scal(v, Fr(1, p))
            tot = F.mul(tot, v)
        return tot

    def _Ey_brute(self, lists, hs):
        # honest Haar average over y in prod Z/pZ of (3.8) -- control for the shortcut
        tot = F.ZERO; cnt = 0
        for y in itertools.product(*[range(p) for p in self.P]):
            v = F.ONE
            for i, L in enumerate(lists):
                for p, yp in zip(self.P, y):
                    hit = (yp + hs[i]) % p == 0
                    if p in L:
                        if not hit: v = F.ZERO; break
                    elif hit: v = F.mul(v, self.qv[i])
                if v == F.ZERO: break
            tot = F.add(tot, v); cnt += 1
        return F.scal(tot, Fr(1, cnt))

    # =================== RHS: memory evolution with distinct-birth rule ===================
    def rhs(self):
        P, M = self.P, self.M
        tot = F.ZERO
        for L0 in itertools.permutations(P, M):        # initial active slots are births: distinct
            w = F.ONE
            for p in L0: w = F.mul(w, self.birthmass(p))
            tot = F.add(tot, F.mul(w, self.G(0, L0, (), frozenset(L0))))
        return tot

    def birthmass(self, p):
        return self.mu[p] if 'mu_not_mut' in self.flags else self.mut[p]

    def baseline(self):
        x = F.ONE
        for p in self.P: x = F.mul(x, self.b[p])
        return x

    def G(self, i, L, mem, born):
        key = ('G', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho)
        Z = [j for j, (p, r) in enumerate(mem) if r == 0]
        tot = F.ZERO
        cterm = F.div(F.neg(self.etaR[i]), rho)                       # -eta_i/rho  (termination)
        ccont = F.div(self.qvR[i], F.mul(rho, rho))                    # q_i/rho^2   (continuing zero)
        cbirth = F.div(F.mul(F.neg(self.etaR[i]), self.Ve), rho)       # -eta_i V_g/rho (birth)
        unborn = list(self.P) if 'ghost_repeat' in self.flags else [p for p in self.P if p not in born]
        for na in range(len(Z) + 1):
            for A in itertools.combinations(Z, na):
                wA = F.mul(F.powe(cterm, na), F.powe(ccont, len(Z) - na))
                mem1 = tuple(x for j, x in enumerate(mem) if j not in A)
                for nb in range(len(unborn) + 1):
                    for Bs in itertools.combinations(unborn, nb):
                        # (1/b!) * ordered integral over distinct values == sum over b-sets
                        wB = wA
                        for p in Bs: wB = F.mul(wB, F.mul(cbirth, self.mut[p]))
                        if 'no_bfact' in self.flags: wB = F.scal(wB, factorial(nb))
                        mem2 = tuple(sorted(mem1 + tuple((p, 0) for p in Bs)))
                        born2 = born | frozenset(Bs)
                        if i == self.N:
                            if not mem2: tot = F.add(tot, wB)      # 1_empty at the end
                        else:
                            tot = F.add(tot, F.mul(wB, self.E(i, L, mem2, born2)))
        self.memo[key] = tot
        return tot

    def E(self, i, L, mem, born):
        key = ('E', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        P, M = self.P, self.M
        rho = F.E(self.rho)
        sig = 1 if i % 2 == 0 else -1
        tot = F.ZERO
        nz_old = sum(1 for (p, r) in mem if r == 0)
        for perm in self.edge_perms[i]:
            S = tuple(L[j] for j in perm)
            wp = F.E(Fr(1, factorial(M)))
            for pi in self.edge_patterns[i]:
                C = self.patterns[pi]
                shared, unsh = self.slots(C)
                for free in itertools.product(P, repeat=len(C)):
                    if 'free_equal_only' in self.flags and len(set(free)) > 1: continue
                    if 'no_ban' not in self.flags and any(f in S for f in free): continue
                    wf = wp
                    for f in free: wf = F.mul(wf, self.mut[f] if 'free_mut' in self.flags else self.mu[f])
                    D = self.Dval(i, S, shared, free)
                    w_ii = F.mul(wf, F.powe(rho, nz_old))                 # (ii) rho per old pending zero
                    for ns in range(len(unsh) + 1):
                        for St in itertools.combinations(unsh, ns):      # subset of unshared source slots stored
                            if 'no_pnotD' not in self.flags and any(D % S[s] == 0 for s in St): continue
                            stored = [(S[s], 0) for s in St]
                            old_tr = [(p, (r + sig * D) % p) for (p, r) in mem]      # (iii) translate
                            new_tr = [(p, (r + sig * D) % p) for (p, r) in stored]
                            pool = list(enumerate(old_tr))
                            if 'prom_new' in self.flags:
                                pool = pool + [(len(old_tr) + j, x) for j, x in enumerate(new_tr)]
                            allp = old_tr + new_tr
                            cand = [j for j, (p, r) in pool if r == 0 and
                                    ('no_pnotD' in self.flags or D % p != 0)]
                            for npro in range(len(unsh) + 1):
                                for Tp in itertools.combinations(unsh, npro):
                                    for inj in itertools.permutations(cand, npro):
                                        rem = tuple(sorted(x for j, x in enumerate(allp) if j not in inj))
                                        wpr = F.mul(w_ii, F.E(self.V ** (-npro)))   # V_g^{-1} per promotion
                                        fresh_slots = [s for s in unsh if s not in Tp]
                                        if 'fresh_repeat' in self.flags:
                                            fpool = list(P)
                                        else:
                                            fpool = [p for p in P if p not in born]
                                        for fl in itertools.product(fpool, repeat=len(fresh_slots)):
                                            if 'fresh_repeat' not in self.flags and len(set(fl)) < len(fl):
                                                continue                       # distinct births
                                            T = list(S)
                                            for s, j in zip(Tp, inj): T[s] = allp[j][0]
                                            for s, p in zip(fresh_slots, fl): T[s] = p
                                            T = tuple(T)
                                            if 'no_ban' not in self.flags and any(f in T for f in free): continue
                                            wfr = wpr
                                            for p in fl: wfr = F.mul(wfr, self.birthmass(p))
                                            nz_new = sum(1 for (p, r) in rem if r == 0)
                                            if 'no_rho_iv' not in self.flags:
                                                wfr = F.mul(wfr, F.powe(rho, nz_new))   # (iv)
                                            wfr = F.mul(wfr, self.edge_mult(i, pi, S, T, free, D))
                                            wfr = F.mul(wfr, F.e8(self.th * sig * D))     # (i) e(theta sigma k D)
                                            born2 = born | frozenset(fl)
                                            tot = F.add(tot, F.mul(wfr, self.G(i + 1, T, rem, born2)))
        self.memo[key] = tot
        return tot

    def rhs_full(self):
        return F.mul(self.baseline(), self.rhs())
```

### `model2g.py`

```python
# Two (or more) genuine big groups, raw pattern only (J=1 shared, l=1 unshared per group, M=2), exact.
import itertools, random, zlib, sys, time
from fractions import Fraction as Fr
import field as F

class Toy2:
    def __init__(self, groups, N, q, rho, th, k, seed=1, flags=()):
        self.groups = [sorted(g) for g in groups]; self.N = N; self.q = Fr(q); self.rho = Fr(rho)
        self.th = th; self.k = k; self.seed = seed; self.flags = set(flags)
        self.allp = sorted(p for g in self.groups for p in g)
        self.gof = {p: gi for gi, g in enumerate(self.groups) for p in g}
        self.V = [sum(Fr(1, p) for p in g) for g in self.groups]
        sq = F.sqrt_of_q(self.q)
        self.qv = [sq if i in (0, N) else F.E(self.q) for i in range(N + 1)]
        self.eta = [F.sub(F.ONE, x) for x in self.qv]
        se = F.ZERO
        for x in self.eta: se = F.add(se, x)
        self.b = {p: F.sub(F.ONE, F.scal(se, Fr(1, p))) for p in self.allp}
        self.mu_t = {p: F.inv(F.mul(F.E(self.V[self.gof[p]] * p), self.b[p])) for p in self.allp}
        self.memo = {}; self._psi = {}
    def psi(self, D):
        if D not in self._psi:
            r = random.Random(zlib.crc32(repr(('psi', self.seed, D)).encode()))
            self._psi[D] = F.E(Fr(r.randint(1, 9), r.randint(1, 5)), 0, Fr(r.randint(-9, 9), r.randint(1, 5)), 0)
        return self._psi[D]
    def mult(self, i, D):
        sig = 1 if i % 2 == 0 else -1
        m = self.psi(D) if sig == 1 else F.conj(self.psi(D))
        return F.mul(m, F.e8(self.th * sig * D))
    # ---------- LHS ----------
    def lhs(self):
        self.tot = F.ZERO; self.nz = 0; self.cross = 0
        w0 = F.ONE
        for V in self.V: w0 = F.mul(w0, F.E(V ** -2))
        for L0 in itertools.product(*[list(itertools.permutations(g, 2)) for g in self.groups]):
            self._rec(0, [L0], [0], w0)
        return self.tot
    def _rec(self, i, lists, hs, w):
        if i == self.N:
            E = self._Ey(lists, hs)
            if E != F.ZERO: self.nz += 1
            self.tot = F.add(self.tot, F.mul(w, E)); return
        sig = 1 if i % 2 == 0 else -1
        L = lists[-1]
        for perms in itertools.product([(0, 1), (1, 0)], repeat=len(self.groups)):
            S = tuple(tuple(Lg[j] for j in pm) for Lg, pm in zip(L, perms))
            D = self.k
            for Sg in S: D *= Sg[0]
            choices = [[(Sg[0], c) for c in g if c != Sg[0]] for Sg, g in zip(S, self.groups)]
            for T in itertools.product(*choices):
                we = F.scal(w, Fr(1, 2 ** len(self.groups)))
                for V in self.V: we = F.mul(we, F.E(1 / V))
                we = F.mul(we, self.mult(i, D))
                self._rec(i + 1, lists + [T], hs + [hs[-1] + sig * D], we)
    def _Ey(self, lists, hs):
        tot = F.ONE
        for p in self.allp:
            gi = self.gof[p]
            act = [i for i, L in enumerate(lists) if p in L[gi]]
            if act:
                rs = {(-hs[i]) % p for i in act}
                if len(rs) > 1: return F.ZERO
                r = rs.pop(); v = F.E(Fr(1, p))
                for i in range(len(lists)):
                    if i not in act and (r + hs[i]) % p == 0: v = F.mul(v, self.qv[i])
            else:
                cls = {}
                for i in range(len(lists)):
                    c = (-hs[i]) % p; cls[c] = F.mul(cls.get(c, F.ONE), self.qv[i])
                v = F.E(p - len(cls))
                for x in cls.values(): v = F.add(v, x)
                v = F.scal(v, Fr(1, p))
            tot = F.mul(tot, v)
        return tot
    # ---------- RHS ----------
    def rhs(self):
        tot = F.ZERO
        for L0 in itertools.product(*[list(itertools.permutations(g, 2)) for g in self.groups]):
            w = F.ONE
            for Lg in L0:
                for p in Lg: w = F.mul(w, self.mu_t[p])
            born = frozenset(p for Lg in L0 for p in Lg)
            tot = F.add(tot, F.mul(w, self.G(0, L0, (), born)))
        bp = F.ONE
        for p in self.allp: bp = F.mul(bp, self.b[p])
        return F.mul(bp, tot)
    def G(self, i, L, mem, born):
        key = ('G', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho)
        Z = [j for j, (p, r) in enumerate(mem) if r == 0]
        ct = F.div(F.neg(self.eta[i]), rho); cc = F.div(self.qv[i], F.mul(rho, rho))
        unborn = [p for p in self.allp if p not in born]
        tot = F.ZERO
        for na in range(len(Z) + 1):
            for A in itertools.combinations(Z, na):
                wA = F.mul(F.powe(ct, na), F.powe(cc, len(Z) - na))
                mem1 = tuple(x for j, x in enumerate(mem) if j not in A)
                for nb in range(len(unborn) + 1):
                    for Bs in itertools.combinations(unborn, nb):   # batch in each group (product over groups)
                        wB = wA
                        for p in Bs:
                            cb = F.div(F.mul(F.neg(self.eta[i]), F.E(self.V[self.gof[p]])), rho)
                            wB = F.mul(wB, F.mul(cb, self.mu_t[p]))
                        mem2 = tuple(sorted(mem1 + tuple((p, 0) for p in Bs)))
                        born2 = born | frozenset(Bs)
                        if i == self.N:
                            if not mem2: tot = F.add(tot, wB)
                        else:
                            tot = F.add(tot, F.mul(wB, self.E(i, L, mem2, born2)))
        self.memo[key] = tot; return tot
    def E(self, i, L, mem, born):
        key = ('E', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho); sig = 1 if i % 2 == 0 else -1
        nz_old = sum(1 for (p, r) in mem if r == 0)
        tot = F.ZERO
        ng = len(self.groups)
        for perms in itertools.product([(0, 1), (1, 0)], repeat=ng):
            S = tuple(tuple(Lg[j] for j in pm) for Lg, pm in zip(L, perms))
            D = self.k
            for Sg in S: D *= Sg[0]
            w0 = F.mul(F.E(Fr(1, 2 ** ng)), F.powe(rho, nz_old))
            for stores in itertools.product([False, True], repeat=ng):     # store slot 1 of each group?
                if any(st and D % S[g][1] == 0 for g, st in enumerate(stores)): continue
                stored = [(S[g][1], 0) for g, st in enumerate(stores) if st]
                if 'own_D' in self.flags:   # NEGATIVE CONTROL: translate group-g residues by k*(own shared label) only
                    Dg = {g: self.k * S[g][0] for g in range(ng)}
                    old_tr = [(p, (r + sig * Dg[self.gof[p]]) % p) for (p, r) in mem]
                    new_tr = [(p, (r + sig * Dg[self.gof[p]]) % p) for (p, r) in stored]
                else:
                    old_tr = [(p, (r + sig * D) % p) for (p, r) in mem]
                    new_tr = [(p, (r + sig * D) % p) for (p, r) in stored]
                # per group: target slot 1 is promoted from an old zero of that group, or fresh
                opts = []
                for g in range(ng):
                    o = [('prom', j) for j, (p, r) in enumerate(old_tr) if r == 0 and self.gof[p] == g and D % p != 0]
                    o += [('fresh', p) for p in self.groups[g] if p not in born]
                    opts.append(o)
                for ch in itertools.product(*opts):
                    proms = [c[1] for c in ch if c[0] == 'prom']
                    if len(set(proms)) < len(proms): continue
                    fresh = [c[1] for c in ch if c[0] == 'fresh']
                    if len(set(fresh)) < len(fresh): continue
                    w = w0
                    T = []
                    for g, c in enumerate(ch):
                        if c[0] == 'prom':
                            w = F.mul(w, F.E(1 / self.V[g])); T.append((S[g][0], old_tr[c[1]][0]))
                        else:
                            w = F.mul(w, self.mu_t[c[1]]); T.append((S[g][0], c[1]))
                    rem = tuple(sorted([x for j, x in enumerate(old_tr) if j not in proms] + new_tr))
                    w = F.mul(w, F.powe(rho, sum(1 for (p, r) in rem if r == 0)))
                    w = F.mul(w, self.mult(i, D))
                    tot = F.add(tot, F.mul(w, self.G(i + 1, tuple(T), rem, born | frozenset(fresh))))
        self.memo[key] = tot; return tot

if __name__ == '__main__':
    runs = [([[5, 7, 17], [11, 19, 23]], 2, Fr(1,2), Fr(9,10), 1, 1),
            ([[5, 7, 17], [11, 13, 19]], 2, Fr(1,4), Fr(3,4), 3, 2),
            ([[5, 7, 17], [11, 13, 19]], 2, Fr(4,9), Fr(5,6), 1, 3)]
    if len(sys.argv) > 1 and sys.argv[1] == 'control':
        for (groups, N, q, rho, th, k) in runs[1:2]:
            t = Toy2(groups, N, q, rho, th, k, seed=71); L = t.lhs()
            tc = Toy2(groups, N, q, rho, th, k, seed=71, flags=('own_D',)); R = tc.rhs()
            print(f"control own_D (group-g memory translated by k*s_g instead of k*D): equal={L == R}  RHS-LHS ~ {F.approx(F.sub(R, L)):.6g}")
        sys.exit()
    for (groups, N, q, rho, th, k) in runs:
        t0 = time.time(); t = Toy2(groups, N, q, rho, th, k, seed=71)
        L = t.lhs(); R = t.rhs()
        print(f"[{'EQUAL' if L == R else 'DIFFER'}] two big groups {groups} N={N} q={q} rho={rho} theta={th}/8 k={k}:"
              f" nonzero physical paths={t.nz}  ({time.time()-t0:.1f}s)\n    LHS = {F.fmt(L)}\n    RHS = {F.fmt(R)}\n    LHS ~ {F.approx(L):.10g}", flush=True)
```

### `battery.py`

```python
# Battery of exact checks of Lemma 3.7 (memory identity) on toy instances.
import sys, time
from fractions import Fraction as Fr
import itertools
import field as F
from model import Toy
RAW = frozenset(); C0 = frozenset({0})
P4 = [5, 7, 17, 19]          # 7 | 19-5, 5 | 17-7  -> endpoint / pending hits occur
P5 = [5, 7, 17, 19, 29]      # 5 | 29-19 as well
P6 = [5, 7, 17, 19, 29, 31]
ID2 = [(0, 1)]; ID3 = [(0, 1, 2)]
results = []
def run(tag, **kw):
    t0 = time.time()
    toy = Toy(**kw)
    L = toy.lhs(); R = toy.rhs_full()
    ok = (L == R)
    results.append((tag, ok))
    print(f"[{'EQUAL' if ok else 'DIFFER'}] {tag}\n    paths={toy._npaths} stats={toy.stats} memo={len(toy.memo)} ({time.time()-t0:.1f}s)"
          f"\n    LHS = {F.fmt(L)}\n    RHS = {F.fmt(R)}\n    LHS ~ {F.approx(L):.10g}", flush=True)
    return toy, L, R
which = sys.argv[1] if len(sys.argv) > 1 else 'A'
if which == 'A':
    for (q, rho, th, ks) in [(Fr(1,2), Fr(9,10), 1, [1,1]), (Fr(1,4), Fr(3,4), 3, [2,3]),
                             (Fr(4,9), Fr(5,6), 2, [1,4]), (Fr(1,9), Fr(3,5), 1, [3,1])]:
        run(f"A raw N=2 P={P4} q={q} rho={rho} theta={th}/8 k={ks}",
            P=P4, J=1, ell=1, patterns=[RAW], N=2, q=q, rho=rho, theta_num=th, kseq=ks, seed=11)
if which == 'B':
    for (q, rho, th, ks, sd) in [(Fr(1,2), Fr(9,10), 1, [1,1], 21), (Fr(1,4), Fr(3,4), 3, [2,1], 22)]:
        run(f"B raw+cmp(C={{0}}) N=2 P={P5} q={q} rho={rho} theta={th}/8 k={ks} full Sym",
            P=P5, J=1, ell=1, patterns=[RAW, C0], N=2, q=q, rho=rho, theta_num=th, kseq=ks, seed=sd)
if which == 'C':
    for (q, rho, th, ks) in [(Fr(1,2), Fr(9,10), 1, [1,1,1,1]), (Fr(1,4), Fr(3,4), 3, [1,2,1,2]),
                             (Fr(4,9), Fr(5,6), 1, [2,1,3,1])]:
        run(f"C raw N=4 P={P4} q={q} rho={rho} theta={th}/8 k={ks} full Sym",
            P=P4, J=1, ell=1, patterns=[RAW], N=4, q=q, rho=rho, theta_num=th, kseq=ks, seed=31)
if which == 'D':
    for (seq, ks, sd) in [([0,1,0,0], [1,1,1,1], 41), ([1,0,0,1], [1,1,2,1], 42), ([0,0,1,0], [2,1,1,1], 43)]:
        run(f"D N=4 P={P5} patterns per edge={seq} (0=raw,1=cmp) identity perms q=1/2 rho=9/10 theta=1/8 k={ks}",
            P=P5, J=1, ell=1, patterns=[RAW, C0], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=ks, seed=sd,
            edge_patterns=[[x] for x in seq], edge_perms=[ID2]*4)
if which == 'E':
    run(f"E M=3 (J=2,l=1) N=2 P={P6} cmp C={{0}} on both edges (1 shared + 1 free), identity perms, q=1/2",
        P=P6, J=2, ell=1, patterns=[RAW, C0], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=51,
        edge_patterns=[[1],[1]], edge_perms=[ID3]*2)
    run(f"E M=3 (J=2,l=1) N=2 P={P5} raw+cmp both edges, identity perms, q=1/4",
        P=P5, J=2, ell=1, patterns=[RAW, C0], N=2, q=Fr(1,4), rho=Fr(3,4), theta_num=3, kseq=[1,2], seed=52,
        edge_perms=[ID3]*2)
C01 = frozenset({0, 1})
if which == 'F':
    run(f"F J=2,l=0 (M=2) N=2 P={P5} patterns raw(2 shared) + C={{0,1}} (2 free labels, may coincide), identity perms, q=1/2",
        P=P5, J=2, ell=0, patterns=[RAW, C01], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=61,
        edge_perms=[ID2]*2)
    run(f"F J=2,l=0 (M=2) N=4 P={P5} pattern seq [C01,raw,raw,C01], identity perms, q=1/4",
        P=P5, J=2, ell=0, patterns=[RAW, C01], N=4, q=Fr(1,4), rho=Fr(3,4), theta_num=3, kseq=[1,1,1,1], seed=62,
        edge_patterns=[[1],[0],[0],[1]], edge_perms=[ID2]*4)
print("SUMMARY", which, [(t.split()[0], ok) for t, ok in results])
```

### `controls.py`

```python
# Negative controls: perturb ONE rule of the paper's memory evolution (RHS only) and check the identity breaks.
import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); C0 = frozenset({0})
P4 = [5, 7, 17, 19]; P5 = [5, 7, 17, 19, 29]; ID2 = [(0, 1)]
def case(name):
    if name == 'A1':
        return dict(P=P4, J=1, ell=1, patterns=[RAW], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=11)
    if name == 'C1':
        return dict(P=P4, J=1, ell=1, patterns=[RAW], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1,1,1], seed=31)
    if name == 'F1':   # two free labels forced EQUAL (path-data restriction applied to both sides)
        return dict(P=P5, J=2, ell=0, patterns=[RAW, frozenset({0,1})], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1,
                    kseq=[1,1], seed=61, edge_perms=[ID2]*2, flags=('free_equal_only',))
    if name == 'D1':
        return dict(P=P5, J=1, ell=1, patterns=[RAW, C0], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1,1,1],
                    seed=41, edge_patterns=[[0],[1],[0],[0]], edge_perms=[ID2]*4)
cname = sys.argv[1]
flagsets = sys.argv[2].split(',')
kw = case(cname)
bflags = tuple(kw.pop('flags', ()))
base = Toy(**kw, flags=bflags); L = base.lhs(); R0 = base.rhs_full()
print(f"case {cname}: paths={base._npaths} stats={base.stats}\n  LHS = {F.fmt(L)}\n  LHS ~ {F.approx(L):.12g}; unperturbed RHS equal: {L == R0}", flush=True)
for fl in flagsets:
    if fl.startswith('rho='):
        kw2 = dict(kw); kw2['rho'] = Fr(fl[4:]); t = Toy(**kw2, flags=bflags)
    else:
        t = Toy(**kw, flags=bflags + (fl,))
    R = t.rhs_full()
    d = F.sub(R, L)
    print(f"  control {fl:24s}: RHS ~ {F.approx(R):.12g}   equal={R == L}   RHS-LHS ~ {F.approx(d):.6g}", flush=True)
```

### `ey_control.py`

```python
# Control for the per-prime residue shortcut _Ey: compare with honest Haar average over prod Z/pZ on sampled paths.
import random
from fractions import Fraction as Fr
import field as F
from model import Toy
t = Toy([5,7,17,19],1,1,[frozenset()],2,Fr(1,2),Fr(9,10),1,[1,1],seed=11)
paths = []
orig = t._lhs_rec
def rec(i, lists, hs, w, brute, pats):
    if i == t.N: paths.append((list(lists), list(hs))); return
    return orig(i, lists, hs, w, brute, pats)
t._lhs_rec = rec; t.lhs()
rnd = random.Random(5)
nz = [p for p in paths if t._Ey(*p) != F.ZERO]
sample = rnd.sample(nz, 12) + rnd.sample([p for p in paths if t._Ey(*p) == F.ZERO], 4)
bad = 0
for lists, hs in sample:
    a = t._Ey(lists, hs); b = t._Ey_brute(lists, hs)
    if a != b: bad += 1; print("MISMATCH", lists, hs, F.fmt(a), F.fmt(b))
print(f"sampled {len(sample)} paths ({len(nz)} nonzero of {len(paths)}): mismatches = {bad}")
```

### `incl_excl.py`

```python
# Check (3.41): 1_{distinct performed values} = sum_pi mu(pi) 1_{C_pi}, over collections pi of disjoint blocks
# (size>=2) of POTENTIAL addresses; C_pi = all addresses in pi performed and equal within blocks.
# Also check (3.42): sum_{r(pi)=r} |mu(pi)| = e_r(0,1,...,A-1) <= A^{2r}.
import itertools, random
from math import factorial, prod
def collections(addrs):
    """all collections of disjoint blocks of size >= 2 from addrs"""
    addrs = list(addrs)
    if not addrs:
        yield []; return
    a, rest = addrs[0], addrs[1:]
    yield from collections(rest)                       # a in no block
    for k in range(1, len(rest) + 1):                  # a in a block with k others
        for others in itertools.combinations(rest, k):
            rem = [x for x in rest if x not in others]
            for c in collections(rem):
                yield [(a,) + others] + c
def mu(pi): return prod((-1) ** (len(B) - 1) * factorial(len(B) - 1) for B in pi)
def r(pi): return sum(len(B) - 1 for B in pi)
rnd = random.Random(7); bad = 0; trials = 0
for A in range(1, 8):
    cols = list(collections(range(A)))
    for _ in range(60):
        performed = {a for a in range(A) if rnd.random() < 0.8}
        val = {a: rnd.randint(1, 3) for a in performed}
        lhs = 1 if len(set(val.values())) == len(val) else 0
        rhs = sum(mu(pi) for pi in cols
                  if all(a in performed for B in pi for a in B) and all(len({val[a] for a in B}) == 1 for B in pi))
        trials += 1; bad += (lhs != rhs)
    # (3.42)
    for rr in range(0, A):
        s = sum(abs(mu(pi)) for pi in cols if r(pi) == rr)
        er = sum(prod(c) for c in itertools.combinations(range(A), rr)) if rr else 1
        assert s == er, (A, rr, s, er)
        assert s <= A ** (2 * rr)
        assert all(sum(len(B) for B in pi) <= 2 * rr for pi in cols if r(pi) == rr)
print(f"(3.41) checked on {trials} random realized paths with A<=7 potential addresses: failures = {bad}")
print("(3.42) sum_{r(pi)=r}|mu(pi)| == e_r(0..A-1) <= A^{2r}, and #addresses <= 2r: verified for A<=7")
# negative control: drop the (h-1)! factor
bad2 = 0
for _ in range(200):
    A = 5; performed = set(range(A)); val = {a: rnd.randint(1, 2) for a in performed}
    lhs = 1 if len(set(val.values())) == len(val) else 0
    rhs = sum(prod((-1) ** (len(B) - 1) for B in pi) for pi in collections(range(A))
              if all(len({val[a] for a in B}) == 1 for B in pi))
    bad2 += (lhs != rhs)
print(f"negative control (drop (|B|-1)! in mu): failures = {bad2}/200")
```

### `run1.py`

```python
import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy, brute=False):
    t = time.time()
    L = toy.lhs(brute=brute); n = toy._npaths
    R = toy.rhs_full()
    print(f"{tag}: paths={n}  LHS={F.fmt(L)}\n   RHS={F.fmt(R)}\n   equal={L==R}  LHS~{F.approx(L):.6g} RHS~{F.approx(R):.6g}  ({time.time()-t:.1f}s)", flush=True)
    return L, R
toy = Toy([5,7,11], 1, 1, [RAW], 2, Fr(1,4), Fr(3,4), 1, [1,1])
Lb = toy.lhs(brute=True); Ls = toy.lhs(brute=False)
print("brute-force residue average == per-prime shortcut:", Lb == Ls, F.approx(Lb))
show("raw N=2 P={5,7,11} q=1/4 rho=3/4 th=1/8 k=1", toy)
```

### `run2.py`

```python
import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy):
    t = time.time()
    L = toy.lhs(); n = toy._npaths
    R = toy.rhs_full()
    print(f"{tag}: paths={n} memo={len(toy.memo)}\n   LHS={F.fmt(L)}\n   RHS={F.fmt(R)}\n   equal={L==R}  LHS~{F.approx(L):.6g} RHS~{F.approx(R):.6g}  ({time.time()-t:.1f}s)", flush=True)
    return L, R
show("raw+cmp N=2 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1)", Toy([5,7,11],1,1,[RAW,CMP],2,Fr(1,2),Fr(9,10),1,[1,1],seed=3))
show("raw+cmp N=2 P={5,7,11} q=1/4 rho=3/4 th=3/8 k=(2,3)", Toy([5,7,11],1,1,[RAW,CMP],2,Fr(1,4),Fr(3,4),3,[2,3],seed=4))
show("raw N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1,1,1)", Toy([5,7,11],1,1,[RAW],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=5))
show("raw+cmp N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,2,3,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),1,[1,2,3,1],seed=6))
```

### `run3.py`

```python
import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy):
    t = time.time()
    L = toy.lhs(); n = toy._npaths
    R = toy.rhs_full()
    irr = (L[1] != 0 or L[3] != 0)
    print(f"{tag}: paths={n} memo={len(toy.memo)} equal={L==R} sqrt2-part-present={irr} LHS~{F.approx(L):.6g} ({time.time()-t:.1f}s)\n   LHS={F.fmt(L)}\n   RHS={F.fmt(R)}", flush=True)
    return L, R
show("raw+cmp N=4 P={5,7,11} q=1/2 th=0 k=(1,2,3,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),0,[1,2,3,1],seed=6))
show("raw+cmp N=4 P={5,7,11} q=1/2 th=1/8 k=(1,1,1,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=7))
show("raw+cmp N=2 P={5,7,11,13} q=1/2 th=1/8 k=(1,1)", Toy([5,7,11,13],1,1,[RAW,CMP],2,Fr(1,2),Fr(9,10),1,[1,1],seed=8))
show("raw N=4 P={5,7,11,13} q=1/2 th=1/8 k=(1,1,1,1)", Toy([5,7,11,13],1,1,[RAW],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=9))
```

## Appendix B — outputs (verbatim)

### `out_prelim.txt`

```
brute-force residue average == per-prime shortcut: True (1.3853815782219703+0j)
raw N=2 P={5,7,11} q=1/4 rho=3/4 th=1/8 k=1: paths=96  LHS=(19395804505/14000333778)
   RHS=(19395804505/14000333778)
   equal=True  LHS~1.38538+0j RHS~1.38538+0j  (0.1s)
raw+cmp N=2 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1): paths=384 memo=54
   LHS=(15501578015/14000333778)
   RHS=(15501578015/14000333778)
   equal=True  LHS~1.10723+0j RHS~1.10723+0j  (0.2s)
raw+cmp N=2 P={5,7,11} q=1/4 rho=3/4 th=3/8 k=(2,3): paths=384 memo=46
   LHS=(31032830675/74668446816)*sqrt2 + (-27791446375/74668446816)*i*sqrt2
   RHS=(31032830675/74668446816)*sqrt2 + (-27791446375/74668446816)*i*sqrt2
   equal=True  LHS~0.587759-0.526367j RHS~0.587759-0.526367j  (0.3s)
raw N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1,1,1): paths=1536 memo=102
   LHS=(2118059699100083585/22212568674681856)
   RHS=(2118059699100083585/22212568674681856)
   equal=True  LHS~95.3541+0j RHS~95.3541+0j  (0.9s)
raw+cmp N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,2,3,1): paths=24576 memo=50
   LHS=0
   RHS=0
   equal=True  LHS~0+0j RHS~0+0j  (13.9s)
raw+cmp N=4 P={5,7,11} q=1/2 th=0 k=(1,2,3,1): paths=24576 memo=50 equal=True sqrt2-part-present=False LHS~0+0j (13.7s)
   LHS=0
   RHS=0
raw+cmp N=4 P={5,7,11} q=1/2 th=1/8 k=(1,1,1,1): paths=24576 memo=102 equal=True sqrt2-part-present=False LHS~115.239+0j (13.2s)
   LHS=(809923156956213685/7028195557223556)
   RHS=(809923156956213685/7028195557223556)
raw+cmp N=2 P={5,7,11,13} q=1/2 th=1/8 k=(1,1): paths=10800 memo=468 equal=True sqrt2-part-present=False LHS~3.55371+0j (8.2s)
   LHS=(2730219303857045/768273587900928)
   RHS=(2730219303857045/768273587900928)
raw N=4 P={5,7,11,13} q=1/2 th=1/8 k=(1,1,1,1): paths=15552 memo=1332 equal=True sqrt2-part-present=False LHS~259.479+0j (10.6s)
   LHS=(12002802039802802054979527375/46257277455034833256316928)
   RHS=(12002802039802802054979527375/46257277455034833256316928)
```

### `out_AC.txt`

```
[EQUAL] A raw N=2 P=[5, 7, 17, 19] q=1/2 rho=9/10 theta=1/8 k=[1, 1]
    paths=432 stats={'nonzero': 152, 'hN_nonzero': 56, 'cmp_edge': 0, 'multirun': 56, 'endpoint_hit': 64, 'pending_hit': 0, 'ghost_needed': 64} memo=460 (1.1s)
    LHS = (11550819174788635/927766734962688) + (15892945173875/57985420935168)*sqrt2
    RHS = (11550819174788635/927766734962688) + (15892945173875/57985420935168)*sqrt2
    LHS ~ 12.83774792+0j
[EQUAL] A raw N=2 P=[5, 7, 17, 19] q=1/4 rho=3/4 theta=3/8 k=[2, 3]
    paths=432 stats={'nonzero': 100, 'hN_nonzero': 100, 'cmp_edge': 0, 'multirun': 4, 'endpoint_hit': 8, 'pending_hit': 0, 'ghost_needed': 8} memo=406 (0.6s)
    LHS = (-3372251795784655/133598409834627072)*sqrt2 + (4528564694107895/133598409834627072)*i*sqrt2
    RHS = (-3372251795784655/133598409834627072)*sqrt2 + (4528564694107895/133598409834627072)*i*sqrt2
    LHS ~ -0.0356971631+0.04793737902j
[EQUAL] A raw N=2 P=[5, 7, 17, 19] q=4/9 rho=5/6 theta=2/8 k=[1, 4]
    paths=432 stats={'nonzero': 100, 'hN_nonzero': 100, 'cmp_edge': 0, 'multirun': 4, 'endpoint_hit': 8, 'pending_hit': 0, 'ghost_needed': 8} memo=405 (0.6s)
    LHS = (950166951286105/6262425460998144) + (-320690737344845/6262425460998144)*i
    RHS = (950166951286105/6262425460998144) + (-320690737344845/6262425460998144)*i
    LHS ~ 0.1517250716-0.05120871128j
[EQUAL] A raw N=2 P=[5, 7, 17, 19] q=1/9 rho=3/5 theta=1/8 k=[3, 1]
    paths=432 stats={'nonzero': 100, 'hN_nonzero': 100, 'cmp_edge': 0, 'multirun': 4, 'endpoint_hit': 8, 'pending_hit': 0, 'ghost_needed': 8} memo=406 (0.7s)
    LHS = (-562032333876125/4174950307332096) + (481238379864935/5566600409776128)*i
    RHS = (-562032333876125/4174950307332096) + (481238379864935/5566600409776128)*i
    LHS ~ -0.1346201254+0.08645103734j
SUMMARY A [('A', True), ('A', True), ('A', True), ('A', True)]
[EQUAL] C raw N=4 P=[5, 7, 17, 19] q=1/2 rho=9/10 theta=1/8 k=[1, 1, 1, 1] full Sym
    paths=15552 stats={'nonzero': 636, 'hN_nonzero': 228, 'cmp_edge': 0, 'multirun': 636, 'endpoint_hit': 256, 'pending_hit': 80, 'ghost_needed': 336} memo=1300 (19.2s)
    LHS = (167047058786631979736402711915/3044844103186717240530567168) + (-131709697146489965111525/1321546919785901580091392)*sqrt2
    RHS = (167047058786631979736402711915/3044844103186717240530567168) + (-131709697146489965111525/1321546919785901580091392)*sqrt2
    LHS ~ 54.72132467+0j
[EQUAL] C raw N=4 P=[5, 7, 17, 19] q=1/4 rho=3/4 theta=3/8 k=[1, 2, 1, 2] full Sym
    paths=15552 stats={'nonzero': 32, 'hN_nonzero': 16, 'cmp_edge': 0, 'multirun': 32, 'endpoint_hit': 4, 'pending_hit': 0, 'ghost_needed': 4} memo=829 (16.9s)
    LHS = (418000514841857557799303275/253737008598893103377547264) + (103768172022013560672666475/63434252149723275844386816)*i
    RHS = (418000514841857557799303275/253737008598893103377547264) + (103768172022013560672666475/63434252149723275844386816)*i
    LHS ~ 1.647377011+1.635838187j
[EQUAL] C raw N=4 P=[5, 7, 17, 19] q=4/9 rho=5/6 theta=1/8 k=[2, 1, 3, 1] full Sym
    paths=15552 stats={'nonzero': 24, 'hN_nonzero': 24, 'cmp_edge': 0, 'multirun': 24, 'endpoint_hit': 4, 'pending_hit': 0, 'ghost_needed': 4} memo=690 (11.9s)
    LHS = (10083249536376058206009125/126868504299446551688773632)*sqrt2 + (3500866824204795433735375/14096500477716283520974848)*i*sqrt2
    RHS = (10083249536376058206009125/126868504299446551688773632)*sqrt2 + (3500866824204795433735375/14096500477716283520974848)*i*sqrt2
    LHS ~ 0.1123988048+0.3512200316j
SUMMARY C [('C', True), ('C', True), ('C', True)]
```

### `out_BDE.txt`

```
[EQUAL] B raw+cmp(C={0}) N=2 P=[5, 7, 17, 19, 29] q=1/2 rho=9/10 theta=1/8 k=[1, 1] full Sym
    paths=128000 stats={'nonzero': 2916, 'hN_nonzero': 1596, 'cmp_edge': 2304, 'multirun': 1476, 'endpoint_hit': 480, 'pending_hit': 0, 'ghost_needed': 480} memo=5560 (182.2s)
    LHS = (195772372889513416474507706846184239335060817735/24046747385091623193217907287047579197718583296) + (-7630994504264911221671345513845/4877131396380140400227922593088288)*sqrt2
    RHS = (195772372889513416474507706846184239335060817735/24046747385091623193217907287047579197718583296) + (-7630994504264911221671345513845/4877131396380140400227922593088288)*sqrt2
    LHS ~ 8.139111723+0j
[EQUAL] B raw+cmp(C={0}) N=2 P=[5, 7, 17, 19, 29] q=1/4 rho=3/4 theta=3/8 k=[2, 1] full Sym
    paths=128000 stats={'nonzero': 2034, 'hN_nonzero': 2034, 'cmp_edge': 1536, 'multirun': 594, 'endpoint_hit': 360, 'pending_hit': 0, 'ghost_needed': 360} memo=5291 (135.5s)
    LHS = (124506320404010972500988350174699761238569425/667965205141433977589386313529099422158849536)*sqrt2 + (1500605459323023153745596703396654340798284475/6011686846272905798304476821761894799429645824)*i*sqrt2
    RHS = (124506320404010972500988350174699761238569425/667965205141433977589386313529099422158849536)*sqrt2 + (1500605459323023153745596703396654340798284475/6011686846272905798304476821761894799429645824)*i*sqrt2
    LHS ~ 0.2636043398+0.353008506j
SUMMARY B [('B', True), ('B', True)]
[EQUAL] D N=4 P=[5, 7, 17, 19, 29] patterns per edge=[0, 1, 0, 0] (0=raw,1=cmp) identity perms q=1/2 rho=9/10 theta=1/8 k=[1, 1, 1, 1]
    paths=46080 stats={'nonzero': 56, 'hN_nonzero': 56, 'cmp_edge': 56, 'multirun': 56, 'endpoint_hit': 4, 'pending_hit': 0, 'ghost_needed': 6} memo=4159 (41.7s)
    LHS = (-185308347188188006372823724066545375946609125/144280484310549739159307443722285475186311499776) + (-536107449661809500356488735263260514703125/8015582461697207731072635762349193065906194432)*sqrt2 + (-257947744386357999592086945310061864785790375/144280484310549739159307443722285475186311499776)*i + (-1278218892917239799280954674351774198546875/12023373692545811596608953643523789598859291648)*i*sqrt2
    RHS = (-185308347188188006372823724066545375946609125/144280484310549739159307443722285475186311499776) + (-536107449661809500356488735263260514703125/8015582461697207731072635762349193065906194432)*sqrt2 + (-257947744386357999592086945310061864785790375/144280484310549739159307443722285475186311499776)*i + (-1278218892917239799280954674351774198546875/12023373692545811596608953643523789598859291648)*i*sqrt2
    LHS ~ -0.001378948898-0.001938168143j
[EQUAL] D N=4 P=[5, 7, 17, 19, 29] patterns per edge=[1, 0, 0, 1] (0=raw,1=cmp) identity perms q=1/2 rho=9/10 theta=1/8 k=[1, 1, 2, 1]
    paths=414720 stats={'nonzero': 0, 'hN_nonzero': 0, 'cmp_edge': 0, 'multirun': 0, 'endpoint_hit': 0, 'pending_hit': 0, 'ghost_needed': 0} memo=2558 (283.1s)
    LHS = 0
    RHS = 0
    LHS ~ 0+0j
[EQUAL] D N=4 P=[5, 7, 17, 19, 29] patterns per edge=[0, 0, 1, 0] (0=raw,1=cmp) identity perms q=1/2 rho=9/10 theta=1/8 k=[2, 1, 1, 1]
    paths=46080 stats={'nonzero': 5, 'hN_nonzero': 5, 'cmp_edge': 5, 'multirun': 5, 'endpoint_hit': 0, 'pending_hit': 0, 'ghost_needed': 0} memo=4124 (37.8s)
    LHS = (-983711177457721458220689896129847767396875/375730427892056612394029801360118424964352864)*sqrt2 + (-1872009647640647264816851661192259142128125/375730427892056612394029801360118424964352864)*i*sqrt2
    RHS = (-983711177457721458220689896129847767396875/375730427892056612394029801360118424964352864)*sqrt2 + (-1872009647640647264816851661192259142128125/375730427892056612394029801360118424964352864)*i*sqrt2
    LHS ~ -0.003702595226-0.007046066105j
SUMMARY D [('D', True), ('D', True), ('D', True)]
[EQUAL] E M=3 (J=2,l=1) N=2 P=[5, 7, 17, 19, 29, 31] cmp C={0} on both edges (1 shared + 1 free), identity perms, q=1/2
    paths=155520 stats={'nonzero': 1632, 'hN_nonzero': 192, 'cmp_edge': 1632, 'multirun': 1632, 'endpoint_hit': 0, 'pending_hit': 0, 'ghost_needed': 0, 'orphan_possible': 1440, 'two_orphans_possible': 0} memo=12260 (148.3s)
    LHS = (2404088327633053247159232159809880675892508003447077990742530625/271640777906201146986830757830920299758903182665110442848494288896)
    RHS = (2404088327633053247159232159809880675892508003447077990742530625/271640777906201146986830757830920299758903182665110442848494288896)
    LHS ~ 0.008850248281+0j
[EQUAL] E M=3 (J=2,l=1) N=2 P=[5, 7, 17, 19, 29] raw+cmp both edges, identity perms, q=1/4
    paths=13500 stats={'nonzero': 120, 'hN_nonzero': 120, 'cmp_edge': 0, 'multirun': 0, 'endpoint_hit': 0, 'pending_hit': 0, 'ghost_needed': 0, 'orphan_possible': 0, 'two_orphans_possible': 0} memo=1800 (10.2s)
    LHS = (94544823705684496655786975/45652060821410496167476139568)*sqrt2 + (2892272452816872343308475/45652060821410496167476139568)*i*sqrt2
    RHS = (94544823705684496655786975/45652060821410496167476139568)*sqrt2 + (2892272452816872343308475/45652060821410496167476139568)*i*sqrt2
    LHS ~ 0.002928817879+8.959707087e-05j
SUMMARY E [('E', True), ('E', True)]
```

### `out_F.txt`

```
[EQUAL] F J=2,l=0 (M=2) N=2 P=[5, 7, 17, 19, 29] patterns raw(2 shared) + C={0,1} (2 free labels, may coincide), identity perms, q=1/2
    paths=106580 stats={'nonzero': 564, 'hN_nonzero': 304, 'cmp_edge': 544, 'multirun': 304, 'endpoint_hit': 24, 'pending_hit': 0, 'ghost_needed': 24, 'orphan_possible': 500, 'two_orphans_possible': 20} memo=4058 (95.3s)
    LHS = (4767242227143646527895411930608633714932384064806481309029/2315678508046403540055538620391948810533854200666905807360) + (-6928442993113536131062419419413/13005683723680374400607793581568768)*sqrt2
    RHS = (4767242227143646527895411930608633714932384064806481309029/2315678508046403540055538620391948810533854200666905807360) + (-6928442993113536131062419419413/13005683723680374400607793581568768)*sqrt2
    LHS ~ 2.057927131+0j
[EQUAL] F J=2,l=0 (M=2) N=4 P=[5, 7, 17, 19, 29] pattern seq [C01,raw,raw,C01], identity perms, q=1/4
    paths=103680 stats={'nonzero': 304, 'hN_nonzero': 64, 'cmp_edge': 304, 'multirun': 304, 'endpoint_hit': 0, 'pending_hit': 24, 'ghost_needed': 16, 'orphan_possible': 240, 'two_orphans_possible': 0} memo=5676 (106.3s)
    LHS = (103242156580797434491485698493404897149632987716156679508985/3794007667583227560026994475650168931178666722372658474778624)
    RHS = (103242156580797434491485698493404897149632987716156679508985/3794007667583227560026994475650168931178666722372658474778624)
    LHS ~ 0.02721189982+0j
SUMMARY F [('F', True), ('F', True)]
```

### `out_2groups.txt`

```
[EQUAL] two big groups [[5, 7, 17], [11, 19, 23]] N=2 q=1/2 rho=9/10 theta=1/8 k=1: nonzero physical paths=144  (8.5s)
    LHS = (47838947920237520898775/17049841958960727688328)
    RHS = (47838947920237520898775/17049841958960727688328)
    LHS ~ 2.805829405+0j
[EQUAL] two big groups [[5, 7, 17], [11, 13, 19]] N=2 q=1/4 rho=3/4 theta=3/8 k=2: nonzero physical paths=144  (9.1s)
    LHS = (112496611438713532815785/60486908118762618754704)
    RHS = (112496611438713532815785/60486908118762618754704)
    LHS ~ 1.859850585+0j
[EQUAL] two big groups [[5, 7, 17], [11, 13, 19]] N=2 q=4/9 rho=5/6 theta=1/8 k=3: nonzero physical paths=144  (9.8s)
    LHS = (16559539870364223377645/20162302706254206251568)
    RHS = (16559539870364223377645/20162302706254206251568)
    LHS ~ 0.821311936+0j
control own_D (group-g memory translated by k*s_g instead of k*D): equal=False  RHS-LHS ~ -0.209881+0j
```

### `out_controls_A1.txt` (the trailing traceback is my own guard refusing ρ = 4/5, which violates the paper's ρ² > √q; ρ = 19/20 was run instead)

```
case A1: LHS ~ 12.8377479206+0j; unperturbed RHS equal: True
  control no_bfact                : RHS ~ 12.8377479206+0j   equal=True   RHS-LHS ~ 0+0j
  control fresh_repeat            : RHS ~ 43.2807431419+0.578410368833j   equal=False   RHS-LHS ~ 30.443+0.57841j
  control ghost_repeat            : RHS ~ 13.0869192716+0j   equal=False   RHS-LHS ~ 0.249171+0j
  control mu_not_mut              : RHS ~ 8.1645868652+0j   equal=False   RHS-LHS ~ -4.67316+0j
  control no_rho_iv               : RHS ~ 12.8205296509+0j   equal=False   RHS-LHS ~ -0.0172183+0j
  control q0_bulk                 : RHS ~ 12.2509851181+0j   equal=False   RHS-LHS ~ -0.586763+0j
  control baseline_internal_only  : RHS ~ 13.4724525599+0j   equal=False   RHS-LHS ~ 0.634705+0j
  control prom_new                : RHS ~ 12.8377479206+0j   equal=True   RHS-LHS ~ 0+0j
  control no_pnotD                : RHS ~ 12.8377479206+0j   equal=True   RHS-LHS ~ 0+0j
  control rho=19/20               : RHS ~ 12.8377479206+0j   equal=True   RHS-LHS ~ 0+0j
Traceback (most recent call last):
  File "/tmp/oaimath/011/scripts_memory/controls.py", line 23, in <module>
    kw2 = dict(kw); kw2['rho'] = Fr(fl[4:]); t = Toy(**kw2)
                                                 ^^^^^^^^^^
  File "/tmp/oaimath/011/scripts_memory/model.py", line 19, in __init__
    assert F.approx(self.sq).real < float(self.rho)**2, "need rho^2 > sqrt q"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: need rho^2 > sqrt q
```

### `out_controls_C1.txt`

```
case C1: paths=15552 stats={'nonzero': 636, 'hN_nonzero': 228, 'cmp_edge': 0, 'multirun': 636, 'endpoint_hit': 256, 'pending_hit': 80, 'ghost_needed': 336, 'orphan_possible': 80, 'two_orphans_possible': 0}
  LHS = (167047058786631979736402711915/3044844103186717240530567168) + (-131709697146489965111525/1321546919785901580091392)*sqrt2
  LHS ~ 54.721324674+0j; unperturbed RHS equal: True
  control mu_not_mut              : RHS ~ 20.3678542429+0.0246493833262j   equal=False   RHS-LHS ~ -34.3535+0.0246494j
  control no_rho_iv               : RHS ~ 54.5901930392-0.0080286293893j   equal=False   RHS-LHS ~ -0.131132-0.00802863j
  control q0_bulk                 : RHS ~ 52.3157161032+0j   equal=False   RHS-LHS ~ -2.40561+0j
  control baseline_internal_only  : RHS ~ 57.4283320549+0j   equal=False   RHS-LHS ~ 2.70701+0j
  control prom_new                : RHS ~ 54.721324674+0j   equal=True   RHS-LHS ~ 0+0j
  control no_pnotD                : RHS ~ 54.721324674+0j   equal=True   RHS-LHS ~ 0+0j
  control rho=19/20               : RHS ~ 54.721324674+0j   equal=True   RHS-LHS ~ 0+0j
```

### `out_controls_F1.txt`

```
case F1: paths=27380 stats={'nonzero': 564, 'hN_nonzero': 304, 'cmp_edge': 544, 'multirun': 304, 'endpoint_hit': 24, 'pending_hit': 0, 'ghost_needed': 24, 'orphan_possible': 500, 'two_orphans_possible': 20}
  LHS = (4767242227143646527895411930608633714932384064806481309029/2315678508046403540055538620391948810533854200666905807360) + (-6928442993113536131062419419413/13005683723680374400607793581568768)*sqrt2
  LHS ~ 2.05792713072+0j; unperturbed RHS equal: True
  control no_ban                  : RHS ~ 2.10456087634+0j   equal=False   RHS-LHS ~ 0.0466337+0j
  control free_mut                : RHS ~ 2.06363029499+0j   equal=False   RHS-LHS ~ 0.00570316+0j
```

### `out_controls_F1b.txt`

```
case F1: paths=27380 stats={'nonzero': 564, 'hN_nonzero': 304, 'cmp_edge': 544, 'multirun': 304, 'endpoint_hit': 24, 'pending_hit': 0, 'ghost_needed': 24, 'orphan_possible': 500, 'two_orphans_possible': 20}
  LHS = (4767242227143646527895411930608633714932384064806481309029/2315678508046403540055538620391948810533854200666905807360) + (-6928442993113536131062419419413/13005683723680374400607793581568768)*sqrt2
  LHS ~ 2.05792713072+0j; unperturbed RHS equal: True
  control no_bfact                : RHS ~ 2.05828707771+0j   equal=False   RHS-LHS ~ 0.000359947+0j
  control prom_new                : RHS ~ 2.05792713072+0j   equal=True   RHS-LHS ~ 0+0j
  control no_pnotD                : RHS ~ 2.05792713072+0j   equal=True   RHS-LHS ~ 0+0j
```

### `ey_control.py` / `incl_excl.py` output

```
sampled 16 paths (152 nonzero of 432): mismatches = 0
(3.41) checked on 420 random realized paths with A<=7 potential addresses: failures = 0
(3.42) sum_{r(pi)=r}|mu(pi)| == e_r(0..A-1) <= A^{2r}, and #addresses <= 2r: verified for A<=7
negative control (drop (|B|-1)! in mu): failures = 80/200
```

### `out_controls_C1_killed_partial.txt` (first C1 control run, stopped because `ghost_repeat` at N=4 explodes the state space; its single completed line is consistent with the rerun)

```
case C1: paths=15552 stats={'nonzero': 636, 'hN_nonzero': 228, 'cmp_edge': 0, 'multirun': 636, 'endpoint_hit': 256, 'pending_hit': 80, 'ghost_needed': 336, 'orphan_possible': 80, 'two_orphans_possible': 0}
  LHS = (167047058786631979736402711915/3044844103186717240530567168) + (-131709697146489965111525/1321546919785901580091392)*sqrt2
  LHS ~ 54.721324674+0j; unperturbed RHS equal: True
  control no_bfact                : RHS ~ 54.721324674+0j   equal=True   RHS-LHS ~ 0+0j
```
