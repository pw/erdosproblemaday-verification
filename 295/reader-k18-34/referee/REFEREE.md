# Referee report — Bae, "A 34-term unit-fraction expansion with minimum denominator 18"

Submission received 2026-10-11 12:08Z (github.com/qorud02/erdos-295-k18 v1.0.0, Zenodo 10.5281/zenodo.23297810).
Referee: hostile mode (try to refute). Report date 2026-10-11.
None of the submitter's code was executed or compiled. Every computation below is the referee's own code in
`/tmp/erdos295-referee/`, run with `python3 -I`.

Files read: NOTE.md, README.md, proofs.md (Korean; translated below), erdos295-note.tex, CITATION.cff,
certificate-34-independent.json, verify-certificate.py, search-independent.py, search-strong.py, search-cpp.cpp,
early-n18-t32.log, cpp-n18-t32.log, independent-native-validation.jsonl, manifest-sha256.json, the Zenodo record and the
GitHub repo/user API records. The first download did NOT include the engine the README names
(`search-earlyterminal.py`), nor `search-terminalbound.py`, `search-fasttail.py`, `search-runner.py`,
`search-native.cs`, `run-native.ps1` or the CI workflow. I fetched these from raw.githubusercontent.com (tag v1.0.0)
into a separate directory, `/tmp/erdos295-sub2/`. All ten match `manifest-sha256.json` byte for byte, and so do the
13 files in `/tmp/erdos295-sub/`.

---

## 1. Certificate — PASS

Checker: `cert_check.py`. It keeps a running exact sum num/den ← (num·d + den)/(den·d) and reduces by gcd at each
step. It does not use `fractions` or `lcm`.

- D has 34 elements, all distinct, min 18, strictly increasing; the sum reduces to **1/1**. PASS. This agrees with your
  three routes (Fraction, LCM, PARI).
- Surgery: 1/42+1/640+1/337280+1/1735650+1/68479214496 and 1/46+1/275+1/14143068+1/10457416992 both equal
  **577164227639/22744881957600**. Our 35-set minus the five, plus the four, is exactly D. Our 35-set sums to 1.
- M = lcm(old ∪ new) = 636856694812800. M·577164227639/22744881957600 = 16160598373892 exactly. L = 6209352774424800.
  Both match the note.
- Negative controls, all rejected:
  - 275→276 gives 75899/75900.
  - Last term +1 gives 109357570155027745055/109357570155027745056.
  - Last term −1 gives …073/…072.
  - 18→17 is flagged "min < N" and gives 307/306.
  - 275→46 is flagged "not distinct".

So **k(18) ≤ 34 is a theorem.**

Factorisations (for the record): 275 = 5²·11; 14143068 = 2²·3²·19·23·29·31; 10457416992 = 2⁵·3·11·17·19·23·31·43.

## 2. The note's claims (NOTE.md and erdos295-note.tex)

Every mathematical sentence is true. The objections below concern framing and attribution, not mathematics.

**(a) Splitting argument — VALID.**
> "Excluding exactly 32 terms also excludes every shorter expansion: replace its largest denominator d by d+1 and
> d(d+1) … The new denominators exceed every retained denominator."

- Every retained term is < d < d+1 < d(d+1), because d ≥ 18 > 1. So the result is distinct, still ≥ 18, and has the
  same sum.
- Each step adds one term, so any m < 32 expansion lifts to a 32-term expansion.
- It is the standard monotonicity of k. It makes his k(18) ≥ 33 rest on his 32-term run alone, and that is
  legitimate.

**(b) Reference [1] — ACCURATE.**
- His title "Erdős #295: k(17) = 32, and now 33 ≤ k(18) ≤ 35 by exact exhaustion" is our title with "Erdős"
  prefixed.
- The date (2026-08-11), the slug, and "exhaustive exclusions of 31 and 32 terms" are all correct.

**(c) Attribution — mostly correct, with three objections.**

1. > "The construction can also be obtained from the 35-term certificate published by Patrick White with Claude"

   "Can also be obtained" understates the dependence. 30 of the 34 denominators are ours, and the set is
   literally our 35-set with five terms swapped for four. His own Zenodo description states it correctly:
   > "The construction replaces five terms of the 35-term witness reported by Patrick White and Claude … with four
   > terms."

   NOTE/tex should use that sentence. Separately, the note never says how the construction was found. proofs.md §5
   (a CRT/0-1 model over a "finite denominator candidate set", k ∈ {33,34}) and "optimization solver" suggest a
   solver run over a candidate set built from our identity. Worth asking.

2. > "Together with the previously reported computational lower bound, independently reproduced in the accompanying code"

   This appears in the abstract and the first paragraph, and the tex abstract carries no citation. The lower bound
   is ours. The citation should be in the abstract.

   "Independently" is also too strong. With his prime prune switched off, his search tree is *state for state*
   ours (§4 below). His interval sentence is our page's sentence. His three engines are ports of one another: the
   jsonl itself says "independent GMP UI primitive port" and "parent GMP joint-prime implementation copied into
   independent audit harness". Honest wording would be a *decorrelated re-implementation with two additional
   proved pruning lemmas*. The note's own sentence
   > "The programs share the same mathematical recurrence; their agreement cross-checks implementation and arithmetic."

   is the right register.

3. > "At two terms, the forced final denominator is y=bx/(ax−b). Its integrality is checked exactly, without an imposed denominator cap."

   This is true of the code but **misleading as a description of the run**.
   - Not one two-term candidate was ever tested. The C++ log has `"two_candidates":0`. The Python log has
     `terminal_scans 0`, `terminal_divisors 0`, and no `quadratic_two_candidates` key at all. My re-implementation
     agrees: 648,193 two-term states, all 648,193 killed by the §3 inequality, 0 candidates.
   - So the terminal level of his exclusion rests entirely on lemma §3, plus §2 at t ≥ 3. No exact integrality test
     carries any weight.
   - §3 is correct (see §3 below), so nothing breaks. But the note should say "every terminal state was eliminated
     by the quadratic inequality of proofs.md §3; the explicit integrality branch was never reached." As written,
     a reader would credit the wrong mechanism.

Minor:
- > "The full certificate was also checked with an independently written JavaScript BigInt calculation."

  This is not in the release, so it cannot be checked. It does not matter, because the certificate checks
  trivially.

## 3. The lemmas in proofs.md

Translation summary (mine):
- **§1** finite next-denominator interval plus the harmonic bound H(x,t).
- **§2** p-adic forced denominator.
- **§3** two-term quadratic condition.
- **§4** divisor form (ax−b)(ay−b)=b².
- **§5** CRT 0/1 model used to *find* constructions.
- **§6** sqrt-free terminal test.
- **§7** joint multi-prime partition bound.

**§1 — SOUND.**
- x > b/a: a positive tail must remain when t ≥ 2.
- a/b ≤ H(x,t) ≤ t/x, so x ≤ ⌊tb/a⌋.
- H(·,t) is strictly decreasing, so the binary search is valid.
- It is identical to our published recurrence.

**§2 — SOUND.** The exposition has one small gap.
- *At least one multiple of p^e*: if every remaining denominator has v_p ≤ e−1, the sum has v_p ≥ −(e−1). But a/b
  has v_p = −e, because a/b is reduced so p ∤ a. Correct; it needs reduction, which every engine maintains.
- *≥2 multiples*: bound by the max sum over t-sets containing q₁ = p^e⌈D/p^e⌉ and q₂ = q₁+p^e, with the rest the
  smallest integers ≥ D other than q₁, q₂.
  - The text says "replace the larger multiples with q₁, q₂ in turn". That needs the replaced multiples to be the
    **two smallest** multiples m₁ < m₂ in the set. Only then does m₁ ≥ q₁, m₂ ≥ q₂ hold and q₁, q₂ ∉ S∖{m₁,m₂}.
    (q₁ ∈ S forces m₁ = q₁; q₂ ∈ S∖{m₁,m₂} contradicts minimality.)
  - With that reading the bound is correct. The text should say "the two smallest multiples".
- *Exactly one multiple x*: v_p(x) = e, since otherwise the unique maximal valuation survives in the sum.
  - Multiplying by p^e: a/v = 1/u + Σ p^e/d with every p^e/d ∈ pℤ₍ₚ₎. So u ≡ v·a⁻¹ (mod p) and
    x ≡ p^e·(v a⁻¹ mod p) (mod p^{e+1}). Correct.
  - The bound with the smallest such x ≥ D forced is valid: the rest cannot contain that x, since it is a multiple
    of p^e.
- Requiring both cases to fail before pruning is correct.

**§3 — SOUND.**
- With g = gcd(x,b), x = gu, b = gv, and c = au−v > 0: gcd(c,u) = gcd(v,u) = 1 and gcd(c,v) = gcd(au,v) = 1. The
  second uses gcd(a,b) = 1.
- So y = gvu/c is an integer iff c | g iff (ax−b) | g². Then ax−b = gc ≤ g² ≤ x², i.e. f(x) = x²−ax+b ≥ 0.
- When a² > 4b: x < 2b/a < a/2 < r₊, so x ≤ r₋.
- With s = ⌈√(a²−4b)⌉: x ≤ r₋ ⇔ √Δ ≤ a−2x ⇔ a−2x ≥ s ⇔ x ≤ ⌊(a−s)/2⌋. The endpoint rounding is exact, including the
  perfect-square case.

**§4 — SOUND.** (ax−b)(ay−b) = b² is equivalent to a/b = 1/x+1/y. It was never used in the 32 run
(`terminal_divisors 0`).

**§5 — SOUND as stated.**
- L | S is forced by CRT, and 0 < S/L ≤ k/18 < 2 for k ≤ 35, so S = L.
- It explicitly says a candidate-set computation speaks only for that set.
- It is not load-bearing for any claim.

**§6 — SOUND.** f(L) < 0 ⇒ Δ > 0 ⇒ U = ⌊2b/a⌋ < a/2 ⇒ f is decreasing on [L,U] ⇒ f < 0 throughout.

**§7 — SOUND as written.**
- Each prime power of b is assigned to some denominator. Blocks of the induced partition π correspond to distinct
  denominators, each ≥ Q_B = P_B⌈D/P_B⌉ (P_B = product of powers of distinct primes = lcm).
- Rest ≤ H(D, t−|π|).
- The C++ `joint_obstruction` uses a *stronger* bound than §7 states. It adds 1/max(Q_(j), e_{j−1}+1) in sorted
  order instead of 1/Q_B with overlap allowed.
  - I checked that this is still valid: in any admissible set, s_{t−m+k} ≥ Q_(k), because at least m−k+1 elements
    are ≥ Q_(k). Hence s_i ≥ E_i elementwise.
  - So code ≠ doc, but the code is sound. It is off by default (`joint=false`; `joint_prunes 0` in the 32 run) and
    plays no part in the result.

**Numerical controls** (`lemma_controls.py`, `quad_regime.py`, `walk_certs.py`):

- **§3, exhaustive small range.** Over all reduced a/b with b ≤ 500 and a < 2b:
  - 14,514 two-term solutions.
  - 0 with f(x) < 0.
  - 0 mismatches of "y integral ⇔ (ax−b) | g²", over every x in (b/a, 2b/a).
  - 2,792 solutions with a² > 4b, 0 above (a−s)//2, and **2,343 exactly at it**. The bound is sharp, so an
    off-by-one would kill real solutions. It does not.
- **§3, in the regime the search lives in.** 300,000 random a/b = 1/x+1/y with x ∈ [18,200] and y up to 10⁴⁰:
  - 296,226 have a² > 4b.
  - 0 bound violations.
  - 0 cases where the prune fires despite the solution.
  - 292,155 are tight at the bound.
- **§2, random sets.** 20,000 random t-sets (2 ≤ t ≤ 9) with prime-power-heavy elements, giving 113,224
  (set, p^e‖b) pairs:
  - 0 sets with no multiple.
  - 99,984 exactly-one cases, with 0 valuation errors and 0 congruence failures.
  - 0 bound violations in either case.
  - The prime test fired on a *genuine* set 0 times.
  - Example: S = {40,52,64,71}, sum 21839/295360, 2⁶‖b. The unique multiple is 64, and the predicted class is
    64 mod 128.
- **Real certificates.** Walked state by state through every prune: Bae-34, our 35, our k(17) 32, and Alekseyev's
  a(16), a(15), a(13), a(11) witnesses. No prune fires along any true path, and every unique-multiple congruence
  holds (e.g. 3³ forces 54 ≡ 54 mod 81 at depth 10).

## 4. The implementation

Engine chain for the logged run: search-runner → search-earlyterminal → search-terminalbound → search-strong →
search-independent (subclass overrides, module re-binding of `_base.Search`). I traced it; the class actually
instantiated is the early-terminal `Search`.

What it does:
- **DFS order.** x runs over range(lo, hi+1), with lo = max(d, b//a+1) and hi = the largest x ≤ ⌊tb/a⌋ having
  H(x,t) ≥ a/b (exact Fraction binary search). The child gets d = x+1. So the sequence is strictly increasing with
  the correct endpoints.
- **Residual.** Reduced by gcd at every step. The C++ `subtractunit` shortcut is algebraically correct; I re-derived
  that gcd(c, b'x') = 1.
- **Terminal.**
  - The early check fires only under `a*a>4*b`, with s = ⌈√Δ⌉ computed as isqrt+1 when not a square, and tests
    (a−s)//2 < max(d,b//a+1). This is exactly §3.
  - The C++ guards with `delta>0`. Its f(lo) < 0 test needs no guard (§6).
  - The explicit test is exact divmod(bx, ax−b), rem == 0 and y > x, with no cap (`cap=None` throughout).
- **Prime test** (`search-strong.py`; identical logic in the C++ and C#):
  - It skips the prime when q₂ < d+t, because then the ≥2 bound equals H(d,t) ≥ a/b and there is no prune
    anyway.
  - The exactly-one branch is entered only after the forced-{q₁,q₂} bound fails.
  - `pow(a,-1,p)` / `mpz_invert` would *raise*, not silently prune, if gcd(a,p) ≠ 1. That cannot happen because the
    residual is reduced.
  - The prime list contains only certified primes: trial division ≤ 10⁴, and the cofactor is appended only when
    d² > cofactor. A composite there would be unsound, and it cannot occur. The C++ `(int)` cast of that cofactor is
    safe (< 10001²).
  - Memo key (a,b,d,t) omits the prime list. That is fine, because failure is a property of the state.
    `memo_hits` = 0 anyway.

**I found no prune that can discard a valid branch.** Nothing the brief asked about happens here:
- no prime condition applied without gcd(a,p) = 1;
- no endpoint off by one;
- no exponent-e congruence applied while two multiples were still possible;
- no terminal bound applied without checking a² > 4b.

**Re-execution by my own code.** `ref_search.py` is written from the lemma statements, not from his code, using
integer cross-multiplication. All exhausted at N=18:

| mode | t | states | two-term states | terminal outcome | prime prunes | failed |
|---|---|---|---|---|---|---|
| §2+§3 (his algorithm) | 32 | **814,918** | 648,193 | all quadratic-pruned, 0 candidates | **134,999** | **31,726** |
| §3 only, no memo | 32 | 14,678,224 | 11,753,049 | all quadratic-pruned | — | — |
| plain (no §2, no §3) | 32 | **14,678,224** | **11,753,049** | **114,603,091** x scanned, 0 hits | — | — |
| §2+§3 | 31 | 38 | 0 | — | 18 | 20 |
| plain | 31 | 20,293 | 13,139 | 69,727 scanned | — | — |

- Row 1 equals his Python, C# and C++ logs exactly. Row 4 equals his C# t=31 record.
- Rows 3 and 5 equal **our** published counters exactly. That is a third-party reproduction of our run.
- Audit pass: every one of his 648,193 quadratic-pruned terminal states was re-scanned in full: 19,527,066
  candidates, 0 solutions.

End-to-end soundness with solutions present (`enum_compare.py`): enumerate *all* solutions with §2+§3 on versus all
off, memo off.
- Identical solution sets for N=2..10 at t = a(N) and above:
  - e.g. N=5, t=11: 40,105 = 40,105;
  - N=4, t=9: 9,351 = 9,351;
  - N=10, t=19: 13 = 13, with 59,684 prime prunes and 484,318 quadratic prunes exercised.
- Random residual states: 23,095 states, each built as a sum of t ≤ 5 distinct unit fractions ≥ d, so every one has
  at least one solution. 345 were skipped over a 300k-state budget.
  - 477,764 solutions in the unpruned enumeration.
  - **0 solution-set mismatches.**
  - 152,159 prime prunes and 3,099,086 quadratic prunes exercised (`enum_random2.py`).
- Regime control: his algorithm (my implementation) at N=17, t=31 exhausts after 72,764,818 states, 7,374,920 prime
  prunes and 63,048,179 quadratic prunes. That is consistent with our k(17) = 32.

Seeded control (`seeded.py`): fix the first 34−m terms of Bae-34 and search the last m (m = 2..6). The pruned search
re-finds the certificate tail every time, e.g. m=6: 503,216 states, 1,702 prime prunes, 497,684 quadratic prunes,
witness found. The m=7 run hit the 15-min background limit and was stopped; it counts as not run. First-witness
searches at (N=17, t=32) and (N=18, t=35) were also stopped incomplete after 33 min; no result is claimed for them.

**Verdict on the implementation.** Assuming his logs are honest — and they are reproducible: my independent code hits
all four counters to the unit — his exhausted run is a valid exact proof of the 32-term exclusion, modulo §2 and §3.
I have proved and stress-tested both lemmas.

It is **not** an independent method:
- With §2 off, the tree is ours, state for state.
- The terminal step swaps our explicit scan for a proved inequality.
- The 134,999 prime prunes cut that tree by 18×.

Value as confirmation:
- It cross-checks our arithmetic with a different terminal mechanism and a different pruning set.
- Because the full unpruned tree also exhausts (row 3), the instance itself confirms that his prunes discarded no
  solution.

## 5. Novelty

| query | result |
|---|---|
| `"k(18)" Egyptian fraction … "34"` (WebSearch) | nothing on k(18) |
| `"14143068" OR "10457416992" unit fraction` | nothing |
| `"34 unit fractions" "at least 18" sum to 1` | nothing (arXiv 1603.07035, two-digit denominators, unrelated) |
| `A192881 a(18) …` | A192881 data ends at a(16)=30 |
| `Erdős problem 295 k(18) unit fractions 33 34 terms` | erdosproblems /295 and /history/295; arXiv 2403.17041 (a different unit-fraction problem); nothing on k(18) |
| `"k(18)=33" OR … "k(18) = 34" Egyptian` | nothing relevant (OEIS A395997, unrelated) |
| `"Kyunghan Bae" Erdős 295` | nothing |
| `"1735650" "68479214496" Egyptian fraction` | **nothing** |

The last row is a **positive control that failed**. These two numbers are printed in A192881's example text (the a(16)
witness), and the search engine still returned nothing. So web-search negatives here are coverage claims and carry
little weight.

The direct reads are what count:
- **OEIS A192881 JSON**, fetched via Hetzner today: revision 58, 2026-05-30. Data ends at
  1,3,…,28,30 (a(16)). The a(11)–a(16) witnesses are Alekseyev's. Nothing at n ≥ 17.
- **Múgica's a192881.txt**: decompositions through n=10 only.
- **erdosproblems.com/295**, its forum thread, and its single proof claim. The claim, by "tienxion" (GPT-6/Codex,
  2026-09-04), is about lower bounds under denominator restrictions, not k(18).

Derivability:
- The new identity removes 42, 640, 337280, 1735650 and 68479214496. The last two are the pair shared by Alekseyev's
  a(16) witness, our k(17) identity and our 35-set. So the 34-set is not a sub-list of any published witness.
- 14143068 and 10457416992 occur nowhere I can reach.
- **I find no prior statement of k(18) ≤ 34.** Priority then sits with our 35 (2026-08-11) → Bae 34 (2026-10-11).

## 6. Our page (`/day/295-k17-exact`, src/index.js ~2028–2215)

Once this is published as a reader result, the following become false or misleading.

**False:**
- Summary:
  > "Whether k(18) is 33, 34, or 35 remains open, as does Erdős's asymptotic question."

  35 is now excluded as the value.
- Body:
  > "We have not found a 33- or 34-term identity, nor excluded either length; k(18) could be 33, 34, or 35."

  A 34-term identity now exists.

**Stale as headline / current-state claims** (true only as history):
- Title:
  > "#295: k(17) = 32, and now 33 ≤ k(18) ≤ 35 by exact exhaustion"
- Summary:
  > "Round 2 now proves the rigorous computational bounds 33≤k(18)≤35."
- Body:
  > "Round 2 (11 August): the next cutoff is narrowed to three values."

  plus the displayed "33 ≤ k(18) ≤ 35." It is now two values: 33 ≤ k(18) ≤ 34.
- The "The 35-term upper certificate" section stays correct but is superseded. Add the 5-for-4 surgery and credit
  Bae (Zenodo DOI).

**Should be extended:**
- "The OEIS connection" paragraph only states a(17)=32. The same logic now gives **33 ≤ a(18) ≤ 34**, since Bae's
  identity starts at 18.

**Elsewhere on the site** (already stale before this submission):
- `src/ledger_data.js:93`, the #295 gist, still reads
  > "prove 31 <= k(17) <= 32, but … the 31-versus-32 case remain open"

  That has been false since Round 1.
- `verification/295/README.md` and `verification/295/k18/README.md` are dated bundles. A one-line "superseded upper
  bound" note is enough.

## 7. Verdict

**VERIFIED** — for the submission's claim that k(18) ≤ 34, hence (with our lower bound) 33 ≤ k(18) ≤ 34.

- The 34-term identity checks exactly. My checker uses no fractions or lcm, and its negative controls reject.
- It is a valid 5-for-4 surgery on our 35-term certificate.
- I found no prior statement of the bound.
- Every mathematical sentence in the note is true.

Required wording fixes before we quote it:
1. Say plainly that the set *is* our 35-set with a 5-for-4 replacement. Zenodo already does; "can also be obtained"
   does not.
2. Cite the lower bound to us in the abstract.
3. Do not describe the terminal step as an exact integrality check. In the logged run it was never executed; all
   648,193 terminal states fell to the §3 inequality.
4. Replace "independently reproduced" with "re-implemented with two additional proved pruning lemmas".

None of these affects correctness.

**Lower-bound reproduction:** a sound, exactly reproducible re-execution of the 32-term exclusion.

What it establishes:
- k(18) ≥ 33 again, by a program whose two extra prunes (§2 p-adic, §3 quadratic) are correct. I proved both and
  stress-tested both with zero failures.
- Its counters are reproduced to the unit by a third implementation written from the lemma text.

What it does not establish:
- It is not an independent mathematical method. With §2 off it is our search tree, state for state.
- His three engines are ports of one another.
- It adds two lemmas to the trusted base.
- It is a computational result, not an elementary proof.
- It says nothing about whether k(18) = 33. His jsonl shows partial 33-term prefix runs, none claimed.
