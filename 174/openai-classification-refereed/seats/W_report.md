# Seat W (sources + world): OpenAI, "A classification of finite Euclidean Ramsey configurations" (23 Sep 2026), Erdős #174

Checked 2026-10-21, about 21:05–21:25Z. The scratch files and verbatim copies are in `/tmp/oaimath/172/seats/W_src/`: `dl/` holds the downloaded PDFs and their text extractions, `prior/` the third-party prior-work files, and `wstrinz/` the READMEs. The paper's printed numbering is cited as instructed.

Scope: this seat checks two things. (1) Do the cited sources say what the paper uses them for? (2) What is the public state of the world? I did not referee the paper's internal proofs. (I did one hand check of the algebraic corollary in §3, plus a 4-line exact-arithmetic check.)

---

## 1. Citation audit

Unless a row says otherwise, I read the cited statement in the primary source.

| Ref | Where the paper uses it (printed) | Cited source says | Verdict |
|---|---|---|---|
| [4] EGMRSS 1973, **Thm 13** | §1: "proved that every finite Ramsey set is spherical [4, Theorem 13]"; Cor 7.1 | p. 349: "THEOREM 13. If K is not spherical, then K is not Ramsey." | **ACCURATE** |
| [4] **Lemma 15** | before Prop 2.4: "The invariant-and-coloring strategy goes back to Erdős et al. [4, Theorem 13 and Lemma 15] … Their real-variable coloring lemma extends Rado's work on partition regularity [21]." | Lemma 15: "Let c1,…,ck, b be real numbers, b ≠ 0. Then there exists an integer r, and some r-coloring of the real numbers, such that the equation Σ ci(xi − x0) = b ≠ 0 has no [monochromatic] solution." Then: "It extends the fundamental work of R. Rado [6]." EGMRSS's [6] is Rado, *Note on combinatorial analysis*, PLMS (2) 48. Proof of Thm 13: colour by χ(‖v‖²), i.e. "spherical shells". | **ACCURATE**. Prop 2.4 proves its own modular colouring and only credits EGMRSS for the strategy. |
| [4] **Prop 4** | Lemma 5.2: "the compactness principle … compare [4, Proposition 4]" | Prop 4 is the finite-subsets compactness statement for the Ramsey property. | **ACCURATE** (cited only as "compare"). |
| [7] Graham 1994 | §1: "Graham later conjectured that sphericity is also sufficient [7]" | p. 120: "Conjecture ($1000). If X is spherical then X is Ramsey." EGMRSS p. 350 had left this "undecided". | **ACCURATE**. Pálvölgyi and ILW attribute the question to EGMRSS; Graham made it a conjecture. That is consistent with "later conjectured". |
| [15] LRW 2011, **Cor 2** | Cor 7.5: "Leader, Russell and Walters proved that K_a does not embed in any finite transitive Euclidean set [15, Corollary 2]" for transcendental a ∈ (−1,1) | arXiv:1012.5468v1 p. 2: "Corollary 2. The cyclic quadrilateral with vertices (−1,0), (1,0), (a,√(1−a²)), (a,−√(1−a²)), where a is transcendental, does not embed into any transitive set." Here "transitive set" means a *finite* transitive set. Lemma 4 uses a finite group G, and LRW 2012 says "when we say X is transitive we shall assume implicitly that X is finite". | **ACCURATE**. The kite is the same point set. LRW state no range for a; the paper's a ∈ (−1,1) is just the condition for real coordinates. I re-derived the reduction: with z=(−1,0), y=(1,0), x=(a,√(1−a²)), w=(a,−√(1−a²)) one gets α = −1 ≠ 1 and β = a+1, which is transcendental over Q(α) = Q. So Thm 1 applies. I also re-checked the α<0 case of Lemma 4 (β = α, triangle-inequality equality case); it is sound. |
| [15] **Conj 3** | §1 and after Cor 7.5: "The same family also disproves their conjecture that these kites are not Ramsey [15, Conjecture 3]" | p. 3: "Conjecture 3. Let −1 < α < 1 be transcendental. Then the cyclic quadrilateral with vertices (−1,0), (1,0), (a,√(1−a²)), (a,−√(1−a²)) is not Ramsey." (The α/a mismatch is a typo in the source.) | **ACCURATE** |
| [16] LRW 2012, **Conj A** | §1 and after Cor 7.5: "a finite set is Ramsey exactly when it embeds in a finite transitive Euclidean set [16, Conjecture A]"; "the necessity direction … fails" | arXiv:1012.1350v1 p. 3: "Conjecture A. A finite set X ⊂ Rn is Ramsey if and only if it is (congruent to) a subset of a finite transitive set." | **ACCURATE**. Cor 7.5 refutes the Ramsey ⇒ subtransitive direction only. |
| [16] **Conj C**, §§2–3 | §1 ("group and word methods … [16, Sections 2–3]"); proof of Prop 5.1: "the number of varying positions is prescribed before coloring; without that restriction, ordinary Hales–Jewett applies" | Conj C: "there exist positive integers n and d such that whenever Gⁿ is k-coloured there exists a word g and a set I ⊂ [n] with \|I\| = d …"; next paragraph: "without the restriction '\|I\| = d', Conjecture C would be an easy consequence of the Hales-Jewett theorem." §2 holds Conjectures B–F; §3 is "The first cases of Conjecture E". | **ACCURATE** |
| [18] Mirabi 2608.11736v1 | §1: "Moore and, independently, Mirabi proved that adjoining a point outside the affine span of a Ramsey set preserves the Ramsey property" | "Theorem 1.1. Let X be a finite Ramsey set in a Euclidean space, and let z be a point outside aff(X). Then X ∪ {z} is Ramsey." Plus: "obtained independently of the recent preprint of Moore [4] … circulated privately … in June 2026." v1 dated 12 Aug 2026. | **ACCURATE** |
| [19] Moore 2608.09649v1 | same sentence | "Theorem 1.2 (Conjecture 8 in [7]). Let B be a finite Ramsey set … z … outside of the affine hull of B. Then B ∪ {z} is Ramsey." v1 dated 10 Aug 2026. | **ACCURATE** |
| [20] Pálvölgyi 2609.23327v1, **Thm 1** | §1: "a seven-point circle configuration that is not Ramsey, disproving the spherical conjecture [20, Theorem 1]" | "Theorem 1. For any transcendental r > 2, the seven-point set P = {(0,0)} ∪ {(j, ±√(j(2r−j))) : j ∈ {1,3,4}} lies on the circle (x−r)² + y² = r² and is not Ramsey." | **ACCURATE** |
| [20] **Thm A.2** | after Prop 7.3: "products of two line equations supply the required interpolation. The same observation appears in Pálvölgyi's analysis … [20, proof of Theorem A.2]" | Proof of A.2: "At any specified point among at most five distinct circle points, a quadratic polynomial can be nonzero while vanishing at all the others: take the product of two line equations covering the other points and avoiding the specified point." (A.2 itself says that ≤ 6 circle points admit no nonzero fixed derivation-energy identity.) | **ACCURATE** (cited for the observation only, not for a Ramsey conclusion). |
| [20] **Thm A.3** | §1 and before Prop 7.6: "generic seven-point claim [20, Theorem A.3] already implies its non-Ramsey conclusion by taking a subset; the source labels its appendix as unchecked" | "Theorem A.3. … p(t) = ((1−t²)/(1+t²), 2t/(1+t²)). Fix three distinct real numbers t1, t2, t3. If t4,…,t7 are algebraically independent over K = Q(t1,t2,t3), then {p(t1),…,p(t7)} is not Ramsey." It sits under the header "Appendix by ChatGPT — unchecked". | **ACCURATE**. It is the same parametrisation, and 9 algebraically independent parameters contain 7 that satisfy the hypotheses. A non-Ramsey subset makes the superset non-Ramsey. |
| [20] **author's note** | §1: "Its author's note announces a proof that all finite transitive sets are Ramsey and says that its exposition is still being prepared." Footnote: writing, proofs and ideas attributed to ChatGPT; appendix unchecked. | "ChatGPT did find a proof that all transitive sets are Ramsey; … I am still working on the exposition of that proof, which uses elementary group theory." AI disclosure: "written entirely by ChatGPT. I … contributed nothing to the proofs or ideas … Appendix … further results by ChatGPT that I have not verified." | **ACCURATE** |
| [1] Behague 2510.15677v3 | §1: "constructed soluble transitive extensions for many known Ramsey classes and further permutation configurations" | Title: *Nearly all known Euclidean Ramsey sets are subsoluble*. Thm 1.5: "The following sets are subsoluble"; Thm 1.6 covers permutation sets X(i,j,1,1). v3 dated 4 Dec 2025. | **ACCURATE** |
| [10] ILW, Forum Math Sigma 14:e67 (arXiv:2406.01459) | §1: "Their group-theoretic and Hales–Jewett formulations led to the Block Sets Conjecture; subsequent work studies the possible block sizes" | The abstract says the block sets conjecture was "introduced by Leader, Russell and Walters"; the paper shows "the sizes of the blocks … cannot be bounded". Crossref confirms FMS 14 (2026). | **ACCURATE** |
| [11] ILW 2606.13472v1 | §1: "generalized-prism constructions, with Ramsey conclusions under a soluble symmetry hypothesis" | "the 'prism' … is itself contained in a finite set on which a group of isometries acts transitively. Moreover, if the initial group … is soluble then so is the final group." | **ACCURATE** |
| [12] Karamanlis, EJC 29(3) 3.66 | §1: "embedded every simplex in a finite product of regular polygons" | arXiv abstract: "any finite affinely independent set can be isometrically embedded into a regular polygonal torus, that is, a finite product of regular polygons." | **ACCURATE** |
| [13] Kříž 1991 PAMS 112:899–907 | §1: "finite sets with a soluble transitive isometry group … by Kříž" | Primary text not reached (AMS returned 403). Secondary sources agree: LRW 2012 p. 2 ("any finite set X which is acted on transitively by a soluble group G of isometries is Ramsey … soluble subgroup … at most two orbits"); Graham 1994; Behague Thm 1.2. Metadata confirmed via Crossref. | **ACCURATE** (via secondary sources) |
| [14] Kříž 1992 Discrete Math 108:59–62 | §1: "cyclic trapezoids, by Kříž" | Title: "All trapezoids are Ramsey". A non-cyclic trapezoid is non-spherical, so the content is the isosceles (= cyclic) ones; Behague says "isosceles trapezia [10]". The primary text returned 403. | **ACCURATE** (via secondary sources) |
| [2] Cantwell, JCTA 114:555–562 | §1: "vertex sets of regular polytopes, by Cantwell" | Title: "All regular polytopes are Ramsey" (Crossref). LRW 2012: Cantwell used Kříž to handle the 120-cell. Primary text 403. | **ACCURATE** (via title and secondary sources) |
| [23] Stacks, Tag 00MB | Lemma 3.1 proof: "R is Noetherian … Its m-adic completion is therefore flat over R [23, Lemma 10.97.2, Tag 00MB]" | "Lemma 10.97.2. Let I be an ideal of a Noetherian ring R. … The ring map R → R^∧ is flat." | **ACCURATE**. The next step, I·R^ = ∩ J_i·R^ (tensoring the injection R/I → ⊕R/J_i with a flat module), is correct. |
| [3] Ellis 1958, Lemma 1 | before Lemma 5.4: "Ellis's semigroup lemma [3, Lemma 1]; taking the opposite semigroup matches the one-sided continuity convention" | "LEMMA 1. Let S be a compact Hausdorff space with a semigroup structure such that the maps s → ts … are continuous for all t ∈ S. Then there exists an idempotent." (Left translations here; the paper uses right ones, hence the "opposite semigroup" remark.) | **ACCURATE** |
| [9] Hindman–Strauss, Thms 2.5, 1.42, Cor 2.6 | before Lemma 5.4 | Checked against the **2nd edition (2012)**: Thm 2.5 says a compact right topological semigroup has an idempotent; Cor 2.6 says minimal left ideals are closed and contain idempotents; Thm 1.42 says that for a minimal left ideal L with idempotent e, "G = eL = eSe is a group". The product convention matches the paper's (20). I did not check the cited 1998 first edition's numbering. Lemma 5.4 is proved in full in the paper anyway. | **ACCURATE** (2nd-ed numbering; non-load-bearing) |
| [8] Hales–Jewett; [22] Shelah p. 686 | proof of Prop 5.1 | Standard; only the existence of the HJ length is used. I did not reach Shelah p. 686. | Not checked; non-load-bearing |
| [21] Rado; [17] Liouville | context | Crossref gives 1945 for PLMS s2-48 (EGMRSS wrote 1943). Liouville 1851 is the standard Liouville-number source. | **ACCURATE** |

All 23 reference entries also match Crossref metadata and arXiv version dates (titles, volumes, pages, years). The arXiv version dates: Pálvölgyi v1 is Sun 20 Sep 2026 03:28 UTC, Behague v3 is 4 Dec 2025, Moore v1 10 Aug, Mirabi v1 12 Aug, ILW prisms v1 11 Jun 2026.

**Objections from the citation layer:** none rise to FATAL, GAP or ERROR-NONFATAL. Two EXPOSITION-level notes:

- (E1) The Hindman–Strauss theorem numbers were checked against the 2012 2nd edition, while the paper cites the 1998 edition. Lemma 5.4 is self-contained, so nothing depends on this.
- (E2) Cor 7.5's non-subtransitivity rests entirely on LRW 2011 Cor 2. That result is cited, not re-proved, and it is **not** in OpenAI's Lean: grep of `OAI/Combinatorics/{EuclideanRamsey,SphericalRamsey}` finds no kite or subtransitive content. `docs/172.md` correctly claims only the ≤ 5-circle-points Ramsey half. CONTENTS.md's "It also disproves the Leader–Russell–Walters conjecture" is therefore part formal (Ramsey half) and part cited (LRW Cor 2). I checked LRW Cor 2 and it is sound.

## 2. World

### (a) Other characterisation claims, and responses (2025–2026)

**No independent characterisation claim found.** I searched arXiv (title/abstract/author searches: "Euclidean Ramsey", "spherical Ramsey", "non-Ramsey", "subtransitive", "transitive sets Ramsey", "Ramsey configurations", "sphere-Ramsey", "Ramsey OpenAI"; Pálvölgyi's author listing), GitHub, the web (blogs, MathOverflow, X/HN via web search), the erdosproblems page and forum text in `live/`, and Tao's `teorth/erdosproblems` database. The responses I found:

- **Axenovich–Liu–Sagdeev, arXiv:2512.15516v3 (13 Oct 2026)**. This is the only arXiv response found. §1.4: "Rather surprisingly, both conjectures have recently been disproved. Pálvölgyi [81] constructed a 7-point counterexample to Graham's conjecture [52], while OpenAI [79] found a 4-point counterexample to the conjecture of Leader, Russell, and Walters [72]. Moreover, OpenAI [79] announced a complete characterization of Ramsey sets in terms of a tensor condition over their coordinate fields." It is hedged ("announced"), and it is neither a critique nor a check.
- **erdosproblems.com #174.** The page was last edited 16 Oct 2025, and the site no longer displays statuses. The forum has 5 comments; the last is Pálvölgyi's, 23 Sep 2026 09:20: "ChatGPT 6 found a counterexample for Graham's conjecture, a cyclic non-Ramsey heptagon". There is no mention of OpenAI, and new comments are suspended. **teorth DB** (`data/problems.yaml`): #174 `status: open` (last_update 2025-08-31), `formalized: yes` (2026-10-20). Nothing on Bloom's page records the heptagon or OpenAI as resolving anything.
- **No blog posts, MathOverflow threads or X posts** were found from Bloom, Pálvölgyi, Leader, Walters or Tao about OpenAI #172. Emergent Mind's OpenAI-math explorer lists #172 with LRW "Disproved"; it shows no reviews or errata.
- **Third-party work building on #172.** All of it is AI-produced, says "no human expert has reviewed", and trusts OpenAI's Lean sufficiency proof:
  - JD-Jones-ASES/six-concyclic-lean (from 2026-10-07): ≤ 6 concyclic points satisfy the criterion; an "m+4" dimension theorem; the algebraic case (see §3).
  - Rogerhu12/openai-math-extensions (2026-10-07).
  - atimics/math2 (2026-10-08).
  - wstrinz/spherical-ramsey, mobius-ramsey and algebraic-plus-three-ramsey (2026-10-13 to 10-16, with Zenodo DOIs). Among other claims: Möbius invariance of Ramsey; "algebraic concyclic points + ≤ 3 arbitrary points on the circle are Ramsey".
  - None disputes #172.
- **Consistency cross-check.** Two partly independent ChatGPT-generated lines agree at the boundary. Pálvölgyi's appendix, which does not use #172, gives:
  - A.2/A.11: derivation certificates cannot refute ≤ 6 spherical points;
  - A.3: 3 fixed + 4 independent circle points are not Ramsey;
  - A.10: certificates cannot exist for algebraic-plus-≤3 circle sets, which "does not determine whether the configuration is Ramsey".

  The #172-based results above give exactly the matching positive side. I found no contradiction anywhere.

### (b) Pálvölgyi arXiv:2609.23327: revised?

**No.** As of 2026-10-21 the abs page lists only `[v1] Sun, 20 Sep 2026 03:28:20 UTC (23 KB)`, and `arxiv.org/abs/2609.23327v2` returns HTTP 404 "Article not found". His arXiv author listing and his homepage (`domotorp.web.elte.hu/cikkek/`) show nothing newer than 2609.23327. The announced "all transitive sets are Ramsey" proof has **not** been posted.

### (c) Formal Conjectures, Erdős #174

**File and provenance.** The file is `FormalConjectures/ErdosProblems/174.lean`, blob sha `95dbb296…`; my verbatim copy is `W_src/fc_174.lean` (sha256 `b6ac1bcd…`, FC main head `2a315101`, 2026-10-21T11:11Z). It was added **yesterday** in PR #7469 (veljjanoski, opened 2026-10-20T06:42Z, merged 15:57Z; "Fixes #404"; "AI-usage disclosure: Claude"). That is its only commit, and there are no later or open PRs touching it. The PR body says of Graham's and LRW's conjectures: "Both are open." That is stale: it ignores Pálvölgyi's 20 Sep heptagon and OpenAI's #172.

**Statements in the file:**

| Declaration | Category | Content |
|---|---|---|
| `erdos_174 (n) : {A \| IsRamsey A} = erdos_174.answer n` | `research open`, `question value` | The answer is `sorry`. |
| `erdos_174.variants.spherical` | `research solved` | IsRamsey A → Cospherical A |
| `erdos_174.variants.graham` | **`research open`** | A.Finite → Cospherical A → IsRamsey A |
| `erdos_174.variants.leader_russell_walters` | **`research open`** | A.Finite → (IsRamsey A ↔ IsSubtransitive A) |
| `brick`, `simplex`, `trapezoid` (isosceles) | `research solved` | — |
| `isRamsey_singleton` | `test` | Proved. |

`IsRamsey` is defined as A.Finite ∧ ∀ k ≥ 1, ∃ d, ∀ c : ℝᵈ → Fin k, ∃ p : A → ℝᵈ, Mathlib `Congruent` (edist) ∧ monochromatic. `IsTransitive` uses ambient isometries g with g''X = X.

**Related FC item:** `FormalConjectures/Paper/EuclideanRamseyCircle.lean` (PR #6980, issue #6975, by anxkhn using GPT-6.1 Sol; merged **2026-10-21 10:05Z**). It states OpenAI's Cor 7.4 (≤ 5 circle points Ramsey) as `research solved` with no `formal_proof` attribute. Maintainer mo271 asked for a link to OAI `Circle.lean`; the author declined until the axiom closure was checked. Its statement is OAI's comparator `at_most_five_circle_points_ramsey` with `Ramsey` unfolded. So FC now holds a #172 consequence as solved while 174.lean still says the Graham and LRW conjectures are open.

**Bridges, as I assess them (no Lean compiled):**

1. **`erdos_174.variants.graham` is false and formally refutable now**, from `OAI.GrahamSpherical.full_main`. The witness has `ncard = 12`, hence is finite, and lies ⊆ `Metric.sphere 0 1`, hence is Cospherical. The definitions bridge: FC `IsRamsey witness` → OAI `EuclideanRamsey witness`. The k ≥ 1 / r > 0 quantifiers match; d > 0 is forced because 12 distinct points cannot be congruent into ℝ⁰; Mathlib `Congruent` on the subtype is exactly `Isometry` (edist equality). So `¬ (∀ n A, A.Finite → Cospherical A → IsRamsey A)` at n = 2.
   - This route **does not depend on the classification**: `SphericalRamsey/*` imports only Mathlib and its own files.
   - Pálvölgyi's heptagon would also refute it, but it is not formalized.
2. **`erdos_174.variants.spherical`** bridges from `OAI.EuclideanRamsey.ramsey_cospherical` (comparator `EuclideanRamseySpherical.lean`). Enumerate finite A injectively; the ≤ 1-point case is trivially cospherical; for ≥ 2 points, d ≥ 1 is forced.
3. **`leader_russell_walters` (iff).**
   - The "if" half, IsSubtransitive → IsRamsey, bridges from `OAI.EuclideanRamsey.TransitiveConsequence.subset_of_finite_transitive_ramsey`. FC's ambient-isometry transitivity gives OAI's distance-preserving permutations directly (the easy direction), and `ramsey_congruent_iff` transfers back to A. FC has no separate solved variant for this half.
   - The "only if" half is refuted only informally (Cor 7.5). A formal refutation needs LRW 2011 Cor 2, which is not formalized anywhere I found; it requires finite-group representations over algebraic numbers. So the iff **cannot** be formally disproved from OAI's Lean alone.
4. **`erdos_174` (answer set).** OAI `Main.lean` has `classification_nonempty`: for injective nonempty a, Ramsey a ↔ s = 1 ∨ there is a congruent full-affine-span representative b with `FieldCriterion b`. That supplies a candidate `answer n` together with a proof modulo Set ↔ Fin bookkeeping.
   - Whether FC would accept the tensor criterion as "the answer" to a `question value` problem is an editorial call.
   - The criterion is exact-algebraic. The paper itself says it "is not a procedure for recovering those relations from numerical approximations".
   - `classification` itself (comparator `EuclideanRamsey.lean`: `Ramsey a ↔ FieldCriterion a` under hs, hd, injective, full span) is exactly the full-span case.

### (d) openai/math CONTENTS.md entry 172, and errata

I copied the entry verbatim to `W_src/openai_CONTENTS_172.md`. Its blob sha `2c68c086…` is identical on live GitHub and in the local checkout at HEAD `1581d4c` (2026-10-12). It reads:

> "**172. Classification of finite Euclidean Ramsey configurations.** Classifies finite point configurations that occur monochromatically, at their original scale, in every finite coloring of sufficiently high-dimensional Euclidean space. The characterization is an algebraic condition over the coordinate field. It also disproves the Leader–Russell–Walters conjecture that every such configuration is a subset of a finite transitive set."

**Errata:** none.
- The repo has **issues disabled** (`has_issues: false`), and PR conversations are auto-locked (PR #2).
- Only 2 PRs exist: #1 "Update manuscripts and Lean formalizations" (10-08), which mentions "withdrawal notices" for other families, and #2.
- `git diff adc7f124..HEAD` touches **no** family-172 file (preprint, `docs/172.md`, `EuclideanRamsey/*`, `SphericalRamsey/*`, comparators). `paper.pdf` at HEAD has sha256 `0900061b…`, identical to our copy, and CONTENTS has no 172 change.

## 3. Novelty: "every spherical finite set with algebraic coordinates is Ramsey"

**Not stated in the OpenAI paper.**
- grep of all `.tex` and `paper.txt` for "algebraic number", "number field", "Qbar", "separable", "finite extension", "product of fields" finds nothing relevant.
- The closest sentence (after Thm 1.1) is: "It uses exact relations in the coordinate field."
- Prop 7.3 and Cor 7.4 are the only positive families. Neither CONTENTS.md nor `docs/172.md` mentions the algebraic case.

**Not stated in Pálvölgyi.** Appendix Thm A.10 (unchecked ChatGPT) comes closest: "Derivations annihilate algebraic numbers, so b_i = 0 at every point with algebraic coordinates … This is a limitation of the certificate method and does not determine whether the configuration is Ramsey." That is a method limitation, not a Ramsey claim. His 2608.10865 also has nothing of the sort.

**Not on erdosproblems.com, the forum, or Bloom's material.**

**It is stated publicly elsewhere.** Earliest first:

1. **JD-Jones-ASES/six-concyclic-lean**, root commit `0703d7d2`, **2026-10-07T02:56Z**. The README at that commit lists "every spherical set with algebraic coordinates, of any size — `algebraic_spherical_fieldCriterion`" and "every spanning spherical set with algebraic coordinates is Ramsey — `algebraic_spherical_ramsey_of_sufficiency`". In `Challenge.lean`:

   > "/-- Every spherical set whose coordinates are algebraic numbers satisfies the tensor criterion, whatever its size: the separability idempotent of `F ⊗_ℚ F` lifts an `F`-rational sphere. -/ theorem algebraic_spherical_fieldCriterion … (halg : ∀ i j, IsAlgebraic ℚ (a i j)) (hsphere : …) : FieldCriterion a"

   The criterion level is unconditional; the Ramsey conclusion is conditional on a hypothesis `hsuff` standing for OpenAI's sufficiency direction. The README claims that, as of 2026-10-07, no such statement was located in the paper, the Lean tree, arXiv, MathOverflow, erdosproblems, FC, Palomar or GitHub.
2. **Rogerhu12/openai-math-extensions**, commit `f8a2bb24`, **2026-10-07T20:18Z**, `papers/172-euclidean-ramsey/algebraic_spherical_configurations.tex`:

   > "Assume the source tensor criterion. Every finite nonempty spherical set whose coordinates are real algebraic numbers is Euclidean Ramsey."

   Proof sketch: algebraic Gram–Schmidt reduction to full span, then the separability idempotent.
3. **atimics/math2**, commit `8ab51fac`, **2026-10-08T18:18Z**: `EndToEnd/AlgebraicRamsey.lean`. This is "end to end in Lean for configurations with full affine span", using OpenAI's proof.
4. **wstrinz/spherical-ramsey** v1.0.0 (2026-10-14) "Theorem A. A finite spherical set with real algebraic coordinates is Ramsey" (Lean, with no affine-span hypothesis). It credits items 1–3 as prior work. The same author's algebraic-plus-three-ramsey (2026-10-16) adds "+ ≤ 3 arbitrary circle points".

**Bottom line for §3.** The statement is an immediate corollary of Theorem 1.1, and it is **not novel as a public claim**: four AI-generated GitHub/Zenodo artifacts state it from 2026-10-07, all resting on OpenAI's #172. It appears in **no** human-authored or peer-reviewed source and in **no** arXiv paper I could find. None of these artifacts has been reviewed by a human expert.

I checked the mechanism the coordinator gave. For a number field F, F ⊗_ℚ F is étale with a separability idempotent e: m(e) = 1, and (x⊗1 − 1⊗x)e = 0. Then P := (H⊗1)·e, with H the F-rational sphere matrix, satisfies (p_i⊗1)ᵀP(1⊗p_i) = (p_iᵀHp_i ⊗ 1)e = 0 and m(P_αβ) = δ_αβ on the spatial block. An exact-arithmetic check for Q(√2), with e = ½(1⊗1 + ½√2⊗√2), confirms (√2⊗1 − 1⊗√2)e = 0, e² = e and m(e) = 1.

## Summary of objections (this seat)

- **FATAL:** none.
- **GAP:** none.
- **ERROR-NONFATAL:** none.
- **EXPOSITION:**
  - E1: Hindman–Strauss numbering verified only against the 2nd edition.
  - E2: Cor 7.5's non-subtransitivity half is a citation (accurate) and is not in OpenAI's Lean, while CONTENTS.md words the LRW disproof without that distinction.
- **Not reached (paywall/403):** the primary texts of Kříž 1991 and 1992, Cantwell 2007, and Shelah p. 686. All are context-only; secondary sources agree with how the paper uses them.
- **World-state discrepancies** (not paper errors):
  - FC `174.lean` (added 2026-10-20) still tags `graham` and `leader_russell_walters` as `research open`. `graham` is formally refutable today from `OAI.GrahamSpherical.full_main`, independently of the classification.
  - teorth DB lists #174 `open`.

All cited statements say what the paper uses them for, and no public source disputes the paper.

VERDICT: HOLDS AS READ
