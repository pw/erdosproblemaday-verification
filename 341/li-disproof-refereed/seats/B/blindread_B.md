# Blind consistency read B — /day/341-li-disproof-refereed

Read: /tmp/erdos2100/render341.txt (whole page). ⟨REFEREE⟩/⟨BLINDREAD⟩ ignored.
Re-ran: `check_li.py 10000000` (ALL PASS, rc 0), `mutate_check.py` (4/4 FAIL as intended), the four `certify.py` runs quoted on the page (outputs below), plus my own probe `/tmp/erdos2100/seats/B/distinct_gap.py`.
Note: `mutate_check.py` writes `/tmp/erdos2100/_mut.py` by design, so running it rewrote that file with the same content. I also launched `leanchecker --help` once by mistake (with no module argument it starts replaying every olean). I killed it by PID after ~1 min. The running `--fresh` job (pid 818040) was not touched.

---

## SUBSTANTIVE

**S1. Three wrong theorem numbers.**
Page: "(the "shield", Lemma 3.2)", "Together (Theorem 3.3): for every t > 97…", "so no period h survives past 8k > h (Lemma 2.3)".
Artefact: `pdftotext paper/Erdos341.pdf` (and the TeX's shared section counter) numbers them as follows. Lemma 2.1 is the controller identities, **Lemma 2.2** is Y0 not ultimately periodic, **Lemma 3.1** is the finite shield, and **Theorem 3.2** is the recurrence t∈S ⇔ t∉S+S. Lemma 1.2 and Lemma 4.1 are cited correctly. A Lemma 3.2, a Theorem 3.3 or a Lemma 2.3 does not exist.
Fix: Lemma 3.2 → **Lemma 3.1**; Theorem 3.3 → **Theorem 3.2**; Lemma 2.3 → **Lemma 2.2**.

**S2. The replayed commit is not the Zenodo version the page names.**
Page: "repository LiAlreadyExists/Erdos-341, commit c1d9121 of 20 August 2026; Zenodo DOI 10.5281/zenodo.22030511, v2.0.1, same day". Sources: "Zenodo record of the formalization, v2.0.1 (20 Aug 2026), DOI 10.5281/zenodo.22030511".
Artefact:
- The GitHub tags API gives `v2.1.0 → c1d9121` and `v2.0.1 → 4583844`.
- Zenodo `…/22030511/versions` gives v2.1.0 = record **22030579** (created 14:03:34Z, "add lean") and v2.0.1 = 22030511 (13:58:38Z).
- `zenodo_22030511.json` itself has `relations.version[0].is_last = False`.
- `compare/4583844...c1d9121` shows only `paper/Erdos341.tex` (+2 lines: the "Formal verification" sentence) and the PDF changed. **The Lean files are byte-identical**, so the replay result stands; only the provenance is wrong.
Fix: "commit c1d9121 (tag v2.1.0, 20 Aug 2026; Zenodo 10.5281/zenodo.22030579). The paper cites the v2.0.1 record 10.5281/zenodo.22030511, whose Lean files are identical." Update the Sources label the same way.

**S3. "Closed in the literature" overclaims.**
Page: "The problem is closed in the literature, by a reader with a model, two months ago, and nobody had refereed it in public." (The HEADLINES tag in `apply341.py` also says "CLOSED IN THE LITERATURE".)
Artefact: no journal or arXiv version exists. The paper is a GitHub PDF plus a Zenodo *software* deposit (`resource_type: software`). My arXiv API and MathOverflow API searches returned nothing. A number theorist will read "in the literature" as "published", and the page says itself that nobody had refereed it.
Fix: e.g. "A complete disproof, with a Lean formalization, has been public since August (a GitHub/Zenodo preprint, not refereed), and nobody had refereed it in public."

**S4. The leanchecker sentence implies more coverage than the run gave.**
Page: "leanchecker re-checks both modules (46 s; a non-existent module exits 1)".
Artefact:
- `leanchecker_driver.sh` ran `leanchecker LeanProject.Erdos341 LeanProject.Erdos341g`.
- In the toolchain source (`src/lean/LeanChecker.lean`), non-fresh mode replays only the *new* declarations of the named modules on top of their imports (matched by `Name.isPrefixOf`, and `LeanProject.Erdos341` is not a name-prefix of `LeanProject.Erdos341Shield`).
- `Erdos341.lean` line 1 is `import LeanProject.Erdos341Shield`.

So **Erdos341Shield**, which holds the 17 `decide` calls (the page itself calls it "the kernel-decided residue certificate"), was never replayed by leanchecker. Only the still-running `--fresh LeanProject` pass covers it. The page counts "three first-party sources" in the scan sentence and "both modules" here, which a reader will take to mean the whole development was replayed.
Fix: "leanchecker (non-fresh) replays the declarations of Erdos341 and Erdos341g on top of their imports (46 s); Erdos341Shield is covered only by the --fresh pass below."

**S5. The Queneau mechanism is misstated.**
Page: "The construction needs the diagonal sums 7 + 7, 14 + 14, 28 + 28, and those are exactly what the distinct-index rule forbids."
Artefact/maths: 7+7, 14+14 and 28+28 here are *residue* sums (Lemma 3.1's diagonal pairs in P×P). Queneau's rule forbids only *index* repetition x + x. It does not forbid (49u+7)+(49v+7) with u ≠ v, which is still allowed and lands on the 14-rail. What breaks is narrower: the controller identities lose the self-sums. For example 63 = 49·1+14 is the only 14-rail element with quotient 1, so 126 = 63+63 is no longer represented, and 126 joins the 28-rail. The first differences between the two greedy runs bear this out: `li_eq` vs `li_dist` symmetric difference below 400 is {126, 203, 210, 371, 399}; 126 = 63+63, and 203 = 126+77 propagates it. In interval terms, distinct sums of [a,b]+[c,d] lose the endpoints 2a and 2b when the intervals coincide, and lose {0}+{0}, so Y1 = (Y0+Y0)^c etc. fail.
Fix: "The controller needs the self-sums x + x on the rails (e.g. 63 + 63 = 126 keeps 126 off the 28-rail); Queneau's rule drops exactly those, which shifts the endpoints of every Y + Y and breaks the three controller identities. The two runs first differ at 126."

**S6. The distinct-rule certificate is not the July lemma "unchanged" (proof gap; the conclusion survives).**
Page: "our July finite certificate (the lemma on /report/341, unchanged: check the recurrence … through 2N + q − 2 = 12,459 and the identity E + R = ℤ/qℤ ∖ R …) proves it periodic forever". Labels: "The two Queneau-rule periodicity certificates …: (a) the lemma".
Artefact:
- The July lemma (ledger_data.js `n:341`, also `runs/erdos341_wave8u.md`) is stated and proved for T+T with equal summands.
- `certify.py`'s docstring extends it to the distinct rule with this argument: "we may take them distinct unless e=r and only one tail element of that residue is ≤ x — impossible since x ≥ 2N+q−1 ≥ N+(N+q) gives two."

That argument is wrong. Take x ≥ 2N+q−1 with x mod q ∉ R, whose only witness is e = r ∈ R, and let u0 ∈ [N, N+q) be the tail element of residue e. If x = 2u0 (possible whenever u0 ≥ N + (q−1)/2), the only pair of tail elements of residue e summing to x is (u0, u0). The next one, u0+q, would need a partner x−u0−q = u0−q < N. Having two tail elements of residue e below x does not help, because their sum is not x. So the distinct-rule lemma needs one more hypothesis:
- either every residue outside R has a witness with e ∈ P mod q or with e ≠ r,
- or the recurrence must be checked through **2N+2q−2** instead of 2N+q−2.

I checked both certificates against the corrected lemma (`seats/B/distinct_gap.py`):
- Li seed, distinct rule: zero residues with only a diagonal witness; recurrence clean through 2N+2q−2 = 18,192; the proposal matches the greedy run on [1, 9,999,991] with 0 mismatches.
- Square seed, distinct rule: zero only-diagonal residues; clean through 134; 0 mismatches to 1,999,989.

So the periodicity claims are true, but the cited proof is not "unchanged".
Fix: state the distinct-rule version (check through 2N+2q−2, or add the residue condition) and say both certificates pass it. Correct the `certify.py` docstring. Until that is done, "(a) the lemma" is wrong for the Queneau certificates.

**S7. The square seed is not one of the seeds in [12].**
Page: "certified every nonempty seed in [12] except one (4,094 of 4,095, including {1, 4, 9, 16, 25}'s 1,176/224 tail exactly)".
Artefact: 16, 25 ∉ [12]. The July report keeps them separate: "certified the exact 1176/224 square-seed tail **and** 4094 of 4095 seeds in [12]". Any reader will catch this.
Fix: "certified the square seed's 1,176/224 tail exactly, and every nonempty seed in [12] except one (4,094 of 4,095), leaving E = …".

**S8. The family theorem's statement was not matched, and part of it is not formalized.**
Page (Labels): "Li's Theorem 1.1 and the family theorem: (d) computer-assisted — kernel-checked by the author and replayed here with the statement matched". Also "§5 gives an infinite family Ap (… with 7p − 20 elements …)".
Artefact:
- `audit.log` prints pp.all definitions only for the `Erdos341` namespace. For `Erdos3417p` it prints only `#print axioms`; `Erdos3417p.Seed p`, `S p` and `M p` were never printed or compared with the paper's (25).
- Li's README says: "The separate elementary cardinality identity `|A_p| = 7p - 20` is not part of this formalization."
- The Lean family theorem (`Erdos341g.lean:871`) contains no cardinality clause.
Fix: "Theorem 1.1: … replayed here with the statement matched. Theorem 5.1: kernel-checked and replayed (axioms only); its seed predicate was not matched against (25) here, and the count 7p − 20 is not formalized (author's README)."

**S9. "A model found the construction" is unsupported by the disclosure and contradicts the page.**
Page: "A model found the construction; a human and a kernel checked it". Earlier: "Li's counterexample is designed, not found".
Artefact: Li's disclosure, quoted on the same page, says only "developed with assistance from OpenAI's GPT-5.6 Sol". Nothing on disk says who found the construction. The page then says both "designed, not found" and "a model found".
Fix: "Li developed it with GPT-5.6 Sol's assistance; Li and a kernel checked it; …".

**S10. "A second human and a second kernel now have": wrong on both counts as written.**
Page: "…a second human and a second kernel now have."
Artefact:
- This referee report was produced by Claude seats. The same release's HEADLINES tag in `apply341.py` reads "UNREVIEWED BY HUMANS", which contradicts "a second human".
- plby/lean-proofs re-hosted Li's development on Lean v4.33.0 / Mathlib v4.33.0 (header of `plby/Erdos341.lean`, Revision c1d9121), and Formal Conjectures links that build as `formal_proof` since 18 Sep. On its face that is already an independent kernel build on a different toolchain, so ours is not "the second kernel".
- "nobody had refereed it in public" can stand: there are no comments on the claim and no written report anywhere.
Fix: e.g. "…; plby re-built it on Lean v4.33.0 and Formal Conjectures' curators linked it; this entry is the first public referee report, with a further kernel replay."

---

## MINOR

**M1. Quotation not verbatim.** "Green's "both variants appear to be open"". Green (`green.txt` l.~221) actually says: "For both variants, the following question appears to be open". Either quote it exactly or drop the quotation marks.

**M2. Garbled sentence and odd notation.** "Why 7, 14, 28: these are the only pairs of rails whose sums land on a rail, and they do so only diagonally — … 28 + 28 = 49 + 7 (mod 49)". "these are the only pairs" has no referent, and "= 49 + 7 (mod 49)" mixes an integer identity with a congruence. Lemma 3.1 says: the only ordered pairs in P×P whose sum lies in Q are the three diagonal ones. Suggested: "Of all pair sums of rail residues, only the diagonal ones land in Q: 7+7 = 14, 14+14 = 28, 28+28 = 56 ≡ 7 (mod 49)". Also, the "why" is the doubling loop: 8·7 ≡ 7 (mod 49).

**M3. Class counts exclude the seed.** "the five B-classes each holding 204,079–204,080 terms and the rails 91,734 / 74,903 / 37,453". `li_eq_1e7.log`'s census covers elements > 97 only. 5 B-classes + rails = 1,224,487, which is 21 short of 1,224,508. With the seed included, the B-classes hold 204,081–204,082 and the rails 91,735 / 74,904 / 37,455. Add "above 97".

**M4. Shield checks miscounted.** "(41 residues covered, the three avoidance identities, the diagonal-pairs claim)". `check_li.py` [2] checks one cover identity (41 residues), **one** avoidance identity (Q ∩ (B+B ∪ P+B ∪ D+B ∪ D+P) = ∅), (P+P)∩Q = P, and the diagonal-pairs claim. Write "the cover identity (41 residues), the avoidance identity, (P+P)∩Q = P, and the diagonal-pairs claim".

**M5. The Y0 mutation widens every block, not one.** "widen a Y0 block". `mutate_check.py` replaces `blocks(4,8,q)` with `blocks(4,9,q)`, which widens every block [4·8^k, 8·8^k) to [4·8^k, 9·8^k). The 4,681 count is 1+8+64+512+4096, i.e. five blocks. Write "widen every Y0 block by 8^k".

**M6. "5,040 sums" is a residue count.** "706 + 693 residues, 5,040 sums". `certify.py` reports |E| = 706, |R| = 693, |E+R| = 5,040 = 5,733 − 693 residues. Write "|E| = 706, |R| = 693, |E+R| = 5,040 residues = ℤ/5733 ∖ R".

**M7. The audit prints less than the page says.** "Our own audit file prints, with pp.all, the final theorem and every definition it rests on". `Audit341.lean` applies `pp.all` only to the theorem and five definitions (GreedyExtension, LeastGreedyStep, PrefixPairSum, EventuallyPeriodic, PairSum). Seed, S, enumeration, gap, enumOf and gapOf are printed without pp.all. D, B, residue, Y0–Y2, Pow8 and Nat.nth are not printed at all. This is harmless for fidelity, because GreedyExtension Seed S 97 pins S uniquely, but the sentence overstates. Write "…the final theorem and the definitions its statement uses (S's internals don't matter: GreedyExtension pins S)".

**M8. teorth row misdescribed.** "teorth database says OPEN (last update 31 August 2025, "unformalized")" and "teorth database: OPEN, last touched 31 August 2025". The row has `status/informal_status: open, last_update 2025-08-31`, `formal_status: unformalized` (meaning no formal *proof*), **and** `formalized: {state: yes, last_update: 2026-01-22}` (the statement is formalized). So "last touched 31 August 2025" is false, and quoting only "unformalized" misleads. Write "status OPEN (last status update 31 Aug 2025; formal proof: none recorded)".

**M9. "(15:32 UTC)" is unverified.** The claim shows "Submitted 2026-08-09 15:32:18" with no timezone. Drop "UTC" or establish the site's clock.

**M10. "still reads as open".** The captured page shows no status at all (`problem-text id=neutral`; the site stopped displaying statuses). Write "shows no resolution (the site no longer displays a status)".

**M11. Cache timing omits the failed first attempt.** "a tagged release, so lake exe cache get fetched 8,643 files in 52 s". `steps.tsv` shows the first `cache_get` failed (rc 1 after 103 s); the 52 s is the relaunch, possibly with a warm cache. v4.33.0-rc1 is a release-candidate tag, and the "so" is not really causal (CI caches exist for any mathlib commit). It is true as logged; consider "after one failed attempt".

**M12. Green's Problem 7 is Ulam's sequence.** "Problem 7 on Green's list" / Sources "Problem 7 (Dickson's rule vs Queneau's variant)". Green's Problem 7 is Ulam's sequence; Dickson and Queneau appear in its Comments ("A (somewhat) related class…"). Write "discussed in the comments to Problem 7".

**M13. Two overstatements in the statement match.**
- "LeastGreedyStep enumeration j … is Erdős–Graham's sentence verbatim". It is a faithful formal encoding, not verbatim.
- "the cast is a one-line argument". It is a short lemma, not one line: IsLeast over ℤ, the ∀ᶠ, and ℕ-subtraction versus ℤ-subtraction (fine by strict monotonicity). Say "short".

**M14. "What is left" (1) is loose.** "the modulus 49 = 7² and the loop 7 → 14 → 28 → 7 come from 2 having order 3 mod 7, so a smaller modulus with the same loop (21, say)…".
- A 3-cycle under doubling, r → 2r → 4r → 8r ≡ r (mod M), forces only M | 7r, so only **one** factor of 7 comes from ord₇2 = 3. The other 7 is Li's free parameter: his §5 family is modulus 7p with rails p, 2p, 4p, and the main example is p = 7.
- The smallest modulus with the loop is 7 (rails 1, 2, 4); "21, say" is arbitrary.
- "Lemma 1.2 plus a finite shield is all a candidate needs" leaves out that the controller Y0–Y2 must also carry over. It does, unchanged, whenever 4r+4r = M + r gives the same +1 carry. The seed must also equal S ∩ [1, 2M−1].
Reword.

**M15. "What is left" (4).** "Erdős's question for seeds that are themselves sum-free, Calkin–Finch's setting". No artefact attributes a sum-free-seed question to Erdős. The July report ties the sum-free literature to Calkin–Finch/Cameron, and EG p.53 has no such clause. Also "the family Ap does not obviously settle" can be made definite: for every p ≥ 18, 1, 3, 4 ∉ F_p (by (24)), so 1, 3, 4 ∈ D_p ⊂ A_p and 1 + 3 = 4. No A_p is sum-free.

**M16. D is only part of the seed.** "Seven small integers D = {1, 2, 5, 13, 27, 36, 47} are in by fiat (the seed)". The seed is D ∪ B ∪ (49+B) ∪ {7, 28, 63, 77} (paper eq. (21)). Write "(part of the seed)". Note also that the paper says "B-rail" too; the page reserves "rails" (in quotes) for P only.

**M17. Not everything else is mod-49 arithmetic.** "Everything else is a finite check in ℤ/49ℤ". Theorem 3.2's r ∉ Q case also needs the small representatives 7, 63, 28 to be in S (controller initial values 0∈Y0, 1∈Y1, 0∈Y2), q ≥ 2 to absorb carries ≤ 1, and D+D ≤ 94 < t. This is small integer bookkeeping, not ℤ/49ℤ. Write "a finite check (mod 49 plus a few small carries)".

**M18. The claim predates the refereed version.** "submitted 9 August … : Counterexamples to Erdős Problem 341, a seven-page paper (… commit c1d9121 of 20 August 2026 …)". The claim links to `blob/main`, which has been revised since: Zenodo v1.3.0 (16 Aug) "Adding generalized version", v2.0.0 (20 Aug) "add generalization section". The §5 family postdates the claim. Say "we referee the paper at main = c1d9121 (20 Aug), which the claim's link now points to".

**M19. Unverifiable here.** Labels: "the one tool-equipped hostile seat found no gap". This must agree with ⟨REFEREE⟩ when filled; I did not read the referee report (blind seat).

**M20. Placeholder must be updated.** "A leanchecker --fresh pass … is running as this is written". It is still running: pid 818040, started 21:27:18Z, no `leanchecker_fresh_LeanProject` row yet. Update before publishing, or keep the hedge.

---

## Counts
**SUBSTANTIVE: 10** (S1–S10). **MINOR: 20** (M1–M20).

## Verified clean (checked against artefacts)
- **Numbers from our greedy run** (`li_eq_1e7.log`): 1,224,508 terms, density 0.122451 ≈ 6/49, largest gap 19.
- **Period structure of that run:**
  - The last-quarter suffix (gap index 918,380 = integer 7,499,947, q = 153,060) has smallest period 6, inside Y0 block [131072, 262144) where Y1 and Y2 are both off (rails constant).
  - The last-half suffix (612,254 gaps) has no period at all, so "no period up to 306,127" is true (understated).
  - `greedy341.c` is 47 lines.
- **`check_li.py`:** |S| = |greedy| = 1,224,508, 0 mismatches, S∩[1,97] = seed, shield (41 residues), gates 01/12/20 true on [0, 8^7). The transcription follows Lean's `16·8^k ≤ q+1` form.
- **Mutations:** 204,081 / 4,681 / 1 / shield false.
- **`certify.py` runs:**
  - Li seed, distinct rule: gap period 693, q = 5,733, onset index 421 (= 422nd term), N = 3,364, check through 12,459, |E| = 706, |R| = 693, |E+R| = 5,040, certified.
  - Square seed, equal rule: 224 per 1,176, from a_87 = 440, certified.
  - Square seed, distinct rule: 10 per 41 from 27 (index 5 = first greedy term), certified.
  - Negative control: violation at 12,845,035, E+R identity False.
- **Lean replay:**
  - Toolchain v4.33.0-rc1 and Mathlib rev v4.33.0-rc1 (`lean-toolchain`, `lakefile.toml`, `lake-manifest.json`).
  - 8,643 files / 52 s, 8,663 jobs; Shield 86 s / Erdos341 15 s / Erdos341g 101 s.
  - Five declarations each depend on [propext, Classical.choice, Quot.sound]; the negative control shows sorryAx.
  - Source scan is clean. I re-ran it with broader patterns (bare `extern`, `partial`, `axiom`, `ofReduceBool`, `debug.skipKernelTC`): only `#print axioms` lines matched.
  - leanchecker non-fresh took 46 s rc 0; the non-existent module gave rc 1. Commit c1d9121 is dated 20 Aug 2026.
- **Statement match:** GreedyExtension, PairSum (equal summands), Seed (literal 21-term disjunction), Nat.nth 0-indexed so i = 20, LeastGreedyStep/PrefixPairSum (u, v ≤ j), EventuallyPeriodic with 0 < p, gap = nth(n+1) − nth n — all match `audit.log`. The FC ℤ/IsLeast seam is described correctly. The FC docstring quote "casting it to ℤ gives a counterexample" is verbatim.
- **Paper:** 7 pages. The page's maths matches Li's paper:
  - the Y0/Y1/Y2 definitions and the three controller identities, including Y0 = {0} ∪ (1 + (Y2+Y2)^c);
  - B, D, P and the shield's three clauses plus the diagonal pairs;
  - 24·8^k gaps between Y0 blocks;
  - the readings of Lemmas 1.2 and 4.1;
  - §5 with p ≥ 18, 7p − 20 elements, modulus 7p.
  The disclosure quote is verbatim.
- **Sources and live captures:**
  - EG p.53 OCR: "old problem of Dickson [Dic (34)] is still wide open" and "even a starting set as small as {1, 4, 9, 16, 25} requires thousands of terms before periodicity eventually occurs" are both verbatim. The Ulam paragraph that follows has "i ≠ j"; Dickson's has none.
  - Dickson, "The converse of Waring's problem", Bull. AMS 40 (1934) 711–714 (bib-106).
  - The long Green quote is verbatim.
  - erdosproblems: last edited 20 Jan 2026; one claim, Z_Li "(using GPT-5.6 Sol)", 2026-08-09 15:32:18, 0 comments on it; one thread comment, KentaKitamura 08 Jul 2026, a_{n+224} = a_n + 1176 for n ≥ 87, a_87 = 440.
  - FC commit a8d2933, 2026-09-18, message "Erdős 341: the answer is no (Li 2026), link the formal disproof (#6070)"; `research solved`, `answer(False)`, forbidden sums {a i + a j | (i ≤ n) (j ≤ n)}, a : ℕ → ℤ, IsLeast, citation "Li, Z., Counterexamples to Erdős Problem 341 (2026)".
  - plby: v4.33.0 / Mathlib v4.33.0, `not_erdos_341` over ℕ.
  - The paper's DOI is Zenodo 10.5281/zenodo.22030511.
- **Dates:** 12 days (28 Jul → 9 Aug) and "two months ago" (9 Aug → 13 Oct) are right.
- **OpenAI catalogue:** #341 does not appear in `/tmp/oaimath/CONTENTS.md`. Its "341." entry is Donaldson's hypersymplectic family, an unrelated numbering collision. The snapshot also contains manuscripts dated 7 Oct; "6 October" is the release date the site uses elsewhere.
- **July report:** 4,094/4,095; E = {1, 4, 8, 10, 11, 12}; no q ≤ 20,000 with onset ≤ 479,993 through 500,000; "not a proof of aperiodicity" is verbatim; it did not call E a counterexample.
- **arXiv and MathOverflow:** the arXiv API (several queries) and the MathOverflow search API returned nothing on the claim. This is a coverage result, consistent with the page.
