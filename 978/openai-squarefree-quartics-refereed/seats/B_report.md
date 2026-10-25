# Seat B: blind hostile read of the #978 entry page, checked against the files (22 Oct 2026)

Inputs: `entry/entry_rendered.txt`, `entry/entry978.js` (identical to `entry978.js.pre-blind`), plus `headline.js`, `lean_label.txt` and
`closed_by.txt`, all checked against the files listed in B_BRIEF. My scratch is in `seats/B_work/`. I ran only small python and gp jobs, all under
ulimit. I did not run lean or lake, and I edited nothing outside `seats/`.

The checks that hold are listed at the end. **Six MUST-FIX items.** The first matters most.

---

## MUST-FIX

### B1. The page says ours is the first kernel replay. Two earlier public replays exist.
The claim appears in four places:
- Body: *"Seat W searched GitHub, the aggregators and the forums and found no earlier report of anyone replaying this formalization. … As far as we can find, this is the first reported kernel replay."*
- LEAN_LABEL (the notice box): *"Kernel-replayed on our machine on 22 Oct 2026 (as far as we could find, the first reported replay)"*.
- Summary: *"— as far as we could find, the first reported replay."*
- Headline tag: *"LEAN KERNEL-REPLAYED HERE (63 MODULES, STATEMENT MATCHED; NO EARLIER REPLAY FOUND)"*.

All four are false. Both earlier replays are public on GitHub and turn up under the challenge name `PowerFreeValues`. W searched only
`QuarticPowerFree` and `OAI.NumberTheory.PowerFree`, which is why it missed them (`gh search code PowerFreeValues`).

- **carlostoledo1891/cert-machine**, file `corpus/openai-math/kernel-runs/38019899278/PowerFreeValues.json`.
  - Committed in d93dd5b4 on **2026-10-10T08:34:51Z**, with the message *"openai/math lane K: 202 of 416 challenges decided — 193 CERTIFIED by Lean's kernel and nanoda"*.
  - The record reads `"challenge":"PowerFreeValues","exit":0,"okay":true`.
  - Its kernels field reads `["Lean default kernel accepts the solution","nanoda kernel accepts the solution"]`.
  - It exports `OAI.QuarticPowerFree.allDegrees` from `OAI.NumberTheory.PowerFree.Main` on Lean 4.34.1.
  - So this replay used two kernels, one more than ours.
- **nealmcb/openai-math-lean-tooling**, file `results/cmp-all/configs.csv`.
  - The PowerFreeValues row reads `accepted, OAI.NumberTheory.PowerFree.Main, in_repo_closure 63, … check_peak_rss_gib 6.7, … started 2026-10-11T04:59:17Z`.
  - The commit "Record the finished Comparator run: all 416 configs accepted" landed on 2026-10-13.
  - The README says Comparator "has the Lean kernel re-check the solution's proof, confirm that the theorem statement is identical to the challenge's, and confirm that only the permitted axioms are used".
  - The pins are the same as ours (Lean 4.34.1, Mathlib d13f23b7). The PowerFree files are byte-identical between its commit fd4aeeb and ours.

Our other entries already say "after others had built it" (see own952 and own371 in LEAN_LABEL). This entry contradicts the site's own record.

**Corrected body sentence:**
> "Two third-party kernel replays came first. carlostoledo1891/cert-machine ran OpenAI's Comparator on PowerFreeValues, and Lean's kernel and nanoda both accepted (GitHub Actions run 38019899278, committed 10 Oct). nealmcb/openai-math-lean-tooling ran Comparator on all 416 configurations; PowerFreeValues was accepted on 11 Oct and recorded on 13 Oct. Ours is an independent third replay. It builds module by module from source, and adds a pp.all match of the theorem and its seven definitions under a mutation-tested matcher, a source scan, and the Formal Conjectures bridge. Seat W's search (QuarticPowerFree, OAI.NumberTheory.PowerFree) missed both, which appear under the challenge name PowerFreeValues."

**Matching edits:**
- LEAN_LABEL: "Kernel-replayed on our machine on 22 Oct 2026, after two earlier third-party Comparator replays (10 and 11 Oct; one also with nanoda): …".
- Summary: replace the last clause with "independently of two earlier third-party replays".
- Headline: "(63 MODULES, STATEMENT MATCHED; TWO EARLIER THIRD-PARTY REPLAYS)".
- Where to look, kernel item: these replays are worth citing there too. Two kernels (Lean and nanoda) have now accepted it.

### B2. 24979/25000 and 3122/3125 are exponent bounds, not margins
Page: *"§11 assembles the tail … The worst margins are 24979/25000 and 3122/3125."*

Paper §10.1, eqs. (parameter-final-box-exponent) and (parameter-fiber-exponent), says something different:
- The combined box exponent satisfies *"m+ΣE_h(u,v)+dτ < 24979/25000 < 1"*.
- The removed-fibre exponent satisfies *"m+2u−2j+2τ < 3122/3125 < 1"*.
- The paper adds: *"The estimate uses only the advertised 999/1000 bound and d ≤ 8; Table 1 gives stronger bounds."*

So both numbers are exponents, which leave margins of 21/25000 and 3/3125. They are crude uniform bounds, not the worst cases.

**Fix:**
> "Every box exponent is below 24979/25000, and every removed-fibre exponent in the quartic mode Q is below 3122/3125. These are uniform bounds from the 999/1000 certificate; Table 1's are stronger."

### B3. "the tightest margin is 0.00059" is contradicted by L's own checker
Page: *"L re-checked every certificate inequality in exact arithmetic; the tightest margin is 0.00059."*

L's report and `L_work/cert.py` say 0.00059 is the tightest **full-threshold margin among the quartic bins** (at j = 0), not the tightest margin overall. The same checker shows two tighter cases (my run is in `B_work/margins.py`):
- For d = 5 the exponent sum plus 1/1000 equals exactly 997/1000. That is margin 0, which is allowed because the inequality is ≤. L says so itself.
- The medium-degree full-threshold envelopes clear their thresholds by 0.00094 (d = 5), 0.00096 (d = 6), **0.00049 (d = 7)** and 0.00058 (d = 8).

**Fix:**
> "L re-checked every certificate inequality in exact arithmetic, and all hold. For d = 5 the exponent sum meets its 997/1000 bound exactly (allowed, since the inequality is ≤). The full-dimension thresholds clear their envelopes by as little as 0.00049 (d = 7) and 0.00059 (d = 4, first bin)."

### B4. The page invents a disagreement and puts W's reasoning in M1's mouth
Page: *"One disagreement, on Corollary 1.3 only. … W graded this a GAP: Reuss's §§2–3 work in ℤ[θ] with θ integral … M1 graded it EXPOSITION: Reuss's statement is for general irreducible f, and the estimate is assembled from his proof text rather than stated."*

M1's report never mentions monic polynomials, integral θ, or "general irreducible f" (grep returns 0 hits).
- M1's objection 2 is a different point. Reuss never states the triple estimate; it is assembled from his proof text. M1 graded that EXPOSITION.
- The mitigation "Reuss's statement is for general irreducible f, so the citation is defensible" is **W's own sentence**, in W §3.

So no second seat examined the monic reduction and disagreed. Only W examined it.

**Fix:**
> "One GAP, in Corollary 1.3 only. For d = k+1 the proof cites Reuss's Lemma 3, its proof and his §6 for the triple count. W graded this a GAP: Reuss's §§2–3 work in ℤ[θ] with θ integral, i.e. for monic f, and the paper applies them to a primitive, possibly non-monic g without the standard reduction (substitute y = cn, so that c^{d−1}g(y/c) is monic). W adds that Reuss's statement is for general irreducible f, so the citation is defensible. M1 checked the same citation for a different point: the estimate is assembled from Reuss's proof text rather than stated. M1 graded that EXPOSITION and did not examine the monic reduction. Either way the gap is fillable, it touches only Corollary 1.3, and Corollary 1.3 has no Lean."

The seat-verdict sentence should still say W's GAP.

### B5. The page says every count was made twice. One cell was made once, and the stated provenance is wrong.
Page: *"Each count was made twice, by different methods. The first factors every n⁴+w in PARI/GP: our July run to 10⁵, whose factorisations a separate program certified; today's run to 2·10⁵; and seat M2's to 10⁶. … The two agree at every checkpoint."*

The files say otherwise:
- The July report (`erdos978_wave7y.md`) counted only n⁴+2. Its counts table is for n⁴+2 and it never mentions n⁴+1.
- `compute/euler.gp` prints totals only at N = 2·10⁵.
- M2's `out_w*_c*.txt` are blocks of 2.5·10⁵, so they have no checkpoint at 10⁵.

So the n⁴+1 cell at 10⁵ (98,090) comes from the sieve alone, and no factoring run in the bundle covers it.

The number itself is right. A one-line gp factoring count (`B_work/c1.gp`, `issquarefree`) gives 98,090 for n⁴+1 and 75,670 for n⁴+2.

**Fix:** add that factoring run to the bundle and say so. Or write: "our July run to 10⁵ (n⁴+2 only, with certified factorisations); a factoring run to 10⁵ for n⁴+1 (98,090, added today); today's run to 2·10⁵; and seat M2's to 10⁶."

### B6. "in each, the unsaturated weight would have given the wrong count" is false for one of M2's three examples
Page, in the M2 bullet: *"… three examples of Proposition 7.1's pair image under five weightings (15 runs), with no mismatch; in each, the unsaturated weight would have given the wrong count, so the saturation step is needed and right."*

M2's own output (`M2_work/whilb2.out`) contradicts this:
- Example E2 (F₁ = a₁a₂ − n) has series(naive) = series(D) in all five weightings: 600=600, 616=616, 863=863, 192=192, 223=223.
- The unsaturated weight differs only for E1 and E3, which is 10 of the 15 runs, and for the first-cut component.

M2's report sentence "In each…" carries the same overstatement, and the page inherited it.

**Fix:**
> "… with no mismatch. In two of the three examples (10 of the 15 runs), and for the first-cut component, the unsaturated weight would have given the wrong count. So the saturation step is needed, and it is right."

---

## SHOULD-FIX

### S1. "The Lean uses g = 3 and does not need them"
"Them" here means Propositions 8.1 and 8.2. Two places contradict this:
- The page's own Lean paragraph says the Lean has *"quartic surface and curve alternatives in the spirit of §§8–9"*.
- L maps AffineHilbert, PoleCoefficients, ThreePoles, TwoPoles and QuarticSurfaces to an analogue of Prop 8.1. M1 notes that the Lean's δ₂ uses a "pole" bound UV²/(V+4U) that the paper does not have.

**Fix:**
> "The Lean uses g = 3 and its own surface bound, an analogue of Proposition 8.1 with different alternatives. It needs no quintic deletion, because it counts on a different variety."

Also, the "needs none of" list rightly omits 8.1, so this sentence should match it.

### S2. Summary: "(no determinant cuts, no quintic deletion)"
The Lean's affine counting theorem is itself a determinant method: residue-class determinant cuts at auxiliary primes, in GenericCuts, PureCuts and AffineCounting. What it lacks is the **archimedean** (Taylor) cut. The body says that correctly; the summary should say "no archimedean determinant cuts".

### S3. "which read literally removes degrees 4 and 8 from part (ii)"
FC's `parts.ii` has `(¬ ∃ l : ℕ, f.natDegree = 2 ^ l)` together with `natDegree > 3`. That excludes **every** power-of-two degree: 4, 8, 16, 32, …. The page's preamble ("k ≠ 2^l for any l ≥ 1") does the same.

**Fix:** "removes every power-of-two degree (4, 8, 16, …), including 4 and 8 from Theorem 1.1's new range."

### S4. "Formal Conjectures marked the problem solved after a build and a source inspection (PR #6898)"
PR #6898's stated checks are:
- *"every changed module and the four importing modules build with `lake --wfail build`"*, which is FC's own files;
- link resolution by source inspection;
- a grep for sorry;
- comparator config inspection.

A reader can take "after a build" to mean OpenAI's Lean was built, which would be a replay. **Fix:** "after building its own changed files, checking that the link resolves, grepping the release for sorry and inspecting the comparator config. It did not build or replay OpenAI's proof." The later "Record elsewhere" sentence should get the same treatment.

### S5. The headline overstates the result
HEADLINES has *"OpenAI's proof for every quartic"* in the title and *"OpenAI claims all of them"* in the line. The result is for **every irreducible quartic with no fixed square divisor**. Counterexamples to the literal wording:
- x⁴+4 is reducible.
- x(x−1)(x−2)(x−3)+24 has 4 | f(n) for every n.

The tag already says it correctly. The title and line should too.

### S6. The letter k means two things on the page
The page switches between the problem page's k (the degree) and the paper's k (the exponent, k = d − 2) without saying so.
- Right after "Theorem 1.1: … put k = d − 2", it says *"The (k−2)-question is answered for every k ≥ 4 with density"*, where k is the degree.
- The record list uses k as the exponent ("k ≥ (√2−½)d").

**Fix:** "The problem page's (k−2)-question (k the degree) is answered for every degree ≥ 4 …". Alternatively, write d for the degree throughout.

### S7. Corollary 1.3, §12 and the paper's route have no label
The labels paragraph defines (a) to (d), labels Theorem 1.1, Cor 1.2 and the FC statements (d), and then calls Corollary 1.3, §12 and the paper's own route only "paper-only".

Under the site's own scheme these should be **(c) plausible, unverified**. They were read by AI seats only, are unrefereed, and Corollary 1.3 carries an open GAP. State the label.

### S8. "Where to look for a hole" is missing some places
**Formal side.** The page says *"only four places can hide one"*. It omits:
- Mathlib's definitions as they enter the statement (tprod, Multipliable, IsLittleO, Nat.floor and so on). L argues the tprod and HasProd-0 traps are guarded, which is worth saying.
- The fact that Mathlib's compiled files came from `lake exe cache get`. `--trust=0` does not re-check them; only the pending `leanchecker --fresh` does.

If the leanchecker pass is not finished or fails at publication, the third bullet ("the kernel (our replay, and the leanchecker pass)") must change with the placeholder.

**Paper side.** The list *"Lemma 4.2, §§5–6, Proposition 8.2, the certificate of §10 and Appendix A, and Corollary 1.3"* omits several things the page itself says the Lean does not touch:
- §12;
- the §11.1 direct-surface argument for d ≤ 8;
- Prop 8.1 and the §7–9 thresholds as stated, which the Lean only parallels;
- the Browning/Xiao citation for d ≥ 9.

Make it match the "needs none of" list plus Cor 1.3 and §12.

### S9. W's verdict is reported without its caveat
Page: *"W returned HOLDS AS READ on … the cited ranges …"*. W's verdict also says *"Browning 2011 primary text COULD NOT be fetched"*. The range k ≥ (3d+1)/4 rests on secondary attestations (Xiao, Heath-Brown 2013, Reuss). Add a clause.

### S10. "17 minutes of wall time on four workers"
The 63 modules form a **single linear import chain**: each imports exactly the previous one, and the longest path is 63 of 63 (my check). `driver.log` shows strictly sequential builds. The worker cap was 4, but only one module ever ran at a time. **Fix:** "17 minutes of wall time, one module at a time (the closure is one import chain)".

---

## NIT

- **"Table 1 rounds it down to 0.00191"** — 0.0019350 does not round to 0.00191. Table 1 gives a rigorous lower bound by rounding radicals up (its caption). Say "Table 1's 0.00191 is a lower bound from upward-rounded radicals".
- **Misquoted branch count** — *the "at most k^d local branches" count* is in quotation marks, but the paper says "at most k^d root choices / such choices". Drop the quotes or quote exactly.
- **"All seven bridge theorems depend only on …"** — Bridge978.lean contains 13 theorems. AxBridge printed the 7 top-level ones, and the other 6 are reached transitively. Say "the seven top-level bridge theorems (the rest are used by them)".
- **Unescaped HTML in LEAN_LABEL** — the own978 string carries raw `<` and `>` ("ρ_f(p^(d−2)) < p^(d−2) … c_f > 0") into HTML without escaping. Browsers render it, but any tag-stripping consumer (our own renderer, feeds) deletes the clause. That is why the rendered page reads "ρ_f(p^(d−2))  0". Use `&lt;` and `&gt;`.
- **"refereed here 22 Oct" in the notice** — a cold reader may read this as human refereeing. Say "read by four AI referee seats here". The path `/day/978-…` is also plain text in the notice, not a link.
- **"two independent counts" (summary)** — the sieve is exact only through the factorisation census of p > n, which the body says. "Two counts by different methods" is safer.
- **"at d−2 the record stopped at degree 9 (Browning 2011)" (summary)** — this holds for general polynomials. Binomials x^d+c already reached d ≥ 6 (Heath-Brown 2013), as the body says.
- **"Seat W found its constants wrong as well: 0.757159 …"** — our July report had already flagged Carella's 0.757159 against the enclosure ≤ 0.75668401. W added 0.981003 and the Theorem 1.3 constant (0.9006 for T⁴−2T²+2 checks out: `B_work/t3.gp` gives 0.900592; the displayed n⁴−n²+2 would give 0.97452).
- **ZCJ summary** — "monic irreducible degree-2q polynomials whose field has a degree-q Galois subfield" omits "q prime" and "squarefree fixed divisor". Corollary 2.4 likewise requires gcd h(ℤ) squarefree. The ZCJ "includes n⁴+1 … n⁴+2 too" point appears twice, in Smaller points and in Sources.
- **Simhi (2610.29911)** — *"still calls the problem 'a deep open problem' beyond degree 3"*. Simhi's sentence is about E_P = o(x) for **every** admissible P, which is still open for degree ≥ 5 even after OpenAI. Better: "still says the squarefree asymptotic is known only for degree ≤ 3 (Hooley), and does not cite OpenAI".
- **"§11.1 condition η(1 − kη/d) ≤ 0.2495"** — the paper writes a strict "<". The 0.2495 is §10's transition threshold; §11.1 itself needs √(b′η′/D) < 0.4999.
- **"Everything rests on Proposition 1.4"** — Theorem 1.1 does. Corollary 1.2 for d ≥ 9 rests on Browning, and Corollary 1.3 partly on Reuss and Xiao.
- **"the trivial bound ρ(p^k) ≤ d for primes up to X"** — this holds outside a finite set of primes, by Hensel. The finite set goes in the sieve.
- **"M2 … checked every concrete claim by computation"** — M2 says it computed "every Hilbert-function claim that can be made concrete" and checked the rest by hand.
- **"Erdős problem #978 [Er53; Er65b, p. 219; Er81h, p. 178]"** — the live page's own source tags are [Er65b, p. 219] and [Er81h, p. 178]. Er53 is cited only in its commentary.
- **"every case, conditionally on the abc conjecture (Granville 1998)"** — Granville's Theorem 1 is about squarefree values. The k-free case follows because the large-prime tail for p^k sits inside the tail for p². That is fine, but it is an inference.
- **Sources link label** — it says "and the comparator challenge …", but the link points only at the PowerFree directory.
- **Our bundle link** — it returns 404 (repository private). The page discloses this.
- **Bundle hygiene, not on the page:**
  - `bridge/verbatim.log` and `verbatim_mut.log` were written at 12:12, before Bridge978.lean was fixed at 12:23. I re-ran `verbatim_check.py` on the current file in `B_work/vb`: all 7 MATCH (rc 0), and `--mutate` gives rc 1. Re-save the logs.
  - In `mutate_matcher.sh`, the "REFUSED (mutation did not apply)" guard can never fire. `diff -rq logs mut/$name` always differs on the uncopied `mod_*.txt` files. Every mutant still demonstrably changed its input (I diffed each), so the result stands.

---

## Checked and holds (no change needed)

**The replay**
- 63 modules and 23,269 lines; the only import outside the closure is `import Mathlib`.
- Lean v4.34.1 and Mathlib d13f23b7 are the manifest pins. Mathlib came from cache.
- Build: 63/63 with rc 0 and errors 0. Every `mod_*.txt` holds only the `/usr/bin/time` line, so 0 warnings.
- Wall time 12:05:12 → 12:22:34, i.e. 17 min 22 s. Peak maxrss 7,139,132 kB = 6.81 GiB.
- `--trust=0` axioms for allDegrees are {propext, Classical.choice, Quot.sound}, and the comparator shows sorryAx. The planted-sorry control shows sorryAx.
- pp.all statement match: 8/8. The matcher's 8 mutants are exactly the ones described.
- Scan: the only `sorry` is the challenge's line 42. There is no `set_option` and there are no comments anywhere.

**The bridge**
- Main.lean#L144 is allDegrees.
- The Main.lean blob (4f47d76) and the manuscript.pdf blob (67d6339) are identical at adc7f12 and 1581d4c; the whole PowerFree directory and preprint directory diff empty. The manuscript has 55 pages.
- FC's 978.lean at a7b87c8d is identical to current main (3252e5a). sub_two is tagged "research solved" and its proof is sorry.
- The bridge is 330 lines, and its seven top-level theorems are on the standard axioms under `--trust=0`.
- The three mutants behave as described. The DeepMind polynomial does refute the no-local-condition parts.ii: degree 6, monic, Eisenstein at 3, and f ≡ x(x−1)⋯(x−5) mod 16.

**The record**
- PR #6898 was authored and merged by Moritz Firsching on 2026-10-11. Issue #7135 is open (a bot, filed 11 Oct). teorth lists 978 as open, last_update 2025-08-31.
- The live page was last edited 31 Mar 2026, shows 0 proof claims, has comments suspended, and has 0 hits for "OpenAI".
- The thread contains the DeepMind prover-agent post and Bloom's "Indeed (this has been changed)", both on 31 Mar.
- conjectures.io shows "OWNER_ACCEPTED_PUBLICATION_CLOSURE … no independent proof replay", and the quote lives in conjectures-io/conjectures-tasks.

**Sources and quotes**
- ZCJ v1 is dated 11 Aug and was withdrawn as v2 on 15 Oct, with the quoted comment verbatim. Corollary 2.4 includes D4 quartics, so x⁴+2.
- Carella's constants are 0.981003, 0.757159 and 0.963802. The "deep open problem" sentence is in Simhi's v1 of 21 Oct.
- Booker–Browning Theorem 1.2 is as stated.
- The Heath-Brown quote and the ranges hold: Nair d ≥ 24, Heath-Brown 2006 d ≥ 10, Browning d ≥ 9, binomials d ≥ 6.
- The three Erdős quotes are verbatim in W's texts.
- All arXiv, GitHub and renyi links return 200. erdosproblems returns 403, which is the usual datacenter block from exe.dev.

**Numbers**
- Counts: 75,670, 151,346, 756,674, 196,180 and 980,831 match the files. M2's blocks sum to 756,674 and 980,831. 98,090 is confirmed by my own run.
- The no-lift sieve mutant gives 65,353.
- Tail census: n = 2 (p = 3) and n = 97 (179²·2763 = 88,529,283).
- ρ(p²) formula; c = 0.756684003 (truncated at 2·10⁷, tail bound 1.2·10⁻⁸), inside July's [0.7566837026, 0.7566840053]; c₈ ≈ 0.98081747.

**M1's numbers**
- min gap 0.0019350 at z = 3555; cut margin 1.53·10⁻⁸ at z = 4902.
- Mutations 434 and 609. I re-ran these: 414 of the 434 and 601 of the 609 cells have exponent ≥ 1, so "the route breaks" is real and not just a breach of the 1/1000 buffer.
- Direct-range exponents 0.99943 (d = 4) and 0.99954 (d = 8).
- Table 1 values.

**M2 and L**
- M2: 25 quintics; bicone 10 bidegrees; first-cut component 5 bidegrees; gap − 4τ = 1941/10⁵.
- L: 100 bins; U = 1/3 and V = 2/5; savings 3/1000 and 1/2000; φ_d(1) = 2/d.

**Seats**
- All four seats served claude-opus-5-5, per `receipts.sh`.

## Summary of MUST-FIX items
1. **B1:** "first reported kernel replay" / "no earlier replay found" appears in four places and is false. cert-machine (10 Oct, Lean and nanoda) and nealmcb (11 Oct) replayed PowerFreeValues first.
2. **B2:** 24979/25000 and 3122/3125 are exponent bounds, not "worst margins".
3. **B3:** "tightest margin 0.00059" — L's checker shows d = 5 at exactly 997/1000 and d = 7 at 0.00049.
4. **B4:** "One disagreement": M1 never examined the monic issue, and the "general irreducible f" reasoning attributed to M1 is W's.
5. **B5:** "Each count was made twice": no factoring run backs n⁴+1 at 10⁵, and the July run did n⁴+2 only. The number 98,090 is right, by my run.
6. **B6:** "in each, the unsaturated weight would have given the wrong count" is false for M2's E2 (5 of the 15 runs).
