# Seat W (WORLD + SOURCES) report — OpenAI family 184, "A logarithmic independence bound for clique-free graphs"
Verdict: HOLDS AS READ (sources + world) — every prior-result sentence matches its source; Theorem 1.1 is exactly AEKS (3) / Erdős #802 (small t, small r trivial);
no competing claim, no public refutation, no revision of the paper. Two EXPOSITION nits only. COULD NOT CHECK: AKS 1980 + Shearer 1983 primary PDFs (ScienceDirect 403;
secondary-verified), Bloom's blog:10 verbatim (erdosproblems.com off-limits per brief), Mathstodon/X directly.

## Key points for the main seat
1. Sources: AEKS p.314 eq.(3) is literally "f(n,t,p) ≥ c_p (n/t) log t" with t = AVERAGE valency, log = max{1,ln}, "for every fixed p", uniform; AEKS Thm 2 = (n/t) log((log t)/p);
   Shearer 1995 Cor. 2 = c'(r) n ln d/(d ln ln d) in AVERAGE degree; Alon Thm 1.1 + Remark (fractional χ); Davies 2609.04654v1 EXISTS and its §3.3 Theorem 17 potential
   Φ = Σw(1+log(ℓ/w)) − CΣw_xw_y specializes (ℓ=C=1) to F_G exactly; KT §3 L3.1–3.2 and Angel–Spinka Thm 2/§2.1 give Lemma 5.1's construction and 2d/(1+d) bound;
   BDKY §2 Thm 8 is the entropy-increment precedent; DKPS Thm30/Cor31, Dhawan Thms1.3/1.4, DMS Thm1.3 all retain log log; DJM Thms 1.4/1.6 are (1−o(1))n log d/d for 3-colourable F only.
2. World: the only technical engagement is Ross Kang's Zenodo "Ode to the AEKS conjecture" (13 Oct 2026): an expert-curated but self-declared "wholly AI-generated" re-derivation that
   ADAPTS OpenAI §§2–5 (T ≤ 256r·M at maximisers; α ≥ 2^-18 n log d/(rd)), says "OpenAI proved", flags no error. Not independent (same architecture). Chen arXiv:2610.15293 uses
   Theorem 1.1 as a black box for r(4,t). Bloom's 8 Oct blog lists 802 as a claim, explicitly no endorsement. openai/math has issues disabled + PRs locked.
3. Status everywhere is still OPEN: FC erdos_802 added 2026-10-20 (PR #7165) as `research open`, no PR to change it; teorth DB 802 "open"; erdosproblems page unedited since Oct 2025.
4. Companion correspondence-colouring paper re-proves the same machinery ("We prove all the ingredients needed here"), does not use Theorem 1.1 as a lemma; it implies AEKS by
   itself (Alon's remark via Chen) but shares the method — not an independent line of defence. Indep paper does not cite it (no circularity).

Started 2026-10-21. Sections filled as checked. AEKS pp. 313–314 also RENDERED (W_work/aeks-1.png, aeks-2.png) to confirm the OCR: (3) prints as
"f(n, t, p) > c_p(n/t) log t" (the scan's relation sign reads '>'/'≧'; same sign as in (2) and (2')), t = (1/n)Σdeg(P) = 2e/n, "log x = max{1, ln x}", "tacitly assume t ≧ 1".

## Part 1 — prior-result sentences vs sources (sources downloaded to W_work/src/)

### 1a. AEKS 1981 [1] (Combinatorica 1(4) 313–317; scan https://renyi.hu/~p_erdos/1981-19.pdf, 5pp, read from OCR + checked)
- Paper §1.1: "In 1981, Ajtai, Erdős, Komlós and Szemerédi conjectured the same order of growth for each fixed forbidden clique [1, p. 314, Equation (3)]."
  Source p. 314: "Denote by f(n, t, p) the largest integer such that every graph of n vertices and average valency t that contains no K_p satisfies α ≥ f(n,t,p). ...
  It is possible that for every fixed p we have (3) f(n, t, p) ≥ c_p (n/t) log t. Perhaps (3) is too optimistic, but we feel that it is an interesting and
  challenging question." ... "we cannot decide whether (3) is true or not even in the case p=4."
  Notation p. 313: "t = t(G) = (1/n)Σ deg(P) = 2e/n = average valency in G (we will tacitly assume t ≥ 1)"; "log x = max{1, ln x}".
  VERDICT: matches. AVERAGE degree (not max degree), uniform in n and t (no "t→∞"), every fixed p (p = 3 is their Theorem 1, so the open content is p ≥ 4 —
  exactly Theorem 1.1's r ≥ 4). AEKS's log is max{1, ln x}; for t ≥ 2 this is within a factor 1/ln 2 of ln t, and for 1 ≤ t < 2 (3) is Turán
  (α ≥ n/(t+1) ≥ n/(2t)). So Theorem 1.1 (d ≥ 2, natural log) ⇔ (3) for every p ≥ 4 up to the constant. No discrepancy. (Note AEKS phrase it as a
  question "It is possible that…", the paper calls it a conjecture — standard; Alon 1996 and Shearer 1995 also call it the AEKS conjecture.)
- "They proved the lower bound Ω_r(n log log d/d) as d → ∞": source Theorem 2 (p. 314): "There is an absolute constant c_1 such that (4) f(n,t,p) ≥ c_1 (n/t) log A,
  where A = (log t)/p." For fixed p, log((log t)/p) = log log t − log p = Ω_p(log log t) as t → ∞. MATCHES (AEKS is actually uniform in p with absolute c_1, slightly stronger
  than quoted). Alon 1996 states it as c(r)(n/t) log log(t+1) — same.
- "The order n log d/d is best possible up to a constant factor even for triangle-free graphs ... [1, pp. 314–315]": p. 314 "(2) is best possible up to
  constant multiple" [(2) = α ≥ 0.01 (n/t) log t for triangle-free]; p. 315 (Spencer's remark) uses "a trianglefree graph G' on n' points with average valency t',
  10 < t' < (n')^{1/3}, and independence number α' < c(n'/t') log t'. (That such a graph exists is mentioned in [3] – take a random graph and delete the few
  vertices in triangles.)" MATCHES. EXPOSITION-level nit only: tightness holds in the sparse regime (AEKS: t' < n'^{1/3}); for d of order n the bound is
  not tight (triangle-free ⇒ α ≥ Δ ≥ d). Standard usage; not an error.
- "The recursive use of clique-free neighborhoods goes back to the sparse-subgraph argument of AEKS [1, Section 3]" (§2.2): AEKS §3 "Sparse Subgraph Lemma":
  induction on p, "let H' be the neighbourhood of P. It contains no K_{p−1}". MATCHES.

### 1b. Shearer 1995 [15] (RSA 7(3) 269–271; Toronto mirror, pages rendered — pdftotext garbles the fractions)
- Paper: "Shearer [15, Corollary 2] improved this to Ω_r(n log d/(d log log d)), again in terms of the average degree."
  Source p. 271: "Corollary 2. Let G be a graph on n points with average degree d and which contains no K_r (r ≥ 4). ... Then, for large d, α ≥ c'(r) n ln d/(d ln ln d)."
  (Proof: delete the ≤ n/2 vertices of degree > 2d, apply Corollary 1 [max degree].) MATCHES — AVERAGE degree, r ≥ 4, "for large d".
  Shearer p. 269 also states the open question: "it does not settle the question (asked in [1]) of whether α ≥ c'(r) n ln d/d".

### 1c. Alon 1996 [3] (RSA 9(3) 271–278; author PDF)
- Paper: "Alon [3, Theorem 1.1 and the remark following its proof] treated graphs whose neighborhoods have bounded chromatic number, obtaining an average-degree
  bound of the required order. His argument also admits bounded fractional chromatic number in each neighborhood."
  Source: "Theorem 1.1 Let G be a graph on n vertices with average degree t ≥ 1 in which for every vertex v the induced subgraph on the set of all neighbors of v is
  r-colorable. Then the independence number of G is at least (c/log(r+1)) (n/t) log t". "Remark. ... In particular it suffices to assume that the chromatic number
  (or even the fractional chromatic number) of the induced subgraph of G on the neighborhood of any vertex is at most r." MATCHES. (Alon p. 1 also restates the AEKS
  conjecture in average degree and calls it "still open".)

### 1d. Davies, "Random independent sets and local sparsity", arXiv:2609.04654 — EXISTS (v1, 4 Sep 2026, 31 pp; dated 3 Sep 2026)
- Paper §2.1: "The functional below is the unit-parameter specialization of the entropy-minus-edge potential used by Davies [6, Section 3.3, proof of Theorem 17]."
  Source §3.3 (p. 20), proof of Theorem 17: "define the potential Φ_H(w) = Σ_x w(x)(1 + log(ℓ_x/w(x))) − C Σ_{xy∈E(H)} w(x)w(y)", with ℓ_x = log(1+λ_x),
  C = e^{aL}; maximizer satisfies (3.8) "log(ℓ_x/w(x)) = C Σ_{y∈N(x)} w(y)". Setting ℓ_x ≡ 1, C = 1 gives exactly F_G(w) = Σ w(1 − log w) − M_G(w) and the
  stationarity (2.1) log(1/w_v) = w(N(v)). ATTRIBUTION ACCURATE (and Lemma 2.1's existence/positivity argument mirrors Davies' "tends to −∞ ... no maximizing
  coordinate is zero" paragraph). Davies uses Φ to lower-bound log Z_G(λ) (independence polynomial), under mad(G[N(v)]) ≤ a — a different use.
- Paper §1.1: "Davies [6, Theorems 1 and 3] establishes weighted local versions: he bounds individual vertex inclusion probabilities in a random independent set
  under bounded neighborhood maximum average degree or fractional chromatic number." Source Thm 1: mad(G[N(v)]) ≤ a ⇒ distribution μ with μ(v) ≥ (1−o(1)) log d_w(v)/d_w(v);
  Thm 3: fractionally r-colorable neighborhoods ⇒ μ(v) ≥ (1−o(1)) log d_w(v)/(K(r) d_w(v)). MATCHES.
- Overlap with Theorem 1.1? NO. Every Davies hypothesis (bounded neighbourhood mad, Θ(G) ≤ b [weighted triangle density sup over ALL weights], fractionally
  r-colourable neighbourhoods) fails for general K_4-free graphs (a K_4-free graph's neighbourhoods are arbitrary triangle-free graphs: unbounded mad and unbounded
  fractional chromatic number). Davies never mentions the AEKS conjecture. Davies' ref [11] = "E Davies, A Dhawan, D Gallardo, A Methuku, H Nguyen, J Seo, S Spiro.
  Fractional colorings of K_r-free graphs with local demands. To appear. 2026." — a live adjacent project (checked in Part 2).
  Note Davies Θ(G) (Thm 2) is a sup over all weights of 6T/D; Theorem 1.1's central step bounds T ≤ C_r M only at the F-maximizer (+ cross-mass property) — that is
  the new idea, not in Davies.

### 1e. DKPS [7] arXiv:2003.14361v1 — Theorem 30, Corollary 31 (§7 "Bounded clique number")
- Source Cor 31: "For any graph G of clique number ω and maximum degree Δ ... α(G) ≥ (1−o(1))|V(G)| max{ log Δ/((ω−2)Δ log log Δ), (1/2Δ) sqrt(log Δ/log(ω−1)) }" as Δ→∞;
  Thm 30 adds fractional/correspondence colouring. DKPS themselves: "this therefore constitutes the best progress towards ... the conjecture of AEKS ...
  [they] would have had little interest in an increased leading constant, but rather in the removal of the stubborn log log Δ factor".
  Paper's "improves constants and also gives coloring estimates ... retain a log log loss" — MATCHES (max-degree parameter; "relevant degree parameter" wording covers it).

### 1f. Dhawan [8] (Ann. Comb. 30 (2026) 277–304 = arXiv:2403.03054, current v3 21 Jul 2025)
- Thm 1.3: (k, r+1)-sparse [≤ n d^{εr}/(r+1) copies of K_{r+1} globally], average degree d ⇒ α ≥ (1−o(1)) n/(9ηd), η = ε + r log log d/log d.
  Thm 1.4: (Δ^{εr}, r)-locally-sparse [≤ Δ^{εr} r-cliques in each neighbourhood], max degree Δ ⇒ α ≥ (1−o(1)) n/(ηΔ).
  At ε = 0 both give n log d/(r d log log d): log log loss retained. MATCHES. EXPOSITION nit: "allows bounded numbers of cliques" — the allowed counts are
  d^{εr}/Δ^{εr}, i.e. polynomially growing, not bounded; "few"/"a controlled number" would be precise. (Theorem numbers checked on arXiv v3; journal numbering not seen.)

### 1g. DJM [9] arXiv:2511.17191v2 (4 Dec 2025)
- Source Thm 1.4: "Let F be a 3-colorable graph. Then, for any F-free graph G of maximum degree Δ and average degree d, α(G) ≥ (1 − o(1)) n log d/d" ;
  Thm 1.6: "For all ε > 0 and t ∈ N, there exists d_0 such that ... for all d ≥ d_0 and n ∈ N. Any n-vertex K_{t,t,t}-free graph G of average degree d satisfies
  α(G) ≥ (1 − ε) n log d/d." Paper's "(1−o(1)) n log d/d as d → ∞, uniformly in n ... leading coefficient 1 in that restricted class" — MATCHES.
  "complete tripartite graphs ... are K_4-free and contain every fixed three-colorable graph once their parts are large enough" — correct (K_{t,t,t} ⊇ F for t = |V(F)|).
  NB DJM's Conjecture 1.1 attributes to AEKS a statement "for every fixed graph F" (with (c_1(F) − o(1))); AEKS p. 314 only poses it for cliques K_p.
  The paper under review quotes AEKS correctly (cliques only).

### 1h. Dutta–Mubayi–Subramanian [10] (SIDMA 26 (2012))
- Source Thm 1.3: "For every ε ∈ (0,1) and r ≥ 4 ... Every K_r-free graph G with average degree D has independence number at least c (log D/log log D) Σ_v 1/max{D^ε, d(v)}."
  Paper's "bounds involving the full degree sequence ... retain a log log loss" — MATCHES.

### 1i. Kleinberg–Tardos [11] (JACM 49 (2002)) §3, Lemmas 3.1, 3.2
- Source §3 (p. 624): "In a single phase, we pick a label a uniformly at random, and a real number α uniformly in [0,1]. For each object p that currently has no label
  assignment, we give it the label a if α ≤ x_pa." Lemma 3.1: assigned label a w.p. exactly x_pa overall; any label w.p. 1/k per phase. Lemma 3.2: separation prob ≤ 2z_e
  = Σ_a |x_pa − x_qa| = 2·TV. This is exactly the construction in the paper's Lemma 5.1 (uniform Z_t on J, uniform U_t, accept if U_t ≤ p_i(Z_t)). MATCHES.
  (The bib URL focs99-mrf.pdf serves the JACM version, pp. 616–639 — consistent with the bib entry.)

### 1j. Angel–Spinka [4] arXiv:1903.00632v2 — Theorem 2, §2.1
- Source Thm 2: "there exists a coupling of the variables in S such that, for any X, Y ∈ S, P(X ≠ Y) ≤ 2d_TV(X,Y)/(1 + d_TV(X,Y))." §2.1 "Coupling I" (rejection sampling /
  Poisson process): "in the case of distributions on a finite set, Coupling I simplifies to the Kleinberg–Tardos rounding scheme"; "Lemma 3.2 of [6] gives Theorem 2 ...
  with the slightly worse bound 2d_TV". The paper's Lemma 5.1 bound 2d/(1+d) and attribution MATCH. I also re-derived the bound: at the first trial accepted by
  either row, P(both accept | one accepts) = Σmin/Σmax = (1−d)/(1+d) [Σmin = 1−d, Σmax = 1+d], so P(Y_i ≠ Y_i') ≤ 1 − (1−d)/(1+d) = 2d/(1+d). Correct.

### 1k. Benjamini–Duminil-Copin–Kozma–Yadin [5] (Ann. Probab. 43 (2015); arXiv:1111.4853v2) §2 "The entropy argument"
- Source Lemma 7 / Theorem 8: Σ_y P(Y=y) Δ²(L(X), L(X|Y=y)) ≤ 2(H(X)+H(Y)−H(X,Y)); "E(Δ_n(ρ,X_1)²) ≤ 2(H_n − H_{n−1})" — entropy increments control
  averaged (Δ ≥ TV-type) distances between walk distributions from neighbouring starts. Paper (§4): "The use of entropy increments to control averaged distances
  between walk distributions has a precedent in BDKY [Section 2]." MATCHES.

### 1l. AKS 1980 [2] and Shearer 1983 [14] — primary PDFs NOT retrieved (ScienceDirect 403 from this box)
- "AKS [2] proved the logarithmic improvement when triangles are excluded": corroborated by AEKS p. 314 ("formulated by Ajtai, Komlós and Szemerédi in [2] and [3]
  as follows: Theorem 1. If G is trianglefree then (1) can be improved to (2) α ≥ 0.01 (n/t) log t", [3] = AKS 1980 JCTA 29), Alon 1996 §1, DMS §1.1.
- "Shearer [14] ... asymptotic coefficient 1: triangle-free graphs of average degree d → ∞ have independent sets of size at least (1−o(1)) n log d/d": corroborated
  by Davies 2609.04654 §1 ("Shearer's theorem giving ... lower bound on the independence number of a triangle-free graph of given AVERAGE degree [32]"; f(x) =
  (x log x − x + 1)/(x−1)² "is Shearer's function [32]") and DJM §1.1. Standard; marked SECONDARY-VERIFIED only.

### Part 1 summary
Every prior-result sentence in §1/§1.1 (and the in-body attributions in §2.1, §2.2, §4, §5.1) matches its source as quoted. No misattribution, no
average-vs-max-degree slip, no wrong theorem number found. Two EXPOSITION nits only: (i) "best possible up to a constant factor" holds in the sparse
regime d ≤ n^{1/3} (AEKS p. 315), not for all d relative to n; (ii) Dhawan's hypotheses allow d^{εr}/Δ^{εr} cliques — "bounded numbers" overstates.

## Part 2 — WORLD (as of 2026-10-21)

### 2a. The artifact itself is unrevised
- github.com/openai/math: repo created 2026-10-06; HEAD 1581d4c (2026-10-12) = our local clone HEAD. The 184-indep paper directory has ONE commit (adc7f12, initial,
  2026-10-06); the 2026-10-08 "Update manuscripts and Lean formalizations" commit (the one that followed the Weil-class withdrawals) touched NO file of family 184
  (indep, corr, lean/OAI/Combinatorics/CliqueFree, ComparatorChallenges/CliqueFreeLog). sha256 of indep.pdf 15717a7c… = current.
- Issues are DISABLED on openai/math and PR conversations are auto-locked (PR #2, 2026-10-12). Total issues+PRs ever: 2 (both OpenAI's own). So there is no public
  GitHub venue where anyone could have refereed it.

### 2b. Independent/derivative engagement found
1. **Ross J. Kang (U. Amsterdam; DKPS co-author), "Ode to the Ajtai-Erdős-Komlós-Szemerédi conjecture", Zenodo 10.5281/zenodo.23351325, v1 13 Oct 2026, 32 pp**
   (W_work/world/kang.pdf, md5 709b4763…). Abstract: "For a K_r-free graph on n vertices of average degree d ≥ 2, where r ≥ 4, we bound the mean size of a uniformly
   chosen independent set, and hence the independence number, below by absolute constant multiples of n log d/(rd) and (n/d)√(log d/log(e + r/√log d))."
   - States plainly: "OpenAI proved α(G) = Ω_r(n log d/d) in A logarithmic independence bound for clique-free graphs [28, Theorem 1.1]." It "adapt[s] OpenAI's
     structural argument [28, Sections 2–5]" — same functional (from Davies), cross-mass bound from global maximality (its (13): e_q(S,T) ≤ 4q(S)log(e+q(S∪T))+1
     with q = w/r), preservation under splitting [28, Lemma 3.2], triangle control from cross mass [28, Thm 3.1], refined splitting [28, Lemma 5.3] (e^ℓ → e^{ℓ/2},
     lazy walks K = (P^m+P^{m+1})/2, m = ⌈ℓ³⌉), giving T ≤ 256 r · M at global maximisers (its Theorem C) and α ≥ 2^{-18} n log d/(rd) (its Theorem A).
   - It reports NO error, gap or correction in OpenAI's manuscript (grepped: every [28] citation is "adapt"/"refinement"; the only "corrected" item is a lemma of
     Bansal–Gupta–Guruganesh, unrelated). It says the 1/r dependence "is new relative to that manuscript, whose coefficient depends on its terminal splitting threshold."
   - CAVEAT, load-bearing: its "AI declaration" says it is "wholly AI-generated" — Kang "adversarially carr[ied] out a 'rinsing' process" of OpenAI's output with
     "a closed-weight commercial agentic generative AI system", left in structured-proof (Lamport) format, unrefereed. So it is an AI re-derivation curated by an
     expert, NOT an independent human verification — and it shares the same proof architecture, so a flaw in that architecture would likely be inherited, not caught.
     It is nonetheless the strongest external signal: an expert in exactly this area chose to build on the argument rather than flag it.
2. **Kaizhe Chen (Princeton), "A note on the logarithmic exponent of Ramsey number r(4,t)", arXiv:2610.15293v1 (11 Oct 2026)** — uses Theorem 1.1 as a black box:
   "Lemma 1.3 ([9]). For any fixed integer s ≥ 4, there exists c_s > 0 such that every K_s-free graph G on n vertices with average degree d ≥ 2 satisfies α(G) ≥ c_s n log d/d"
   ([9] = this paper) to get r(4,t) = t³/(log t)^{2+o(1)} from OpenAI's r(5,t)/r(s,t) papers. "Solely for informal circulation." Acknowledges Noga Alon "for pointing out
   that the coloring theorem in [10] [the companion] allows us to avoid the log log t loss". So the result is already being used downstream; no scrutiny of it.
3. **Thomas Bloom, erdosproblems.com blog "Erdős problems in the OpenAI proofs" (thread blog:10, 8 Oct 2026)** — lists 802 among ~23–25 Erdős problems with OpenAI claims.
   Per search snippets + OfficeChai summary (I did NOT fetch erdosproblems.com, per brief): post is "a summary of claims and not an endorsement"; Bloom "hasn't yet looked
   seriously at any of the proofs", "hasn't checked that the Lean formalisations compile or that the formal statements capture the original problems"; expects
   "most to be correct". (For a different problem, #3, the snippet says "the Lean file ... appears to prove [a] weaker bound than the one claimed in the PDF" — the
   failure mode seat L should rule out for 802; my reading of CliqueFreeLog.lean in 3b says the 802 comparator statement is faithful.)
   → Main seat: if you want this blog's 802 paragraph verbatim, save forum/thread/blog:10 from a machine that can reach the site.
4. Press (implicator.ai, aiweekly, tech-insider, Retraction Watch via secondary): coverage of the 722-manuscript/372-family drop and the 10-07 withdrawal of three
   Weil-class manuscripts + 14 revisions. None names family 184 among withdrawn/revised (consistent with git: 184 untouched).

### 2c. No competing/independent claim found
- arXiv/WebSearch over 2025–2026 for "Ajtai–Erdős–Komlós–Szemerédi conjecture", "independence number K_r-free log d/d", "clique-free graphs independence number
  logarithmic": no non-OpenAI proof claim of the AEKS conjecture. Closest prior progress: DJM arXiv:2511.17191 (3-colourable F only), Dhawan, DKPS, Davies — all
  checked in Part 1, none covers K_4-free. Pending (Davies' ref [11]): "Davies, Dhawan, Gallardo, Methuku, Nguyen, Seo, Spiro — Fractional colorings of K_r-free
  graphs with local demands. To appear. 2026." — not found online yet; would be the natural venue for an independent expert check/overlap.
- No public refutation, criticism or reproduction failure of family 184 found anywhere (GitHub, arXiv, Zenodo, press, Bloom's post).
- Mathstodon / X: WebSearch surfaced nothing specific to 802/184; not exhaustively searchable from here (COULD NOT CHECK social media directly).

### 2d. Formal Conjectures (google-deepmind/formal-conjectures, main)
- FormalConjectures/ErdosProblems/802.lean was ADDED only on 2026-10-20 (commit fd095e0, PR #7165 by mnn31, opened 2026-10-11, merged 2026-10-20; fixes issue #952 of
  2025-10-11). Main statement `erdos_802` tagged `@[category research open, question, AMS 5]`:
  `∀ r : ℕ, ∃ c > 0, ∀ n, ∀ G : SimpleGraph (Fin n), G.CliqueFree r → c * (log G.averageDegree / G.averageDegree) * n ≤ G.indepNum` (with sorry).
  Variants aeks / shearer (with 2 ≤ t) / r_eq_three / alon tagged research solved. PR description and review (bocowgill, Paul-Lez) make NO mention of OpenAI's claim.
- No open PR changing 802's status (searched PRs/issues for "802", "erdos_802", "AEKS", "Ajtai", "OpenAI"; the OpenAI-related FC PRs found concern other problems,
  e.g. #6896 circulant Hadamard, #7314 Erdős 821, #7340 Erdős 604).
- teorth/erdosproblems data/problems.yaml (main, auto-updated 2026-10-20T22:19Z): 802 → status "open" (last_update 2025-08-31), informal_status open,
  formal_status "unformalized" (no formal proof recorded), formalized: "yes" (statement, 2026-10-20). No issue/PR mentions 802.
- erdosproblems.com/802 (main seat's saved copy, accessed 2026-10-21): "last edited 26 October 2025"; text still lists AEKS/Shearer/AKS/Alon only; "Proof claims (0)";
  comments thread has only Quanyu Tang's 2025 typo fix; new comments suspended.

### 2e. Companion paper "Correspondence coloring graphs with a forbidden clique" (OpenAI, 5 Oct 2026) — dependency direction
- Companion Theorem 1.1: K_r-free, Δ ≥ Δ_r ⇒ χ_DP(G) ≤ C_r Δ/log Δ (AKS coloring conjecture). It cites the indep paper as [22] and says: "The structural argument
  develops the multiplier and entropy-splitting methods of the companion manuscript ... [22, Sections 2–5]. We prove all the ingredients needed here." and
  "We establish the required weighted and dual estimates directly." ⇒ it does NOT use Theorem 1.1 as a lemma (logically independent), but it RE-USES the same core
  technique (cross mass → splitting via neighbourhood walks + shared rejection coupling → triangle mass ≤ C·edge mass), in a priced/dyadic-level variant.
- The indep paper (dated 25 Sep, earlier) does not cite the companion at all; its sentence "Neither companion is an input to the proof" refers to the two Ramsey
  papers [RamseyFive, RamseyFixed]. So no circularity.
- Consequence for refereeing: the companion implies AEKS independently of Theorem 1.1's proof TEXT (χ ≤ C_rΔ/logΔ ⇒ α ≥ n log Δ/(C_rΔ); truncate to degree ≤ 2d —
  exactly the route Chen/Alon note), but NOT independently of its METHOD. A fatal flaw in §3–§5's splitting/entropy argument would plausibly sink both; the companion
  is not a second line of defence. (Not refereed here per brief.)

## Part 3 — Is erdosproblems.com/802 exactly Theorem 1.1?
Problem text (saved copy): "Is it true that any K_r-free graph on n vertices with average degree t contains an independent set on ≫_r (log t/t) n many vertices?"
Theorem 1.1: r ≥ 4, finite simple K_r-free, n vertices, average degree d ≥ 2 ⇒ α ≥ c_r n log d/d, c_r depending only on r.
- Degree parameter: both AVERAGE degree (2|E|/n). ✓ Constant: depends only on r, uniform in n and t. ✓ (Quantifier order in the comparator
  CliqueFreeLog.lean is also right: r, hr fixed → ∃ c > 0 → ∀ V G.)
- r range: problem says "K_r-free" with no range. r ≤ 2 trivial (r = 2: edgeless, t = 0); r = 3 is AKS and is ALSO covered by Theorem 1.1 at r = 4 since K_3-free ⇒ K_4-free
  (take c_3 = c_4). So "r ≥ 4" loses nothing. ✓
- Small t (the only subtlety): Theorem 1.1 needs d ≥ 2; the problem has no lower bound on t.
  · t = 0 (edgeless): log 0 undefined (−∞); vacuous/trivial (α = n). In Lean (FC erdos_802) log 0 = 0 and 0/0 = 0, so LHS = 0. ✓
  · 0 < t ≤ 1: log t ≤ 0, RHS ≤ 0, trivial. ✓
  · 1 < t < 2: Turán/Caro–Wei α ≥ n/(t+1), and sup_{1<t≤2} (ln t)(t+1)/t = 1.0397 (at t = 2, computed), so the problem's bound holds with any c ≤ 1/1.04.
  · 2 ≤ t < e: inside Theorem 1.1 (ln t ∈ [0.693, 1), no degeneracy). The only t-range where log t/t behaves badly is t → 1⁺ / t ≤ 1, where the bound is trivial.
  Hence #802 ⇔ (Theorem 1.1) ∧ (Turán bound) ∧ (monotonicity in r): a positive answer, with c = min(c_4, …, 1/1.04)-type constants. No hidden gap.
  AEKS's own convention log x = max{1, ln x} with "tacitly assume t ≥ 1" makes the same point: for 1 ≤ t ≤ e their (3) is just Turán.
- Formal statement (FC erdos_802): ∀ r ∈ ℕ (incl. 0..3), ∀ n, all t incl. t < 2. Deriving it from OpenAI's comparator theorem needs exactly the bridging above:
  CliqueFree.mono for r < 4 and a Turán/Caro–Wei lemma for t < 2 (I did not find a Caro–Wei/Turán independence lemma in the Mathlib checkout on this box —
  /tmp/erdos85-1019/.../Mathlib/Combinatorics/SimpleGraph has no such theorem; so this bridge is mathematically trivial but not free in Lean).
  FC's `averageDegree` (ℚ, Σ deg/|V|) vs OAI's `averageDegree` (ℝ, 2|E|/|V|) agree by the handshake lemma. These are formal-plumbing notes, not gaps in the paper.
- Note on DJM's restatement: DJM's "Conjecture 1.1 (AEKS)" is for every fixed graph F; AEKS only posed it for K_p. Equivalent anyway (every F ⊆ K_{|F|}),
  so Theorem 1.1 settles DJM's Conjecture 1.1 too.

## Files
- Sources: /tmp/oaimath/184/seats/W_work/src/ (aeks1981, shearer1995, alon1996, kt, dms, arx_2609.04654 Davies, arx_2511.17191 DJM, arx_2003.14361 DKPS,
  arx_1903.00632 Angel–Spinka, arx_1111.4853 BDKY, arx_2403.03054 Dhawan; .pdf + .txt)
- World: /tmp/oaimath/184/seats/W_work/world/ (kang.pdf/.txt Zenodo 23351325; arx_2610.15293 + r4t.txt Chen; fc802.lean FC main; problems.yaml teorth;
  arx_2603.17730 + dh.txt Dhawan v4; hajlasz.html catalogue snapshot 12 Oct, lists 184-indep as "status current", no verification column)
- Current-version check (arxiv abs pages, 2026-10-21): Davies v1, DJM v2, DKPS v1, Angel–Spinka v2, BDKY v2, Dhawan v3 — all = versions cited.
