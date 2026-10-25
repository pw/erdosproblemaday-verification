HOLDS AS READ — every literature claim and citation I checked in the paper is accurate, and no prior unconditional proof of Theorem 1.1 (for any C ≥ 0.58) or Corollary 1.2 exists that I could find. No competing proof, and no public criticism specific to this paper, was found up to 21 Oct 2026. The remaining issues are exposition gaps: the paper omits the RH plus pair-correlation conditional route (Heath-Brown 1982, BLZ Theorem 6, Tao's 10 Sep 2025 forum comment) and Erdős's own 1965 remark on d_n > log n.

Seat W, 2026-10-21. Working files are in /tmp/oaimath/026/seats/W_work/ (my fetches are in w2/; the dead tick's caches are in agentB/ and src/). Tasks 3 and 4 (Formal Conjectures history and prior Lean work) were done by the dead tick's agentA (W_work/agentA.md). I spot-checked them and they are carried forward in findings 7 and 8. All printed locations in the OpenAI paper refer to the PDF layout rendering (O_work/paper_layout.txt).

---

## 1. Novelty: the strongest prior unconditional result is BLZ 2010, Theorem 5, which covers C < 0.579038… only
Severity: none (the paper's claim holds).

**Source.** Bazzanella, Languasco, Zaccagnini, "Prime numbers in logarithmic intervals", Trans. AMS 362 (2010) 2667–2684 (electronically published 17 Nov 2009). I checked both the published PDF (Padova repository, research.unipd.it/bitstream/11577/2425130/1/[27].pdf, saved as w2/blz_tams.pdf) and arXiv:0809.2967v1. arXiv has only v1. Theorem numbering is identical in the two.

**Definitions.** In (1.3), A(K) = {p ≤ X prime : ∃ prime p′ with 0 < p′ − p ≤ K} and A₁(K) = {p ≤ X prime} \ A(K). So A₁(K) counts **prime starts** whose next gap exceeds K. Here K = λ log X ≥ λ log p, so the bound transfers to d_n > λ log p_n.

**Theorem 5, verbatim:** "Let ε > 0, X be a sufficiently large parameter and 0 < λ < 2/B − ε … We have that |A₁(λ log X)| ≥ (1 − λ(B+ε)/2) X/log X." The paper then says: "we can set B = 3.454 and hence Theorem 5 holds for every λ < 0.579038 . . .". I computed 2/3.454 = 0.5790387956 ✓.
- B is the Bombieri–Davenport constant of their Lemma 2. The value 3.454 is Fouvry–Grupp's, valid for n ≤ log^A X.
- The proof (§7) is a one-line upper-bound sieve count.
- With B = 1 it would give λ < 2.

**Theorem 3** counts **integer starts**: "there exists λ > 1 such that |B₁(λ log X)| ≥ (c₂(B,λ) − ε)X", with best λ ≥ 1.145358…. It improves Cheer–Goldston 1987 (TAMS 304), which had λ = 1 + 1/(2B) = 1.144759….

**Theorem 6** is conditional: hypotheses (1.14) and (1.15), where (1.15) is Heath-Brown's Corollary 1 under RH plus pair correlation.

**Why Corollary 1.2 was out of reach.** Since p_n/n = log p_n − 1 + o(1), Corollary 1.2 needs gaps of size about log p_n, i.e. C close to 1. No unconditional prime-start result reached C = 1:
- **Tao, MathOverflow answer 332888 (2019-05-30).** Proves only λ < 1/4. He says that "If one could prove an upper bound on f_X(Λ) that went to zero as Λ → ∞ then we could use the above arguments to show that S_λ(x) ≫_λ x/log x for all λ < 1", and that this "do[es] not appear to be known unconditionally".
- **Comments on the same MO question:**
  - Tao (comment 830696): BLZ's integer-start result "*almost* implies that p_{n+1}−p_n ≥ λ log p_n for a positive proportion of n, but one first has to eliminate the scenario that the prime gaps are … really, really big".
  - The accepted answer (332607): "I doubt it has already been proven such lower bound unconditionally for any λ>0."
- **Erdős 1965 ([Er65b], printed p. 202).** I checked the page image: "Unfortunately I cannot prove that the upper density of the integers n for which d_n > log n is positive." So even the **upper**-density version with C = 1 was open in 1965.
- **Tao on the #968 thread (10 Sep 2025):** "This seems close to the limit of current technology."

**Other literature checked; none gives a density of large gaps:**
- Banks–Freiberg–Maynard (arXiv 1404.5094; Thm 1.1 / Cor 1.2): at least 1/8 of [0, T] (asymptotically) lies in the limit-point set L of d_n/log p_n.
- Pintz (arXiv 1407.2213; Thm 1): [0, c_f] ⊂ J_f.
- Merikoski (arXiv 1811.03008; Thm 1, Cor 2): μ(L ∩ [0,T]) ≥ T/3; Cor 3: the limit points have bounded gaps.
- Ford–Maynard–Tao, chains (arXiv 1511.04468; Thm 1): G_k(X) ≫ k⁻² log X log₂X log₄X / log₃X.
- Baker–Freiberg (arXiv 1510.08054).
- Freiberg (arXiv 1508.00143): intervals with exactly m primes, counts x^{1−o(1)}.
- GPY "Primes in tuples IV" (arXiv 1103.5886; Thm 1): #{p_n ≤ x : d_n ≤ η log p_n} ≫_η π(x). This is small gaps only.
- Gallagher 1976 and Jha 2026: conditional.

Limit points and maximal gaps are infinitely-many statements, compatible with zero density.

**Not checked:** whether a later twin-prime sieve constant (e.g. Wu 2004) is uniform in the shift 2n ≤ log^A X. If it is, BLZ's argument would give about 2/3.3996 ≈ 0.588. That is still far below 1 and does not change the verdict. The paper itself never claims 0.579 is the best known; COMMON.md does.

## 2. Competing proofs and public criticism since 25 Sep 2026: none found
Severity: none.

**arXiv.**
- Searched the cached math.NT listing: 8,279 records, 2025-01-01 to 2026-10-20 (agentB/nt_all.json). I grepped titles and abstracts for prime gaps, positive proportion/density with gap, Prachar, p_n/n, OpenAI and "Erdős problem".
- Also checked the live arxiv.org/list/math.NT/new page for 21 Oct 2026.
- Nothing proves or disputes a positive proportion of large gaps or #968.
- Nearest hits, all unrelated:
  - Freiberg 2609.33692 (27 Sep 2026): conditional on HL.
  - Uğurdoğan 2610.10582: rough numbers in gaps.
  - Stadlmann 2608.31126: H₁ ≤ 240.
  - 2609.28253: tilted sieve beyond Erdős–Rankin, i.e. maximal gaps.

**erdosproblems.com** (live copies of /968, the forum thread and the proof-claims tab, fetched 21 Oct 2026):
- The page is "last edited 31 March 2026". It shows "Proof claims (0)" and "No proof claims have been submitted yet".
- Comments: 2, both by Tao, from 2025. "The ability to post new comments has been suspended."
- Bloom's blog post "Erdős problems in the OpenAI proofs" (8 Oct 2026) lists [968] only as a claim: "This blog post is just acknowledging the existence of the proof claims, and does not mean to make any judgements about novelty or attribution." It paraphrases the main theorem as "p_{n+1}−p_n > C log n". That is weaker than the paper's C log p_n; the discrepancy is Bloom's, not the paper's.
- None of the 11 comments on that post concern 968.

**Other venues (cached):**
- Tao's blog: 55 posts to 20 Oct 2026, with comments. Nothing on 968, Prachar or large-gap density.
- Tao's Mastodon: 80 statuses. Nothing.
- HN: Algolia story and comment searches for 968, Prachar and prime gaps found no relevant comment. One "968" hit is a PR count.
- Bluesky: nothing.
- The news pieces in agentB/dl_web mention 968 only in lists.
- The mid-August "OpenAI prime gaps" rumours in the Quanta-style Stadlmann article concern bounded gaps (openai/PrimeGaps186), not this paper.

**Databases:**
- teorth/erdosproblems problems.yaml (fetched today) still has 968 `status: open`, `last_update: 2025-08-31`.
- The plasma.ai "Erdős Problems" wiki marks 968 "Solved · Proved". Its stated basis is that the corpus "built it, checked its axioms and found it identical to the release's comparator challenge". That is a Lean-build acceptance, not a human referee of the analytic proof.
- Formal Conjectures: see finding 7.

**Conclusion:** I found no independent human verification and no published objection.

## 3. What Erdős and Prachar asked: explicitly LOWER density ("untere Dichte"); the paper's [5, p. 256] is accurate
Severity: none.

**Source.** Erdős and Prachar, "Sätze und Probleme über p_k/k", Abh. Math. Sem. Univ. Hamburg 25 (1961/1962) 251–256. The Rényi Institute index gives MR 25 #3901 and Zbl 107,266. The paper is signed "Eingegangen am 9. 1. 1961". I checked the scan at src/erdos/ep-6.png, printed p. 256, verbatim:

> "Eine weitere Frage ist die, ob die untere Dichte der k-Werte, für die p_k/k < p_{k+1}/(k+1) bzw. p_k/k > p_{k+1}/(k+1) gilt, positiv ist. Im letzteren Fall ist dies so einzusehen: … Es scheint schwierig zu sein, zu beweisen, daß die k mit p_k/k < p_{k+1}/(k+1) positive untere Dichte haben."

On the same page they ask "ob es unendlich oft vorkommen kann, daß p_k/k > p_{k+1}/(k+1) > p_{k+2}/(k+2)".

Their k is 1-based, matching Corollary 1.2's n ≥ 1.

**Satz 2** (p. 251) says that an increasing *chain* p_{k_i}/k_i < p_{k_{i+1}}/k_{i+1} has o(x/log x) members. This concerns monotone subsequences, not consecutive increases, and does not conflict with Corollary 1.2.

**Er65b** ("Some recent advances and current problems in number theory", Lectures on Modern Mathematics III, Wiley 1965, 196–244), printed p. 204, page image checked: "We easily show that the density of the integers k for which u_k > u_{k+1} is positive. We cannot show that the same holds for the k for which u_k < u_{k+1}." Here "density" is unqualified. Er65b's own reference [17] miscites the 1961 paper as "26 (1962) 51-56".

**erdosproblems.com/968** states "positive density" and hedges "by 'positive density' here he most likely meant positive lower density". The 1961 primary source settles this as **lower** density, so the hedge is unnecessary.

**OEIS A387591** ("Primes prime(k) such that (k+1)*prime(k) < k*prime(k+1)", Vishal Doshi, Sep 2025) carries the comment "Sequence relates to Erdős problem 968". Its data begins 3, 5, 7, 13, 19, 23, …, matching the dead tick's sieve (proportions 0.40–0.45 up to N = 2·10⁷, W_work/ratio_density.out; I did not re-run it).

## 4. Tao's two forum comments on #968, in full substance
Severity: exposition — the paper does not cite either.

**Comment of 06:23, 08 Sep 2025** (marked "[Completely rewrote this answer, which previously was based on a sign error.]"). Its claims:
- u_n < u_{n+1} rearranges to p_{n+1} − p_n > p_n/n, "so by the prime number theorem this is essentially asking for a large prime gap p_{n+1}−p_n ≳ log n".
- The Erdős–Prachar decreasing case follows from GPY's positive-density small gaps (link to arXiv 1103.5886).
- He guesses the Maynard sieve gives u_n > u_{n+1} > u_{n+2} on a positive-density set ("haven't checked this carefully").
- "The enemy preventing one from proving u_n < u_{n+1} for a set of positive density is if almost all prime gaps in say [x,2x] are less than log x, and a small number (zero density) of prime gaps are much larger than log x."
- He suggests large-gap theory or the Maier matrix method might help.

**Comment of 21:57, 10 Sep 2025.** He claims the answer is positive assuming RH and "a weak form of the pair correlation conjecture, specifically estimate (5) of this paper of Heath-Brown" (link: Acta Arith. 41, aa4118.pdf). The argument:
1. By Heath-Brown's Corollary 1, Σ_{p_n≤x, d_n≥A log x} d_n ≪ x/A.
2. Telescoping plus PNT gives Σ_{d_n≤log x}(log x − d_n) = Σ_{d_n>log x}(d_n − log x) + o(x).
3. Small-gap results (GPY) make the left side ≫ x.
4. Hence (1+ε) log x ≤ d_n ≤ A log x for ≫ x/log x values of p_n, which gives u_n < u_{n+1}.

He adds that a sufficiently uniform prime-tuples conjecture (Gallagher) also suffices. He concludes: "This seems close to the limit of current technology, so further progress may need to await some breakthrough on the pair correlation conjecture or the prime tuples conjecture."

His reaction tag on the problem is "Looks difficult".

**Scope.** Tao's conditional argument gives only some C slightly above 1, not every C. The paper's Theorem 1.1 for every fixed C is strictly stronger than this conditional route, and is unconditional.

**Missing from the paper.** The paper's "Conditional results" paragraph (printed p. 2) cites only Gallagher [8] and Jha [12]. It does not mention:
- the RH plus pair-correlation route (Heath-Brown 1982 Corollary 1);
- BLZ Theorem 6;
- Tao's forum comment;
- Er65b p. 202.

These are omissions in the literature review, not errors.

## 5. Citation spot-checks: 10 checked, all accurate
Severity: none.

| Paper's citation (printed location) | What the source says | Verdict |
|---|---|---|
| "[5, p. 256]" (p. 1, before Cor. 1.2) | The untere-Dichte question, as quoted in finding 3 | ✓ |
| "[1] … Their Theorem 5 … below 2/3.454 = 0.579038 …, whereas their Theorem 3 reaches some intervals longer than the average prime spacing by counting integer starts" (p. 2) | Matches the published and arXiv texts (finding 1) | ✓ |
| "[8, Theorem 1]" (p. 2): Poisson statistics for integer-start intervals of length λ log X under a uniform HL hypothesis | Gallagher, Mathematika 23 (1976) 4–9, p. 4, Theorem 1: P_k(h,N) for n ≤ N, h ∼ λ log N, provided (1) holds uniformly for 1 ≤ d_i ≤ h | ✓ |
| "[8, p. 5, equation (3)]" (§5.3, "Gallagher's singular-series mean") | p. 5, (3): Σ_{1≤d_1,…,d_r≤h distinct} 𝔖(d) ∼ h^r | ✓ |
| "[3, p. 206, equation (1.4)]; their ψ notation is defined on p. 204" (§5.1) | BFI, Acta Math. 156 (1986), p. 206, (1.4): Σ_{q≤Q} max_{(a,q)=1} \|ψ(x;q,a) − x/φ(q)\| ≪ x𝓛^{−A}, Q = x^{1/2}𝓛^{−B}. This is the endpoint form, with no max over y. The notation list on p. 204 defines ψ(x;q,a) = Σ_{n≤x, n≡a(q)} Λ(n) | ✓ |
| "[10, p. 6, equation (2.14) and the preceding paragraph]" (p. 3) | GY arXiv math/0504336v1 (16 Apr 2005), p. 6: "we detect primes by the square of the linear combination of tuple approximations (a₀ + Σ_{j=1}^k a_j Σ_{distinct h's} Λ_R(n;H_j))²" (2.14). This squares terms of cardinalities j = 1..k | ✓ |
| "[13, Section 6, p. 404]" (§5) | Maynard, Annals 181 (2015), p. 404 (§6), Remark: "Tao … estimates the corresponding sums directly using Fourier integrals" | ✓ |
| "[13, Section 7]" (§4) | §7 "Choice of smooth weight for large k": F = Π g(k t_i) on the simplex, truncation controlled through the centre of mass of g² | ✓ |
| "[12, Theorems 1.4 and 1.6] … under a stronger uniform tuple hypothesis" (p. 2) | Jha, arXiv 2605.23014 v2 (12 Sep 2026; v1 21 May 2026). Both theorems assume HL[λ′ log x, exp(√(log₂x log₃x))] | ✓ |
| "[16] … MathOverflow, answer 332888, May 2019" | Answer 332888 by Terry Tao, created 2019-05-30 | ✓ |

**Bibliographic data** also matches its source:
- [5]: 25:251–256 (1961/62).
- [1]: 362:2667–2684.
- [8]: 23(1):4–9.
- [13]: 181(1):383–413.
- [10]: PLMS 95 (2007) 653–686, confirmed via Maynard's reference list.

## 6. Framing sentences checked against the sources
Severity: none.

**Checked:**
- "Bazzanella, Languasco and Zaccagnini distinguish the two counting measures explicitly [1]" (p. 2). True: they define A(K)/A₁(K) for primes and B(K)/B₁(K) for integers separately in (1.3)–(1.4).
- "Tao's empty-interval argument [16] also identifies the additional control required to pass from interval measure to gap counts" (p. 2). True: Proposition 1 in his answer, and comment 830696.
- "A lower bound for the largest gap does not by itself give a positive proportion of gaps exceeding a fixed multiple of log p" (p. 1). True, as the limit-point literature in finding 1 illustrates.

**No priority claim.** The paper makes no explicit "first" or "previously open" claim beyond "answering a question of Erdős and Prachar" (Abstract; p. 2). So there is nothing to refute on priority.

## 7. Formal Conjectures (agentA's findings; spot-checked)

**Spot-check (GitHub API, today).** PR #6898 "feat: mark problems solved in the OpenAI math release and link formal proofs" by mo271:
- opened 2026-10-07T10:16:42Z;
- merged 2026-10-11T08:10:50Z;
- merge commit 3dfd999dfe5a…, committer date 2026-10-11T07:51:35Z;
- the file list includes FormalConjectures/ErdosProblems/968.lean.

This matches agentA exactly.

**AgentA's findings, carried forward (not re-verified beyond the above):**
- FC `erdos_968` is `0 < {n : ℕ | u n < u (n + 1)}.lowerDensity`, with 0-based `u n = nth Prime n / (n+1)` and FC's own `Set.lowerDensity` (a liminf over Iio b). It is mathematically equivalent to OpenAI's statement after a shift n ↦ n+1 and unfolding liminf to sSup. They are not syntactically identical, and no bridge exists in FC.
- The formal_proof link points to RatioCorollary.lean#L30 at adc7f12. That line is the comparator-checked conjunction `large_gaps_and_ratio_density`, not the standalone corollary at L20.
- PR #6898's list of routine transports omits 968, even though 968 needs a transport of the same kind as Erdős 371, which it does list.
- No executed `#print axioms` or Comparator run backs the flag.
- No FC issue or PR questions 968.
- Earlier history:
  - FC switched HasPosDensity → lowerDensity on 2026-08-05 (PR #4736).
  - On 2026-09-30, PR #6752 still said the main question "stays open".

## 8. Prior Lean BV/SW/large sieve (agentA's findings; spot-checked)

**Spot-check (GitHub API):** kimihiro64/bombieri-vinogradov
- repo created 2026-08-31T18:36:23Z;
- release v0.1.0 at ec3e36e0, published 2026-09-05T03:49:34Z (v0.1.4 at 17:35:22Z the same day);
- the tag's tree contains BombieriVinogradov.lean and BombieriVinogradov/Assembly/SiegelWalfisz/….

This matches agentA.

**AgentA's other findings, carried forward:**
- Mellendijk's amellendijk/lean-bombieri-vinogradov assumes SW and the large sieve as axioms and still has sorrys.
- AxiomMath/PrimeGapsLib takes BV as a hypothesis.
- Mathlib (d13f23b7 and current) has no BV, SW or large sieve.

So a sorry-free public Lean BV, SW and large sieve existed about 3 weeks before 25 Sep 2026 (self-assessed, unreviewed). The OpenAI paper never mentions Lean, so this contradicts nothing in it. It only matters for third-party "first formalization" framing.

**Timing.** openai/math was created 2026-10-06T21:47Z. Nothing from this paper was public before 6 Oct, consistent with FC calling it open on 30 Sep.

---

## What I did NOT check
- **The mathematics of the paper.** Not read beyond §1 and the citation contexts.
- **Heath-Brown 1982 (Acta Arith. 41), Corollary 1 and (5).** The fetch was blocked. I relied on BLZ's own statement that (1.15) is Heath-Brown's Corollary 1 under RH plus pair correlation, and on Tao.
- **Other sources not opened:** Cheer–Goldston 1987 (known only via BLZ and an OpenAlex abstract); Gallagher's 1981 corrigendum; whether Wu's twin-prime constants are uniform in the shift.
- **Bibliographic data not checked** for [2], [4], [6], [7], [9], [11], [14], [15], [17], [18].
- **Venues not searched:** Lean Zulip (no direct search), X/Twitter, Reddit, Chinese-language forums. Journal-only publications without an arXiv version (outside the arXiv math.NT window) were covered only by web search. My live arXiv API query was rate-limited ("Rate exceeded"), so freshness rests on the cached 8,279-record listing to 20 Oct plus the 21 Oct HTML new-listing.
- **AgentA's Lean and FC work** was spot-checked on two claims (the PR #6898 dates and the kimihiro64 release dates), not re-done. The local Bridge968.lean was not audited.
