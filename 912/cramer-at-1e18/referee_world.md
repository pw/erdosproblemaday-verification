# Erdős #912: WORLD / PRIORITY referee report

Seat: world/priority referee (hostile). Date: 2026-11-10, fetches made 09:33–09:50 UTC.
Scope: prior art for every "ours" claim in `CLAIMS.md`, plus a check of every sentence about other people's work.
The lead's note (our July report, `sources/our_july_report_912.md`) is folded in throughout.

Fetch notes. erdosproblems.com and OEIS were fetched through Hetzner (exe.dev is CF-blocked on both).
arXiv, MathOverflow and GitHub were fetched directly. Scratch copies are in `/tmp/w912/` and are not part of the deliverable.
**Could not search:** arXiv full text (the API searches only metadata and abstracts), Google Scholar (no access), and the zbMATH citing-documents page (returned empty).
Semantic Scholar answered once for 2609.25341 (0 citing papers) and once for Sanna 1902.09224 (2 citing papers). It was rate-limited (429) for 2309.16072.

---

## Headline: four things the write-up does not yet know

1. **The c = √(2π) Cramér heuristic is not Tao's first.** Will Sawin posted it on MathOverflow on **7 Jan 2022**, 3½ years before Tao's forum comment, and Tao commented under that answer the same day. erdosproblems.com, G–I, OEIS, formal-conjectures and our own CLAIMS all credit Tao alone.
2. **|h(n+1) − h(n)| ≤ 1 was first conjectured by Amiram Eldar on OEIS A357385 on 26 Sep 2022**, checked to 10^7. That is four years before Owmire's forum comment. A357385 also records our "n+1 prime ⇒ no move" corollary, but with an off-by-one index error.
3. **The first public proof of |Δh| ≤ 1 I can find is our own July report** at erdosproblemaday.com/report/912. Its git commit is 2026-07-28 01:19 UTC; the earliest third-party-verifiable date is the Wayback capture of **2026-10-05**. Nobody else has proved it or posted a proof.
   - Claim 2's exact rule is strictly sharper than the July report: at prime squares, July allowed a jump of 0 or 1, and Claim 2 shows it is always 0.
4. **The Granville and Montgomery–Soundararajan sentences we planned are both mis-scoped** (details under Q5).
   - Granville (1995) says that at interval length ≍ log x the Cramér model *agrees* with Hardy–Littlewood.
   - M–S's variance result is conditional, and in our range their Corollary 1 *confirms* Cramér at leading order.
   - The literature that does predict a log log x / log x second-order correction is the singular-series lower-order term: M–S (2004) eq. (17), and the conjectural Lemke Oliver–Soundararajan (2016) Main Conjecture.

---

## Q1. Is |h(n+1) − h(n)| ≤ 1, or the exact move rule, already known or published?

**Verdict.**
- The bound was **conjectured** (Eldar 2022 on OEIS; Owmire 2026 on the forum).
- It was **proved** first in our own July 2026 report. I found no other proof anywhere.
- The **exact move rule** (h moves only at n+1 = kQ with Q prime and Q² > n+1; the indicator formula of Claim 2(b); zero change at prime squares) appears nowhere I looked, including our July report, which only gets "at most one value changes" and "0 or 1 at prime squares".
- The **special case** "h(p) = h(p−1) for odd primes p" is on OEIS (Eldar 2022), but mis-indexed.

### OEIS
- **A357385** (https://oeis.org/A357385, "a(n) = A071626(n+1) − A071626(n)", by Amiram Eldar, created 26 Sep 2022). It is unchanged since revision #10 of 28 Sep 2022; I checked the full edit history.
  - Comment: "Conjectures: 1) The only distinct terms of this sequence are -1, 0 and 1. 2) The asymptotic density of the occurrences of 0 is 0.943..., and the asymptotic densities of the occurrences of -1 and 1 are equal and the common value is 0.028...". It gives a table of counts up to n = 10^7.
  - Formula line: "a(p) = 0 for an odd prime p."
  - **That formula is false as printed.** With the entry's own offset 1, the data reads a(3) = h(4) − h(3) = 1, a(5) = 1, a(43) = 1, and so on: 105 odd primes below 10^4 fail.
  - The true statement is a(p−1) = 0, i.e. h(p) = h(p−1). Against the b-file it has 0 failures below 10^4. This is our corollary "h(n+1) = h(n) when n+1 is prime".
  - So credit Eldar for the corollary, and note the index slip if we quote it. (We should not edit OEIS from here; the brief says post nothing.)
- **A357388 / A357390** (Eldar, 2022): numbers k with A071626(k) < A071626(k+1) and > A071626(k+1) respectively. Each carries only a density-0.028 conjecture. There is no structural description and no mention of n+1 = kQ.
- **A357386, A357387, A357389, A357391** (Eldar, 2022): runs of equal, increasing and decreasing values.
  - A357391 was extended on 2 Oct 2026 by **Wesley Stuart Kruis** with a(7) = 1784800612 and a(8) = 165493254306, "obtained by exhaustive computation. For each k, A071626(k) was computed incrementally…". That is an exhaustive computation of h(k) for every k ≤ 1.655×10^11.
  - His code is at https://github.com/Xer0H3r0-87/a357391 (created 2026-09-20). I read `src/a357391_a8_search.cpp`: it tracks only decreasing runs (`if (current < state.previous_value)`) and **never tests |Δ| ≤ 1**. So no third-party exhaustive check of the step bound exists beyond Owmire's 10^8 and Eldar's 10^7.
  - A357387 was edited on 15 Aug 2026 by Jason Yuen, a format-only change moving the examples into EXAMPLE.
- **A071626** (https://oeis.org/A071626) is revision #60 of Sep 25 2026, identical to our stored copy. Its comments: Sanna's ≍ remark (2019) and Miraj's identity remark (2024). Nothing on steps.
- **A071625 / A051903 / A051904 / A323023 / A240751 / A325272 / A325273 / A325276 / A325508 / A115627 / A076934**: I read all the comment and formula lines. Nothing on consecutive differences of A071626.
- OEIS search on the jump positions (65, 114, 133, 152, 217, 248, 279) and the increase positions (2, 4, 6, 10, 15, 22, 33, 44, 55, 66, 68, 85) returns **No results**.

### MathOverflow / Math.SE
- **MO 413332**, "Distinct exponents in the factorization of the factorial, a problem of Erdős" (https://mathoverflow.net/q/413332, asked by sebaztian on 2022-01-07). It has one answer (Will Sawin) and three comments (Sylvain Julien, Sawin, Tao).
  - Nothing about h(n+1) − h(n). See Q3 and the "must change" list for what it does contain.
- StackExchange API searches on both sites for "distinct exponents factorial", "A071626", "distinct values floor(n/p)", "exponents in n! distinct" and "number of distinct exponents" found nothing else relevant. MO 469682 is about exponent patterns over 1..n, a different problem.

### arXiv
- **Heyman–Miraj, 2309.16072 v4 (16 Jul 2024)**: no consecutive-n statement.
  - The *decomposition* is in their proof of Theorem 2, §3. They show "every prime not exceeding √X adds exactly 1 to the cardinality" and that for p > √X, "v_p(X!) = ⌊X/p⌋".
  - Their argument never explicitly shows that the small-prime and large-prime values cannot collide. Our Lemma, and §2 of the July report, supply that step.
- **G–I, 2609.25341 v1**: works only at fixed n. No mention of Owmire, steps, u_r or Heyman–Miraj. G–I do not cite HM at all; they prove a weaker "(1.6) h(n!) = #{⌊n/p⌋ : p ≤ n} + O(n^{1/3})".
- **Sanna, 1902.09224 v1 (25 Feb 2019)**: concerns f(m) for general m. A grep for "factorial", "n!" and "Erd" gives 0 hits. Not relevant to n!.
- arXiv API phrase searches across all categories: `"distinct exponents"` (only Sanna and G–I are relevant), `"floor function set(s)"` (Heyman 2019, Heyman 2021, Ma–Wu 2021, a 2021 AP paper, HM 2023: none about consecutive n), and `factorial AND Cramer`, `"Erdos problem" AND factorial` (nothing relevant).

### Erdős 1982 (https://users.renyi.hu/~p_erdos/1982-08.pdf), pp. 25–27
- Theorem 1, ≍ only: "Recently Selfridge and I proved the following Theorem 1. Denote by h(n) the number of different exponents a_i(n). There are absolute constants c1 and c2 …"
- Then: "There is no doubt that there is a constant c>0 for which h(n) = (c+o(1))(n/log n)^{1/2}. The proof of (4) seems to present very serious difficulties since we do not know enough about the difference of consecutive primes."
- Nothing on h(n+1) − h(n).

### Web, GitHub, other repositories
- Web searches on several phrasings ("distinct exponents" n!; "number of distinct exponents" factorial "h(n+1)"; "floor(n/p)" distinct values; A071626; erdosproblemaday 912) return only the sources above.
- GitHub code search for "A071626" turned up third-party "AI Erdős" notes on #912:
  - przchojecki/agentic-erdos (to 2026-05-09; exact h to 5×10^7, ratio 2.6485)
  - techno-optimist/erdos-frontier-atlas (2026-07-26)
  - rjwalters/lean-genius (axioms only)
  - kevinfff08/erdos_ai_solvability_review (2026-07-27)
  - zsophiaaa/conjecturehub (2026-08)
  - Hybrid-Quantum-Exchange (2026-09)
  - None states or proves |Δh| ≤ 1 or the move rule. I grepped each for h(n+1), {−1,0,1}, 2−√2, binom{1/2}, Sawin, Eldar and A357385, and skimmed the files.
- primereboot.pages.dev/erdos/problem/912 ("DumbPrime") is a scraped mirror of the problem statement. Its "SOLVED" badge is a scraping artefact; it has no mathematics.

### Our own priority record
- The erdosproblemaday.com/report/912 page is live (HTTP 200 today, no noindex). It contains "|h(n+1)-h(n)| ≤ 1 for every n ≥ 1" with proof (§3), the multiplicity identity (2.1)–(2.2), the c_r correction (§5), and h through 10^9.
- The ledger row was committed as `995ee0e` "ledger sync 7s+7t" on 2026-07-28 01:19:30 UTC in ~/ErdosProblemADay.
- Wayback CDX: **first capture 2026-10-05 14:18 UTC**, second 2026-10-07. That is the earliest date a third party can verify. It is after G–I v1 (21 Sep), but G–I contain none of these results, so nothing is lost.
- github.com/pw/MathDyad is **private**, so `runs/erdos912_wave7t.md` there is not public evidence.

---

## Q2. Literature of the last ~30 days, and is there a G–I v2?

**Verdict:** nothing new on #912 anywhere. G–I is still v1 only.

- https://arxiv.org/abs/2609.25341, submission history: "[v1] Mon, 21 Sep 2026 19:31:21 UTC (17 KB)". No v2 and no Comments field.
  - So Theorem 1.2, the sentence "numerical calculations reveal that the ratio h(n!)/(n/log n)^{1/2} at n = 10^15 is equal to 2.57 . . ., which is somewhat larger", and the sentence "Since the second term in h_C(n!) turns out to be negative, it is not clear to us whether the Cramér model gives the correct prediction for this problem" all stand as in our stored text.
  - Minor: the PDF's internal "Date: September 23, 2026" differs from the arXiv v1 date. Cite the arXiv date.
- arXiv API: **all 1,081 math.NT submissions from 2026-10-01 to 2026-11-09**, keyword-scanned (factorial, distinct exponent, Cramér, floor, prime gap, short interval, Erdős problem, n!, Legendre, Gabdullin, Iudelevich, Heyman, Poisson…prime, random model).
  - I read every hit. None concerns h(n!) or #912, and none cites G–I. The nearest are 2610.34525 (frangible prime gaps), 2610.10582 (rough numbers in prime gaps) and 2610.27830 (RH short intervals).
  - A second filter for exponent–factorial phrases gave 0 hits.
- Semantic Scholar: 0 citing papers for arXiv:2609.25341.
- Tao's blog (WordPress API search for "912", "distinct exponents", "Gabdullin", "Cramer model", "Erdos problem"): no post on #912.
  - Relevant context: the **2026-10-06 guest post by Thomas Bloom**, "Changes to the Erdős problems web site": "A hiatus on problem comments and proof claims: I will freeze new problem comments and proof claims… suggestions for updates can be emailed to erdosproblemsonline@gmail.com"; "No problem statuses"; "No credit/ownership language to describe future solutions"; "An emphasis on high-quality expositions".
  - Bloom also writes: "it is, however, rude to use without permission the text from my site".
  - Tao's plot linked in the forum (terrytao.wordpress.com/output-2/) only goes up to n = 1000.
- MathOverflow: no new #912 question. The 2026-10-01 MO question 515657 (Leonardo Ursino) compares Pólya / Banks–Ford–Tao random-sieve models with Lemke Oliver–Soundararajan. Not #912, but relevant to Claim 4's sieve model (see Q5).

---

## Q3. Prior computations beyond 10^15? Comparisons with the exact Cramér or sieve models? Owmire's c_r?

**Verdict.**
- **h at 10^16, 10^17, 10^18: no prior values found.** At 10^15, G–I give only the ratio "2.57…"; I found no published value of h(10^15) itself.
- **Exact finite-n Cramér expectation vs actual: not done before.** G–I compare against their asymptotic expansion, qualitatively.
- **Sieve-corrected model for #912: not done.** G–I name it as open and harder.
- **Owmire's c_r: corrected only by our July report.** Nobody else.

Evidence:
- Other exact-h computations I found, all much smaller:
  - our July report, to 10^9 (h(10^9) = 18233)
  - Kruis, exhaustive to ≈1.655×10^11; he publishes only the run-boundary values
  - Owmire, to 10^8
  - agentic-erdos, to 5×10^7 (ratio 2.6485)
  - Eldar, to 10^7
  - the OEIS b-file, to 10^4
  - Tao's plot, to 10^3
- Web search for "13837595", "42289684", "129533241", "397503133" and OEIS search for "13837595": no hits.
- **Positive control I ran (stdout only, no files written): our `hfast` reproduces all six third-party values Kruis published.**

  | n | h from hfast | Kruis |
  |---:|---:|---:|
  | 1,784,800,611 | 23,962 | 23,962 |
  | 1,784,800,612 | 23,962 | 23,962 |
  | 1,784,800,619 | 23,956 | 23,956 |
  | 165,493,254,305 | 207,878 | 207,878 |
  | 165,493,254,306 | 207,878 | 207,878 |
  | 165,493,254,314 | 207,871 | 207,871 |

  hfast(10^9) = 18233 also matches the July report, and hfast(5×10^7) has ratio 2.648524, matching agentic-erdos's "≈ 2.6485". **Recommend adding these to the Instruments section**: they are the only outside checks above 10^4.
- G–I on sieve models: "It would be interesting to apply other models for the primes, such as the Cramér–Granville model (see, e.g., [13, Chapter 17]), to this problem, but this seems to be more difficult." Claim 4 is a first numerical answer to that stated suggestion; see the caveat on naming under Q5.
- G–I's own reasoning has a gap worth stating carefully if we discuss it. "Since the second term … is negative" ignores their positive third term (1+γ+log 8)/(2 log n), which at n = 10^15 is larger: −0.05128 vs +0.05294. Their expansion therefore *exceeds* √(2π) at every n we tested (2.5108, 2.5083, 2.5063, 2.5046). It is still well below the actual 2.5717 … 2.5591.
- On Owmire's c_r: the forum thread has exactly 2 comments (Tao, Owmire) and is now frozen. Owmire's profile shows only that one comment. OEIS, arXiv, MathOverflow and the third-party repos above say nothing about c_r.
  - The only correction is our July report §5: "c_r = Γ(r−½)/(√2 r!) = √(2π)(−1)^{r+1}C(1/2,r), not the C(2−√2,r) displayed in the 2026 tracker comment".
  - That report also already notes that "Those constants also happen to sum to √(2π), by the binomial series". So Claim 5, including its sum-check remark, is a repeat of our own July result, not a new one.

---

## Q4. Live erdosproblems.com, forum and database

**Verdict: unchanged since our fetch. No new comments, and none are possible now.**

- `/forum/thread/912`, `/912` and `/forum/thread/912/proof-claims`, fetched live via Hetzner at about 09:34 UTC. They differ from our stored copies only in Cloudflare email-obfuscation and beacon tokens (diffed).
  - "Comments (2)" (Tao, 31 Aug 2025; Owmire09, 24 Jun 2026); "Proof claims (0)"; "No proof expositions yet"; "The ability to post new comments has been suspended."
- `/history/912` shows one revision, 2025-10-20, a LaTeX/formatting change only. The current text is "A heuristic of Tao using the Cramér model…".
- teorth/erdosproblems `data/problems.yaml` entry for 912: `status: open, last_update: 2025-08-31`; `formalized: yes, last_update: 2026-01-26`; `oeis: ["A071626"]`. No comments field.
- google-deepmind/formal-conjectures `ErdosProblems/912.lean` (last content commit 2026-02-20): `erdos_912.variants.selfridge` is "research solved", while `erdos_912` and `erdos_912.variants.tao` are "research open". There is **no |Δh| ≤ 1 variant**.
  - Two 2026-03-03 PRs (#2585, #3109), both titled "formally solved variants.selfridge in 912", were *closed*.
- Practical consequence: there is no forum route for a write-up. Bloom's channel is email to erdosproblemsonline@gmail.com plus "high-quality expositions"; the brief says post nothing, so I posted nothing. His post also asks that his site's text not be reused, so quote only the problem statement.

---

## Q5. The planned Granville / Maier / Montgomery–Soundararajan sentences

### "the Cramér model is known to miss correlations coming from divisibility by small primes (Granville 1995 …; Maier 1985)"

**Verdict: the citations are real, but the sentence must be re-scoped.**

- **Granville 1995** is real: A. Granville, "Harald Cramér and the distribution of prime numbers", Scand. Actuarial J. 1995, no. 1, 12–28 (Harald Cramér Symposium). It is an expository survey. I OCR'd the PDF at dms.umontreal.ca/~andrew/PDF/cramer.pdf.
  - He does say the model ignores small-prime divisibility, and he proposes the fix: "from Cramér's model one expects that there are ~x/log² x prime pairs p, p+1 up to x, whereas our new model recognizes that one of these two numbers must be even".
  - His modified model: "Let Z_1, Z_2, … be a sequence of independent random variables with Z_n = 0 whenever n has a prime factor <T. When n is free of prime factors <T then Prob(Z_n = 1) = (∏_{p<T} p/(p−1))/log n … where T is a parameter to be chosen appropriately. Note that when T = 1 this is exactly Cramér's model; however, we shall take T to be at least some power of log x."
  - **But for our regime he says the opposite of what the sentence implies:** "Thus, for y large (≪√x), Cramér's model confirms what is known from assuming the Riemann Hypothesis, and for y small (≍log x), it confirms what is known from assuming a uniform version of the Hardy-Littlewood conjecture." This refers to Gallagher's theorem.
  - So Granville supports "Cramér ignores small-prime divisibility". He does **not** support "this is known to matter at interval length ≍ log n", and he says nothing about second-order terms there.
- **Maier 1985** is real: H. Maier, "Primes in short intervals", Michigan Math. J. 32 (1985), 221–225. I checked this via the reference lists of Granville and of M–S, not Maier's own text.
  - Granville's statement of it: "there exists a constant δ_N > 0 such that π(x_+ + log^N x_+) − π(x_+) > (1+δ_N) log^{N−1} x_+ for arbitrarily large values of x_+, and … < (1−δ_N) log^{N−1} x_− for arbitrarily large values of x_−". He also calls Maier's theorem "a severe blow to Cramér's model".
  - It concerns intervals of length (log x)^λ with λ > 1, at sparse exceptional x. Granville writes: "The values of x given by Maier's proof are scarce". It is **not** a statement about the average over ~√(n/log n) intervals of length ≍ log n, which is what #912 measures.
  - I did not verify Maier's own range of λ from his paper. Granville states it for N > 2; M–S print "for any fixed a > 0". Quote Granville's version if we quote one.
- **Corrected sentence (suggested).** "Cramér's model ignores divisibility by small primes (Granville 1995, who proposes the modified model in which integers with a prime factor < T are never prime and the rest are prime with probability ∏_{p<T}(1−1/p)^{−1}/log n; Maier 1985 shows the effect is visible in intervals of length (log x)^λ). At interval length ≍ log x the Cramér/Poisson law is correct to leading order under Hardy–Littlewood (Gallagher 1976). The first correction comes from the average of the singular series, Σ_{distinct d_i ≤ h} S(D) = h^k − C(k,2)h^{k−1} log h + O(h^{k−1}) (Montgomery–Soundararajan 2004, eq. (17)), a relative correction of order log h / log x ≍ log log x / log x when h ≍ log x. Corrections of this size are conjectured, and numerically observed, for consecutive-prime statistics (Lemke Oliver–Soundararajan 2016)."
  - Then present our 0.63–0.645·log log n/log n gap as *consistent with that order*, not as "known".
  - Gallagher reference: P. X. Gallagher, "On the distribution of primes in short intervals", Mathematika 23 (1976), 4–9; corrigendum 28 (1981), 86. This is the M–S reference [6]; Granville's text prints "1966", but the paper is 1976.

### "Montgomery–Soundararajan (2004) show the variance of primes in short intervals is smaller than the Cramér/Poisson prediction"

**Verdict: wrong as stated. It must say "conditionally" or "conjecture", and it must give the range.**

- Paper: H. L. Montgomery, K. Soundararajan, "Primes in short intervals", Comm. Math. Phys. 252 (2004), 589–617 (arXiv math/0409258). I verified the arXiv text; the journal reference is from secondary knowledge.
- Abstract: "Contrary to what would be predicted on the basis of Cramér's model concerning the distribution of prime numbers, we develop evidence that the distribution of ψ(x+H) − ψ(x), for 0 ≤ x ≤ N, is approximately normal with mean ∼ H and variance ∼ H log N/H, when N^δ ≤ H ≤ N^{1−δ}." Note the words "develop evidence".
- Theorem 3 is **conditional** on (20), "E_k(x;D) ≪ N^{1/2+ε} uniformly", a strong uniform Hardy–Littlewood hypothesis. It gives M_K(N;H) = μ_K H^{K/2} ∫_1^N (log x/H + B)^{K/2} dx + error, "uniformly for log N ≤ H ≤ N^{1/K}", with B = 1 − C_0 − log 2π.
- Corollary 1 (under the same hypothesis), for H/log N → ∞ and log H/log N → 0: the distribution is "approximately normal with mean 0 and variance H log N". **That is, in our regime the Cramér variance is correct at leading order.**
- The smaller variance H log(N/H) at H ≥ N^δ is **Conjecture 2**, not a theorem.
- The unconditional piece that matters for us is eq. (17) and Theorem 2 on singular-series sums: "Σ S(D) = h^k − C(k,2) h^{k−1} log h + C(k,2)(1 − C_0 − log 2π) h^{k−1} + O(h^{k−3/2+ε})".
- **Corrected sentence (suggested).** "Assuming a strong uniform Hardy–Littlewood conjecture, Montgomery–Soundararajan (2004) show that the variance of ψ(x+H) − ψ(x) is H(log(x/H) + B) rather than Cramér's H log x for log N ≤ H ≤ N^{1/K}, and conjecture H log(N/H) for N^δ ≤ H ≤ N^{1−δ}. At H ≍ log N the two agree to leading order, and the difference is a relative log log N / log N effect."

### Related context (optional to cite)
- **Lemke Oliver–Soundararajan**, "Unexpected biases in the distribution of consecutive primes", arXiv 1603.03720 (PNAS 2016). Main Conjecture: "π(x;q,a) = li(x)/φ(q)^r (1 + c_1(q;a) log log x/log x + c_2(q;a)/log x + O(1/(log x)^{7/4}))". It is conjectural (based on Hardy–Littlewood), and they report "the observed fit is very good".
- **Banks–Ford–Tao**, "Large prime gaps and probabilistic models", Invent. Math. 233 (2023), 1471–1518 (arXiv 1908.08613). This random-sieve model with growing z(t) is the principled modern version of our "sieve model z".
- **Granville–Lumley**, "Primes in short intervals: heuristics and calculations", arXiv 2009.05000 (v3 May 2021). It numerically compares short-interval prime counts with models, for y ≪ (log x)²; I read the abstract only. Possibly the closest computational precedent for Claim 4's method, though not for #912.

---

## Sentences in CLAIMS.md that must change

1. **"Tao (forum, 31 Aug 2025): Cramér ⇒ c = √(2π)."**
   - Why: Will Sawin derived it first, on MathOverflow 413332 on 2022-01-07: "That said, the Cramér random model suggests that c is exactly ∫_0^∞ (1 − e^{−2/x²}) dx = √(2π), if I did the calculation right".
   - Sawin's answer also has the reduction: "For primes p > √n, the exponent of p is simply ⌊n/p⌋. So an equivalent problem is to count the number of 1 ≤ k ≤ ⌊√n⌋ such that the interval (n/(k+1), n/k] contains a prime."
   - Tao commented under that answer on 2022-01-07: "Most likely a sufficiently uniform version of the k-tuple conjecture would imply an averaged version of the asymptotic…".
   - Replace with: "Sawin (MathOverflow 413332, 7 Jan 2022) and, independently in writing, Tao (forum, 31 Aug 2025): Cramér ⇒ c = √(2π)." Also fix "Tao's heuristic" wherever the write-up uses it.

2. **"Owmire (forum, 24 Jun 2026): computed h(n+1) − h(n) ∈ {−1,0,1} for n ≤ 10^8, 'a proof seems intractable to me'"**
   - Why: as quoted it is accurate, but it implies Owmire originated the conjecture. Eldar conjectured it on OEIS A357385 on 26 Sep 2022, checked to 10^7.
   - Prepend: "First conjectured by Eldar (OEIS A357385, 26 Sep 2022, checked to 10^7); …".

3. **"## Claim 2 (ours, elementary). Theorem For every n ≥ 1, |h(n+1) − h(n)| ≤ 1."**
   - Why: the bound is ours, but it is not new today. We first proved it, by a different route, in the erdosproblemaday.com/report/912 working report (committed 2026-07-28; publicly archived 2026-10-05).
   - Say so, and state what is new now:
     - the exact indicator formula (b);
     - the move rule "h moves only at n+1 = kQ, Q prime, Q² > n+1";
     - the prime-square case h(q²) = h(q²−1) for q ≥ 3. The July report had only "Their difference is 0 or 1". Against the b-file, all 24 odd prime squares up to 10^4 give 0, and the only move without a prime factor above √m is m = 4.

4. **"Corollaries: h(n+1) = h(n) when n+1 ≥ 5 is prime (Bertrand gives a prime with exponent 1)"**
   - Why: Eldar recorded it on OEIS A357385 (2022) as "a(p) = 0 for an odd prime p". That is off by one: the entry's own data has a(3) = a(5) = 1, and the intended statement is a(p−1) = 0.
   - Credit it as "recorded (mis-indexed) by Eldar".
   - Minor: it also holds at n+1 = 3, since h(3) = h(2) = 1, so "≥ 5" is merely conservative.

5. **"Also: h(n) = π(√n) + #{⌊n/p⌋ : √n < p ≤ n} (Lemma at x = n: exponents of primes ≤ √n are distinct and exceed all others)."**
   - Why: this decomposition is the structure of Heyman–Miraj's proof of Theorem 2 (§3, eqs. (2)–(3): "every prime not exceeding √X adds exactly 1 to the cardinality", and v_p(X!) = ⌊X/p⌋ for p > √X). It is also eq. (2.2) of our July report, and Sawin's 2022 reduction.
   - It is not new. The only addition is that our Lemma supplies the "exceed all others" separation, which HM's written proof leaves implicit.

6. **"## Claim 1 (ours, elementary). Lemma (isolation)"**
   - Why: the part "exponents of primes p < q ≤ √x are distinct" is in Heyman–Miraj §3: "For any two primes 2 ≤ p < q ≤ √X … v_p(X!) = Σ ⌊X/p^t⌋ > Σ ⌊X/q^t⌋ = v_q(X!)". It is also in our July report §2, which has the ⌊n/m⌋ > ⌊n/(m+1)⌋ separation.
   - Label it "ours in this form". What is ours: the statement for all q with q² ≤ x+1, including boundary case (iii) q² = x+1, and the explicit e_x(q) > e_x(q⁺) separation. That is exactly what Claim 2 needs at a prime-square step.

7. **"## Claim 5 (ours, calculus). Owmire's c_r is not the Cramér limit"** and **"Both families sum to √(2π) … which is why a sum check cannot tell them apart."**
   - Why: both appear verbatim in substance in our July report §5, publicly archived 2026-10-05: "c_r = Γ(r−½)/(√2 r!) = √(2π)(−1)^{r+1}C(1/2,r), not the C(2−√2,r) …"; "Those constants also happen to sum to √(2π), by the binomial series".
   - Label it "ours, first given in our July 2026 report". Nobody else has pointed it out: the forum has 2 comments and is frozen, and OEIS, arXiv, MO and the repos are all silent.

8. **"## Claim 4 … The Cramér model's finite-n prediction is wrong by hundreds of its own SDs"**
   - Why: the numbers are fine, but G–I already observed, qualitatively, that the actual ratio at 10^15 (2.57…) exceeds the Cramér prediction. Credit them: "G–I observed the 2.57 at 10^15 and doubted the model; we quantify it…".
   - Also say "SD of h_C under the model". The SD is the model's sampling spread, not an error bar on a prediction for the real primes.
   - Be careful with G–I's "second term is negative" logic. Their positive third term dominates at these n, and their expansion gives 2.5108 … 2.5046, above √(2π).

9. **"Reading: the 2.57 at 10^15 is the Cramér model's known blindness to small-prime divisibility (Granville 1995) acting at second order"**
   - Why: Granville (1995) states that at y ≍ log x the Cramér model "confirms what is known from assuming a uniform version of the Hardy-Littlewood conjecture". He gives nothing about second-order terms at that scale. Maier's theorem is about (log x)^λ, λ > 1, at scarce x.
   - The right anchor for a log log n / log n second-order effect is the singular-series lower-order term: M–S 2004 eq. (17) (unconditional statement about S(D)), with Lemke Oliver–Soundararajan 2016 (conjectural, numerically supported) as the precedent for such corrections. Use the corrected sentence under Q5.
   - "Known" may describe the mechanism. Its application to #912, and the 0.63–0.645 coefficient, are ours.

10. **"Sieve model z (integers coprime to P_z = ∏_{p≤z} p are prime w.p. θ_z/log l …)"**
    - Not wrong, but name it correctly: it is Granville's 1995 modified model with T = z *fixed* (≤ 19). Granville takes "T to be at least some power of log x".
    - Do not call it "the Cramér–Granville model" when answering G–I's suggestion; their pointer is to the model in Koukoulopoulos, Ch. 17. Say "a fixed-depth Granville sieve model".
    - Optionally note that the residual ~5% at z = 19 is what a growing depth, such as the Banks–Ford–Tao calibration, should address.

11. **The planned Montgomery–Soundararajan sentence** (from the brief; not yet in CLAIMS.md): "show the variance … is smaller than the Cramér/Poisson prediction".
    - Why: the result is conditional (Theorem 3, assuming a strong uniform Hardy–Littlewood bound) or conjectural (Conjecture 2 for H ≥ N^δ), and in our range (log H/log N → 0) their Corollary 1 *agrees* with Cramér at leading order.
    - Use the corrected sentence under Q5.

### Sentences that check out (no change needed)
- "Gabdullin–Iudelevich, arXiv 2609.25341 v1 (21 Sep 2026), Thm 1.2 …": the formula matches the paper verbatim, including "With probability 1" and "for all n ≥ 2"; it is still v1 as of 2026-11-10. The "2.57…" sentence and the "not clear to us whether the Cramér model gives the correct prediction for this problem" sentence are verbatim.
- "Heyman–Miraj (arXiv 2309.16072): h(n) = #{⌊n/p⌋ : p ≤ n} exactly.": correct. Cite v4 (16 Jul 2024), proof of Theorem 2: "We will show that |Sp(X)| = |α(X!)|".
- "Erdős–Selfridge: h(n) ≍ (n/log n)^{1/2}.": correct (Erdős 1982, Theorem 1: "Recently Selfridge and I proved").
- Owmire quotes: verbatim, including "by the same Cramer model as Tao (the other comment)" and "though a proof seems intractable to me".
- Claim 3 values: the first published exact values at 10^15–10^18 that I can find. 10^15 agrees with G–I's 2.57…, and the instrument reproduces Kruis's six independent values at 1.8×10^9 and 1.65×10^11.
