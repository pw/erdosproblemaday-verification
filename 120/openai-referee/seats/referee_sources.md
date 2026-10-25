# Referee report — SOURCES (tag: sources)

**Scope:** the reference lists and §1.1 of both papers (GEOMETRIC, 5 Oct 2026, 13 pp; DYADIC, 25 Sep 2026, 16 pp), every body sentence that cites an outside source, and the live literature as of 2026-10-14. I did not referee the proof itself (§§2–5 / §§2–6). Part C (the live-world sweep) was run by one delegated research seat. I re-verified its load-bearing items against the saved artifacts: Green's Problem 94 text, the formal-conjectures `green_94` and `erdos_120` statements, the Jiang–Xi attribution paragraph, and Bloom's #120 paragraph.

**Where the evidence is (all under /tmp/erdos0300/refs/):**
- **Primary PDFs:** `<arxiv-id>v<n>/paper.pdf` with `paper.txt`. These cover 1512.05607v1, 2001.02395v1, 2204.12720v1, 2208.02637v1+v2, 2312.01319v1, 2607.03584v1+v2 and 2609.04456v1.
- **Other papers:**
  - `kol97/`: the author's preprint of Kol97 (ps2ascii plus rendered pages 9, 11 and 12).
  - `hl98/` and `fal84/`: Wayback copies of the AMS PDFs. ams.org itself served a bot challenge.
  - `sol11/` and `tom15/`: the UBC USRA PDFs.
- **arXiv metadata:** `abs/*.html`, the arXiv abstract pages with their version-history blocks.
- **Live sweep:** `live/` (`LIVE_FINDINGS.md` plus raw fetches).

## Objections (numbered)

None of these touches the mathematics of Theorem 1.1. Nothing in my scope is FATAL or a GAP.

**S1. [Erd74] / dyadic [6]: a sub-locator that cannot be verified, on a citation the literature itself disagrees about.**
- *Location:* GEOMETRIC p.1, "The Erdős similarity conjecture [Erd74, Problem 4.33.7*] asserts that no infinite set is measure universal", and its reference list p.12: "Paul Erdős. Problems. Mathematica Balkanica, 4:203–204, 1974. Problem 4.33.7*." DYADIC p.1 "[6, Problem 4.33.7*]" and ref [6], with the same text.
- *What I found:* The item "P. Erdős, Problems, Math. Balkanica 4 (1974), 203–204" is the citation used by HL98 (with "MR 55:2715"), Falconer 1984, KP25 and IKMC+26, so the item exists in the standard citation tradition.
  - zbMATH indexes only "Erdős, Remarks on some problems in number theory, Math. Balk. 4, 197–202 (1974)".
  - The Jung–Lai–Mooroogen survey (arXiv:2412.11062v2) cites the problem's origin as that same 197–202 item, "MR 429704", quoting Erdős: "I hope there are no such sets".
  - **"Problem 4.33.7*" appears in no source independent of OpenAI.** I grepped 23 downloaded texts and ran two web searches. Its only other occurrence is Jiang–Xi, arXiv:2610.11449 (8 Oct 2026), ref [5], which builds on the OpenAI manuscripts and evidently copied the citation.
- *Severity:* COSMETIC. It is bibliographic, and possibly an invented precision.
- *Fix:* drop "Problem 4.33.7*", or cite a document that carries that numbering. Ideally reconcile 197–202 against 203–204.

**S2. Formalization status of the GEOMETRIC theorem is overstated by the release packaging (not by the paper).**
- *Location:* openai/math `CONTENTS.md`, entry 084: "This resolves the geometric-progression case of the Erdős similarity conjecture for every ratio. ([Lean](lean/docs/084.md))". The linked `lean/docs/084.md` (local copy /tmp/oaimath/084/lean_doc.md) is headed "# The geometric case of the Erdős similarity conjecture", yet its Scope says "The formalization proves the dyadic case of the Erdős similarity conjecture". It links only the DYADIC paper.
- *What is wrong:* the only comparator is `DyadicAvoidance.lean` (q = 1/2). **Geometric Theorem 1.1 for q ≠ 1/2 has no Lean proof.** A reader following the "Lean" link from the geometric headline would think otherwise.
  - Bloom's blog post states it correctly: "formalised in the special case when q=1/2".
  - So does the third-party re-check (haraldschilly/math-distance-set-similarity): "`GeometricAvoidanceStatement q` … no (q = 1/2 is the dyadic case)".
- *Severity:* COSMETIC for the paper, which never claims a formalization. It is material for anyone writing "Lean-verified geometric case".
- *Fix:* retitle `084.md`, or state in it that only q = 1/2 is formalized.

**S3. DYADIC §1.1 slightly over-describes Cruz–Lai–Pramanik.**
- *Location:* DYADIC p.2: "the avoiding sets in their construction have Lebesgue measure zero [4, preprint, Corollary 1.2 and Proposition 4.4]".
- *What the source says:* CLP's Prop 4.4 says only that the *exhibited subset* O has measure zero: "the set O constructed in (2.11) has Lebesgue measure zero". CLP explicitly leave the full avoiding set open: "We do not know if there are more points in E_K other than points in O". Their open problem 2 asks whether E_K has positive measure.
- The CLP *abstract* does say "we construct a Borel set O … of Hausdorff dimension 1, but Lebesgue measure zero", so the dyadic wording is defensible as a description of "the constructed set".
- The GEOMETRIC paper already uses the precise version: "the subsets establishing that dimension have Lebesgue measure zero".
- *Severity:* COSMETIC.

**S4. Related work not cited, including the survey that states this exact open question.**
- *Location:* both §1.1 sections and both reference lists.
- *What is omitted:* neither paper cites any of the following.
  - Jung–Lai–Mooroogen, *Fifty years of the Erdős similarity conjecture* (arXiv:2412.11062v2; Res. Math. Sci. 12 (2025) art. 9). Its Question 7.2 is exactly Theorem 1.1 with q = 1/b: "Let b > 1 be a real number. Is there a set of positive measure containing no sequence (x + yb^{−n}) for any x, y ∈ R with y ≠ 0?" The same survey says determining whether (2^{−n}) is measure universal "has been the major bottleneck of the problem".
  - Svetic's survey (RAE 26, 2000/01). Green's Problem 94 points to it.
  - Burgin–Goldberg–Keleti–MacMahon–Wang (RAE 48(2):351–364, 2023; arXiv:2210.09284). They ask whether every positive-measure set contains a similar copy of *some* infinite geometric progression, with the ratio free.
    - Theorem 1.1 does **not** answer that, because its E depends on q.
    - The geometric abstract correctly disclaims this: "the result makes no simultaneous assertion for different ratios".
  - Gao–Mooroogen–Yip (BLMS 57(6), 2025), Shmerkin–Yavicoli (2503.21079), Iosevich–Yavicoli (2604.01493) and Kolountzakis 2023. All of these are cited by IKMC+26, which the papers do cite.
- *Severity:* COSMETIC. Completeness only; none of these contains the result (see Part C).
- *Fix:* cite JLM24 Question 7.2 as the precise statement being answered, and BGKMW23 as the open ratio-free variant.

**S5. "preprint" labels and numbering source.**
- *Location:* GEOMETRIC p.2 "[CLP23, preprint, Corollary 1.2 and Proposition 4.4]" and "[FLX24, preprint, Theorem 1.1]". DYADIC "[4, preprint, …]" and "[8, preprint, …]".
- *What is wrong:* both works are published (RAE 2023; IMRN 2024), and the reference lists give the journal versions. The theorem numbers are taken from the arXiv v1s, which I read. I did not check them against the journal versions.
- *Severity:* COSMETIC.

**S6. Two cited originals could not be fetched.**
- Bourgain 1987 (Springer, paywalled) and Eigen 1985 (Akadémiai Kiadó, 2 pp).
- Their characterisations are corroborated by secondary sources quoted in B7–B8 below:
  - Kol97 §0.3, MCIK+26 §1, CLP23 §1 and Chlebík §5 for Bourgain;
  - HL98 Corollary 1 and the zbMATH review for Eigen.
- *Severity:* UNCLEAR (unverified at source), almost certainly MATCH.

## Lemma / statement status for my scope

| Item | Status |
|---|---|
| GEOMETRIC §1 statement of Theorem 1.1 (p.1) vs abstract, vs Lean comparator at q = 1/2 | VERIFIED LINE BY LINE |
| GEOMETRIC §1.1 finite-pattern (Steinhaus) argument | VERIFIED LINE BY LINE (B21) |
| GEOMETRIC §1.1 Chlebík display and the "geometric progressions fail it" computation | VERIFIED LINE BY LINE (B1, B22) |
| GEOMETRIC §1.1, every remaining sentence carrying a citation | VERIFIED against source (Part B) |
| GEOMETRIC body citations p.10 ("[Chl15, proof of Theorem 15] and [KP25, Section 3.1]") and p.11 ("Tom [Tom15, Lemma 0.2]; see also Chlebík [Chl15, Section 3, final remark; Proposition 1(vi), (viii)]") | VERIFIED against source (B16–B19) |
| DYADIC §1 Theorem 1.1, §1.1 (every sentence), §1.2 citation sentences (p.3), body citations p.11 and p.13 | VERIFIED against source |
| DYADIC §1.1 IKMC+26 Prop 3.2 non-applicability to D ∪ {0} (2^k-invariance mod 1, distance 1/4 from 3/4) | VERIFIED LINE BY LINE (B12) |
| GEOMETRIC Prop 2.1, Lemmas 3.1–3.3, 4.1–4.3, 5.1, §2 deduction, §5 repair; DYADIC §§2–6 | NOT READ (outside this scope) |
| OpenAI Lean proof (`OAI/MeasureTheory/DyadicAvoidance/*`, 75 files) | NOT READ / NOT REPLAYED. Only the comparator statement was checked (Part D). |
## Part A — Does every cited work exist as described? (bibliographic check)

Read: arXiv abs pages (version-history blocks fetched 2026-10-14), Crossref API, zbMATH API, publisher/author PDFs. File locations under /tmp/erdos0300/refs/.

| Key (geo / dyadic) | As cited | What the record says | Verdict |
|---|---|---|---|
| [Bou87] / [1] | Bourgain, *Construction of sets of positive measure not containing an affine image of a given infinite structure*, Israel J. Math. 60(3):333–344, 1987 | Crossref 10.1007/bf02780397: same title, J. Bourgain, Israel J. Math. vol 60 iss 3 pp 333–344, Dec 1987 | EXISTS |
| [Chl15] / [2] | Chlebík, *On the Erdős similarity problem*, arXiv:1512.05607v1, 17 Dec 2015 | arXiv abs: "On the Erdös similarity problem", Miroslav Chlebik, history "[v1] Thu, 17 Dec 2015 14:43:50 UTC (20 KB)", only version, 17 pp | EXISTS (title spelled "Erdös" on arXiv — cosmetic) |
| — / [3] | Cruz, Lai, Pramanik, *A proof of the Erdős similarity conjecture*, arXiv:2001.02395v2, withdrawn; v2 11 Jan 2020 | arXiv abs: "[v1] Wed, 8 Jan 2020 06:58:09 UTC (10 KB) [v2] Sat, 11 Jan 2020 22:40:16 UTC (1 KB) (withdrawn)"; comment "A gap was found in Proposition 3.3 of the paper. We would like to thank professor Vjekoslav Kovac for pointing this out. Therefore, we would like to withdraw the paper" | EXISTS; description (withdrawn, gap in Prop 3.3, claimed full conjecture) MATCH |
| [CLP23] / [4] | Cruz, Lai, Pramanik, *Large sets avoiding affine copies of infinite sequences*, Real Anal. Exchange 48(2):251–270, 2023; arXiv:2204.12720v1 | Crossref 10.14321/realanalexch.48.2.1681628520: same title/authors, RAE vol 48 iss 2 pp 251–270, 2023-10-01. arXiv: only "[v1] Wed, 27 Apr 2022" | EXISTS |
| [Eig85] / [5] | Eigen, *Putting convergent sequences into measurable sets*, Studia Sci. Math. Hungar. 20(1–4):411–412, 1985 | zbMATH 0627.28004: same title, S. J. Eigen, Stud. Sci. Math. Hung. 20, 411–412 (1985) (issue field empty in zbMATH; "1–4" not independently confirmed) | EXISTS |
| [Erd74] / [6] | Erdős, *Problems*, Math. Balkanica 4:203–204, 1974, "Problem 4.33.7*" | HL98's bibliography: "P. Erdős, Problems, Math. Balkanica 4 (1974), 203–204. MR 55:2715"; same in Falconer 1984, KP25, IKMC+26. zbMATH indexes only Erdős, *Remarks on some problems in number theory*, Math. Balk. 4, 197–202 (1974), not the 203–204 item. **The problem number "4.33.7*" appears in no source I could fetch** (none of the 12 downloaded papers, two web searches) | EXISTS; "Problem 4.33.7*" UNVERIFIED |
| [Fal84] / [7] | Falconer, *On a problem of Erdős on sequences and measurable sets*, PAMS 90(1):77–78, 1984 | Crossref 10.1090/s0002-9939-1984-0722418-0: PAMS vol 90 iss 1 pp 77–78; PDF read (Wayback copy of ams.org PDF; ams.org itself served a bot challenge) | EXISTS |
| [FLX24] / [8] | Feng, Lai, Xiong, *Erdős similarity problem via bi-Lipschitz embedding*, IMRN 2024(17):12327–12342; arXiv:2312.01319v1 | Crossref 10.1093/imrn/rnae167: IMRN vol 2024 iss 17 pp 12327–12342. arXiv: only "[v1] Sun, 3 Dec 2023" | EXISTS |
| [HL98] / [9] | Humke, Laczkovich, *A visit to the Erdős problem*, PAMS 126(3):819–822, 1998 | Crossref 10.1090/s0002-9939-98-04167-7; PDF header "Volume 126, Number 3, March 1998, Pages 819–822" | EXISTS |
| [IKMC+26] / [10] | Iosevich, Kulkarni, Mora Cuéllar, Rojas Aravena, Yavicoli, *The Erdős similarity conjecture and Rajchman measures*, arXiv:2609.04456v1, 3 Sep 2026 | arXiv abs: identical title and author order; "[v1] Thu, 3 Sep 2026 20:30:33 UTC (25 KB)", only version; "28 pages" | EXISTS |
| [Kol97] / [11] | Kolountzakis, *Infinite patterns that can be avoided by measure*, Bull. LMS 29(4):415–424, 1997 | Crossref 10.1112/s0024609397003056: Bull. LMS vol 29 iss 4 pp 415–424, July 1997. Read the author's posted preprint (fourier.math.uoc.gr/~mk/ps/universal.pdf, header "Bulletin LMS 29 (1997), 4, 415-424", dated June 1996), not the publisher's typeset version | EXISTS |
| [KP25] / [12] | Kolountzakis, Papageorgiou, *Large sets containing no copies of a given infinite sequence*, Anal. PDE 18(1):93–108, 2025; arXiv:2208.02637v2 | Crossref 10.2140/apde.2025.18.93: Anal. PDE vol 18 iss 1 pp 93–108, 2025. arXiv "[v1] Thu, 4 Aug 2022 … [v2] Fri, 6 Oct 2023", comment "To appear in Analysis & PDE" | EXISTS |
| [MCIK+26] / [13] | Mora Cuellar, Iosevich, Kulkarni, Rojas Aravena, Yavicoli, *The Erdős similarity conjecture for two-fold sumsets with a geometric summand*, arXiv:2607.03584v2, 1 Aug 2026 | arXiv abs: same title (title-case), same author order and spelling "Mora Cuellar"; "[v1] Fri, 3 Jul 2026 19:58:28 UTC (20 KB) [v2] Sat, 1 Aug 2026 19:22:26 UTC (20 KB)" | EXISTS (version and date correct) |
| [Sol11] / [14] | David Solymosi, *Patterns in sparse sets*, UBC Summer NSERC USRA report, 2011 ("three-page report" in dyadic) | https://oldwww.math.ubc.ca/Ugrad/NSERC/USRA-PDF/S11_solymosi.pdf — "2011 SUMMER NSERC USRA REPORT / PATTERNS IN SPARSE SETS / DAVID SOLYMOSI", 3 pages, PDF created 2011-09-27 | EXISTS |
| [Tom15] | Foster Tom, *Sets avoiding images of a given sequence*, UBC Summer NSERC USRA report, 2015 | https://oldwww.math.ubc.ca/Ugrad/NSERC/USRA-PDF/S15_Tom.pdf — "Summer 2015 - NSERC USRA Report / Sets Avoiding Images of a Given Sequence / Foster Tom", 2 pages, PDF created 2015-09-01 | EXISTS |

No fabricated arXiv id, version number or date was found. Every version stamp quoted in either paper (1512.05607v1 17 Dec 2015; 2001.02395v2 11 Jan 2020 withdrawn; 2204.12720v1; 2312.01319v1; 2208.02637v2; 2607.03584v2 1 Aug 2026; 2609.04456v1 3 Sep 2026) matches the arXiv version-history block. The single unverifiable item is the problem number "4.33.7*" in [Erd74]/[6].
## Part B — Is each cited RESULT characterised correctly? (citation table)

| # | Cited result | What the paper(s) claim | What the source says (quote) | Verdict |
|---|---|---|---|---|
| B1 | Chlebík [Chl15, Thm 15] (arXiv:1512.05607v1, p. 14–15) | Geo p.2 display: "a bounded infinite set is nonuniversal if it contains finite subsets a1 > ··· > am, of arbitrarily large cardinality, for which −log( min_{i<m}(a_i − a_{i+1}) / (a_1 − a_m) ) = o(m)." Dyadic: "Chlebík gives a translation-invariant formulation normalized by the diameter [2, Theorem 15]." | "Theorem 15. Let X ⊆ R be a bounded infinite set which contains, for arbitrarily small σ > 0, a subset {x1, x2, ..., xn} with x1 > x2 > ··· > xn, n ≥ 3, and min_{i=1,...,n−1} (x_i − x_{i+1})/(x_1 − x_n) ≥ (1 − σ)^n. Then X is non-universal (modulo similarities) w.r.t. the sets with complement of finite Lebesgue measure." The preamble restates it as "lim inf_{n→+∞} −log δ_n(X)/n = 0". | MATCH. The o(m) form is equivalent: min-gap/diameter ≤ 1/(n−1) ≤ 1/2 forces n ≥ log 2/(−log(1−σ)) → ∞ as σ → 0, so "arbitrarily small σ" ⇔ a sequence of subsets with m → ∞ and −log δ/m → 0. (Chlebík's n ≥ 3 is dropped — cosmetic.) |
| B2 | Kolountzakis [Kol97, Thm 3] | Geo: "a probabilistic criterion using large finite subsets with sufficiently large normalized minimum gap." Dyadic: "the minimum gaps, divided by their largest points, must have negative logarithms growing sublinearly in the cardinalities [11, Theorem 3]." | "Theorem 3 Let A ⊆ R be an infinite set which contains, for arbitrarily large n, a subset {a1,...,an} with a1 > ··· > an > 0 and −log δn = o(n), (14) where δn = min_{i=1,...,n−1} (a_i − a_{i+1})/a_1. Then A is not universal." (p. 9, rendered and read) | MATCH |
| B3 | Kolountzakis [Kol97, §3.4] double sums | Geo: "Kolountzakis [Kol97] treated certain double sums, including G1/2 + G1/2." Dyadic: "including D + D [11, Section 3.4]." | "3.4 Sets of the type B + B, with B = {2^{−n^α}} and 0 < α < 2. To prove using Theorem 3 that such a set is not universal …"; "Falconer's criterion (1) does not apply even to the case α = 1. One can prove that the sequence {2^{−n}} + {2^{−n}} does not contain a subsequence x_n ↓ 0 that satisfies (1)." (p. 12, rendered) | MATCH (α = 1) |
| B4 | Kolountzakis [Kol97, §3.2; §2.2, §3.2] methods | Dyadic: random cells + scale discretization at a fixed center + integration over centers occur in [11, Section 3.2]; "Exceptional centers are repaired by an open cover in Kolountzakis [11, Sections 2.2 and 3.2]". | §3.2: "Partition [0,1] into k intervals … put each I_i in E independently … with probability p"; "Fix x ∈ [0,1]. To check whether there exists t ∈ [α,β] … it is sufficient to check whether such a t exists in a finite set S = S(x)"; "E ∫ φ(x) dx ≤ …". §2.2: "Remove then from the set E an open cover of P of measure no larger than λ(E)/2 … (Again, we take here 0 to be an accumulation point of A.)" §3.2: "We then remove from the intersection of the sets a small open cover of all those x's for which some φ(x) = 1 (see discussion in §2.2)." | MATCH |
| B5 | Humke–Laczkovich [HL98, Thms 1–2, Cor 1] | Geo: "developed a finite covering characterization and further criteria in terms of relative gaps." Dyadic: "finite hitting-set characterization and further relative-gap criteria [9, Theorems 1–2]"; Falconer/Eigen "see also the proof in [9, Corollary 1]". | Thm 1: Λ_n = "cardinality of the smallest set B ⊂ N_n that intersects each subset of N_n of the form A_{x,y}"; non-universality ⇔ lim inf Λ_n/n = 0 (for A ⊂ [0,1], inf A = 0, sup A = 1). Thm 2: "Let A be a bounded set such that inf_{u<v} A(u,v)/(v−u) = 0. Then there is a measurable set of positive measure which contains no subset similar to A." Cor 1 "(Eigen [2] and Falconer [7]) … lim a_{n+1}/a_n = 1 … is an immediate corollary of Theorem 2." | MATCH |
| B6 | Falconer [Fal84] | "nonuniversality for positive decreasing sequences a_n → 0 with a_{n+1}/a_n → 1" | "Theorem. Let {x_n} be a decreasing sequence of real numbers convergent to 0 such that (1) lim x_{n+1}/x_n = 1. Then there exists a closed set E with m(E) > 0 such that for any numbers b, c with c ≠ 0, c x_n − b ∉ E for infinitely many n." | MATCH |
| B7 | Eigen [Eig85] | same as B6 | Original not fetched (Akadémiai Kiadó, 2 pp). zbMATH 0627.28004 review: "For any sequence of positive numbers which converges to zero slowly enough there is a set of positive measure which contains no similar sequence". HL98 Cor 1 attributes exactly the ratio → 1 condition to Eigen. | MATCH via secondary sources; original COULD NOT FETCH |
| B8 | Bourgain [Bou87] | "the sum of three infinite sets is nonuniversal" | Original (Springer, paywalled) not fetched. Kol97 §0.3: "His method also gives that any set of reals of the type S1 + S2 + S3, where the S_j are infinite, is not universal." MCIK+26 §1: "Bourgain [1] proved that for any infinite A1, A2, A3 ⊂ R the sumset A1 + A2 + A3 is not measure universal." | MATCH via secondary sources; original COULD NOT FETCH |
| B9 | MCIK+26 Thm 2 (arXiv:2607.03584v2) | Geo: "proved that the sum or difference of a geometric null sequence and any infinite set is nonuniversal. Avoiding such a larger pattern does not imply avoidance of the single geometric progression". Dyadic: "Their Introduction explicitly separates the single dyadic sequence from this two-fold sumset result." | "Theorem 2. Let S ⊂ R contain a lacunary subsequence (b_i)_{i≥1} ⊂ (0,∞) with −log b_i = O(i). Then S + A and S − A are not measure universal for every infinite set A ⊂ R. In particular, {2^{−n}} + A is not measure universal for any infinite A ⊂ R." Introduction: "The prototype is a single geometric sequence (λ^k) with λ ∈ (0,1); even {2^{−n}} is not known to be non-universal." and "this conclusion does not follow by monotonicity from non-universality of the structured summand: it applies to S = {2^{−n}}, whose own non-universality remains open." Abstract: "even though the non-universality of {2^{−n}} itself remains open." Also §2 (v2, l. 306–309): "a version of Theorem 9 with O(n) in place of o(n) would imply that {2^{−n}} is not measure universal." | MATCH (the "explicitly separates" claim is literally true). Theorem number is 2 in both v1 and v2. |
| B10 | IKMC+26 Thm 1.5 (arXiv:2609.04456v1) | Geo: "prove nonuniversality for sets supporting a probability measure whose Fourier transform tends to zero at infinity." | "Theorem 1.5. Let A ⊆ R support a Rajchman measure. For every ε ∈ (0,1) there exists a closed, 1-periodic, nowhere dense set E ⊆ R such that m(E ∩ I) ≥ 1 − ε for every interval I ⊆ R of length 1, and x + sA ⊄ E for every x ∈ R and every s ∈ R \ {0}." Def 1.4: Rajchman = "μ̂(ξ) → 0 as \|ξ\| → ∞". | MATCH |
| B11 | IKMC+26 Prop 4.1 | "Such a measure is atomless, so the hypothesis excludes countable sets" / "A countable set cannot support such a measure [10, Proposition 4.1]" | "Proposition 4.1. Every Rajchman probability measure on R is atomless. Consequently its support is uncountable and has no isolated points." | MATCH |
| B12 | IKMC+26 Prop 3.2 (dyadic only) | "Their more general uniform-density criterion on the circle [10, Proposition 3.2] also fails for D ∪ {0}: for every integer k ≥ 1, dilation by 2^k leaves its image modulo one unchanged, and that image stays a distance 1/4 from 3/4." | "Proposition 3.2 (Multiscale blocking). Let K ⊆ R be a nonempty compact set with the following property: for every δ > 0 there is a finite Λ(δ) ≥ 1 such that τK mod 1 is δ-dense in T for every τ ≥ Λ(δ). Then …" | MATCH. Checked: 2^k(D∪{0}) mod 1 = {0} ∪ {2^{−m} : m ≥ 1} = D∪{0}; nearest points to 3/4 are 1/2 and 1 ≡ 0, both at distance 1/4; so τ K mod 1 is not δ-dense for δ < 1/4 at τ = 2^k → ∞. (Remark 3.3 of IKMC+26 shows a different countable compact set does satisfy the hypothesis — consistent.) |
| B13 | IKMC+26 Lemma 3.1, Prop 3.2 as precedent (dyadic) | "Periodic blocking sets and summable measure budgets also appear in [10, Lemma 3.1 and Proposition 3.2]" | Lemma 3.1 "(Single-scale blocking)" with B(q,η) = {u : ‖qu‖_T < η}; Prop 3.2 proof: "η_k = ε2^{−k−1} … B_k = B(q_k, η_k) … E = R \ ∪ B_k". | MATCH |
| B14 | CLP23 Cor 1.2 + Prop 4.4 (arXiv:2204.12720v1) | Geo: "construct sets of Hausdorff dimension one avoiding certain null sequences together with their limit point; the subsets establishing that dimension have Lebesgue measure zero." Dyadic: "the avoiding sets in their construction have Lebesgue measure zero". | "Corollary 1.2. Let A = {a_k} be a null sequence obeying (1.2). Then there exists a Borel set E of Hausdorff dimension 1 that does not contain any nontrivial affine copy of A ∪ {0}." Remark 1: "We will prove the theorem by exhibiting a subset of E that has Hausdorff dimension 1 but Lebesgue measure zero (see Proposition 4.4)." "Proposition 4.4. Under the assumption of Theorem 2.1, the set O constructed in (2.11) has Lebesgue measure zero." Also: "We do not know if there are more points in E_K other than points in O". Abstract: "we construct a Borel set O ⊆ R of Hausdorff dimension 1, but Lebesgue measure zero, that avoids all nontrivial affine copies of A ∪ {0}." | MATCH (geometric wording is the precise one; dyadic wording agrees with CLP's abstract, i.e. with the exhibited set O, though CLP leave open whether the full Erdős-point set E_K is null — COSMETIC) |
| B15 | FLX24 Thm 1.1 (arXiv:2312.01319v1) | Geo: "implies that every G_q embeds into every measurable set of positive measure by a bi-Lipschitz map." Dyadic: "applies to the dyadic sequence". | "Theorem 1.1. Let (a_n) be a strictly decreasing sequence of positive numbers with a_n → 0 as n → ∞. If there exists an integer N ≥ 1 such that lim sup_{n→∞} a_{n+N}/a_n < 1, then for any measurable set E ⊂ R with positive Lebesgue measure, there exists a bi-Lipschitz map f : R → R such that f(a_n) ∈ E for all n ≥ 1 and f′(0) = 1." Followed by: "This result shows that fast decaying sequences like (2^{−n}) is bi-Lipschitz measure universal." | MATCH (G_q has a_{n+1}/a_n = q < 1, N = 1) |
| B16 | KP25 §3.1 (arXiv:2208.02637v2) | Geo: random cells, fixed-center scale discretization and integration appear in [KP25, Section 3.1]; "the latter paper treats unbounded sequences"; body (p. ~10): "The finite boundary-representative argument has precedents in [Chl15, proof of Theorem 15] and [KP25, Section 3.1]." | §3.1: "keep each I_{i,m} in E independently … with probability p_N"; "E\|B\| = E ∫ 1_B(x) dx = ∫ P[∃t ∈ [a,b] : …] dx"; "Fix x ∈ [−N,N]. To check whether there exists t ∈ [a,b] such that (x + tA) ∩ [−N,N] ⊆ E, it is sufficient to check whether such a t exists in a finite set S = S(x)". Class (A): "a_0 = 0, a_{n+1} − a_n ≥ 1, log a_n = o(n)". Intro: "This is not known if a_n = 2^{−n}, for example." | MATCH |
| B17 | Chlebík [Chl15, §5] and [Chl15, proof of Thm 15] | same precedent claims | §5 proof of Thm 15: "Consider intervals I_j = [jτ,(j+1)τ) … put each I_j in G independently … with probability q"; "it is sufficient to check whether such b exists in a finite set S(a) = {b1 = 1, b2, ..., bN} … \|S(a)\| ≤ 4ny_1/τ = 4n/δ"; "E ∫_A^B φ_G(a) da ≤ 4(1 + C(X)) n (1 − q)^n/δ." | MATCH |
| B18 | Chlebík [Chl15, §3 final remark] and Prop 1(vi),(viii) | Dyadic: "Chlebík also describes adding the centers themselves when the pattern contains zero [2, Section 3, final remark]". Geo body: "see also Chlebík [Chl15, Section 3, final remark; Proposition 1(vi), (viii)]". | Last remark of §3 (p. 11–12): "Using the fact that 0 ∈ X, we can add to H that small set of a's in [0,1] for which {a} × [1,2] is not covered by L_X(H) and conclude non-universality of X this way." Prop 1 (rendered p. 4): "(vi) L_{X̄}(G) = L_X(G) whenever G is open. … (viii) For each A ⊆ R × (R \ {0}) there are open sets G_k ⊆ R … such that L_X(G_k) ⊇ A and λ(G_k) ≤ μ_X(A) + 2^{−k}." | MATCH |
| B19 | Tom [Tom15, Lemma 0.2] (geo body, open-neighbourhood repair) and Tom's construction (§1.1) | Geo body: "Open-neighborhood repair for null sequences is explicit in Tom [Tom15, Lemma 0.2]". §1.1: "Solymosi … and Tom report incomplete dyadic constructions based on random cells; Tom also considers nested dyadic intervals and tests independent of the dilation." | "Lemma 0.2 Suppose ∃E ⊂ R with m(E) > 0 and m(P) = 0 where P = {x : ∃t : x + tA ⊂ E}. Then A is non-universal. Proof: P has an open cover Q with F = E \ Q having positive measure. If for some x, t, x + tA ⊂ F ⊂ E, then by definition x ∈ P ⊂ Q. But Q is open so ∃a ∈ A with x + ta ∈ Q, contradicting x + tA ⊂ F." Construction: "we divide (0,1) into intervals I_{a1} = (2^{−a1}, 2^{−a1+1}), selecting each with probability p1. Then divide each I_{a1} into intervals I_{a1,a2} …"; "Note that to calculate the appropriate expectation, the required subintervals must be independent of the scaling."; ends "Hopefully, one can refine the probability estimate". | MATCH (Tom's lemma silently needs 0 ∈ closure(A), which holds for the null sequences the paper means; "dyadic intervals" here are intervals between consecutive powers of 2, subdivided again — a loose but fair description) |
| B20 | Solymosi [Sol11, §3] | Geo: "report incomplete dyadic constructions based on random cells". Dyadic: "An earlier attempt to extend the random-cell approach to the dyadic sequence is described by Solymosi [14, Section 3]; that report does not claim a completed construction." | §3 "Our work": "We try to improve the argument for the special case of the infinite set A being {2^{−n}} … Below I outline our attempt at constructing a set of positive measure which avoids all affine copies"; random indicator cells X_i with "p → 1 such that p^n → 0"; §3.3 "for larger p which satisfy our conditions, such as p = 1 − 1/√n, the results are inconclusive"; §3.4 "with no major results yet". | MATCH |
| B21 | Steinhaus-type finite universality (§1.1 of both, no citation in geo) | "if F is finite and A is measurable with finite positive measure, continuity of translations in L1 gives m(∩_{a∈F}(A − sa)) → m(A) > 0 (s → 0)." | Standard; checked: m(A \ (A − sa)) ≤ ‖1_A − 1_{A+sa}‖_1 → 0 for each of finitely many a. | VERIFIED |
| B22 | §1.1 obstruction computation (both papers) | Geo: "For distinct powers of q, we have a_{m−1} ≤ q^{m−2}a_1 and a_1 − a_m ≥ (1 − q)a_1. Their normalized minimum gap is therefore at most q^{m−2}/(1 − q)". Dyadic: "the minimum gap is at most a_{n−1} ≤ 2^{−(n−2)}a_1, whereas the diameter a_1 − a_n is at least a_1/2. Either normalized minimum gap is therefore at most 2^{−(n−3)}." | Checked: min gap ≤ a_{m−1} − a_m < a_{m−1} ≤ q^{m−2}a_1; a_m ≤ q a_1 so a_1 − a_m ≥ (1−q)a_1. −log of the ratio ≥ (m−2)log(1/q) + log(1−q), linear in m. Dyadic: 2^{−(n−2)}/(1/2) = 2^{−(n−3)}; normalised by a_1 it is ≤ 2^{−(n−2)} ≤ 2^{−(n−3)}. | VERIFIED |
## Part C — Novelty against the live world (as of 2026-10-14)

Full log with URLs, HTTP statuses and quotes: `/tmp/erdos0300/refs/live/LIVE_FINDINGS.md`.

**Verdict: NO PRIOR PROOF FOUND among the sources searched.** Every source dated before the 6 Oct 2026 release that mentions the case says it is open.
- MCIK+26 v2 abstract (1 Aug 2026): "even though the non-universality of {2^{−n}} itself remains open." Its v1 (3 Jul 2026) says "{2^{−n}} is not known to be non-universal".
- JLM survey, arXiv:2412.11062v2: "determining whether (2^{−n}) is measure universal has been the major bottleneck of the problem". Its Question 7.2 is introduced by "the following special case of the Erdős similarity conjecture is open".
- KP25: "This is not known if a_n = 2^{−n}, for example."
- Chlebík 2015, final remark: "it is (rather surprisingly) still unknown whether the geometric sequence X = {2^{−k}}_{k=0}^∞ is universal or not."
- Shmerkin–Yavicoli (2503.21079v2, Dec 2025): "it is not known whether {2^−n : n ∈ N} is measure universal".
- Li–Wang–Xu (2512.02146): "remains open even for any geometric sequence A={r^n} where 0<r<1".
- FrontierMath Erdős (Adamczewski–Bloom, 2609.25050, 6 Sep 2026) lists Erdős 120 as a benchmark target.

| Source | What it shows | Bears on novelty? |
|---|---|---|
| arXiv search, all:"Erdős similarity" and variants. arxiv.org/search HTML (32 queries) + search.arxiv.org full text (10 queries); the export API returned HTTP 429 from two hosts | The 2025–26 hits are listed in LIVE_FINDINGS §1. None proves the single-sequence {q^n} case before the release. | No prior proof |
| Cruz–Lai–Pramanik, arXiv:2001.02395 | Claimed the full conjecture. Withdrawn 3 days later: "A gap was found in Proposition 3.3 of the paper." | The only earlier claim. Withdrawn. |
| **Gao–Mooroogen–Yip**, arXiv:2311.06727v3 = BLMS 57(6):1801–1818 (2025). Forum comment by Alfaiz, 7 Nov 2025: "An analog question of this problem (which was constructed by Kolountzakis and Papageorgiou) has been solved in affirmative by X. Gao, Y. Mooroogen and C. H. Yip" | Thm 1.5: "Let {a_n} be an increasing sequence of real numbers such that the set A = {⌊a_n⌋} ⊂ Z has positive upper Banach density. Then, for each ǫ ∈ (0,1], there exists a (1 − ǫ)-large set S ⊂ R that does not contain any affine copy of {a_n}." Cor 1.9 covers {2^n} for ǫ ∈ (1/2, 1]. | **NOT this problem.** It handles increasing, unbounded sequences and largeness "in every unit interval". Their own text: "Proving the non-universality of the sequence {2^{−n}} in E has long been an impediment to resolving the Erdős similarity problem", and it is "not clear if progress on either question implies progress on the other." |
| JLM survey, Question 7.2 | "Let b > 1 be a real number. Is there a set of positive measure containing no sequence (x + yb^{−n})_{n=1}^∞ for any x, y ∈ R with y ≠ 0?" Theorem 7.1 (Burgin et al.) handles only x = 0. | This is exactly the case OpenAI claims. It is recorded as open. |
| **Ben Green, 100 open problems.** PDF 200, Last-Modified 30 Jan 2026; footnote "Most recent update: December 2025" | p.44: "Problem 94. Let A ⊂ R be a set of positive measure. Does A contain an affine copy of {1, 1/2, 1/4, . . . }? Comments. This is a special case of the Erdős similarity problem; see [290] for a survey and https://www.erdosproblems.com/120 for further discussion." No "(Solved)" tag and no update note. | Open as of the PDF date, which is before the release |
| **Bloom, "Erdős problems in the OpenAI proofs", 8 Oct 2026** (erdosproblems.com/forum/thread/blog:10). 403 from exe.dev; 200 via Hetzner | Disclaimer: "all of these should be read as 'claims' … This post should not be read as any kind of endorsement". On #120: "This PDF claims a proof of the following special case … If q∈(0,1) and A={q,q^2,q^3,…} then there exists a compact set E⊆[0,1] with measure at least 1/2 such that a·A+b⊄E … This proof has been formalised in the special case when q=1/2." Bloom's paraphrase "at least 1/2" is weaker than the paper's 1−η. | Listing only, no endorsement. The /120 page is unchanged: "last edited 23 January 2026", "Proof claims (0)". Forum: "The ability to post proof claims and comment on individual problems has been paused." |
| **formal-conjectures**, `GreensOpenProblems/94.lean` | `@[category research solved, AMS 28, formal_proof using lean4 at "https://github.com/openai/math/blob/adc7f124…/lean/OAI/MeasureTheory/DyadicAvoidance/Main.lean#L103"] theorem green_94 : answer(False) ↔ ∀ A : Set ℝ, MeasurableSet A ∧ volume A > 0 → ∃ a b : ℝ, a ≠ 0 ∧ ∀ n : ℕ, a * (1 / 2^n) + b ∈ A`. Flipped to solved by PR #6898 (merged 2026-10-11, Firsching). The PR records that `#print axioms` and Comparator were **not** run. | Third party marks Green 94 solved, citing OpenAI. It is not an independent check. |
| formal-conjectures, `ErdosProblems/120.lean` | `@[category research open, AMS 5 28] theorem erdos_120 : answer(sorry) ↔ ∀ A : Set ℝ, A.Infinite → Erdos120For A`. No commit after 2026-09-25 and no geometric or dyadic variant. A 2026-10-08 comment on PR #6898 ("should Erdos problem 120 in this repo also be updated?") got no reply. | Still open (correctly, since the full conjecture is open) |
| The 14 Mar 2026 non-measurable variant (erdosproblems.com/120 thread) | Firsching: the DeepMind prover found that dropping MeasurableSet allows "the ℤ-span of a Hamel basis [which] entirely avoids affine copies of the sequence {1, 1/2, 1/4, …} … strictly positive outer measure, but it is not a measurable set." Sothanaphan: "De Reyna (1983) proved this positive outer measure variant … only requiring that \|A\| ≥ 3". This became `green_94_outer_measure` (PR #3526). | Irrelevant to the measurable case. It confirms FC's `green_94` now requires MeasurableSet. |
| Third-party Lean | (i) haraldschilly/math-distance-set-similarity (2026-10-07) re-builds OpenAI's DyadicAvoidance ("yes, by OpenAI; re-checked here") and marks the geometric statement "no". (ii) mxym/math `formalizations/geometric-avoidance` (2026-10-07) claims a kernel-replayed Lean proof of a stronger uniform all-ratio statement, AI-assisted and building on OpenAI. Not replayed by us. (iii) ProveIt priority audit names OpenAI as the antecedent. | All downstream of the release, none prior |
| **Jiang–Xi, arXiv:2610.11449v1 (8 Oct 2026)** | Thm 1.1: a_n > 0, a_n → 0, liminf a_{n+1}/a_n > 0 ⇒ for every η there is a compact E ⊂ [0,1], m(E) > 1 − η, with no nontrivial affine copy. Text: "Our proof uses the finite-tree construction of the unpublished manuscripts [17, 18] … the geometric case and the tree construction are due to [17, 18]", where [17] and [18] are the two OpenAI manuscripts. They add (l. 465): "The proof does not give the same conclusion for every sequence with lim inf a_{n+1}/a_n = 0." | **Downstream generalisation crediting OpenAI**, not prior art. Relevant to referee item (ix): the method extends exactly as far as two-sided ratio bounds on a subsequence and no further, so it does not prove the full conjecture. That is consistent with the papers' own account of where q is used. |
| Reactions: MathOverflow API, HN Algolia, Tao's blog and Mathstodon, Kalai's blog | Seventeen MO questions about the OpenAI release (7–13 Oct). None mentions similarity, #120, dyadic or Green 94. | No error report or prior-proof claim found |

**COULD NOT CHECK (Part C):**
- **Humke, "The Erdős Similarity Problem", Notices AMS 73(7):549–551, Aug 2026, doi 10.1090/noti3375.** AMS returned 403 from every route and there is no Wayback copy. It is a 3-page piece published before the release. It is almost certainly expository, but it is unread.
- The arXiv export API (HTTP 429). arXiv's own search was used instead, and full-text index coverage is partial.
- The Wiley PDF of GMY (arXiv v3 read instead) and the Springer correction to JLM24.
- Reddit (403) and X (no search access).

## Part D — OpenAI's Lean scope doc and comparator statement

- Scope doc `/tmp/oaimath/084/lean_doc.md`:
  - Heading: "The geometric case of the Erdős similarity conjecture".
  - Links only: "The dyadic case of the Erdős similarity conjecture".
  - Scope: "The formalization proves the dyadic case … For every 0<η<1, it constructs a compact set E⊂[0,1] of measure greater than 1−η that contains no affine copy of {2^{−n}:n≥1} … Both signs of s are included."
  - Comparator table: one row, `DyadicAvoidance.lean`.
- Comparator `/tmp/oaimath/159/world/oai_sparse/repo/lean/ComparatorChallenges/DyadicAvoidance.lean`:
  ```
  def dyadicPoint (n : ℕ) : ℝ := (2 : ℝ)⁻¹ ^ n
  theorem dyadic_affine_avoidance :
      ∀ η : ℝ, 0 < η → η < 1 → ∃ E : Set ℝ,
        E ⊆ Set.Icc (0 : ℝ) 1 ∧ IsCompact E ∧
        MeasureTheory.volume E > ENNReal.ofReal (1 - η) ∧
        ∀ x s : ℝ, s ≠ 0 → ∃ n : ℕ, 1 ≤ n ∧ x + s * dyadicPoint n ∉ E
  ```
  The JSON sidecar: `theorem_names: ["OAI.Problem310.dyadic_affine_avoidance"]`, `permitted_axioms: ["propext","Quot.sound","Classical.choice"]`.

**Which theorem this is.** It is **DYADIC Theorem 1.1 verbatim**, which is also GEOMETRIC Theorem 1.1 at q = 1/2:
- q = 1/2 only;
- both signs of s, since only s ≠ 0 is required;
- every real x;
- E compact with E ⊆ [0,1];
- m(E) > 1 − η, strict, where 1 − η > 0 because η < 1, so the set is non-empty and non-null;
- the hitting index ranges over n ≥ 1.

**There is no Lean statement or proof of GEOMETRIC Theorem 1.1 for q ≠ 1/2** (objection S2).

**Equivalence with erdosproblems.com/120's special case.** The page's A is {1, 1/2, 1/4, …} = {2^{−k} : k ≥ 0}, and its statement is "Must there be a set E ⊂ ℝ of positive measure which does not contain any set of the shape aA+b … a≠0?". Writing D = {2^{−n} : n ≥ 1}, we have aA + b = (2a)·D + b. The map a ↦ 2a is a bijection of ℝ∖{0}, so "E contains no aA + b (a ≠ 0)" ⇔ "E contains no x + sD (s ≠ 0)".
- **Including or omitting the point 1 makes no difference.**
- Even without rescaling, the implication needed runs the easy way: x + s{1, 1/2, …} ⊇ x + sD, so avoiding every copy of D avoids every copy of the larger set.
- The same reasoning covers FC's `green_94`, which quantifies `∀ n : ℕ` (n = 0 included) and asks about `a * (1/2^n) + b`. The comparator statement implies `green_94` with answer False.

**Conclusion of Part D.** The comparator statement is a faithful formalization of the special case named on erdosproblems.com/120 and in Green's Problem 94, in the measurable form; compact E is automatically measurable. I did not replay the 75-file proof. PR #6898 states that formal-conjectures did not run `#print axioms` or Comparator on it. A third party (Schilly) reports a re-check.

## Verdict for my scope

**HOLDS AS READ.**
- Every one of the 14 entries in GEOMETRIC's reference list, and the extra DYADIC entry [3], **EXISTS**. Every arXiv id, version number and date matches the arXiv version history. No fabricated version or date was found.
- Every cited *result* is characterised correctly (Part B: 22 rows, all MATCH or VERIFIED). Two match only via secondary sources (Bourgain, Eigen: originals not fetched).
- The cosmetic defects are:
  - the unverifiable sub-locator "Problem 4.33.7*" (S1);
  - packaging that hangs a dyadic-only Lean proof on the geometric headline (S2);
  - a slightly loose CLP description in DYADIC (S3);
  - missing related work, notably JLM24 Question 7.2, which is the exact question answered (S4).
- **Novelty:** no proof of the dyadic or geometric single-sequence case exists anywhere I could reach before OpenAI's 25 Sep / 5 Oct manuscripts. The pre-release literature, up to 1 Aug and 6 Sep 2026, calls it open. All later work (Jiang–Xi, mxym, Schilly, FC #6898) is downstream and credits OpenAI.

**COULD NOT CHECK:**
- the Bourgain 1987 and Eigen 1985 originals (paywall / no copy);
- the numbering "Problem 4.33.7*" (no source);
- Humke, Notices AMS Aug 2026 (403, unarchived);
- the arXiv export API (429);
- X and Reddit;
- the 75-file Lean proof itself (not replayed; out of scope).
