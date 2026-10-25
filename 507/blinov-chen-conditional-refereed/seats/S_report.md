VERDICT: HOLDS WITH FIXES — no MUST-FIX. All three of the panel's claims, and the Wróblewski-set addendum, survived every attack I could make. The fixes are in wording, scope and credit. One addendum: our own argument gives slightly more than we claim (finding 4).

Per-claim verdicts
- Claim 1 (seat G's sharpened proportional-pair bound): HOLDS.
- Claim 2 (the 2,921-element set with max 178,077, k′ = 356,155): HOLDS WITH FIXES. Every fix is a text substitution or a provenance statement (findings 1, 2).
- Addendum: the Wróblewski set (max 137,692, k = 275,385, tags 0, 15, 16, 21, 22): HOLDS WITH FIXES. The fixes are the same kind as claim 2's. Tag span 22 is harmless, because every tag lies below the first norm word, 37.
- Claim 3 (lift box N = hqB^u, η = 2/(X+2)): HOLDS WITH FIXES.
  - The arithmetic is exact at all three k: 2/74,806,940, 2/65,176,382 and 2/50,395,469.
  - The steps in §§6–8 that depend on N all go through for N = hqB^u.
  - "sup 2/(183k+8)" and "u−1 is insufficient" are true only relative to stated estimates. Each can be beaten inside our own argument (findings 3, 4).

Seat S, hostile referee of the panel's own claims. Sources read:
- OpenAI TeX §§6–8 (`/tmp/oaimath/191/paper/src/build/sections/0{6,7,8}-*.tex`) and §2's lattice hypotheses.
- Blinov `patches/reserved-tags.patch` (sha256 a177ca56…), `notes/sphere-packing.tex` §sec:five and §sec:reserved, `lean/FiveTagged.lean`, `FiveFiniteTheorem.lean`, `FiveTags.lean`, `ReservedPacking.lean`.
- Chen `chen191.pdf` (sha256 bc03013e…). I rendered p. 4 to confirm the quoted §2.4 text.
- Seat G's report.
- The coordinator's `compute/ours.py`.

Set files checked:
- `packing178077.txt`: sha256 c36f2b7e…
- `wroblewski2921.txt`: sha256 bd40ac29…

No script under `src/` was executed.

---

## Findings

### 1. SHOULD-FIX (claim 2 and Wróblewski addendum). Blinov's written proof of the packing, and all his formal certificates for it, are specific to his set. Our substitution needs its own AP-freeness proof and a disclosed list of text replacements.

Blinov, patch to §3 (just before eq. norm:matching): "No carries in base three give c(x)+c(y)=2c(z) only when x=y=z". After it: "Lean proves the exact cutoff counts, selection, bounds, injections, matching and both tag exclusions; no large shift of the norm supports is used."

- **The AP-freeness argument does not transfer.** Neither of our sets is a base-3 {0,1} set, so that argument proves nothing about them.
- **The formal check does not transfer.** `lean/ReservedPacking.lean` hard-codes `packingSize := 408781`, `binaryWord 12`, `tag_values … = 0,1,3,4,9` and the interval `[10,204391)`. `certificates/reserved.json` is the same. None of it covers our sets.
- **What our page must contain instead:**
  - (a) An AP-freeness proof.
    - For the 178,077 set it is two lines. Write x = 163·bt(a) + l with l ∈ O23 ⊂ [0,81]. Since l + l′ ≤ 162 < 163, x + y = 2z splits into bt(a) + bt(a′) = 2bt(a″) and l + l′ = 2l″.
      - The first equation has no base-3 carries, so a = a′ = a″.
      - O23 is 3-AP-free, so l = l′ = l″.
    - For the Wróblewski set the proof is the exhaustive computation below, or Wróblewski's own construction proof.
  - (b) A statement that Blinov's Lean certificates do not apply. Our sets are certified only by our scripts.
  - (c) The text substitutions:
    - in the patch: "twelve binary coordinates", "All words have centered squared norm 12" (decorative; delete it), "#{c(x)<10}=5", "#{c(x)<204 391}=2 921", "(t_0,…,t_4)=(0,1,3,4,9)", "k=2(204 391)−1=408 781";
    - in Lemma orb:tagged-moment: "put a=t_s<10", "For degrees below 10", "Since a<10 and k≥20, we have v≥10>a";
    - in Chen §2.2: "takes 2920 … to 204390", "The words below ten are 0, 1, 3, 4, 9", "x, y ∈ A ∪ {0, 1, 3, 4, 9}";
    - in Chen §2.4: "Below degree ten the A polynomials have digits 1, r, r, …" and "b ≤ a < 10".

  Every "10/ten" above should become T, the first norm word: T = 10 for the 178,077 set and T = 37 for the Wróblewski set.
- **Nothing else depends on the set's structure.** I traced every use. The coefficient bound A₀ = 6k²P only counts position pairs. The carry bound 47/50, θ ≤ 1/2, B ≫ L₃ and the zero-count are all set-independent. The Lean finite theorem (`TaggedData`) asks only for a < d (the tag span) and 2d ≤ k, which hold with d = 10 and d = 23.

### 2. NIT (claim 2 and addendum). The tag exclusion silently needs 0 ∈ set. State it.

Blinov, §3 patch: "Every tag is the encoding of another word of the same cube. Hence t_s+i_a+ℓ_b=k−1 would force the tag word to equal a norm word".

Row 1 carries residue 1 at position 0. That position is a designated position in row 1 but is not one of the five row-2 tags. It is excluded from the k−1 coefficient only because 0 is itself a member of the AP-free set.

As a mutation, I shifted the set by +1, which keeps it AP-free. Position-0 triples then sum to k−1: 9 of them for the 178,077 set and 22 for the Wróblewski set. The checker reports "matching property / tag exclusion FAILS".

Both of our sets contain 0, so the claims hold. The written statement should say: "the set contains 0; the tags are its five smallest elements; all of them lie below the first norm word T".

### 3. SHOULD-FIX (claim 3, wording). The sup and "u−1 is insufficient" are properties of the estimates, not of the method.

- **Within the claim-1 pair bound plus the printed triple bound, the sup is 2/(183k+8). It is not attained.**
  - Write N = hq·K with K ≍ r^κ, κ real.
  - The pair term has r-exponent γ + 123k + 3 − 1.5κ, and X = 60k + 3 + 1.5κ.
  - So X > 183k + 6 + γ and η = 2γ/(γ+X) < 2γ/(183k+6+2γ), which increases to 2/(183k+8) as γ → 1.
  - Values of the sup:
    - k = 408,781: 2/74,806,931;
    - k′ = 356,155: 2/65,176,373;
    - k = 275,385: 2/50,395,463.
- **"u−1 is insufficient" holds only inside the family N = hqB^u.** At u−1 the pair exponent is γ > 0 for k = 408,781 and k′ = 356,155, and about 4 for k = 275,385 (verified). But the finer box N = hq·B^{u−1}·r^j works with j = 1, 1, 3 respectively:
  - X = 183k + 7.5 at both k = 408,781 and k′ = 356,155;
  - X = (100,790,925)/2 at k = 275,385;
  - in every case η is marginally larger than claimed.
- **γ = X/(X+1) is also not optimal.** Any γ < 1 works, and η → 2/(X+1).
- **The binding loss is the residue-blind lift count.** Pr(u=v) alone is at least r^{−5}M^{−k}s^{−1}(hq/N)³. That is smaller than the claim-1 upper bound by a factor of about r⁵(hq)³ = r^{126k+5}. So "2/(183k+8)" must not be published as a ceiling of the construction. Say instead "of these two estimates".

### 4. NIT (claim 3, an improvement left on the table — optional, rigorous). The (1,2)-minor forces equal labels. That adds a factor r^{−5} to claim 1, and then u−1 suffices.

Step (α) of claim 1 uses only the minor c₁c′₃ − c₃c′₁. The minor c₁c′₂ − c₂c′₁ ≡ 0 (mod h) also holds on the event π(u)=π(v), and it gives more:
- Below the first norm word T, the row-1 digits are (1, r, …, r) for every label. So c₁ ≡ c′₁ (mod B^T), and both are units.
- Hence c′₂ ≡ c₂ (mod B^T). Row-2 digits lie in [1, r] ⊂ [0, B), so the row-2 digits below T agree.
- Those digits include the five tag values, so ξ = ξ′.
- Then c′₁ = c₁, c′₂ = c₂, and (α) gives c′₃ ≡ c₃, i.e. c′ = c.

Therefore Pr(π(u)=π(v)) ≤ 2C·r^{−5}·M^{−k}·s^{−1}·(hq)⁶N^{−3}. The pair exponent drops by 5, the sup becomes 2/(183k+3), and u−1 suffices at all three k:

| k | u | η = 2/(X+2) |
|---|---|---|
| 408,781 | 5,586,674 | 2/74,806,931 |
| 356,155 | 4,867,452 | 2/65,176,373 |
| 275,385 | 3,763,595 | 2/50,395,460 |

These numbers come from `claim3_extra.py`.

I checked the label-forcing step exhaustively in `minor12.py`:
- 87,990 distinct label pairs, with real tag layouts T = 10 and T = 37: zero pairs have the minor ≡ 0 (mod B^T).
- Mutation dropping one tag: 1,260 violations (= 60·C(7,2), as expected).

The panel may adopt this or leave it. It is not an error in our claim.

### 5. NIT (claim 3). "the bad-triple term is unchanged (it does not depend on N)" — it depends on N through (log 2N)².

The term is (log 2N)²·r^{2γ−2}·O(1). Since u = O_k(1), log 2N = O_k(log r). Write "unchanged up to the logarithm".

### 6. NIT (credit and provenance).

- **Credit.** Common brief: "(a Salem–Spencer set)". The base-3 {0,1} construction is Erdős–Turán (1936) (W's correction). "Salem–Spencer set" is acceptable only as a generic name for 3-AP-free sets.
- **Provenance of the Wróblewski file (independently confirmed).** The file reproduces exactly from the stated recipe:
  - the 216th roots of unity mod 3889, mapped by x ↦ 1331x + 640 mod 3889, in blocks 3889·b for b ∈ {1,2,4,8,9,13,21,23,26,27,30,32,35,36};
  - the file is the first 2,921 of these 3,024 elements, shifted down by 3,890.
  - The full 3,024-element set and the 14-element block index set are each 3-AP-free.
  - The file's window has the minimal span among all 2,921-element windows (137,692).
  - The reflected window has tags 0, 2, 11, 19, 35 with T = 37, so it also works, with the same k.

### 7. NIT (claim 2, Chen port only). Chen's s₀ is not portable verbatim.

Chen's s₀ = 102195 = (k−1)/4. At k′ = 356,155, (k′−1)/4 = 89,038.5 is not an integer. If anyone ports Chen's (9) to a new set, s₀ must be re-chosen; any integer s₀ with 3s₀ < k−1 works, as seat G found. This does not affect claim 3, which uses its own N.

### 8. NIT (instruments). The coordinator's `ours.py` is circular, and my first tag-minor check could not fail.

- `ours.py` defines β from the same formula it then asserts (X == 60k+9u+3). It can only check self-consistency. My `claim3.py` instead derives every exponent from the parameter definitions: B, h, τ, q, the lower bound on s, M and N. It agrees.
- My first run of `tagU.py` drew uniform labels. With those, the first differing coordinate is almost never s ≥ 2, so the "tag above a norm word" mutation passed vacuously (max a seen = 3 and 16). I rebuilt it to force each s ∈ {0,…,4}. The mutation then fails: 4,011 and 3,946 violations out of 20,000 trials.

---

## Claim 1 in detail (HOLDS)

Each question in the brief:

- **Does c′₁ fix c′₃ uniquely?** Yes, given c. π(u)=π(v) ⇒ every 2×2 minor of (u|v) vanishes over ℤ, hence mod h. The minors of (G_hc | G_hc′) are Λ²(G_h) applied to those of (c|c′), and Λ²(G_h) is invertible since Λ²(G_h⁻¹) is its inverse. So c₁c′₃ ≡ c₃c′₁ (mod h). Since c₁ is a unit (its lowest digit is 1), c′₃ is a single residue mod h. Third-row digits lie in [1, L₃] ⊂ [0, B−1], so Σd_vB^v < h, and at most one digit vector of the M^k gives that residue.
- **What if c′₁ is not a unit?** Irrelevant: only c₁ is inverted. (It is a unit anyway.)
- **Independence and equal labels.** Given (G_h, V) and the label ξ′, the k third-row digits of v are fresh and uniform on M^k vectors. They are independent of everything else, including when ξ′ = ξ. So Pr(α | G_h, V) ≤ M^{−k}.
- **Is π(u)=π(v) contained in (α)∧(β), including u = v?** Yes.
  - mod q: u_q ≠ 0 because 0 ∉ V (‖a₁‖_q > 3Hw), so v_q ∈ F_q·u_q, a line.
  - V = G_q(a+S) is a cap, so that line holds ≤ 2 points of V, and Pr(β | V) ≤ 2/s.
  - u = v gives c = c′ and v_q = u_q, both in the event.
- **Is the conditioning legitimate?** Yes. Given (G_h, V), the mod-h data (labels, digits) and the mod-q data are independent. Given all residues, Pr(lifts proportional) ≤ (total proportional pairs in 𝓑²)/(N/hq)⁶ ≤ C N³(hq/N)⁶, uniformly. So Pr ≤ Pr(α)Pr(β)·C(hq)⁶N^{−3} ≤ 2C M^{−k}s^{−1}(hq)⁶N^{−3}.
- **The constants.** C = 6750 (Chen (B16)). M^k ≥ (2B)^{k/2}, because M² = 160000k⁴r⁶ ≥ 2B. s ≥ q²/(8000h²).

Toy confirmations, all exact in Fractions:

- **`prop_toy.py`.** Blinov-shaped toy: B = 11, k = 2, h = 121, r = 2, M = 4, L₃ = 8 < B, rows 1–2 deterministic per label, G_h ∈ SL₃(ℤ/121), slab cap V with q = 7, s = 21, N = hqK, K ∈ {1, 2, 3}. All outcome pairs and all lift pairs are enumerated. 5/5 base runs PASS.
  - With one label the bound is tight to a factor 2: truth/bound = 0.500.
  - Mutations that must fail, all rejected:
    - L₃ = 24 > B: Pr(α) = 97/10368 > 1/144.
    - Stale third row (a function of the label): Pr(α) = 1/4 > 1/16, and the FINAL inequality fails, 1.19e-2 > 5.95e-3.
    - Non-cap V with 3 points per line through 0: Pr(β) = 1/7 > 2/21.
    - 0 ∈ V: Pr(β) = 67/441 > 2/21.
    - Claim M^{−(k+1)} in place of M^{−k}, at K = 1 and K = 2: FINAL fails at truth/bound = 2.0.
  - Disclosed blind spot: in this toy every proportional pair has u = v, so the containment check over distinct outcomes is vacuous. A wrong-(α) mutation passed here. That is why `prop_alg.py` exists.
- **`prop_alg.py`.** Exhaustive at h = 9, q = 7.
  - (1) Over all pairs (c, c′) ∈ ((ℤ/9)³)², if minors(G c | G c′) ≡ 0 then minors(c|c′) ≡ 0. That gives 9,153 implications and 0 violations. A singular G must break it: 67,392 violations.
  - (2) Over all 40,936 ordered proportional pairs u ≠ v in [0,63)²×[63,126): (α) holds on 18,197 / 19,221 checks (c₁ a unit) and (β) on 37,129 checks (u_q ≠ 0), with 0 violations. The wrong (α) "c′₃ ≡ c₃" must break it: 15,082 violations.

## Claim 2 and the Wróblewski set in detail

`claim2.py` checks each of the 178,077 set (generated independently and confirmed equal to the file) and the Wróblewski file:
- size 2,921, distinct, contains 0;
- 3-AP-free, by an exhaustive check over all pairs;
- tags = the five smallest, increasing, and all below the first norm word T;
- 2,916 norm words;
- k = 2·max+1, and every designated position lies in [0, k);
- injective within each row, with tags disjoint from norm positions;
- a full enumeration of every (row-1 designated position, row-2 designated position) pair, testing whether k−1−p₁−p₂ is a row-3 position.

Results:

| set | max | k | tags | T | matched triples | tag-involved triples | unmatched norm triples |
|---|---|---|---|---|---|---|---|
| 178,077 set | 178,077 | 356,155 | 0, 1, 3, 7, 8 | 10 | exactly 2,916 | 0 | 0 |
| Wróblewski set | 137,692 | 275,385 | 0, 15, 16, 21, 22 | 37 | exactly 2,916 | 0 | 0 |

For both sets, the fresh position v = k−1−a > a holds for every tag, and k ≥ 2·span.

Mutations, all rejected (output in this session's log):
- inserting a 3-AP: 56 or 84 unmatched triples plus a tag triple, "3-AP found";
- a tag placed on a norm word;
- a tag above a norm word;
- 0 removed (finding 2).

**Tagged-moment lemma (`tagU.py`), with the real position layout.** r = 37, 20,000 label pairs with each first-differing coordinate s forced. In every trial: U_j = 0 for j < a, U_a = Q_μ,a − Q_λ,a ≠ 0, and |U_a| < r. The trials reached a up to 8 and a up to 22, with 0 violations. The mutation with a tag above a norm word gives about 4,000 violations.

**Why tag span 22 is harmless.** Blinov's argument needs three things:
1. a < T, so that the row-1 coefficients 0…a are (1, r, …, r) for both labels. This holds: 22 < 37.
2. v = k−1−a ≥ k−23 > a ≥ j, so the fresh digit is outside the Schur prefix.
3. θ ≤ 1/2, so Σ_{j≤a}θ^j ≤ 1 for any a.

None of these depends on a ≤ 9. The Lean hypotheses are a < d and 2d ≤ k, and they hold with d = 23.

## Claim 3 in detail

**Exact bookkeeping (`claim3.py`).** All exponents are derived from the definitions:
- B ∈ (40000k⁴r⁶, 80000k⁴r⁶], h = B^k, τ ∈ [B^{k−1}/3, B^{k−1}/2];
- q ∈ (h⁶, 2h⁶], s ≥ q²/(8000h²), M = 400k²r³;
- N = hqB^u, a_r = r^γ√(N³/τ).

Results:
- pair term r-exponent = γ + 123k + 3 − 9u;
- triple term = 2γ − 2, times (log)²;
- X = 60k + 9u + 3;
- η = 2γ/(γ+X) = 2/(X+2) at γ = X/(X+1).

| k | u | 3u − (41k+2) | η | approx. | pair exponent |
|---|---|---|---|---|---|
| 408,781 | 5,586,675 | 2 | 2/74,806,940 | 2.6735e-8 | γ − 9 |
| 356,155 | 4,867,453 | 2 | 2/65,176,382 | 3.0686e-8 | γ − 9 |
| 275,385 | 3,763,596 | 1 | 2/50,395,469 | 3.9686e-8 | γ − 6 |

All three match the coordinator's numbers. Blinov's formula at k = 275,385 gives 1/34,285,435, also matching.

"3u ≥ 41k+2" is the exact integer condition for every γ ∈ (0,1), not only for γ near 1.

Mutations, each rejected:
- u−1: the pair term does not decay, and the stated numbers mismatch;
- X+1;
- η = 2/(X+1).

**§§6–8 with the smaller N.**
- hq | N, so the lifting identity holds.
- λ₃(Λ) ≤ E ≤ h < 4N, so lat:fixed-det applies with X = 4N. Its only hypotheses are X ≥ 2 and λ₃ ≤ X; Chen's (B4) radii lie in [1, 64X].
- Zero-determinant count:
  - row counts need only λ₂ ≤ 4N when the count is nonzero;
  - shells run from 1 to |x| ≪ N², O(log 2N) of them;
  - the affine case uses R > H/2 = h, which is independent of N;
  - the equal-pair cases use |x| ≥ q, and are vacuous if that is out of range.
  - Nothing needs N ≫ q or N ≫ h.
- log 2N = O_k(log r).
- The area bound τ/(16N³) and n_r²Δ ≥ r^{2γ}/64 are unchanged.
- Two-sided bounds: a_r ∈ (√2·r^γB^β, 2^{1.5}√3·r^γB^β] with β = (20k+3u+1)/2. With the B window this gives A_k r^α ≤ n_r ≤ D_k r^α. A non-integer α = γ + X is harmless for the interpolation via primes r ≡ 1 (mod 3) in (m, 2m].

## What I checked and how

Everything is in `/tmp/oaimath/191b/seats/S_work/`. Every run used `bash -c 'ulimit -v 8000000; exec timeout … nice -n 19 python3 -I <script> …'`, single-threaded. No script from `src/` was run.

- `claim2.py <bt163 | file:PATH> [ap | tagonnorm | tagabovenorm | l0missing]`: packing, matching and tag exclusion.
- `tagU.py <set> [tagabovenorm]`: low coefficients of the tag minor.
- `claim3.py [uminus1 | Xoff | etaoff]`: exact exponent arithmetic.
- `claim3_extra.py`: finding 4's numbers.
- `minor12.py <tags> <T> [droptag]`: finding 4's label-forcing step.
- `prop_toy.py <seed> <K> <labels> [bigL | stale | noncap | zeroinV | tightclaim | wrongalpha]`: claim-1 probability, exact. Mutation log in `mut_toy.log`.
- `prop_alg.py <seed> [singular | wrongalpha]`: claim-1 algebraic containment, exhaustive.
- `wrob_recon.py`: provenance of the Wróblewski file and minimal-window search.
- `chenp-04.png`: rendered Chen p. 4.

## What I did NOT check

- **The rest of Blinov's construction.** I did not check the CGLV 18-form identity, the 9-node descent, or the "J ⇒ F_{k−1} = 0" carry bound. I relied on Blinov's text and Lean statements for these (seats P/W).
- **The Lean files.** I read the Lean hypotheses but did not build any Lean.
- **Prior art.** I did not check whether the 178,077 product set (163·bt(a) + O23) or the Wróblewski table appears in the literature with prior credit (seat W).
- **Finding 4's further heuristic.** I did not attempt the per-residue lift count. The ceiling it suggests near 2/(57k+3) is unproved and must not be stated as a result.
- **Explicit constants for claim 3.** I did not redo Chen-style explicit constants (c, N₀) for any of the new parameter choices. Our claims are asymptotic only. Any explicit-constant statement would need its own pass.
