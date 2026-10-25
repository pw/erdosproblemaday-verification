# Seat B: blind read of the #371 entry page against its files (22 Oct 2026)

**What I read.** `entry/entry_rendered.txt` (rendered 09:01:21Z) and `entry/entry371.js`. The source was re-touched at 09:03:27Z, so every quote below was re-checked against the current source by `B_work/quotecheck.py`, and all are still present.

**What changed during the read.** At 09:03Z, `lean_label.txt`, `headline.js` and `closed_by.txt` were regenerated:
- the banner's doubled period (`from it.. Bloom`) is gone from the source;
- the stale "1,834 modules" in the summary, the headline and the closed_by comment now read 1,837.

The rendered file predates both fixes, so **re-render and confirm**.

**My scripts and outputs** are all in `seats/B_work/`, each run under `ulimit -v 4000000; timeout 600`:
- `scan3.py`
- `closure_check.py`
- `alpha_recompute.py`
- `alpha_count_1e6.py`
- `second_order.py`
- `bfile.py`
- `hist_1e7.txt`
- `quotecheck.py`
- `urls.txt`

The earlier blind seat's `B_mods_*.txt` are only the module lists from `deps.log`. I did not use them.

---

## MUST-FIX

**M1. The profile extraction is placed in the wrong section, and the "where to look" sentence repeats the error.**
- The page says: *"§4 supposes the decorrelation fails along some sequence of scales and passes to a limit profile on (0,∞) × Ẑ. It then amplifies with a divisor weight…"*
- It also says: *"Then read §4's profile extraction, §5's coupling of auxiliary-prime sets, …"*

In the paper, the bad subsequence and the profile W on (0,∞)×Ẑ come from **§2.6, "A profile of a nonzero mixed correlation"** (paper.txt l. 736 ff.: "We begin the proof by supposing that Proposition 2.2 fails … Passing to a subsequence …"). §4 starts *"from the fixed nonzero correlation profile in Section 2"* (l. 1497). §4 only *preserves* the profile under D_B (Lemma 4.4, §4.5). The page itself elsewhere says *"The profinite limit profile of §2.6"*, so it contradicts itself.

Fix:
- *"§2.6 supposes the decorrelation fails … and passes to a limit profile …; §4 amplifies it with a divisor weight …"*
- *"… then read §2.6's profile extraction and its preservation under the divisor weight (Lemma 4.4), §5's coupling …"*

**M2. A deliberate weakening in the paper is reported as a slip.**
- The page says: *"Small slips (R). … Prop. 7.1 states c₇ = 1/200 where its proof gives 1/80."*

The paper writes the stronger bound and then deduces the weaker constant on purpose (paper.txt l. 3149–3155): *"Taking the square root … gives the stronger bound ‖(1 − Pav)Ud‖ ≪ B^{−1/80}. In particular (7.2) holds with c7 = 1/200."* Stating a weaker exponent than you prove is not an error. R misclassified it and the page inherited that.

Fix: drop it from "slips", or write *"Prop. 7.1 states c₇ = 1/200; its proof gives, and says it gives, the stronger 1/80."*

**M3. The page calls something "ours" that the files show was done elsewhere first.**
- The page says: *"What is ours: … the Lean statement and proof of #928 as posed; …"*
- The heading says: *"Formal Conjectures and #928 in Lean (ours)."*

jbaelaw/Erdos928 (9–10 Oct) already states #928 as posed in Lean. See `W_src/erdos928_repo/Challenge.lean`: `def Problem928` with `strictEvent` = `P n < n^a ∧ P (n+1) < (n+1)^b`. It also proves the implication. The page's own credit paragraph concedes this (*"We were not first to formalize #928 or the implication"*), but the summary of what is ours does not.

What is ours:
- the **unconditional** proof, i.e. the discharge by OpenAI's kernel-checked theorem;
- the statement in **Formal Conjectures' density language**.

Fix: *"…an unconditional Lean proof of #928 as posed, stated in Formal Conjectures' density language (jbaelaw/Erdos928 stated it, in OpenAI's density convention, and proved the implication first)…"*, and retitle the heading, e.g. *"Formal Conjectures' erdos_371 and an unconditional #928 in Lean"*.

**M4. The forbidden-construct scan did not cover "all 1,837" closure files.**
- The page says: *"A scan of all 1,837 source files for forbidden constructs found nothing in the proof."*

`L_work/scan.py` read `oai_files.txt` (1,796 entries, including `lake-manifest.json`, `lean-toolchain` and the comparator) plus 41 non-OAI modules from `L_nonoai_modules.txt`. That makes 1,837 files, but the 41 came from the **v1 (parser-bug) closure**. It missed exactly the three modules the bug dropped:
- `PrimeNumberTheoremAnd.Sobolev`
- `PrimeNumberTheoremAnd.SmoothExistence`
- `PrimeNumberTheoremAnd.Mathlib.Analysis.Asymptotics.Asymptotics`

I scanned those three with L's patterns (`B_work/scan3.py`, raw and comment-stripped): **clean**. So the conclusion stands, but the sentence is false as written.

Fix: *"A scan of every Lean file in the closure (seat L's scan, plus the three modules its list missed, scanned by seat B) found nothing in the proof: …"*

**M5. The module and line counts are off by one for "its" (PaperMain's) closure.**
- The page says: *"The solution is OAI.NumberTheory.JointDickman.PaperMain. Its import closure is 1,837 modules and 221,524 lines: 1,793 of OpenAI's own (1,457 under JointDickman, …)"*
- The banner says: *"1,837 modules (1,793 OpenAI + …)"*

`all_order.txt` also contains the umbrella module `OAI.NumberTheory.JointDickman`. It is 15 lines, imports PaperMain, is **not** imported by PaperMain, and was the last module the driver built ("1837/1837"). PaperMain's own closure, which I recomputed with a nested-comment-aware parser in `B_work/closure_check.py`, is:
- **1,836 modules and 221,509 lines**;
- 1,792 OAI modules, of which 1,456 are under JointDickman.

This agrees with `ESTIMATE.md` ("1,792 OAI modules (1,456 JointDickman …)") and with `closure_sol.txt` (1,792 lines). The bridge's `leanchecker --fresh Bridge371` likewise covers PaperMain's closure, not the umbrella.

Fix, either:
- *"Its import closure is 1,836 modules and 221,509 lines … (we built 1,837: the closure plus the one-line umbrella module OAI.NumberTheory.JointDickman)"*, or
- keep 1,837 and say it is the closure of the umbrella module that imports PaperMain.

Apply the same fix in `lean_label.txt`, `headline.js` and the summary.

**M6. The page says the joint law "approaches" its limit, and one row of its own table moves away from it.**
- The page says: *"The joint law approaches its limit slowly and from below."*

In `compute/joint_table_1e10.txt`, row (a,b) = (0.3, 0.7) reads 0.013352 → 0.012092 → 0.012052 at 10⁶ / 10⁸ / 10¹⁰, against the limit ρρ = 0.015215. It is below the limit but moving **away** over this range; it is consistent with the second-order product 0.011759. The a = 0.3 marginal also starts *above* ρ(10/3) at 10⁶ (0.025267 vs 0.023650) before falling below.

Fix: *"At every tested (a,b) the joint share is below its limit at 10¹⁰; at small exponents it is not yet moving toward it (e.g. (0.3, 0.7): 0.0134, 0.0121, 0.0121 at 10⁶, 10⁸, 10¹⁰ vs 0.0152), as the second-order term predicts."*

**M7 (confirm only).** The rendered banner still shows *"… #928 as posed from it.. Bloom calls these claims, not endorsements."* The source is fixed (`lean_label.txt` now ends "from it"; `src/index.js` own371 also ends without a period). Re-render before shipping.

---

## SHOULD-FIX

**S1. The banner says "refereed", the body says no human has refereed.**
- The banner says: *"… via the joint Dickman law in natural density — refereed here 22 Oct, see /day/371-…"*
- The body says: *"No human has refereed the paper."*

A cold reader reads "refereed" as human refereeing. Suggest *"read by four AI seats here 22 Oct"*. The slug can stay.

**S2. The comparator's main theorem does have hypotheses.**
- The page says: *"OpenAI's comparator challenge … states joint_law, increasing_order and decreasing_order with no hypotheses."*

`joint_law` takes `0 < a < 1, 0 < b < 1`. Suggest *"with no hypotheses beyond 0 < a, b < 1 (no analytic inputs assumed)."*

**S3. The leanchecker run is not independent of the kernel.**
- The page says: *"An independent re-check by leanchecker --fresh …"*

leanchecker replays declarations through the **same** Lean kernel and toolchain (v4.34.1). It is independent of the build's elaboration, not of the kernel. Suggest *"A second, from-scratch kernel replay (leanchecker --fresh, same kernel) …"*.

**S4. The second-order sentence: the constant and sign are right, but the numbers are averages and the sentence carries no label.**
- The page says: *"…the marginal density near n is about ρ(1/a) − γρ(1/a − 1)/log n … At X = 10¹⁰ that predicts 0.2806 for a = ½ and 0.6171 for a = 0.7; we count 0.2811 and 0.6172."*

I re-derived the term from de Bruijn's Ψ(x,y) = xρ(u) + (1−γ)xρ(u−1)/log x + O(x/log²x). Then ∂ₓ at fixed y gives ρ(u) − ρ(u−1)/log x + (1−γ)ρ(u−1)/log x = **ρ(u) − γρ(u−1)/log x**. So the constant γ is correct, and the sign (below the limit) is correct.

The quoted values are the **average over n ≤ X**, using 1/(log X − 1) ≈ li(X)/X. Recomputed (`B_work/second_order.py`):

| a | average with li(X)/X | average with 1/(log X − 1) | pointwise at n = 10¹⁰ |
|---|---|---|---|
| ½ | 0.2806 | 0.2806 | 0.2818 |
| 0.7 | 0.6171 | 0.6171 | 0.6183 |

The counts 0.281109 and 0.617241 are averages too (`joint_table_1e10.txt` marginals), so the comparison itself is right.

Two fixes:
- say *"averaged over n ≤ X (1/log n averages to li(X)/X)"*;
- label the sentence **(c)**. `joint_table.py` itself calls it "a HEURISTIC second-order product (label (c))".

**S5. Two different lists are each called "the eight inputs".**
- The page says: *"The 'published input' propositions it does reach (an upper sieve, Selberg–Delange, a Siegel–Walfisz-type bound, two Mertens theorems, McDiarmid's inequality, a Chebyshev bound, the finite-bin distribution) are each supplied by a proof."*
- And later: *"Each of the eight inputs the unconditional proof uses is proved with a non-vacuous statement."*

The two sets differ:
- L's eight are CharacterDistanceDivergence plus seven others, with **no** Chebyshev.
- The walk reaches `ChebyshevPrimeCountingInput`, which L did not assess. It is a proved, non-vacuous π(t) ≤ Ct/log t (`Amplification/ChebyshevDischarge.lean`; checked).
- The walk also reaches `TwoPointCorrelations.PrimeReciprocalInput`, supplied by `primeReciprocalInput`.

Reconcile the two lists or name both.

**S6. "Littlewood-strength" overstates the bound.**
- The page says: *"…excluded once ζ(1+it) … is o(log t), a Littlewood-strength bound the library proves from Weyl differencing."*

Littlewood's bound is O(log t/log log t), which is strictly stronger than o(log t). Suggest *"an o(log t) bound (weaker than Littlewood's log t/log log t), proved from Weyl differencing."*

**S7. The page does not say where the Lean route's machinery comes from.**
- The 141 "Matomäki–Radziwiłł and Halász files" are 75 `MRT*` and 66 `Halasz*` modules. 140 of them are in `OAI.NumberTheory.TwoPointCorrelations`, i.e. OpenAI's sibling **family 007**, "Ordinary two-point correlations of multiplicative functions". The paper never cites it (W objection 4).
- The page's "Omissions in the history (W)" paragraph and the Lean-route paragraph both omit this. A reader "looking for the hole" in the Lean route needs to know the analytic engine is family 007's development.

Add one sentence.

**S8. The Epoch detail is not in the files.**
- The page says: *"Epoch's four Lean runs on Erdos371 (September, $300–$1,000 budgets) were all scored incomplete."*

W's report says only *"all four Erdos371 runs scored "I", at $300–$1000 budgets"*:
- there is no date, so "September" is unsupported;
- "I" is read as "incomplete" with no source.

Source both or drop them.

**S9. "The citations hold" is broader than what W could check.**
W lists as COULD NOT CHECK:
- de la Bretèche–Pomerance–Tenenbaum (0.05544/0.05866);
- Lü–Wang (0.2017, full text not opened);
- Wang 2021 (abstract only).

These are corroborated only secondhand. Add a clause saying so.

**S10. The Erdős–Pomerance sentences (extra point 1).**
- The page says: *"It says Erdős and Pomerance proved that each ordering has positive upper density; their paper says 'the lower density of integers n for which P(n) > P(n+1) is positive', which is stronger."*

Verified against `W_src/ErPo78.txt`:
- the live page says *"positive upper density"*;
- ErPo78 p. 312 has the quoted sentence verbatim;
- **§6 (p. 319)** proves lower density > 0.0099 and adds *"Note that the same is true for integers n for which P(n) < P(n+1)"*.

The quote alone covers only one ordering; "each ordering … stronger" needs the §6 sentence. Cite both: p. 312, and §6 p. 319 with the bound 0.0099.

Relatedly, *"They proved that each ordering occurs for a positive proportion of n"* would be sharper as *"…has positive lower density (at least 0.0099)"*.

**S11. Attribution of the density-½ conjecture.**
- The page says: *"Erdős and Pomerance posed it in 1978 …"*

ErPo78 has the independence "guess" and calls density ½ "the almost certain truth". Teräväinen 2018, Tao–Teräväinen 2019, Yang and the paper itself all attribute the ordering conjecture to the **Erdős–Turán correspondence (1930s)**. Suggest *"…posed in Erdős–Pomerance 1978 (the ordering conjecture goes back to Erdős–Turán's correspondence in the 1930s) …"*.

**S12. The α-table's 10⁶ column has no output file in `compute/`.** Only `out_alpha_1e9.txt` exists. I recounted with exact integers (P(n+1)²⁰ vs P(n)²⁰·n^k, `B_work/alpha_count_1e6.py`). All five values match: 0.4378, 0.3754, 0.2621, 0.1695, 0.0490, with 0 exact ties. Add an output file to the bundle.

**S13. The history paragraph says "proved" where the page later notes the 2019 result is a sketch.**
- The page says: *"Tao and Teräväinen proved it in natural density at almost all scales."*

"It" here is the joint law. The 2019 version (Remark 3.3) is the sketch the page later criticises the paper for calling "obtained". The full proof is 2512.01739 Thm 1.8, with thresholds x^{1/u} and exceptional scales. Suggest *"Tao and Teräväinen sketched it at almost all scales in 2019 and proved a quantitative form in 2025–26."*

---

## NIT

- **N1.** *"'0 < |j| ≤ T' should be strict."* The non-strict bound is true. The paper's §1.2 already writes 0 < |j| < T; §5.1 is just inconsistent with it.
- **N2.** *"All coupling failures together cost O(B⁵⁰/P₀)."* The paper (graph.tex l. 431) has O(B⁵⁰/P₀) + O(B⁵⁰e^{−B}).
- **N3.** *"…decided with a margin of 10⁻⁹ in log(P(n+1)/P(n)) − α·log n."* `alpha_count.c` applies 10⁻⁹ to 20·(that quantity), so the margin is 5·10⁻¹¹.
- **N4.** The banner says "family 12"; the body says "family 012".
- **N5.** *"…match the comparator's character for character."* That is true after whitespace collapse and dropping `noncomputable`/`@[reducible]` (statement_match.py).
- **N6.** *"Their 2026 paper (arXiv 2512.01739v2 …)"*. v1 is dated 1 Dec 2025.
- **N7.** *"…for all n beyond an explicit n₀"*. The Lean takes n₀ existentially. It is explicit mathematically (n₀ = ⌈2^{β/δ}⌉).
- **N8.** *"Two of the library's docstrings … 'propositions to be supplied as hypotheses'"*. Only PublishedInputs.lean says that. CharacterInputs.lean says "an explicit conditional input, not a proof of that analytic result".
- **N9.** *"An older conditional route through ConditionalMain.lean"*. Nothing in the files supports "older".
- **N10.** *"#print axioms under --trust=0"*. The trust level does not affect `#print axioms`.
- **N11.** *"Seat R found the same consequence unprompted."* W did too (W §2.3).
- **N12.** The independence-table description divides only one marginal by X. It is arithmetically equal to joint·X/(m₁m₂), but reads oddly; write it symmetrically.
- **N13.** The problem's source list drops [Va99, 1.10].
- **N14.** The bundle link returns 404 publicly. This is disclosed on the page.
- **N15.** Not on the page, but in the bundle:
  - R's 11,804 instances come from an unseeded run, so they are not reproducible. Harmless, since the identity is algebraic.
  - `lpf_numpy.py` at 10⁸ crashed (MemoryError) *after* printing its checkpoints. The page claims only checkpoints, so it is unaffected.
  - `rho_check2.py`'s "negative control: one iteration short" cannot fail, because Picard iterate f_n is already exact on [0, n+1].

---

## Checked and found right (selection)

**Replay**
- steps.tsv / post.log: 1,837/1,837, 0 errors, `build 1` stopped at 1,576/1,834. The three missed modules are as named.
- Σwall = 4.01 CPU-h; peak 7.35 GiB per process.
- leanchecker: rc 0, 3,629 s, maxrss 8.91 GiB; the missing-module control returns rc 1.
- Axioms are exactly {propext, Classical.choice, Quot.sound} for all three theorems; the planted sorry shows `sorryAx`.
- 10/10 MATCH, and 7/7 mutants are caught.
- Pins: v4.34.1, Mathlib d13f23b7, PNT c39a751, StrongPNT 2f5835c; the comparator imports only Mathlib.
- 28/7/9 non-OAI modules.

**Dependency walk**
- 10,515–10,572 constants in 1,626–1,627 modules.
- RealShortIntervalInput, ComplexShortIntervalInput, MultiplicativeExponentialInput, CharacterDistanceInput, MRTShortExponentialInput and MRTLiouvilleShortInput are never reached. Only *module* names containing two of these strings appear.
- 141 = 75 MRT* + 66 Halasz* modules.

**Bridge**
- Verbatim copy of FC at 3b7c94ec, with 3 mutations caught.
- The 2/b lemma.
- The sandwich directions and the n^δ ≥ 2^β step.
- Axioms are standard; the 3 mutants fail at the stated steps.
- FC_371.lean is byte-identical to the live copy.
- The 3dfd999 reviewer-notes quote is verbatim.

**Mathematics**
- Theorem 1.1 and Corollary 1.2 as printed.
- The §5 substitution, re-derived.
- The α-argument (extra point 3): §11's proof of Cor. 1.2 does establish weak convergence of (U_n, V_n) to D⊗D. The line v = u+α has mass ∫μ({u+α})dμ(u) = 0, so {v > u+α} is a continuity set. f(t) = ρ(1/t−1)/t follows from uρ′ = −ρ(u−1). So "(b) modulo Theorem 1.1" is honest.

**α-table predicted limits (extra point 4)**
- I recomputed all five independently: ρ from u·ρ(u) = ∫_{u−1}^{u}ρ, and the mirror formula ∫_α^1 f(y)F(y−α)dy.
- Results: 0.428844, 0.361011, 0.241256, 0.146827, 0.031405 (0.5 at α = 0). All match.
- The 10⁹ counts and mirror values match `out_alpha_1e9.txt`.

**Counts**
- 4,999,983,166 + 5,000,016,833 = 10¹⁰ − 1.
- The 16 joint counts at 10⁷ agree between the histogram and numpy programs (rerun).
- July census A(X) = inc + 1 at every power of ten.
- The A070089 b-file (1,000 terms, n ≤ 1,981) matches my independent recomputation.
- ρ(3) and ρ(4) agree with the literature to ~4·10⁻¹¹.
- The independence table matches `indep_ratio_1e10.txt`.

**Sources and world**
- MRT v3 remark (e^{−M}M → e^{−M}); Bloom quotes; TT 2019 quote; Yang dates (17 Jul / 13 Aug / 3 Sep / 16 Oct); 84 pages.
- The #371 page's "formalised proof" link points to the comparator file; the #928 page has no claims and no formal statement.
- Seats ran on Opus 5.5 (MODEL_RECEIPTS.txt).

**Links**
- arXiv ×6, GitHub ×5: 200.
- OEIS and erdosproblems: 403 from this datacenter IP, which is a known bot wall and not a dead link.
- pw bundle: 404 (private, disclosed).
