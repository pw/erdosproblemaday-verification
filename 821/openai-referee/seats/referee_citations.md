# Referee report — scope `citations` (reference list [1]–[23], §1, §2's cited forms, the live world)

Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers", 24 Sept 2026, /tmp/oaimath/011/paper.pdf
(sha256 351692885d112277e969901e75fe56eeee0d263d5d5847d0b980fe2c8c7744c0, matches paper.sha256).
Report date 2026-10-11. All primary sources downloaded under /tmp/oaimath/011/refs/<id>/ (PDF + pdftotext); the
world search is in /tmp/oaimath/011/WORLD_FINDINGS.md.

**Bottom line for this scope.** Every one of the 23 references exists, and every version number and date the paper gives
checks out against the arXiv version-history block, Crossref, zbMATH or the publisher's page. Every theorem-number locator
I could fetch (21 of 22; the exception is Montgomery–Vaughan 1974, behind a Wiley/Cloudflare wall) says what the paper
says it says. No citation is load-bearing in a way that a mismatch would break: every external result the proof actually
*uses* (Siegel–Walfisz, PNT, Mertens, the multiplicative large sieve, the two van der Corput derivative tests) is classical
and quoted correctly, and every "compare"/"in the spirit of" pointer (Efron–Stein, Ford–Halberstam, Matomäki–Radziwiłł,
Soundararajan, Friedlander–Iwaniec, Buchstab) is either re-proved in the paper or is only a pointer. **Nothing in the
bibliography refutes the paper. Nothing in it supports the paper's main claim either:** the paper's novelty (Theorems
3.5, 4.1, 5.1, 6.1) cites no external result that would carry it. In particular no cited work proves anything of the
strength x^{1−o(1)} for small smoothness exponents. The bibliography is clean, so the verdict rests on §§3–7, which are
outside this scope.

Below: objections (all COSMETIC or UNCLEAR, none FATAL or GAP), the citation table, the existence table, a parameter table
for the §2 lemmas I re-derived, and a verified-versus-skimmed list.

---

## 1. Objections

**C1. Pomerance's Theorem B needs a positive proportion; Theorem 1.2 gives only x^{1−o(1)}.** UNCLEAR (exposition), not load-bearing.
- Location: §1, p. 2: *"The final passage from plentiful smooth shifted primes to large totient fibers belongs to the method
  of Erdős and Pomerance; Pomerance states the relevant transfer explicitly in [19, Theorem B]. We give the needed
  product-and-pigeonhole proof in full."* Also §8, p. 65: *"see [19, Theorem B and its proof]"*.
- Source (Pomerance 1980, p. 87, verbatim): *"THEOREM B (Erdős [3]). Suppose that there is an ε > 0 such that
  Π(x, x^u) > επ(x) for all large x. Let m_1 < m_2 < … be the values of m where N(m) > m^{1−u}. Then there are infinitely
  many m_i and, in fact, log m_{i+1}/log m_i → 1."*
- Problem: Theorem B's hypothesis is a **positive proportion** Π(x,x^u) > επ(x). Theorem 1.2 gives x^{1−o(1)}, which is
  much weaker. So Theorem B, as Pomerance states it, does not apply to Theorem 1.2's output. "The relevant transfer" is
  stated explicitly only for the positive-proportion input.
- Why it is harmless: the paper does not invoke Theorem B. It proves its own transfer in §8. The transfer does work from
  x^{1−o(1)}. Sketch: take k ≍ X^{2δ} primes; there are ≥ C(P,k) ≥ (X^{1−o(1)}/k)^k products. Their totients are
  X^δ-smooth numbers ≤ (5X)^k, and there are at most (k log X)^{π(X^δ)} = X^{o(k)} of those. That gives n with
  g(n) ≥ n^{1−2δ−o(1)}.
- Also, Theorem B concludes log m_{i+1}/log m_i → 1. Theorem 1.1 neither claims nor needs this.
- Fix: write "Pomerance states the transfer from a positive proportion in [19, Theorem B]; the x^{1−o(1)} version proved
  in §8 follows the same product-and-pigeonhole scheme". The details of §8 are for the `whole`/§8 referee.

**C2. "Lemma 16.4" is listed in the [15] entry but never cited in the body.** COSMETIC.
- [15] (p. 67) lists *"Lemma 16.4, Corollary 16.6, Theorem 16.7, and Theorem 19.16"*. The body cites only
  [15, Corollary 16.6 and Theorem 16.7] (p. 7) and [15, Theorem 19.16] (p. 6). `grep "16.4"` finds no body occurrence.
- Lemma 16.4 is the geometric-series bound |Σ_{n≤N} e(nα)| ≤ min(N, 1/(2‖α‖)). If it is used implicitly (e.g. on the
  minor arcs), the use is uncited. If it is not used, the locator is dead.

**C3. [15] cites an undated draft although the book was published in 2026.** COSMETIC.
- The URL resolves: HTTP 200, 472 pp., server `Last-Modified: Thu, 10 Sep 2026`, PDF CreationDate 9 Oct 2024. All four
  locators exist in it.
- Crossref lists the published book: *Multiplicative Number Theory II*, Cambridge UP, issued 2026-04-30,
  DOI 10.1017/9781009445030 (chapter "Primes in Arithmetic Progressions: III", pp. 189–225 appears in the search).
- Numbering in the published edition was not checked. A reader with the book may not find "Theorem 19.16".
  The paper does say "author-hosted draft", so this is transparent.

**C4. [18] omits the journal publication.** COSMETIC.
- Pilatte's paper appeared in J. Amer. Math. Soc. online on 2026-09-10 (DOI 10.1090/jams/1084), two weeks before the
  preprint's date. The paper cites only arXiv v3 (25 Aug 2026). That date is correct.

**C5. [10] page range: 267–323 vs Crossref 267–324.** COSMETIC.
- The MSRI/SLMath contents page says *"Smooth numbers: computational number theory and beyond by Andrew Granville,
  267-323"*, which matches the paper. Crossref (CUP) has 267–324. No action needed.

**C6. [4] title capitalisation.** COSMETIC.
- The paper has "Asymptotische abschätzung einer allgemeinen zahlentheoretischen funktion". zbMATH (JFM 63.0902.01) has
  "Asymptotische Abschätzung einer allgemeinen zahlentheoretischen Funktion", Rec. Math. Moscou (2) 2(44), No. 6,
  1239–1246 (1937). Volume, issue, pages and year are correct.

**C7. Friedlander–Iwaniec is "compared" but its hypotheses are not those used here.** COSMETIC. Noted so nobody reads
it as an import.
- FI's asymptotic sieve needs the Type I level (R1) *"x^{2/3} < D(x) < x"* together with their bilinear hypothesis.
- This paper's Type I level is x^{1/2−κ/2} (Prop 7.2). Its prime extraction is its own Buchstab/proxy accounting (§7),
  not FI's theorem.
- §1.1 says only "compare Friedlander and Iwaniec [9, Section 1]". That is accurate as a pointer and imports nothing.
  Whether the paper's own sieve really extracts primes at level ½ plus its Type II is the §7 referee's question.

**C8. The cited divisibility-graph works do not underwrite the step where this paper needs something new.** UNCLEAR.
Flagged so downstream referees do not assume [11], [14], [18], [23] cover Theorem 5.1.

- **The graph/expansion theorems in [11] and [18] already hold for arbitrary functions.** Helfgott–Radziwiłł's
  Corollary 1.1 is stated for any f, g : N → C with |f|_2, |g|_2 ≤ 1 and |f|_4, |g|_4 ≤ e^{CL}:
  (1/NL) Σ_n Σ_σ Σ_{p∈P, p|n} f(n)g(n+σp) − Σ_n Σ_σ Σ_{p∈P} f(n)g(n+σp)/p = O(1/√L). Pilatte's Remark 2.6 allows
  arbitrary signs c_{p_1,…,p_J}. So the analogue of this paper's Theorems 3.5/4.1 ("raw pattern ≈ comparison patterns")
  is, in those works, a statement about arbitrary endpoints.
- **Multiplicativity enters those works at two other steps:**
  - (a) converting λ(n)λ(n+1) into the graph sum via λ(pn) = −λ(n). This paper replaces it with invariance of F_0, G_0
    under multiplication by group primes, built into (5.3).
  - (b) bounding the averaged term Σ_p Σ_n f(n)g(n+σp)/p. HR §1.4.2: *"We will bound the second sum on the right of (1.10)
    using [MRT15, Thm. 1.3] (essentially as in [Tao16a, Lemmas 3.4–3.5])"*. That is, it uses Matomäki–Radziwiłł-type
    short-interval cancellation **for multiplicative functions**. Tao [23] uses the same input; his abstract lists among his main tools *"a recent result of
    Matomäki, Radziwiłł, and the author on the averages of modulated multiplicative functions in short intervals"*.
- **Step (b) is exactly where this paper needs something with no precedent.** Its endpoints (5.3) are not
  multiplicative. Its substitute for MRT is the local Fourier energy bound (5.11), proved in §5.4–5.8 from a one-sided
  character/Mellin discrepancy (5.4) plus the compulsory long W-rough factor.
- Nothing in the bibliography proves a short-interval / local-Fourier statement of that type for non-multiplicative
  sequences. Matomäki–Radziwiłł [13] is cited only for the method ("in the spirit of … we do not invoke their
  short-interval theorem", p. 42).
- The paper is honest about this. §3, p. 10: *"The operators and ranges here differ; the memory identity and transference
  estimate below are proved for the present model."*
- So the citations are accurate, and **no** external result carries the new step. §5.4–5.8 (and the transference
  §3/§4, which the companion paper also imports) stand or fall on the paper's own proofs.

No FATAL or GAP findings arise in this scope.

---

## 2. Citation table (cited result → paper's claim → source verbatim → verdict)

| # | Cited result | What the paper says it says | What the source says (verbatim quote, version read) | Verdict |
|---|---|---|---|---|
| [19] p.84 | Pomerance 1980 | "formulates the conjecture as C = 1, where C is the supremum of the exponents c for which g(n) > n^c infinitely often, and attributes it to Erdős [7]" | p. 84: "Let C be the least upper bound of the set of c for which (1) holds" [(1): N(m) > m^c for infinitely many m] … "Erdős [4] has conjectured that C = 1." Pomerance's [4] = "P. Erdős. 'On pseudoprimes and Carmichael numbers', Publ. Math. Debrecen, 4 (1956), 201-206" = paper's [7]. (Read: author copy math.dartmouth.edu/~carlp/popular.pdf, 6 pp.) | MATCH |
| [19] Thm B | Pomerance 1980 | "Pomerance states the relevant transfer explicitly in [19, Theorem B]" | p. 87: "THEOREM B (Erdős [3]). Suppose that there is an ε > 0 such that Π(x, x^u) > επ(x) for all large x. Let m_1 < m_2 < … be the values of m where N(m) > m^{1−u}. Then there are infinitely many m_i and, in fact, log m_{i+1}/log m_i → 1." | MATCH as a pointer; the hypothesis is a positive proportion, so it does not apply verbatim to x^{1−o(1)} (see C1). The paper re-proves the transfer. |
| [6] §3 | Erdős 1935 | "Erdős's work on totient multiplicities and smooth shifted primes dates to [6, Section 3]" | §3 (pp. 211–213), Lemma 4: "We can find a positive ρ so small that there are more than C_22 μ^{1+ρ}/ν primes p not exceeding μ^{1+ρ} such that p−1 is composed of primes all less than μ." Main theorem: "an integer m … represented Ω(n^{α−ε}) … times as the φ of another integer … the number of these representations is greater than m^{C_3}". (renyi.hu Erdős archive 1935-08.pdf) | MATCH |
| [7] | Erdős 1956 | "The expectation that p − 1 can have all its prime factors smaller than every fixed power of p was recorded in [7]" (and C = 1 is attributed to it via Pomerance) | p. 206: "It is reasonable to expect that for u < (log x)^{c_18} there are more than c_19 π(u) (c_19 = c_19(c_18)) r's not exceeding u (though this will probably be very hard to prove)" [r prime with (r−1) \| A, A = product of primes < ε log x] … "The above arguments (using only the first conjecture) would imply that c_20 can be taken as close to 1 as we please." (renyi.hu 1956-10.pdf, page image read) | MATCH. Erdős's expectation is stronger (a positive proportion). |
| [12] Intro | Lichtman v1 | "see also [12, Introduction]" | "Following an old conjecture of Erdős [11, 12], we expect there are infinitely many primes p with P^+(p − a) ⩽ p^ε, for any ε > 0." | MATCH |
| [2] §1 Thm 1 | Baker–Harman 1998 | "obtained exponent 0.2961 for shifted primes" | "THEOREM 1. For y ≥ x^β we have π(x, y) > x/(log x)^{C_1} for x ≥ x_0. Here β = 0.2961; x_0 may depend on a; C_1 is an absolute constant." (Acta Arith. 83.4, pp. 331–361, matwbn aa8342.pdf, page image read) | MATCH. NB the count is x/(log x)^{C_1}, **not** ≫ x/log x as REFEREE_BRIEF.md states; the paper itself does not state the count for [2]. |
| [2] Cor 1 | Baker–Harman 1998 | "with the corresponding totient multiplicity exponent 0.7039" | "COROLLARY 1 (Erdős–Pomerance). Let m_1 < m_2 < … denote those positive integers m such that the equation φ(n) = m has more than m^{1−β} solutions n. Then the sequence (m_i) is infinite, and satisfies lim log m_{i+1}/log m_i = 1." 1 − 0.2961 = 0.7039. | MATCH (0.7039 is implicit as 1−β, not printed) |
| [2] §1 | Baker–Harman 1998 | "This improved Friedlander's threshold 1/(2√e) + ε; their introduction also describes preceding work of Pomerance, Balog, and Fouvry–Grupp" | "The previous best exponent is 1/(2√e) + ε = 0.3032… (Friedlander [8]). Earlier results in this direction were obtained by Pomerance [11], Balog [3] and Fouvry and Grupp [7]." | MATCH |
| [12] Thm 1.1 | Lichtman arXiv:2211.09641v1 | "proved a lower bound x/(log x)^C for x < p ≤ 2x and P^+(p−1) ≤ x^β whenever β > 15/(32√e) = 0.284311…" | "Theorem 1.1. For fixed nonzero a ∈ Z and β > 15/32√e = 0.2843···, there exists C ⩾ 1 such that Σ_{x<p⩽2x, P^+(p−a)⩽x^β} 1 ≫ x/(log x)^C." Checked numerically: 15/(32√e) = 0.284311246… | MATCH |
| [12] Cor 1.3 | Lichtman v1 | "and obtained multiplicity exponent 0.7156" | "Corollary 1.3. Denote by m_1 < m_2 < ··· the integers m ∈ Z for which m = ϕ(n) admits at least m^{0.7156} solutions n ∈ Z. Then the sequence (m_i) is infinite, and satisfies lim log m_{i+1}/log m_i = 1." | MATCH |
| [12] current version | Lichtman | v1 is cited | arXiv abs page: only "[v1] Mon, 14 Nov 2022 12:54:15 UTC (23 KB)". There is no later version, so the current version is v1. zbMATH lists it only as "Preprint, arXiv:2211.09641"; no journal version in Crossref. | v1 = current; unpublished (coverage claim: zbMATH + Crossref + one web search) |
| [10] §5.3 | Granville 2008 | "The expected Dickman law predicts a positive proportion of primes for every such exponent; see Granville [10, Section 5.3]" | §5.3 "Primes p where p − 1 is smooth": "One would guess that π(x; y) ∼ π(x)ρ(u) when y = x^{1/u} (5.1) and, indeed, this follows for all u ≥ 1 from a weak form of the Elliott–Halberstam conjecture". (MSRI Book 44, 09andrew.pdf) | MATCH |
| [3] Prop 2 | Bharadwaj–Rodgers arXiv:2402.11884v4 | "their Proposition 2 establishes distribution level one half and the other conditions unconditionally" | "Proposition 2. Shifted primes are 1/2 well-distributed. That is: for a fixed integer a, consider the set B = {p − a : p is prime} and let a_n = 1[n ∈ B]. Then (a_n) has index 1, has level of distribution ϑ = 1/2, and is congruence uniform." Proof: "The level of distribution 1/2 follows from the Bombieri-Vinogradov theorem". | MATCH. Yes, Prop 2 is level ½ for shifted primes (by Bombieri–Vinogradov). |
| [3] Thm 7 | B–R v4 | "prove the full Poisson–Dirichlet law for sequences satisfying their regularity and congruence-uniformity conditions together with level-one distribution" | "Theorem 7. If (a_n) is 1 well-distributed, then P(log p_1/log u ≤ c_1, …, log p_k/log u ≤ c_k) → P(L_1 ≤ c_1, …, L_k ≤ c_k) … tends in distribution to the Poisson-Dirichlet process". "σ well-distributed if (a_n) satisfies each of (A), (B), and (C)" [index, level of distribution, congruence uniform]. | MATCH |
| [3] Conj 5 | B–R v4 | "For shifted primes this gives the prediction under the Elliott–Halberstam conjecture" | "Conjecture 5. The shifted primes have level of distribution ϑ = 1. Indeed this is a slightly weaker version of the Elliott-Halberstam conjecture". | MATCH |
| [1] | AGP 1994 | "Smooth predecessors also enter the construction of Carmichael numbers … combined with a separate distribution theorem for primes in arithmetic progressions" | p. 704: "Let 𝓔 denote the set of numbers E … such that (0.1) π(x, x^{1−E}) ≥ γ_1(E)π(x) … Erdős has conjectured that any positive number less than 1 is in 𝓔 … Define π(x; d, a) … The prime number theorem for arithmetic progressions states that (0.2) …" (author copy carlp/PDF/paper95.pdf) | MATCH |
| [9] §1 | Friedlander–Iwaniec 1998 (arXiv math/9811186v1) | "This division of work is familiar from prime-detecting sieves; compare [9, Section 1]" | §1 sets up the congruence sums A_d(x) = g(d)A(x) + r_d(x), (R) Σ_{d≤D} µ²(d)\|r_d(t)\| ⩽ A(x)(log x)^{−22} with (R1) "x^{2/3} < D(x) < x", "We assume an estimate for bilinear forms…" | MATCH as a comparison (see C7: FI's level x^{2/3} ≠ this paper's x^{1/2−κ/2}) |
| [14] Thm 5.1 | MRT 2016 (Forum Sigma e14, 44 pp.; published PDF and arXiv v2 both read) | "studied connectivity of a graph with prime-divisibility edges" | "We then define E to be the set of pairs {a, b} of distinct vertices a, b in V, such that \|b − a\| is an odd prime number dividing n + a … THEOREM 5.1. The random graph G is almost surely connected." | MATCH |
| [23] | Tao 2016 (FoM Pi e8, 36 pp.) | "Tao's entropy-decrement argument [23] replaces such divisibility conditions by their mean at a suitable scale" | "it allows one to select a scale parameter H … for which the sequence (λ(n+1),…,λ(n+H)) and the graph G_{n,H} exhibit some weak independence properties … use standard concentration of measure … to approximate (1.5) by the significantly simpler expression (1/H)Σ_j Σ_{p∈P} λ(n+j)λ(n+p+j)/p" | MATCH |
| [11] §1.5 | Helfgott–Radziwiłł arXiv:2103.06853v2 | "study centered adjacency operators through signed closed-walk moments, with repeated primes creating dependent congruences" | §1.5 "Strategy of proof": "Tr(A\|X)^{2k} can also be expressed as a sum over closed walks of length 2k … edges of Γ∪Γ′ have the weight 1−1/p … or −1/p … any two appearances of p impose a divisibility condition on the sum of the steps taken between those two appearances" | MATCH |
| [18] Thm 2.4, §5 (§3) | Pilatte arXiv:2310.19357v3 | "develops this approach for shifts that are products of primes"; §3: "Pilatte [18, Sections 3 and 5]" | "Theorem 2.4. Let N be an integer such that log N ⩾ (log H)^{2.001}. Then \|Σ_{(p_1,…,p_J)} Σ_{n∈(N,2N], p_1⋯p_J\|n} λ(n)λ(n+p_1⋯p_J)\| ⩽ e^{O(J)}(V_1⋯V_J)^{1/2}N." §5 "High trace bound for the non-backtracking operator"; §3.1 "Centred sum … 1_{p\|n} − 1/p". | MATCH |
| [5] §2 | Efron–Stein 1981 (Ann. Statist. 9(3), 586–596; Project Euclid scan read as images) | "the orthogonal product-space decomposition of Efron and Stein [5, Section 2, Decomposition Lemma]"; used as F_S = Π_{i∈S}(1−E_i)Π_{i∉S}E_i F′ | §2: "DECOMPOSITION LEMMA. The random variable S(X_1, …, X_n) can be expressed as (2.4) S = µ + Σ_i A_i(X_i) + Σ_{i<i′} B_{ii′}(X_i,X_{i′}) + … + H(X_1,…,X_n), where all 2^n − 1 random variables on the right side … have mean zero and are mutually uncorrelated with each other." Hypotheses: independent X_i (not necessarily identically distributed), ES² < ∞. | MATCH. The operator form used here is the standard equivalent for independent coordinates; the ideal space H_id = ⊗ µ_g^{⊗M} is a product measure, so the hypothesis holds. ES's scalar statement extends verbatim to complex L² and to decomposing in a subset of coordinates with the others as parameters. |
| [8] §1 Lemma 1 | Ford–Halberstam 2000 (author copy hooleysieve.pdf, 15 pp.) | "the product of block upper bounds and its one-block correction are the inequalities of Ford and Halberstam [8, Section 1, Lemma 1]" | (2)–(3): Σ_{d\|(a,P)} µ(d) = Π_j Σ_{d\|(a,P_j)} µ(d) ≤ Π_j Σ_{d\|(a,P_j), ν(d)≤k_j} µ(d). "Lemma 1. Suppose that 0 ≤ x_j ≤ y_j (j = 1, …, r). Then (4) x_1⋯x_r ≥ y_1⋯y_r − Σ_{ℓ=1}^r (y_ℓ − x_ℓ) Π_{j≠ℓ} y_j." (5): "0 ≤ y_ℓ − x_ℓ ≤ Σ_{d\|(a,P_ℓ), ν(d)=k_ℓ+1} 1". | MATCH. With x_j = I_j, y_j = U_j, (4)+(5) give exactly Lemma 2.9's "0 ≤ ΠU_j − ΠI_j ≤ Σ_j E_j Π_{k≠j} U_k" (p. 9). I re-derived U_j = C(t−1, h_j) for t ≥ 1 (h_j even) and U_j − I_j ≤ C(t, h_j+1) = E_j. |
| [15] Cor 16.6 | MV II draft | Lemma 2.7(i): "If f′ is monotone and stays in [j+λ, j+1−λ] for some integer j and 0 < λ ≤ 1/2, then Σ_n e(f(n)) ≪ λ^{−1}." | "Corollary 16.6 Let f(x) be a real valued function continuous on [a, b], with a continuous derivative on (a, b), and such that f′(x) is increasing. Suppose further that M_1 is a positive real number such that ‖f′(x)‖ ≥ M_1 for all x ∈ (a, b). Then \|Σ_{a≤n≤b} e(f(n))\| ≤ 2/(πM_1)." | MATCH. Decreasing f′ follows by conjugation; a monotone derivative is continuous by Darboux. |
| [15] Thm 16.7 | MV II draft | Lemma 2.7(ii): "If f is twice continuously differentiable and λ ≤ \|f′′\| ≤ Cλ throughout the interval, then Σ_n e(f(n)) ≪_C Hλ^{1/2} + λ^{−1/2}." | "Theorem 16.7 Let N be a positive integer with a ≤ b ≤ a + N and suppose that f is twice differentiable on [a, b] and that 0 < M_2 ≤ f″(x) ≤ AM_2 … Then Σ e(f(n)) ≪_A M_2^{1/2}N + M_2^{−1/2}. If instead we have −AM_2 ≤ f″(x) ≤ −M_2, then the same bound applies" | MATCH (continuity of f″ plus \|f″\| ≥ λ > 0 forces a constant sign) |
| [15] Thm 19.16 | MV II draft | Theorem 2.3: Σ_{r≤R} (r/φ(r)) Σ*_χ \|Σ_{n∈I∩Z} a_n χ(n)\|² ≪ (H + 1 + R²) Σ\|a_n\|² | "Theorem 19.16 Let M and N be integers with N ≥ 1 … Then for any integer Q ≥ 1, Σ_{q≤Q} (q/φ(q)) Σ★_χ \|S(χ)\|² ≤ (N + Q²) Σ_{n=M+1}^{M+N} \|c_n\|²" | MATCH (the paper's form is weaker: N ≤ H+1, Q = ⌊R⌋) |
| [15] Lemma 16.4 | MV II draft | listed in the bibliography only | "Lemma 16.4 … \|Σ_{n=1}^N e(nα)\| ≤ min(N, 1/(2‖α‖))." | Exists; never cited in the body (C2) |
| [16] Thm 2, Cor 3 | MV 1974 | Lemma 2.6 is "a weaker elementary form of the Dirichlet-polynomial mean-value theorem; compare [16, Theorem 2 and Corollary 3]" | — | COULD NOT FETCH (Wiley returns a Cloudflare "Just a moment…" page to both curl and headless Chromium; paywalled). Not load-bearing: the paper proves Lemma 2.6 itself, and I checked that proof (§5). |
| [21] Thm 15 | Tao 254A notes 1 (blog, posted 2014-11-24T00:51Z = 23 Nov US time; modified 2025-01-24) | Mertens Σ_{p≤y} 1/p = log log y + O(1) | "Theorem 15 (Second Mertens' theorem) One has Σ_{p≤x} 1/p = log log x + c_1 + O(1/log x) for x ≥ 2" | MATCH |
| [21] Thm 26 | Tao notes 1 | Π_{p≤y}(1 − 1/p) ∼ e^{−γ_E}/log y | "Theorem 26 (Third Mertens' theorem) We have Π_{p≤x}(1 − 1/p) = (e^{−γ} + O(1/log x))/log x" | MATCH |
| [22] Cor 39, Ex 40 | Tao 254A notes 2 (posted 2014-12-10T02:05Z = 9 Dec US time; modified 2025-06-14) | "the prime number theorem with an error smaller than any fixed negative power of the logarithm" | "Corollary 39 (Prime number theorem with classical error term) … Σ_{n≤x} Λ(n) = x + O(x exp(−c√log x)) … In particular … x + O_A(x log^{−A} x)"; "Exercise 40 (Alternate form of prime number theorem) … π(x) = li(x) + O(x exp(−c√log x))" | MATCH |
| [22] Ex 64 | Tao notes 2 | Theorem 2.2 (Siegel–Walfisz) "follows from its von Mangoldt formulation by partial summation; see [22, Exercise 64]" | "Exercise 64 (Siegel-Walfisz theorem) For any A > 0, show that there exists an (ineffective) constant c_A > 0 such that Σ_{n≤x: n=a (q)} Λ(n) = x/φ(q) + O(x exp(−c_A √log x)) for all primitive residue classes a (q) and all x ≥ 2 with q ≤ log^A x." | MATCH (the paper also notes that the constants are ineffective) |
| [13] §2.1, §4 Lemmas 8–9 | MR arXiv:1501.04585v4 | "The split into ordinary and exceptional times, followed by high prime-polynomial moments and a sparse mean-square estimate, is in the spirit of … [13, Section 2.1 and Section 4, Lemmas 8–9]. The estimates needed here are proved below" | §2.1: "We begin by splitting the range of integration … into J + 1 disjoint sets T_1, …, T_J, U … The set U is rather sparse"; "Lemma 8. Let P(s) = Σ_{P≤p≤2P} a_p/p^s … T ⊂ [−T, T] well-spaced points such that \|P(1+it)\| ≥ V^{−1} … Then \|T\| ≪ T^{2 log V/log P} V² exp(2 (log T/log P) log log T)"; "Lemma 9 (Halász inequality for integers) … Σ_{t∈T} \|A(it)\|² ≪ (N + \|T\|√T) log 2T Σ\|a_n\|²" | MATCH (the paper re-proves what it needs) |
| [20] Lemma 3 | Soundararajan 2009 (published Annals PDF and arXiv v2 both read) | "the standard prime-polynomial moment argument; compare [20, Lemma 3 and its proof]" | "LEMMA 3. Let T be large, and let 2 ≤ x ≤ T. Let k be a natural number such that x^k ≤ T/log T. For any complex numbers a(p) we have ∫_T^{2T} \|Σ_{p≤x} a(p)/p^{1/2+it}\|^{2k} dt ≪ T k! (Σ_{p≤x} \|a(p)\|²/p)^k." | MATCH |
| [4] | Buchstab 1937 | "Buchstab's rough-number densities … the corresponding Buchstab identity [4]" | zbMATH review (JFM 63.0902.01, by A. Scholz): "Die Anzahl der Zahlen ≤ x in der teilerfremden Progression …, die durch keine Primzahl unterhalb x^{1/α} teilbar sind, ist Φ_l(k; x; x^{1/α}) = (1/φ(k))(x/log x)ψ(α) + o(x/log x) mit ψ(α) = 1 + ∫_1^{α−1} dz_1/z_1 + …" | MATCH as an attribution (review read; full text on mathnet.ru unreachable from this host) |
| [17] | companion | "These graph and ideal-kernel estimates also serve as inputs to the companion paper [17, Theorem 1.1]" | Companion (local copy pd_paper.txt), p. 5: "We use the dilation-graph and ideal-kernel theorems of the companion Weighted dilation graphs, smooth shifted primes and totient fibers [21], denoted S."; §6.1: "This is the combination of the local transference theorem, endpoint pairing corollary, and physical Schur bound of S [21, Theorem 3.5, Corollary 3.11, and Lemma 3.4]." and "This is S [21, Theorem 4.1 and Lemma 4.3]." | MATCH. **The companion imports Theorem 3.5, Corollary 3.11, Lemma 3.4, Theorem 4.1 and Lemma 4.3 of this paper. A gap in §3 or §4 here propagates to the Poisson–Dirichlet paper.** |

---

## 3. Existence table for [1]–[23] (authors, title, venue, year, pages, arXiv id, version, date)

| # | Verdict | Evidence |
|---|---|---|
| [1] AGP, Ann. Math. 139(3):703–722, 1994 | EXISTS-AS-CITED | Crossref 10.2307/2118576: vol 139, iss 3, p. 703, 1994-05. (Curiosity: the author-hosted scan carlp/PDF/paper95.pdf prints "Annals of Mathematics, 140 (1994), 703–722" in its header; Crossref and Lichtman's bibliography both give 139.) |
| [2] Baker–Harman, Acta Arith. 83(4):331–361, 1998 | EXISTS-AS-CITED | Crossref 10.4064/aa-83-4-331-361; IMPAN page "Acta Arithmetica 83 (1998), 331-361"; scan is 31 pp. |
| [3] Bharadwaj–Rodgers, CMB pp. 1–17, 2026, First View 17 Apr 2026; arXiv:2402.11884v4, 9 Apr 2026 | EXISTS-AS-CITED | Crossref 10.4153/s0008439526101982, online 2026-04-17, pp. 1–17; arXiv history "[v4] Thu, 9 Apr 2026 08:00:29 UTC", comment "Incorporates referee comments and corrections". |
| [4] Buchstab, Mat. Sb. 2(44)(6):1239–1246, 1937 | EXISTS-AS-CITED (title capitalisation, C6) | zbMATH JFM 63.0902.01 / Zbl 0018.24504. |
| [5] Efron–Stein, Ann. Statist. 9(3):586–596, 1981 | EXISTS-AS-CITED | Crossref 10.1214/aos/1176345462; scan header "1981, Vol. 9, No. 3, 586–596". |
| [6] Erdős, Quart. J. Math. os-6(1):205–213, 1935 | EXISTS-AS-CITED | Crossref 10.1093/qmath/os-6.1.205. |
| [7] Erdős, Publ. Math. Debrecen 4:201–206, 1956 | EXISTS-AS-CITED | Crossref 10.5486/pmd.1956.4.3-4.16 (vol 4, iss 3–4, pp. 201–206); renyi.hu 1956-10. |
| [8] Ford–Halberstam, JNT 81(2):335–350, 2000 | EXISTS-AS-CITED | Crossref 10.1006/jnth.1999.2479. |
| [9] Friedlander–Iwaniec, Ann. Math. 148(3):1041–1065, 1998 | EXISTS-AS-CITED | Crossref 10.2307/121035; arXiv math/9811186 journal-ref. |
| [10] Granville, MSRI Publ. 44, 267–323, CUP 2008 | EXISTS-AS-CITED (Crossref 267–324, C5) | SLMath Book44 contents "267-323". |
| [11] Helfgott–Radziwiłł, arXiv:2103.06853v2, 13 Apr 2021 | EXISTS-AS-CITED | "[v2] Tue, 13 Apr 2021 17:38:44 UTC". |
| [12] Lichtman, arXiv:2211.09641v1, 14 Nov 2022 | EXISTS-AS-CITED | "[v1] Mon, 14 Nov 2022 12:54:15 UTC"; the only version; unpublished per zbMATH/Crossref. |
| [13] Matomäki–Radziwiłł, Ann. Math. 183(3):1015–1056, 2016; locators to arXiv v4 | EXISTS-AS-CITED | Crossref 10.4007/annals.2016.183.3.6; "[v4] Sun, 15 Oct 2017". |
| [14] MRT, Forum Math. Sigma 4:e14, 2016, 44 pp. | EXISTS-AS-CITED | Crossref 10.1017/fms.2016.6 article-number e14; published PDF 44 pp. |
| [15] Montgomery–Vaughan, MNT II draft URL, accessed 13 Sep 2026 | EXISTS-AS-CITED | HTTP 200, 472 pp., Last-Modified 10 Sep 2026; all four locators present. (Book published by CUP 2026-04-30, C3.) |
| [16] Montgomery–Vaughan, JLMS 8:73–82, 1974 | EXISTS-AS-CITED | Crossref 10.1112/jlms/s2-8.1.73 (series 2, vol 8, iss 1, pp. 73–82, May 1974). Text not fetched. |
| [17] OpenAI, PD law, OpenAI Math Release preprint | EXISTS (local copy, 74 pp.); repo path: see WORLD_FINDINGS.md | pd_paper.pdf/.txt; dated "September 24, 2026"; it cites this paper as its [21]. |
| [18] Pilatte, arXiv:2310.19357v3, 25 Aug 2026 | EXISTS-AS-CITED (omits JAMS, C4) | "[v3] Tue, 25 Aug 2026 13:08:40 UTC", comment "Minor typos corrected. 66 pages"; JAMS 10.1090/jams/1084 online 2026-09-10. |
| [19] Pomerance, Mathematika 27(1):84–89, 1980 | EXISTS-AS-CITED | Crossref 10.1112/s0025579300009967. |
| [20] Soundararajan, Ann. Math. 170(2):981–993, 2009 | EXISTS-AS-CITED | Crossref 10.4007/annals.2009.170.981. |
| [21] Tao, 254A notes 1, 23 Nov 2014 | EXISTS-AS-CITED | Live post; title matches; published 2014-11-24T00:51Z (= 23 Nov US time). |
| [22] Tao, 254A notes 2, 9 Dec 2014 | EXISTS-AS-CITED | Live post; title matches; published 2014-12-10T02:05Z (= 9 Dec US time). |
| [23] Tao, Forum Math. Pi 4:e8, 2016, 36 pp. | EXISTS-AS-CITED | Crossref 10.1017/fmp.2016.6 article-number e8; published PDF 36 pp. |

No fabricated version numbers or dates. Every arXiv version cited (B–R v4, H–R v2, Lichtman v1, MR v4, Pilatte v3) exists
with exactly the stated date.

---

## 4. Parameter-dependency table (§2 results whose proofs I re-derived)

| Constant | Fixed where | Depends on | Used where | Claimed independent of |
|---|---|---|---|---|
| A, C (Thm 2.2) | before y → ∞ | — | Cor 2.4 | y, a, r (ineffective). Consistent with Tao Ex. 64. |
| c, C, B, A (Cor 2.4) | before x | — | §5 discrepancy/major arcs | t (\|t\| ≤ L^B), I ⊂ [exp(L^c), x^C], χ. The internal K is chosen after B, c, A; verified: the bound L^{2B}(log a)^{1−K} ≤ L^{2B−c(K−1)}. |
| C, C′, j (Lemma 2.8) | C′ = C′(b, C) fixed **before** A; j chosen after A | b, C | Fourier/Mellin separation everywhere | A (verified: tail ≪ L^{C(j+1)−C′(j−b)}, so with C′ > C fixed, increasing j gives any L^{−A}). |
| η_0, C (Lemma 2.9) | given | — | §7 sieve, Cor 2.10 | h (verified: R_h = Σ_j e_j/a_j ≤ e^{C/η_0}Σ_j C^{(j+1)h+1}/((j+1)h+1)! ≪ e^{−h} once h ≥ h_0(C); constants depend on η_0, C only). |
| h, z, D = z^{4h+2} (Cor 2.10) | h large even, chosen by user | — | rough-integer polynomials (Lemma 5.4 etc.) | z, I (verified: error \|I\|e^{−h} + D). |

Nothing in §1–§2 is circular. Lemma 2.8 is the only result here with an order constraint (C′ before A), and it is stated.

---

## 5. Verified line by line vs skimmed

**Verified line by line (against the primary source, quoted above):**
- All 23 bibliographic entries: metadata, version numbers, dates.
- §1 pp. 1–3, every sentence carrying a citation, including the numerics 15/(32√e) = 0.2843112…, 1 − 0.2961 = 0.7039,
  1/(2√e) = 0.30327.
- Theorem 2.2 vs Tao Ex. 64. Theorem 2.3 vs MV Thm 19.16. Lemma 2.7(i)(ii) vs MV Cor 16.6 / Thm 16.7. (2.2) vs Tao
  Thms 15/26. PNT vs Tao Cor 39 / Ex 40.
- Corollary 2.4's proof (summation over residue classes, partial summation, choice of K).
- Lemma 2.6's proof: diagonal/off-diagonal; |log(n/m)| ≥ |n−m|/Y; Sobolev step producing the (log 2Y)² factor in (2.3).
- Lemma 2.9's telescoping inequality vs Ford–Halberstam Lemma 1 / (5). The identity U_j = C(t−1, h_j). U_j − I_j ≤ E_j.
  The level 4h(+1 ≤ 4h+2) from Σ_j (j+1)2^{−j} = 4. The e_j and a_j bounds. R_h ≪ e^{−h}.
- (4.22)'s counting fraction C(M−m−ℓ, j−m)/C(M, j) = (j)_m(M−j)_ℓ/(M)_{m+ℓ} (checked because it sits next to the
  Efron–Stein citation).
- The companion's import of Thms 3.5/4.1, Cor 3.11, Lemmas 3.4/4.3 (grep plus reading the context).

**Skimmed / taken on trust:**
- The §8 transfer itself (sketch only, under C1; the §8 referee owns it).
- Lemma 2.8's proof beyond the order-of-constants claim.
- Cor 2.10's (2.8) harmonic bound.
- Buchstab 1937 full text (only the zbMATH review).
- MV 1974 (not fetched).
- Whether MV's published 2026 edition keeps the draft's numbering.

---

## 6. Verdict for this scope

**HOLDS AS READ** for the bibliography, §1's attributions and §2's cited forms. There are no FATAL or GAP findings, and
there are 8 cosmetic/unclear notes (C1–C8).

**COULD NOT CHECK:** Montgomery–Vaughan 1974 Theorem 2 / Corollary 3 (paywall plus Cloudflare). This does not matter: the
paper proves its Lemma 2.6 without it.

**THE WORLD** (details and URLs in WORLD_FINDINGS.md): see the summary at the end of this file.
