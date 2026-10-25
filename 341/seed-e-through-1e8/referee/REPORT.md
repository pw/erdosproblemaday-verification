# Hostile referee report: Erdős #341, seed E = {1,4,8,10,11,12} (2026-10-15)

**VERDICT: GAP AT the spectral/structural characterisation.** The title, summary, headline and body ¶3 say E is "a two-frequency quasicrystal (its spectrum sits on ℤf₁+ℤf₂)". The entry's own data refute that. The two generators are not independent: **4f₁ + 9f₂ ≡ 0 (mod 1) to 0.015 of a bin** (1.9·10⁻⁹). With exact peak locations, **36 of the 40 largest peaks are integer multiples m·g of one frequency, g = 0.28459193622** (|m| ≤ 82, residuals ≤ 0.013 bin). The other four are three window sidelobes and one stray. So the module has rank ONE, not two. f₁ = −9g and f₂ = 4g (mod 1). For {3,5,8,10,13} the rank is TWO, not three.

Everything else **HOLDS WITH FIXES** (listed below):
- the exact computation (generator, border-array bound, recurrence check);
- the shield SAT census (I re-encoded it independently and extended it to unions of cycles);
- the controller model (checked against the real greedy);
- the certificate patch.

Two of those fixes are statements that are false as worded and must change before publication: the title/summary/headline line "no Li-type shield exists at any modulus below 49" (15 shields exist), and the claim that the census driver now tells a crash from a failure (it does not).

All referee scripts and logs are in this directory. Paths below are relative to `erdos341e/`.

---

## A. Spectral and structural claims (the new instrument `spectrum.py`, and ¶3 of `entry/body.html`)

**1. Fatal to the label: the frequency module has rank one.**
- Objected to:
  - `entry/body.html:42–46`: "the peaks sit on a **rank-two frequency module** … the greedy from E settles into a two-frequency quasi-periodic set — … a model set whose internal space is two-dimensional".
  - `entry/title.txt`: "a two-frequency quasicrystal (its spectrum sits on ℤf₁+ℤf₂)".
  - `entry/headline.json` "title" and "line" ("pure-point-like on a rank-two frequency module").
  - `entry/summary.txt`: "a two-frequency model set".
  - `README.md:15–18`.
- How I checked: `referee/ref_spectrum.py` (log `ref_spectrum_E.log`). It locates each of spectrum.py's 40 peaks by golden-section maximisation of the exact DTFT over the element set, with no parabolic step.
- Result:
  - The smallest relation between the top two peaks is (4, 9), at 0.015 bin. The next smallest is 24,386 bins away.
  - The chance of a relation that close among |c| ≤ 20 is about 3·10⁻⁶.
  - The top three peaks satisfy f₁ + f₂ + f₃ ≡ 0 exactly.
  - A single generator g = 0.28459193622 explains every one of peaks #1–#24, and 36 of 40 overall, with a worst residual of 0.013 bin.
  - The four exceptions: #25, #32 and #36 sit 3.5–4.5 bins from f₂ and f₁. These are rectangular-window sidelobes, because the peak picker only excludes ±3 bins. The fourth is #30 (0.4476787).
- `spectrum.py` printed its own symptom of this. "70 module points with |coef| ≤ 6" should be 84 folded points; the 14 collisions are exactly pairs that differ by (4, 9), e.g. (−6,−6) and (−2,3).
- The "rank" the script reports is "how many generators are needed with |coef| ≤ 6". It is not the ℤ-rank. Generators are chosen greedily: f₂ is accepted as independent because no |c| ≤ 6 multiple of f₁ hits it. Independence requires that no integer relation exist at all.
- Consequence: the reading should be one frequency (internal space one-dimensional, Sturmian-type), not two.
- And see #2: even that reading fails as a description of the set.
- Fix: test the generators for integer relations up to a large bound (e.g. LLL/PSLQ, or a scan to |c| ≤ 50) before calling them independent. Then rewrite title, summary, headline and ¶3.

**2. The one-frequency picture is not a rotation coding either; "model set" is unsupported in any rank.**
- The near-period ladder is partly the continued fraction of g.
  - g = [0; 3,1,1,17,1,1,1,1,2,1,2,1,2,1,12].
  - Convergent denominators: 3, 4, **7**, 123, **130, 253**, 383, **636, 1655**, 2291, 6237, 8528, 23293, 31821.
  - 130, 253, 636 and 1655 in the autocorrelation chain are convergents. 889, 9547 and 27875 are not.
- A coding of the rotation by g with a finite-interval window would agree almost perfectly at the late convergents. E does not (`ref_convergent_agreement.log`):

  | shift q | ‖qg‖ | agreement |
  |---|---|---|
  | 8528 | 3.2·10⁻⁵ | 0.974 |
  | 23293 | 3·10⁻⁵ | 0.974 |
  | 31821 | 2·10⁻⁶ | 0.967 |
  | 27875 (best shift) | 2.2·10⁻⁴ | 0.988 |

- About 19% of the variance lies off the module.
- Fix: describe what is measured — a dominant rotation g plus a residual of undetermined type. Label "model set" and "quasicrystal" as (c) speculation at most, or delete them.

**3. The statistics of the spectral test.**
- (a) Chance per peak.
  - The code's estimate `(2C+1)^r·4·bw` is about 8.5·10⁻⁵. As arithmetic for one uniformly random frequency it is right (169 points, ±2 bins, folding cancels).
  - But it is the wrong null. Harmonics and intermodulation products of the dominant oscillation land on the module automatically. The question that decides rank is whether the generators satisfy a relation, and the test never asks it.
  - The "14 of 14" includes the two generators themselves, so it is really 12 of 12.
- (b) One bin or two.
  - `body.html:44` says "to within one frequency bin (1.3·10⁻⁷; chance per peak about 10⁻⁴), 34 of the 40 largest are".
  - The code tests `d <= 2*bw` (spectrum.py:41), and the 10⁻⁴ figure is the two-bin chance.
  - With the script's parabolic generators, 14 of 14 also pass at one bin. But "34 of 40" is a two-bin count. State which tolerance each number uses.
- (c) Parabolic refinement.
  - Against the exact maxima, the log-parabolic `refine()` is off by 0.24 bin on average for E (0.12 for S13).
  - The generators are off by −0.16 and +0.09 bin. The worst errors, 1.5–2.2 bins, are on sidelobe-adjacent peaks.
  - At a module point with |a|, |b| ≤ 6, generator error grows to as much as ~1.5 bins, which is comparable to the tolerance. So the refinement can make or break matches.
  - It did not fake the result here: exact locations tighten the residuals to 0.013 bin. But the test should run on exact (or tapered-window) locations.
  - The rectangular window also creates the sidelobe "peaks" #25, #32 and #36.
- (d) A huge-period periodic set looks the same.
  - Any statistic of a finite window is also a statistic of a periodic set whose period is at least the window (tile [1, 10⁷]). So the spectral test excludes no periodicity the border array has not already excluded.
  - Control `referee/periodic_ctl_elems.u32` (E up to 2·10⁶, then exactly periodic with period 3,333,331; log `spectrum_periodic_ctl.log`): spectrum.py finds the same sharp peaks (82.8% of variance) but only 11/40 on the module. So the test can see sub-window periods, which the border array already excludes.
  - Above the window it is blind. In particular it cannot decide whether g is rational: g = p/q with q beyond the reach of the current precision (≳10⁶) gives an identical spectrum.
  - The entry must say this explicitly, next to the spectral claim.
- (e) S13 (`ref_spectrum_S13.log`, `ref_rank_S13.log`).
  - The claimed rank-3 generators satisfy f₁ + 2f₂ − 2f₄ ≡ 0 to 0.024 bin. So f₁ = 2(f₄ − f₂) and the module is ℤ·0.40918482 + ℤ·0.46374126.
  - That module holds 40/40 peaks within one bin at |coef| ≤ 20, and 38/40 at ≤ 10.
  - No single generator works (6/40).
  - So `body.html:53–55` ("a spectrum on a rank-three module … its members differ in the rank of their frequency module") has the wrong ranks: they are 1 versus 2.

**4. "No peak sits at a rational frequency with a small denominator — which is the spectral statement of 'no rail'" (`body.html:45–46`).**
- Nothing in the bundle computes this, and "small" is undefined.
- With denominators ≤ 400 (the census range), peak #21 (0.3993903, 0.31% of variance) is 0.8 bin from 131/328, and #31 is 1.6 bins from 33/164.
- m = 328 is also the census's worst modulus (`body.html:29`). Neither is an accident: 26·328 = 8528 is a convergent denominator of g.
- Fix: define the denominator range, compute it, and report the 328 coincidence.

**5. "There is no rail and no shield: nothing is permanently in or permanently out" (`body.html:30`); "rail-free" (summary, README claim 3); "a shape Li's shield-and-controller cannot describe" (title).**
- This is measured only for m ≤ 400. At the near-period moduli it is false over the measured window (`ref_largemod_census.log`, classes on [N/2, N]):

  | modulus | classes empty | classes ≥ 95% full | random-set expectation |
  |---|---|---|---|
  | 31821 | 78.9% | 11.6% | ~0% for both |
  | 27875 | 62.1% | 2.3% | ~0% for both |

- Whether these become a shield at a large modulus is untested. The SAT census covers only M < 49.
- Fix: scope every "no rail / no shield" sentence to m ≤ 400 and say what happens at the near-period moduli. Change the title's "cannot describe" to "is not of Li's type at any modulus ≤ 400 or any doubling cycle below 49".

**6. Factor complexity (`body.html:37–39`: "slope about 2.5 … i.e. zero entropy, deterministic").**
- The numbers are limited by sample size and include the transient (`ref_complexity.log`).
  - p(100) is 38–52% of the number of available windows. As the data double, p(100) roughly doubles: 101,527 → 179,749 → 296,467 → 599,636. That growth tracks the amount of data, not n.
  - `analyze.py:62` uses the whole gap word from the seed. On the last half alone p(10) = 671, not 1,774; the quoted p(10) is inflated by the early transient.
- "Zero entropy" cannot be inferred from p(k ≤ 100) at this sample size.
- Fix: compute on a post-transient suffix, report p(k)/#windows, and drop "zero entropy, deterministic" or label it (c).

**7. Discrepancy.**
- `analyze.py`'s statistic (max |count − δx| over [1, N], with δ fitted on the same range) at 10⁷ is 949.6, reached at x = 1,702,604, inside the transient. A random set of the same density gives ~1,000 (draws: 831, 1,406, 904; `ref_discrepancy.log`). So as computed, E's number is indistinguishable from random.
- Refitted on the post-transient window [2·10⁶, 10⁷], E gives 215 against ~890 for a random set. That is a genuine signal.
- The random comparator at 10⁸ is ~3.2·10³. README's earlier "~10⁴" is wrong.
- For ⟨E8_DISC⟩/⟨E8_DISC_READING⟩: use the post-transient window and the correct baseline. Do not write "bounded".
- {3,5,8,10,13} gives 3,234 on [2·10⁶, 10⁷] against ~795 random, four times worse than random. So "whose extension has the same type with different constants" (`body.html:50`) is contradicted on discrepancy.

**8. Autocorrelation instrument (`analyze.py:44–53`).**
- `ac = ac/ac[0]` is not normalised by the overlap length, so it is biased by (n−q)/n.
  - At 10⁷ it cannot register a new best above its own 0.9512 for q > 390,400.
  - Its 0.8 candidate threshold is unreachable for q > 1.6·10⁶, half of the stated maxshift.
- My exact, overlap-normalised agreement over all 21 ≤ q ≤ 3,333,331 (`ref_agree.py`, `ref_agree_E.log`) confirms the 10⁷ numbers: 27875 at 0.98799 is the true maximum, then 37422, 47858, 9547. The quoted agreements 96.2–98.8% are correct. 766, 2544, 4199 and 10436 are local maxima of ac above 0.8, as claimed.
- But the 10⁸ sentence "no shift up to ⟨E8_MAXSHIFT⟩ ever agrees better than ⟨E8_BEST_AGREE⟩" (`body.html:34`) must come from exact agreement. With biased ac and n = 8·10⁷, shifts above roughly (1 − best)·n ≈ 4·10⁶ cannot be seen at all.
- "Fibonacci-like ladder of a rotation" (`body.html:34`) is a reading and must be labelled. In the light of #2, name the convergents of g instead.

**9. "The mismatch set under the best shift is spread uniformly over the residues modulo that shift" (`body.html:35`).**
- No code or log in the bundle computes this (grep finds only the mismatch fraction). Add the computation or delete the sentence.

**10. Citation (`body.html:47–48`): "the kind of object Calkin and Erdős had in mind when they wrote that no known method could prove such sets aperiodic".**
- Calkin–Erdős actually write: "Unfortunately there is currently no way to show that these sets are aperiodic (though there is good evidence [2,3] to suggest that they are)."
- "These sets" are two specific computed greedy sum-free sets, {1,3,8,20,26,…} and {2,15,16,23,27,…}, not "two-frequency quasi-periodic sets".
- The same paper's actual theorem is directly relevant given #1. The single-rotation codings S_α = {n : {nα} ∈ (1/3, 2/3)} are aperiodic sum-free sets and are never complete, i.e. never a greedy extension.
- Quote the sentence exactly. Cite the S_α result: E's dominant structure is a rotation, and Calkin–Erdős show a pure interval coding of a rotation cannot be greedy.
- Green's Problem 7 (`lit/green.txt:207–225`) is primarily about Ulam's sequence. The Dickson/Queneau question is in its Comments. Steinerberger's single-frequency phenomenon cited there is the natural analogue of E's rank-one spectrum and deserves a sentence.

## B. Exact computation (attack items 1–3): holds

**11. The generator is correct.**
- `fast341.c` line by line:
  - Seed elements are added unconditionally (line 21), and all seed-pair sums, including 2s, enter R (equal rule: SETB before the shift, line 24).
  - Truncation `lim = min(N−t, t)` (line 25) loses only sums above N or summands above t, which are not in S yet.
  - The carry form (line 28) is branch-free and flushes `prev>>(64−r)` into word top+1+q < W. No bit is dropped.
  - `el` holds N/2+64 entries, enough because S ∩ (M, N] is sum-free (at most ⌈N/2⌉) plus at most 64 seed elements.
- My set-based Python generator, written from the statement (`ref_greedy.py`, `ref_greedy.log`), matches fast341 and greedy341 byte for byte:
  - 9 seeds × both rules to 6,000 (E, {1,2}, the late certifier, S13, squares, {2,3,5,9,13}, {1}, {5,6,7}, Li);
  - E under both rules to 40,000;
  - the prefix ≤ 40,000 of `F_E_eq_1e7_elems.u32`.

**12. The border-array inference is correct, with an exact scope.**
- If the gaps are p-periodic from gap index n₀ ≤ s, the suffix g[s..] has period p. So "smallest period of the suffix > L/2" excludes every p < (that smallest period) with onset ≤ s.
- Control (`ref_periodic_control.log`):
  - The July-certified {1,2,7,8,10,11,12} gives gap period 204 (membership 2039) from both instruments.
  - A synthetic word that is periodic from index 5000 is detected from suffixes starting at 5000 and 6000, and correctly not from 4000 (15799 > half).
- Fixes:
  - (a) The summary's "finds no gap period at all", and the title's "has no period through 10⁸", overclaim. They should read "no gap period ≤ P terms beginning at or before term S".
  - (b) `body.html:19–20`, "excludes every membership period up to about ⟨E8_VALUE_PERIOD⟩": state the rigorous form. A membership period q with onset x₀ ≤ a_S induces gap period |S ∩ [x₀, x₀+q)| ≤ δq + 2·disc, so every q ≤ (P − 2·disc)/δ is excluded.
  - (c) ⟨E8_FACTOR⟩ must compare like with like. July's 20,000 is a membership (value) period and the new P is in terms.

## C. Shield SAT census (attack item 4): holds; wording fixes

**13. The encoding matches Li's Lemma 3.1, and the census reproduces independently.**
- Line by line against `Erdos341.tex` Lemma lem:shield and the proof of Thm 3.2:
  - cover = (B+B) ∪ (P+B) ∪ (D+B) ⊇ ℤ/M ∖ Q;
  - avoid on Q includes D+P;
  - (PP) means mixed sums lie outside Q (on-rail mixed sums are rejected statically);
  - B is nonempty;
  - B ∩ D = ∅.
- `shield_sat_L.py` matches all of this.
- My own encoder written from the tex (`ref_shield_union.py`, `ref_shield_union.log`) gives the same 50 PP / 29 UNSAT / 15 SAT on the 94 cycles. Cycle enumeration is complete: 94 cycles, identical to `cycles_all_below_49.txt`.
- Controls reproduce: Li's B/D forced at M = 49 is SAT, and forbidding B gives UNSAT. Re-runs of `shield_sat_L.py` on 10 instances agree (`shield_rerun.log`).
- **Extension the entry did not do:** P a union of ≥ 2 doubling cycles with at least one cycle of length ≥ 3, for all M ≤ 48 (320 instances): 316 fail (PP), 4 are UNSAT, none is SAT. So the multi-cycle variant of Li's architecture is also closed below 49. Worth adding.
- MaxSAT (`ref_shield_min49.py`): at M = 49 both 3-cycles have min |D| + 2|B| = 17, which is Li's. So "his 21 elements … the smallest seed it can produce" (`body.html:74–75`) is supported up to |R|, within the model seed = D ∪ B ∪ (M+B) ∪ R. The bundle had no artifact for it; add this one.

**14. False as written in the title, summary and headline.**
- The claims:
  - `title.txt`: "no Li-type shield exists at any modulus below 49";
  - `summary.txt`: "no shield of Li's type exists for any doubling cycle at any modulus below his 49";
  - `headline.json` "line": "Li's shield conditions are unsatisfiable for every doubling cycle at every modulus below 49";
  - README claim-4 heading.
- The census itself has 15 SAT shields (two-rail, M = 6…48).
- Correct form: "for every doubling cycle of length ≥ 3 below 49; the two-rail shields that exist carry controllers that were periodic from every initial content tried."

**15. Detail errors in ¶4 (`body.html`).**
- Line 59: "every sum landing on a rail comes from that rail's own diagonal" is wrong. It comes from the diagonal of the predecessor rail (7+7 lands on 14).
- Line 57: the description of avoid omits D+P.
- Line 67: the parenthetical "the four- and six-cycles at 10, 15, 18, 27, 36, 45" is incomplete.
  - The PP-failing short cycles are at M = 5, 9, 10, 15, 18, 20, 25, 27, 30, 35, 36, 40, 45 (14 cycles).
  - "Every cycle of length 8 or more" is correct: 36 cycles.
- Line 69: "the 15 that are satisfiable are exactly the two-rail cycles {M/3, 2M/3} for 3 | M". There are 16 such cycles; M = 3 is UNSAT. Say "6 ≤ M ≤ 48".
- The 50 PP cases are infeasible only for a diagonal-only gate. A controller fed by mixed rail sums is an untested architecture. The ¶ ends "a finite census of one mechanism", which is fine; the headline is not.

## D. Controller census (attack item 5): model correct; claim overstated

**16. `census2.c` carries and processing order are right.**
- Rail j with predecessor i reads q − c_i, where c_i = [2x_i ≥ M].
- Carry-0 predecessors have smaller residue, so they are processed first within a block.
- Independent check (`ref_rails.py`, `ref_rails.log`): the REAL greedy from Lemma-5 seeds produces rail contents identical, for 1,500 blocks, to my set-based simulation of the forced dynamics.
  - Seeds: three at M = 6 (two-rail), plus Li's seed and a variant at M = 49.
  - No non-shield residue appears after 2M−1, and the B rails are full.

**17. Over-claims about controller periodicity.**
- `headline.json` "line" and `summary.txt` say "every two- and four-rail controller is periodic".
  - (a) Only initial contents on q ≤ 3 (two rails) and q ≤ 1 (four rails) were tried.
  - (b) "Periodic" means a suffix period ≤ 8000 was seen on [Q/2, Q). That was detected, not certified. The verdict depends on Q and Pmax: at M = 49, Q = 4096 with Pmax = 1000 gives 25 aperiodic-to-Q, versus 23 at 65536/8000.
  - (c) The four-rail census is the single-wrap carry pattern only, while multi-wrap 4-cycles exist (M = 15, x = 7 has carries 0, 1, 1, 1; likewise M = 30 x = 14 and M = 45 x = 21).
- The body's own wording (`body.html:69–71`, "finds every one of them periodic") should read "shows a period ≤ 9 on [2¹⁵, 2¹⁶)".
- The [13] claim survives: for M = 6, seeds in [13] need q₀ ≤ 2.

## E. Seed census (attack item 6)

**18. The patch is sound.**
- `certify.py:31`, `L = max(L, M+1)`. When X₀ = 2N+q−2 < M, the lemma's tail argument already covers every x > X₀ ⊇ (M, ∞). The patch only makes the seed assertion and the (now trivial) range well defined.
- Certification cannot be false. rc 0 requires zero violations on a from-scratch FFT recurrence check plus E+R = ℤ_q∖R.

**19. False: "the driver now distinguishes the two" (`body.html:86–87`).**
- `census.py:35` treats any return code other than 1 as TOOL ERROR. An uncaught Python exception exits with status **1**.
- Demonstrated (`crash_vs_fail.log`):
  - `certify.py` with a mismatched seed raises AssertionError, rc 1;
  - an absurd qgap raises IndexError, rc 1.
  - Both read as "not certified", escalate, and end UNRESOLVED.
- The failure mode that produced the false survivor {2,3,5,9,13} is still live for any other edge case.
- I re-checked the current survivors ({3,5,8,10,13}, {2,4,6,9,10,11,13}, {2,6,8,9,10,11,14}, {3,6,8,9,12,14}; `survivors_recheck.log`). They are genuine: no period ≤ half the suffix at 2·10⁶, so certify was never called. But the census is still running.
- Fix: have certify.py exit 1 only on a clean NOT CERTIFIED (wrap the body; uncaught exceptions → exit 3), then rerun or recheck every UNRESOLVED.

## F. Scope and register (attack items 7–8)

**20. "E is the smallest seed on record that resists every finite test" (summary).**
- True only by largest element. {3,5,8,10,13} has five elements to E's six.
- Likewise `body.html:42–43`, "the smallest counterexample seed would drop … to 6 inside [12]": say "smallest by largest element".

**21. "Two thirds of its gaps are 7 … 1/f₂ = 7.227 is the 'seven' the gaps keep hitting" (`body.html:43`) is a reading.**
- Under #1 the seven is the convergent denominator 7 of g (‖7g‖ = 0.008), and f₂ = 4g.

**22. Stale chain pointers in README.**
- "Chain" cites `shield/cycles_below_49.txt` + `shield/shield_all.log` as the census, but the census is `cycles_all_below_49.txt` + `shield_all_v3.log`.
- It also cites `shield/census6_*.log`, `shield/census2_rail2_q3.log` and `shield/census_ref.log`, which do not exist. Everything is in `census_controllers.log`.

## Numbers I checked and found right

- Gap histogram and density.
- The m = 328 extremes 0.826 / 1.182.
- Autocorrelation agreements 96.2 → 98.8%, and the five ladder sums.
- Spectrum variance shares: 77.31% within ±3 bins of the top 14, 85.73% for the top 40, 80.73% within ±1 bin of the module points.
- S13's gap-suffix bound (no period ≤ 297,128 from 594,256) and residue extremes.
- July SHA through 500,000.
- verify341 controls.
- The 94-cycle count and the 50/29/15 split.

## Referee artefacts
`ref_greedy.py/.log` · `ref_agree.py`, `ref_agree_E.log` · `ref_spectrum.py`, `ref_spectrum_E.log`, `ref_spectrum_S13.log`, `ref_rank_S13.log`, `*.peaks.npy` · `ref_convergent_agreement.log` · `periodic_ctl_elems.u32`, `spectrum_periodic_ctl.log` · `ref_largemod_census.log` · `ref_complexity.log` · `ref_discrepancy.log` · `ref_periodic_control.log` · `ref_shield_union.py/.log`, `ref_shield_min49.py/.log`, `shield_rerun.log` · `ref_rails.py/.log` · `crash_vs_fail.log`, `survivors_recheck.log`.
