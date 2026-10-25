# Seat W: the world, the sources, and what is new
OpenAI, "A nine-dimensional counterexample to Borsuk's covering assertion" (dated 23 Sep 2026; released in github.com/openai/math, family 156, on 6 Oct 2026).
Referee seat W. Checked 2026-10-20, ~18:00–18:36 UTC (report file last written 18:35:51Z).

**VERDICT: HOLDS WITH FIXES.** All fixes are EXPOSITION. No source anywhere disputes the claim, and every historical citation in §1 checks out against its source. Two things could not be checked:
- No independent kernel replay of OpenAI's Lean has been made public by anyone. The main seat's replay is the only one I know of.
- I could not get the Arnoux–Marin primary text. Their result is confirmed through a secondary source.

New finding: the special case of Theorem 1.1 for covers by caps was already known. It follows from Walkup 1970 (see the heading "b(X_4) = 11 and the 10-line covering corollary" below). The paper's novelty is therefore exactly the step from caps to arbitrary covering sets. That step is what the paper says it does, but the paper never makes the cap case explicit.

---

## 0. Ten-line summary
1. erdosproblems.com/505 has not moved: last edited 30 Dec 2025, still says **64** (it was already stale against 63), 0 proof claims, forum commenting suspended. Bloom's 8 Oct 2026 post on the OpenAI release lists 25 Erdős problems and **505 is not among them**.
2. Formal Conjectures records the claim. PR #6898 (merged 2026-10-11) marks `Borsuk.borsuk_conjecture.not_nine` as `research solved` with a link to OpenAI's Lean. That PR built only its own modules: no `#print axioms`, no Comparator run. PR #7312 (n ≥ 9) is open.
3. Wikipedia still gives 63 as the record. The 9-dimensional claim appears only in a new "Variations" section (14 Oct): "claimed … infinitely many points … does not disprove finite variation." Tao's constant 28a still says 63; PR #217 to change it to 9 is open and unreviewed.
4. Kalai's blog (7 Oct) summarizes the result without comment. On 11 Oct he posted "TYI 60: The Finite and Infinite Borsuk's Problem" (is g(d) = f(d)?), prompted by the result. No verification, simplification or dispute exists on arXiv, MathOverflow or the blogs. Xie (arXiv 2610.17090) rates it "combination leaning new" and did not compile the Lean.
5. Priority: nobody proved b(X_k) ≥ N_k or > N_k before. Kalai did propose this exact set (C3) as a candidate counterexample: in the 2015 survey §2.4 ("for d > 70 or so", conditional on the double-cap conjecture) and on his blog in 2011 ("below 100"). The paper's attribution sentence understates this.
6. A measure argument can never reach 11: the double cap shows the orthogonality-free density on S³ is ≥ 0.1817, so measure gives at most 6. Topology is essential, and that method appears to be new for Borsuk.
7. **The cap special case is classical.** If 10 lines in ℝ⁴ had covering radius < 45°, their Delaunay complex, taken modulo ±, would be a 10-vertex triangulation of RP³. That contradicts Walkup 1970 (Prop. 8.1 + Thm 3). So the "10-line corollary" is old; only the arbitrary-set statement is new.
8. b(X₄) ≤ 11 had already been stated numerically, not certified: acprk/openai-math-followups, 10 Oct 2026. No published covering tables for RP³ exist. Walkup's own explicit 11 lines (polytope P₀) have covering radius **46.378°**, so they do NOT give b ≤ 11.
9. My numerics: best 11 lines reach 41.385°, and their Delaunay nerve is an 11-vertex, 53-edge RP³ triangulation. Best 10 lines converge to **45.332°** from 4 independent starts, consistent with the theorem and close to its 45° bound.
10. History paragraph: every number and attribution checks out. Grinsztajn's note exists and its verifier reruns clean here. Fixes: the 903 bound has a written Magdeburg preprint (97-25) that the paper doesn't cite, and the paper never says the finite-set problem stays open in dimensions 9–62.

---

## 1. Live state of the problem (as of 2026-10-20)

**erdosproblems.com/505.** Fetched today via the Hetzner box (direct fetch gets a Cloudflare challenge).
- Problem text unchanged: "The current smallest n where Borsuk's conjecture is known to be false is n=64, a result of Brouwer and Jenrich [BrJe14]."
- "This page was last edited 30 December 2025." Comments (1), Proof claims (0). The only comment is Boris Alexeev, 03:34 on 3 Feb 2026: "The famous proof by Kahn & Kalai was formalized by Aristotle."
- The thread page says "The ability to post new comments has been suspended."
- So the page is stale twice over: 63 since May 2026, and 9 if the claim holds.
- Thomas Bloom, "Erdős problems in the OpenAI proofs" (8 Oct 2026; https://www.erdosproblems.com/forum/thread/blog:10):
  - It lists 25 problems: 3, 90, 120, 138, 148, 172, 174, 181, 184, 293, 304, 371, 416, 431, 508, 551, 604, 802, 821, 952, 968, 970, 986, 1083, 1150.
  - **505 is not listed**, and neither the post nor its comments mention Borsuk.
  - Its disclaimers say the claims are unchecked and that there are plagiarism/priority concerns about some of the families.

**teorth/erdosproblems database** (data/problems.yaml at repo HEAD 5268e3bc15, 2026-10-20T17:30Z):
- 505: informal_status `disproved`, formal_status `Lean`, status `disproved (Lean)`, all with last_update 2026-02-02 (the Aristotle formalization of Kahn–Kalai).
- formalized `yes` (2026-05-13). comments "Borsuk's problem".
- The database has no dimension field, so the claim doesn't affect it.
- No issue or PR mentions 505; the only Borsuk hit is unrelated issue #370.

**Formal Conjectures** (google-deepmind/formal-conjectures). Paths: FormalConjectures/ErdosProblems/505.lean (blob 9df60e93) and FormalConjectures/Wikipedia/BorsukConjecture.lean.
- Both were last changed by commit 3dfd999dfe (2026-10-11), from **PR #6898** by Moritz Firsching (opened 2026-10-07, merged 2026-10-11): "mark problems solved in the OpenAI math release and link formal proofs".
- 505.lean docstring: "In September 2026 an internal OpenAI model gave a counterexample for n = 9 [OAI26], with a formal Lean proof; see `Borsuk.borsuk_conjecture.not_nine`."
  - `erdos_505` itself links to the Aristotle Kahn–Kalai proof (plby/lean-proofs@96cd549…, src/v4.24.0/ErdosProblems/Erdos505.lean#L1153).
- BorsukConjecture.lean:
  - `borsuk_conjecture.not_nine` is `@[category research solved, … formal_proof using lean4 at "https://github.com/openai/math/blob/adc7f124…/lean/OAI/Geometry/Borsuk/Main.lean#L117"]`.
  - The main statement is restated as `¬ ∀ n, 4 ≤ n → n ≤ 62 → BorsukConjecture n` (research solved).
  - `borsuk_conjecture.four` stays `research open`. The docstring says "The cases 4 ≤ n ≤ 8 are open."
  - It also records Tolmachev–Voronov b(4) ≤ 8 (arXiv 2605.19068, unrefereed).
- What PR #6898 says it checked:
  - Executed: `lake --wfail build` of the changed FC modules, resolution of each link to a `theorem`, a grep for no `sorry`, and inspection of the Comparator config.
  - Explicitly not executed: `#print axioms` and Comparator.
  - Noted transport gap: "Borsuk (`Metric.diam` vs `ediam`, and the cover is intersected with the set)".
- **Open PR #7312** (bengoechea, 2026-10-14) adds the n ≥ 9 statement (Corollary 7.1) with `sorry`, plus a proved isometry-transport lemma.
- Earlier: issue #5657 / PR #5780 (Sept 2026) on the `Metric.diam` junk value. #5265 (2026-09-15) moved FC to `ediam`.
- Nothing in FC adds a lemma about dimension 9 beyond the link.

**Wikipedia, "Borsuk's conjecture"** (current revid 1380296605, 2026-10-14T22:53Z, user Arsenniy):
- The Problem section still says the 64 bound "stood as the record until May 2026, when Max Grinsztajn, assisted by OpenAI's GPT-5.5 Pro, lowered the minimum known failing dimension to 63". That text was added in revid 1373727236 on 2026-09-07.
- The OpenAI claim appears only in a new "Variations" section: "In 2026, OpenAI claimed to have constructed counterexample to Borsuk's conjecture in ℝ⁹, but the construction has infinitely many points and therefore (if correct) does not disprove finite variation". The citation is marked "(temporary citation)".
- So Wikipedia has **not** been updated to 9 as the record.
- "List of mathematical discoveries by artificial intelligence" (revid 1381041815, 2026-10-19) still calls 63 "the smallest dimension for which a counterexample is known", with no entry for the 9-dimensional result.

**Tao's optimization-problems table, constant 28a** (https://teorth.github.io/optimizationproblems/constants/28a.html):
- Current best is still **63** [Gri2026], from PR #84 by Grinsztajn, merged by **teorth** on 2026-05-29.
- **PR #217** (kleinwaks, opened 2026-10-06, open, no comments) would set the bound to 9. Its body: "I did not independently check the Lean."

**Gil Kalai's blog** (gilkalai.wordpress.com):
- 2026/10/07, "Updates: Sharing AI progress on mathematics (amazing!)": one paragraph, "Borsuk's problem in dimension nine … gives a compact set in nine-dimensional Euclidean space that cannot be covered by ten sets of smaller diameter." No assessment. He also says news from the release is relevant to his Borsuk lecture at Jeff Fest, Rutgers.
- 2026/10/11, "Test Your Human Intuition 60: The Finite and Infinite Borsuk's Problem": defines f(d) (all sets) and g(d) (finite sets) and asks whether g(d) = f(d).
  - This is exactly the question the compact witness raises.
  - Comments: Lior Silberman (15 Oct) argues that the standard compactness arguments fail and gives a uniform diameter-gain lemma for f(d).
- No post since 23 Sep verifies or disputes the result. The 14 Oct post is unrelated.

**arXiv.** API query `all:Borsuk`, sorted by submission date, 60 newest (mostly LHCb noise, since "Borsuk" is an author name). Nothing verifies, simplifies, extends to lower dimension, or disputes the 9-dimensional claim. No complex or quaternionic analogue paper exists. Relevant items:
- Ying Xie, arXiv:2610.17090v1 (12 Oct 2026), "What the Machine Invented…": §9.3.3 covers family 156.
  - Verdict "combination leaning new".
  - "Kalai's survey names the set but asks no topological question about it; Adams–Bush–Frick 2021 is the nearest relative."
  - The 10-label obstruction is "Walkup-style".
  - Caveats: the witness is continuous, so it says nothing about finite sets; its convex hull gives a convex-body counterexample; the paper cites an unrefereed GitHub note.
  - "No Lean development was compiled or kernel-checked for this survey."
- Yibo Ji, arXiv:2608.12561. v1 (12 Aug 2026) gave the same 321-point 63-dimensional example, found with GPT-5.6 Sol. Withdrawn in v2 (14 Aug) as a duplicate of Grinsztajn.
- Adjacent work, none of which bears on the claim:
  - Noel, arXiv:2609.22680 (19 Sep 2026): circular chromatic number of the real orthogonality graph on S² is 4.
  - Musin, arXiv:2609.09688: a Borsuk–Ulam theorem for O(k).
  - Tolmachev–Voronov, arXiv:2605.19068: b(4) ≤ 8.

**Independent checks by third parties:**
- **acprk/openai-math-followups** (GitHub, created 2026-10-10), results/03-borsuk.md:
  - States "b(X) = 11 numerically" from a nearest-line Voronoi partition by 11 optimized lines, "margin 0.036". It is not interval-certified, and validity was checked by random-start Nelder–Mead.
  - With K = 10 the partition was "invalid, consistent with OpenAI's theorem".
  - Also: the CP² projector set in the 8-dimensional Hermitian space is coverable by 9 sets (Hesse SIC lines), so it is not an 8-dimensional counterexample.
- **No public kernel replay of OpenAI's Borsuk Lean** exists by anyone: FC built only its own modules, Tao's PR didn't check, and Xie didn't compile.
- The openai/math repo has issues disabled, and PR conversations have been locked since commit 2710f995ca (2026-10-12).
- The paper directory and the lean/OAI/Geometry/Borsuk directory have only the initial commit adc7f1241b (2026-10-06T21:58Z). They were not touched by the 7 Oct fix round, and history.md doesn't list them. The repo's paper.pdf is 413,156 bytes, matching our copy (sha256 e7ffa6f8…).

**MathOverflow.** API search for 2026 questions mentioning "Borsuk": only Bing–Borsuk and LSB questions, nothing on the 9-dimensional result. Prior art for the finite-vs-infinite question: MO 196319 (12 Feb 2015, "Infinite counter-examples to Borsuk conjecture"), which asks "Is it possible that, in some dimensions, only infinite counter-examples exist?" (0 answers).

---

## 2. Priority and novelty

**Kalai, "Some old and new problems in combinatorial geometry I: Around Borsuk's problem".** arXiv:1505.04952v1 (19 May 2015; the only version). Published in Surveys in Combinatorics 2015, LMS Lecture Note Series 424, pp. 147–174, DOI 10.1017/CBO9781316106853.005 (Crossref).
- §2.3, "Embedding the elliptic metric into an Euclidean one":
  - Defines E_n (lines in ℝⁿ, angle metric), the embedding into ℝ^{n(n+1)/2} by x ↦ x⊗x, and three images: C₁ (balanced ±1 vectors, the original Kahn–Kalai example), C₂ (all ±1 vectors, the cut polytope), and **C₃ = "the image of all unit vectors … the unit vectors in the cone of rank-one positive semi-definite matrices"**, which is the paper's X_n.
  - Asks Problem 2.7 (embeddings into o(n²) dimensions preserving the diameter relation).
  - Cites de Caen to say a strictly order-preserving embedding needs quadratic dimension.
- §2.4: Witsenhausen's bound μ ≤ 1/(n+1), Conjecture 2.8 (the double cap), and then: **"If true, this … will show that C₃ defined above is a counterexample to Borsuk's conjecture for d > 70 or so."**
- Kalai's blog, 15 Jun 2011, "The combinatorics of cocycles and Borsuk's problem", Construction 3 (the same set): "It is quite possible that this set will give better bounds than construction 2 … which will reduce the lowest dimension where Borsuk's conjecture is false to below 100."
- So Kalai explicitly proposed the full projector set as a counterexample candidate, conditionally and in dimension ≳70, via a measure argument. Nowhere does he ask about n = 4, a topological bound, or anything like b(X₄) ≥ 11. Xie reached the same reading.

> **Objection 2a (EXPOSITION).** The paper says: "Kalai describes the map x ↦ x⊗x and the full rank-one positive semidefinite configuration in his account of the Kahn–Kalai construction [14, Section 2.3]."
> - That is accurate but incomplete. In the very next section (§2.4) Kalai proposes C₃ = X_n **as a Borsuk counterexample**, conditional on the double-cap conjecture, for d > 70.
> - The set itself is therefore a published candidate. What is new is (i) proving it works and (ii) proving it already works at n = 4 (d = 9).
> - Fix: cite §2.3–2.4, and Kalai's 2011 blog post if desired.

**Why the measure route could not get here (supports novelty of method).** Fix n = 4 (S³) and let α be the largest density of a set on S³ with no orthogonal pair.
- Two opposite caps of angular radius π/4 have normalized measure 2·(π/2 − 1)/(2π) = 0.1817. So α ≥ 0.1817, and any measure-only argument proves at most ⌈1/0.1817⌉ = **6** parts.
- DeCorte–Oliveira Filho–Vallentin, "Complete positivity and distance-avoiding sets" (arXiv:1804.09099v4), Table 1, n = 4: 0.1817 ≤ α ≤ 0.21676.
- Reaching 11 is impossible by measure, so the topological route (odd map, mod-2 degree, local preimage counts) is essential.
- I found no earlier use of it for Borsuk. The closest relative is Adams–Bush–Frick, "The topology of projective codes and the distribution of zeros of odd maps" (arXiv:2106.14677v3; Michigan Math. J. 2023). Their Lyusternik–Schnirelmann–Borsuk generalization (Thm 15) is about **antipodal** pairs, not orthogonal ones.

**Earlier results on covering projective space with orthogonality-free pieces.** Searches run:
- Web: covering RP^n by closed sets with no orthogonal pair; closed or open chromatic number of the orthogonality graph; Borsuk number of the Veronese surface or embedding; rank-one PSD Borsuk partitions; Lusternik–Schnirelmann with an orthogonality condition.
- MathOverflow API, by title and keyword.
- arXiv listing.
- GitHub repository search for "Borsuk".

Nothing proves b(X_k) ≥ N_k or b(X_k) > N_k for any k, and nothing proves non-existence of an orthogonality-respecting partition of unity with k(k+1)/2 labels. Nearest items:
- Godsil–Zaks, arXiv:1201.0486: χ = 4 for arbitrary colorings of S² by orthogonality.
- Noel 2026: circular chromatic number = 4 on S².
- "Orthogonal colorings of the sphere", arXiv:1505.02514: 4-colorings with interiors must be octahedral.
- Kochen–Specker sets: for ℝ⁴ lines, χ ≥ 5 on finite sets.

None of these concerns ℝ⁴ with open or closed classes, or count k(k+1)/2.

**But the CAP special case is classical** (Walkup 1970). See the heading "b(X_4) = 11 and the 10-line covering corollary" below. This sharpens Objection 2c.

> **Objection 2c (EXPOSITION; affects the novelty statement, not correctness).** The paper says: "These results cannot be applied directly to the complex here: its faces are positive coordinate supports of a map, not simplices in a triangulation of projective space."
> - True for arbitrary covering sets.
> - But for covers by metric caps (equivalently, finite line configurations with covering radius < π/4), Walkup's Theorem 3 does apply directly, via the Delaunay complex (argument below).
> - The paper should state that the cap or "geodesically nice" case of Theorem 1.1 is classical, and that its contribution is removing the cap hypothesis. As written, a reader cannot tell which part is new.

**Observation, not a defect.** By Conway–Hardin–Sloane Thm 2, X₄ − I/4 lies on a sphere of radius √3/2 in the 9-dimensional trace-zero space. Its diameter is √2, so after normalizing the diameter to 1 it lies on a sphere of radius r = √6/4 ≈ 0.612.
- Theorem 1.1 therefore gives a concrete instance of Kalai's Problem 2.9 (spherical Borsuk): f_r(9) ≥ 11 > 10 for r = √6/4.
- Kupavskii–Raigorodskii, as quoted in Kalai §2.5, give only asymptotic statements.
- The paper doesn't mention this.

**Finite sets.** The 9-dimensional witness is compact and infinite. A finite F ⊂ X₄ with diameter √2 has b(F) equal to the chromatic number of the orthogonality graph on F. By de Bruijn–Erdős, finite subsets of X₄ give a finite 9-dimensional counterexample **iff** the orthogonality graph on all lines of ℝ⁴ has (ordinary) chromatic number ≥ 11. I found no result on that (known: ≥ 5 from Kochen–Specker sets; ≤ 11 if b(X₄) = 11).

> **Objection 2b (EXPOSITION).** The paper says: "Theorem 1.1 improves this dimension bound using the full compact image of projective space rather than a finite configuration."
> - Correct for Borsuk's question as posed (all bounded sets; also as defined by Tao's 28a and by FC).
> - But every earlier record (946 → 63) was a finite set, and the finite version stays open in dimensions 9–62. Kalai's TYI 60 and the Wikipedia edit both flag exactly this.
> - Fix: add one sentence saying the result says nothing about finite sets below 63.

---

## 3. The history paragraph (printed §1, "History and the method"), claim by claim

| Claim in paper | Source checked | Status |
|---|---|---|
| Borsuk posed the question in 1933 [3] | Fund. Math. 20 (1933) 177–190 (doi 10.4064/fm-20-1-177-190) | ✓ |
| Kahn–Kalai disproved it in high dimensions using Frankl–Wilson [13], [5] | arXiv math/9307229 abstract ("f(d) ≥ (1.2)^√d"); Bull. AMS 29(1) 60–62 (1993) | ✓ (they also claimed n = 1325; Weißbach showed the stated derivation doesn't give it; Jenrich arXiv:1809.09612v4 repaired it. The paper doesn't mention 1325, which is fine) |
| 946 by Nilli [16] | Kalai survey ref [96]; Bondarenko p.2 (quoted on Tao's 28a page: "Nilli [14] (n = 946)"); Grey–Weißbach abstract | ✓ |
| "the announced bound 903 of Grey and Weissbach [6]", cited as a 17th Kolloquium über Kombinatorik announcement | **Magdeburg preprint 97-25**, J. Grey, B. Weißbach, "Ein weiteres Gegenbeispiel zur Borsukschen Vermutung" (https://math.ovgu.de/-p-2678). Abstract: "Kahn and Kalai … smallest d = 2016. A. Nilli … d = 946. We show here that such a counterexample already exists for d = 903." | ✓ number. **EXPOSITION**: a written preprint exists; cite it rather than only a conference announcement. (Kalai's survey credits 903 to Weissbach alone.) |
| 561 by Raigorodskii [18] | Russian Math. Surveys 52(6) (1997) 1324–1325 (doi 10.1070/RM1997v052n06ABEH002184); Bondarenko p.2: "Raigorodskii [17] (n = 561)" | ✓ |
| 560 by Weissbach [20] | Beiträge Alg. Geom. 41(2) (2000) 417–423; abstract: counterexample in dimension C(34,2) − 1 = 560, generalizing Raigorodskii | ✓ |
| Hinrichs 323 using Leech-lattice vectors [10] | Discrete Math. 243 (2002) 253–256; Kalai §2.6: "construction of Hinrichs … rely on the Leech lattice"; Pikhurko abstract: "false for all n ≥ 323" | ✓ |
| Pikhurko 321 "and credited an independent discovery by Hinrichs and Richter" [17] | arXiv:math/0202112v1 (12 Feb 2002; only version) abstract: "(This result has been independently discovered by Hinrichs and Richter.)" | ✓ verbatim |
| Hinrichs–Richter 298 in 2003 [11] | Discrete Math. 270 (2003) 137–147; Bondarenko: "false for n ≥ 298; see [9]" | ✓ |
| Bondarenko two-distance counterexample in dimension 65 [2] | arXiv:1305.2584 v3 (29 Aug 2013): 416 points on S⁶⁴, not partitionable into 83 parts; DCG 51(3) (2014) 509–515 | ✓ |
| Jenrich–Brouwer 64 [12], EJC 21(4) P4.29 (2014), 3 pp. | EJC v21i4p29, submitted 3 Feb 2014, published 6 Nov 2014: 352-point two-distance set, needs ≥ 71 parts. (Jenrich's own arXiv:1308.0206v6 came first.) | ✓ |
| "Grinsztajn's public proof note gives a finite counterexample in dimension 63 [7]" (May 2026, author's repository, 6 pp.) | github.com/maaxgrin/borsuk-63-counterexample, created 2026-05-26T20:30Z, last push 2026-05-27 (HEAD cdcdbeac2e). borsuk_63_counterexample.pdf: 6 pp., dated "May 2026", built 2026-05-27. | ✓ exists exactly as cited (details below) |
| Kalai describes x ↦ x⊗x and the full rank-one PSD configuration [14, §2.3] | Survey §2.3 (see §2 above) | ✓ but understated (Objection 2a) |
| CHS use the projection-matrix model [4, Section 5, Theorem 2]; chordal distance = Frobenius/√2 | arXiv:math/0208004v1, §5 Theorem 2 (p.19): "isometric embedding of G(m,n) into a sphere … d_c(P,Q) = (1/√2)‖P − Q‖" | ✓ |
| Walkup's eleven-vertex minimum for triangulations of RP³ [19, Theorem 3] | Acta Math. 125 (1970) 75–107, Theorem 3 (p.76): "There exists a triangulation K of projective 3-space P³ with f₀ vertices and f₁ edges if and only if f₀ ≥ 11 and 4f₀ + 7 ≤ f₁ ≤ f₀(f₀−1)/2." | ✓ verbatim (read from the full text) |
| Projective-space vertex bounds of Arnoux and Marin [1] (Mem. Fac. Sci. Kyushu Univ. Ser. A 45(2) (1991) 167–244) | Primary text not reachable. Bibliographic data confirmed in several reference lists. Content via Balagopalan, EJC 24(1) #P1.52 (2017): "Arnoux and Marin, in 1991, proved that the minimum number of vertices needed to triangulate RPⁿ, n ≥ 3, is at least C(n+2,2) + 1." | ✓ via a secondary source. COULD NOT CHECK the primary. Note: C(k+1,2) + 1 = N_k + 1, exactly the paper's threshold, so the analogy the paper draws is apt. |

**Grinsztajn's note in detail.**
- Claim: a 321-point set X ⊂ ℝ⁶³ in which every subset of smaller diameter has ≤ 5 points, so at least 65 > 64 parts are needed. It comes from the G₂(4) representation (the 320-point subconfiguration in a codimension-2 subspace, plus one adjoined projected point).
- GPT-5.5 Pro assistance is disclosed. The repo has an exact verification script, DIMACS certificates, and a Sage verifier with CI.
- Checks so far:
  - Accepted into Tao's table: PR #84 merged by teorth, 2026-05-29.
  - Independently re-found by Ji (arXiv:2608.12561, withdrawn as a duplicate). The FC docstring also credits Konz.
  - **I ran `verify_borsuk63.py` here** (python3 -I, ulimit, 900 s): exit 0, "all exact verification checks passed" (srg(416,100,36,20); B = 96 / C = 320; no K₆; no K₅ on N_C(b₀)). This checks only the finite combinatorial facts; I did not re-derive the geometric projection step in the PDF.
  - Not refereed.
- The paper cites the note but does not use it. Fine.

---

## 4. Which erdosproblems.com/505 facts change
- "Trivially true for n = 1, easy for n = 2, true for n = 3 (Eggleston)": unchanged.
- "Kahn–Kalai … false for n > 2014": unchanged. (KK also stated 1325; see the table.)
- "α(n) ≥ (1.2)^√n" and "Schramm: α(n) ≤ ((3/2)^{1/2} + o(1))ⁿ": unchanged. A single dimension says nothing about asymptotics.
- Status "disproved (Lean)": unchanged. 505 asks about *every* set of diameter 1, so a compact witness qualifies, but the problem was already disproved.
- **Only "the current smallest n … is 64 (Brouwer and Jenrich)" changes.** It was already stale, being 63 (Grinsztajn, finite, unrefereed, May 2026). If Theorem 1.1 holds it should split into two statements:
  - **n = 9** for arbitrary bounded sets (OpenAI, Lean-formalized; open range 4 ≤ n ≤ 8).
  - **n = 63** for finite sets (open range 4 ≤ n ≤ 62).
- The paper adds that every n ≥ 9 fails (Corollary 7.1, the standard adjoining construction). For finite sets, failure in every n ≥ 63 follows from Grinsztajn plus the same construction.

---

## b(X_4) = 11 and the 10-line covering corollary
(The main seat asked: has anyone stated b(X₄) ≤ 11 or = 11? Are there published 11-line coverings of RP³ by caps of radius < 45°, or covering tables for lines in ℝ⁴? Was an 11-vertex RP³ triangulation used to build a cover? Is "every 10 lines leave a line at ≥ 45°" in the literature?)

**(a) b(X₄) ≤ 11 or = 11 already stated?**
- **Yes, numerically and uncertified**, by acprk/openai-math-followups, results/03-borsuk.md (repo created 2026-10-10): "b(X) = 11 numerically. Nearest-line partitions of ℝP³ by K optimized lines: K = 11 valid with margin 0.036; K = 12 valid (margin 0.001); K = 10 invalid …"
  - Their criterion is "no Voronoi cell contains an orthogonal pair", checked by random-start Nelder–Mead in scripts/borsuk/rp3_voronoi.py.
  - They say: "To make (2) a theorem, the 11 cells must be certified."
- I found nothing before 6 Oct 2026, and nothing certified. If the main seat's exact rational certificate holds, it is the first certified statement of b(X₄) ≤ 11, and with Theorem 1.1, of b(X₄) = 11.
- Note the criteria differ. Covering radius < 45° (caps) is stronger than the Voronoi no-orthogonal-pair condition.

**(b) Covering tables or published 11-line coverings of RP³?**
- **None found.**
  - Hardin–Sloane–Smith spherical covering tables (neilsloane.com/coverings) cover S² only (n = 4…130).
  - Conway–Hardin–Sloane is about packings only; the word "covering" doesn't appear.
  - "Covering Grassmannian codes" papers are over finite fields.
  - Riasat–Mahdavifar (arXiv:2512.22911) treat average covering radius.
- Walkup's own explicit geometric 11-vertex RP³ is P₀ (Acta Math. 125, §8): 22 unit vectors, namely (0,0,0,±1), (±β,0,0,±β), (0,±β,0,±β), (0,0,±β,±β) with β = √2/2, and (±α,±α,±α,0) with α = 1/√3. These are 11 lines.
  - **I computed their exact Voronoi vertices: covering radius = 46.378°** (vertex circumradii 35.657°, 39.925°, 41.819°, 46.378°; a 2·10⁶-sample check agrees).
  - So **Walkup's P₀ does NOT witness b(X₄) ≤ 11** by caps. Its quotient K₀ is a triangulation, but some Delaunay cells have circumradius > 45°.
- My own optimization (w_scripts/cover10.py, then vpolish.py, a Voronoi-vertex minimax polish with SLSQP):
  - Best 11 lines: **covering radius 41.385°** (exact Voronoi-vertex enumeration on a float configuration, not certified). This matches the main seat's "< 42°".
  - The Delaunay nerve of this cover is a **closed 3-pseudomanifold with f = (11, 53, 84, 42)**. Every triangle lies in exactly 2 tetrahedra; Betti numbers are (1,0,0,1) over ℚ and (1,1,1,1) over 𝔽₂, which is the homology of RP³.
  - It has 53 edges, inside Walkup's range 51 ≤ f₁ ≤ 55, and is not K₀ (51 edges).
  - So the optimal 11-cover realizes an 11-vertex Walkup-class triangulation of RP³ as its nerve. Nobody seems to have used this to build a cover; this is new data, not literature.
  - Coordinates, rows = unit vectors:
    ```
    [-0.122360 -0.193312 -0.209034  0.950770]  [ 0.843192 -0.025240  0.346425 -0.410342]
    [-0.635891 -0.360274  0.114011 -0.672939]  [ 0.366273 -0.762214 -0.375903  0.378907]
    [-0.487054 -0.692345  0.399866  0.351489]  [-0.953090  0.154913  0.259829  0.010531]
    [-0.522166  0.392774 -0.595319 -0.467618]  [ 0.120825  0.104358 -0.947807  0.275993]
    [ 0.486412  0.651387  0.579893  0.053128]  [ 0.223268 -0.845605  0.254739 -0.412566]
    [ 0.261787 -0.298598 -0.632633 -0.664892]
    ```
    (saved as /tmp/oaimath/156/seats/w_scripts/best_K11_s11_vp.npy)

**(c) "Every 10 lines in ℝ⁴ leave some line at angle ≥ 45° from all of them". In the literature?**
- Not stated anywhere I found. But **it is an elementary consequence of Walkup 1970**, and of Arnoux–Marin for general k. So it is not new, and it is strictly weaker than Theorem 1.1. The argument:
  1. Suppose 10 lines with unit vectors ±u_i have covering radius θ < π/4. Let P be the 20 points ±u_i on S³. Because θ < π/2, 0 lies in the interior of conv P, so conv P is a centrally symmetric 4-polytope with vertex set P.
  2. Covering radius is continuous in the configuration, so a small symmetric perturbation keeps θ < π/4 and makes conv P simplicial.
  3. Each facet {⟨n,x⟩ = 1} gives a cap centered at n/|n| of radius ρ = arccos(1/|n|) with no point of P in its interior. So ρ ≤ θ < π/4.
  4. Hence the vertices of each facet lie within ρ of one point, and are pairwise at angle < π/2.
  5. Therefore no edge joins x to −x, and no 2-edge path x–y–(−x) exists (it would need ∠(x,y) < π/2 and ∠(y,−x) < π/2 at once).
  6. Walkup's **Proposition 8.1** (p.92) then says ∂conv P / ± is a triangulation of projective 3-space with 10 vertices. That contradicts **Theorem 3** (f₀ ≥ 11). ∎
- The same argument with Arnoux–Marin gives: for k ≥ 4, any N_k = k(k+1)/2 lines in ℝᵏ have covering radius ≥ π/4. This is the cap version of b(X_k) > N_k.
- Walkup's Theorem 6 (cs simplicial 4-polytopes with no antipodal pair joined by a path of fewer than 3 edges satisfy f₁ ≥ 4f₀ + 14) is the polytope form of the same fact. Walkup notes that it "follows as an easy corollary to Theorem 3 using (8.1)".
- Consequence for the novelty statement: Theorem 1.1 restricted to cap covers (or to any covering sets whose nerve is forced to be such a Delaunay triangulation) is 1970 mathematics. The paper's contribution is exactly the passage to arbitrary sets, which it handles through the support complex of a partition of unity. The paper says this in words ("cannot be applied directly") but never states the cap case. See Objection 2c.
- Numerical tightness (not a proof): minimizing the covering radius of 10 lines, **four independent runs** (seeds 10, 201, 202, 203; soft-minimax descent, then Voronoi-vertex SLSQP polish) **all converge to 45.332°**.
  - That is consistent with the theorem and its classical cap version, and close to the 45° bound. No run went below 45°.
  - Sanity check at k = 3: the best 5 lines in ℝ³ reach 46.02°, consistent with b(X₃) ≥ 6 = N₃.
  - For comparison, the 12 lines of the D₄ root system (24-cell) have covering radius exactly 45°, so they are not a strict cover.

---

## Files and receipts
- All downloads are in /tmp/oaimath/156/seats/w_dl/: Kalai survey (kalai1505.pdf/.txt), Kalai blog posts (kb_*.txt, kalai_blog_10{07,11,14}*), Walkup 1970 (walkup1970.pdf/.txt), CHS (chs.pdf), Adams–Bush–Frick (abf2106.pdf), DeCorte–Oliveira–Vallentin (docv.pdf), Jenrich–Brouwer (jb_ejc.pdf), Grinsztajn (grin63.pdf), Xie (xie2610.pdf), FC files (fc505.lean, fcborsuk.lean), the teorth database (ep_problems.yaml), Wikipedia wikitext (wiki_borsuk_raw.txt, wiki_aimath.txt), erdosproblems pages fetched today via Hetzner (ep_*.html; blog10.txt), and acprk/03-borsuk.md plus rp3_voronoi.py.
- Scripts and logs are in /tmp/oaimath/156/seats/w_scripts/: cover10.py, coverD.py, vpolish.py, nerve11.py, homol.py, walkup11.py; logs cover_*.log, vpolish_*.log; configurations *.npy.
- The Grinsztajn verifier run is in /tmp/oaimath/156/seats/w_grin/run.log.
- Nothing was posted or contacted. No Lean was built. Nothing was written outside seats/.
