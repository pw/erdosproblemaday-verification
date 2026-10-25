# Seat W report: world, sources, priority
## OpenAI, "The joint Dickman law for consecutive integers" (24 Sep 2026), family 012

Scope: priority and novelty, the live problem pages, the formalization landscape, the MR/MRT input versions, and release chronology. I did not assess the mathematics of §§2–10.

Sources are in `/tmp/oaimath/012/seats/W_src/`. arXiv PDFs and abstract pages were fetched today (22 Oct 2026). erdosproblems pages were fetched today via the Hetzner box. GitHub data comes from `gh api` and the read-only clone at `/tmp/oaimath/024/repo`. My one numerical script is `W_scripts/check928.py`, with a copy in `W_src/`.

Objection classes follow the brief: FATAL, GAP, ERROR-NONFATAL, EXPOSITION. An **OBS** label marks a world-state observation that is not an objection to the manuscript.

---

## 1. Priority and novelty

### 1.1 Was the natural-density statement open before 24 Sep 2026 and before 6 Oct 2026?

**Yes.** I found no unconditional proof of either of these before the OpenAI release:
- the ordinary-density joint law;
- density 1/2 for P⁺(n) < P⁺(n+1).

I checked the following sources.

**The authors of the strongest prior results say they cannot remove the exceptional scales.**

- Tao–Teräväinen 2019 (arXiv 1809.02518v2, current version), after Corollary 1.16: *"It would of course be desirable if we could upgrade 'almost all scales' to 'all scales' in the above results. We do not know how to do so in general…"*
- Tao–Teräväinen 2026 (arXiv 2512.01739v2, 25 Apr 2026, current version; v1 was 1 Dec 2025).
  - **Theorem 1.8** (it was numbered Theorem 1.7 in v1; I diffed the text and it is otherwise identical) reads: *"There is a set 𝒳 ⊂ ℕ with (1/log X) Σ_{n∈[1,X]∖𝒳} 1/n ≪ log^{−c} X … (so in particular, 𝒳 has logarithmic density 1) such that for any x ∈ 𝒳 and any u, v ≥ 1 we have (1/x) Σ_{n≤x} 1_{n is x^{1/u} smooth} 1_{n+1 is x^{1/v} smooth} = ρ(u)ρ(v) + O(log^{−c} x)."*
  - So Theorem 1.8 does **not** give the full natural density: it holds only for x in a set of scales of logarithmic density 1, with an exceptional set of logarithmic density 0. Its proof (§3.7) is a deduction from their Theorem 3.1, which itself holds "for all scales N outside of a small exceptional set" (p. 5).
  - In §4, about the analogous ω-problem: *"For similar reasons we are currently unable to remove the exceptional set in Theorem 1.7."*

**Working researchers treated it as open after the paper's date.**

- Yang, arXiv 2607.16032v1 (17 Jul 2026, only version), Theorem 1.4: *"#{n < x : P⁺(n) < P⁺(n+1)} > 0.280x. The lower bound is also true for the pattern P⁺(n) > P⁺(n+1)."* The introduction cites Tao–Teräväinen 2019's exceptional set as the state of the art.
- Yang, arXiv 2608.13299 (v1 13 Aug 2026 gives 0.296; v2 3 Sep 2026 gives 0.299, current version), §1.2: *"One of Erdős and Turán's conjectures … asserts that the asymptotic density … is 1/2"*. Theorem 1.3 gives *"> 0.299x. The lower bound is also true for the pattern P⁺(n) > P⁺(n+1)."*
- Yang, arXiv 2610.23280v1, **16 Oct 2026** (ten days after the release). It still states *"Conjecture 1.1. (Erdős-Turán) … #{n ≤ x : P⁺(n) < P⁺(n+1)} ∼ x/2"* and lists 0.280/0.299 as the best results. It does not mention OpenAI. **OBS:** so the release had not reached, or not been accepted by, at least one active author in this area.

**Literature searches found nothing competing.**

- arXiv API searches ("largest prime factor(s)" + consecutive, "Erdős–Pomerance", Dickman + consecutive, friable + consecutive, "consecutive smooth", "smooth numbers"/"consecutive integers", "Erdos problem" 371) turned up nothing before 6 Oct 2026 that claims the unconditional natural density. Result lists are in `arxs_*.xml` and `arxiv_search1.xml`.
- Two web searches found only Yang's papers, the TaTe papers and Wang's conditional result.

**Conclusion on priority:** the manuscript's novelty statement is accurate as far as the public record goes: *"the distinction is therefore the unconditional ordinary limit at every sufficiently large scale"* (§1.1, p. 3).

The release is the first public appearance:
- the PDF's internal date is 24 Sep 2026;
- the first public commit is adc7f124, 2026-10-06T21:58:50Z;
- I found no earlier copy.

### 1.2 Does Tao–Teräväinen 2026 [25, Theorem 1.8] already give the full result?

**No.** See the quote above: Theorem 1.8 has an exceptional set 𝒳ᶜ of logarithmic density zero. Its thresholds are fixed, x^{1/u} and x^{1/v}.

The manuscript describes it accurately: *"[25, Theorem 1.8] gives a quantitative joint law outside an exceptional set of scales, with uniformity in the smoothness parameters and a power saving in log X."* The citation's version and theorem number are right: the bibliography gives "Version 2, 25 April 2026", and the result is Theorem 1.8 in v2 (Theorem 1.7 in v1).

### 1.3 Citation-by-citation check of §1.1

| Manuscript claim (§1.1) | Source opened | Verdict |
|---|---|---|
| "Erdős and Pomerance [7] formulated the joint independence problem and proved that each ordering has positive lower natural density. Their explicit lower bound was 0.0099." | ErPo78 (renyi PDF). p. 311 has *"One might guess that b(t,s)=lim x⁻¹B(x,t,s) exists … b(t,s)=a(t)a(s)"*. §6 has *"the lower density of integers n for which P(n) > P(n+1) is at least (0.08)·(0.1239) > 0.0099. Note that the same is true for integers n for which P(n) < P(n+1)."* | Correct. |
| "[7, Theorem 1]: … X^{−δ} < P⁺(n)/P⁺(n+1) < X^δ less than εX" | ErPo78 Theorem 1: *"For each ε>0, there is a δ>0 such that for sufficiently large x, the number of n ≤ x with x^{−δ} < P(n)/P(n+1) < x^δ is less than εx."* | Correct. |
| "upper-tail independence conjecture of Erdős and Pomerance [7, p. 311]" (§1 and (11.8)) | I rendered p. 311 to an image (`erpo_p1-01.png`) because the OCR drops the ≥ sign. It reads: *"A(x,t) denote the number of n ≤ x with P(n) ≥ x^t … B(x,t,s) the number of n ≤ x with P(n) ≥ x^t and P(n+1) ≥ x^s"*. | Correct. This is an upper-tail, fixed-threshold (x^t) formulation, and (11.8) is exactly it. |
| 0.05544 (de la Bretèche–Pomerance–Tenenbaum [5, §3]), 0.05866 (Fouvry, same section) | Could not open BPT (tenenb.perso.math.cnrs.fr timed out from both boxes; Crossref confirms *Ramanujan J.* 9 (2005) 131–138). Yang 2608.13299v2 independently says *"improved to 0.05544 by La Bretèche, Pomerance and Tenenbaum [3], and to 0.05866 by Fouvry's arguments in 'Further remarks' of the same paper."* | COULD NOT CHECK directly. Corroborated by Yang. |
| Wang [27, 28]: 0.1063 and 0.1356 | Teräväinen 2018 p. 6: *"to 0.1063 by Wang [35], and a further improvement to 0.1356 was given by Wang in [36]"*. [35] is PAMS 145(8) 3211–3220; [36] is arXiv 1706.02980, published in *Mathematika* 64(2). | Correct. |
| Lü and Wang [15]: 0.2017 | Could not open: the HAL PDF returned HTML. Yang 2607 and 2608, and erdosproblems #371, all give *Monatsh. Math.* 206(2) (2025) 403–418 with 0.2017. | Corroborated. Not opened directly. |
| "Yang's recent preprint [30, Theorem 1.4] gives 0.280 for both orderings" | 2607.16032v1, Theorem 1.4 (quoted above). | Correct, **but stale. ERROR-NONFATAL (omission):** Yang's 0.296 (2608.13299v1, 13 Aug) and 0.299 (v2, 3 Sep) both predate the 24 Sep manuscript and are not cited. The live #371 thread recorded the 0.299 improvement (comment by Alfaiz, 20 Jul 2026, with an "Update"). This does not propagate, because the lower bounds are only context. |
| Teräväinen [26, Theorem 1.14] predicted product in log density | arXiv 1710.01195v2 (current version). *"Conjecture 1.13 (Erdős–Pomerance). For any a,b ∈ (0,1), the asymptotic density of {n : P⁺(n) ≤ n^a, P⁺(n+1) ≤ n^b} exists and equals ρ(1/a)ρ(1/b)."* *"Theorem 1.14. Conjecture 1.13 holds when asymptotic density is replaced with logarithmic density."* | Correct. Note that Theorem 1.1 is **verbatim Teräväinen's Conjecture 1.13**, with the same n^a and n^b thresholds and ≤. |
| "His Theorem 1.16 gives logarithmic density 1/2 for the ordering" | Theorem 1.16: *"Conjecture 1.15 holds when asymptotic density is replaced with logarithmic density"*. Conjecture 1.15 is Erdős–Turán. | Correct. |
| "Theorem 1.19 proves positive lower natural density for every nondegenerate rectangle" | Theorem 1.19: *"{n : n^a ≤ P⁺(n) ≤ n^b, n^c ≤ P⁺(n+1) ≤ n^d} has positive asymptotic lower density."* | Correct. |
| Tao–Teräväinen [24, Remark 3.3, eq. (50)] "obtained the joint product law for ordinary averages outside an exceptional set of scales of logarithmic density zero; their Corollary 1.16 gives the corresponding ordering result" | 1809.02518v2. Corollary 1.16: *"there is an exceptional set X₀ of logarithmic density 0, such that lim_{X→∞; X∉X₀} E_{n≤X} 1_{P⁺(n)<P⁺(n+1)} = 1/2."* Remark 3.3, (50): *"lim_{X→∞; X∉X₀} E_{n≤X} 1_{P⁺(n)<n^α} 1_{P⁺(n+1)<n^β} = ρ(1/α)ρ(1/β)"* | Correct, with one **EXPOSITION** quibble. Remark 3.3 is a proof sketch that ends *"We leave the details to the interested reader."* "Obtained" is slightly generous. TaTe 2026 later says Theorem 1.8 *"strengthens … [51, Remark 3.3]"*, which treats it as a result. |
| "Wang [29] proved the ordinary joint law under the Elliott–Halberstam conjecture for friable integers" | Full text not openable (ScienceDirect 403). Semantic Scholar abstract: *"assuming the Elliott-Halberstam conjecture for friable integers, we deduce that the three sets E₁ = {n ≤ x : P⁺(n) ≤ x^s, P⁺(n+1) ≤ x^t}, E₂ = {…P⁺(n+1) … x^α}, E₃ = {P⁺(n) < P⁺(n+1)} have an asymptotic density ρ(1/s)ρ(1/t), ∫_{T_α} u(y)u(z), 1/2 respectively"*. Crossref: JNT 223 (2021) 1–11. | Correct (abstract only). |
| Jiang, Lü and Wang [13]: averaged-over-shift forms | Crossref: *Adv. Math.* 409 (2022) 108592. Yang 2607 describes it as covering *"almost all shifts h with (log x)^{1+ε} ≤ h ≤ x^{1−ε}"*. | Consistent. |
| Comparison conjecture "usually attributed to Erdős and Turán" | Teräväinen 2018: *"A closely related conjecture, formulated in the correspondence of Erdős and Turán in the 1930s"*. TaTe 2019 says the same. | Correct. |

### 1.4 Version currency of every arXiv citation (abstract pages fetched today)

All cited versions are the current ones:

| Citation | Cited version | Current status |
|---|---|---|
| MR | 1501.04585v4 | v4 is current (15 Oct 2017) |
| MRT | 1503.05121v3 | v3 is current (1 Mar 2022) |
| TaTe19 | 1809.02518v2 | current |
| Te18 | 1710.01195v2 | current |
| TaTe26 | 2512.01739v2 | current (25 Apr 2026) |
| Pilatte | 2310.19357v3 | current (25 Aug 2026) |
| Helfgott–Radziwiłł | 2103.06853v2 | current |
| Ford | 1910.08205v5 | current (18 Feb 2025) |
| Wang | 1706.02980v1 | current |
| Yang | 2607.16032v1 | current |

The manuscript's version dates (for example "Version 2, 25 April 2026" and "Version 3, 25 August 2026") match arXiv exactly.

### 1.5 Omissions

- **EXPOSITION. The 1976 provenance.** erdosproblems #928 cites [Er76d] and [Er76e, p. 273] for the independence question. The manuscript credits only ErPo78, which was received May 1976 and published 1978.
- **EXPOSITION / provenance. No citation of the sibling OpenAI family 007**, "Ordinary two-point correlations of multiplicative functions" (same 24 Sep 2026 date; it claims the ordinary two-point Chowla conjecture). Family 012's Lean development depends on it (see §4).
- **EXPOSITION (under-claim). Erdős's α-question [Er79e]** is not mentioned (see §2.3).
- **ERROR-NONFATAL. Yang 0.296/0.299 not cited** (see the table in §1.3).

---

## 2. Live state: erdosproblems #371, #928, #372

### 2.1 #371 page (`live/p371.txt`, page "last edited 16 October 2026")

- The statement is *"Show that the set of n with P(n)<P(n+1) has density 1/2."*
- The page now carries *"A formalised proof that the density of such n is 1/2 is available here"*. The link goes to `github.com/openai/math/blob/main/lean/ComparatorChallenges/JointDickman.lean`.
- `/history/371` (saved as `W_src/history_371.html`) shows this sentence was added in the **2026-10-16 07:31:58** revision. The only earlier stored revision is dated 2025-10-20.
- Site-wide status badges are hidden, so the saved page shows no OPEN/SOLVED label.
- "Proof claims (0)". The page does not mention OpenAI by name.

**OBS: errors on the live page (not the manuscript's).**

- (a) *"Conjectured by Erdős and Pomerance [ErPo78], who proved that this set and its complement both have positive upper density."* ErPo78 §6 proves positive **lower** density (≥ 0.0099), which is stronger. The manuscript states this correctly.
- (b) *"The best unconditional lower bound available is due to Lü and Wang [LuWa25] … 0.2017"*. This is stale: the same page's thread records Yang 0.280 and then 0.299.
- (c) The "formalised proof … here" link points to the **comparator challenge file**, whose three theorems end in `sorry`. It does not point to the proof (`PaperMain.lean`).

### 2.2 #928 (`live/p928.html`, "last edited 03 April 2026", "Formalised statement? No", comments suspended)

The statement is *"Let α,β∈(0,1) … Does the density of integers n such that P(n)<n^α and P(n+1)<(n+1)^β exist?"* The page continues: *"Erdős asked whether … the density … is equal to ρ(1/α)ρ(1/β)."*

**Does Theorem 1.1 answer #928 as stated? Yes, with an elementary transfer that the manuscript does not state.**

There are two convention differences:
- strict < instead of ≤;
- the threshold (n+1)^β instead of n^β.

Let A(X) be the count of n ≤ X in the #928 event and B(X) the count in the Theorem 1.1 event. Then |A(X) − B(X)| ≤ ⌊X^α⌋ + ⌊(X+1)^β⌋ = o(X), for two reasons:
- **First coordinate.** P(n) = n^α forces n^α to be an integer (a prime), and there are at most X^α such n ≤ X.
- **Second coordinate.** P(n+1) is an integer. For β < 1 the interval (n^β, (n+1)^β] has length < 1, so it contains at most one integer, and each integer m lies in such an interval for at most one n. That gives at most (X+1)^β exceptional n.

So the #928 density exists and equals ρ(1/α)ρ(1/β).

- A third party formalized this bound and implication on 9–10 Oct 2026: github.com/jbaelaw/Erdos928 (Codex-drafted, "Mathlib only", explicit-hypothesis implication). It states *"This repository does not re-prove OpenAI's analytic theorem … makes no assertion … about worldwide priority"*.
- I checked the bound numerically for 6 pairs (a, b) at X up to 3·10⁶ (`check928.py`). No violation; the largest |A−B| was 68 for a = b = 0.5, coming from n = p².
- The second sentence on the #928 page, the r-tuple conjecture [Er76e], is **not** answered (it needs r ≥ 3 consecutive integers).

**Who claims #928?**
- **OpenAI:** no. Neither the paper nor `CONTENTS.md` mentions any erdosproblems number. CONTENTS entry 012 says only *"Resolves the Erdős–Pomerance joint Dickman conjecture"*.
- **Bloom's blog** (8 Oct 2026) lists 25 problems. #371 is included; **#928 is not**. For #371 it says *"The above theorem is a corollary of a more general joint distribution law (hinted at in the remarks of [371])."*
- **The #928 page:** unchanged since 3 Apr 2026. "Proof claims (0)". Formal Conjectures has no `928.lean` (GitHub 404).
- **Third parties that attribute #928 to family 012:**
  - jbaelaw/Erdos928;
  - the plasma-ai/erdos wiki (`E0928/claims/2026_09_24_openai.md`, and the E0371 page: *"The same theorem answers Problem 928"*).

### 2.3 Erdős's second #371 question [Er79e]: does the density of {n : P(n+1) > P(n)·n^α} exist for every α?

**The manuscript does not state it, but §11.4 proves it in one line.**

§11.4 defines U_n = log P⁺(n)/log n and V_n = log P⁺(n+1)/log n, and proves *"weak convergence to the product law with marginal distribution function D"*. D (11.5) is continuous with no atoms.

The steps are:
1. P(n+1) > P(n)·n^α holds exactly when V_n > U_n + α.
2. The boundary of the region {v > u + α} is the line v = u + α. By independence and the absence of atoms, P(V = U + α) = ∫ P(V = u + α) dD(u) = 0.
3. So the region is a continuity set, and by the paper's own wording (*"Applying the same continuity-set argument…"*) the density exists for every real α.
4. It equals ∫∫_{y>x+α} D′(x)D′(y) dx dy, with D′(t) = ρ(1/t − 1)/t. This is exactly Teräväinen's Theorem 1.17 log-density value u(x) = x⁻¹ρ(x⁻¹ − 1).

**EXPOSITION (under-claim).** Neither OpenAI, Bloom, nor the #371 page records this second question as answered.

### 2.4 #372 (`live/p372.html`)

Solved by Balog. Theorem 1.1 does not address it (it needs three consecutive integers). No change.

---

## 3. Formalization landscape

### 3.1 Formal Conjectures `ErdosProblems/371.lean`

- **Commit 3dfd999dfe** (author date 2026-10-11T07:51:35Z) belongs to **PR #6898** "feat: mark problems solved in the OpenAI math release and link formal proofs". The PR was opened 2026-10-07T10:16:42Z and merged 2026-10-11T08:10:50Z by mo271 (Moritz Firsching).
- The diff changes `@[category research open, AMS 11]` to `@[category research solved, AMS 11, formal_proof using lean4 at "…/adc7f1241…/lean/OAI/NumberTheory/JointDickman/PaperMain.lean#L21"]`. It adds the docstring *"This was proved by an internal OpenAI model in September 2026 [OAI26a]"*.
- Line 21 at that commit is `theorem increasing_order` (verified in the local copy).
- The commit message itself flags a gap: *"a few links differ from the repository statement by a routine transport that is not in the linked proof: … Erdős 371 (density over Icc 2 ⌊X⌋ vs Iio b)"*.

**OBS:**
- FC's own `erdos_371` (`{n | maxPrimeFac(n+1) > maxPrimeFac n}.HasDensity (1/2)`) still ends in `sorry`.
- FC's density is `Tendsto (fun b : ℕ => S.partialDensity univ b)`, i.e. |S ∩ Iio b|/b over natural b. OpenAI's is `count(Icc 2 ⌊X⌋)/X` over real X.
- The transport is trivial (restrict to integer X; the two counting ranges differ by O(1) terms), but no Lean proof of FC's exact statement exists.
- Earlier history of the file: added in PR #1131 (2025-10-21); refactored in #4433 and #4688.

### 3.2 Third-party replays and re-formalizations

- **jbaelaw/Erdos928** (created 2026-10-09; last push 2026-10-10). This is an implication-only development: `problem928_of_jointDickmanLaw (ρ) (h : JointDickmanLaw ρ) : Problem928 ρ`. It does not import or replay OpenAI's proof. The README claims a Lean 4.35.0-rc3 build with standard axioms only, and a `--paranoid` Comparator run. I did not rebuild it.
- **plasma-ai/erdos wiki**, `E0371/claims/2026_09_24_openai.md` (created 2026-10-07T10:44Z). It claims *"This corpus's verification built `OAI.JointDickmanPaper.increasing_order` at the pinned revision of 6 October 2026 with the toolchain `leanprover/lean4:v4.34.1`. It checked the axioms, which are exactly propext, Classical.choice and Quot.sound, and found no sorry."* This is a self-reported third-party replay; I could not independently verify it.
- **GitHub code search** found:
  - for `JointDickman` and `jointDickmanLaw`: only openai/math and jbaelaw/Erdos928;
  - for `erdos_371` / `Erdos371`: FC copies, Epoch LeanOpenProblems runs (all four Erdos371 runs scored `"I"`, at $300–$1000 budgets), scaffolding repos (rjwalters/lean-genius has history only, last touched July 2026), proofbee, conjectures-io, and our own pw/MathDyad. No independent re-formalization of the analytic theorem was found.

### 3.3 Bloom's blog post ("Erdős problems in the OpenAI proofs", by Thomas Bloom, 8 October 2026)

Fetched from `/forum/thread/blog:10` (`erdosproblems.com/blog` returns 404).

- **On #371:** *"This PDF claims a proof of the following. If P(n) is the largest prime factor of n then the set of n such that P(n)<P(n+1) has density 1/2. Lü and Wang [LuWa25] proved a lower density of >0.2017. Teräväinen [Te18] proved this set has logarithmic density 1/2. This proof has been formalised. The PDF is 84 pages long. The above theorem is a corollary of a more general joint distribution law (hinted at in the remarks of [371])."*
- **General caveats:** *"I have not yet looked at in any serious way any of the proofs … all of these should be read as 'claims'"*. *"There have been some accusations of plagiarism, and some of the proofs below have appeared online in some form before the 6th October release … does not mean to make any judgements about novelty or attribution."*
- #371 is listed among *"solutions to 12 problems on the FrontierMath Erdős list"*.
- **Public criticism:** the blog comments I could retrieve (8–12 Oct) do not discuss #371. They criticize other families (#3, #304: "rushed to say the least").
- No #371 comments or proof claims were posted after the release (the last #371 comment is dated 20 Jul 2026, and commenting is now suspended).
- No openai/math issues exist (issues appear disabled; only PRs #1 and #2).

---

## 4. The MR and MRT inputs

### 4.1 MRT (arXiv 1503.05121)

- The current version is v3 (1 Mar 2022); there is no v4. The comments field reads *"32 pages; proof of Proposition A.3 corrected"*.
- **What was corrected:**
  - The remark after Proposition A.3 reads: *"In the published version of the paper, the proof of this proposition is incorrect when M(f;X) grows very slowly with X. The corrected proof that we provide here gives a slightly stronger result with exp(−M(f;X)) in place of exp(−M(f;X))M(f;X). We state the result with the weaker factor … to remain consistent with the published version."* The acknowledgements credit Fei Wei for this.
  - Separately, footnote 3 corrects Ramaré's identity: *"the term 1_{p∤m} was incorrectly expressed as 1, leading to a slight gap"* (credited to Sedunova and Ke Wang).
- **Theorem A.1's statement is unchanged between v2 and v3.** Both have *"(1/X)∫_X^{2X}|(1/h)Σ_{x≤n≤x+h} f(n)|² dx ≪ exp(−M(f;X))M(f;X) + (log log h)²/(log h)² + 1/(log X)^{1/50}"* for X ≥ h ≥ 10, with M(f;X) = inf_{|t|≤X} D(f, n^{it}; X)², which is (1.6).
- The manuscript's Theorem 2.5 (p. 10) is this, with the weaker factor (1+M)e^{−M}. Its (2.13) matches (1.6). Its sentence *"This is [17, Theorem A.1], in the revised version with the corrected proof of Proposition A.3"* is accurate. The manuscript relies on the current version.
- Lean `Amplification/PublishedInputs.lean` `ComplexShortIntervalInput` encodes the same inequality: (1+M)e^{−M} + (log log H/log H)² + (log X)^{−1/50}, with `minimumDistance` taken over t ∈ [−X, X] and the hypothesis 10 ≤ H ≤ X. Faithful.
- Lean `TwoPointCorrelations/PublishedInputs.lean` cites *"corrected arXiv:1503.05121v3 (1 March 2022), Theorems 1.3 and 1.7"*. It encodes Theorem 1.7 as follows:
  - the cutoff is Q = min(log^{1/125} X, log^5 H);
  - the error is exp(−M/20) + log log H/log H + log^{−1/700} X;
  - the frequency is fixed, which is weaker than the sup over α outside the integral;
  - M is a supplied lower bound on every D(b, χ(n)n^{it}; X)², q ≤ Q, |t| ≤ X. This matches v3's M(g;X,Q) = inf_{q≤Q; χ(q)} D(g, n ↦ χ(n)n^{it}; X)².

  Faithful.

### 4.2 MR (Annals 183 (2016), arXiv 1501.04585v4, current version)

**Theorem 1:** *"Let f : ℕ → [−1,1] be a multiplicative function. There exist absolute constants C, C′ > 1 such that for any 2 ≤ h ≤ X and δ > 0, |(1/h)Σ_{x≤n≤x+h} f(n) − (1/X)Σ_{X≤n≤2X} f(n)| ≤ δ + C′ (log log h)/(log h) for all but at most CX((log h)^{1/3}/(δ² h^{δ/25}) + 1/(δ²(log X)^{1/50})) integers x ∈ [X, 2X]."* The paper adds: *"Note that Theorem 1 allows h, δ and f to vary uniformly."*

The manuscript's Theorem 2.4 (*"There is a function r(H) → 0 such that, for every real multiplicative g : ℕ → [−1,1] and 2 ≤ H ≤ X, (1/X)∫_X^{2X}|A_H g(z) − L_X g|² dz ≤ r(H)"*) is a valid consequence:
- It is uniform in g, real-valued, and |g| ≤ 1.
- Take δ = (log h)^{−1/200}. Bound the exceptional set's contribution by 4·(exceptional proportion), and use X ≥ h to absorb (log X)^{−1/50} into (log h)^{−1/50}.
- Endpoint and integer-versus-real-origin differences cost O(1/H).

Lean `RealShortIntervalInput` states the same mean-square form (∀ multiplicative f with |f n| ≤ 1, 2 ≤ H ≤ X, ≤ r H, r → 0). The "manuscript says / source says" match holds.

### 4.3 OBS for the Lean seat: the closed theorem does not use either Prop

The `Amplification/PublishedInputs.lean` header says these are *"propositions to be supplied as hypotheses"*. However:
- `PaperMain.joint_law` and `increasing_order` are hypothesis-free and call `UnconditionalMain.jointDickmanLaw_unconditional`.
- That theorem passes only `characterDistanceDivergence`, `fordUpperSieveInput`, `squarefreeSelbergDelangeInput`, `squarefreeCharacterEstimateInput`, `primeReciprocalMertensInput`, `primeProductMertensInput`, `finiteMcDiarmidInput`, `finiteBinDistributionInput`, all of which are theorem constants.
- `RealShortIntervalInput` and `ComplexShortIntervalInput` appear only on the `ConditionalMain`/`DischargedMain` route.
- On the unconditional route the short-average estimates are `*_proved` lemmas, for example `Counting/PrescribedShortDischarge.all_characters_short_with_center_proved` and `Counting/NonprincipalShortDischarge.nonprincipal_weightedBinAverage_short_proved`.
- 15 JointDickman files import **family 007's** `TwoPointCorrelations` modules (MRT Ramaré identity, mean square, large values, Halász). The closure contains 216 TwoPointCorrelations modules.

So the formal proof replaces MR16 Theorem 1 and MRT Theorem A.1 with an in-Lean development taken from the sibling family 007, which the paper never cites. That is a route difference from the §1.2 narrative; it is not an error in the paper. I did not audit those modules.

---

## 5. Release chronology (repo: read-only clone plus GitHub API)

- `git log -- lean/OAI/NumberTheory/JointDickman preprints/The-joint-Dickman-law-…-September-24-2026` returns only **adc7f1241**. The GitHub API returns the same for those two paths and for `ComparatorChallenges/JointDickman.lean` and `lean/docs/012.md`.
- The remote head is still **1581d4cbd** (2026-10-12T21:55:24Z).
- Hashes at each of adc7f124, 30148886, fd4aeeb2, 2710f995 and 1581d4cb:

| Object | Hash | Changed across commits? |
|---|---|---|
| `lean/OAI/NumberTheory/JointDickman` tree | 4903e6231371db95940b3d3b882942feb67fc15e | No |
| preprint folder tree | 7ff876bf1b8f54f8ac294f4e838e2cea4dcbdbec | No |
| `paper.pdf` blob | a213750a1589b891e36184313e16df52f14df5dd | No |
| `ComparatorChallenges/JointDickman.lean` blob | df9a8e26 | No |
| `docs/012.md` blob | a92487d8 | No |
| `TwoPointCorrelations` tree (family 007, which 012 imports) | 51a24bc0 | No |

- `git hash-object /tmp/oaimath/012/paper/paper.pdf` gives a213750a…, matching the repo blob. Its sha256 is e66b4e8a1fe197d3bb2c195548cd3bdd3fba8595db1356e571205a6baab43cb3.
- **The coordinator's closure copy (`/tmp/oaimath/012/src/oai`):**
  - 1,458 of the 1,504 repo files under JointDickman are present and byte-identical (git blob hashes compared), with 0 differing.
  - The 46 repo files absent from the copy are all outside `closure_sol.txt`; they are dead modules (list in `W_src/repo_jd_tree.txt` vs the copy).
  - 216/216 present TwoPointCorrelations files are byte-identical.
- The 7 Oct update (30148886, "Update manuscripts and Lean formalizations"; `history.md`: three withdrawals plus 14 revised manuscripts) did **not** touch family 012.

### Chronology table

| Date (UTC) | Event | Source |
|---|---|---|
| 1976-05-19 (recv.) / 1978 | Erdős–Pomerance: fixed-threshold upper-tail independence guess; 0.0099 lower density | ErPo78 p. 311, §6 |
| 1979 | Erdős [Er79e]: does the density of {P(n+1) > P(n)n^α} exist? | #371 page |
| 2017-10-03 / 2018-05-21 | Teräväinen arXiv v1/v2 (FMS 2018): Theorems 1.14, 1.16, 1.17, 1.19 in log density | 1710.01195 |
| 2018-09-07 / 2019-06-26 | Tao–Teräväinen v1/v2 (ANT 2019): Corollary 1.16, Remark 3.3 (50), "almost all scales" | 1809.02518 |
| 2021-01-20 (online) | Wang JNT 223: all three conjectures under EH for friable integers | Crossref / abstract |
| 2022-03-01 | MRT v3 (corrected proof of Prop. A.3) | 1503.05121 |
| 2022-11 | Jiang–Lü–Wang, *Adv. Math.* 409 (averaged shifts) | Crossref |
| 2025 | Lü–Wang *Monatsh.* 206(2): 0.2017 | Yang refs |
| 2025-12-01 / 2026-04-25 | Tao–Teräväinen 2512.01739 v1 (Thm 1.7) / v2 (Thm 1.8): quantitative, with an exceptional set | arXiv |
| 2026-04-03 | erdosproblems #928 last edited | history/928 |
| 2026-07-17 | Yang 2607.16032: 0.280 | arXiv |
| 2026-08-13 / 09-03 | Yang 2608.13299 v1 (0.296) / v2 (0.299) | arXiv |
| 2026-08-25 | Pilatte 2310.19357 v3 | arXiv |
| **2026-09-24** | OpenAI manuscript date (internal; no public trace before the release) | PDF |
| **2026-10-06 21:58:50** | openai/math initial commit adc7f124: public release of 012 (paper plus Lean) | git / API |
| 2026-10-07 10:16 | FC PR #6898 opened | GitHub |
| 2026-10-07 10:44 | plasma-ai/erdos wiki claim page for #371 created (reports a v4.34.1 build) | GitHub |
| 2026-10-08 05:03 / 05:20 | openai/math 30148886 / fd4aeeb2 (7 Oct update); 012 unchanged | git |
| 2026-10-08 | Bloom blog "Erdős problems in the OpenAI proofs" (#371 listed; #928 not) | forum/thread/blog:10 |
| 2026-10-09 – 10-10 | jbaelaw/Erdos928: Lean implication, joint law ⇒ #928 | GitHub |
| 2026-10-11 07:51 / 08:10 | FC 3dfd999 / PR #6898 merged: `erdos_371` → research solved, linking PaperMain.lean#L21 | GitHub |
| 2026-10-12 21:55 | openai/math 1581d4cb (lock PRs); current head; 012 unchanged | git / API |
| 2026-10-16 07:31:58 | #371 page edit adds the "formalised proof … here" link (to the comparator file) | history/371 |
| 2026-10-16 10:51 | Yang 2610.23280: still calls Erdős–Turán a conjecture; no mention of OpenAI | arXiv |
| 2026-10-22 | This audit; #371, #928 and #372 pages fetched | live/ |

---

## Summary of objections (seat W)

1. **ERROR-NONFATAL.** §1.1: *"Yang's recent preprint [30, Theorem 1.4] gives 0.280 for both orderings."* Yang's 0.296 (13 Aug) and 0.299 (3 Sep, arXiv 2608.13299v2) predate the 24 Sep manuscript and are omitted.
2. **EXPOSITION.** §1.1: *"Tao and Teräväinen [24, Remark 3.3, equation (50)] then obtained…"*. Remark 3.3 is a sketch ("We leave the details to the interested reader").
3. **EXPOSITION.** There is no mention of the Er79e α-question. The manuscript's §11.4 weak-convergence argument answers it in one line (see §2.3), so this is an under-claim.
4. **EXPOSITION / provenance.** The sibling family 007 (ordinary two-point correlations), whose Lean modules the 012 formalization imports, is not cited. The §1.2 narrative names MR/MRT as external inputs, while the hypothesis-free Lean theorem instead uses in-house replacements (OBS for the Lean seat).
5. **EXPOSITION.** The 1976 Erdős sources for the independence question ([Er76d], [Er76e]) are not cited.
6. **No citation was found to misstate its source.** All checked theorem numbers, versions and dates are correct: Te18 1.14/1.16/1.19, TaTe19 Cor. 1.16 and Rem. 3.3 (50), TaTe26 Thm 1.8 (v2), MR Thm 1, MRT Thm A.1 (v3), ErPo78 Thm 1 and p. 311, Wang 2021 (abstract).
7. **Priority holds.** Nothing public before 6 Oct 2026 gives the unconditional natural density. TaTe26 Theorem 1.8 has an exceptional set of scales.
8. **#928 is answered by Theorem 1.1** via the O(X^α + X^β) count transfer. It is not claimed by OpenAI, not listed by Bloom, and not on the #928 page; jbaelaw and the plasma-ai wiki attribute it.

**COULD NOT CHECK:**
- de la Bretèche–Pomerance–Tenenbaum 2005 (site timed out);
- Lü–Wang full text (HAL returned HTML);
- Wang 2021 full text (403; abstract only);
- any blog comments beyond those served on the forum page;
- the kscn.discourse post (DNS failure);
- the independent rebuilds claimed by plasma-ai and jbaelaw (not rebuilt).

VERDICT: HOLDS AS READ. This covers seat W's scope only (priority, citations, live state, formalization landscape, chronology); the mathematics of §§2–10 was not assessed. Nonfatal citation and exposition issues are listed above.
