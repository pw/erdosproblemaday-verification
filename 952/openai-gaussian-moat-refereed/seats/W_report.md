# SEAT W — world, sources, priority — hostile referee report

**Target:** OpenAI, *Bounded-Step Walks on Gaussian Primes* (dated 26 Sep 2026; 29 pp., sha256 a032c3f94f247e90…), Erdős #952.
**Seat:** W (world, sources, priority). Out of scope: the mathematics of §§3–8, which the other seats covered. Where I touch a proof
step, it is only to check that a cited tool is used within its hypotheses.
**Run:** 2026-10-22, about 02:30–03:40Z. Downloads are in `seats/W_src/` (from the earlier W seat) and `seats/W_work/` (mine). Scripts are in `seats/W_work/scripts/`.
Every quote below comes from a source I actually opened. Anything I could not open is marked COULD NOT CHECK.

---

## 0. Release chronology (needed for priority)

| Event | Date | Evidence |
|---|---|---|
| Printed manuscript date | 26 Sep 2026 | Title page of paper.pdf |
| PDF `CreationDate` | 27 Sep 2026 00:00:00 UTC | `pdfinfo src/paper.pdf` |
| Conrad notes "accessed 27 September 2026" | 27 Sep 2026 | Paper's ref. [2]. This access date is one day *after* the printed date (EXPOSITION; harmless) |
| First public appearance | 6 Oct 2026, 14:58:50 −07:00 | `openai/math` initial commit adc7f124 ("Initial commit"). Bloom: "On Tuesday 6th October, OpenAI released a github repository containing 372 significant proof claims" (erdosproblems.com blog, 8 Oct 2026) |
| Later commits fd4aeeb (7 Oct) and 1581d4c (12 Oct) | — | The git tree hash of `lean/OAI/NumberTheory/GaussianMoat` is **c84262a935 at all three commits**. The comparator `.lean/.json`, `docs/028.md`, the preprint folder, `lean-toolchain` and `lake-manifest.json` are also identical. The local `paper.pdf` sha256 equals `src/paper.pdf`. Our clone (1581d4c) is therefore the exact object that FC (adc7f12), RGD (fd4aeeb) and cert-machine checked. |

---

## 1. PRIORITY / NOVELTY

### 1a. Was the problem open before 26 Sep 2026? — **Yes, by every record I could find.**

- **Adamczewski & Bloom, "FrontierMath Erdős", arXiv:2609.25050v1, submitted 6 Sep 2026.**
  - Abstract: "a benchmark of 68 Erdős problems that are open as of August 2026".
  - p. 7 (text line 318): "No proof of any of the 68 conjectures was known as of August 2026".
  - The list includes "Erdos952 — There is an infinite sequence of distinct Gaussian primes with uniformly bounded gaps between consecutive terms".
  - Bloom is the curator of erdosproblems.com, so this is the strongest dated "open" attestation available. It was written three weeks before the manuscript date.
- **Epoch's FME runs on `Erdos952.erdos_952`** (`epoch-research/LeanOpenProblems-results`, committed 2026-09-03): three runs (vega/ultima, $300–$1000 budgets). All are scored `I`.
- **erdosproblems.com/952 discussion thread.** Vjeko_Kovac, 5 Dec 2025: "Last time I checked the literature, it seemed that the claim was still open."
- **Gethner–Stark 1997, p. 289:** "Still open, it has seemingly joined the ranks of the many number theoretic questions that are easy to state but deeply difficult to solve."
- **Wikipedia "Gaussian moat"** (raw text fetched 03:1xZ today) still carries `{{unsolved|…}}` and "remained unsolved as of 1998".
  - On 7 Oct 2026, two edits added the OpenAI claim. **David Eppstein reverted both** (revision log).

### 1b. Earlier claimed resolutions — all disowned by their own authors

arXiv search for "Gaussian moat" (arxiv.org/search, all fields, newest first; 6 results in total, none from 2025–2026):

| arXiv | Author, date | Claim | Author's own comment |
|---|---|---|---|
| 1908.10392 | M. Das, 27 Aug 2019 | negative answer | v2 (6 Sep 2024): "The claim in Theorem 3 is incorrect. The defined paths P_i … do not cover all the Gaussian primes…" (quoted via plasma-ai wiki; consistent with the arXiv search snippet "comment says the claim in Theorem 3 is incorrect") |
| 1901.10016 | M. Das, 28 Jan 2019 | "On the Extension of the Gaussian Moat Problem" | arXiv comment: proofs of Theorems 1 and 2 incorrect |
| 1901.04549 | M. Das, 14 Jan 2019 | algorithm; §8 claims | arXiv comment: §8 claims incorrect |
| 2401.08441 | J. C. Stumpenhusen, 16 Jan 2024 | negative answer | v2 comment: "The width of the moat was not correctly computed" |

None of these is a live prior resolution. The paper cites none of them. That is defensible, since all four were disowned. It is still a small omission in a history paragraph (EXPOSITION).

### 1c. Parallel or later claims (none before 6 Oct 2026)

- **erdosproblems.com/952, re-fetched today at 03:05Z via the Hetzner egress:** "Proof claims (0)" and "No proof claims have been submitted yet." Comments are "suspended".
- **Bloom's blog "Erdős problems in the OpenAI proofs" (8 Oct 2026)** lists #952 as a claim only: "This PDF claims a proof of the following. Any walk on the Gaussian primes, in which the consecutive elements are at most $D$ apart, has $O_D(1)$ many elements … The proof has been formalised."
  - Its general disclaimer reads: "some of the proofs below have appeared online in some form before the 6th October release". The only prior claim named in its comments is for **#184** (Coffey, 1 Oct; Kim, arXiv 2610.07840). Nothing is named for #952.
- **GitHub repository search "gaussian moat"** (5 repos):
  - `buildoak/gaussian-moat-cuda` (Mar–Sep 2026): computations only. Its README says rows are "detector evidence, not origin-component moat proofs".
  - `vibemathing/problem-wikipedia-a554d1594d61b14f` (16 Sep 2026): a research-harness template with no result.
  - Three repos dated after 6 Oct (see next item).
- **Derivative works after the release**, all crediting OpenAI:
  - **Renriviera/quadratic-moats-lean** (created 7 Oct): extends to all quadratic fields.
  - **KitaKen1/erdos-952-binary-form-moat-classification** (10 Oct): a binary-form generalisation and classification. The README says "Solved by: OpenAI" for Conjectures 1–2; its sketch is the OpenAI argument transported via Chebotarev. Disclosure: GPT-6 Astra / GPT-6.1 sol.
  - **femboy2112/SUCC PR #23** (12 Oct): periodic-certificate interface. "No academic priority claimed."
  - **RichardGeorgeDavis/research-artifact-ledger** (12–18 Oct): a rebuild.
  - **plasma-ai/erdos wiki** (7 Oct): a rebuild with axiom check.
  - **carlostoledo1891/cert-machine** (10 Oct): a Comparator run. "Lean default kernel accepts the solution", "nanoda kernel accepts the solution", Lean 4.34.1.
- **Hacker News** (Algolia: "gaussian moat", "\"gaussian moat\"", "\"gaussian primes\""): no proof claim. The only on-topic hits are two March 2026 comments about running moat *solvers*.
- **Tao** (blog search "moat" and "gaussian primes"; RSS for 15–21 Oct; Mastodon to 8 Oct): no post on the moat claim. The erdosproblems page shows "Looks difficult: TerenceTao".
- **Kalai** (RSS): only general posts on the release.
- **Persiflage** (site search "moat"): "Nothing Found".
- **MathOverflow:** answer 515867 (Sawin) only classes "028 (the Gaussian moat conjecture)" among results "with conventional wisdom".
- **Web searches run** (the exact queries):
  - "Gaussian moat problem solved proof" (extended)
  - "\"Gaussian moat\" arXiv 2026"
  - "OpenAI \"Gaussian moat\" Bounded-Step Walks on Gaussian Primes" (extended)
  - "\"Gaussian moat\" proof claim 2025 OR 2026 blog OR github OR mathoverflow"
  - "\"Gaussian moat\" OpenAI proof discussion Tao OR Calegari OR Persiflage OR reddit OR \"Hacker News\"" (extended)
  - "\"erdos_952\" Lean proof formal-conjectures …"

  None surfaced a prior or parallel resolution.
- **Coverage caveat:** the arXiv *API* returned HTTP 429 (rate limit), so arXiv was searched through the listing UI. GitHub code search covers default branches only. Lean Zulip and X/Twitter were not searched.

**Finding 1:** I found no earlier or parallel resolution. Theorem 1.1, if correct, is the first resolution of an open problem whose openness Bloom himself attested on 6 Sep 2026. All post-release work is derivative and credits OpenAI.

### 1d. The three live states, precisely

| Source | State now | Detail |
|---|---|---|
| **erdosproblems.com/952** (dump 00:05Z; re-fetched 03:05Z, text identical) | **No status label is rendered at all.** The problem box is `<div class="problem-text" id=neutral>`. The brief's "shows status open" is not literally on the page. | "Proof claims (0)"; "Comments (5)"; "This page was last edited 08 April 2026"; "Formalised statement? Yes". History page: revisions 2025-10-20 and 2026-04-08 13:11:56 only, both the same text. "Looks difficult: TerenceTao". |
| **teorth/erdosproblems `data/problems.yaml`**, entry `number: "952"` (local copy 00:17Z, identical to a fresh fetch; repo HEAD auto-updated 2026-10-21T10:29Z) | **open** | `status: {state: "open", last_update: "2025-08-31"}`, `informal_status: open`, `formal_status: {state: "unformalized"}`, `formalized: {state: "yes", last_update: "2025-11-21"}`, `comments: "Gaussian moat problem"` |
| **Formal Conjectures `FormalConjectures/ErdosProblems/952.lean`** at main 3b7c94ec (2026-10-21T21:42Z). Last change to this file: 7db2ea3 (14 Oct). The four local copies are byte-identical (sha256 6262ea8c…). | **`research solved`, proof body still `sorry`** | `@[category research solved, question, AMS 11, formal_proof using lean4 at "https://github.com/openai/math/blob/adc7f124…/lean/OAI/NumberTheory/GaussianMoat/Main.lean#L102"] theorem erdos_952 : ¬ ∃ (x : ℕ → GaussianInt) (C : ℤ), Function.Injective x ∧ ∀ n, Prime (x n) ∧ (x (n + 1) - x n).norm < C := by sorry`. Main.lean line 102 is `theorem fullMain : MainEndpoint ∧ UniformEndpoint` (checked). Docstring: "No. This was disproved by an internal OpenAI model in September 2026 [OAI26a]". |

FC history for 952.lean:

| Commit | Date | Change |
|---|---|---|
| bed0441 | 2025-11-21 | added |
| 25379ca | 2026-08-16 | restated as `answer(sorry) ↔` (PR #4992 by Kuberwastaken) |
| 3dfd999 | 2026-10-11 | PR #6898 by mo271: marked solved and linked to fullMain |
| 75a6d3d | 2026-10-14 | `question` attribute added |
| 7db2ea3 | 2026-10-14 | prop-valued `answer(…)` removed, giving the present `¬ ∃` |

The 3dfd999 message says:
> "Reviewer notes: a few links differ from the repository statement by a routine transport that is not in the linked proof: … Erdős 952 (norm vs distance) …"
> "Checked: … every proof link resolves to a `theorem` in the release at the pinned commit (source inspection)"

So FC's tag rests on source inspection, not on a build or a bridge.

---

## 2. ATTRIBUTION in §1 and §1.1 (printed)

Classification is per the brief: FATAL / GAP / ERROR-NONFATAL / EXPOSITION, or VERIFIED.

| # | Paper says (quoted) | Source says (quoted) | Class |
|---|---|---|---|
| A1 | §1: "Gethner and Stark trace the question to Basil Gordon at the 1962 International Congress of Mathematicians in Stockholm [5, p. 289]." | GS 1997, p. 289: "At the 1962 International Congress of Mathematicians in Stockholm, Basil Gordon proposed an analogous journey on the Gaussian primes: starting at the origin…" (GWW 1998, p. 327 says the same.) | **VERIFIED** |
| A2 | §1: "Erdős later credited Gordon and Motzkin, recalling that Motzkin had told him the problem at the Pasadena number theory meeting in November 1963 [4, p. 69]." | Erdős 1977 (LNM 626), printed p. 69: "I did not remember who told me this but E. Straus cleared this up. The conjecture was told me by Motzkin at the Pasadena number theory meeting 1963 November and it was apparently raised by Basil Gordon and Motzkin." | **VERIFIED**, with an EXPOSITION nit: Erdős did not "recall" it himself; he says Straus cleared it up. |
| A3 | Er80 p. 114 ("the answer is almost certainly negative") | Quoted on the erdosproblems page. **The paper does not cite Er80.** | Not cited. COULD NOT CHECK the primary (not needed). |
| A4 | §1: "Gethner, Wagon, and Wick constructed such disks with centers on any line containing two Gaussian integers, and constructed arbitrarily isolated real Gaussian primes; they credit Vardi with an independent proof of the latter result [6, Theorems 4.1 and 4.4]." | GWW 1998 (MAA Chauvenet PDF via Wayback):<br>Thm 4.1: "Let L be a line that contains at least two distinct Gaussian integers and let k be a positive integer. There is a Gaussian integer w on this line such that all Gaussian integers within a distance k of w are composite."<br>Thm 4.4: "For any k > 0 there is a real k-isolated G-prime." Its proof: "I. Vardi [V] has proved this theorem independently." | **VERIFIED** (both theorem numbers and the Vardi credit) |
| A5 | §1: "Tsuchimura obtained a finite bound on the distance reachable with steps of length at most 6 from the origin, adjoined as an initial vertex [13]. This is a result about the component of that vertex." | Tsuchimura, METR 2004-13 (the technical-report version of the cited IEICE 2005 paper, same title and author): "the vertex set is the set of all Gaussian primes augmented by the origin"; "have confirmed the existence of a moat of width k = √36, whereas the best previous result was k = √26 due to Gethner et al."; "search for the farthest point reachable from the origin". | **VERIFIED** against the METR preprint. The IEICE text itself is COULD NOT CHECK (Cloudflare challenge at academic.oup.com). |
| A6 | §1: "Gethner and Stark formulated a bound on the length of a distinct-prime walk that is uniform over its starting point, established periodic obstructions for step bounds √2 and 2, and proposed sieving by small Gaussian primes for larger bounds [5, pp. 290–292]." | GS p. 290, Conjecture: "Given any k > 0, there is an M_k such that taking steps of at most size k and starting on any Gaussian prime one can take at most M_k steps on distinct Gaussian primes…"<br>Same page: "We have proved that such is the case for k = √2 and for k = 2." (√2: sieve by the prime divisors of 65+65i; 2: the lattice generated by 7113990.)<br>p. 291–292: "The method of sieving out small primes to find periodic subsets of a k-moat, for arbitrary k seems hopeful…" | **VERIFIED**. Omission (EXPOSITION): GS p. 290 themselves say "Jordan and Rabung [1976] proved that the conjecture is true for k = √2, with M_k = 48". The paper never mentions JR 1976, which has priority for √2. |
| A7 | §1: "Vardi studied the associated periodic coprimality graphs and the passage from the absence of an infinite walk to a uniform bound on component sizes [14, Section 6, Proposition 6.2]." §2: "The periodicity principle also appears in Vardi [14, Section 6, Proposition 6.2]." | Vardi 1998 (EMIS PostScript via Wayback), §6 "Walks relatively prime to an integer": "Proposition 6.2. If there is no walk to infinity along Gaussian integers relatively prime to N, then there is an upper bound on the largest connected component, so Conjecture 1.2 holds." Also: "This approach reduces a question of infinite walks to a finite problem, and in particular, only a single N needs to be found to prove Conjecture 1.2". | **VERIFIED.** Note: A(P) = Gaussian integers coprime to Q = ∏p, which is exactly Vardi's setting with N = Q. Prop 2.1 is a quantitative version of Vardi's Prop 6.2. |
| A8 | "This proves the uniform form of the Gaussian moat conjecture" (attributed implicitly to GS) | Vardi 1998, p. 276: "Conjecture 1.2. For any k, there is a bound on the largest component of Gaussian primes connected by step size at most k." | EXPOSITION. Theorem 1.1 *is* Vardi's Conjecture 1.2 (and GS's 1997 conjecture). The paper credits GS for the formulation but never names Vardi's Conjecture 1.2. Not wrong. |
| A9 | Jordan–Rabung 1970 (Math. Comp. 24, 221–223) | **Not cited by the paper.** Secondary sources agree on its content: GS p. 289 "Jordan and Rabung [1970] first showed that at least one step of size 4 is necessary on a walk to infinity"; Vardi p. 275 "no walk of step length √10 starting from the origin"; GWW p. 327 "a √10-moat". | Omission (EXPOSITION). COULD NOT CHECK the primary (ams.org 403 from both egresses; Wayback offline). |
| A10 | "methodologically related to Tao's entropy-decrement argument [12, Section 3]" (§1 and §8: "[12, Section 3, Equation (40) and Lemma 17]") | Tao, FMP 4 (2016), §3 "The entropy decrement argument": eq. (40) is H(X_{kH})/kH ≤ H(X_H)/H − I(X_H,Y_H)/H + O(1/k), obtained from "approximate translation invariance" and relative subadditivity. Lemma 17 "(Entropy decrement argument)" iterates (40) and telescopes until "a random variable with negative entropy". | **VERIFIED.** Cited as a methodological relation only; the paper says the components "are established in full within this paper". |

**Attribution verdict:** every attribution the paper makes is accurate where I could check it (A1, A2, A4–A8, A10). The gaps are omissions:
- Jordan–Rabung 1970 (first origin moat).
- Jordan–Rabung 1976 (first uniform bound, for k = √2; credited by GS itself).
- The disowned arXiv claims.
- Vardi's explicit Conjecture 1.2.

All of these are EXPOSITION. None misstates a source.

---

## 3. Cited TOOLS used in the proof

| Tool (paper's citation) | Used as | Source check | Class |
|---|---|---|---|
| Hoeffding [9, Theorem 2, Eq. (2.6)], in Lemma 4.2 | Tail of log P_σ(v) = Σ_i log p_i·1[π_i(σ) ∣ v]: "a sum of independent variables, each of range at most log(2T)" | Hoeffding 1963, p. 16 (page image): "Theorem 2. If X₁,…,X_n are independent and a_i ≤ X_i ≤ b_i (i = 1,…,n), then for t > 0, Pr{X̄ − μ ≥ t} ≤ e^{−2n²t²/Σ(b_i−a_i)²}. (2.6)". | **VERIFIED.** Hypotheses hold: signs are independent; primitivity of v puts at most one factor over each p_i dividing v, so each summand depends on σ_i alone and lies in [0, log 2T]. The mean is ≤ log\|v\| (the paper's bound, with slack 2×). The deviation is ≥ d·log P − log√2 ≥ d·r·log T − O(1). This gives exp(−2(d r log T − O(1))²/(r log²2T)) ≤ exp(−c₀d²r), with absolute c₀ < 2 for large T. Direction and shape are correct. |
| Pinsker [3, Lemma 11.6.1] | D_KL ≥ 2·TV² (natural log), in §3.2 and §6.4 | The paper reproves it ("For completeness": log-sum reduction to Bernoulli, second derivative 1/[u(1−u)] ≥ 4). I checked that self-proof: correct, with TV = P(B) − Q(B) for B = {P > Q}. Cover–Thomas 2nd ed. Lemma 11.6.1 reads D ≥ (1/2 ln 2)‖P−Q‖₁² in bits, which equals 2TV² in nats. | Statement **VERIFIED**. Book numbering COULD NOT CHECK against the text (copyrighted; matches my knowledge). Non-load-bearing because self-proved. |
| PNT in APs, Selberg [11, Eqs. (1.1)–(1.2), p. 66], used for (3.1) | k_T = (1/2+o(1))T/log T, from Σ_{p≤x, p≡1(4)} log p ∼ x/2 | Selberg 1950, p. 66: "(1.1) lim ϑ_{k,l}(x)/x = 1/φ(k)" and "(1.2) ϑ_{k,l}(x) = Σ_{p≤x, p≡l(k)} log p … (k,l) = 1". With k = 4, l = 1 this gives x/2. | **VERIFIED.** The paper's subtraction at T and 2T is correct. **Only the fixed modulus 4 is used anywhere** (grep: the only prime-count inputs are (3.1) and its uses in §6 and §8). Siegel–Walfisz or uniformity in the modulus is not needed and not invoked. |
| Fano-type list bound, Lemma 3.3 ("adapts … [3, Theorem 2.10.1]") | log a − H(X\|Y) ≥ ρ log(a/b) − h(ρ) | The self-proof is correct: H(X\|Y) ≤ H(B) + H(X\|B,Y) ≤ h(ρ) + ρ log b + (1−ρ) log a. Theorem 2.10.1 is Fano's inequality in Cover–Thomas 2nd ed. (from my knowledge). | **VERIFIED** (self-contained). Numbering COULD NOT CHECK against the text. |
| Tao entropy decrement [12] | Methodological only | See A10. | **VERIFIED**, not a black box. |
| Conrad [2, Cor. 7.9, Thms 7.14, 9.7, 9.9] | Split primes: nonassociate conjugate factors of norm p; residue field of size p | Conrad notes (Wayback 2026-10-04):<br>Cor 7.9: Z[i]/(π) is a field.<br>Thm 7.14: "the size of Z[i]/(α) is N(α)".<br>Thm 9.7(ii): "If p ≡ 1 mod 4 then p = ππ̄ is a product of two conjugate primes π, π̄ that are not unit multiples".<br>Thm 9.9: classification. | **VERIFIED** |
| Hatcher [8, §3.3, Thm 3.26(a), Prop 3.29, Ex. 7] | Lemma 4.1 torus-degree argument: "a map omitting a point factors through a punctured torus, whose second homology is zero, and therefore has degree zero" | Hatcher (AT.pdf):<br>Thm 3.26(a): orientable closed n-manifold has H_n ≅ R.<br>Prop 3.29: "If M is a connected noncompact n manifold, then H_i(M;R) = 0 for i ≥ n".<br>§3.3 Ex. 7: defines the degree of a map between closed oriented manifolds. | **VERIFIED** |
| Lugosi [10, Exercise 8, p. 13] (+ BLM "see also") | Binomial lower tail P{Bin(n,λ) ≤ n(λ−δu_p/p)} ≤ exp(−n(δu_p/p)²/(2λ)) in Thm 5.2 | Lugosi, "Concentration-of-measure inequalities", 25 Jun 2009 (Wayback copy of econ.upf.edu/~lugosi/anu.pdf). Exercise 8, on p. 13, ends: "Finally, P{S_n ≤ m(1−ε)} ≤ e^{−mε²/2}" for S_n a sum of independent [0,1] variables with m = E S_n. With m = nλ and ε = δu_p/(pλ), this is exactly the paper's display. The paper also reproves it. | **VERIFIED** (exercise number and page correct) |
| Harper [7] ("see also"), cube edge-isoperimetry (4.?) \|∂_E S\| ≥ \|S\| log₂(2^r/\|S\|) | Lemma 4.2 | The paper proves it by induction. I verified it exhaustively for all nonempty S ⊆ {0,1}^r, r ≤ 4 (65,535 subsets at r = 4; min slack 0, attained at subcubes) — `scripts/cube_iso.py`. Harper's 1964 text not opened. | **VERIFIED** (statement). Harper text COULD NOT CHECK; decorative only. |

**Tools verdict:** every load-bearing cited statement says what is used, under hypotheses the paper satisfies. Three tools (Pinsker, the Fano-list bound, cube isoperimetry) are also re-proved in the paper, so their citations are not load-bearing.

---

## 4. STATEMENT SCOPE

**#952 as phrased:** "Is there an infinite sequence of distinct Gaussian primes x₁, x₂, … such that |x_{n+1} − x_n| ≪ 1?" Here ≪ 1 means an absolute bound. Erdős 1977 has "|y_{n+1} − y_n| < C".

**Theorem 1.1:** "For every finite real D there is a finite B_D such that every connected component of G_D has at most B_D vertices. The bound is independent of the starting prime and includes primes on the coordinate axes."

G_D has *all* irreducible elements as vertices, so associates are distinct vertices. That makes it the maximal reading of "Gaussian primes", and every narrower reading follows by restriction.

| Reading | Covered? |
|---|---|
| Any start point vs. Gordon's origin start (GS p. 289; JR70's \|γ₁\| < M, \|γ_j − γ_{j−1}\| < M, \|γ_j\| → ∞) | Yes. A walk to infinity has infinitely many distinct vertices in one component of G_D (origin start: drop the first step); components are finite. Even non-injective walks with \|γ_j\| → ∞ are covered by component finiteness, not only by the injective form. |
| Strict < C vs. ≤ D; real vs. integer bound | Yes. Every D is covered. |
| "Distinct" read up to associates, first-quadrant only, or norm-prime only | Yes. These are subsets of all irreducibles. |
| Axis primes (p ≡ 3 mod 4, and the ramified 1+i) | Yes, explicitly. |
| FC's norm form ‖x_{n+1} − x_n‖ < C with C ∈ ℤ | Yes, via D = √C. This is the "routine transport" FC flags. Our bridge proves it (§5b). |

**Is this the strongest form?** It is the *uniform* form, which is Vardi 1998 Conjecture 1.2 (= the GS 1997 conjecture). That is stronger than #952 as asked. It is not quantitatively strongest:
- **B_D is nonexplicit.** Paper: "The bound B_D is nonexplicit: the proof chooses sufficiently large scales after fixing D." `lean/docs/028.md`: "No explicit function of D is supplied." Prop 2.1 gives B_D ≤ max{Q², |E| + (K_D−1)|E|Q²} with Q = ∏P_D, but P_D itself is nonexplicit.
- **Observation (mine, not the paper's):** for a given finite P, whether A(P) has an infinite D-walk is decidable. Do a BFS on the period-Q quotient and look for a closed walk with nonzero net displacement; this is our `compute/bfs_all.py` instrument. So Theorem 1.2 implies some valid B_D is *computable* by search, but with no bound on the search.
- **Not addressed:** Vardi's growing-step Conjecture 1.3 (k√log|z| threshold); any explicit origin-moat radius.

**Lean statement:** `MainEndpoint` and `UniformEndpoint` in `ComparatorChallenges/GaussianMoat.lean` match Theorem 1.1:
- irreducibles; Euclidean `dist` in ℂ; injective sequences; every real D;
- the component bound plus a finite-walk-length bound.

I found no reading under which Theorem 1.1 fails to answer #952.

---

## 5. WHAT IS OURS — and whether it duplicates public work

### (a) Kernel replay of OpenAI's 41 modules

**Not a first.** Public replays before ours:
- **plasma-ai/erdos (7 Oct):** "The corpus's verification built the declaration `OAI.GaussianMoat.fullMain` … checked its axioms".
- **carlostoledo1891/cert-machine (10 Oct):** the Comparator run cited in §1c — Lean default and nanoda kernels both accept, Lean 4.34.1.
- **RichardGeorgeDavis (12 Oct):** built at fd4aeeb. "'OAI.GaussianMoat.fullMain' depends on axioms: [propext, Classical.choice, Quot.sound]".
- **FC's reviewers checked by source inspection only.**

Because the GaussianMoat tree is identical at adc7f12, fd4aeeb and 1581d4c, ours is an **independent replication of the same object**. Describe it as replication, not as a first build.

### (b) Bridge `bridge/Bridge952.lean` proving FC's `erdos_952` verbatim from `fullMain.1`

**I found no public duplicate.**
- FC itself keeps `sorry`, and its 3dfd999 notes say the norm→distance transport "is not in the linked proof".
- plasma-ai: "no bridging statement was checked".
- conjectures-io (`owner-accepted-corpus-closures-2026-10-06.json`): `"disposition": "hold_review_new_corpus"`, "Exact statement/assumption bridges and independent verification remain required".
- KitaKen1 proves `Erdos952.erdos_952_openai`. That is a *different*, uniform finite-walk FC-style variant (`False ↔ ∃ C, ∀ N, ∃ x, …`), taken from its own generalisation, not from `fullMain`, and it is not FC's `erdos_952`. Its FC issue #7091 is open, with 0 comments. (Their variant trivially implies `erdos_952`, but they never state it.)
- GitHub code search for `erdos_952` (105 hits) and `GaussianMoat.fullMain`/`MainEndpoint` (≈100 hits) found nothing else proving FC's statement. The `erdos_952` hits I inspected:
  - lean-genius: pre-release, uses axioms.
  - kavanaghpatrick ×2, NexusVerifier: `sorry`.
  - Epoch results: failed pre-release attempts.

**Honest size:** the bridge is a ~10-line square-root monotonicity transport, which FC calls "routine". Its value is that it closes exactly the gap FC recorded. It is not mathematics.

**Two caveats worth stating:**
1. It elaborates FC's statement text under OpenAI's toolchain (Lean v4.34.1, Mathlib d13f23b), not FC's pin (Lean v4.33.1, Mathlib v4.33.1). The statement uses only stable Mathlib constants (`GaussianInt`, `Prime`, `Zsqrtd.norm`, `Function.Injective`), but it is not a build inside FC's tree.
2. The verbatim check compares whitespace-normalised source text (`verbatim.log` MATCH; the mutation `verbatim_mut.log` correctly reports MISMATCH). It is not a term-level comparison.

The bridge's own controls are in place:
- Axioms: `[propext, Classical.choice, Quot.sound]`.
- `sorry` mutation: `sorryAx` detected.
- Drop-injectivity mutation and wrong-step mutation: both fail to compile.

### (c) Miniature check of Theorem 1.2 (`compute/`)

Our D = 1 positive control (P = {5, 13}, Q = 65: "FINITE max_component=580") **reproduces a published 1997/1998 computation**:
- Vardi 1998 §7, Fig. 7: "There is no unbounded walk prime to 2·5·13 of step size √2 … Inspection of the diagram shows that the largest connected component has 580 elements."
- Gethner–Stark's √2 periodic moat with the 65+65i sieve.

Why they coincide: z ↦ (1+i)z + 1 maps step-1 walks on a translate of A({5,13}) onto step-√2 walks on odd Gaussian integers coprime to 65. Odd Gaussian integers are at mutual distance ≥ √2, so the 8-neighbourhood is the only adjacency.

I confirmed numerically (`scripts/vardi130.py`):
- largest component of Z[i] coprime to 130 with step ≤ √2 = **580**;
- A({5,13}) with step ≤ 1 = **580**.

This is a valid positive control, and it independently confirms Vardi's figure. It is **not new**, and the coordinator should label it as a reproduction of Vardi 1998 / GS 1997 when writing it up.

The "none with Q ≤ 4000" results at D = √2 and D = 2 (split primes only) are consistent with GS needing Q = 7113990 (including the primes 2 and 3) for k = 2.

---

## 6. Objections (classified)

1. **EXPOSITION** — Missing history:
   - Jordan–Rabung 1970: the first origin moat, √10, which the forum thread discusses.
   - Jordan–Rabung 1976: proved the uniform bound for k = √2 (GS p. 290: "Jordan and Rabung [1976] proved that the conjecture is true for k = √2, with M_k = 48").

   The paper credits the √2 periodic obstruction only to GS.
2. **EXPOSITION** — Missing disowned prior claims (Das 2019 ×2, Stumpenhusen 2024). Their omission is harmless, but a careful history would note them.
3. **EXPOSITION** — Theorem 1.1 is Vardi's Conjecture 1.2 verbatim in content. The paper credits only GS for the uniform formulation, although it cites Vardi's Prop 6.2.
4. **EXPOSITION** — "Erdős … recalling that Motzkin had told him": Erdős says he "did not remember" and that "E. Straus cleared this up".
5. **EXPOSITION** — Dating: the manuscript is dated 26 Sep 2026, cites a web source "accessed 27 September 2026", has PDF CreationDate 27 Sep, and was first public on 6 Oct 2026. Priority should be dated from the 6 Oct public release, not the printed date.
6. **No ERROR-NONFATAL, GAP or FATAL** found within W's scope.
   - Every cited tool says what is used, with satisfied hypotheses.
   - Every checked attribution is accurate.
   - Theorem 1.1 answers #952 under every reading.

**COULD NOT CHECK** (all non-load-bearing):
- Cover–Thomas numbering (Lemma 11.6.1, Thm 2.10.1) against the book.
- Harper 1964 text.
- Tsuchimura's IEICE text (the METR preprint was checked instead).
- Jordan–Rabung 1970/1976 primaries (not cited by the paper).
- Er80 (not cited).
- Lean Zulip and X/Twitter for parallel claims.

VERDICT: HOLDS AS READ
