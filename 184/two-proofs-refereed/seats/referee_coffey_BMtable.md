# Referee seat: citation fidelity of Coffey's "Cited results of Bucić–Montgomery" (s1.tex §1.x, lines 400–775)

**Verdict (this seat's scope only): HOLDS WITH FIXES (exposition).** Every numbered result is the right one in
BM arXiv v2. No quoted *hypothesis* is weaker than BM's, and no *conclusion* is stronger than what BM prove.
The one place where a quoted statement is stronger than what BM *state* is Lemma 25 "explicit form". Coffey says
so, the constant does follow from BM's proof, and it is proved in Lean (`EG.bmLemma25`). But it is still
labelled "published". I found nothing FATAL or GAP-level.

Sources: BM = arXiv:2211.07689**v2** (14 Nov 2023, 26 pp), `/tmp/oaimath/181/refs/bm_2211.07689.pdf`. I read
bm.txt and rendered pages 8, 11, 12, 16, 18, 21, 22 and 23 to check every formula pdftotext garbles
(fractions, exponents, `log²`, `n/2`). Coffey's TeX: `paper/src/s1.tex`. Lean is cross-checked only through
`CORRESPONDENCE.md` and `formal/EG/Spec/Ext/*.lean`; nothing was built.

**Bibliography.** `ms.bbl` [BM] gives *Adv. Math.* **437** (2024) 109434, arXiv:2211.07689 (no version), plus
the STOC 2023 extended abstract pp. 839–852. Crossref confirms DOI 10.1016/j.aim.2023.109434, vol. 437,
art. 109434, Feb 2024, and the STOC pages. The text of §1 (s1.tex l. 403–404) fixes the numbering:
"numbers refer to the arXiv version arXiv:2211.07689v2". So the journal citation is right and the numbering
is tied explicitly to v2. I did **not** check whether the journal version numbers results the same way (we
only have v2). BM v2 itself says Lemma 17's proof replaced "a much more complex argument from initial versions
of this work" (p. 15), so v1 numbering may differ. Pinning v2 is the right call.

## Table

| Coffey label (line) | Coffey's statement | BM v2 actual statement (page) | Match? | Notes |
|---|---|---|---|---|
| `s1:citNotation` (410) | [BM §2.1, §2.6] notation: d_G, N_G, Δ, N_G(U) = vertices outside U with a neighbour in U, G[V], G∖V, G−F, \|G\| = #vertices, log base 2, log^[k], log* = least k ≥ 0 with log^[k] n ≤ 1, path through V, ball B^i_G(U,V) ⊆ V with start not required in V | §2.1 (p. 3) and §2.6 (p. 8): same definitions, same wording for B^i_G(U,V) | EXACT (one COSMETIC) | BM never define \|G\| in §2.1. They use it implicitly (\|G_i\|, \|G\|/2), so it is not "from §2.1". |
| `s1:citChernoff` (427) | [BM Thm 4]: X ~ Bin(n,p), 0 ≤ δ,p ≤ 1, P(X > (1+δ)μ) ≤ e^{−δ²μ/3}, P(X < (1−δ)μ) ≤ e^{−δ²μ/2} | Theorem 4 (p. 7), identical | EXACT | Black box in §3 and §4. Lean: `ChernoffBinomialStatement` is not in the final closure; the Lean uses `ChernoffGen`. |
| `s1:citDef7` (439) | (ℓ,t)-path connected through V: every collection P ⊆ (V(G) choose 2) with each vertex in ≤ t pairs has edge-disjoint xy-paths through V of length ≤ ℓ. Plus a "multiset clause (quoted in substance)": same pair may repeat; a k-fold pair gets k edge-disjoint paths; t counts occurrences; ends need not lie in V | Definition 7 (p. 7), same, followed by "We denote by (V(G) choose 2) the multiset of pairs of distinct vertices of G, so in particular the same pair may appear multiple times in the collection P" | FAITHFUL-RESTATEMENT | "k-fold pair gets k paths / t counts occurrences" is Coffey's reading. It is the natural one, but those are not BM's words (EXPOSITION E4). "Ends unrestricted" follows from BM's "a path through V is a path with all its internal vertices in V". Load-bearing definition (§§3–6). |
| `s1:citProp8` (455) | 1 ≤ ℓ,t ≤ n; \|V\| ≥ 4t−2; \|B^ℓ_G(U,V)\| > \|V\|/2 for all \|U\| = t; x_1..x_{2t−1}, y_1..y_{2t−1} distinct ⇒ some x_jy_j-path through V of length ≤ 4ℓ log n | Proposition 8 (p. 8), identical | EXACT | **Black box**, applied inside s3:lemL9rho (s3 l. 718, 754). I checked the hypotheses at the call site: 1 ≤ ℓ_* ≤ n, t_{0*} ≤ n, 4t_{0*}−2 ≤ \|V\|, distinct ends. Proved in Lean (`EG.BM8.bmProp8`, in closure). |
| `s1:citLem9` (464) | n ≥ 2, 1 ≤ ℓ,k ≤ n, \|V\| ≥ n/8+1, every non-empty U and \|F\| ≤ 2^9 k\|U\|(ℓ log n)² give \|B^ℓ_{G−F}(U,V)\| > \|V\|/2 ⇒ (4ℓ log n, k)-path connected through V. Proof summary + "applies verbatim to multisets" | Lemma 9 (p. 8), identical statement; proof p. 8–9 matches the summary (M_I maximal matching, \|M_I\| ≥ 4ℓ log n·\|I\|, I′, t = ⌈\|I′\|/16⌉, \|F\| < 8kt(8ℓ log n)², Prop 8 on G−F, Theorem 6) | EXACT (summary has a silent COSMETIC fix) | Proof-structure only; the modified s3:lemL9rho is proved in full. Coffey's summary says "4t−2 ≤ ⌈n/8⌉+1 ≤ \|V\|" where BM say "4t−2 ≤ n/8+1 ≤ \|V\|". BM's literal inequality fails at n = 34, \|I′\| = 17 (t = 2: 6 > 5.25) and holds only after rounding \|V\| up. Coffey's version is correct (C2). The multiset argument checks out: 2k\|I′\| ≥ \|I\| counts with multiplicity. |
| `s1:citDef11` (496) | (ε,s)-expander: for all U, F with 1 ≤ \|U\| ≤ 2n/3, \|F\| ≤ s\|U\|: \|N_{G−F}(U)\| ≥ ε\|U\|/log²n. Remark "hypotheses made explicit": if n ≥ 2 and ε > 0 then δ(G) > s | Definition 11 (p. 10), identical. BM's remark: "δ(G) > s for any (ε,s)-expander G", argued via U = {v} | EXACT (remark FAITHFUL, corrected) | BM's remark tacitly needs ε > 0 (and n ≥ 2, so that \|U\| = 1 ≤ 2n/3). Coffey makes both explicit, which is correct. Used everywhere. |
| `s1:citProp12` (512) | (ε,s)-expander, **1 ≤** \|U\| ≤ 2n/3, \|F\| ≤ s\|U\|/2, 0 < d ≤ s ⇒ (a) \|N_{G−F}(U)\| ≥ s\|U\|/(2d) or (b) \|N_{G−F,d}(U)\| ≥ ε\|U\|/log²n | Proposition 12 (p. 11): same, but with no lower bound on \|U\| | FAITHFUL-RESTATEMENT (slightly weaker than BM) | The extra 1 ≤ \|U\| only restricts BM (U = ∅ makes (a) trivial). Proof summary matches BM. **Exposition (E5):** s1 l. 405 and the citedresult (l. 519) say Prop 12's "counting is modified in s3:propP13s", but s3 l. 314 and 375 apply Prop 12 **verbatim as a black box**. It is load-bearing as stated, not proof-structure-only. Proved in Lean (`EG.FGraph.IsExpander.bmProp12`, in closure). |
| `s1:citProp13` (529) | ∃ n_0: n ≥ n_0, 1 ≥ ε ≥ 2^{−9}, s ≥ 8 log^{13} n, \|U\| ≤ 2n/3, \|F\| ≤ s\|U\|/4 ⇒ (a) \|U\|/log^7 n disjoint stars with log^9 n leaves (centre in U, leaves outside), or (b) bipartite H on (U, X) with \|X\| ≥ ε\|U\|/(2 log²n), deg_H(x) ≥ log^4 n on X, deg_H(u) ≤ 2 log^9 n on U | Proposition 13 (p. 11), identical; proof p. 11–12 matches the summary (C, L, (4), d = log^4 n, Δ = 2 log^9 n, U′ bound ε\|U\|/(8 log²n), B = C ∪ U′, Prop 12 on U∖B) | EXACT | Proof-structure only; s3:propP13s (general parameters) is proved in full. |
| `s1:citLem14` (560) | n-vertex G, integer s ≥ 0, ε ≤ 2^{−5}: delete ≤ 4sn log n edges, partition the rest into (ε,s)-expanders G_1..G_r with Σ\|G_i\| ≤ 2n ("for s = 0 nothing is deleted"). Proof summary with stronger induction bound 2n − 2n/(2+log n), (6)–(9) | Lemma 14 (p. 12), identical. Proof p. 12–13: same G_1 = G[U ∪ N_{G−F}(U)] − F, G_2 = G∖U − E(G_1) − F, (6)–(9) | EXACT | "(For s = 0 nothing is deleted)" follows at once from 4·0·n log n = 0 (BM, p. 12: "Setting s = 0 … obtains a full decomposition"). In the summary Coffey re-derives (9) separately for n ≥ 3 and n = 2. I checked both (log 3 > 2/(2√2−1) ≈ 1.094; at n = 2, n_1 = 1: 1 > 2/3 + 1/10). Proof-structure for Lemma 14^τ (s2:lem14tau, proved in full). This is the core BM lemma Coffey modifies. |
| `s1:citLem15` (605) | n,s ∈ N, integer k ≥ 1, 0 < ε ≤ 1, s ≥ 2^{12}ε^{−1}k²log^4 n ⇒ edge-disjoint G_1..G_k covering E(G), each an (ε/4, √(sε)/(8k log n))-expander on V(G) | Lemma 15 (p. 13), identical (n, k, s ∈ N) | EXACT | Not used. Replaced by s3:lemL15p. |
| `s1:citThm16` (619) | (ε,s)-expander, 1 ≥ ε ≥ 2^{−7}, s ≥ log^{135} n, V a 1/3-random subset ⇒ whp (4 log^5 n, 2^8 log^5 n)-path connected through V. Proof sketch: Lemma 15 with k = 2^{17}log^{42}n, Lemma 19 in each part, a part with ≤ \|U\|/log^{27}n edges of F when \|F\| ≤ 2^{17}\|U\|log^{15}n, Lemma 9 with k = 2^8 log^5 n, ℓ = log^4 n | Theorem 16 (p. 14), identical; proof §4.3 (p. 19) matches the sketch in every constant | EXACT | Not a black box; s3:thmT16s is proved in full. I checked the arithmetic: 2^9·2^8 log^5 n·log^{10} n = 2^{17}log^{15} n. |
| `s1:citLem17` (633) | n ≥ 2, 2^{−9} ≤ ε ≤ 1, s ≥ 8 log^{13} n, \|N_G(U)\| ≥ \|U\|log^{24}n, \|F\| ≤ \|U\|, V 1/3-random ⇒ with prob. 1 − e^{−Ω(\|U\|log²n)}: \|B^{log^4 n}_{G−F}(U,V)\| > \|V\|/2. Sketch: ℓ = log^4 n, q = 3/11, (1−p)^{ℓ−1} = 11/12, p ≥ 1/(15 log^4 n), B_i, (14), Prop 13 cases a/b, Lemma 5 | Lemma 17 (p. 16; exponent confirmed by rendering: e^{−Ω(\|U\| log² n)}), proof p. 16–18 matches the sketch | EXACT | Proof-structure only; s3:lemL17s is proved in full. (BM p. 17 has a typo, "every vertex of U has degree at most Δ" where W is meant. Coffey does not inherit it.) |
| `s1:citProp18` (657) | n ≥ 2, 0 < ε ≤ 1, s ≥ log^{24}n, \|U\| ≤ 2n/3 ⇒ ∃ U′ ⊆ U with \|N_G(U′)\| ≥ \|U′\|log^{24}n and \|U′\| ≥ ε\|U\|/(3 log^{26}n). Remark: BM's "at most θ" outside-neighbours is exact only for integer θ = log^{24}n; the proof needs s ≥ θ+1 | Proposition 18 (p. 18), identical statement. Proof: "v has at most log^{24}n neighbours outside U′ ∪ N_G(U′)", \|F\| ≤ \|U∖U′\|log^{24}n ≤ s\|U\| | EXACT (with a correct erratum on BM's proof) | Coffey's remark is right. Adding v to U′ can remove v itself from N_G(U′), so maximality gives only k < θ+1 outside-neighbours. This lies within BM's declared convention ("we also omit floor and ceiling signs wherever they are not crucial", p. 3). Not load-bearing: Coffey uses s3:lemP18s with s_1 ≥ θ_*+1, and BM's own use (Lemma 19) has s ≥ 2θ. Coffey still quotes the unproved-as-written form as a "published result" (E2). |
| `s1:citLem19` (680) | (ε,s)-expander, 2^{−9} ≤ ε ≤ 1, s ≥ 2 log^{24} n, V 1/3-random ⇒ with prob. 1 − o(1/n), for every **non-empty** U and every \|F\| ≤ \|U\|/log^{27}n: \|B^{log^4 n}_{G−F}(U,V)\| > \|V\|/2 | Lemma 19 (p. 18), says "for every U ⊆ V(G)" | FAITHFUL-RESTATEMENT (corrects BM) | For U = ∅ BM's literal statement is false (the ball is empty and \|V\| > 0 whp). Coffey flags the change. The proof sketch matches p. 19 (union bound, Prop 18, the Ū trick for \|U\| > 2n/3). Proof-structure only (s3:lemP18s(ii)). BM's proof also uses "n large" implicitly (\|F\| ≤ \|U′\| needs log n ≥ 6/ε); Coffey's quote keeps the asymptotic o(1/n), which is fine. |
| `s1:citThm21` (699) | Lovász: every n-vertex graph decomposes into at most n/2 paths and cycles | Theorem 21 (p. 21; rendered "n/2") | EXACT | Not used directly; enters only through Cor 22. Proved in Lean (`EG.LovaszC.lovasz`). |
| `s1:citCor22` (705) | Every graph decomposes into paths with each vertex an end of ≤ 2 paths (BM's proof: add a vertex joined to the even-degree vertices, apply Thm 21, delete it). Consequence: if all edges of H lie in W, then E(H) splits into ≤ \|W\| paths | Corollary 22 (p. 21), identical; proof as summarised | EXACT (consequence correctly derived) | The consequence is Coffey's two-line count (2·#paths ≤ 2\|W\|). It is correct, and BM use the same count in Lemma 23 ("\|P_i\| ≤ n"). **Black box** in §4 (vortex/TPV; s4 l. 76). Proved in Lean (`EG.cor22`, in closure). |
| `s1:citLem25` (719) | **Explicit form:** ε ≥ 2^{−5}, m ≥ max(2, 2^{30}/ε²) ⇒ every m-vertex (ε,0)-expander has a cycle of length ≥ ε²m/(18 log^4 m). Sketch of BM's DFS proof | Lemma 25 (p. 22): "n ≥ 2^{30}/ε² … contains a cycle of length Ω(n/log^4 n)". Proof (p. 22–23): \|P\| ≥ εn/(3 log²n); X, Y, Z with \|X\|,\|Z\| ≥ \|P\|/3 and ε²n/(18 log^4 n) ≤ \|Y\| < ε²n/(9 log^4 n); the cycle contains every vertex of Y | DERIVED-EXPLICIT-FORM (stronger than BM's *statement*, implied by BM's *proof*) | **The key "claims more" item, and it is sound.** BM's cycle contains Y, so its length is ≥ \|Y\| + 2 > ε²m/(18 log^4 m). Integrality also works: an (ε,0)-expander forces ε ≲ log²m/2, so 2ε²m/(18 log^4 m) ≤ \|P\|/6, and an integer \|Y\| exists because ε²m/(18 log^4 m) ≥ 2^{30}/(18 log^4 m) ≥ 1 in range. The added m ≥ 2 is needed only for the degenerate m = 1 case and is flagged. Where it is proved: the paper gives only a sketch. The full proof is the Lean `EG.bmLemma25` (DFS.lean, DFSCycle.lean; no `sorry`), and CORRESPONDENCE.md says "the explicit constant is the manuscript's". **Load-bearing:** s2:lemCap(ii), the size cap M_l on s = 0 pieces, used at ε = 2^{−5}, m ≥ 2^{40} (constant 1/18432). Labelled "\deps{none (published)}" (E1). |
| `s1:remBMused` (743) | Usage table: Def 7 → §§3–6; Lemma 9, Prop 8 → s3:lemL9rho; Thm 6 not used (Haxell instead); Def 11 everywhere; Props 12–13, Lemma 17, Prop 18, Lemma 19 → §3; Lemma 14 → §2; Cor 22 → §4; Lemma 25 → s2:lemCap; Thm 4 → §§3–4; Lemma 15, Thm 16, Thm 21 not used directly; Thm 2, Thm 24, Lemma 26 not used | — | ACCURATE | The ref/grep census matches every row: Def 11 in s2 and s3; Def 7 named in s3, s5, s6 and "path connected" ×8 in s4; Chernoff in s3, s4; Cor 22 in s4; Lemma 25 in s2. One mis-grouping: Prop 12 sits with the "modified" results but is a verbatim black box (E5). |

**Overview claim (s1.tex l. 166–172), "Where BM lose the factor log* n":** accurate. BM's proof of Theorem 2
(p. 23–24) does iterate Lemma 26 (p. 23) ℓ times, with ℓ the largest integer such that log^[ℓ] n ≥ 300C, so
ℓ ≤ log* n. Each Lemma 26 step:

- removes a maximal family of edge-disjoint cycles of length ≥ d (at most n/2 cycles);
- applies **Lemma 14 with s = 0**, ε = 2^{−5};
- uses Lemma 25 to show each expander has order O(d log^4 d) ("necessarily small");
- decomposes each expander by Theorem 24 into ≤ 6|G_i| cycles and O(|G_i| log^{274} d) edges.

The leftover average degree is O(log^{274} d), "a polylogarithm of d". The log* comes from
d_{i+1} ≤ C log^{274} d_i: only ℓ ≤ log* n rounds are needed before d is O(1).

Two small looseness points (E3):

- "Each iteration costs **Θ**(n) objects": BM prove only an **O**(n) upper bound per iteration (≤ 13n in
  Lemma 26, ≤ Cn in the proof of Theorem 2).
- "charged to all vertices that are active in it" is Coffey's interpretation, not BM's wording.

## Discrepancies, ranked by severity

**FATAL:** none. **GAP:** none. **UNCLEAR:** none.

**EXPOSITION**

- **E1. Lemma 25 "explicit form" is filed as a published result.**
  - Coffey, s1 l. 408: "All items of this subsection are published results". The citedresult carries
    `\deps{none (published)}`.
  - BM state only "a cycle of length Ω(n/log⁴n)" for n ≥ 2^{30}/ε².
  - Coffey's ε²m/(18 log⁴m) bound and the m ≥ 2 hypothesis are *derived* from BM's proof (BM: "ε²n/(18 log⁴n)
    ≤ |Y|"; the cycle contains every vertex of Y). The derivation is correct, and Coffey does say
    "Explicit form from the proof in [BM]".
  - In the paper the derivation is only a sketch. The full proof exists only in Lean (`EG.bmLemma25`).
  - It is load-bearing (s2:lemCap(ii)).
  - Fix: relabel it "derived from the proof of [BM, Lemma 25]; proved in full in Lean". Better, write out the
    roughly 8-line proof, including the integrality of |Y| and the bound |Y| < |P|/6.
- **E2. Prop 18 is quoted in BM's form while Coffey's own remark says BM's proof does not give that form.**
  - Coffey states "s ≥ log^{24} n", then: "the proof needs s ≥ θ+1 rather than s ≥ θ".
  - BM's line is "v has at most log^{24} n neighbours outside of U′ ∪ N_G(U′)".
  - The remark is correct, and the slip is within BM's no-floors convention.
  - It is harmless: Coffey uses s3:lemP18s with s_1 ≥ θ_*+1, and BM apply it only at s ≥ 2θ.
  - But the item is presented as a published result whose published proof needs a stronger hypothesis.
    Fix: one clause saying so.
- **E3. The overview overstates BM's per-iteration cost.**
  - Coffey l. 171: "Each iteration costs Θ(n) objects, charged to all vertices that are active in it".
  - BM prove O(n), not Θ(n), and the "charged to active vertices" accounting is Coffey's.
  - Everything else in l. 166–172 matches BM §5.6.
- **E4. Def 7's "multiset clause (quoted in substance from [BM])" adds an interpretation.**
  - Coffey adds: "a pair occurring k times receives k pairwise edge-disjoint paths, and the bound t counts
    occurrences."
  - BM only say: "the multiset of pairs of distinct vertices of G, so in particular the same pair may appear
    multiple times in the collection P."
  - The reading is natural, and BM's Lemma 9 proof supports it, but it should be marked as Coffey's gloss.
- **E5. Prop 12 is misdescribed as modified.**
  - s1 l. 405 and l. 519 say Prop 12's "counting is modified in Proposition s3:propP13s".
  - In fact s3:propP13s *applies* Prop 12 verbatim (s3 l. 314, 375: "By Cited result s1:citProp12 one of two
    cases holds"). That application is within BM's hypotheses.
  - So Prop 12 is a load-bearing black box. remBMused groups it with the modified lemmas.

**COSMETIC**

- C1. The [BM] bib entry has no version, though the in-text pin is v2. Journal-vs-v2 numbering is unchecked
  (only v2 available).
- C2. Lemma 9 summary: "4t−2 ≤ ⌈n/8⌉+1 ≤ |V|" silently corrects BM's "4t−2 ≤ n/8+1 ≤ |V|", which is false
  at n = 34, |I′| = 17. Coffey is right.
- C3. Lemma 19: the added "non-empty U" corrects BM's literal statement, which fails at U = ∅. It is flagged
  and correct.
- C4. Def 11 remark: n ≥ 2 and ε > 0 are made explicit. Correct.
- C5. Prop 12: the added 1 ≤ |U| only restricts BM.
- C6. Notation: "|G| is the number of vertices" is attributed to BM §2.1, which uses it but never defines it.
- C7. Lean `formal/EG/Spec/Ext/BMLemma25.lean` docstring still says "proves it (at present with `sorry`…)" and
  quotes the pre-v6 wording without m ≥ 2. The proof file has no `sorry`, and CORRESPONDENCE.md row
  `s1:citLem25` acknowledges the stale docstring.

## Load-bearing vs proof-structure

- **Black boxes whose quoted statement enters the proof** (each claimed proved in Lean, except where noted):
  - Def 7, Def 11 (definitions);
  - Prop 8, in Lemma 9_ρ;
  - Prop 12, in Prop 13*;
  - Theorem 4, Chernoff (the Lean uses the general Chernoff instead);
  - Cor 22, in the §4 vortex;
  - Lemma 25 explicit form, in Lemma Cap.

  All of these quotations are EXACT or correctly derived.
- **Cited for proof structure only; the modified version is proved in full in the paper:**
  - Lemma 9 → s3:lemL9rho;
  - Prop 13 → s3:propP13s;
  - Lemma 14 → s2:lem14tau;
  - Lemma 17 → s3:lemL17s;
  - Prop 18 and Lemma 19 → s3:lemP18s;
  - Theorem 16 → s3:thmT16s.

  Their summaries match BM's proofs constant for constant.
- **Not used:** Lemma 15, Theorem 21 (except through Cor 22), Theorem 6, Theorem 2, Theorem 24, Lemma 26.
