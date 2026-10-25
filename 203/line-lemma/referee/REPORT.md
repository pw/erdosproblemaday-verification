# Hostile referee report: Erdős #203, the Quotient Lemma (lines / coarse tori)

**VERDICT: HOLDS WITH FIXES.**

The mathematics is right. I re-derived every step of the Quotient Lemma, checked the line, coarsening and torus formulas by direct enumeration with 2^k3^ℓ mod p (never through u, v), and re-verified all 33 pools. The claimed exclusions are all true.

I also found that they need no solver at all. In direction (1,1), one averaging argument over 30 cells mod 60 excludes all 26 periods ≤ 65,520 with density ≥ 1 and all five open pools, 720720 included (finding 5).

What does not hold is several of the written statements about the computations. Fix those before publishing:
- "every direction" is false;
- "worst case ≈ 0.93" is false;
- "proven optimal values" is false;
- MILP and brute force are described as cross-checks but were never run on the published rows;
- 110880 is missing from the table;
- the decorrelated solver failed to confirm 166320 at exact M;
- there is no statement of scope (pure coverings only).

Snapshot: 2026-10-14 ~10:40Z. The batches were still writing during the review (55440 had 14 of 16 rows, 65520 had 5 of 16), and table.py and linelemma.py were edited while I worked. Row counts below are as of that time.

---

## Findings

**1. FIX: the claim "EVERY direction" is false.**
Quoted: *"the line instance excludes N in EVERY direction tested (16 directions), with proven optimal values V well below 1 (worst case ≈ 0.93, best ≈ 0.53)"* and *"for N ≤ 65,520 in EVERY direction tested"*.

- **55440, three directions cannot exclude it.** Each has a re-counted witness with V ≥ 1:
  - (0,1) is OPTIMAL with V = 1.0274;
  - (1,0) has V ≥ 1.0637;
  - (2,3) has V ≥ 1.0301.
- **Undecided directions** (best < 1 ≤ bound):

  | N | direction(s) | bound |
  |---|---|---|
  | 30240 | (2,3) | 1.0569 |
  | 36960 | (2,3) | 1.0295 |
  | 45360 | (2,3) | 1.0595 |
  | 50400 | (1,−1), (3,1), (2,3) | — |
  | 55440 | (1,−1), (2,1), (1,2), (3,1) | — |
  | 60480 | (2,3) | 1.0623 |
  | 65520 | (1,−1) | 1.0327 |

- **Totals over 409 rows with N ≤ 65,520:** 354 are OPTIMAL with V < 1, 36 are bound-only < 1 (time-limited, not "optimal"), 16 are undecided, and 3 have V ≥ 1.
- **Worst excluding value is 0.9947, not ≈ 0.93.** Examples: 55440 (3,2) OPTIMAL 1313/1320; 25200 (3,1) bound-only 0.9919; 39600 (2,3) OPTIMAL 0.9867; 50400 (2,−3) OPTIMAL 0.9853. Best is 0.5229 (51480, (1,1)).
- **What is true:** every one of the 26 periods has at least one excluding direction, and (1,1) excludes all of them.
- **Restate as:** "in at least one direction (in fact always (1,1))", with the per-direction table shown honestly.

**2. FIX: TABLE.md does not exist, and table.py crashed as shipped.**
- There is no `lines/TABLE.md`.
- `table.py` died at line 7 with `ValueError: invalid literal for int() with base 10: '110880_first3'`. It was patched during the review to skip non-numeric names.
- The patched version runs, but see finding 3.

**3. FIX: 110880 is excluded but absent from the table, and its stored verdict contradicts itself.**
- The patched table skips `ll_110880_first3.jsonl`, and there is no `ll_110880.jsonl`, so 110880 does not appear.
- In that file, the decisive (1,1) row has bound 5977/7392 = 0.8086 < 1 but carries the stale verdict *"UNDECIDED (best 0.6790 < 1 but bound 0.8086)"*. That string comes from an earlier code version.
- The exclusion itself is real. In `milp_110880.jsonl`, CP-SAT at 1200 s gives bound 44827/55440 = 0.8086, and HiGHS gives dual bound 101623/110880 = 0.9165.
- Regenerate the row, or better, use finding 5.

**4. FIX: at exact M the open pools rest on single time-limited CP-SAT bounds, and the second solver disagreed on 166320.**
- `milp_166320.jsonl`: HiGHS dual bound `"4825/4158"` = 1.160, `"agrees_cpsat": false`, `"excludes": false`.
- 221760, 332640 and 720720 have no MILP result. 720720's only evidence is one 600 s CP-SAT bound (0.9039) at Mp = 55440.
- As claims this is the weakest part of the bundle, and finding 5 makes it unnecessary.

**5. NOTE (strong, in the claim's favour): small certificates, and a solver-free proof, for every pool.**

*Coarse M = 60.* Coarsening direction (1,1) to M = 60 is a legitimate instance by the coarsening rule, which I verified. Every open pool then has an exactly-solved V < 1:

| N | V at M = 60 (CP-SAT OPTIMAL) | time |
|---|---|---|
| 110880 | 0.7556 | ≤ 3 s |
| 166320 | 0.7788 | ≤ 3 s |
| 221760 | 0.7610 | ≤ 3 s |
| 332640 | 0.7954 | ≤ 3 s |
| 720720 | 0.8424 | ≤ 3 s |

These were confirmed three ways:
- by HiGHS on my own formulation (i_p from ord_p(6) on the actual prime, no symmetry fixing): the feasibility model "W ≥ 1 on every cell" is INFEASIBLE, and the max-z dual bounds match within the 1e-4 gap;
- by my own branch-and-bound, which reports INFEASIBLE in ≤ 17 nodes;
- that branch-and-bound was controlled: it returns FEASIBLE on known-feasible instances (an exact 2-D partition, and the real 110880 (0,1) instance at 85,622 nodes) and INFEASIBLE on known-infeasible ones.

*The one-shot proof.* The tree has 17 nodes because one averaging step does all the work:
- In direction (1,1), 6 ≡ 1 (mod 5), so prime 5 has i = 4 and w = 1: it kills whole lines k − ℓ ≡ c₅ (mod 4).
- 6 ≡ −1 (mod 7), so prime 7 has i = 3 and w = 1/2.
- Translations act transitively on the pairs (c₅ mod 4, c₇ mod 3), by CRT, so take c₅ = c₇ = 0.
- Let T = {τ mod 60 : 4 ∤ τ, 3 ∤ τ}, so |T| = 30. Some cell of T has W ≤ avg_T W ≤ B, where
  B = Σ_{p≠5,7} w′_p · max_c |T ∩ (c mod i′_p)| / 30, with i′_p = gcd(i_p, 60) and w′_p = i′_p / e_p.

Exact values of B:
- 0.6854 (5040), 0.7365 (25200), 0.8344 (55440), 0.7821 (65520);
- 0.8490 (110880), 0.8682 (166320), 0.8541 (221760), 0.8835 (332640);
- **11255/12012 = 0.9370 (720720)**;
- all 26 periods ≤ 65,520: B ≤ 0.8344.

I computed B twice, once via sympy n_order and once via linelemma's (u,v) instance; both agree. The exact M = 60 optimum V is ≤ B in every case, as it must be.

This is a transverse version of Theorem A (5 and 7 forced to share lines), and I recommend publishing it as the primary proof, with the solver tables as corroboration.

*Corollary for the torus run.* Because 60ℤ² ⊆ {k − ℓ ≡ 0 (mod 60)}, monotonicity gives V_{60ℤ²}(pool 720720) ≤ 0.8424 < 1. So `torus_720720_T60_feas.jsonl`'s UNKNOWN is a solver timeout on an instance that is provably infeasible. The page should say so or drop the row.

**6. FIX: the solver description in LEMMA.md overstates what was run.**
Quoted: *"HiGHS MILP (scipy) on the same formulation as a decorrelated second solver, exhaustive enumeration where ∏ i_p is small"*.
- **Brute force:** the smallest ∏ i_p of any published row is 3,732,480, above the 3·10^6 limit, so `--brute` has never run on real data. The brief's example "(0,1) at N = 5040 where it does" has ∏ i_p = 20,736,000, so it does not.
- **MILP:** no `milp_*` file exists for any N ≤ 65,520. `feas_5040.jsonl` (16/16 directions, both solvers INFEASIBLE) and `feas_7920.jsonl` (5/5 so far) appeared during the review.
- So, apart from those, every published exclusion with N ≤ 65,520 rests on CP-SAT alone.
- I closed part of the gap myself (see the recomputation list), but the text must describe what was actually run.

**7. FIX: the witness recount uses the wrong test on time-limited runs, and covers less than the text implies.**
- Code: `out["cpsat"]["recount_ok"] = (rc == V)`. For FEASIBLE runs, CP-SAT's z need not equal min_τ W, so the right check is rc ≥ V.
- Two headline open-pool rows therefore ship with `"recount_ok": false`, and the .err files say `!! RECOUNT MISMATCH`:
  - 166320: recount 38723/55440 vs V 29041/41580;
  - 332640: recount 19697/27720 vs V 1475/2079.
- Both mismatches are benign (the recount is the larger value) but alarming to a reader. Report rc as the witness value.
- `recount_np` is independent of the solver but **not** of `instance()`: it reuses the same i_p, w_p. Witness recounts only certify lower bounds. Exclusions are upper bounds, and those are certified only by solver optimality or bound claims. LEMMA.md should say this plainly.

**8. FIX: the shipped `--control` never exercises the line formulas.**
- Both controls use direction (0,1) with (u,v) = (1,0). Then s = v = 0, so i = e and w = 1 for every class.
- The case 1 < i < e and fractional weights are never tested.
- My replacement controls are in `/tmp/ref203lines/`: an exact 2-D partition with mixed characters (`synth3.py`), which must give V = 1 in all 17 directions, and the φ-based 2-D end-to-end check (`e2e.py`).
- I mutation-tested the partition control:
  - with w = 1/e instead of i/e it fails in 12 of 17 directions, so it catches weight bugs;
  - with u, v swapped or the transverse sign flipped it does not fail. Those bugs reflect a cover into a cover, so they relabel directions rather than break soundness. The e2e check is what catches them, because it compares per-direction values (e.g. (1,0) = 13/30 vs (0,1) = 9/20).

**9. NOTE: the monotonicity justification argues a weaker statement than it claims.**
- Quoted: *"Λ' ≤ Λ ⇒ V_{Λ'} ≤ V_Λ (a cell of ℤ²/Λ is a union of cells of ℤ²/Λ', and (★) for the finer cells implies it for their union)"*.
- The parenthesis proves only "V_{Λ'} ≥ 1 ⇒ V_Λ ≥ 1".
- The stated inequality is true for a different reason. For every coset choice, W_Λ(g) is the average of W_{Λ'} over the Λ′-cells inside g (equal weights; use periodicity when [Λ : Λ′] is infinite), so min W_Λ ≥ min W_{Λ'}. Write that instead.

**10. NOTE: the torus paragraph contains an undefined quantity.**
- Quoted: *"so V_{Tℤ²}(pool) ≤ the block bound's slack"*.
- What is true and provable: if Theorem B's inequality fails for block B at T = lcm_B e_p, then V_{Tℤ²} < 1.
- Proof: summing W over the cells left uncovered by the block gives Σ_{p∉B} 1/e_p ≥ 1 − U(B) whenever the torus is feasible.

**11. FIX: the scope is not stated.**
- LEMMA.md never says the exclusions are for the **pure** covering mechanism.
- The perfect-power free sets of Theorem C (qℤ² and the Aurifeuillean set) are not part of (★).
- The page must say "covering system without algebraic free sets". `--pp` mode exists but is not part of this claim, and I did not review it.

**12. NOTE: table.py presentation issues.**
- The column header "directions run (exact)" also covers 720720's coarsened run (Mp = 55440).
- `ll_*_rerun.jsonl` rows replace the originals unconditionally, even if the rerun is worse.

**13. NOTE: the CP-SAT bound is read through float truncation.**
- Code: `F(int(s.BestObjectiveBound()), S)` truncates a double.
- For integer objectives CP-SAT returns an integral double, and the closest excluding bound to 1 (0.9919) leaves a margin far larger than 1/S, so no verdict depends on this.
- Still, assert integrality before truncating.

**14. NOVELTY.**
- **The lemma itself is folklore.** Quotient Lemma (i)–(ii) is the standard restriction of a coset cover to the cosets of a subgroup: a coset of K meets a coset of Λ in nothing or in a coset of K ∩ Λ. This goes back to B. H. Neumann (1954, *Groups covered by permutable subsets*) and is used throughout the literature (Tomkinson; Z.-W. Sun, *Finite covers of groups by cosets or subgroups*, IJM 2006, arXiv:math/0501451).
- **Inside the #203 thread there are two antecedents:**
  - AnimishSharma (21 Jun 2026): *"any such 2D Sierpiński number would also be a classical 1D Sierpiński number, by setting ℓ = 0"*. This is (★) on a single line, unweighted.
  - veljjanoski (15 Sep 2026, and README item 3): the shear k′ = k + Jℓ and "strip ℤ_N × ℤ_d". This is direction (−J, 1), but only as a restricted family of aligned primes, not as a necessary condition on the full pool.
- **Published work:** Granville–Pappalardi (arXiv:2601.10296, 2D covering systems for a^m − b^n) does not project to lines.
- **What appears new for #203, as far as I can find:** the weighted transverse condition (w_p = 1/ord_p(2^a3^b) on one class mod i_p = [H_p : ⟨2^a3^b⟩]), its max–min form, and the resulting exclusions of the full pools, including the 5–7 cut of finding 5.
- **Credit required:** call the restriction step standard and cite both thread comments.
- I could not consult Erdős–Graham p. 27 directly.

---

## Checked and correct

- **Lemma (i):** the coset meets each cell in z + (Λ ∩ L_p), a full coset, not merely a subset.
- **Index identity:** e_p = [G : S_p]·[Λ : Λ ∩ L_p], by the second isomorphism theorem.
- **(★):** a covered cell has union density 1, which is at most the sum of densities.
- **Exactness:** at Λ = ∩ L_p the test is exact.
- **Subset and divisor monotonicity:** W grows with P, and pool(d) ⊆ pool(N).
- **One coset per prime:** for fixed m, the hitting set is the preimage of the single element −m⁻¹ ∈ H_p.
- **Lemma 1 (ℕ² → ℤ²):** sound. 2 and 3 hit only k = 0 and ℓ = 0, and periodicity under Nℤ² lifts a quadrant cover to ℤ².
- **Scaling:** S = lcm of the denominators, so every weight is an exact integer.
- **`fix_one`:** valid. Shifting every t_p by c is the substitution τ ↦ τ + c, which preserves min_τ W. Verified empirically: 7920 (1,1) gives 4459/7920 both by full enumeration (3,732,480 configurations) and with the symmetry fix (414,720).
- **Verdict logic:** a direction excludes only on OPTIMAL with V < 1 or on bound < 1, and table.py uses bound < 1. No pool is called excluded without a bound < 1.

## What I recomputed (scripts and outputs in /tmp/ref203lines/)

- **Pools** (`check_pools.py`). All 33 pool JSONs, from 720 to 720720:
  - primality checked;
  - ord_p 2 and ord_p 3 recomputed with sympy;
  - each (e, u, v) checked against an explicit generator h = 2^α3^β with αu + βv ≡ 1 (mod e), requiring h^u = 2, h^v = 3, ord h = e;
  - completeness checked by dividing every pool prime out of gcd(2^N−1, 3^N−1).
  - Result: residual 1 for all 33, 0 errors. The densities match the JSONs.
- **Scan:** 26 periods N ≤ 65,520 have density ≥ 1, out of 65,520 rows, all `complete`.
- **Line formulas** (`check_lines.py`): 448 tests, 0 failures.
  - Coverage: primes with e ≤ 240 from pools 720, 5040 and 7920; directions (2,−1), (3,−2), (1,1), (1,−3), (2,3), (1,0), (0,1), (5,−7).
  - Checked: i_p, w_p = 1/ord_p(2^a3^b), the met lines being exactly τ ≡ τ(x) (mod i_p), and coarsening at M ∈ {6, 8, 10, 12}, both as a 1-D average and as a 2-D cell density on the torus.
  - Sample non-trivial lumps in direction (2,−1): p = 37: i = 12, w = 1/3; p = 241: i = 3, w = 1/40; p = 337: i = 21, w = 1/8.
- **Torus lattice image** (`check_torus.py`): T ∈ {8, 9, 15, 20, 24, 36}, 5040-pool primes with e ≤ 360. 144 checks of image, intensity and met cells, 0 failures.
- **Shipped controls:** `linelemma.py --control` PASS; `torus.py --selftest` PASS.
- **End-to-end** (`e2e.py`): the 2-D brute force uses φ on (ℤ/60)², shares no code with the formulas, and is compared with linelemma's CP-SAT for real primes with e | 60. 5-prime subpool: 17/17 directions agree exactly. 6-prime subpool (5.2M choices): 14 directions agree. 0 mismatches overall; the run then hit its time cap.
- **Exact 2-D partition control** (`synth3.py`): {3k+ℓ ≡ 0, 2, 4 (mod 6)}, {k+3ℓ ≡ 1 (mod 4)}, {k+7ℓ ≡ 3, 7, 11 (mod 12)}. V = 1 exactly in 17/17 directions (CP-SAT, bound and brute force).
- **Mutations, predicted before running:**
  - M1: classical cover with 23(24) given weight 1/2 → predicted V = 1/2, got 1/2;
  - M2: partition with the B coset halved → predicted V < 1 everywhere and ≤ 7/8, got max 7/8;
  - M3: 5040 (1,1), prime 11 weight halved → predicted V − 1/20, got 2671/5040 → 2419/5040 exactly.
- **Spot checks of three rows:** 5040 (0,1) = 529/630, 7920 (1,1) = 4459/7920, 7920 (1,−3) = 123/176. Each was reproduced exactly by my own exhaustive split enumerator (`splitbrute.py`, i_p from ord_p) and by linelemma's `--milp`. The brute force inside linelemma did not run (∏ i_p above its limit).
- **Coarse certificates:** M = 60 and M = 360 for the open pools (`coarse_run.py`), independent HiGHS (`indep_milp.py`), branch-and-bound (`bnb60.py`, controls in `bnb_controls.py`), and the closed-form 5–7 cut (`cut57.py`, `cut57_check.py`). Results as in finding 5.
- **Table:** regenerated with the patched table.py (`TABLE_regen.md`). Row status is as in finding 1.

Sources:
- [Z.-W. Sun, Finite covers of groups by cosets or subgroups (arXiv:math/0501451)](https://arxiv.org/abs/math/0501451)
- [Mathlib CosetCover, citing B. H. Neumann 1954](https://florisvandoorn.com/LeanCourse24/docs/Mathlib/GroupTheory/CosetCover.html)
- [Gorokhovsky–Matte Bon–Tamuz, A quantitative Neumann lemma (arXiv:2203.11099)](https://arxiv.org/pdf/2203.11099)
- [Granville–Pappalardi, Two dimensional covering systems (arXiv:2601.10296)](https://arxiv.org/html/2601.10296v1)
- [AnimishSharma forum profile](https://www.erdosproblems.com/forum/user/AnimishSharma)
