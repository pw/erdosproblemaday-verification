# B2 cold-read report — #431 page (Ostmann / OpenAI family 013)

STATUS: FINAL (2026-10-23)

**VERDICT: SHIP WITH FIXES — MUST 2 · SHOULD 8 · NIT 15**

Note on the brief: /tmp/oaimath/013/seats/B2_BRIEF.md does not exist. I followed /tmp/oaimath/013/seats/B_BRIEF.md, which is headed "seat B2".

Method: I re-derived every number on the page from the files it cites (lean-build/modules.tsv, steps.tsv, post.log, driver.log, statement_match; deps/*.log and *.lean; bridge/*; scan/hits.json; closure_*.txt; world/*; live/*; the four reports; paper.txt/PDF/bib). Scripts: B2_work/dupnames.py. I also made read-only GitHub API reads (gh search/api) to check the absence and priority claims. A side effect to declare: I ran `git log -1` and `git status` once, read-only, in /tmp/erdos0300/lean/mathlib4 to confirm the Mathlib revision and that it is clean. I touched no other repo, did not run lean, and killed nothing. The leanchecker run is still going (post.log's last line is BEGIN leanchecker_fresh_BothProbe at 09:12:00Z); per the brief I do not object to its absence.

---

## MUST

### M1. The Granville / Tao–Ziegler sentence is false as written
Page (body, after "What was known"): "Those sets put no composites in their sums, but their sums do not cover the primes, so they are not counterexamples."

Why it is wrong:
- **Granville.** The page's own previous sentence (and live/text.txt) says Granville's sets have every **(b+c)/2** prime. Every sum b + c is therefore 2·(prime), which is composite. Their sumset B + C contains no prime at all.
- **Tao–Ziegler.** Only the sums b_i + c_j with **i < j** are prime. The sums with i ≥ j are unconstrained.
- So the reason these are not counterexamples is not that "their sums do not cover the primes". It is that their actual sumsets are not even close to lying inside the primes. A number theorist will catch this in one line.

Replacement: "Neither is a counterexample: Granville's sums b + c are twice a prime, so all composite, and Tao–Ziegler control only the sums with i < j. In both, it is a restricted set of sums that is prime, not the sumset A + B."

### M2. "Neither Lean route contains a module from that family … the separate formal proof": OpenAI's own catalogue puts the Siegel-zero theorem inside family 003
Page (Sources and the world, last bullet): "Neither Lean route contains a module from that family. Route M does contain the separate formal proof that Landau–Siegel zeros do not exist (see the Lean section), which the paper does not cite." (The summary and the Lean label also call it "the release's separate claim".)

Evidence:
- OpenAI's lean/docs/003.md at 1581d4c (fetched read-only; saved as B2_work/doc003.md) is titled "The quasi-Riemann hypothesis". It lists two papers, *The Quasi-Riemann Hypothesis* **and** *Uniform exclusion of Landau–Siegel zeros*. It describes the formalized "uniform logarithmic exclusion region for Landau–Siegel zeros … 1−β ≥ c/log q", and its comparator table includes SiegelZeros.lean.
- world/CONTENTS.md lines 66–93 list "Uniform exclusion of Landau–Siegel zeros" under "003. The quasi-Riemann hypothesis". The family's alternate QRH abstract says "In particular, this rules out the existence of Landau–Siegel zeros".
- The page's own link label reads "OpenAI's Lean doc 003 — the quasi-Riemann hypothesis and 'Uniform exclusion of Landau–Siegel zeros' (comparator SiegelZeros)".

What is true and what is not:
- The literal module claim holds. The closure files contain no OAI.NumberTheory.SiegelZeros.* or DirichletL.* module.
- But route M rests on a second formalization (Jacobsthal/Siegel, 105 modules) of a family-003 theorem. gh code search shows the parallel copy lean/OAI/NumberTheory/SiegelZeros/Characters/DirichletRealZeroBound.lean. Calling it "separate" from family 003 contradicts OpenAI's catalogue and the page's own link.
- It also understates the finding. Remark 5.4 declines family 003's zero-free theorem; route M uses family 003's Siegel-zero theorem, which QRH would also imply.

Replacement: "Neither Lean route imports family 003's own Lean: there is no SiegelZeros or DirichletL module in either closure. Route M does rest, through a second formalization housed in OpenAI's Jacobsthal directory, on the theorem of family 003's companion manuscript, 'Uniform exclusion of Landau–Siegel zeros', which the paper does not cite. So Remark 5.4 declines family 003 and route M uses it." In the summary and the Lean label, "the release's separate claim" should become "a claim from the release's family 003 (uniform exclusion of Landau–Siegel zeros)".

---

## SHOULD

### S1. "without lake … and an unmodified Mathlib": Mathlib was not rebuilt from source
Page (Our replay): "We rebuilt the whole closure from source on our own machine, without lake: … and an unmodified Mathlib at d13f23b, the revision OpenAI pins."

Evidence:
- lean-build/cacheget.sh runs `lake exe cache get` in /tmp/erdos0300/lean/mathlib4. cacheget.out says "Decompressed 8907 already-cached file(s) … exit 0 06:08:34Z". lean_path.txt points at those cached oleans.
- The Mathlib source is unmodified: d13f23b, and `git status` shows only the untracked LAKE_DELETED.txt. But Mathlib's declarations were not compiled or kernel-checked on our machine. Only the pending leanchecker --fresh would re-check them.
- This matters because the no-Siegel-zero check trusts Mathlib's cached olean for DirichletCharacter.LFunction.

Replacement: "We compiled every module above Mathlib from source, without lake: 7,582 modules from OpenAI's tree at 1581d4c (…) and its pinned PNT+, StrongPNT and AINTLIB with OpenAI's 4.34.1 patches. They compile against Mathlib d13f23b, the revision OpenAI pins; its source is unmodified and its oleans come from Mathlib's own cache (lake exe cache get). Mathlib itself is re-checked only by the leanchecker pass below."

### S2. "§5 is where coverage enters" contradicts the page's own §2 and R1 bullets
Page (argument): "§5 is where coverage enters."

Evidence:
- The page's own §2 bullet uses coverage ("too few to cover the ≍ Y/log Y primes").
- R1's bullet says "coverage supplies π(Y) ≤ |A|·B(Y) + O(1)" and "without coverage it loses Lemma 2.4's lower bound, which the moment step needs".
- The paper says "Prime coverage enters **separately** in Section 5 … This comparison retains the coverage information beyond the preliminary lower bounds for the summands" (p. 3, paper.txt l.108–112). Coverage is also used at paper l.258, 300, 305 (§2).

Replacement: "§5 is where coverage enters again, beyond the size bounds of §2."

### S3. "Route C is the paper, formalized" overclaims, and the shared modules are mislabelled
Page (The Lean): "Route C is the paper, formalized." Also: "the definitions and statement (Defs, Statement, Endpoint, FiniteCRT, FiniteFactor)". Also: "route C is the formal proof that corresponds to the paper".

Evidence:
- FiniteFactor.lean (`finite_factor_impossible`) and FiniteCRT.lean (`separatingPrime`) are the finite-summand reduction, Lemma 2.2. They are not definitions or statement. Both routes share them, and route C's FiniteSummands.lean ("Lemma 2.2") imports FiniteFactor.
- R1 (§3, "Cited sources") reports that the Lean follows the Laffer–Mann/Dirichlet–CRT route, not the paper's sieve proof of Lemma 2.2.
- The page itself says route C avoids the §4 Kneser step by a route "we did not trace".
- L's table, row 1, says the Lean takes MV Cor. 11.20 directly where the paper derives (8.8).

The architecture and the analytic inputs do follow the paper. "The paper, formalized" is still too strong.

Replacements:
- "Route C follows the paper and formalizes every analytic input the paper cites. It departs in small places: Lemma 2.2 is proved by a CRT argument, in modules both routes share, rather than the paper's sieve, and the §4 Kneser step is avoided by a route we did not trace."
- Shared modules: "the definitions and statement (Defs, Statement, Endpoint) and the finite-summand reduction (FiniteCRT, FiniteFactor)".

### S4. R1 did not "rebuild" Heath-Brown's quadratic large sieve
Page (reading, R1 bullet): "R1 rebuilt §3 step by step: …, the common rational centre, Heath-Brown's quadratic large sieve, the exceptional-zero step and the final collision count."

Evidence: R1 §4 says: "Heath-Brown 1995 … Theorem 1. The PDF was not retrievable. I relied on the Lean transcription plus memory." R1 checked the use at (3.28) and the signed/even extension. It did not check the theorem against its source.

Replacement: "… Heath-Brown's quadratic large sieve as used at (3.28), compared with the Lean's transcription because the 1995 paper could not be retrieved, …"

The same caveat applies to the Lean-section phrases "(1995, Theorem 1, full statement)" and "Montgomery 1969, as stated by Inoue". L §4 says L did not open those sources either. The page says "read each input against the paper's citation", which is accurate, but a reader will take "full statement" as source-checked. Add "(compared with the paper's citation; the sources were not opened)".

### S5. "every name spelled _root_." is not what deps/SiegelStmt.lean does
Page: "So we wrote the statement ourselves at the root namespace, every name spelled _root_. so that it can only be Mathlib's: DirichletCharacter.LFunction …, IsPrimitive, Real.log."

Evidence:
- In deps/SiegelStmt.lean only `_root_.DirichletCharacter`, `_root_.DirichletCharacter.LFunction` and `_root_.Real.log` carry the prefix.
- `χ.IsPrimitive` is dot notation, which resolves to DirichletCharacter.IsPrimitive. `ZMod`, `NeZero` and `(χ a).im` are bare.
- The faithfulness argument still holds: the file has no `open` or `namespace`, the #check output under pp.fullNames shows root names, and no OAI file declares an `LFunction` (I re-grepped repo/lean and ext). But the sentence describes the file wrongly, and this paragraph is exactly what a Lean expert will open.

Replacement: "… written at the root namespace, with no `open`, the type and L-function written `_root_.DirichletCharacter` and `_root_.DirichletCharacter.LFunction`, and the logarithm `_root_.Real.log`. `IsPrimitive` is reached by dot notation on that type, so every name resolves to Mathlib's."

### S6. Path lengths are off by one ("28 steps", "29 steps")
Page: "From OAI.Ostmann.main it reaches dirichlet_real_zero_bound in 28 steps". Also "#970 … reaches dirichlet_real_zero_bound in 29 steps". The #970 update says "The chain has 29 steps."

Evidence:
- deps/ProbeM.log prints "path length 28" and lists 28 constants, main through dirichlet_real_zero_bound. That is 27 steps. DepProbe.lean's `path.length` counts nodes.
- Probe970.log likewise: "path length 29" is 29 constants, 28 steps.
- The mismatch shows on the page itself: L's "25 links from actual_no_decomposition" equals the probe's edge count from actual_no_decomposition to the wrapper. 1 + 25 + 1 = 27, not 28.

Replacement: "a chain of 28 constants (27 steps)" and, for #970, "29 constants (28 steps)", in both the #431 page and the #970 update.

### S7. Card: "A and −B occupy disjoint halves of every 𝔽_p"
Page (CARD LINE): "A sum a + b ≡ 0 mod p would be composite, so A and −B occupy disjoint halves of every 𝔽_p."

Evidence:
- Disjointness holds for every p, and only for large elements, where a + b > p. The "about half each" holds only on prime averages: paper p. 2 ("on suitable prime averages"), Lemma 2.5, and R1's "Chebyshev deletion" note.
- "Halves of every 𝔽_p" is precisely the average-to-every-prime slip that the page tells readers the referees checked for.

Replacement: "A large sum a + b ≡ 0 mod p would be composite, so the large elements of A and −B occupy disjoint parts of every 𝔽_p, about half each on average over p."

### S8. Importing both bridges silently drops one copy of each theorem
Page (Ours): "A single file importing both routes also compiles, so the two developments coexist in one environment." The pending bullet reads "leanchecker --fresh over a file importing both routes".

Evidence:
- Bridge431C.lean and Bridge431M.lean both declare `Erdos431.erdos_431` and `Erdos431.erdos_431.variants.ostmann`, with identical types.
- Lean 4.34.1's `finalizeImport` (toolchain src/lean/Lean/Environment.lean l.2268–2343, `subsumesInfo`) accepts a duplicate theorem when name, type and level parameters agree, and keeps only one copy. That is the later import, so probably route M's.
- LeanChecker.lean `replayFromFresh` replays `env.constants`, which is that deduplicated map.
- So BothProbe's `#print axioms Erdos431.erdos_431` and the pending leanchecker pass see one bridge proof, not two. Route C's own theorems (inverseGoldbach, twoInfiniteSummandsImpossible) are still in the environment and will be re-checked. My textual scan (B2_work/dupnames.py) found 0 other same-named declarations between the C-only and M-only modules, so the developments themselves do coexist.
- The sentence is true. The leanchecker line, when filled in, must not imply that both bridges were re-checked.

Replacement: "A single file importing both routes also compiles: the two developments coexist in one environment. Lean merges our two identically-stated bridge theorems into one copy there, so the leanchecker pass below re-checks both developments and one bridge. Each bridge was kernel-checked when it compiled." Alternatively, run leanchecker on Bridge431C and Bridge431M separately.

---

## NIT

1. **Laffer–Mann page range.** The link reads "Pacific J. Math. 14 (1964) 547–561". It is 547–558: paper bib, paper.txt l.4727–4728, and R1_work/lm.txt, whose next article, Lindberg, starts at 559.
2. **"no single process went above 7.3 GiB."** The maximum in modules.tsv over the 7,582 modules is 7,693,536 kB = 7.34 GiB. Write "peaked at 7.34 GiB".
3. **"A planted file with a sorry, compiled the same way, reports sorryAx."** post.sh compiles Neg.lean without `--trust=0`; only the Ax probes use it. Write "a planted sorry, compiled against the same build, reports sorryAx".
4. **Controls attributed to the wrong probe.** The page says: "A constant on route C's path is reached as a positive control, and a constant declared beside the probe and never used is not reached." The unused-constant negative control is in ProbeM/Probe970, not ProbeC. Route C's namespace count is a separate walk, and its real positive control is its own count of 113 constants under OAI.LargePrimeGaps. Say so.
5. **"the proof gets (log)^10".** L table row 3: only for σ ≥ ½ + 1/log Q²T, with a trivial count below. Write "the proof gets (log)^10 in the range that matters".
6. **"deleting that prime from every prior".** R3: "from every **nongiant** prior".
7. **"(384 against the bound's 384)".** The 384 is the counting sum inside the proof of (9.1), not the displayed (9.1) bound (L §3c). Write "against the 384 allowed by the counting step in (9.1)'s proof".
8. **"the Lean proves it as infinitely_many_composite_sums".** That theorem is in Corollaries.lean, built on `_root_.OAI.Ostmann.main`, so it is route M's and rests on the no-Siegel-zero theorem. Add "(in route M's Corollaries.lean)".
9. **"Both statements are the theorem as the page asks it."** OstmannPrimes states Theorem 1.1, which is stronger than the problem page's two-infinite-sets question. Write "Both state Theorem 1.1; OstmannComplete also states Theorem 2.3, the problem page's question."
10. **"nealmcb's report lists the two closure sizes (3,207 and 4,358 modules)".** REPORT.md has 3,207 (l.221). 4,358 is only in the configs CSV (world/nealmcb_configs.csv l.416). Write "nealmcb's sweep data lists".
11. **Unbanked evidence.** The teorth database "current to its 22 October commit" has no commit metadata in world/teorth_problems.yaml. The GitHub searches behind "We found no earlier record…" are not banked in world/ either; gh_search.txt holds only the challenge-name and erdos_431 searches. I re-ran them: `dirichlet_real_zero_bound` hits only openai/math (both the Jacobsthal/Siegel and SiegelZeros copies) and a mirror, kbr-/math-research; "OstmannPrimes Siegel", "Ostmann Landau-Siegel" and "Ostmann dirichlet_real_zero_bound" return []. Bank the queries.
12. **"25 links from actual_no_decomposition to the theorem".** L's chain ends at the wrapper `dirichletRealZeroBound_proof`, one step short of `dirichlet_real_zero_bound` (L B.4). Write "to the theorem's wrapper".
13. **Weak false-strengthening controls.** "Two false strengthenings fail to compile". Bridge431CMutDropB fails on "Unknown identifier `hB.nontrivial`", a script error that Lean hits before it ever meets the false goal. The Nonempty mutants fail at an application type mismatch. These are true "fails to compile" results but weak controls. Optional wording: "fail to compile (as any proof of a false statement must)".
14. **"That is a formal proof that Landau–Siegel zeros do not exist, and it checks."** Given the size of the claim, say in this paragraph what "checks" means: compiled from source and kernel-accepted on our machine, Mathlib from its official cache, from-scratch leanchecker pending.
15. **#970 update wording.** "the Lean is a second proof of Theorem 1.1, not a formalization of the paper's §10 input" reads garbled. Suggest "the Lean is a second proof of Theorem 1.1 that replaces the paper's §10 input (classical Siegel–Walfisz) with a far stronger one". "An estimate for primes in short progressions" is `interval_AP_li_error`, i.e. primes of a progression in an interval.

---

## Checked and correct (so the next reader need not redo it)

**The replay.**
- 7,582 modules, 0 errors, rc 0: modules.tsv joined with all_order.txt.
- Σ wall 99,882.5 s, 27.7 h.
- 06:08:58Z to 09:09:03Z, W ≤ 12.
- Commit 1581d4c: repo/.git/refs.
- Mathlib d13f23b is both the pin (lake-manifest) and the checkout.
- Statement match: 7/7 and 1/1, ALL_MATCH. The Nat.Prime → Nat.Coprime mutant gives FAIL.
- Axioms are exactly the standard three for all three headline theorems. Neg gives sorryAx.

**Closures.**
- C = 3,207 OAI modules, M = 4,358, shared 47 (5 Ostmann + 42 PrimeGaps).
- Union 7,518 OAI modules (Ostmann 7,335, Jacobsthal 135, PrimeGaps 48). Route C has 0 Jacobsthal modules; route M has all 105 Jacobsthal.Siegel modules.
- Every Siegel-directory declaration sits inside `namespace OAI` / `Erdos970`; Main.lean is imports only. No `_root_` declarations.
- 7,716 Ostmann files.

**The no-Siegel-zero theorem.**
- Statement bridge, axioms, and both mutants rejected: deps/SiegelStmt.log and the two mutant logs.
- Mathlib's LFunction is defined through hurwitzZeta (ZMod.lean l.85).
- No OAI or ext declaration is named `LFunction`.
- The #970 morning replay (/tmp/oaimath/021) compiled the same 105 Siegel modules: same sha for DirichletRealZeroBound.
- The probe paths and the 99,798 / 99,655 counts match the logs.

**Scan and bridges.**
- The scan claims match scan/hits.json: sorry 2 + 1 in the comparators only; the partial def and two syntax declarations in AdditiveCombination; one attribute [-instance].
- Bridges compile clean; the verbatim check passes and its mutant fails; the sorry mutants show sorryAx.

**The referee summaries.** Every R1/R2/R3/L summary sentence matches its report except S4 and NITs 5–7 and 12. All quoted numbers match: 6e−12 and 91.6; 2e−10 and 2.3–4.0; multiplicity 8; 384; 24 vs 10.9; exp(e^{.012L}). Printed locators were checked against the PDF: p. 74 (9.1), p. 76 (9.6)/(9.8), p. 66 Lemma 8.1/(8.9), p. 56 (7.2), p. 31 (4.12), pp. 13/15, p. 44 Remark 5.4.

**The world.**
- Bloom's quote and date (world/bloom_blog10.html: "infinitely many composite numbers in A+B, and infinitely many primes not in A+B"; "not yet looked at in any serious way"; 25 problems; FrontierMath list).
- Plasma's quotes.
- atimics wording and date: 2026-10-08, commit 0fe7b23, Redundancies.lean l.9–10.
- cert-machine: 3,528 s and 10,338 s, both kernels, committed 2026-10-10.
- nealmcb: OstmannComplete and OstmannPrimes accepted 10 Oct, OstmannPrimes in the nanoda table, SiegelZeros accepted 2026-10-11T18:46Z.
- FC PR #6898 merged 2026-10-11T08:10Z. The FC links go to Complete.lean#L16 and Result.lean#L14.
- Only the initial commit (adc7f124, 6 Oct) touches the Ostmann Lean, the preprint, Jacobsthal/Siegel, or OstmannPrimes.lean.
- The problem page: no claims or comments, "The ability to post new comments has been suspended", last edited 8 April 2026, no OpenAI mention.
- teorth: open, 2025-08-31.
- Epoch: $300 budget, sorryAx, scored I.
- The other GitHub hits (grandchallenge editorial, ryantuck AI reviews, lean-genius, TheJustinSunPrize) contain no expert assessment and no independent proof.

**The mathematics on the page.**
- Example: A = {1,3}, B = {2,4} gives A + B = {3,5,7}.
- The two readings of Theorem 1.1 are equivalent. Infinitely many non-primes is the same as infinitely many composites, since only 0 and 1 differ.
- Theorem 1.1 and its ℕ₀ convention match the paper.
- Remark 5.4 is quoted verbatim.
- The paper's only OpenAI citation is QRH; it does not cite the Siegel-zero preprint.

---

## The sentence I would bet is wrong

"Those sets put no composites in their sums, but their sums do not cover the primes, so they are not counterexamples." Granville's construction makes (b+c)/2 prime, so every b + c is twice a prime: his sumset is entirely composite and contains no prime. Tao–Ziegler control only the i < j sums. The sentence is false for the first example and unsupported for the second. It also gives the wrong reason these are not counterexamples, and any number theorist who knows Granville's construction will see it at once. The family-003 sentence (M2) is the subtler error. It is literally true about module paths, but OpenAI's own docs/003.md, and the page's own link label, put the Siegel-zero theorem inside the family the page says route M does not touch.
