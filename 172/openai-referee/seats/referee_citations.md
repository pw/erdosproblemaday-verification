# Referee report — tag `citations`
Scope: (A) the reference list [1]–[37] and §1.1 "History and significance" (PDF pp. 3, 68–70); (B) novelty and reception of Theorem 1.1 in the live world. I did not referee the proof.
Fetched 2026-10-11. Primary sources sit under /tmp/oaimath/refs/ (arXiv abs pages: refs/abs/; PDFs: refs/pdf_<id>/; Hindman material: refs/hindman/; erdosproblems pages: refs/ep/; openai/math: refs/openai_math/; third-party Lean repo: refs/cadamcat/).

Headline: **no bibliographic detail is fabricated.** All 11 arXiv version numbers and dates match the arXiv record exactly, and every DOI'd venue, volume, issue and page range matches Crossref or zbMATH. I found three small defects: one wrong attribution in §1.1, one wrong month and one DOI that does not resolve (the journal's fault). For (B), the big item: **a third-party Lean 4 formalization of the core conjecture appeared on 7 Oct 2026, following this paper, and it reports two independent kernel checks.** It swaps two of the paper's cited §5 inputs for different theorems (details in B5).

---
## (1) Bibliography table

Method. arXiv entries: I curled `https://arxiv.org/abs/<id>` and parsed the submission-history block. DOI entries: Crossref API (`api.crossref.org/works/<doi>`). Non-DOI entries: zbMATH API, journal pages, or the hosting URL itself.

| # | Cited as | Record found | Verdict |
|---|---|---|---|
| 1 | Alweiss, *Monochromatic sums and products over Q*, arXiv:2307.08901v6, 12 July 2026, accepted Duke | Versions: v1 18 Jul 2023 · v2 7 Aug 2023 · v3 10 Aug 2023 · v4 31 Aug 2023 · v5 17 Nov 2023 · **v6 Sun 12 Jul 2026 03:14 UTC**. Comment: "v6, accepted in Duke Math Journal". (The PDF's own date line reads "July 14, 2026"; the arXiv stamp says 12 Jul 2026.) | EXISTS-AS-CITED |
| 2 | Alweiss, *Monochromatic sums and products of polynomials*, Discrete Anal. 2024, Paper No. 5, 7 pp., doi 10.19086/da.117575 | The DA article page and the PDF footer both print DOI 10.19086/da.117575, "2024:5, 7 pp.", published 27 Aug 2024; it is arXiv:2211.00766v4. **However, doi.org does not resolve that DOI**: HTTP 404, and the handle API returns `responseCode 100` (handle not found). The journal never registered it. | EXISTS-AS-CITED (dead DOI link; journal-side, not a fabrication) |
| 3 | Alweiss–Bowen–Sabok, *Sums, products, and exponents in two-colorings of the naturals*, arXiv:2512.09598v1, 10 Dec 2025 | Only version: v1, Wed 10 Dec 2025. Title and authors match. | EXISTS-AS-CITED |
| 4 | Bergelson–Leibman, *Set-polynomials and polynomial extension of the Hales–Jewett theorem*, Ann. Math. 150 (1999) 33–75, URL annals…/1999/150-1/p02 | The Annals page at that URL reads "Pages 33-75 from Volume 150 (1999), Issue 1". | EXISTS-AS-CITED |
| 5 | Bergelson–Leibman, Adv. Math. 175 (2003) no. 2, 271–296 | Crossref matches. | EXISTS-AS-CITED |
| 6 | Bergelson–Moreira, ETDS 38 (2018) no. 2, 473–498 | Crossref matches. | EXISTS-AS-CITED |
| 7 | Bergelson–Moreira, ETDS 37 (2017) no. 3, 673–692 | Crossref matches. | EXISTS-AS-CITED |
| 8 | Bowen, *Monochromatic products and sums in 2-colorings of N*, Adv. Math. 462 (2025) 110095 | Crossref matches (Feb 2025). | EXISTS-AS-CITED |
| 9 | Bowen–Sabok, *Monochromatic products and sums in the rationals*, Forum Math. Pi 12 (2024) e17 | Crossref matches. | EXISTS-AS-CITED |
| 10 | Gowers, BLMS 42 (2010) no. 4, 573–606 | Crossref matches. | EXISTS-AS-CITED |
| 11 | Green–Sanders, *Monochromatic sums and products*, Discrete Anal. 2016:5, 48 pp. | The DA PDF header reads "DISCRETE ANALYSIS, 2016:5, 48 pp." (the arXiv journal-ref says 43 pp; the journal's own header governs). | EXISTS-AS-CITED |
| 12 | Green–Tao, Ann. Math. 175 (2012) no. 2, 465–540 | Crossref matches. | EXISTS-AS-CITED |
| 13 | Green–Tao erratum, Ann. Math. 179 (2014) no. 3, 1175–1183; further revision arXiv:1311.6170v3, 14 Aug 2015 | Crossref matches. arXiv versions: v1 24 Nov 2013 · v2 3 Feb 2014 · **v3 Fri 14 Aug 2015**. v3 comment: "further updated in August 2015 after a further small error came to light (we cannot have one of the N_i being extremely small)". | EXISTS-AS-CITED |
| 14 | Green–Tao, *Linear equations in primes*, Ann. Math. 171 (2010) no. 3, 1753–1850 | Crossref matches. | EXISTS-AS-CITED |
| 15 | Green–Tao, Ann. Math. 167 (2008) no. 2, 481–547 | Crossref matches. | EXISTS-AS-CITED |
| 16 | Green–Tao, *An arithmetic regularity lemma, an associated counting lemma, and applications*, An Irregular Mind (Bolyai Soc. Math. Stud.), 261–334; corrected arXiv:1002.2028v3, 24 Nov 2020 | Crossref (10.1007/978-3-642-14444-8_7) gives pp. 261–334. arXiv versions: v1 10 Feb 2010 · v2 20 Jun 2010 · **v3 Tue 24 Nov 2020**. Comment: "corrected version of article which appeared in An Irregular Mind". | EXISTS-AS-CITED |
| 17 | Green–Tao–Ziegler, Ann. Math. 176 (2012) no. 2, 1231–1372; further revision arXiv:1009.3998v5, 23 Apr 2026 | Crossref matches. arXiv versions: v1 21 Sep 2010 · v2 22 Sep 2010 · v3 27 Mar 2011 · v4 22 Apr 2024 (386 KB) · **v5 Thu 23 Apr 2026 (114 KB)**. v5 comment: "corrects a mistake in the proof of Lemma 13.2 (the wrong filtration was specified) and two small typos on page 28". | EXISTS-AS-CITED |
| 18 | GTZ erratum, "author-hosted erratum, April 2024, 6 pp.", people.maths.ox.ac.uk/greenbj/papers/GI(s)-erratum.pdf | The URL serves HTTP 200, a 6-page PDF titled "Erratum for 'An inverse theorem for the Gowers U^{s+1}[N]-norm'". **Its date is February, not April:** the PDF CreationDate/ModDate are 25 Feb 2024 15:55 UTC, the server's Last-Modified header is 25 Feb 2024, and the text itself carries no date. Green's preprints page says only "An erratum for this paper was issued in 2024." "April 2024" most likely comes from arXiv v4 (22 Apr 2024). | EXISTS-BUT-DETAILS-WRONG (month: Feb 2024, not April). Cosmetic. |
| 19 | Hindman, JCTA 17 (1974) no. 1, 1–11 | Crossref matches. | EXISTS-AS-CITED |
| 20 | Hindman, *Partitions and sums and products of integers*, TAMS 247 (1979) 227–245 | Crossref matches. The AMS abstract (read through a browser) ends: "…and some related finite questions are investigated." | EXISTS-AS-CITED |
| 21 | Hindman, *Partitions and sums and products—Two counterexamples*, JCTA 29 (1980) no. 1, 113–120 | Crossref, zbMATH 0443.05010 and Elsevier metadata all match the title, volume, issue and pages. **The content it is cited for in §1.1 does not match; see the table in (2).** | EXISTS-AS-CITED (bibliographically) |
| 22 | Hindman–Phulara, *Some new additive and multiplicative Ramsey numbers*, J. Combin. 4 (2013) no. 1, 81–93 | zbMATH 1301.05352: "J. Comb. 4, No. 1, 81-93 (2013)", DOI 10.4310/JOC.2013.v4.n1.a4. Hindman's own reprint (nhindman.us/research/plustimesnumberspost.pdf) agrees. | EXISTS-AS-CITED |
| 23 | Hindman–Strauss, *Algebra in the Stone–Čech compactification*, 2nd rev. ext. ed., De Gruyter Textbook, 2012 | Crossref 10.1515/9783110258356 (online 21 Dec 2011, print 2012). | EXISTS-AS-CITED |
| 24 | Host–Kra, Ann. Math. 161 (2005) no. 1, 397–488 | Crossref matches. | EXISTS-AS-CITED |
| 25 | Leibman, GAFA 4 (1994) no. 6, 648–659, URL people.math.osu.edu/leibman.1/papers/tmr.pdf | Crossref 10.1007/bf01896657 gives 4(6) 648–659 (Nov 1994). The URL serves the paper (HTTP 200; page 1 reads "Vol. 4, No. 6 (1994)"). | EXISTS-AS-CITED |
| 26 | Leibman, ETDS 25 (2005) no. 1, 201–213 | Crossref matches. | EXISTS-AS-CITED |
| 27 | Moreira, Ann. Math. 185 (2017) no. 3, 1069–1090 | Crossref matches. | EXISTS-AS-CITED |
| 28 | Reingold–Trevisan–Tulsiani–Vadhan, arXiv:0806.0381v1, 2 Jun 2008 | Only version: v1, Mon 2 Jun 2008. Title matches. | EXISTS-AS-CITED |
| 29 | Richter, *Sums and products in sets of positive density*, arXiv:2507.00515v2, 7 Feb 2026 | Versions: v1 1 Jul 2025 · **v2 Sat 7 Feb 2026**. (Richter–Tsinas 2026 list it as "To appear in Algebra Number Theory".) | EXISTS-AS-CITED |
| 30 | J. H. Sanders, *A Generalization of Schur's Theorem*, excerpt from 1968 Yale PhD thesis; arXiv:1712.03620v1 (2017) | Only version: v1, Mon 11 Dec 2017. The abstract reads: "This paper is an excerpt from the author's 1968 PhD dissertation [Yale University, 1968]…" | EXISTS-AS-CITED |
| 31 | Schur, Jahresber. DMV 25 (1916) 114–117 | zbMATH JFM 46.0193.02: "Deutsche Math. Ver. 25, 114-117 (1916)". | EXISTS-AS-CITED |
| 32 | Selberg, Canad. J. Math. 2 (1950) 66–78 | Crossref matches. | EXISTS-AS-CITED |
| 33 | Szemerédi, *On sets of integers containing no k elements…*, Acta Arith. 27 (1975) 199–245 | Crossref matches; Crossref's metadata title drops the word "no", but the paper's title is correct. | EXISTS-AS-CITED |
| 34 | Tao–Ziegler, Discrete Anal. 2016:13, 61 pp.; revised arXiv:1603.07815v4, 17 Jan 2017 | The v4 PDF header reads "DISCRETE ANALYSIS, 2016:13, 61 pp." arXiv versions: v1 25 Mar 2016 · v2 1 Jul 2016 · v3 15 Jan 2017 · **v4 Tue 17 Jan 2017**. | EXISTS-AS-CITED |
| 35 | van der Waerden, Nieuw Arch. Wiskd. (2) 15 (1927) 212–216 | zbMATH JFM 53.0073.12: "Nieuw Archief (2) 15, 212-216 (1927)". | EXISTS-AS-CITED |
| 36 | Yamada, *Explicit improvements of the Brun–Titchmarsh theorem for arbitrary intervals*, arXiv:2312.16090v1, 26 Dec 2023 | Only version: v1, Tue 26 Dec 2023. | EXISTS-AS-CITED |
| 37 | Zorin-Kranich, J. Anal. Math. 123 (2014) 183–225; revised arXiv:1206.0287v4, 4 Jun 2018 | Crossref matches. arXiv versions: v1 1 Jun 2012 · v2 20 Aug 2012 · v3 14 Oct 2013 · **v4 Mon 4 Jun 2018** ("v4: switch to TeXlive 2016 and biblatex"). | EXISTS-AS-CITED |

Result: 37/37 entries exist. 35 are exact. [18] has the wrong month. [2] carries the DOI the journal prints, but that DOI is not registered. I found no invented version number, date, venue or page range.

Pointers for the proof referees, from the version blocks (not judged by me): GTZ v5 (Apr 2026) fixes "the wrong filtration" in the proof of Lemma 13.2. The 2024 erratum withdraws Proposition 8.3 "as stated" and notes that the equidistribution results of [12] cited in Appendix D are stated with G_0 = G_1. Green–Tao 1311.6170v3 adds the condition that no N_i can be extremely small. The §5.3 and §6.1 referees should check that the forms they quote come from these corrected versions.

---
## (2) Theorem-citation table for §1.1

| §1.1 claim | Source text (quoted) | Verdict |
|---|---|---|
| Schur gives monochromatic {x,y,x+y} [31] | Standard; Alweiss v6 §1 restates it the same way. | MATCH (not re-read in German) |
| Sanders's argument in "[30, Theorem 2 and Corollary 1.1]" | arXiv 1712.03620v1: "Theorem 2. Let P(t,n) be the statement, 'Given numbers t, n there exists a number J(t,n) such that if the set S = {1,…,J(t,n)} is divided into t classes … there exists a sequence of (not necessarily distinct) numbers a1,…,an and a number ℓ … such that Σ_{i∈I} a_i ∈ A_ℓ for all I…' Then P(t,n) is true…" and "Corollary 1.1. The a_i may be assumed distinct in the above theorem." | MATCH |
| Hindman proved the infinite finite sums theorem [19] | JCTA 17 (1974), *Finite sums from sequences within cells of a partition of N*. | MATCH |
| "Hindman constructed a finite coloring of N with no infinite set whose terms, pairwise sums and pairwise products all have one color [21]" | **Hindman himself puts this result in the 1984 paper, not the 1980 paper [21].** Hindman–Phulara 2013 (Hindman's own final version, p. 1): "it was shown in [3] that there is a 7-coloring of N such that there is no sequence ⟨x_n⟩ with PS(⟨x_n⟩) ∪ PP(⟨x_n⟩) monochromatic", where [3] = "N. Hindman, Partitions and pairwise sums and products, J. Comb. Theory (Series A) 37 (1984), 46-60". Hindman–Ivan–Leader 2022 (arXiv 2210.07831v3) say the same and also cite the 1984 paper as their [4]. Semantic Scholar's machine summaries of the publisher abstracts agree. For 1984: "A seven cell partition of N is constructed with the property that no infinite set has all of its pairwise sums and products in any one cell." For **1980 [21]**: "…a two celled partition of N with the property that neither cell includes an infinite set together with all finite products and pairwise sums from that set." Bergelson–Hindman–Leader 1999 credit the 1980 paper with ruling out a sequence "with all of its sums and products". The 1980 result (A ∪ FP(A) ∪ PS(A), 2 colours) does not imply the claimed statement (A ∪ PS(A) ∪ PP(A)); the 1984 result does. **I could not read the 1980 PDF**: ScienceDirect showed a captcha from both the datacenter IP and the home-IP browser, and I stopped as policy requires. The evidence above is secondary but consistent, and part of it is Hindman's own. The same mis-attribution appears on erdosproblems.com/172 ("Hindman [Hi80] has proved this is false (with 7 colours)…") and in Griffin's arXiv:2605.24751 (which also merges the two titles), so the paper probably inherited it. | **MISMATCH**: right fact, wrong paper; should cite Hindman, JCTA 37 (1984) 46–60. Cosmetic. |
| "His finite conjecture asks for arbitrarily large finite sets instead [20]" | AMS abstract of [20]: "…some related finite questions are investigated." Alweiss v6 quotes [16]=[20]: Hindman "asked about 'the natural finite version of the main sums and products problem'". Richter v2: "Hindman also formulated an extension … in [Hin79]". | MATCH (via the abstract plus two independent quotations; I could not get the TAMS PDF, which returns 403 / a challenge from the datacenter) |
| "[23, Question 17.18]" | Not fetched (Google Books quota exhausted). Alweiss v6 ("Question 17.18 of [21]", the same 2012 edition) and Richter v2 ("[HS12, Question 17.18]") both cite the same question number for the same conjecture. | MATCH (secondary, two independent sources) |
| "computer-assisted arguments of Graham and Hindman already established … {x, y, x+y, xy} in every two-coloring of N; see the historical account in [22, p. 82]" | Hindman–Phulara (p. 2 of the 81–93 article, i.e. p. 82): "The only case (with r > 1) with a proof is r = k = 2. And this is a computer generated result. R. Graham sometime in the mid 1970's used a computer program to verify that if {1, 2, …, 252} is 2-colored, then there exist x ≠ y such that {x, y, x+y, xy} is monochromatic, and that the corresponding statement fails for {1, 2, …, 251}. He noted that the fact that x = 1 is allowed is crucial…" Also: "In [1] [TAMS 1979] the fact that FSP2(1,2) = 252 was verified and it was established that FSP2(2,2) = 990." | MATCH. Your recollection was right: these are statements about initial segments, and they pass to all 2-colourings of N by restriction. One nuance: in Graham's 252 case x = 1 is allowed, and then xy = y, so the "quartet" is really the triple {1, y, y+1}. Hindman's 990 case (2 ≤ x < y) gives genuine quartets. |
| Bowen [8, Thm 1.1]: x, y distinct and beyond any bound; controls individual variables, prefix products and total sum | arXiv 2205.12921v1: "Theorem 1.1. Given any 2-coloring of N and n ∈ N there are arbitrarily large and distinct x1,…,xn ∈ N such that {x_i, ∏_{j≤i} x_j, Σ_{j=1}^n x_j : i ≤ n} is monochromatic." | MATCH (arXiv v1; numbering in the published Adv. Math. version not checked because Elsevier blocks access) |
| Moreira [27, Thm 1.4 and Cor 1.5]: {x, x+y, xy} as part of a theorem on prefix products and polynomial shifts | arXiv 1605.01469v1: Thm 1.4 gives a monochromatic "{x0···xs} ∪ {x0···xj + f(x_{j+1},…,x_i) : 0 ≤ j < i ≤ s, f ∈ F_{i−j}}", with polynomial f of zero constant term. "Corollary 1.5. For any finite coloring of N there exist (infinitely many) x, y ∈ N such that {x, xy, x+y} is monochromatic." Richter v2 cites "[Mor17, Theorem 1.4]" for the Annals version, so the numbering carries over. | MATCH |
| Alweiss [2, Thm 1.2]: a polynomial proof of the mixed triple and polynomial-shift patterns | "Theorem 1.2. For any set of good polynomials P1,…,Pk, the pattern {x, x+P1(y),…,x+Pk(y), xy} is partition regular over T with primitive recursive bounds, and is thus also partition regular over N…" Here T is the semiring of polynomials with non-negative integer coefficients and zero constant term. | MATCH |
| ABS [3, Thm 1.2]: {x, y, xy, x+iy : 1≤i≤k} in two-colourings | "Theorem 1.2. For any k ∈ N and 2-coloring of N, there exist x, y ∈ N such that {x, y, xy, x+iy : i ≤ k} is monochromatic." | MATCH |
| Green–Sanders [11, Thm 1.2]: the four-term result in large prime fields | "Theorem 1.2. Suppose that F_p is r-coloured. Then there are at least c_r p² monochromatic quadruples (x, y, x+y, xy), where c_r > 0 does not depend on p." | MATCH |
| Bergelson–Moreira [7, 6]: affine ergodic methods | Titles and venues verified; theorems not read. | MATCH (titles only) |
| Bowen–Sabok [9, Thm 1.1]: {x,y,x+y,xy} over Q | arXiv 2210.12290v1: "Theorem 1.1. For any coloring of the rationals into finitely many colors there exists a monochromatic set of the form {x, y, xy, x+y} for some nonzero x, y." | MATCH (arXiv v1) |
| Alweiss [1, Thm 1.3]: "the full finite sums and products theorem over Q" | v6 (and v5): "Theorem 1.3. For any n ≥ 2, if Q is colored in finitely many colors, we can find some x1,…,xn ≠ 0 such that all the numbers Σ_{i∈S} x_i and ∏_{i∈S} x_i, for nonempty S ⊂ [n] are the same color." Distinctness is not part of the theorem statement, which concerns an n-tuple. The text adds that the proof "can easily be modified" to give a ≫ b ≫ c. | MATCH (§1.1 makes no distinctness claim) |
| "[1, Section 5]": the Ramsey and finite-sums argument | v6 §5 "Proof of main result". Step II: "By Ramsey's theorem, we can pass to a subset of the x_i so that the color of x_{i1}···x_{ik} depends only on k". Step III: "Applying Folkman's theorem to this coloring…". **The numbering depends on the version:** in v1, §4 is the proof of the main result and §3 the main lemma. The paper cites v6, where its numbering is correct. | MATCH (for v6) |
| "[1, Section 4]": compensating scale updates | v6 §4 "Statement and proof of the main lemma": "A shift is an update of the form x_i ← x_i + q(x_{i−1},…,x_1) and a scaling is one of the form x_i ← kx_i", ending in Proposition 4.1. | MATCH (as a description) |
| Richter [29, Thms 1.5 and 1.7]: density theorems for {x+Q(y), xy} via Fourier analysis, ergodic theory and logarithmic averages | "Theorem 1.5. Let Q be a polynomial with integer coefficients satisfying Q(1) = 0. Then any A ⊆ N with δ(A) > 0 contains {x + Q(y), xy} for some x, y ∈ N\{1}." "Theorem 1.7. … Q(0) = 0. Then any A ⊆ N with d(A) > 0 contains {x + Q(y), xy}…" The abstract reads: "tools from Fourier analysis and ergodic theory". | MATCH |

---
## (3) Novelty and reception (B)

**B1. No earlier or independent proof found.**
- arXiv API full-text and title searches, 2023-06 to 2026-10, sorted by date: `abs:Hindman AND abs:conjecture`, `abs:"Hindman's conjecture"`, `ti:Hindman`, `abs:"finite sums and products"`, `abs:"sums and products" AND abs:monochromatic`, `abs:"x + y, xy"`, `ti:"Monochromatic finite sums and products"`, `au:OpenAI`, `abs:OpenAI AND abs:Hindman`. None of these contains a proof of the finite conjecture over N. The OpenAI preprint is **not on arXiv**.
- The literature describes even the n = 2 case for general colourings as open:
  - Green–Sawhney, arXiv:2511.09365 (Nov 2025)
  - Alweiss–Bowen–Sabok v1 (Dec 2025): "Hindman's conjecture has remained recalcitrant for decades"
  - Richter v2 (Feb 2026): "Despite this progress, Theorem 1.1 remains open"
- **FrontierMath Erdős** (Adamczewski–Bloom, arXiv:2609.25050, 6 Sep 2026) lists Erdos172 among "68 Erdős problems that are open as of August 2026".
- **Richter–Tsinas**, arXiv:2609.30410: v1 posted 24 Sep 2026, the day after the preprint date. v2 is dated "October 8, 2026" on the PDF and was posted on arXiv 7 Oct 2026, the day after the public release. Both versions still say of {x,y,x+y,xy}: "This remains a central open problem in arithmetic Ramsey theory." The OpenAI release is not mentioned. Their AI-disclosure section says they used GPT-6 Astra to find a gap in v1.
- Bloom's 8 Oct post records plagiarism and prior-posting accusations for some problems in the release. None of the named instances is #172; the comment thread names #184 (Coffey, Kim arXiv:2610.07840).

**B2. erdosproblems.com/172** (live page and /latex/172, read 2026-10-11 through a browser).
- The text is unchanged. It still says "Hindman [Hi80] has proved this is false (with 7 colours) if we ask for an infinite A … Alweiss [Al23] has proved [the Q case]".
- No mention of OpenAI. "Proof claims (0)", "Comments (0)", and the forum thread shows "The ability to post new comments has been suspended."
- The site no longer displays statuses. In the **teorth/erdosproblems** database (data/problems.yaml at main, pushed 2026-10-11T00:28Z), #172 shows `status: open, last_update 2025-08-31`, `formal_status: unformalized`.
- That is a blanket non-update, not a verdict on #172: #3, #138, #148, #184, #371 and #416, all claimed by OpenAI and several Lean-formalized by OpenAI, are also still "open". Every commit since 6 Oct is an automated formal-conjectures sync.
- Google DeepMind Formal Conjectures, `ErdosProblems/172.lean`: still `@[category research open]`, last substantive change 2025-11-25.

**B3. Thomas Bloom, "Erdős problems in the OpenAI proofs", 8 Oct 2026** (https://www.erdosproblems.com/forum/thread/blog:10, read through a browser). Verbatim on #172:
> "Problem [172] - Hindman's conjecture. This PDF claims a proof of the following. For any finite colouring of the positive integers and any k ≥ 1 there is a set with k integers such that all non-empty subset sums and products have the same colour. This was a conjecture of Hindman. It was proved for ℚ by Alweiss [Al23]. This proof has not been formalised. The PDF is 70 pages long."

General disclaimers in the same post:
- "I have not yet looked at in any serious way any of the proofs in this release, so all of these should be read as 'claims'…"
- "These papers are, at a glance, very poorly written … I expect that the vast majority of them are (a) correct yet (b) capable of being substantially simplified".

He lists #172 among the "12 problems on the FrontierMath Erdős list" claimed as solved. No comment on that thread (comments run to 10 Oct, then suspended) discusses #172.

**B4. github.com/openai/math.**
- The repo was created 2026-10-06; the family 164 directory has a single commit (`adc7f124`, "Initial commit", 2026-10-06T21:58Z).
- Our /tmp/oaimath/164/paper.pdf is **byte-identical** to the repo blob (git hash 93d9a678…).
- Family 164 was **not** touched by the 7 Oct withdrawals and fixes (history.md lists 3 withdrawals and 14 revisions, none in this family).
- **Issues are disabled** (`has_issues:false`), discussions too, and there is exactly one PR (OpenAI's own update, closed). So no issue about family 164 exists or can be filed. MathOverflow Q515845 (8 Oct) asks how to contact the authors with corrections.
- CONTENTS.md entry 164 has no "(Lean)" link. Family 164 is absent from lean/formalization.yaml and lean/docs/.
- **However,** the Lean library does contain `lean/OAI/Combinatorics/SumProduct/Alignment/` (259 files), which ends in `OAI.SourceRawMenu.Alignment` / `SourceMenuLiteral.charted_finite_menu_alignment`. So OpenAI formalized the Alignment half (§6–8) without advertising it.

**B5. Third-party Lean formalization — the most important reception fact.**
- Repo: github.com/cadamcat/hindman-sums-products-lean4, by Yao Xu. Created 2026-10-07, release v1.0.0, last push 2026-10-10, 2 stars, 0 issues.
- Statement (Challenge.lean): `∀ r (χ : ℕ → Fin r) m, ∃ (A : Finset ℕ) (c : Fin r), A.card = m ∧ (∀ a ∈ A, 0 < a) ∧ ∀ B ⊆ A, B.Nonempty → χ (∑ b ∈ B, b) = c ∧ χ (∏ b ∈ B, b) = c`. This is exactly the conjecture. It omits the separation clause (1.1) and Corollary 1.2.
- What docs/verification.md reports for a fresh clone on 7–8 Oct:
  - `lake build` finished "no errors and no sorry"
  - `verify.sh` reports the axioms used are only propext, Classical.choice and Quot.sound
  - `leanchecker --fresh` exited 0
  - Comparator exited 0
- A second run on 10 Oct used Comparator with **nanoda**, an independent type checker written in Rust; it also exited 0. Both runs used Comparator's development stand-in for the landrun sandbox. audit/NonVacuity.lean checks the statement is not vacuous (parity colouring, m = 3).
- **The formalization does not follow the paper's cited inputs in §5** (docs/mathematics.md):
  - "The paper uses the Tao–Ziegler concatenation theorem. The formalization uses subgroup box-norm concatenation from N. Kravitz, B. Kuca, and J. Leng [arXiv:2407.08636 §6]".
  - "The paper uses the Green–Tao–Ziegler inverse theorem for linear orbits on a fixed finite family of nilmanifolds. OpenAI's library supplies the cyclic inverse theorem `OAI.Erdos3.exists_cyclicNativeInverse_positive` for polynomial orbits", bridged by a Baker–Campbell–Hausdorff linearization.
  - The Alignment Principle is taken unchanged from OpenAI's library.
  - The arithmetic inputs used are Mathlib, PrimeNumberTheoremAnd (PNT in arithmetic progressions) and "OpenAI's Brun–Titchmarsh bound".
- **I did not build or run it.** The box is CPU-loaded and the brief says reading only; the reported build took 34 minutes plus 30 more on 32 cores. Nobody besides the author has reported reproducing it.
- If the reports hold, the **core theorem is true**, but by a proof that replaces [34] and [17,18] at the §5 steps. That makes §5.3 and the Tao–Ziegler application exactly where the human-readable paper could still have a citation gap even though the theorem holds. The §3–5 referee should look there.

**B6. Expert commentary since 6 Oct 2026.**
- Terence Tao, Ryan Alweiss, Matt Bowen, Joel Moreira, Florian Richter: **not found**. Searches: WebSearch (standard and extended modes) for OpenAI/Hindman with each name, `site:x.com`, mathstodon/terrytao.
- MathOverflow: the StackExchange API search for "Hindman" shows nothing since 18 Mar 2026. I scanned all 7 MO questions created 7–9 Oct about the OpenAI release, plus their 14 answers; none mentions Hindman, 172 or sums and products.
- News coverage (officechai.com, kingy.ai) only relays Bloom's list.

---
## (4) Verdict on §1.1
**INACCURATE AT [21] (one attribution); otherwise ACCURATE.**
- The sentence "Hindman constructed a finite coloring of N with no infinite set whose terms, pairwise sums and pairwise products all have one color [21]" credits the 1980 *Two counterexamples* paper with the 7-colour pairwise result. Hindman himself (2013, 2022) attributes that result to *Partitions and pairwise sums and products*, JCTA 37 (1984) 46–60. The 1980 paper proves a different 2-colour counterexample (finite products plus pairwise sums), which does not imply the stated claim. Severity: COSMETIC. Fix: cite Hindman 1984.
- Every other theorem-number citation in §1.1 says what §1.1 claims.

Bibliography: 37/37 exist, no fabricated details. Two cosmetic defects: [18] is dated "April 2024" but the file is from Feb 2024; [2]'s DOI is printed by the journal but unregistered.

## Verified line by line vs skimmed
- **Verified against the primary text** (fetched and read): the arXiv version blocks for all 11 arXiv entries; Crossref metadata for 24 DOIs; zbMATH for [21], [22], [31], [35]; the theorem statements of [1] v6 Thm 1.3 and §§4–5, [2] Thm 1.2, [3] Thm 1.2, [8] Thm 1.1 (arXiv v1), [9] Thm 1.1 (arXiv v1), [11] Thm 1.2, [27] Thm 1.4 / Cor 1.5 (arXiv v1), [29] Thms 1.5 and 1.7, [30] Thm 2 / Cor 1.1; [22] pp. 81–82 (Hindman's posted final version); the [18] PDF and its timestamps; Bloom's post; the erdosproblems #172 page; the teorth YAML; the openai/math repo state; the cadamcat repo's README, docs, Challenge.lean, Main.lean and OAIAlignment.lean.
- **Secondary or partial:** [20]: abstract only, plus two independent quotations. [21]: content not read (ScienceDirect captcha); attribution judged from Hindman's own later citations and Semantic Scholar's machine summaries of the 1980 and 1984 abstracts. [23] Q17.18: two independent citers, book not fetched. [6], [7]: titles only. Published-version theorem numbering of [8], [9] (arXiv numbering checked; [27]'s carries over per Richter v2). Whether the cadamcat build actually passes: documentation read, not executed.
