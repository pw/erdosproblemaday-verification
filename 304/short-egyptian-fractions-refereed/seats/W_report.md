# Seat W (world and sources): report on OpenAI, "Short Egyptian fractions" (dated 25 Sep 2026)

Scope: how the paper relates to the literature and the live record. This seat did not referee the mathematics line by line.
Paper version: the PDF in `/tmp/oaimath/025/src` is byte-identical (md5 23cd0308…) to `openai/math` initial commit
adc7f1241 (2026-10-06). The 2026-10-07 update did not touch this preprint, so the **public release date is 2026-10-06**,
although the paper is dated 25 Sep.
Sources fetched are in `seats/W_src/` and small scripts in `seats/W_code/`. Every source was read from primary text unless a line says otherwise.

## 1. Citation-by-citation check

| Cite (as printed) | Used for | Source read | Verdict |
|---|---|---|---|
| [6] Erdős 1950, p.195 Thm 1 | N(b) ≪ log b/log log b; de Bruijn's log b/log log log b | renyi.hu scan, p.195 image | **Holds.** p.195: de Bruijn's bound `N(a,b) < c log b/log log log b`; "1. TÉTEL … N(a,b) < c₁ log b/log log b … bármely 0<a<b". N(a,b) is defined on p.193 (after Nakayama) with distinct denominators `0<x₁<…<xₙ` (3), as in the paper. |
| [6] p.195 Thm 2 | lower order, already at a=b−1; conjecture | same | **Holds.** (7) `N(b−1,b) > log log b − 1` for every b; (6) is the average `>(1/2)(log log b −1)`. The conjecture `N(a,b) < c′ log log b` is stated just above Theorem 2 ("Valószínűnek tartom…"). |
| [6] §1 pp.199–203 | factorial-divisor construction | pp.198–203 images | **Holds.** §1 starts on p.198 with the greedy proof of (4). The construction is on pp.199–203: "1. Segédtétel" (every z<n! is a sum of ≤n distinct divisors of n!) is on p.199, and the proof of Thm 1 via u_i=n!/d_i, v_j=n!b/d′_j is on pp.201–203. §2 begins on p.203. |
| [8] Erdős–Graham pp.32, 35, 37–38 | the three problems | ucsd scan (pdf p = book p + 4) | **Holds.** p.32 asks for "asymptotic formulas or even good inequalities for \|𝒳ₙ\|". p.35 has v(n) (see §3). On p.37, N(b) gets "Even showing N(b)=o(log b/log log b) would be of interest". On p.38: "…perhaps even (log n)^c, which would then imply N(b) < c′ log log b". The paper's "pp. 37–38" is more accurate than the site's "p.37". |
| [23] Vose 1985 | N(b) ≪ √log b | Wiley paywalled/bot-walled. **Primary COULD NOT CHECK.** zbMATH 0558.10015 review: "He proves that n ≪ √log b", for 0<x₁<…<xₙ with n minimal, uniform in a/b<1 | Holds (secondary). |
| [22, Lemma 2.2] vDT | explicit modern Vose statement | arXiv 2512.22083**v2** (current, 24 May 2026; v1 26 Dec 2025, same lemma numbering) | **Holds.** Lemma 2.2: "for all fractions a/b∈(0,1) … r+s ≤ C√log b". Footnote: p_i≥5 is not in Vose and is taken from Vose 1984 Lemma 3; definitions are "cosmetically" different. |
| [22, Thm 1.1] | v(k) ≥ exp(ck²) | same | **Holds** ("for all positive integers k", absolute c). |
| [22, Lemma 2.1] | marker-preserving padding | same | **Holds.** "For all k≥2, D_k ⊆ D_{k+1}." The paper's Lemma 7.2 (r≥3) reproves it. Its prime case is slightly cleaner: it shows both exceptional values v=p+1 and v=p(p+1) are impossible by a p-adic argument (p odd), where vDT keep the second case and split n_{k−2}. Brute check over all 2,399 expansions with k=3..6 found 0 prime-exceptional cases, and D₃⊆D₄⊆D₅⊆D₆. |
| [22, §3] | anticipated connection | same | **Holds.** §3: "If, however, (3.2) holds, it seems likely that our lower bound on v(k) can be improved to e^{e^{ck}}." |
| [21] Tenenbaum–Yokota 1990, Thm p.151; Lemma 4, §3 | (1+ε) log b/log log b terms, denominators ≤ 4b(log b)² log log b | **Primary COULD NOT CHECK.** tenenb.perso.math.cnrs.fr times out from three networks and ScienceDirect shows a visible captcha (stopped there, per rule). zbMATH 0713.11029: "r ≤ (1+o(1)) log N/log₂N and n_r ≤ 4N log²N log₂N" | Theorem holds (secondary). Page 151 and Lemma 4/§3 unverified. Background only, not load-bearing. |
| [14] Konyagin 2014, Thm 1; p.312 padding | k/log k lower order; injection F(k)≤F(k+1) | **Primary COULD NOT CHECK** (mathnet.ru unreachable from exe.dev, Hetzner and the home Mac; Springer bot-walled; zbMATH review licence-blocked). Crossref: Mat. Zametki **95(2), 312–316** = paper's citation (English: Math. Notes 95(1–2) 277–281). | Corroborated by independent secondaries. vDT §2: "As observed by Konyagin [10], F(k)≤F(k+1)… due to (2.1)". BvD: folklore "recorded in the introduction to [16]". p.312 is page 1. Elsholtz 2016 and the survey give the k/log k order. **Errata:** the t148 forum thread says Konyagin's eq. (4) is false and his Lemma 1 needs "m odd"; Konyagin confirmed by e-mail (Woett, 29 Dec 2025) and says the main result holds. The paper's hedge "Konyagin *stated*" is apt, and **the paper uses none of the erroneous steps.** §6 relies only on its own Lemma 6.1 and identities (6.1)/(6.2). |
| [4] Elsholtz 2016, Thm 1.1 | ±1 mod P version | arXiv 1606.02117**v1** (only version) | **Holds exactly.** "P=p₁⋯p_s squarefree [s≥1] … k sufficiently large. Moreover, if P is even, let k be odd … x_i ≡ ±1 mod P … \|X_{k,P}\| ≥ exp exp(c(P) k/log k)". Numbering in the published QJM version not checked. |
| [5] Elsholtz–Planitzer, Cor 3(2) | log log F(k)=O(k), repetitions allowed | arXiv 2012.05984v1 | **Holds.** f_k(m,n) counts a₁≤…≤a_k (repetitions allowed). Cor 3(2): f_k(1,1) < c₀^{(2/5+ε)2^{k−1}}. Aside, not load-bearing: EP define c₀ with u₀=1 and Remark 3 gives 1.5979 (=Vardi²), while erdosproblems #148 and vDT quote it with Vardi 1.26408. FC 148.lean records the same inconsistency. Under either constant the double log is O(k), which is all the paper uses. |
| [3] Croot 1999; [17] Martin 2000 §4 L.11–13 | Fourier/modular-inverse precedent | Croot (OCR, correct paper); Martin arXiv math/9811112 | **Holds.** Martin §4 ("The Large Prime Powers") says its methods "are in large part derived from those in Croot [2]". Lemma 12 is "a direct generalization of [2, Proposition 2]" and uses the finite Fourier transform for subset sums of inverses. |
| [7] Erdős 1952 §3 | prime-factor splitting | renyi.hu | **Holds.** §3 proves the upper estimate by splitting f(k)=a_k b_k at the point where the prefix product crosses x. The paper says it proves the needed truncated, shifted version itself. |
| [18] Nakayama 1940 §I | arithmetic criteria for few terms | J-STAGE | **Holds.** §I gives necessary/sufficient conditions for N(a,b)≤2 and ≤3. |
| [20] Takenouchi 1921 §§II–III pp.79–80 | repetition removal (Lemma 2.2) | J-STAGE | **Holds.** (II) "Finiteness of Solutions" is on p.79. (III) "Solutions in which two x's are equal" is on p.80, with the same p+1, p(p+1) / p+1, (p+1)(2p+1) replacements. The paper reproduces the argument. |
| [9] Erdős–Turán 1948 I Thm III; II §§11–16 | discrepancy inequality (4.8) | renyi.hu (both parts) | **Holds.** Theorem III is stated for closed arcs α≤φ≤β, with error C(n/(m+1)+Σψ(k)/k). For a finite list the paper's half-open [0,δ) is the same as a slightly shorter closed arc, so its conversion remark is valid (if roundabout). Part II §§10–16 contain the proof of Thm III. |
| [13] Hildebrand–Tenenbaum p.414 (1.3) | Rankin's method | numdam | **Holds** (p.414, "Rankin's method", (1.3)). |
| [19] Selberg 1949 p.305 (1.1) | PNT | LSU-hosted JSTOR copy | **Holds.** (1.1) is lim ϑ(x)/x = 1 on p.305. |
| [15] Kumchev 1997 (1)–(2); [16] Kumchev–Tolev Thm 1, §3.1 | quantitative 3-primes, uniform in odd u | numdam; author PDF | **Holds.** Kumchev (1)–(2) give Vinogradov's asymptotic with exactly the paper's singular series. KT Thm 1 gives R(n) = n²S(n)/(2 log³n) + O(n²(log n)^{−4}) with an absolute error term, which supports the paper's "absolute threshold". KT §3.1 is "Vinogradov's three prime theorem". |
| [11] Glibichuk–Konyagin Prop 1.1 | bilinear sum bound | arXiv math/0702729v1 | **Holds.** \|Σ_{x∈X,y∈Y} e(axy/p)\| ≤ √(p\|X\|\|Y\|); the paper squares this. The CRM vol. 43 pp. 279–286 metadata was not independently confirmed. |
| [10] Gallagher 1971 | "mechanism underlying" larger sieve | Crossref metadata OK (AA 18, 77–81); text bot-walled | Attribution only, standard. |
| [12] Graham–Kolesnik L.2.5, Thm 2.2 | van der Corput differencing, 2nd-derivative test | book, **COULD NOT CHECK**. From memory these are the Weyl–van der Corput inequality and the second-derivative test. | The paper reproves both estimates, so this is not load-bearing. |
| [1],[2] erdosproblems 293/304 | problem records | live pages + history | See §3. |

Bibliographic metadata (volumes, pages, years) of [3]–[5], [7], [10], [15], [19], [22], [23] all match Crossref. [22] was published online 2026-07-08 (DOI 10.1017/S0305004126102102), as printed.
Each citation used *inside a proof*, as opposed to history, says what the paper uses it for, with the hypotheses it needs: [9], [11], [13], [15]/[16], [19], [20], [22 L2.1]. None is load-bearing in a way that its source fails to support.

## 2. Priority and novelty

**Before 25 Sep 2026 (and before the 6 Oct public release):** I found no public proof or claim of N(b) ≪ log log b, log log F(k) ≫ k, or log log v(k) ≫ k. I checked:
- the erdosproblems threads and proof-claim tabs for 304/148/293: zero claims, comments suspended;
- the edit history of 304/148/293: only versions dated 2025-10-20 and 2026-10-16, the latter adding the Bloom–van Doorn link;
- arXiv (Egyptian/unit-fraction listings through Oct 2026);
- the teorth DB and GitHub issues;
- Formal Conjectures;
- the Bloom–Elsholtz 2022 survey, which lists O(log log n) as Erdős's open conjecture.

**Intermediate results the paper does not cite — EXPOSITION / omitted literature, not a priority problem for the theorems:**
1. **Liam Price (GPT-5.6 Sol Pro), Erdős #18 proof claim, submitted 2026-07-24:** h(n) ≪ (log log n)² for infinitely many practical n.
2. **W. van Doorn & GPT-6 Astra Pro, "Practical numbers and Egyptian fractions"**, github.com/Woett/ChatGPT-s-note-on-Erdos18. The repo was created 2026-09-16, and the #18 proof claim was submitted the same day at 23:18 UTC. It is Lean-formalised by Aristotle and proves **N(b) ≤ 2c₀(log log b)²** and **v(k) ≥ exp(exp(√(k/(2c₀))))** with c₀ = 14/log 2.

   This was public 9 days before the paper's date and 20 days before its release, and it is strictly weaker than both of the paper's theorems. The paper's introduction ("Vose subsequently obtained N(b) ≪ √log b … Van Doorn and Tang prove v(k) ≥ exp(ck²)") therefore misdescribes the state of the art as of its own date. Bloom–van Doorn cite this as [8]: "AI-generated proofs [8] recently improved this to N(b) ≪ (log log b)²".

   Mitigation: the item was never on the #304/#293 pages (their history shows no edit between 2025-10-20 and 2026-10-16), and the paper accessed #304 on 21 Sep.

**After:**
- **Bloom–van Doorn exposition** (erdosproblems.com/static/UnitFractions.pdf, 14 Oct 2026). Site pages 148/293/304 were updated 16 Oct to cite it.
- **Formal Conjectures 304.lean** (matches the copy in fc/) now marks `upper_bound` "research solved" and links to OpenAI `Main.lean#L33` at commit adc7f124.
- No arXiv paper on these problems after 25 Sep (latest relevant listings: 2607.28387, 2609.32140, both unrelated).
- The teorth DB still records 148/293/304 as `open`, last update 2025-08-31. This is stale relative to the site.

**Bloom–van Doorn compared with the paper.** They flag no mathematical error. Their departures:
- **Redundancy:** "the technical arguments of Sections 3-5 (occupying 15 pages, out of 33 total) are entirely redundant". Theorem 1 follows from the much more elementary method the paper itself uses in §§7–8. "Strangely, nowhere in the paper is this oddity mentioned."
- **Missed shortcut:** "The paper also does not make the observation that, since v(k) ⩽ kF(k)+2, the lower bound for F(k) immediately follows from the lower bound for v(k)."
- **Not read by them:** "The authors of this paper have not yet read those sections [3–5] in detail". **So BvD's exposition is no independent check of §§3–5.** It relies on the Lean ("The proofs were formalised in Lean, and hence one can verify their correctness mechanically").
- **Simplification:** "[17] employs an extra iterative procedure which we avoid by passing to the base-B representations in Lemma 7". That is §8.2 grouping, replaced by base-B digits.
- **Different sum-product input:** BvD's Lemma 4 uses Hart–Iosevich (−1 ∈ AA+AA for \|A\| ≥ p^{3/4}). The paper's §8.1 uses a five-product Fourier argument from Glibichuk–Konyagin Prop 1.1. BvD need ≤10 fractions per integer where the paper needs ≤16.
- **Repetition removal:** BvD state it as one theorem (Thm 8: a/b∈(0,1], k≥3, preserving an odd divisor). The paper splits it into Lemma 2.2 (total <1) and Lemma 6.1 (total =1).
- **Constants:** BvD get (61/log 2+o(1)) log log b, improvable to 16/log 2. Their note "every proof … with constant c implies 1/c for Theorems 2 and 3" puts the paper's log 2/257 in context: weaker, not wrong.
- **Attribution criticism:** "it is often unclear which parts of its lengthy arguments appear in these earlier references, and which are novel".

## 3. Problem statements

- **#304** (site: N(a,b) with 1<n₁<…<n_k; N(b)=max_{1≤a<b}; "Is it true that N(b) ≪ log log b?"). Theorem 1.1 answers exactly this, and the classical lower bound gives Θ. The OpenAI comparator `ShortEgyptian.main` and FC 304's `upper_bound` both state N(b) = O(log log b) for the same N.
- **#148** ("Find good estimates for F(k)"; EG p.32 asks for "asymptotic formulas or even good inequalities"). Corollary 1.2 gives log log F(k) = Θ(k), with the constant c unquantified.
  - That is an answer only at double-log precision. EG's speculation on p.32, "Perhaps the lower bound can be replaced by c₀^{2^{n(1−ε)}}", i.e. slope log 2, remains open.
  - The site's phrase "determining the order of growth of F(k) up to constant factors" means constants in log log F, not in F. The paper's own claim ("double logarithms have order k") is precise.
  - FC 148.lean has no statement of the new bound; `erdos_148` is still "research open".
- **#293.** EG p.35 verbatim: "What is the least integer v(n) > 1 which does not occur as an x_k, k variable, for {x₁,…,xₙ} ∈ 𝒳ₙ? It is easy to see that v(n) > cn! … It may be that v(n) actually grows more like 2^{2^{√n}} or 2^{2^{n(1−ε)}}. The corresponding question for 𝒳′ₙ is also interesting here."
  - **What the ambiguity is:** the site's wording ("the minimal integer which does not appear") **drops EG's "> 1"**. With 1≤n₁ that literal reading is degenerate, since v(k)=1 for all k≥2. This was raised by Woett on 8 Dec 2025 and in teorth issue #368. teorth flagged `comments: "ambiguous statement"` on 2026-08-28 (commit 0677cd61). The site text is still unfixed.
  - **The paper's v(k)** = min({2,3,…}∖D_k) is EG's original (and vDT's and OEIS A400352's) definition. The OpenAI Lean `Problem337.v` uses the same (`{m | 2 ≤ m} \ D k`).
  - **Every non-degenerate reading gets the same double-log order from the paper:**
    - Lengths ≤k instead of =k: identical, because D₁=∅ (m≥2), D₂=∅ and D_k ⊆ D_{k+1}.
    - EG's 𝒳′ₙ variant (repetitions allowed): D_k ⊆ D′_k gives the lower bound, and the elementary bound x_k ≤ k^{2^{k−1}} holds for nondecreasing tuples, giving the upper bound.
    - A per-solution reading ("least integer missing from a given solution") is bounded by a constant and is not what EG meant (they cite v(n) > cn!).
  - The paper's liminf ≥ log 2/257 refutes EG's 2^{2^{√n}} alternative. It is consistent with 2^{2^{n(1−ε)}} but does not prove it (limsup ≤ log 2 only).
  - **Formal Conjectures:** `293.lean` does **not** exist (raw URL 404). Issue #476 is open. PR **#6842** (2026-10-04, open) adds only definitions and certificate checks, with no growth theorem. PR #4870 (open) adds the vDT reduction b<v(k) ⇒ N(b−1,b) ≤ k−1 to 304.lean.
  - Side finding: PR #6842 says it "rejects the proposed tuple containing 681943 by checking its exact deficit, 131225/8053056". Exact arithmetic on that tuple as posted on the forum (681943, 2, 3, 7, 44, 984, 15498, 16608039822, 155008371672) gives a sum of exactly 1. Either the PR mis-transcribed the tuple or its check is wrong.

## 4. OEIS (via the oeis/oeisdata GitHub mirror; oeis.org is Cloudflare-walled from here)

- **A097847**: T(n,k) = minimal number of unit fractions for k/n, 1≤k≤n. "distinct" is not stated, but by Takenouchi/Lemma 2.2 it is the same as distinct for k<n. Row k=n is 1 (1/1).
- **A097849**: max of row n of A097847, offset 1. Terms: 1,1,2,2,3,2,3,3,3,3,4,3,4,4,3,4,5,3,4,3,4,4,5,3,4,4,4,4,5,4,5,4,4,5,4,4,5,5,5,4,… So a(b) = N(b) for b≥2 (a(1)=1 is the k=n row). **My exact recomputation of N(b) for b=2..40 matches all 39 terms.**
- **A006585**: F(n), offset 1: 1, 0, 1, 6, 72, 2320, 245765, 151182379. **Recomputed k=1..6: match.** F(1)=1 counts 1=1/1, consistent with the paper's 1≤n₁. F(8) was independently recomputed on the t148 forum (22 Sep 2026).
- **A076393**: Vardi constant 1.26408473530530111307959958416466949111456…
- **A400352**: "Least integer m > 1 that does not occur as a denominator in any representation of 1 as a sum of n distinct unit fractions". Offset 3: v(3..9) = 4, 11, 17, 103, 733, 27539, 13856993. Created 23 Sep 2026 by Jude Wallis; a(9) by certificate plus an exhaustive search for 13856993.
  - **Recomputed v(1..6) = 2, 2, 4, 11, 17, 103: match.**
  - Spot-checked certificates by exact arithmetic: 13856992 (k=9), 9121003 (k=9), 27538 (k=8). All sum to 1.
- Related, not the same sequence: A097048/A097049 (least-denominator fractions needing ≥n terms: 2,3,5,11,17,79,733,27539) agree with v(k) at k=1,4,5,7,8 and differ at k=2,3,6. A097048 is easily confused with A400352.

## 5. Classified objections (seat W scope)

- **EXPOSITION — §1 Introduction, the history of #304/#293.** The paper omits the public intermediate results: Price, #18 claim of 2026-07-24; van Doorn–GPT-6 Astra Pro, 2026-09-16, with N(b) ≪ (log log b)² and log log v(k) ≫ √k. It presents Vose and van Doorn–Tang as the prior state. This is not a priority problem, because the paper's results strictly supersede them.
- **EXPOSITION — §1 / §6.** "Konyagin explicitly records the padding injection [14, p. 312]": the primary is unchecked here, but two independent secondaries corroborate it. Konyagin's known errata (eq. (4); Lemma 1 hypothesis) do not touch anything the paper uses.
- **EXPOSITION — redundancy, as raised by BvD.**
  - §§3–5 are unnecessary given the §8 method.
  - Corollary 1.2's lower bound follows from Corollary 1.3 via v(k) ≤ kF(k)+2, with the explicit slope log 2/257. The paper uses neither shortcut and says neither.
  - Neither point is an error.
- **Nothing FATAL and no citation GAP found:** every citation I could read states what the paper takes from it, with the hypotheses and the uniformity it needs ([9], [11], [15]/[16] uniform in odd u, [19], [20], [22]).
- **Could not check:** [21] (and its p.151 / Lemma 4 / §3 pinpoints), [14] full text, [12], [23] full text. All four are corroborated by secondaries or not load-bearing.

VERDICT: HOLDS AS READ
