# Referee report — seat `sources` (family 158, Erdős #508, "The Euclidean plane is not five-colorable")

Seat: sources. Written 2026-10-14 ~21:50Z. Scope (per PROMPTS.md): (1) every reference in the bibliography (pp. 60–62, paper_plain.txt l.3753ff) fetched at the cited version, with a claim-vs-source table, including Reed's manuscript [23] and the paper's footnote 1; (2) the WORLD on 14 Oct 2026 (erdosproblems.com/508, Bloom's 8 Oct post, teorth database, Formal Conjectures 508.lean, public discussion, other 2024–2026 claims, third-party Lean rebuilds); (3) what is novel and what is not.

Everything fetched is saved under `/tmp/oaimath/158/world/` (`src/` primary PDFs+text, `reed/`, `discussion/`, `thirdparty/`, `erdos1070/`, `m0ar/`, `webfetch_captures_2026-10-14.md` for tool outputs that are not files). Scripts: `/tmp/oaimath/158/seats/sources_scripts/`.

---------------------------------------------------------------------------------------------------

## 0. Headline findings

1. **Citations: no MISMATCH found.** Of 33 references, 24 were fetched and checked against the specific claim/locator the paper attaches (MATCH); 4 could only be checked at abstract/secondary level (Falconer [8], Woodall [31], Hadwiger [13] behind ScienceDirect 403 / e-periodica CAPTCHA; Zimmer [32,33] abstracts only); 1 is closed access (Furstenberg [10]: Lemmas 6.6 and 7.2 NOT checked); 3 are classical metadata-only (Crum [3], Følner [9], von Neumann [29]). Every DOI resolves via Crossref to the stated journal/volume/pages. The brief's "Soifer's book pp. 15–19" is in fact the 2003 *Mathematics Competitions* article [24]; pp. 15–19 are journal pages (PDF pp. 18–22) and support the Nelson/Isbell history (MATCH).
2. **Footnote 1 (Reed [23]) is correct, and understated.** Reed's May manuscript (GitHub AEjonanonymous/Hadwiger-Nelson, PDF blob present since 2026-05-13T19:50Z, also Zenodo 10.5281/zenodo.20149767) claims the "irrationality of 2π ... strictly bounds the angular density of any unit-safe color set below π/3", and its Lean theorem `coloring_collision` takes `h_safe : ∀ i, SafeDensity r (C.color i)` (i.e. that bound) **as a hypothesis**. The half-open arc [0, π/3) has measure π/3 and no unit pair (verified exactly, with failing controls, §2). In fact three alternating arcs give a unit-pair-free subset of the unit circle of measure **π**, and for radius r < 1/2 the whole circle (2π) is unit-pair-free. A third party (github kooshi/AEJonanon-HN-FALSE, 6 Oct 2026) has a Lean audit proving the hypothesis is never satisfiable for r ≥ 0 and false at Reed's own radius 1/√3.
3. **Uncited precursor (citation gap, not a proof gap).** Definition 1.2 ("weak measurable k-coloring") is exactly a partition into *independent sets of the convolution operator A_ω* (ω = normalised surface measure on S^{n−1}) of Bachoc–DeCorte–de Oliveira Filho–Vallentin, *Spectral bounds for the independence ratio and the chromatic number of an operator*, Israel J. Math. 202 (2014) 227–254 (arXiv:1301.1054), Definition 2.1 + §§2.4, 3.1, 3.4. The paper does not cite it. Raised publicly by JoshuaZ (LessWrong, 10 Oct). What *is* new is Theorem 1.3, not the definition.
4. **The brief's world-premise is out of date: the Lean HAS been publicly rebuilt by third parties, and there IS (thin) expert reaction.** (a) `carlostoledo1891/cert-machine` (GitHub Actions runs 38019899278 / 38050007619, committed 2026-10-10): comparator on `EuclideanFiveColor`, "Lean default kernel accepts the solution", "nanoda kernel accepts the solution", strict mode (all definitions compared body-and-all) okay, and a red control (ProperColoring body replaced by sorry → "Type mismatch") rejected. (b) `decalion89/chromatic-number-of-the-plane` (9 Oct): all 70 modules of the Five.lean closure compiled from source at openai/math fd4aeeb2 ("70 built, 0 failed"), `leanchecker` replay, plus a Lean transport of the theorem to Formal Conjectures' `χ(ℝ²)` statement. (c) Li–Su (arXiv:2610.15424, repo daizisheng/erdos-1070): compiled the BorelTransfer closure from source and `leanchecker`-replayed it (transfer half only). (d) plasma-ai/erdos claim card (7 Oct): "kernel-checked Lean proofs were built and axiom-audited here". I did not run any of these; they are the repos' own claims, with logs in the repos. The M0-AR repo's "No Lean rebuild performed here" is true of that repo only. **No one has published a human referee report of the 62-page argument**; the expert reactions (Zelinsky, JoshuaZ, Rybin, Kalai, Davies, MathOverflow) are impressions, a citation complaint, a report, a competing paper, and a question.
5. **Formal Conjectures now marks `6 ≤ χ(ℝ²)` "research solved"** (`HadwigerNelsonAtLeastSix`, PR #6898 by maintainer mo271, merged 2026-10-11, formal_proof link to openai/math Five.lean#L124). Its stated checks were "source inspection", grep for `sorry`, and comparator-config inspection — not a rebuild, and the ℂ → `EuclideanSpace ℝ (Fin 2)` / "no 5-colouring → 6 ≤ chromaticNumber" transport is not among the "routine transports" the PR lists (decalion89 supplies it in Lean). erdosproblems.com/508 and the teorth database still say open, 5 ≤ χ ≤ 7, 0 proof claims.
6. **Concurrent independent work changes the novelty picture of Theorem 1.3.** James Davies, *Measurable obstructions for unmeasurable colourings*, arXiv:2610.12301 (8 Oct 2026, two days after the release), proves χ(ℝ⁴) = χ_m(ℝ⁴) and, for d ≥ 5, χ(ℚ^d) = χ(ℝ^d) = χ_m(ℝ^d) — the measurable/unrestricted coincidence in high dimension, by a different (lattice/radial-inequality) method; he hopes to reach d = 2, 3, conjectures χ(ℝ²) = 6, and writes "Due to the very recent release of [53] by OpenAI, we have posted this paper slightly earlier than we would have liked." He does not assess the OpenAI proof.
7. **Test (A) from the sources' side** (§7): Payne's exact statement is χ(Tℚ²) = 2 while χ_m(Tℚ²) ≥ 5. A rational-field run of §§2–4 would even contradict an elementary bound (a Li–Su-type single-class version would produce a measurable unit-distance-free set of density ≥ 1/2 > 2/7). So the Haar rigidity theorem (Thm 2.3) must FAIL over (ℚ(i), rational circle). The paper's text names the property the rational circle lacks: Lemma 2.4's proof, PDF p. 7: "The action on this finite orbit gives a finite image of the divisible abelian group K. Such an image is trivial: a finite abelian group cannot be divisible unless it is trivial." (ℚ(i)'s unit circle is not divisible: (3+4i)/5 = ((2+i)/√5)² has no square root in ℚ(i).) Also Lemma 2.7 ("The square roots belong to F", l.735) and Lemmas 3.2/3.3 (surjective power maps, l.295–297, 922–923, 1211). A third party (decalion89, notes/six_over_fields.md) lists exactly these uses and claims a Lean-checked rerun of the whole proof over the *constructible* numbers (square roots only). This is consistent with the transfer using something the rational graph lacks; the rigidity seat must confirm the mathematics.
8. **Novelty, in one line each** (§8): χ(ℝ²) ≥ 6 — new (no prior or competing claim; Reed's χ = 7 is void). Theorem 1.4 *alone* gives χ_m(ℝ²) ≥ 6 — the first improvement on Falconer's 1981 measurable bound (the paper does not say this). Theorem 1.3 "⇒" — new in d = 2 as far as anyone has found (Xie, JoshuaZ, Zelinsky, my searches), but concurrent with Davies's d ≥ 4 theorem. Theorem 1.3 "⇐", Definition 1.2, the invariant averaging, the interface exclusions, the Moser spindle, the hexagon — not new (mostly acknowledged; Definition 1.2 not).

---------------------------------------------------------------------------------------------------

## 1. Citation table (claim vs source)

Locators: "l." = line in paper_plain.txt; quotes from the PDF where it matters. Source text quoted from the fetched file named.

| [n] | where / what the paper says | what the source says (quoted) | verdict |
|---|---|---|---|
| [1] Bekka–de la Harpe–Valette, manuscript 23 Feb 2007 (`src/bekka.pdf`, 523 pp, title page "February 23, 2007") | l.366 G.2.1 for an invariant mean on abelian F/ℤ; l.424 D.2.2 Bochner; l.1451 D.3.1 SNAG + D.2.2; l.1486 G.2.1, G.2.2(ii) amenability of E⋊K, G.5.1 Følner | "Theorem D.2.2 (Bochner) Let ϕ be a continuous function of positive type … There exists a finite positive Borel measure µ on Ĝ such that µ̂ = ϕ"; "Theorem D.3.1 (SNAG Theorem) (i) Let (π, H) be a unitary representation of the locally compact abelian group G. There exists a unique regular projection valued measure …"; "Theorem G.2.1 (Markov-Kakutani) Every abelian topological group G is amenable."; "Proposition G.2.2 … (ii) Let N be a closed normal subgroup of G. If N and G/N are amenable, then G is amenable."; "Theorem G.5.1 … (i) G is amenable; (ii) (Følner's Property) …" | MATCH (all five locators) |
| [2] Bourgeat–Heinrich–Melotti–Robert, arXiv:1501.02441v1 | Cor 1.5(ii), l.251–253: periodic and asymptotic "needle frequencies … are bounded below by the minimum monochromatic-edge fraction of H … by Bourgeat et al. [2, Theorems 1–2]"; l.118 "invariant randomization and finite-graph compactness" | Def. 1: "A k-coloring of the plane is a measurable function"; "Theorem 1. … sup_{g∈G} m_k(g) ≤ inf_{c∈C_k^per} p_per(c) ≤ 1/k"; "Theorem 2. … asymptotic k-colorings … sup m_k(g) ≤ inf p(c)"; Def. 3 is the conditional square-table probability given B_R ∈ [−R,R]²; proof uses "Theorem 3 (De Bruijn - Erdős)" | MATCH (measurability, periods, table frequencies all as in Cor 1.5(ii)) |
| [3] Crum 1956 (Crossref: PLMS s3-6(4):548–560) | l.336 "[3, 11]" measurable radial p.d. = continuous + c·1_{0} | full text not fetched; OpenAlex abstract fragment only ("LET p(x) be … 'positive-definite' if …") | metadata MATCH; content via [11] |
| [4] de Bruijn–Erdős 1951 (`src/debruijn_erdos_1951.pdf`, renyi.hu) | l.26, 246, 1618 "[4, Theorem 1] says that a graph is k-colorable, for fixed finite k, if and only if every finite subgraph is k-colorable" | "Theorem 1. Let k be a positive integer, and let the graph G have the property that any finite subgraph is k-colourable. Then G is k-colourable itself." ("The Axiom of Choice is adopted throughout the paper.") | MATCH (paper cites pp. 371–373; reprint shows p. 372; Payne cites 369–373 — cosmetic) |
| [5] de Grey arXiv:1804.02385v3 | l.21–22 "constructed a finite unit-distance graph that is not four-colorable in 2018. His corrected construction has 1,581 vertices." | v3 abstract: "The smallest such graph that we have so far discovered has 1581 vertices." v1 abstract (abs page): "… has 1567 vertices."; v2 (11 Apr 2018): 1581. Secondary (de Grey's account quoted on LessWrong/GreaterWrong; Elkies/Aaronson): the 1567-vertex graph came from a bug and was 4-colourable | MATCH ("corrected" supported by v1→v2 change + secondary) |
| [6] Deroin–Kleptsyn–Navas arXiv:0806.1974v1 | l.1976 "Sullivan's expanding-action and bounded-distortion strategy; see … [6, Section 2.1]" | §2.1 "Minimality, ergodicity, and exceptional minimal sets", p. 12–13: "To show the ergodicity one then would like to apply the exponential expansion strategy. This classical procedure consists on expanding very small intervals … in such a way that the distortion … of the compositions remains controlled … If the action is minimal, this implies that A is a subset of full measure"; intro: "exponential expansion strategy (largely going back to D. Sullivan)" | MATCH |
| [7] Exoo–Ismailescu arXiv:1805.00157v1 (DCG 64:216–226) | l.24 "gave an alternative proof of the lower bound five" | "We present an alternate proof of the fact that given any 4-coloring of the plane there exist two points unit distance apart which are identically colored." | MATCH |
| [8] Falconer 1981 JCTA 31(2):184–189 | l.31 "Falconer [8] proved χ_m(ℝ²) ≥ 5 using density points and rotations"; l.1582 density-point method | ScienceDirect 403 from exe.dev and Hetzner; Elsevier API needs key; publisher elides abstract. Secondary: Payne: "In 1981 Falconer showed that χ_m(ℝⁿ) ⩾ n + 3 [7]", and Payne's adaptation uses density points (S̃), Croft's rigid-motion lemma ("almost all rotations … of m(C) about m(x)") and Falconer's circle lemma; Sokolov–Voronov 2025: "Falconer [6] proved the lower bound, 5 ≤ χ_mes(ℝ²) ≤ 7" | COULD NOT FETCH primary; secondary MATCH |
| [9] Følner 1955 Math. Scand. 3:243–254 | l.370 origin of the finite-set averaging criterion | metadata only (Crossref) | metadata MATCH; content not read |
| [10] Furstenberg 1977 J. Anal. Math. 31:204–256 | l.135, 828–830 "[10, Lemmas 6.6 and 7.2]" (HS kernels → finite-rank modules; bounded bases in ergodic case); l.925 van der Corput | closed access (Springer; no OA copy per OpenAlex) | COULD NOT FETCH — the two lemma locators are UNVERIFIED |
| [11] Gneiting–Sasvári 1999 Math. Geol. 31(1):105–111 | l.336 | Springer abstract (via search): "any measurable, isotropic covariance function on ℝ^d (d ≥ 2) admits a decomposition as the sum of a pure nugget effect and a continuous covariance function" | MATCH (abstract level; Crossref confirms 31(1):105–111) |
| [12] Gwyn–Stavrianos arXiv:2008.07987v1 | Cor 1.5(i), l.249–251 "every normalized finitely additive left-invariant measure µ on all subsets of … E(2)", "mp₅(c) ≥ 1 … the finite-graph bound of Gwyn and Stavrianos [12, Lemma 2.10 and Theorem 2.11]"; l.151 "invariant-mean notion of monochromatic-pair frequency" | "Lemma 2.10. If a given finite unit-distance graph G = (V, E) is not k-colorable, then p_k ≥ 1/|E(G)|."; "Theorem 2.11. If χ(ℂ) > k, then p_k ≥ 1/N for some N ∈ ℤ⁺."; p_k(c) = µ_T({T* : b_{c∘(T*)^{-1}}(0,1) = 1}) with µ_T "a finitely additive measure … invariant … on both sides" | MATCH. Note: G–S fix a bi-invariant µ_T; the paper states (i) for every *left*-invariant µ. Their proof (E[B] = |E(G)|·p_k(c) "by … isometry invariance") only uses µ(T₀S) = µ(S), so the generalisation is valid (COSMETIC) |
| [13] Hadwiger 1961, Elem. Math. 16:103–104 | l.18 "asks for a covering by sets that avoid unit distance and gives the bounds four and seven"; l.85 hexagonal construction | e-periodica PDF behind CAPTCHA ("Verification required") from exe.dev and Hetzner; TOC (WebFetch) confirms an "Ungelöste Probleme" section at Heft 5, p. 103. Secondary, Soifer 2003 p. 17: "in 1961 the famous Swiss geometer Hugo Hadwiger published ([19]) the chromatic number of the plane problem together with proofs of both inequalities … 'We thank Mr. V. L. Klee … The problem is due to E. Nelson; the inequalities are due to J. Isbell.'"; p. 19: "the same hexagonal 7-coloring of the plane that Hadwiger published in 1961" | COULD NOT FETCH primary; bounds/hexagon MATCH via Soifer; the "covering by sets" wording UNVERIFIED |
| [14] Hatcher, Algebraic Topology (`src/hatcher_AT.pdf`) | l.2901 "Brouwer fixed point theorem, in its planar form [14, Theorem 1.9]"; l.2948 "[14, Section 1.A]" reduced paths | "Theorem 1.9. Every continuous map h : D² → D² has a fixed point"; contents "1.A. Graphs and Free Groups 83" | MATCH |
| [15] Heule arXiv:1805.12181 (only v1 exists) | l.23 "used satisfiability proofs and extraction of unsatisfiable cores to obtain 553-vertex examples" | "Our method, which is based on clausal proof minimization, allowed us to compute several 553-vertex unit-distance graphs with chromatic number 5"; "checkers can extract from a refutation an unsatisfiable core" | MATCH |
| [16] Jamneshan ETDS 43(7):2404–2436 (2023) | l.136 "the corrected modern account of Jamneshan [16, 17] supplies further context"; l.828 FZ structure | abstract (OpenAlex/arXiv:2103.17167v4, 27 Sep 2025): "establish a Furstenberg–Zimmer structure theory in full generality" | MATCH (cited as context only) |
| [17] Jamneshan Corrigendum ETDS 46(1):211–217 (2026) (`src/jamneshan_corrigendum.pdf`) | as above | "Ergod. Th. & Dynam. Sys., (2026), 46, 211–217 … Lemma A.5 and Proposition A.6 in the Appendix … are incorrect. These results were used in the proof of Lemma 4.4 … Second, the proof of the implication (iii) ⇒ (iii)′ in Lemma 4.10 is incorrect. We supply a new argument" | MATCH. The paper gives its own tower (Lemma 3.1) and does not rest on Jamneshan's Thm 4.1, so the corrected errors do not propagate |
| [18] Matolcsi–Ruzsa–Varga–Zsámboki arXiv:2311.10069v4 | l.118–119 "Følner averaging over countable groups of plane isometries"; "Version 4, March 27, 2025; first submitted November 16, 2023" | abs history: "[v1] Thu, 16 Nov 2023 … [v4] Thu, 27 Mar 2025"; text: "Consider the group K of Euclidean transformations generated by T. Clearly, K is countable and solvable … all amenable groups have the Følner property. As such, there exists a sequence of sets R_k ⊆ K" | MATCH (dates exact) |
| [19] L. Moser & W. Moser, CMB 4(2):187–189 (`src/moser_1961_solutions.pdf`) | l.19 "seven-point construction … particularly small finite obstruction to three colors" | "P 10. … (b) Show that in (a) six cannot be replaced by seven. L. Moser and W. Moser … Fig. 2 exhibits a configuration of 7 points which cannot be 3-colored." (pp. 187–189) | MATCH |
| [20] Parts arXiv:2010.12661 | l.25 "Parts gave a human-verifiable proof" | "We present a new proof of the known fact that the chromatic number of the plane is at least 5. The main difference of this proof is that it can be verified manually without the help of the computer." | MATCH |
| [21] Parts arXiv:2010.12665v2 | l.23–24 "obtained a 509-vertex graph" | "minimize 5-chromatic unit-distance graphs and obtained a graph with 509 vertices and 2442 edges." | MATCH |
| [22] Payne EJC 16 #N31 (`src/payne_2009.pdf`) | l.32–34 "developed this method for translation-invariant unit-distance subgraphs. In particular, the graph on all of ℝ² whose edges have rational unit displacement vectors is two-colorable, while every measurable coloring requires at least five colors."; l.1582 "[22, Lemma 1 and Proposition 1]" | "the edge set of TKⁿ is invariant under real translations"; "Lemma 1. Let S be a measurable set which is admissible as a colour set for TKⁿ and suppose that x ∈ ℝⁿ is at unit distance from a point in S̃. Then d_S(x) = 0."; "Proposition 1. … χ_m(TKⁿ) ⩾ χ(ℝⁿ)"; "In the most famous case of the plane we have χ(Tℚ²) = 2 while χ_m(Tℚ²) ⩾ 5." | MATCH |
| [23] Reed, May 14 2026 manuscript (`reed/reed_2026-05.pdf`, sha1 a7a9aeb8…) | footnote 1, p. 2 | see §2 | MATCH (footnote correct) |
| [24] Soifer 2003, Math. Competitions 16(1):9–41 (`src/soifer_2003.pdf`; printed page = PDF page − 3) | l.16–18 "The problem dates to Edward Nelson in 1950. Nelson obtained the lower bound four, and John Isbell found the upper bound seven … recounted by Soifer [24, pp. 15–19]" | p. 19: "Now we can finally give a due credit to Edward Nelson for being first in 1950 to prove the lower bound 4 ≤ χ."; "John Isbell was first in 1950 to prove the upper bound χ ≤ 7. He used the same hexagonal 7-coloring" | MATCH (the brief's "book" is this article) |
| [25] Sokolov–Voronov arXiv:2502.01958v1 | l.39–41 "proved a lower bound seven for polygonal colorings in a locally finite map framework. Their interface argument excludes both adjacent colors wherever distances to the interface take values both below and above one"; l.176 "[25, Propositions 1–2]"; l.3097 "[25, Proposition 9]" strips | "Theorem 2. There is no polygonal coloring of the plane in 6 colors, i.e. χ_poly(ℝ²) = 7." ("any bounded region must contain a finite number of polygons"); "Proposition 2. Let u and v lie on the boundary of two monochromatic regions. Then, no point z satisfying ‖z − u‖ < 1, ‖z − v‖ > 1 can be colored with either of the two colors of these regions."; "Proposition 9 … the segment of this ray … is colored in colors 1, 2, 3." | MATCH |
| [26] Tao, 254A Lecture 9 (WebFetch) | l.505 disintegration "concentrated on π⁻¹(y) … unique almost everywhere; see Tao [26, Theorem 4 and Remark 5]" | Thm 4: X regular (compact metrisable model), kernel y ↦ µ_y, g∘π = g(y) µ_y-a.e., "unique up to ν-almost everywhere equivalence"; Rem 5: regular = standard Borel | MATCH |
| [27] Townsend 1981 JCTA 30(1):114–115 (`src/townsend_1981.pdf`, via Hetzner) | l.38–39 "Townsend corrected Woodall's argument for a six-color lower bound in the planar-map setting, announcing the repair in 1981" | "Woodall [3] proves that an infinite planar map requires at least six colours … Unfortunately it is possible to construct a counter-example to the assertion … The theorem is still correct, and by replacing the above assertion with the following lemma it is possible to construct a proof" | MATCH |
| [28] Townsend 2005 Geombinatorics 14(4):184–193 (`src/townsend_2005.pdf`) | "giving its details in 2005"; l.3295 "Townsend's annulus argument [28, Theorems 1 and 4]" | "This paper was written in 1979 but never published. A summary … appeared as a note in … J. Comb. Theory (A), 30, 1 (1981)"; "THEOREM 1 Let A⁰ be a finitely disconnected unit annulus … Then any 2-colouring of A⁰ contains a monochrome unit."; "THEOREM 4 If a 5-colouring of E² contains three disjoint, differently coloured, bounded, open, connected, monochrome sets … all three having one common boundary point, then E² contains a monochrome unit." | MATCH |
| [29] von Neumann 1929 Fund. Math. 13:73–116 | l.370 | metadata only | metadata MATCH |
| [30] Voronov arXiv:2304.10163v3 | l.3098 "[30, Sections 3–5], for a positive interval of forbidden distances"; "Version 3, submitted April 13, 2025; first version April 20, 2023" | history "[v1] Thu, 20 Apr 2023 … [v3] Sun, 13 Apr 2025"; §3 "Colorings of the circle", §4 "Coloring of complementary arcs", §5 "Chromatic number of the bicycle" | MATCH |
| [31] Woodall 1973 JCTA 14(2):187–200 | l.38 "studied distance-avoiding closed covers and region decompositions" | ScienceDirect 403; secondary: Townsend 1981 (quoted above); SV 2025: "Woodall (1973) and Townsend (1981) showed that at least 6 colors would be required" | COULD NOT FETCH primary; secondary MATCH |
| [32] Zimmer IJM 20(4):555–588; [33] IJM 20(3):373–409 | l.135, 828 compact-extension method | Project Euclid PDFs blocked; OpenAlex abstracts: "extensions with relatively discrete spectrum … generalized discrete spectrum"; "extensions in the theory of ergodic actions of a locally compact group" | MATCH (abstract level) |

**Omitted references that a referee would require:**
- Bachoc–DeCorte–de Oliveira Filho–Vallentin 2014 (above): Definition 2.1 "A measurable set I ⊆ V is called an independent set of A if (Af, f) = 0 for each f ∈ L²(V) which vanishes almost everywhere outside of I"; §3.1 convolution operator A_ν f = f ∗ ν; §3.4 "Let N be the unit sphere S^{n−1} … the rotationally invariant probability measure ω on S^{n−1}". With f ≥ 0 and ν ≥ 0, independence of I for A_ω is equivalent to ∫∫ 1_I(x)1_I(x+u) dσ(u) dx = 0, i.e. Definition 1.2's condition for one class; their χ(A) (§2.4: "the smallest number k such that one can partition V into k independent sets") is the weak measurable chromatic number. Their Theorem 2.3 (Hoffman-type) already gives this number ≥ 4 in the plane.
- Székely (1984), whose conjecture that χ and χ_m differ (Davies: "Székely [70] conjectured that the ordinary and measurable chromatic numbers of Euclidean spaces can differ") is the question Theorem 1.3 bears on; and Shelah–Soifer (2003, 2004) on axiom-dependence (§6). Neither is cited.

## 2. Footnote 1 vs Reed's manuscript — exact check

Footnote 1 (PDF p. 2, verbatim): "The May 14, 2026 manuscript of Reed [23] announces χ(ℝ²) = 7 through a circle-density argument. Its proposed strict bound of π/3 on the angular measure of a unit-independent subset of the unit circle fails for the half-open arc {e^{it} : 0 ≤ t < π/3}: this arc has angular measure π/3 and contains no unit pair. The displayed formal theorem assumes that density bound as a hypothesis, so the argument does not establish the announced equality."

Reed (fetched: GitHub HEAD PDF, blob 002a63db; per-commit file lists, only three commits ever touched the PDF: 18eb846d added it 2026-05-13T03:22Z, f5146155 deleted it and abcd3aec re-added the current version 2026-05-13T19:50Z; so the version present on 14 May is the one fetched. Later commits touch README, llms.txt, the .lean file, lake files and a 5 Oct comparator directory). Abstract, verbatim: "we formally verify that the irrationality of 2π relative to the unit chord length introduces an unavoidable phase drift that strictly bounds the angular density of any unit-safe color set below π/3." Lean, verbatim:
```
def SafeDensity (r : ℝ) (S : Set (EuclideanSpace ℝ (Fin 2))) : Prop :=
   is_unit_safe S → color_measure r S < π / 3
theorem coloring_collision (r : ℝ) (C : SixColoring r) (h_safe : ∀ i, SafeDensity r (C.color i)) :
   (∑ i, color_measure r (C.color i)) < 2 * π
```
So (i) the bound is stated for any unit-safe set on a circle of radius r (the unit circle is the r = 1 instance), (ii) it is a hypothesis `h_safe`, and (iii) the "theorem" proves only six numbers < π/3 sum to < 2π. Footnote 1 is correct on all three counts. It understates the failure: on the unit circle a unit-pair-free set can have measure π, and for r < 1/2 the whole circle is unit-pair-free. kooshi's Lean audit (`reed/kooshi_AUDIT.md`): "(a) The theorem applies to nothing … (b) The assumed bound is false … At radius 1/4 the whole circle is such a set, and its measure is 2π … At the paper's radius 1/√3 an arc of 120° is such a set".

Script (`/tmp/oaimath/158/seats/sources_scripts/footnote1_check.py`), verbatim:
```python
# Exact check of footnote 1 (p.2): on the unit circle, two points e^{ia}, e^{ib} are at distance 1
# iff a-b = +-pi/3 (mod 2pi). Work in units of pi/3, so the circle is [0,6) and "unit pair" means a-b in {+-1}+6Z.
# A set is a finite union of intervals given as (lo, hi, lo_closed, hi_closed) with rational endpoints.
from fractions import Fraction as Fr
from itertools import product

def diff_interval(I, J):
    # {a-b : a in I, b in J} is an interval with endpoints I.lo-J.hi, I.hi-J.lo
    (a1, b1, ca1, cb1), (a2, b2, ca2, cb2) = I, J
    lo, hi = a1 - b2, b1 - a2
    lo_closed = ca1 and cb2   # attained iff a=a1 and b=b2 both allowed
    hi_closed = cb1 and ca2
    return lo, hi, lo_closed, hi_closed

def contains(iv, x):
    lo, hi, lc, hc = iv
    return (lo < x < hi) or (lc and x == lo) or (hc and x == hi)

def unit_pairs(S):
    hits = []
    for I, J in product(S, S):
        d = diff_interval(I, J)
        for k in range(-3, 4):
            for t in (Fr(1) + 6*k, Fr(-1) + 6*k):
                if contains(d, t):
                    hits.append((I, J, t))
    return hits

def measure(S):  # in units of pi/3 (assumes disjoint intervals)
    return sum(hi - lo for lo, hi, _, _ in S)

cases = {
  "footnote arc [0,pi/3) (half-open)":            [(Fr(0), Fr(1), True, False)],
  "three alternating arcs [0,1)u[2,3)u[4,5)":      [(Fr(0),Fr(1),True,False),(Fr(2),Fr(3),True,False),(Fr(4),Fr(5),True,False)],
  "CONTROL closed arc [0,pi/3]":                  [(Fr(0), Fr(1), True, True)],
  "CONTROL arc [0,pi/2) (too long)":              [(Fr(0), Fr(3,2), True, False)],
  "CONTROL [0,1)u[2,3)u[4,5]  (last closed)":     [(Fr(0),Fr(1),True,False),(Fr(2),Fr(3),True,False),(Fr(4),Fr(5),True,True)],
}
for name, S in cases.items():
    h = unit_pairs(S)
    print(f"{name:45s} measure = {measure(S)}*(pi/3)   unit pair present: {bool(h)}" + (f"   e.g. difference {h[0][2]}*(pi/3)" if h else ""))

# numeric sanity: sample the half-open arc densely, max chord length must stay < 1
import math
N = 20000
pts = [i*(math.pi/3)/N for i in range(N)]   # t in [0, pi/3)
mx = max(2*math.sin(abs(pts[-1]-pts[0])/2), 0)
print("numeric: max chord in sampled half-open arc =", mx, "(<1:", mx < 1, ")")
```
Output:
```
footnote arc [0,pi/3) (half-open)             measure = 1*(pi/3)   unit pair present: False
three alternating arcs [0,1)u[2,3)u[4,5)      measure = 3*(pi/3)   unit pair present: False
CONTROL closed arc [0,pi/3]                   measure = 1*(pi/3)   unit pair present: True   e.g. difference 1*(pi/3)
CONTROL arc [0,pi/2) (too long)               measure = 3/2*(pi/3)   unit pair present: True   e.g. difference 1*(pi/3)
CONTROL [0,1)u[2,3)u[4,5]  (last closed)      measure = 3*(pi/3)   unit pair present: True   e.g. difference -5*(pi/3)
numeric: max chord in sampled half-open arc = 0.9999546546732045 (<1: True )
```
The three controls (closing one endpoint, lengthening the arc) are rejected, so the checker can fail. Verdict on footnote 1: **correct**.

## 3. Other finite check in scope: the hexagonal 7-colouring (p. 2–3, attributed to Hadwiger [13])

Script `/tmp/oaimath/158/seats/sources_scripts/hexagon_check.py` (verbatim in that file) checks with exact rationals: 2r < 1 and (√21 − 2)r > 1 (as 21r² > (1+2r)²), |2 − ω|² = 7, the minimal nonzero norm of (2 − ω)ℤ[ω] is 7 (so same-colour centres are √7·√3 r = √21 r apart), and the index is 7 (coset count). Output:
```
r=2/5: 2r<1 True, (sqrt21-2)r>1 True <- paper's choice
r=1/2: 2r<1 False, (sqrt21-2)r>1 True (control)
r=3/8: 2r<1 True, (sqrt21-2)r>1 False (control)
r=39/100: 2r<1 True, (sqrt21-2)r>1 True (control)
|2-w|^2 = 7
smallest nonzero norms in (2-w)Z[w]: [7, 21, 28, 49] -> min distance sqrt(7) in lattice units; times spacing sqrt(3) r = sqrt(21) r
number of cosets of (2-w)Z[w] in Z[w]: 7
```
r = 1/2 and r = 3/8 fail, as they should (the valid window is 1/(√21−2) ≈ 0.387 < r < 1/2). The upper-bound paragraph is correct.

## 4. The WORLD on 14 Oct 2026

**erdosproblems.com/508** (`live/live_508*.txt`, fetched 14 Oct via Hetzner). Bounds line, verbatim: "The best bounds currently known are\[5 \leq \chi \leq 7.\]The lower bound is due to de Grey [dG18]." "Proof claims (0)"; claims page: "No proof claims have been submitted yet."; "This page was last edited 22 January 2026."; one comment (BorisAlexeev, 27 Oct 2025, on Erdős's "F(2) ≤ 6" in [Er75f]); forum page: "The ability to post new comments has been suspended." (the same notice is on Bloom's blog thread — site-wide, which partly explains the silence there).

**Bloom, 8 Oct 2026, "Erdős problems in the OpenAI proofs"** (`world/bloom_blog10_2026-10-08.html`; thread re-fetched 14 Oct). #508 paragraph, verbatim: "Problem [508] - Chromatic number of the plane This PDF claims a proof of the following. In any $5$-colouring of $\mathbb{R}^2$ there are two points the same colour which are distance $1$ apart. This is known as the Hadwiger-Nelson problem; it implies the chromatic number of the plane is $6$ or $7$. This proof has been formalised. THe PDF is 62 pages long." FrontierMath list, verbatim: "… [431] , [508] (partial), [821] …". Disclaimer: "I have also not, where a Lean formalisation is provided, yet checked myself that the formalisation compiles or that the statement in the challenge file accurately captures the problem." The 10 comments on the post as of 14 Oct concern #184, #986, #304/#293/#148, #416, #3 — **none mentions #508**. "(partial)" is explained by FrontierMath Erdős (arXiv:2609.25050 §3.2): #508 is encoded as three mutually exclusive conjectures `Erdos508.eq5/eq6/eq7`; the claim refutes eq5 only.

**teorth database**: `~/ErdosProblemADay-main/src/tracker_data.js` (generated 2026-10-14 from teorth 86c3dc3e of 2026-10-13): `"508":{"s":"open","lu":"2025-08-31","pr":"","tg":["geometry","ramsey theory"],"oe":[],"fz":1,"cm":"Hadwiger-Nelson problem"}`. Live `teorth/erdosproblems` `data/problems.yaml` (main, fetched 14 Oct): status "open", last_update "2025-08-31"; formalized "yes" (2025-12-09).

**Formal Conjectures `ErdosProblems/508.lean`** (main, fetched 14 Oct; `world/formal_conjectures_508.lean`): docstring "It is known that $6 \leq \chi(\mathbb{R}^2) \leq 7$"; `HadwigerNelsonProblem : χ(ℝ²) = answer(sorry)` still `research open`; `HadwigerNelsonAtLeastSix : 6 ≤ χ(ℝ²)` tagged `@[category research solved, AMS 52, formal_proof using lean4 at ".../adc7f124.../lean/OAI/Geometry/PlaneColoring/Five.lean#L124"]`, docstring "This was proved by an internal OpenAI model in September 2026 [OAI26]". History: PR #6819 (8 Oct, AtLeast4 link), PR #6898 (by mo271, merged 2026-10-11, approved by Paul-Lez): "Left open on purpose: Hadwiger–Nelson (only 6 ≤ χ ≤ 7 is proved)"; "Checked: … every proof link resolves to a `theorem` in the release at the pinned commit (source inspection); the release's Lean library contains no `sorry` (grep), and each comparator config permits only `propext`, `Quot.sound`, `Classical.choice` (config inspection)." No review comment in the PR discusses #508.

**openai/math state**: the paper, `EuclideanFiveColor.lean`, and the three Lean directories have exactly one commit, adc7f1241b (2026-10-06T21:58Z) — per-path commit history, with a positive control (CONTENTS.md shows both commits). The 8 Oct "Update manuscripts and Lean formalizations" did not touch family 158.

**Public discussion found (all of it):**
- Joshua Zelinsky (Bluesky, 2026-10-06T23:03Z, reply under Zach Weinersmith): "I've only had time to start looking at the chromatic plane proof, and it doesn't look like the method is a direction that the prior lit used to my knowledge. This is far beyond merely building on existing methods or seeing connections between different problems." (thread JSON `discussion/bsky_zelinsky_*.json`)
- JoshuaZ (LessWrong comment, 2026-10-10T17:57Z): "there's been some people who have erroneously concluded from the paper that 'weakly measurable coloring' which the AI defines with not citations is novel. There's a lot of very similar ideas to it in the literature which are not cited, and if I were refereeing the paper I would insist they cite. In particular, there is a 2014 paper of Bachoc, DeCorte, de Oliveira Filho, and Vallentin. … The interesting new idea is there Theorem 1.3 … That's a really key ingredient and doesn't seem (to me at least) to have been in the literature." (`discussion/lw_comments*.json`)
- Dmitry Rybin (X, 2026-10-07T15:17Z; 260k views): "I was trying to read the OpenAI proof that chromatic number of a plane is >= 6. But it is totally unbelievable alien math? Somehow the model found that any K-coloring <=> 'weakly measurable' K-coloring, which seems out of nowhere"; follow-up: "ridiculous human-developed machinery … amenable groups, Pontryagin duality, Furstenberg-Zimmer towers".
- Gil Kalai (blog, 7 Oct, "Updates: Sharing AI progress on mathematics (amazing!)"): "The chromatic number of the plane. In 2018 I reported Aubrey de Grey's breakthrough … The new manuscript raises the lower bound to six, leaving six and seven as the two possible answers." (report only; comments do not discuss it).
- James Davies, arXiv:2610.12301 (8 Oct) — see §5.
- Ying Xie, arXiv:2610.17090 (12 Oct, math.HO survey of the release), §8.3.4: "Transfer … The literature since Falconer treats measurable and unrestricted chromatic numbers as possibly different; the claimed transfer equates existence in these two formulations. The initial literature comparison found no matching transfer theorem." Caveats: "The inspected comparator configuration disables the optional nanoda independent kernel recheck; no build was run here. The paper never exhibits a finite 6-chromatic graph".
- Jonathan Davidson, arXiv:2610.09474 (7 Oct): uses the result as input ("In a preprint publicly released on October 6, 2026, OpenAI reports a proof … The preprint obtains the existence of a finite graph that is not five-colorable through compactness").
- MathOverflow Q516012 (13 Oct, score 22, 0 answers), "What is an example of a finite unit-distance graph that isn't 5-colorable?" ("assuming the paper isn't retracted"); comment by Wojowu: "Their proof seems to be nonconstructive in some sense … It is unclear to me how this could be transformed into a more explicit construction"; Gordon Royle: smallest known non-4-colourable is 509 vertices. Math.SE Q5151609 (11 Oct) asks the same; one answer (enumerate algebraic points).
- Terence Tao (blog, 7 Oct, AHM statement, 156 comments) and Scott Aaronson ("The Mathocalypse", 7 Oct): no passage on #508 (Tao page grep: 0 hits outside the sidebar; Aaronson home page per WebFetch: release discussed via UGC and L = BPL).
- Hacker News (Algolia full-text, created after 2026-09-21): "chromatic number of the plane" 0, "Hadwiger-Nelson" 0, "Hadwiger Nelson" 0, "five-colorable" 0, "weakly measurable coloring" 0; positive controls: same queries without the date filter return 27/6/7/2/2 older hits, and "chromatic" since 5 Oct returns 12 unrelated hits (index covers the period). Reddit: API blocked from exe.dev and WebSearch refuses reddit.com — COULD NOT SEE. Bluesky search API requires auth — COULD NOT SEE beyond the Zelinsky thread. No reaction found from de Grey, Soifer, Exoo, Heule, Parts, Voronov, Falconer, Oliveira Filho, Vallentin, Matolcsi or Varga (WebSearch extended).

So: the absence is not of *any* reaction but of **any expert verification**. Eight days after release, nobody has publicly checked the human-readable argument, nobody has posted it as a proof claim on erdosproblems.com, and none of the reactions engages Payne's obstruction (test (A)). The ones closest to the subject (Davies, JoshuaZ) treat Theorem 1.3 as the new, key, and unexamined step.

## 5. Other 2024–2026 claims on χ(ℝ²) ≥ 6 or on measurable-vs-unrestricted transfer

arXiv API (abstract searches, saved `world/arxiv_search_results.txt`): "chromatic number of the plane" (17 total; 2024+: 2610.09474, 2606.28157 Dúcz–Varga independence ratio < 1/4, 2606.12325, 2502.01958, 2404.14398), "Hadwiger-Nelson" (26; 2024+: 2610.12301, 2609.36220 typical norms, 2608.04542 Moser-spindle-free 5-chromatic 2131-vertex graph, 2606.16642, 2601.05137, 2512.15516, 2502.01958, 2501.18527, 2404.14398), "measurable chromatic number" (13; 2024+: 2610.13551, 2610.12301, 2606.16642, 2602.05185). **No 2024–2026 paper other than OpenAI's claims χ(ℝ²) ≥ 6.** Reed (Zenodo/GitHub, May 2026) claims χ = 7 and is void (§2).

Transfer results:
- **Davies, arXiv:2610.12301** (Leipzig; ChatGPT 5.6/6.1 Sol acknowledged for parts of the proof). Theorem 1.1, verbatim: "Let D = {d₁,…,d_t} ⊂ (0,∞) be finite and nonempty with d₁²,…,d_t² ∈ ℚ. Then α_D(ℝ⁴) = m_D(ℝ⁴) and χ_D(ℝ⁴) = χ_D^(m)(ℝ⁴), furthermore, for d ⩾ 5, α_D(ℚ^d) = α_D(ℝ^d) = m_D(ℝ^d) and χ_D(ℚ^d) = χ_D(ℝ^d) = χ_D^(m)(ℝ^d)." "We remark that the d ⩾ 5 condition is necessary for the extra conclusion on ℚ^d" (χ(ℚ²) = χ(ℚ³) = 2, χ(ℚ⁴) = 4). "We hope that it will be possible to extend our techniques to dimensions 2 and 3." "Conjecture 1.6. χ(ℝ²) = 6." Bearing: an independent, human-led result that measurable and unrestricted chromatic numbers coincide (fully, not "weakly") in d ≥ 4, posted two days after the release; it does not cover d = 2 and does not evaluate the OpenAI claim.
- **Li–Su, arXiv:2610.15424** (11 Oct; Claude-assisted): single-class version of the OpenAI transfer ⇒ f(n)/n → m₁ (Erdős #1070 / Dúcz–Varga conjecture, first half); "Its only non-classical input is the Haar rigidity theorem for wild character laws from the OpenAI preprint". So the first downstream theorem built on Theorem 2.3 already exists; its correctness is hostage to Theorem 2.3.
- **decalion89** (GitHub, 9–10 Oct): claims the transfer for every set of algebraic forbidden distances and for fractional colourings, and the whole χ ≥ 6 proof over the constructible field (Lean).
- **Bachoc–DeCorte–Oliveira Filho–Vallentin 2014**: the definition, not a transfer.

## 6. Shelah–Soifer and Theorem 1.3

Shelah–Soifer (JCTA 103 (2003) 387–391; 105 (2004)) — statement as reported by Payne and secondary sources (primary not fetched): if every finite unit-distance graph is 4-colourable (so χ = 4 in ZFC), then in ZF + DC + LM (every set Lebesgue measurable) χ(ℝ²) ≥ 5; Payne: "Under this new system the chromatic numbers of the graphs were found to be uncountable" (for their other graphs). Bearing on Theorem 1.3: none that conflicts. Their plane result is conditional on a hypothesis de Grey refuted. Theorem 1.3 (a ZFC statement; its "⇐" uses product compactness) would give χ_ZFC(ℝ²) = χ_w(ℝ²), the weak-measurable number. χ_w ≤ χ_m, and "a weak measurable k-colouring exists" is a projective statement about Borel codes, so its truth does not depend on the model. That rules out a ZFC chromatic number *below* the weak-measurable one. It does not decide whether χ_ZFC can be below χ_{ZF+DC+LM} (that would need χ_w = χ_m). The paper works "throughout in ZFC" (p. 2) and needs nothing more.

## 7. Test (A) from the sources' side (for the rigidity/whole seats to confirm)

- Payne's graph is Tℚ²: vertex set ℝ², x ~ y iff x − y is a unit vector in ℚ². "χ(Tℚ²) = 2 while χ_m(Tℚ²) ⩾ 5." Payne's Prop. 1 also gives χ_m(Tℚ²) ≥ χ(ℝ²), so if Theorem 1.1 holds, χ_m(Tℚ²) ≥ 6 for free.
- **A sharper contradiction than Payne's.** Run Li–Su's single-class transfer over ℚ(i) with rational rotations. Every finite subgraph of Tℚ² is bipartite (Woodall: χ(ℚ²) = 2), so the invariant law has P(0 ∈ ω) ≥ 1/2. Lemma 4.1 makes the projected field L²-continuous under all of ℝ², and unit correlations vanish on the dense set of rational directions, hence on every direction. That would give a measurable set of upper density ≥ 1/2 whose density points avoid all unit distances. This contradicts m₁(ℝ²) ≤ 2/7 (Moser spindle averaging) and m₁ ≤ 0.247 (Ambrus et al.). So the Haar rigidity (Thm 2.3) **must fail** for (ℚ(i), K_ℚ). The proof must use a property of F(i)/K that ℚ(i) lacks.
- **Steps in the paper that use such a property** (quoted from paper_plain.txt; PDF p. 6–7, 12, 16, 18):
  - l.295–297: "Every nonzero power map u ↦ uⁿ on K is onto … Thus K is divisible."
  - Lemma 2.4 proof, l.346–349: "If a coset d + C has positive mass, its K-orbit is finite … The action on this finite orbit gives a finite image of the divisible abelian group K. Such an image is trivial: a finite abelian group cannot be divisible unless it is trivial. Hence every u ∈ K fixes the coset". K_ℚ = {z/z̄ : z ∈ ℚ(i)*} is not divisible: (3+4i)/5 has square roots ±(2+i)/√5 ∉ ℚ(i). It has nontrivial finite quotients, so this step fails over ℚ.
  - Lemma 2.7, l.735: "The square roots belong to F" (the decomposition xⱼ = kⱼ + k′ⱼ). This fails in ℚ.
  - Lemma 3.2, l.922–923 ("the power map u ↦ u^d is onto") and Lemma 3.3, l.1211 ("the surjective power map u ↦ u^{−2}"). Both fail over ℚ.
- decalion89's notes (`world/thirdparty/decalion_notes_six_over_fields.md`) list the same uses: "F is closed under square roots … used in four places: … Lemma 2.7; … L = √(AB) in Lemma 3.3; … t + i√(1 − t²) in §3.5; … |z| ∈ F", and "K is divisible: Lemma 2.4 uses that a finite image of K is trivial; Lemma 3.2 uses that the power maps … are onto". They claim a Lean-checked rerun over the constructible numbers. Their changes: "an element of order 2 is enough" in Lemma 2.4, and the triple average at exponents −1, 0, 1 instead of 0, 1, 2 in Lemma 3.3. If true, the transfer needs exactly a *Euclidean* field (square roots of positives), which ℚ is not. That is a coherent, checkable answer to test (A). It is a third-party claim, not something I verified.

## 8. What is novel and what is not (with evidence)

| item | status | evidence |
|---|---|---|
| Theorem 1.1, χ(ℝ²) ≥ 6 | NEW if correct | no earlier or competing claim in arXiv 2024–26, Formal Conjectures, teorth, erdosproblems; Reed's χ = 7 is void; Davies (8 Oct) only *conjectures* χ = 6 |
| Theorem 1.4 alone ⇒ χ_m(ℝ²) ≥ 6 | NEW if correct; **not stated by the paper** | a measurable proper 5-colouring is a weak measurable one. SV 2025: "At this point, the best lower bound for the measurable chromatic number proved in 1981 is a consequence of the general result of [3]" (i.e. 5). This half does not depend on the transfer, so it survives even if test (A) sinks §§2–4 |
| Theorem 1.3 "⇒" (proper ⇒ weak measurable), via Thm 2.3 | NEW in d = 2 as far as anyone has found | Xie: "found no matching transfer theorem"; JoshuaZ: "doesn't seem … to have been in the literature"; Zelinsky; my searches. Concurrent: Davies's d ≥ 4 χ = χ_m (different method, stronger conclusion, higher dimension) |
| Theorem 2.3 (Haar rigidity of wild K-invariant laws) | NEW as stated | Xie classifies it "new"; classical analogue is Crum / Gneiting–Sasvári [3,11], cited by the paper |
| Theorem 1.3 "⇐" | NOT new | Falconer/Payne density points + de Bruijn–Erdős; the paper says "This adapts the familiar density-point mechanism of Falconer and Payne" |
| Definition 1.2 | NOT new; **not cited** | Bachoc–DeCorte–Oliveira Filho–Vallentin 2014, Def. 2.1 + §3.4 |
| invariant law on proper labelings by amenable averaging | NOT new (acknowledged: "standard") | Gwyn–Stavrianos (invariant µ on E(2)), Bourgeat et al., Matolcsi et al. (Følner over countable isometry groups) |
| interface/annulus exclusions (§§7–8) | measure-theoretic analogues of known map arguments (acknowledged) | Sokolov–Voronov Props 1–2 and 9; Townsend 2005 Thms 1, 4 (Thm 4 is the "three regions meet ⇒ 2-coloured annulus" step, the planar-map ancestor of Prop 8.10) |
| Corollary 1.5 | NOT new beyond Thm 1.1 | G–S Lemma 2.10/Thm 2.11 and Bourgeat Thms 1–2 applied to the existential finite graph |
| finite 6-chromatic unit-distance graph | NOT provided | the proof is existential (de Bruijn–Erdős); MO Q516012 open; decalion89: "no finite unit-distance graph without a proper 5-colouring is known" |

---------------------------------------------------------------------------------------------------

## 9. Objections (my scope)

**S1. Definition 1.2 is presented without its precursor.** Location: §1, Definition 1.2, PDF p. 2 ("Definition 1.2 (Weak measurable coloring). … A weak measurable k-coloring is a Lebesgue measurable function c : ℝ² → {1,…,k} … such that, for every R > 0, ∑ᵢ ∫_{B(0,R)} ∫_{S¹} 1_{Aᵢ}(x)1_{Aᵢ}(x+u) dσ(u) dx = 0."). The colour classes are exactly the measurable independent sets of the convolution operator A_ω of Bachoc–DeCorte–de Oliveira Filho–Vallentin (Israel J. Math. 2014, Def. 2.1, §3.4). Their operator chromatic number is the weak measurable chromatic number. Severity: COSMETIC for the proof; a GAP in the EXPOSITION of novelty (the paper's p. 4 contrasts only with Gwyn–Stavrianos). Fix: cite it, and note that its Hoffman-type bound (Thm 2.3) already gives ≥ 4 for this number.

**S2. Footnote 1 is correct but understates the counterexample.** Location: p. 2, footnote 1 (quoted in §2). The bound fails at measure π (three alternating arcs), and at 2π for r < 1/2, not only at the boundary case π/3. Severity: COSMETIC. Fix: none needed for correctness.

**S3. "Hadwiger's published formulation [13] asks for a covering by sets that avoid unit distance and gives the bounds four and seven" (p. 1) — the "covering" wording is unverifiable here.** The primary (Elem. Math. 16:103–104) is behind a CAPTCHA. Soifer confirms the bounds, the Nelson/Isbell attribution and the hexagon. Severity: UNCLEAR (COULD NOT FETCH). Fix: none needed for the proof.

**S4. Furstenberg [10, Lemmas 6.6 and 7.2] (l.828–830) not checked (closed access).** The paper says it gives its own fiberwise proof, so the citation is comparative. Severity: UNCLEAR (COULD NOT FETCH). The rigidity seat's line-by-line check of Lemma 3.1 is what matters.

**S5. Payne's Proposition 1 has an immediate consequence the paper omits:** χ_m(Tℚ²) ≥ χ(ℝ²) ≥ 6. Severity: COSMETIC.

**S6. The paper does not say that Theorem 1.4 alone gives χ_m(ℝ²) ≥ 6.** This is the first improvement of the measurable bound since Falconer 1981, and the part of the result that does not depend on the transfer. Severity: COSMETIC (exposition); it matters for how the community should weigh the result if test (A) is contested. Fix: one sentence after Theorem 1.4.

**S7. Székely's conjecture (χ ≠ χ_m) and Shelah–Soifer are the natural context for Theorem 1.3 and are not cited.** Severity: COSMETIC.

**S8. Cor 1.5(i) silently generalises Gwyn–Stavrianos from bi-invariant to left-invariant µ.** Valid: their proof uses left invariance only. Severity: COSMETIC.

No objection of severity FATAL or GAP-in-proof arises in my scope.

## 10. Read / not read

- Paper: pp. 1–4 (l.1–190), Corollary 1.5 and its proof (l.200–262), the hexagon paragraph, footnote 1, and every sentence containing a citation (contexts at l.336, 366–376, 418–428, 500–510, 822–834, 920–930, 1446–1456, 1482–1490, 1578–1622, 1972–1980, 2896–2904, 2944–2952, 3092–3102, 3290–3300, 3394–3402): VERIFIED LINE BY LINE for the citation claims and the finite arithmetic. Lemma 2.4's proof (l.343–349), the divisibility paragraph (l.295–297), and l.735, 922–923, 1211: read for test (A) pointers only, not verified as mathematics.
- §§2–8 lemmas and propositions: NOT READ (other seats' scope).
- Lean: not run, not read beyond the comparator statement quoted in the brief. Third-party build claims reported as claims (§0.4).

## 11. Verdict for my scope

**HOLDS AS READ** for the bibliography: no MISMATCH; COULD NOT FETCH [8] Falconer, [13] Hadwiger, [31] Woodall (publisher bot walls; secondary sources agree), [10] Furstenberg (closed access; the Lemma 6.6/7.2 locators are unverified), [32]/[33] Zimmer full text (abstracts match). Footnote 1 on Reed is correct. One material uncited precursor: Bachoc et al. 2014, for Definition 1.2.

**World:** χ(ℝ²) ≥ 6 is unrefuted and unrefereed. There are at least three public third-party Lean rebuilds (cert-machine with two kernels; decalion89; Li–Su for the transfer half) and Formal Conjectures labels it "research solved". erdosproblems.com/508 and the teorth database still say open, 5 ≤ χ ≤ 7, no claim. The only engagement with the substance is: Theorem 1.3 is the new, surprising step (Zelinsky, JoshuaZ, Rybin, Xie); the proof is non-constructive (MO); and there is a concurrent human transfer theorem in d ≥ 4 (Davies). Nobody has publicly addressed Payne's test.
