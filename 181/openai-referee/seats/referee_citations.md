# Referee report, tag `citations`: OpenAI, "The hypercube Ramsey number has linear order" (23 Sept 2026, family 171)

**Scope.** (A) The reference list [1]–[34] (PDF pp. 170–172), and §1.1–1.2 (pp. 1–3): every theorem-number citation and every small argument there. (B) Novelty, provenance and reception in the live world. I did not referee the proof (§§2–18). I ran no lake or lean.

**Fetched.** 2026-10-11, ~12:10–13:30Z. Primary sources are under `/tmp/oaimath/171/refs/`:
- Crossref JSON: `crossref/`
- arXiv abs pages: `abs/`
- per-paper PDFs and text: `burr_erdos/`, `erdos_lovasz/`, `lee/`, `cfs2/`, `fs/`, `cfls/`, `fgmss_clique/`, `fgmss_tri/`, `msst/`, `tikh{,1,2}/`, `grr/`, `kr/`, `sudakov/`, `gowers/`
- GitHub API dumps: `world_gh/`
- the world-search sweep: `world/`

**Paper identity.** Our `paper.pdf` is byte-identical to the openai/math blob. `git hash-object` gives `aac972f536c67fe69a9e33a50eeea12e366497b7`, the same as the repo's tree entry for `preprints/The-hypercube-Ramsey-number-has-linear-order-September-23-2026/paper.pdf`.

## Headline

1. **No bibliographic detail is fabricated.** All 34 entries exist. All 31 DOIs resolve (doi.org returns 302 for each). Crossref or zbMATH matches every author list, title, venue, volume, issue and page range. The two renyi.hu URLs serve the right scans. The arXiv id for [34] is right.
2. **Every theorem-number citation in §1.1–1.2 says what the paper says it says.** I quote each source below. The most precise pinpoints check out exactly:
   - Lee's derivation of 2^{2n}+n²2^n sits in the paragraph after Thm 1.3.
   - Tikhomirov's Corollary 1.2 is 2^{2n−cn+1}+2. Caveat: this numbered corollary exists only from arXiv v3 (2 Mar 2024) on; v1 and v2 have no Corollary 1.2.
   - Gowers's sampling lemma is Lemma 11 in Section 4.
   - GRR Theorem 1 has the strict "<".
3. **§1.1's own small arguments are correct.** These are the 3·2^{n−1}−1 two-block colouring, the Gray-code Hamiltonian path and cycle, and the F^{□k} ⊆ Q_{dk} embedding. I checked the Gray-code claim mechanically for d ≤ 8, with a negative control.
4. **Four cosmetic notes, none load-bearing.** They are listed under Objections.
5. **(B) World state.** I found no human proof of R(Q_n)=O(2^n). Other facts:
   - The preprint is not on arXiv, and no improvement on Tikhomirov is anywhere in the literature. DS1 rev. 18 (24 Apr 2026) and erdosproblems.com/181 both still call Tikhomirov's bound current.
   - The source for R(Q_3)=13 is Lidický–Pfender (SIAM J. Discrete Math. 2021, Thm 3). No published bound on R(Q_4) found.
   - erdosproblems.com/181 shows no status (site-wide policy since 6 Oct). It has no mention of OpenAI and 0 proof claims.
   - Bloom's 8 Oct post: "This PDF proves the following… This proof has not been formalised. The PDF is 172 pages long", under general disclaimers that nothing was checked.
   - The teorth database still says `open` / `unformalized`.
   - No expert (Tao, Conlon, Fox, Sudakov, Tikhomirov, Lee) has said anything public about this paper that I could find.
   - openai/math has issues disabled; the paper was never revised (only commit `adc7f124`, 6 Oct). OpenAI's Lean library proves only 2^n ≤ R(Q_n) ≤ 4^{2^n} and the Lemma 2.1 reduction.
   - The only formal-methods artefact is the third-party Lean repo by Yao Xu, a DTU-affiliated LLM-inference engineer with ~3 weeks of public Lean history. The repo was built by AI agent lanes in ~32 hours.
   - Its "independent check" and "second kernel check" were both run and recorded **by the author himself**. His bounty PR says so: "The author ran the check; no independent person has reviewed the formalization… The raw logs are not published… Independent verifier(s), if any: none." They were run on a fresh cloud VM and on an unnamed 32-core machine, the second time also with the nanoda kernel. **Nobody else has reported a build.**
   - The repo's own `formalization.yaml` says `review: status: "agent-reviewed", reviewers: []` and "No independent human expert has reviewed the formalization."
   - The Formal Conjectures "solved" flag comes from the **formalizer's own PR** #7128. FC maintainer Moritz Firsching approved it ("Thanks, great to have a formal proof!") 32 minutes after it opened, in a batch of about 20 such PRs queued in one hour. There is no sign of a re-build, and FC's CI cannot build a linked external proof. The PR's approval came at 07:55:54Z, the merge-queue entry at 07:56:14Z, and the merge at 09:08:52Z.
   - The formalizer also has an open bounty claim for it: Justin Sun Prize PR #4967, JSP-000175.

---

## (1) Bibliography table [1]–[34]

Method:
- DOIs: `curl https://doi.org/<doi>` (302 = registered) plus the Crossref API.
- Entries without a DOI: zbMATH API, or the URL itself.
- arXiv: the submission-history block of the abs page.

| # | Cited as (abridged) | Record found | Verdict |
|---|---|---|---|
| 1 | Azuma, TMJ (2) 19 (1967) no. 3, 357–367, doi 10.2748/tmj/1178243286 | DOI → Project Euclid; Crossref vol 19 no 3 (no pages); zbMATH 0178.21103 "Tohoku Math. J., II. Ser. 19, 357-367 (1967)" | EXISTS-AS-CITED |
| 2 | Beck, *An upper bound for diagonal Ramsey numbers*, Studia Sci. Math. Hungar. 18 (1983) no. 2–4, 401–406 (no DOI) | zbMATH 0589.05051 "Stud. Sci. Math. Hung. 18, 401-406 (1983)". Tikhomirov's bibliography (v3) gives "18 (1983), no. 2-4, 401–406. MR0787944". | EXISTS-AS-CITED |
| 3 | Burr–Erdős, *On the magnitude of generalized Ramsey numbers for graphs*, Infinite and Finite Sets Vol. I, Colloq. Math. Soc. J. Bolyai 10, North-Holland 1975, 215–240, URL renyi.hu/~p_erdos/1975-26.pdf | zbMATH 0316.05110 matches (215–240). The URL serves a 25-page scan, pp. 215–240, of this paper (HTTP 200 with a browser UA; a bare `curl -I` gets 403). | EXISTS-AS-CITED |
| 4 | Chvátal–Rödl–Szemerédi–Trotter, JCTB 34 (1983) no. 3, 239–243 | Crossref matches. Crossref's author field reads "C Chvatál" (a Crossref error; the paper's "V. Chvátal" is right). | EXISTS-AS-CITED |
| 5 | Conlon, *Hypergraph packing and sparse bipartite Ramsey numbers*, CPC 18 (2009) no. 6, 913–923 | Crossref matches | EXISTS-AS-CITED |
| 6 | Conlon–Fox–Lee–Sudakov, *Ramsey numbers of cubes versus cliques*, Combinatorica 36 (2016) 37–70 | Crossref matches (no. 1; online 5 Nov 2014); arXiv 1208.1732v2 (13 Dec 2013) | EXISTS-AS-CITED |
| 7 | Conlon–Fox–Sudakov, *Short proofs of some extremal results II*, JCTB 121 (2016) 173–196 | Crossref matches; arXiv 1507.00547v2 (11 Feb 2016) | EXISTS-AS-CITED |
| 8 | Dirr–Dondl–Grimmett–Holroyd–Scheutzow, *Lipschitz percolation*, ECP 15 (2010) 14–21 | Crossref matches | EXISTS-AS-CITED |
| 9 | Erdős–Lovász, *Problems and results on 3-chromatic hypergraphs…*, Colloq. Math. Soc. J. Bolyai 10 (1975) 609–627, URL users.renyi.hu/~p_erdos/1975-34.pdf | zbMATH 0315.05117 matches; the URL serves the scan (title page verified) | EXISTS-AS-CITED |
| 10 | Erdős–Spencer, *Lopsided Lovász Local Lemma and Latin transversals*, DAM 30 (1991) nos. 2–3, 151–154 | Crossref matches | EXISTS-AS-CITED |
| 11 | Finner, AoP 20 (1992) no. 4, 1893–1901 | Crossref vol/issue; zbMATH 0761.60013 "Ann. Probab. 20, No. 4, 1893-1901" | EXISTS-AS-CITED |
| 12 | Fiz Pontiveros–Griffiths–Morris–Saxton–Skokan, *The Ramsey number of the clique and the hypercube*, JLMS 89 (2014) no. 3, 680–702 | Crossref matches; arXiv 1306.0461v1 | EXISTS-AS-CITED |
| 13 | same authors, *On the Ramsey number of the triangle and the cube*, Combinatorica 36 (2016) 71–89 | Crossref matches; arXiv 1302.3840v1 | EXISTS-AS-CITED |
| 14 | Fox–Sudakov, *Density theorems for bipartite graphs and related Ramsey-type results*, Combinatorica 29 (2009) no. 2, 153–196 | Crossref matches; arXiv 0707.4159v2 | EXISTS-AS-CITED |
| 15 | Freedman, AoP 3 (1975) no. 1, 100–118 | Crossref; zbMATH 0313.60037 "Ann. Probab. 3, 100-118" | EXISTS-AS-CITED |
| 16 | Gandhi–Khuller–Parthasarathy–Srinivasan, JACM 53 (2006) no. 3, 324–360 | Crossref matches | EXISTS-AS-CITED |
| 17 | Gowers, *A new proof of Szemerédi's theorem for APs of length four*, GAFA 8 (1998) no. 3, 529–551 | Crossref matches | EXISTS-AS-CITED |
| 18 | Graham–Rödl–Ruciński, *On bipartite graphs with linear Ramsey numbers*, Combinatorica 21 (2001) no. 2, 199–209 | Crossref matches; zbMATH 0989.05078; the PDF on Graham's UCSD page carries the header "Combinatorica 21 (2) (2001) 199–209" | EXISTS-AS-CITED |
| 19 | Haeupler–Saha–Srinivasan, JACM 58 (2011) no. 6, Art. 28, 1–28 | Crossref vol 58 no 6 pp 1–28 (Crossref has no article-number field; Art. 28 not independently checked) | EXISTS-AS-CITED |
| 20 | Hall, *On representatives of subsets*, JLMS (1) 10 (1935) no. 1, 26–30 | Crossref matches | EXISTS-AS-CITED |
| 21 | Hamming, BSTJ 29 (1950) no. 2, 147–160 | Crossref matches | EXISTS-AS-CITED |
| 22 | Harris–Srinivasan, TALG 13 (2017) no. 3, Art. 33, 1–40 | Crossref vol 13 no 3 pp 1–40 (article number not independently checked) | EXISTS-AS-CITED |
| 23 | Hoeffding, JASA 58 (1963) no. 301, 13–30 | Crossref matches | EXISTS-AS-CITED |
| 24 | Kakutani, Duke 8 (1941) no. 3, 457–459 | Crossref vol/issue; zbMATH 0061.40304 "457-459" | EXISTS-AS-CITED |
| 25 | Kostochka–Rödl, *On graphs with small Ramsey numbers*, JGT 37 (2001) no. 4, 198–204 | Crossref matches; Kostochka's posted PDF has running heads on pp. 199/200 | EXISTS-AS-CITED |
| 26 | Lee, *Ramsey numbers of degenerate graphs*, Ann. Math. (2) 185 (2017) no. 3, 791–829 | Crossref matches; arXiv 1505.04773v2 (1 Dec 2016) | EXISTS-AS-CITED |
| 27 | Lu–Székely, EJC 14 (2007) no. 1, R63, doi 10.37236/981 | Crossref art. R63; DOI → combinatorics.org v14i1r63 | EXISTS-AS-CITED |
| 28 | Moser–Tardos, JACM 57 (2010) no. 2, Art. 11, 1–15 | Crossref pp 1–15 (article number not independently checked) | EXISTS-AS-CITED |
| 29 | Mota–Sárközy–Schacht–Taraz, EJC 48 (2015) 165–176 | Crossref matches; arXiv 1602.05972v1 (journal-ref "European J. Combin. 48 (2015), 165-176") | EXISTS-AS-CITED |
| 30 | Ramsey, PLMS (2) 30 (1930) 264–286 | Crossref matches | EXISTS-AS-CITED |
| 31 | Shi, *Cube Ramsey numbers are polynomial*, RSA 19 (2001) no. 2, 99–101 | Crossref matches | EXISTS-AS-CITED |
| 32 | Shi, *The tail is cut for Ramsey numbers of cubes*, Disc. Math. 307 (2007) no. 2, 290–292 | Crossref matches | EXISTS-AS-CITED |
| 33 | Sudakov, *A few remarks on Ramsey–Turán-type problems*, JCTB 88 (2003) no. 1, 99–106 | Crossref matches; title verbatim on the PDF (Sudakov's own list titles it "Few remarks on the Ramsey-Turan-type problems") | EXISTS-AS-CITED |
| 34 | Tikhomirov, *A remark on the Ramsey number of the hypercube*, EJC 120 (2024) art. 103954; preprint arXiv 2208.14568 | Crossref: EJC vol 120, art. 103954, Aug 2024. arXiv versions: v1 Tue 30 Aug 2022 (21 KB) · v2 Sat 24 Sep 2022 (130 KB) · **v3 Sat 2 Mar 2024** (132 KB). | EXISTS-AS-CITED |

**Result: 34/34 exist. No wrong venue, volume, issue, year, page range or DOI.**
- Three ACM article numbers ([19], [22], [28]) are not in Crossref. I did not check them separately; their page ranges match.
- The LaTeX source (`build/references.tex` in the repo) has exactly 34 `\bibitem`s, in the same order as the PDF.

---

## (2) Theorem-citation table for §1.1–1.2 (paper paraphrase vs source, quoted)

| Paper claim (p.) | Source text read | Verdict |
|---|---|---|
| "Burr and Erdős called a family of graphs an L-set if one constant bounds the Ramsey number of every member by that constant times its order [3, Section 1]… They conjectured that every family of uniformly bounded arboricity is an L-set." (p.1) | [3] §1, p.216: "Definition. A set {G1, G2, …} of graphs is called an L-set if there is a constant c such that r(Gi) ≤ c·p(Gi) for all i … Conjecture. Any set of graphs or pairs of graphs having bounded arboricity is an L-set." | MATCH |
| "uniformly bounded arboricity and uniformly bounded degeneracy are equivalent boundedness conditions for families [3, Section 3]" (p.1) | §1, p.216: "the arboricity of a graph may be written max_{F⊆G} q(F)/(p(F)−1)", with edge-density ρ(G)=max q(F)/p(F) also introduced there. §3, p.220: σ(G)=max_F δ(F); "In [9], a graph with σ(G) = k is called k-degenerate"; "Lemma 3.3. For any graph G not consisting entirely of isolated points, ρ(G) ≤ σ(G) ≤ 2ρ(G)." | MATCH. Strictly, it needs §1 (arboricity ↔ density) plus §3 Lemma 3.3 (density ↔ degeneracy). COSMETIC, Obj. 1. |
| "Burr and Erdős raised the cube question separately in Section 7, asking whether the cubes form an L-set." (p.1) | §7, pp.238–239: "Perhaps any set of graphs satisfying the above two conditions is an L-set. An interesting test case is the set {Q_n} of cubes. The authors offer a total of $25 for deciding whether the set of cubes is an L-set." | MATCH |
| "The first-moment lower bound used by Burr and Erdős implies that a family with one linear Ramsey constant must satisfy e(H)/\|V(H)\| = O(log \|V(H)\|) … [3, Lemma 4.3 and Section 7]" (p.1) | Lemma 4.3, p.226 (rendered page): "Let p, q and s be the number of points, lines, and symmetries of G respectively. Then r(G) > (s·2^{q−1})^{1/p}." It is "taken from [12], which is based on a method of Erdős [13]". p.228: "Note that by Lemma 4.3, a necessary condition for {G_i} to be an L-set is that there be a constant c such that q(G_i)/p(G_i) < c log p(G_i) for every i." §7, p.238: "Lemma 4.3 shows that an order of growth no greater than this is a necessary condition that a set of graphs be an L-set." | MATCH. Arithmetic: e(Q_n)/\|V\| = n2^{n−1}/2^n = n/2 = ½log₂2^n. Correct. |
| "The standard lower-bound coloring with two blocks [6, Introduction] gives R(Q_n) ≥ 3·2^{n−1}−1" (p.1) | [6] arXiv v2, Introduction p.1: "One obvious construction, noted by Chvátal and Harary [16], … take χ(H)−1 disjoint red cliques of size \|G\|−1 and to connect every pair of vertices which are in different cliques by a blue edge … Burr [8] strengthened this bound by noting that if σ(H) is the smallest color class in any χ(H)-coloring of the vertices of H, we may add a further red clique of size σ(H)−1, obtaining r(G,H) ≥ (\|G\|−1)(χ(H)−1)+σ(H)." With G=H=Q_n, χ=2, σ=2^{n−1}: (2^n−1)+2^{n−1} = 3·2^{n−1}−1. | MATCH. The diagonal specialization is the paper's own and is correct; see §(3). |
| "Chvátal, Rödl, Szemerédi and Trotter proved in 1983 that graphs of any fixed maximum degree have Ramsey number linear in their order [4]" (p.2) | Primary not fetched: ScienceDirect answers 403 to curl and to WebFetch. Kostochka–Rödl [25] p.199: "Burr and Erdős [2] conjectured that for every d, there exists k = k(d) such that R(G,G) ≤ k\|V(G)\| (a) for every graph G with maximum degree at most d … The first conjecture was proved by Chvatal, Rödl, Szemerédi, and Trotter [4]". Beck's zbMATH review also states "r(G)<cn, where c … depends only on Δ". | MATCH (secondary, two independent sources) |
| "Lee later proved the corresponding assertion for every fixed degeneracy, resolving the bounded-degeneracy form of the Burr–Erdős conjecture [26, Theorem 1.1]" (p.2) | arXiv 1505.04773v2: "Theorem 1.1. There exists a constant c such that the following holds for every natural number d, r, and n satisfying n ≥ 2^{d2^{cr}}. For every edge two-coloring of the complete graph on at least 2^{d2^{cr}} n vertices, one of the colors is universal for the family of d-degenerate r-colorable graphs on at most n vertices. This settles the conjecture of Burr and Erdős since all d-degenerate graphs have chromatic number at most d+1." | MATCH (arXiv v2, 1 Dec 2016). The Annals page gives "Revised: 21 November 2016 Accepted: 28 November 2016", so v2 is the accepted text; I did not open the published PDF itself. |
| "Early work on cubes includes Beck's 1983 paper [2]." (p.2) | zbMATH review of [2]: "it is shown that r(G)<(2n)^{2Δ^{2k−3}}". Fox–Sudakov v2: "Beck [6] proved that r(Q_d) ≤ 2^{cd²}". GRR p.209: "This improves an old result of Beck [1], who showed that r(Q_n) < 2^{cn²}." | MATCH (secondary; primary not online) |
| "Graham, Rödl and Ruciński proved that a bipartite graph H of maximum degree at most Δ ≥ 1 satisfies R(H) < 8(8Δ)^Δ\|V(H)\| [18, Theorem 1]. For Q_n … R(Q_n) < 8(16n)^n, or m^{O(log log m)}" (p.2) | GRR, Graham's UCSD PDF, p.200: "Theorem 1. For all integers Δ ≥ 1, if H is a bipartite graph with maximum degree at most Δ, then r(H) < 8(8Δ)^Δ\|V(H)\|." p.209: "Corollary 1. There is a constant c > 0 such that for all n, r(Q_n) < 2^{cn log n}." Arithmetic: 8(8n)^n·2^n = 8(16n)^n = 8m^{4+log₂n} = m^{O(log log m)}. | MATCH (verbatim, including the strict "<") |
| "Shi then obtained a bound polynomial in m, using a refinement of Kostochka and Rödl's common-neighborhood lemma [25, 31], and later refined the estimate [32]." (p.2) | [31] abstract (OpenAlex): "for any positive constant c and bipartite graph G=(U,V;E) of order n where the maximum degree of vertices in U is at most c log n, R(G) < n^{1+(c+√(c²+4c))/2+o(1)}. In particular … R(Q_n) < 2^{(3+√5)n/2+o(n)}". Fox–Sudakov v2: "Shi [43], using ideas of Kostochka and Rödl [32], proved that r(Q_d) ≤ 2^{((3+√5)/2)d+o(d)}, which is a polynomial bound in the number of vertices with exponent (3+√5)/2 ≈ 2.618." [32]: the abstract is truncated at the formula in every metadata source; core.ac.uk and ScienceDirect return 403. CFS v2 lists both Shi papers ([47, 48]) among the improvements. | MATCH for [31]. [32]: COULD NOT FETCH its theorem; "refined the estimate" is consistent with the title and with CFS. |
| "Fox and Sudakov obtained R(Q_n) ≤ n2^{2n+5} [14, Corollary 1.3]" (p.2) | arXiv 0707.4159v2: "Corollary 1.3 For every positive integer d, r(Q_d) ≤ d2^{2d+5}." | MATCH |
| "Conlon, Fox and Sudakov obtained R(Q_n) ≤ 2^{2n+6} [7, Corollary 4.2]" (p.2) | arXiv 1507.00547v2 §4: "Corollary 4.2 For every positive integer d, r(Q_d) ≤ 2^{2d+6}." (from "Theorem 4.1 For every bipartite graph H on n vertices with maximum degree Δ, r(H) ≤ 2^{Δ+6}n"). | MATCH. Tikhomirov cites the general bound as "[4, Theorem 4.1]", consistent. |
| "Lee's Theorem 1.3 and the paragraph following it give R(Q_n) ≤ 2^{2n} + n²2^n for all sufficiently large n [26]" (p.2) | arXiv v2, the paragraph right after Thm 1.3: "Theorem 1.3 with ε = n²/2^n and α = 1/2 shows that r(Q_n) ≤ 2^{2n} + n²2^n holds for all sufficiently large n. This bound improves by a constant factor, the current best known bound r(Q_n) ≤ 2^{2n+6} of Conlon, Fox, and Sudakov". §7: "we slightly improved the previous best known bound to r(Q_n) = (1+o_n(1))2^{2n}." | MATCH. I also checked Lee's hypotheses: α^{d(d−2)} = 2^{−n(n−2)} ≤ n²2^{−n}, and \|W₂\|^d/(\|W₂\|)_d ≈ exp(n(n−1)/2^n) ≤ 1+n²/2^n for large n. |
| "Tikhomirov's exponential improvement is R(Q_n) ≤ 2^{2n−cn+1}+2 for an absolute c > 0 and all sufficiently large n [34, Corollary 1.2]" (p.2) | arXiv **v3** (2 Mar 2024): "Corollary 1.2. Let n₀, c > 0 be as in the last theorem. Then for every n ≥ n₀, the Ramsey number of the hypercube Q_n satisfies r(Q_n) ≤ 2^{2n−cn+1} + 2." Remark: "one can take c = 0.03656". **v1 and v2 have no Corollary 1.2.** There Theorem 1.1 itself ends "As a corollary, the Ramsey number of the hypercube satisfies r(Q_n) = O(2^{2n−cn})." | MATCH for v3 and (presumably) the EJC 2024 version the paper cites. The journal PDF was not fetched (Elsevier 403). Version-sensitive pinpoint; correct as cited. |
| "His Theorem 1.1 is a density theorem for one color: … embeds Q_n in every bipartite graph of density at least 1/2 whose two parts each have at least 2^{(2−c)n} vertices" (p.3) | v3: "Theorem 1.1. There are universal constants n₀, c > 0 such that for every n ≥ n₀, and every bipartite graph G = (V^up, V^down, E) satisfying \|V^up\|, \|V^down\| ≥ 2^{2n−cn} and \|E\| ≥ ½\|V^up\|\|V^down\|, the hypercube Q_n can be embedded into G." | MATCH |
| "Tikhomirov [34, Sections 1, 5 and 6] identifies an obstruction to mapping a whole cube bipartition uniformly into one prepared set. His proof instead distinguishes dispersed common neighborhoods, a denser subgraph, and a block structure suited to a facet-wise cube embedding." (p.3) | v3 §1: "the dependent random choice technique for bounding r(Q_n) as outlined in (I)–(II) hits a barrier around 2^{2n}… The deficiency of the scheme (I)–(II) is thus not in choosing the set S but in embedding V_H^up into S uniformly at random" (rigorous version in App. A). Trichotomy: "(a) … common neighborhoods … tend to have small overlaps. (b) G contains a large subgraph of a density significantly larger than 1/2 … (c) G contains a subgraph having a 'block' structure … we construct a special randomized facet-wise embedding". Outline: "In Section 5 we define block-structured bipartite graphs and develop a randomized procedure for embedding … Finally, in Section 6 we state and prove the structural Proposition 6.3". | MATCH. Case (a) is formally treated in §4 (Lemma 4.7), which the paper does not cite, but it describes rather than relies on it. |
| "Kostochka and Rödl's deterministic lemma [25, Lemma 1] … find[s] large host sets in which every subset of a prescribed size has many common neighbors" (p.3) | [25] p.200: "Lemma 1. … Then for every subgraph H = (V₁,V₂;E) of the complete bipartite graph K_{kn,kn} … such that \|E\| ≥ (kn)²/2, there exists M ⊂ V₁ with \|M\| ≥ m with the property that for every d-element subset D of M, the number of vertices of H adjacent to all vertices in D is at least n." The proof is a deterministic double count of "poor" d-tuples and "bad" l-tuples. | MATCH |
| "Sudakov's probabilistic argument [33, Section 2] … Sudakov explicitly drew on Gowers's earlier sampling idea [17, Section 4, Lemma 11]" (p.3) | [33] §2 "Key lemma": "It is based on probabilistic arguments and was influenced by Gowers [7]" ([7] = Gowers, AP4, GAFA). "Lemma 2.1 … contains a set U ⊂ V of size at least m with the property that any subset W of U of size k has \|N(W)\| ≥ m. Proof. Let x₁,…,x_t be … t, not necessarily distinct vertices of G; which we pick uniformly at random." [17] (Gowers's author-hosted GAFA preprint `gafafour2.ps`), Section 4 "An Application of Freiman's Theorem": "We begin with a combinatorial lemma. Lemma 11. Let X be a set of size m, let δ > 0 and let A₁,…,A_n be subsets of X such that ΣΣ\|A_x ∩ A_y\| ≥ δ²mn². There is a subset K ⊂ [n] of cardinality at least … such that for at least 90% of the pairs (x,y) ∈ K² the intersection A_x ∩ A_y has cardinality at least δ²m/2 … Proof. … Choose five numbers j₁,…,j₅ ≤ m at random". | MATCH. Sudakov says "influenced by Gowers"; the Section 4/Lemma 11 pinpoint is the paper's own, and it is correct in Gowers's preprint numbering. |
| "Conlon uses a hypergraph packing argument [5]" (p.3) | [5] abstract: "Our proof hinges upon a quantitative form of a hypergraph packing result of Rödl, Ruciński and Taraz." | MATCH |
| "Fox and Sudakov use an auxiliary hypergraph embedding [14, Lemmas 2.1–2.2]" (p.3) | v2 §2: "Lemma 2.1 If ε > 0 and G = (V₁,V₂;E) is a bipartite graph … there is a subset A ⊂ V₂ … for all but at most … d-sets S in A, we have \|N(S)\| ≥ x." "Lemma 2.2 Let H be a n-vertex hypergraph with maximum degree d … If F is a down-closed hypergraph with N ≥ 4n vertices and more than (1−(4d)^{−h})·C(N,h) edges … then there are at least (N/2)^n labeled copies of H in F." | MATCH |
| "Conlon, Fox and Sudakov use local avoidance of exceptional subsets and collisions [7, Section 4]" (p.3) | v2 Lemma 4.5 proof: "For two vertices uv of H, consider the bad event A_uv that f(u) = f(v). For an edge e of H, we also consider the bad event B_e that … f(e) is not an edge of G … We now apply the local lemma." | MATCH |
| "These refinements give bounds of the form 2^{O(Δ)}m" (p.3) | [5] abstract "less than 2^{cΔ}n"; FS "r(H) ≤ Δ2^{Δ+5}n"; CFS "r(H) ≤ 2^{Δ+6}n" | MATCH |
| "Lee's embedding records a penalty for small common neighborhoods, controls its average over target neighborhoods, and embeds the most constrained vertices first [26, Section 2]" (p.3) | v2 §2: "Definition 2.1 … the θ-defect of Q as ω_θ(Q) = 0 if \|N(Q)\| ≥ θ, θ/\|N(Q)\| otherwise … We give a penalty to the d-tuples having only a small number of common neighbors." Proof of Thm 2.3: "there exists a particular choice of φ such that Σ_v ω(φ(e_v)) ≤ \|W₁\| … Order the vertices in W₁ … in decreasing order of ω(φ(e_{v_i}))". | MATCH |
| "Conlon, Fox, Lee and Sudakov proved R(Q_n, K_s) ≤ c_s2^n for every fixed s ≥ 3 [6, Theorem 1.1]" (p.3) | v2: "Theorem 1.1. For any natural number s ≥ 3, there exists a constant c_s such that r(Q_n, K_s) ≤ c_s2^n." | MATCH |
| "[6, Introduction]" lower-bound colouring, and "R(Q_n,K_s) … least order … red Q_n or a blue K_s" | quoted above | MATCH |
| "Fiz Pontiveros et al. obtained the triangle asymptotic R(Q_n,K_3) = (1+o(1))2^{n+1} [13, Theorem 1.1]" (p.3) | arXiv 1302.3840v1: "Theorem 1.1. r(K₃, Q_n) = (1+o(1))2^{n+1} as n → ∞." | MATCH |
| "R(Q_n,K_s) = (s−1)(2^n−1)+1 for each fixed s ≥ 3 and all sufficiently large n [12, Theorem 1.1]" (p.3) | arXiv 1306.0461v1: "Theorem 1.1. Let s ∈ N. Then r(K_s, Q_n) = (s−1)(2^n−1)+1 for every n ≥ n₀(s)." | MATCH (the paper restricts to s ≥ 3, a weaker statement) |
| "The cube tilings in the Conlon–Fox–Lee–Sudakov and triangle papers use subcubes obtained by fixing initial coordinates" (p.3) | CFLS v2 p.5: "We represent the subcubes of Q_n by using vectors in {0,1,∗}^n … [the procedure] uses only cubes that have all their fixed coordinates at the start of the vector." FGMSS-triangle v1 §2: "the subcube of Q_n consisting of points whose initial coordinates agree with x … We shall call such a subcube an initial subcube". | MATCH |
| "Mota, Sárközy, Schacht and Taraz proved R(P_a□P_b) = (3/2+o(1))ab as ab → ∞ … [29, Corollary 1.4]. Their framework fixes the degree" (p.2) | arXiv 1602.05972v1: "Corollary 1.4. For grid graphs G_{a,b} we have R(G_{a,b},G_{a,b}) = (3/2+o(1))ab … where o(1) tends to 0 as ab → ∞." G_{a,b} has "vertex set [a]×[b] … equal in one coordinate and consecutive in the other" (= P_a□P_b). Thm 1.2 is "For every γ > 0 and natural number Δ …" | MATCH |

**§1.1 verdict: every theorem-number citation is accurate.** Four statements rest on secondary sources only, because the primary is paywalled or not online: CRST [4], Beck [2], Shi [32], and the journal (not arXiv) numbering of [26] and [34].

---

## (3) The paper's own small arguments in §1.1: checked

1. **Lower bound R(Q_n) ≥ 3·2^{n−1}−1** (p.1).
   - Paper: "take blocks of sizes 2^n − 1 and 2^{n−1} − 1, color edges inside each block red, and color crossing edges blue. Each red component is too small for Q_n, while a blue copy would need 2^{n−1} vertices in each block."
   - The construction colours K_{3·2^{n−1}−2}. Red components are cliques of size ≤ 2^n−1 < \|Q_n\|, and Q_n is connected, so there is no red Q_n.
   - Blue is K_{2^n−1, 2^{n−1}−1}. A connected bipartite subgraph of a bipartite graph keeps its unique bipartition inside the sides, so a blue Q_n needs 2^{n−1} vertices on each side, but the small side has 2^{n−1}−1.
   - n = 1: R(Q_1) = R(K_2) = 2 = 3·1−1, "immediate".
   - It is Burr's bound (quoted from [6]) at G=H=Q_n. **CORRECT.**
   - Mechanical check, n = 2: the 3+1 block colouring of K_4 has no monochromatic C_4. Control: a 3+3 block colouring of K_6 does have one.
   - Comparison with known exact values: R(Q_1)=2 (bound tight), R(Q_2)=R(C_4)=6 (bound 5), R(Q_3)=13 (bound 11). So the bound is not tight for n = 2, 3. The paper does not claim it is; it only uses it for the order of growth. Sources for R(Q_3)=13 and known R(Q_4) bounds are in §(4) B1.
2. **Order of growth.** "Theorem 1.1 therefore determines the order of R(Q_n). It gives no numerical value for C and does not determine whether R(Q_n)/2^n converges". Correct, given Thm 1.1.
3. **Ambient-cube monotonicity** (p.2): "If H is a not necessarily induced subgraph of Q_d and 2^d ≤ A\|V(H)\| … R(H) ≤ R(Q_d) ≤ C2^d ≤ CA\|V(H)\|." Correct: Ramsey numbers are monotone under (non-induced) subgraphs.
4. **Cartesian powers** (p.2). For F spanning in Q_d, F^{□k} ⊆ Q_d^{□k} = Q_{dk}, spanning, with \|V(F)\|^k = 2^{dk}. Hence R(F^{□k}) ≤ C2^{dk} = C\|V(F)\|^k. **CORRECT.**
   - Edge case d = 0: F = K_1, R = 1 ≤ C. This needs C ≥ 1, which Thm 1.1 at n = 0 forces, since R(Q_0)=1 ≤ C·1.
5. **Reflected Gray code** (p.2). The construction: "prefixing 0 to the order of Q_{d−1} and then 1 to its reverse. Consecutive vertices are adjacent, and for d ≥ 2 the first and last vertices are also adjacent". The first word is 0^d and the last is 10^{d−1}, which differ in one coordinate. At the junction, 0w and 1w are adjacent. **CORRECT.**
   - Script check: for d = 1..8, all 2^d words are distinct, consecutive words are adjacent, and the first and last are adjacent. The negative control (plain binary order) fails as it should.
   - "cycles on 2^d vertices for d ≥ 2" is right. At d = 1 the "cycle" would be a single edge, and the paper correctly excludes it.
6. **Density arithmetic** (p.1): e(Q_n)/\|V(Q_n)\| = n/2. Correct.
7. **m = 2^n translations** (p.2): an "extra logarithmic factor above m²" (n2^{2n+5} = 32m² log₂m), a "constant multiple of m²" (64m²), "(1+o(1))m²", and an "exponent below 2" (2m^{2−c}+2). All correct.

---

## Objections (all in scope; none FATAL, none GAP)

1. **COSMETIC: §1.1, p.1, "[3, Section 3]".**
   - Verbatim: "uniformly bounded arboricity and uniformly bounded degeneracy are equivalent boundedness conditions for families [3, Section 3]."
   - Section 3 (Lemma 3.3) relates degeneracy σ to edge-density ρ. The arboricity formula that relates arboricity to ρ is in Section 1.
   - The claim is true; the pinpoint is half the story. Exposition only. Fix: "[3, Section 1 and Lemma 3.3]".
2. **COSMETIC (version-sensitive pinpoint): §1.1, p.2, "[34, Corollary 1.2]" and "His Theorem 1.1".**
   - Correct for arXiv v3 (2 Mar 2024) and presumably for EJC 120 (2024), which the bibliography cites.
   - A reader who opens v1 or v2 finds no Corollary 1.2; there the bound is folded into Theorem 1.1 as O(2^{2n−cn}).
   - Fix: "arXiv:2208.14568v3" in [34].
3. **COSMETIC: §1.2, p.3, "Sudakov explicitly drew on Gowers's earlier sampling idea [17, Section 4, Lemma 11]".**
   - Sudakov writes only "was influenced by Gowers [7]". The Section 4/Lemma 11 pinpoint is the paper's own identification.
   - It is correct in Gowers's author-hosted GAFA-format preprint (Lemma 11 opens §4 "An Application of Freiman's Theorem"). I could not check the published GAFA pagination (Springer challenge page).
   - "Explicitly" slightly overstates "influenced by".
4. **COSMETIC: source tree, not the PDF.** `build/sections/01-regime-guide.tex` (8,167 bytes) is in the repo but is never `\input` by `main.tex`. `main.tex` inputs 01-introduction, proof-inputs (= §§2–18) and regime-table (= App. A). It is an orphan draft file. No effect on the paper.

I have no objection to the mathematics of §1.1–1.2. Every quantitative claim there is either a correctly cited external theorem or an elementary argument I checked.

## Parameter-dependency table (scope §1.1–1.2)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| C (Thm 1.1) | the main theorem, absolute | nothing | §1.1 consequences (R(H) ≤ CA\|V(H)\|, R(F^{□k}) ≤ C\|V(F)\|^k). Needs C ≥ 1, forced by n = 0. |
| A ≥ 1 | the hypothesis 2^d ≤ A\|V(H)\| | chosen by the user, fixed | §1.1, p.2 |
| d, k | integers, d ≥ 0, k ≥ 1 | free; C is uniform in them | §1.1, p.2 |
| c (Tikhomirov) | [34] Thm 1.1, absolute (c = 0.03656 allowed) | nothing | historical only |
| c_s (CFLS) | [6] Thm 1.1 | s | historical only |

No proof constants of §§2–18 are in scope.

---

## (4) World state (B), as of 2026-10-11

Sources: (i) my own `gh api` reads, marked [me]; (ii) a tool-equipped search seat whose full log, raw API dumps and saved pages are in `/tmp/oaimath/171/refs/world/` (`WORLD_FINDINGS.md`), marked [seat]. I re-checked against the saved artifacts the [seat] items marked ✔.

### B1. Prior or independent human work: none found

- **arXiv** [seat]. API queries, all https, sorted by date:
  - `abs:"Ramsey number" AND abs:hypercube` (9), `ti:hypercube AND ti:Ramsey` (4), `abs:"Ramsey numbers of cubes"` (0), `abs:Burr AND abs:Erdos AND abs:cube` (1 = 1208.1732), `ti:"Ramsey number of the hypercube"` (2), `abs:"R(Q_n)"` (10), `au:OpenAI` (11, all model/system cards), `ti:"linear order" AND ti:hypercube` (0), exact title (0)
  - variants `abs:hypercube AND abs:Ramsey`, `abs:"Burr-Erdos"`, `ti:cubes AND ti:Ramsey`
  - a completeness sweep `abs:Ramsey AND submittedDate:[202609010000 TO 202610120000]`: 66 papers, none on cubes
  - Every 2022+ hit is listed in WORLD_FINDINGS.md §1(a). They concern poset/Boolean-lattice R(Q_n,Q_n), oriented Ramsey numbers, Erdős–Gyárfás-type colourings *of* Q_n, Euclidean Ramsey, or are false hits.
  - **No improvement on the diagonal bound after Tikhomirov 2208.14568: NOT FOUND.**
  - **No human proof of R(Q_n)=O(2^n), before or independent of OpenAI: NOT FOUND.**
  - **The OpenAI preprint is not on arXiv.**
- **Best human bound as of today**: Tikhomirov, R(Q_n) ≤ 2^{2n−cn+1}+2 (c = 0.03656 allowed). Two sources still call it current:
  - Radziszowski's dynamic survey DS1, "revision #18: April 24, 2026", §5.17(m) ✔: "… the latest one to 2^{2n−cn+1} + 2, for some positive c and sufficiently large n [Tikh]"
  - erdosproblems.com/181 ✔: "the current best bound due to Tikhomirov [Ti22] is R(Q_n) ≪ 2^{(2−c)n}"
- **Small values** [seat, ✔ against `ds1.txt` and `lidp.txt`]:
  - DS1 §5.13: "R(Q3, Q3) = 13, where Q3 is the 8-vertex cube graph [LidP]". §5.17(n): "A lower bound construction for 12 ≤ R(Q3,Q3) was presented in [HaKr2], and R(Q3,Q3) = 13 was shown in [LidP]."
  - [LidP] = Lidický–Pfender, *Semidefinite Programming and Ramsey Numbers*, arXiv 1704.03592v2 (2020), SIAM J. Discrete Math. 35(4) (2021). Its Theorem 3: "R(Q3, Q3) = 13."
  - [HaKr2] = Harborth–Krause, *Distance Ramsey Numbers*, Utilitas Math. 70 (2006).
  - **R(Q_4): no bound found.** DS1 rev. 18 has no Q_4 entry, and WebSearch found nothing.
  - R(Q_2) = R(C_4) = 6 is classical. So the paper's 3·2^{n−1}−1 gives 2, 5, 11 against the true 2, 6, 13.
- **WebSearch** [seat] for `"Ramsey number of the hypercube" OpenAI linear 2^n`, `hypercube Ramsey number linear order OpenAI Burr Erdős conjecture reaction mathematicians` and `"cube Ramsey" OR "hypercube Ramsey" upper bound 2^{2n} improvement 2025 2026 arXiv` found nothing beyond the items here.

### B2. erdosproblems.com, the teorth database, Tao, and commentary since 6 Oct

- **Access.** erdosproblems.com Cloudflare-challenges exe.dev curl and WebFetch. The pages were fetched through our Hetzner IP.
- **The cached `/tmp/oai-math/bloom_blog10.html` is not the blog post.** It is a 5.5 KB Cloudflare "Just a moment…" challenge page. I re-checked: `grep -c "Just a moment"` = 1, `grep -ci hypercube` = 0.
- **https://www.erdosproblems.com/181**, read 2026-10-11 [seat, ✔ `ep_181.txt`]:
  - Statement: "Let $Q_n$ be the $n$-dimensional hypercube graph (so that $Q_n$ has $2^n$ vertices and $n2^{n-1}$ edges). Prove that \[R(Q_n) \ll 2^n.\]"
  - The remarks name Tikhomirov as current best.
  - **No status is displayed** (site-wide since 6 Oct). The Wayback capture of 2026-09-23 showed "OPEN".
  - **No mention of OpenAI.** "Proof claims (0)", "Comments (1)". The one comment is a 23 Jul 2026 typo note. "The ability to post new comments has been suspended."
  - History: the remark text is unchanged since 2025-10-20.
- **Bloom, "Erdős problems in the OpenAI proofs", 8 Oct 2026**, https://www.erdosproblems.com/forum/thread/blog:10 [seat: live copy plus Wayback 2026-10-08 22:59Z; ✔ `ep_blog10.txt` l.84–88]. The #181 paragraph, verbatim:

  > "Problem [181] - Ramsey number of the hypercube. This PDF proves the following. If $Q_n$ is the $n$-dimensional hypercube graph then \[R(Q_n) \ll 2^n.\] This was a conjecture of Burr and Erdős. The best previous lower bound was $\ll 2^{cn}$ for some $c<2$, by Tikhomirov [Ti22]. This proof has not been formalised. The PDF is 172 pages long."

  - For #181 he writes "proves", where most entries read "claims". "lower bound" is his slip for upper bound.
  - General disclaimers: "I have not yet looked at in any serious way any of the proofs in this release, so all of these should be read as 'claims'…"; "This post should not be read as any kind of endorsement"; "These papers are, at a glance, very poorly written, in the usual AI fashion. I expect that the vast majority of them are (a) correct yet (b) capable of being substantially simplified".
  - None of the 9 comments mentions #181.
- **teorth/erdosproblems `data/problems.yaml`** [seat, ✔ `teorth_problems.yaml`]:
  - Entry 181: `status: {state: "open", last_update: "2025-08-31"}`, `formal_status: {state: "unformalized"}`.
  - The latest commit on the file is the bot's ba83a566c6 at 2026-10-11T10:49:07Z, after the FC change. **The database has not picked up FC's "solved" flag.**
- **Tao, 6 Oct 2026**, "Changes to the Erdős problems web site", https://terrytao.wordpress.com/2026/10/06/changes-to-the-erdos-problems-web-site/ [seat]:
  - It is a guest crosspost of Bloom's text. Statuses are no longer displayed; comments and proof claims are frozen.
  - "I will try to link to correct Lean formalisations (if verified on Palomar) quickly; proofs which are poorly explained, and not accompanied by a formalisation, I am unlikely to update the site with."
  - It does not mention 181 or the hypercube, nor do any of Tao's nine October 2026 posts or their comments (grep = 0).
- **Expert commentary specifically on the hypercube paper, since 6 Oct: NOT FOUND.** Sources searched [seat]:
  - Tao: blog and Mathstodon statuses back to 2026-09-03
  - Conlon, Fox, Sudakov, Tikhomirov, Lee: named WebSearches
  - MathOverflow: StackExchange API from 2026-09-01 for "hypercube Ramsey", "Burr Erdos", "cube Ramsey" (all 0), plus full bodies, answers and comments of the 8 OpenAI-related questions of 8 Oct
  - Hacker News: Algolia from 2026-10-01, plus per-story comment searches in 49984923 "Sharing AI progress in mathematics" (1,528 comments) and 50002650 "OpenAI withdraws three mathematical results"
  - X: WebSearch only; a coverage limit, not proof of absence
  - Mathstodon tags
  - The Verge (11 Oct) and the AHM statement page
  - mahrud/openai-math-comments PR #171 "171. The hypercube Ramsey conjecture" (bot-opened 2026-10-09T13:18:15Z) [me]: **0 comments, 0 review comments**
  - **Lean Zulip: NOT ACCESSIBLE.** The API needs a login, and the public archive was last updated Feb 2026.
- **One other formalization effort** [me], TheJustinSunPrize/awards issue #4720 (haoruilee, 2026-10-07T01:26Z, closed 01:30Z): "I am assessing an independent Lean formalization of JSP-000175 … Our initial work covers only small supporting lemmas … Codex agents are assisting this investigation." No completed second formalization found.

### B3. The third-party Lean formalization: github.com/cadamcat/hypercube-ramsey-lean4 (read via `gh api` and the local clone, 2026-10-11 ~13:00Z)

**Who.**
- GitHub `cadamcat` is "Yao Xu", company "Technical University of Denmark", location Copenhagen, account created 2023-08-31.
- Bio: "LLM inference on consumer hardware: multi-GPU AMD Radeon (ROCm, RCCL, vLLM) and the Apple Neural Engine (Core ML, MLX)." 15 public repos, 2 followers.
- Public Lean history starts in September 2026:
  - `catalan-lean4`, created 2026-09-19 ("Complete Lean 4 formalization of Catalan's conjecture")
  - mathlib4 PR #44066, opened 2026-09-22, still open: "doc: note formalisation of Mihăilescu's theorem in 1000.yaml"
  - then four formalizations of OpenAI-release papers in four days: `hindman-sums-products-lean4` (created 2026-10-07T22:52Z, Erdős #172 / family 164), `hypercube-ramsey-lean4` (2026-10-08T07:33Z), `artin-primitive-roots-lean4` (2026-10-09), `distinct-distances-lean4` (2026-10-10)
- Before September 2026 his public work is vLLM, ROCm and CoreML. I found no Lean or combinatorics work, and no publication by this person on Ramsey theory.

**What the repo says about authorship and review** (verbatim):
- AUTHORS.md: "The author planned, dispatched and reviewed the work. Formalization and review used Claude Opus 5.5 in Claude Code, GPT-6 Luna and GPT-6.1 Sol in Codex, and Gemini 3.8 Flash in Antigravity."
- formalization.yaml: `review: status: "agent-reviewed"`, `reviewers: []`, and "No independent human expert has reviewed the formalization."
- `author_endorsement: "not-contacted"`: OpenAI was not contacted.
- "A blueprint split the paper into intermediate Lean statements; each was frozen with a hash of its elaborated type before any proof of it was attempted, and statements were attacked for counterexamples, with those found false repaired and frozen again."
- Its design note `HypercubeRamsey/S03/Injection/DESIGN.md` records such a repair for Lemma 3.9: "The old completion is false. Take one row, d=11^20 …".
  - The false statements there are the agents' own decompositions ("Old node | Old assertion"). The replacements cite the paper's TeX lines ("TeX 627–647: only dummy atoms are O(1/d)").
  - So the note does **not** claim the paper is wrong. It does show that the agents' first reading of Lemma 3.9 was wrong. The proof referee for §3 should read that note against Lemma 3.9 as written.

**Timeline** (GitHub API; commit dates are author-set metadata):

| Time (UTC) | Event |
|---|---|
| 23 Sep 2026 | paper dated |
| 2026-10-06T21:47:02Z | openai/math created |
| 2026-10-06T21:58:50Z | its "Initial commit" `adc7f124` (the paper's only commit) |
| 2026-10-06T22:43:51Z | cadamcat stars openai/math |
| 2026-10-06T23:31:58Z | first repo commit "Set up the Lean project" |
| 2026-10-07 | 1,737 commits |
| 2026-10-08 | 177 commits |
| 2026-10-08T07:25Z | v1.0.0 date set |
| 2026-10-08T07:33:02Z | repo created on GitHub (single push of all ~1,914 commits, per his own JSP PR) |
| 2026-10-08T08:35Z | 1870de67 records "independent check" |
| 2026-10-10 | history rewritten and force-pushed ("Commit hashes were renumbered on 10 October 2026, when local file paths were removed"); v1.0.0 = `ad206e1b`, tree `477b9a49…`, same tree as the pre-rewrite `88b2205…` archived by Software Heritage at 2026-10-08T08:18:42Z |
| 2026-10-11T00:10:48Z | 0d0bebc0 records "second-kernel check" |

- Total: 1,922 commits, all by "Yao Xu".
- So v1.0.0 was produced in about **32 hours** from the public release.
- 41 commits are titled "WIP before escalation (may not compile)".
- Merge commits name agent "lanes" with prefixes `sol-` (258), `q-` (163), `p-` (47), `opus-` (42), `skel-` (22), `fw-`/`fix-` (4 each), `g-` (3). Examples: "Merge lane opus-s05-k1", "Merge lane sol-s10-d56".

**What 1870de67 and 0d0bebc0 record** (`docs/verification.md`; both commits only add text there, +17 and +6 lines):

- **1870de67, "Independent check of v1.0.0".**
  - Setup: "On 8 October 2026 (UTC), release v1.0.0 … was cloned from GitHub onto a new Google Cloud virtual machine (c4d-standard-32, 32 cores, Ubuntu 24.04.5 LTS) and checked".
  - Results: `lake build` exit 0 after 1483 s (9,673 jobs); `verify.sh` exit 0 with axioms [propext, Classical.choice, Quot.sound]; `leanchecker --fresh` exit 0 after 1334 s; Comparator exit 0, "Lean default kernel accepts the solution".
  - Also: "It ran with comparator's development stand-in for the landrun sandbox, so it checked the statement match and kernel acceptance without isolating the build from the code it checks."
  - **No operator is named.** "Independent" means a fresh machine, not a different person. The file also says leanchecker "is a second check by the same Lean kernel, not by an independent one."
- **0d0bebc0, "Second kernel check".**
  - Setup: "On 10–11 October 2026 (UTC), v1.0.0 … was cloned again from GitHub onto a 32-core Linux machine". Comparator ran with `"enable_nanoda": true` (nanoda at `3a24072`, "an independent type checker for Lean written in Rust").
  - Result: "Comparator exited with status 0: the statement matches the challenge, and both nanoda and the Lean kernel accept the solution. The sandbox was again comparator's development stand-in for landrun."
  - Negative controls: "nanoda rejected an export that uses sorryAx and an export with an altered numeral."
  - The machine and operator are unnamed. A second **kernel implementation**, not a second **person**.
- **The author says outright that he ran both checks himself.** JSP PR #4967 body, l.98, describing the 8 Oct run: "Limitations. Comparator ran with its development stand-in for the `landrun` sandbox (it prints "THIS IS NOT REAL LANDRUN"), so the build was not isolated from the code under check. `enable_nanoda` is `false` in `Challenge.json` … Mathlib and the other packages come from official caches and were not rebuilt from source. **The author ran the check; no independent person has reviewed the formalization.**" l.100: "**The raw logs are not published.**" l.107: "**Independent verifier(s), if any: none.**"
- Repo size, from my clone at `35fa1344`: 752 `.lean` files outside `.lake`, 532,033 lines under `HypercubeRamsey/` (the repo's own count is 532,045).

**Has anyone other than the author reported a build?** **Not found.** Searches:
- The repo has 0 issues and 0 PRs, ever (`issues?state=all` → 0), and 0 forks.
- `gh search issues "hypercube-ramsey-lean4"` returns only unrelated hits.
- `gh search code "hypercube-ramsey-lean4"` returns only FC's `181.lean` and the repo's own files.
- The FC PR has no comment reporting a build (see B4).
- His JSP prize PR has no comments or reviews (see below).
- Lean Zulip and HN: see B2's sweep.
- **Our own replay** (`/tmp/oaimath/171/lean-build/`) is in progress and is the first non-author build I know of.

**Incentive context.**
- 2026-10-10T09:50:20Z: he opened TheJustinSunPrize/awards PR #4967, "JSP-000175: complete Lean formalization of the linear hypercube Ramsey bound (Erdős 181)". It is open, with no comments or reviews. The Justin Sun Prize describes itself as "a problem-list-based academic bounty mechanism".
- He opened parallel claims for Hindman (#4966), Artin (#4970) and distinct distances (#4994).
- JSP PR #4869, merged 2026-10-08, had recorded OpenAI's 19 results with the caveat: "Independent mathematical review, a clean Lean build, Comparator execution and transitive axiom audits were not performed".

**What the formalization depends on from OpenAI.**
- It imports one OpenAI module, `OAI.Combinatorics.Ramsey.Hypercube` (THIRD_PARTY.md). That module supplies the cube, `ramseyNumber`, finite Ramsey bounds, cross colourings and `counterexample_sequence_of_not_linear` (= Lemma 2.1).
- The repo itself formalizes "Sections 3 to 18".

### B4. google-deepmind/formal-conjectures #6906 and PR #7128 (gh api)

- **Issue #6906**, "ErdosProblems/181: `erdos_181` is true".
  - Opened **2026-10-07T21:00:50Z by `mo271`** (Moritz Firsching, Google DeepMind; an FC maintainer).
  - Body: "the following result appears to settle the statement … No Lean proof is included in the release for this paper. **Suggested fix:** Mark the declaration `research solved` and cite the paper. Please check the claim against the source and the exact Lean statement before opening a PR. The comparison was prepared with AI assistance and may contain mistakes."
  - Closed 2026-10-11T09:08:54Z by mo271.
- **PR #7128**, "feat(ErdosProblems/181): mark solved and link the formal proof".
  - Author **cadamcat** (the formalizer himself); opened 2026-10-11T07:23:38Z.
  - **One review: mo271, APPROVED, 2026-10-11T07:55:54Z, "Thanks, great to have a formal proof!"**
  - **Merged 2026-10-11T09:08:52Z by mo271**, through GitHub's merge queue. The PR timeline: `reviewed` 07:55:54Z, `added_to_merge_queue` 07:56:14Z (the date stamped on squash commit `59f54ca88e`, which is where "07:56Z" comes from), `merged` 09:08:52Z, `closed` 09:08:53Z.
  - In the same hour mo271 queued about 20 "mark solved / link formal proof" PRs. Commits on `main` between 07:42Z and 08:48Z include #6898 "mark problems solved in the OpenAI math release and link formal proofs" and #7127 (Erdős 172, the same formalizer). This was batch triage, not a per-PR build.
  - Zero comments. One commit, one file (`181.lean`, +5 −1): the category goes `research open` → `research solved`, the attribute `formal_proof using lean4 at "https://github.com/cadamcat/hypercube-ramsey-lean4/blob/ad206e1b…/HypercubeRamsey/Main.lean#L14"` is added, and the OpenAI preprint is added to the references. The statement is unchanged.
  - The PR's own "Checks" section lists only `git diff --check` and `lake --wfail build 'FormalConjectures.ErdosProblems.«181»'`, i.e. building FC's own sorry'd statement file.
- **Did any FC maintainer build the proof?** No evidence:
  - The review is a one-line approval 32 minutes after opening, with no build log.
  - FC's CI runs on the merge commit `59f54ca8`: "Build project success", "Test scripts success", "check-copyright success", "cla/google success".
  - That CI cannot compile the linked proof. FC builds its own repo at Lean v4.33.1 / Mathlib `0df444a`, while the proof needs Lean v4.34.1, Mathlib `d13f23b` and OpenAI's library with 23 patches.
  - The `formal_proof` attribute is a URL string. Grepping all 8 workflow files for `formal_proof`, `clone` or `curl` finds only the welcome-comment text ("longer proofs are welcome to be included/linked via the `formal_proof` mechanism") and unrelated curl calls (actionlint download, label API).
- **So "FC marks 181 solved" is the formalizer's own PR, approved on trust by a maintainer who had earlier opened an AI-assisted issue asking for exactly that change.**
- FC's `update_erdosproblems.yml` ("Notify erdosproblems of update") dispatches to the erdosproblems site, so this flag may propagate there.

### B5. openai/math (gh api)

- Repo created 2026-10-06T21:47:02Z, `has_issues: false`, `has_discussions: false`. There is exactly one PR ever, #1 by `dr-openai`, "Update manuscripts and Lean formalizations" (merged as `fd4aeeb2`, 2026-10-08T05:20Z). **No issue or discussion about family 171 can exist.** `search/issues?q=repo:openai/math+hypercube` / `+Ramsey` / `+181` all return `total_count 0`.
- **The preprint was never revised.** `commits?path=preprints/The-hypercube-Ramsey-number-has-linear-order-September-23-2026/paper.pdf` and the whole directory both return only `adc7f124 2026-10-06T21:58:50Z Initial commit`. The 10-07 update did not touch it. Our copy matches blob `aac972f5…` byte for byte.
- The directory also ships LaTeX source (`build/main.tex`, `references.tex`, `sections/*.tex`). See Objection 4 for an orphan section file.
- CONTENTS.md entry "**171. The hypercube Ramsey conjecture.**" has **no "(Lean)" link**. There is no `lean/docs/171.md` (404). `lean/formalization.yaml` has no hypercube entry. `history.md` (the 10-07 withdrawals/revisions log) does not mention 171, hypercube or Ramsey. `reasoning_traces/` (11 files) has no trace for this paper.
- **OpenAI's Lean library at adc7f12** contains exactly one hypercube-Ramsey file, `lean/OAI/Combinatorics/Ramsey/Hypercube.lean` (287 lines, only commit `adc7f124`). Header: "Finite Ramsey bounds, cross-edge colorings, and counterexample sequences for a *proposed* linear hypercube Ramsey bound."
  - Its strongest hypercube statement is **`elementary_cube_bounds`: `2 ^ n ≤ ramseyNumber (cube n) ∧ ramseyNumber (cube n) ≤ 2 ^ (2 ^ n + 2 ^ n)`**, i.e. 2^n ≤ R(Q_n) ≤ 4^{2^n}, plus `ramseyNumber_cube_zero`.
  - The rest is the Lemma 2.1 reduction `counterexample_sequence_of_not_linear`: from ¬∃C, it constructs d_k → ∞, N_k = (k+1)·2^{d_k} (so N/2^n = k+1 → ∞, with no rate beyond that), N_k ≤ d_k 2^{d_k}, and cross colourings of two N_k-sides with no monochromatic Q_{d_k} in either colour.
  - **Theorem 1.1 is not in OpenAI's library.** Grep for `ramseyNumber`/`hypercube`/`def cube` over the library finds only this file among hypercube-Ramsey material; the other hits are unrelated cubes/Ramsey (CycleClique, SparsestCut, etc.).


---

## Verified line by line vs skimmed

**Verified against the primary text (fetched and read):**
- [3] §1, §3 (Lemma 3.3), Lemma 4.3 (page image), p.228 necessary-condition sentence, §7 (scan from renyi.hu)
- [25] Lemma 1 and its proof opening (page images)
- [26] Thms 1.1–1.3, the paragraph after Thm 1.3, §2 in full, §7 remark (arXiv v2)
- [7] Thm 4.1, Cor 4.2, Lemmas 4.3–4.7, proof of Lemma 4.5 (arXiv v2)
- [14] Cor 1.2, Cor 1.3, Lemmas 2.1–2.2 (arXiv v2)
- [6] Introduction and Thm 1.1, subcube-vector convention (arXiv v2)
- [12] Thm 1.1 (v1); [13] Thm 1.1 and initial-subcube convention (v1); [29] Thm 1.2, Cor 1.4 (v1)
- [34] Abstract, §1 obstruction, Thm 1.1, Cor 1.2, Remark 1.3, outline, section titles: v3, diffed against v1/v2 (v1/v2 statements also read)
- [18] Thm 1 and Cor 1 (Graham's posted PDF)
- [33] §2 Lemma 2.1 and its proof
- [17] §4 Lemma 11 and its proof (Gowers's posted PS, rendered to text with Ghostscript -dSAFER)
- Every DOI's resolution and Crossref record; zbMATH for [1], [2], [3], [9], [11], [15], [18], [24]; all arXiv version blocks
- My own checks of the §1.1 arguments (lower bound, Gray code, Cartesian embedding, arithmetic)

**Secondary or partial:**
- [4] CRST: via [25]'s introduction and Beck's zbMATH review; ScienceDirect 403
- [2] Beck: zbMATH review plus FS/GRR statements; not online
- [31] Shi 2001: publisher abstract plus FS's restatement
- [32] Shi 2007: title, metadata and a truncated abstract only
- [5] Conlon: abstract only
- Journal-version theorem numbering of [26] (Annals) and [34] (EJC): only the arXiv versions were read
- [1], [8]–[11], [15], [16], [19]–[24], [27], [28], [30]: bibliographic only. Their statements as used in §§3–18 belong to the proof referees.

**World state, read directly by me:**
- the cadamcat repo: README, AUTHORS, CITATION.cff, formalization.yaml, docs/verification.md, S03 DESIGN.md, the commit log via API (1,922 commits), and the diffs of 1870de67, 0d0bebc0, 5ca6c52c and 35fa1344
- the user profile and repo list
- JSP PRs #4967 and #4869 and issue #4720
- FC issue #6906, PR #7128 (body, review, timeline, files) and FC's CI workflows and check-runs
- openai/math: repo metadata, the commit history of the preprint path, README, CONTENTS, history.md, formalization.yaml, reasoning_traces, issue search, and `OAI/Combinatorics/Ramsey/Hypercube.lean` in full
- mahrud PR #171

**Read by the search seat**, with spot checks by me (✔): arXiv sweeps, DS1, Lidický–Pfender, erdosproblems /181 and blog:10, teorth yaml, Tao blog, MathOverflow, Hacker News, Mathstodon, press.

**Not checked:** the proof itself (§§2–18, App. A beyond reading it for architecture); the Lean build.

## Verdict for my scope

- **§1.1–1.2: HOLDS AS READ.** The four objections are cosmetic.
- **Bibliography: 34/34 exist, no fabricated detail.**
- **COULD NOT CHECK:** the primary text of CRST [4], Beck [2], Shi [32] (paywalled/not online; secondary sources agree), and journal-version numbering for [26] and [34].
