# Seat W report — the world around OpenAI's "Squarefree values of quartics and power-free values of polynomials" (Erdős #978)

Scope of this seat: Erdős's sources, priority, competing claims, the cited literature, the status record, and what is new. All
quotes are from documents fetched today (2026-10-22); scratch, downloads and scripts are in `seats/W_work/`.

## 1. What Erdős actually asked, and where

**[Er53] Erdős, J. London Math. Soc. 28 (1953) 416–425** (`users.renyi.hu/~p_erdos/1953-02.pdf`, page images checked):
- p. 416 setup: f has integer coefficients "with highest common factor 1", degree l, "highest coefficient in f(x) is positive".
  Irreducibility is **not** assumed.
- p. 417 Theorem: "If l ≥ 3 and f(x) satisfies the conditions stated above, then there are infinitely many positive integers n for
  which f(n) is (l−1)-th power free." The power-of-2 exclusion is introduced **for the (l−1) question**: "if l is a power of 2,
  l! is divisible by 2^{l−1} … We must therefore exclude this case." Positive density for (l−1): "It seems very likely … but this I
  have not been able to prove."
- p. 425 (last page, confirmed by page header): "I have also not been able to prove, for example, that n⁴+2 is squarefree for
  infinitely many n." **This is the only (l−2) content in 1953. It is a remark, not a question with hypotheses.**

**[Er65b] Erdős, "Some recent advances and current problems in number theory", Lectures on Modern Mathematics III (1965)**
(`1965-17.pdf`). Section 6 opens on p. 213: "Let f(x) = a₀xⁿ + ⋯ + aₙ be an irreducible polynomial with integral coefficients."
p. 219 (page image checked): "I proved [37] that if k > 2 then f(x) represents infinitely many (k − 1)-th power-free integers, the
only exception being that if k = 2^l then it may happen that f(n) ≡ 0 (mod 2^{l−1}) …" and then "**I could prove nothing about the
representation of (k − 2)-th power-free numbers, for example, I cannot show that n⁴ + 2 represents infinitely many squarefree
numbers.**" Hypotheses in force: irreducible, integer coefficients, degree k. No fixed-divisor condition, no sign condition, no
"k > 3" (implicit: k − 2 ≥ 2).

**[Er81h] Erdős, "Some problems and results on additive and multiplicative number theory", Analytic number theory (Philadelphia
1980), LNM 899 (1981) 171–182** (identified via erdosproblems.com/bibs/Er81h fetched through Hetzner; file `1981-33.pdf`). p. 178
(page image checked): "I proved that every irreducible cubic polynomial represents infinitely many squarefree integers and Hooley
that the set of integers n for which the cubic polynomial f(n) is squarefree has positive density. It seems hopeless at present to
extend this result to quartic polynomials; in fact **there is no quartic polynomial about which we can prove that it represents
infinitely many squarefree integers** …"

**The erdosproblems.com formulation** (page last edited 31 Mar 2026) is Bloom's normalisation, not Erdős's text: part (ii)'s
local condition ("for all primes p there exists n such that p^{k−2} ∤ f(n)") was added on 31 Mar 2026 after the DeepMind
counterexample (Bloom in the thread: "Indeed (this has been changed)"), and "k > 3" was added after FC PR #3408 (3 Mar 2026).
**Formulation defect on the page (not OpenAI's):** the preamble "suppose that k ≠ 2^l" is Erdős's (k−1)-specific exclusion and,
read literally, removes degree 4 and 8 from part (ii) — including the quartic case the page then asks about in part (iii). A
thread comment (Dogmachine, 19 Sep 2025) already raised this. FC's `erdos_978.parts.ii` keeps `¬ ∃ l, natDegree = 2^l`, so FC's
part (ii) as formalised is about degrees 5, 6, 7, 9, 10, …; quartics enter FC only through `parts.iii` (n⁴+2).

**Does OpenAI's theorem answer each question, under Erdős's/the page's hypotheses?**

| Question | Source | Answered by OpenAI? |
|---|---|---|
| (i) (k−1)-free, positive density | Er53 p. 417; Er65b p. 219 | Not addressed — Hooley 1967 (paper says so). |
| (ii) (k−2)-free infinitely often, k > 3 + local condition | Er65b p. 219 as normalised by the page | **Yes, stronger**: Cor 1.2 gives the full Euler-product density c X + o(X), c > 0, for every irreducible f of degree d ≥ 4 with ρ_f(p^{d−2}) < p^{d−2} ∀p. It does **not** need k ≠ 2^l nor a positive leading coefficient (Lemma 2.3 removes sign and content). The paper's local condition is word-for-word the page's. New content: d = 4…8 (Thm 1.1); d ≥ 9 is Browning. |
| (iii) n⁴+2 squarefree infinitely often | Er53 p. 425; Er65b p. 219; Er81h p. 178 ("no quartic polynomial") | **Yes**: Eisenstein at 2; local condition: 4 ∤ n⁴+2 for all n and f(0)=2. Density c = ∏_p(1−ρ(p²)/p²); I computed c ≈ 0.7567 (Euler product to p < 2·10⁴: 0.756687; empirical n ≤ 2·10⁴: 0.75635). Er81h's "no quartic polynomial" is answered for every irreducible quartic with no fixed square divisor. |

The theorem's "1 ≤ n ≤ X" matches Erdős's "positive integers n". Without the local condition part (ii) is false (below), so the
page's added hypothesis is necessary and OpenAI uses exactly it.

## 2. Prior and concurrent claims

**(a) Carella, arXiv:2310.16952, "Squarefree Values Of Polynomials"** — v1 only, 25 Oct 2023, classified **math.GM** (General
Mathematics, not math.NT), unrefereed. Theorems 1.1–1.3 claim μ²-asymptotics with error O(x^{1/2+ε}) for n⁴+1, n⁴+2 and
T⁴−2T²+2 by an elementary "exact expression" sieve over d ≤ ∞. OpenAI cites it accurately ("claims … for both n⁴+1 and n⁴+2
[Theorems 1.1–1.2]") and does not use it. **My checks** (`W_work/scripts/consts.py`, `consts2.py`): Thm 1.3's constant 0.963802
is wrong for both readings of its polynomial (true density 0.9006 for T⁴−2T²+2, 0.9745 for the displayed n⁴−n²+2; empirical
counts to 2·10⁴ agree with my Euler products, not with Carella); Thm 1.2's local-factor formula (5) is incoherent (its second
product runs over "p ≡ 3 mod 8, p = a²+b²", an empty set; and it gives 4 roots for every p ≡ 1 (8) although x⁴ ≡ −2 has 0 or 4
roots there); its numerics 0.757159 / 0.981003 are off the true 0.756687 / 0.980822 by 5·10⁻⁴ / 2·10⁻⁴ (my truncation error ≈ 10⁻⁵).
A power-saving error term from an elementary sieve is not plausible for the large-modulus range. No published refutation found
(arXiv, MathOverflow API, web search). Status for a page: **an unverified claim; not credited as a proof.**

**(b) Zapata Ceballos–Jalalvand, arXiv:2608.10335, "On the Squarefree Values of Degree-2q Polynomials"** — v1 11 Aug 2026;
**v2 15 Oct 2026 = WITHDRAWN**. arXiv comment: "The proof of Proposition 2.3 is incomplete. The argument does not provide the
estimate needed to control the contribution of square divisors arising from prime ideals of large norm. Consequently, the claimed
squarefreeness result is not established. The authors currently do not know how to complete the proof." The failure is exactly
the large-prime tail that OpenAI's Proposition 1.4 is about. OpenAI (dated 24 Sep, public 6 Oct) cites v1 as a claim it does not
use — correct at the time.
- *EXPOSITION / credit (paper):* OpenAI says the ZCJ class "includes n⁴+1". ZCJ v1 claimed more: Thm 1.1 (monic, degree 2q,
  field contains a Galois degree-q subfield, squarefree fixed divisor) and "As an immediate corollary, irreducible quartic monic
  integer polynomials whose Galois group is neither S4 nor A4 (Corollary 2.4), take infinitely many squarefree values" — this
  includes **x⁴+2** (Q(⁴√−2) ⊃ Q(√−2), Galois group D4). So a public claim covering n⁴+2 predates OpenAI's public release by
  8 weeks; it is now withdrawn. A page must say "withdrawn 15 Oct 2026", not "claimed".

**(c) The JNT link on the forum** (S0022314X24000635) = Browning–Shparlinski, "Square-free values of random polynomials",
J. Number Theory 261 (2024) 220–240, doi 10.1016/j.jnt.2024.02.013 (Crossref `alternative-id`). Averaged over coefficient boxes;
OpenAI cites it [Thms 1.1–1.2] and correctly says averaged statements do not give a fixed polynomial. The forum's second link is
Granville's abc paper (cited as [granville1998abc]; PDF is a scan, Theorem 1 not text-checked — not load-bearing).

**(d) Everything else found (2023–2026):**
- Booker–Browning, "Square-free values of reducible polynomials", Discrete Analysis 2016:8, arXiv:1511.00601. **Theorem 1.2**:
  for squarefree H with every irreducible factor of degree ≤ 3, Σ_{n≤x} μ²(H(n)) = x ∏_p(1−ρ(p²)/p²) + O(x/log x). This is the
  k = 2, factor-degree ≤ k+1 case of OpenAI's **Corollary 1.3**, by the same factorwise-tail mechanism. **Not cited** —
  credit gap (EXPOSITION). Its intro also confirms the 2016 state: "This fact has not yet been extended to a single irreducible
  quartic polynomial."
- Heath-Brown, QJM 64 (2013), arXiv:1103.2028, intro: "the most interesting open question then concerns quartic polynomials
  taking square-free values. We would therefore like to handle k = d − 2 for d = 4."
- Lapkova–Xiao, arXiv:1801.04481 (2018) and 2005.14655 / JNT 265 (2024): multivariable generalisations of Browning's k ≥ (3d+1)/4.
  Optional credit.
- Simhi, arXiv:2610.29911 (21 Oct 2026, yesterday), on random polynomials: "It is a deep open problem to prove that E_P(x) = o(x)
  holds for any 'admissible' P … known for all deg P ≤ 3 by Hooley" — does not cite OpenAI. **Zero third-party uptake so far.**
- Kowalski–Vaughan 2309.10189 / Zarhin 2410.09357 (multivariable boxes), Sofos 2601.19319 (averages, cited), Wang–Yi 2504.00804
  (PNT over k-free values, uses known ranges) — none bears on fixed quartics.
- GitHub: `gh search code QuarticPowerFree` / `OAI.NumberTheory.PowerFree` → only openai/math itself. **No third-party Lean replay
  or rebuild of the PowerFree formalization found.** openai/math has 2 issues/PRs total, none on this paper; PR conversations were
  locked 12 Oct (commit 2710f99). No MathOverflow post. Aggregators (plasma-ai/erdos wiki, conjectures.io) record it — below.

**DeepMind counterexample (31 Mar 2026, Firsching):** f = x⁶+33x⁵+21x⁴+63x³+18x²+24x+48. My check (`dm_poly.py`):
irreducible over Q; f ≡ x(x−1)⋯(x−5) (mod 16) coefficientwise; fixed divisor gcd f(ℤ) = 16 = 2⁴; ρ_f(16) = 16, ρ_f(32) = 8.
With d = 6, k = d−2 = 4, ρ_f(2⁴) = 2⁴ **violates OpenAI's admissibility hypothesis (1.1)** — consistent, excluded. (It satisfies
FC's `allow_fixed_divisors` hypothesis "no fixed p^{k−1}" since ρ_f(32) < 32.) Note degree 6 = 4+2 has binary digit sum 2, which is
exactly when v₂(d!) ≥ d−2 permits a 2-adic obstruction at exponent d−2; the page's k ≠ 2^l does not exclude it.

## 3. The cited theorems — do they say what is used?

- **Xiao [27] Theorem 9.1 / Section 9** (arXiv:1505.05587v2, final accepted, = IMRN 2017): "Theorem 9.1. (Browning, 2011) Let
  f(x) ∈ Z[x] be an irreducible polynomial of degree d ≥ 3. Suppose that k ≥ (3d+1)/4. Then, we have #{n ∈ Z ∩ [1,B] : f(n) is
  k-free} ∼ c_{f,k} B", with c_{f,k} = ∏_p(1−ρ_g(p^k)/p^k) (eq. 1.5). Input interval [1,B] and full Euler product — **as the paper
  says**. No primitivity/sign hypothesis (the paper's normalisation is conservative). For Cor 1.3 the paper uses "E_B(B^{1−δ}) =
  o_g(B)" with E_B(ξ) = #{n ≤ B : b^k | g(n) for some squarefree b > ξ}: Xiao defines exactly "E(ξ) = #{x ∈ Z ∩ [1,B] : ∃ b > ξ
  s.t. b^k | f(x) and μ²(b) = 1}", writes (9.2) N = cB + o(B) + O(E(B^{1−δ})), and the proof of Thm 9.1 is the bound on
  E(B^{1−δ}). I re-did the exponent check: Φ(β) = ((d−k)/d)^{1/2}((d−kβ)/(d−k)+β) is decreasing in β when 2k > d, Φ(1) =
  2((d−k)/d)^{1/2} < 1 ⟺ k/d > 3/4, and the curve contribution (½Φ + ⅓) < 1 follows. **Holds.** EXPOSITION only: the E-bound is
  inside a proof, not a displayed statement.
- **Browning 2011 (Arch. Math. 96, 139–150)**: full text **COULD NOT be fetched** (Springer bot wall from exe.dev and Hetzner; not on
  arXiv; Semantic Scholar's OA link wrongly points to Heath-Brown's 1103.2028). Its content (k ≥ (3d+1)/4, asymptotic) is attested
  independently by Xiao (Thm 9.1, "we state Browning's theorem again"), Heath-Brown 2013 intro, and Reuss 2015 intro. The paper
  deliberately leans on Xiao's form, which I verified.
- **Heath-Brown 2006 [11, Theorem 16], range (3d+2)/4**: LNM chapter not fetchable; Heath-Brown himself (1103.2028, ref [4] =
  LNM 1891): "The author [4, Theorem 16] … demonstrated that the asymptotic formula remained valid for k ≥ (3d+2)/4, so that one
  may take k = d−2 providing only that d ≥ 10." **Holds.**
- **Nair 1976, (√2 − ½)d**; reaches d−2 at d ≥ 24 (0.0858 d ≥ 2): attested by Heath-Brown 2013 and Xiao. **Holds.**
- **Hooley 1967** (k = d−1 asymptotic): attested by Heath-Brown 2013, Reuss, Xiao, Booker–Browning. **Holds.**
- **Heath-Brown 2013 [Theorem 1]**: "Let f(X) = X^d + c ∈ Z[X] be irreducible, and suppose k ≥ (5d+3)/9. Then … N_{f,k}(x) =
  C(f,k)x + O(x^{1−δ(d)})" and "this will allow k = d−2 as soon as d ≥ 6". Paper's description **holds**. Consequence for novelty:
  irreducible binomials x^d+c of degree 6, 7, 8 were already done at k = d−2 (with power saving).
- **Reuss 2015** (arXiv:1307.2802v1; published BLMS numbering not checked): Theorem 2 = power saving at k = d−1 ✓. Lemma 3 reduces
  to N(X;A,B) = #{(n,a,b) ∈ ℕ³ : n ∼ X, a ∼ A, b ∼ B, μ²(a) = 1, a^{d−1}b = f(n)} with A,B ∈ [X^{1−δ}, X^{1+δ}] (B ≪ X^{1−δ}
  disposed of inside the proof via HB Thm 15), and Section 6 gives N(X;A,B) ≪ M^{1−1/d}X^{1−1/d+ε} ≪ X^{1−η}. So "o_g(X) triples with
  X < n ≤ 2X, a > X^{1−δ}, μ²(a) = 1, a^{d−1}b = g(n)" (Cor 1.3, d = k+1) is what Lemma 3 + its proof + §6 give, after summing
  O(log² X) dyadic boxes. **GAP (minor, fillable):** Reuss's §§2–3 work in Z[θ] with f(θ) = 0 and factor the ideal ⟨n+θ⟩ —
  i.e. they treat θ as integral (monic f; also a sign slip n+θ vs n−θ). Cor 1.3 applies this to a primitive, possibly non-monic
  g without the standard reduction (G(y) = c^{d−1}g(y/c) monic, y = cn in a fixed residue class). Reuss's *statement* is for
  general irreducible f, so the citation is defensible; Hooley 1967 would also do. Does not touch Thm 1.1, Cor 1.2 or #978.

## 4. The status record

- **Formal Conjectures** (`978.lean`; history via GitHub API): `parts.ii` and `parts.iii` flipped from `research open` to
  `research solved` with `formal_proof using lean4 at …/adc7f124…/Main.lean#L144` by **PR #6898** (author and merger Moritz
  Firsching / mo271; opened 2026-10-07, merged 2026-10-11, commit 3dfd999), titled "mark problems solved in the OpenAI math
  release". Line 144 at adc7f124 is `theorem allDegrees` (checked); the Lean and paper are byte-identical adc7f124 → HEAD 1581d4c.
  The PR's stated checks: FC build, "every proof link resolves to a theorem … (source inspection)", "no sorry (grep)", comparator
  axiom config — **no kernel replay of OpenAI's proof is claimed**; FC bodies remain `sorry`, so the density ⇒ `.Infinite` and
  `Irreducible` over ℤ[X] ⇒ over ℚ transports are not in any linked proof (they are routine and go the right way). Later
  cosmetic commits 75a6d3d and 7db2ea3 (14 Oct). FC `parts.ii` keeps `k ≠ 2^l` and `0 < leadingCoeff` (so it is weaker than what
  OpenAI proves). Earlier: PR #3670 (31 Mar → 27 Apr 2026) DeepMind solution, restated as `variants.allow_fixed_divisors`; PR #5487
  (10 Sep) fixed `sub_two`'s divisor hypothesis. Open bot issue **#7135** (11 Oct): "status mismatch (repo=formally solved,
  erdosproblems.com=open)".
- **teorth/erdosproblems** `data/problems.yaml` (fetched today, file last auto-updated 2026-10-22): 978 `status: open`,
  `last_update: 2025-08-31`. None of the OpenAI-release problems (3, 138, 184, 371, 431, 952, 968, 970, 1150) has been updated.
- **erdosproblems.com/978**: last edited 31 Mar 2026; the page, LaTeX source, claims tab and thread contain **no mention of
  OpenAI** (grep, 0 hits); "Proof claims (0)"; "The ability to post new comments has been suspended."
- **Aggregators:** conjectures.io closed both targets on 2026-10-06 23:17 UTC on the owner's instruction "Assume the proofs are
  valid and close them", stating "No independent proof replay, exact-target bridge, Lean rebuild, or certification was performed".
  plasma-ai/erdos wiki marks 978 "solved" (Hooley + OpenAI); its ZCJ page is not yet updated for the withdrawal.
- **Dates:** manuscript says "September 24, 2026" (internal); first public commit adc7f124 = **2026-10-06 21:58:50 UTC**.

## 5. What is new, and what a page must credit

**New (if the proof is right):**
1. Theorem 1.1: the (d−2)-power-free Euler-product density for every irreducible f of degree **4–8**. Entirely new for d = 4 and
   d = 5; for d = 6, 7, 8 new except for binomials x^d + c (Heath-Brown 2013, with power saving).
2. In particular the **first unconditional result for any single irreducible quartic** (every one with no fixed square divisor;
   n⁴+2 and n⁴+1 included). The only competing claims are Carella 2023 (unrefereed, numerically wrong constants) and ZCJ 2026
   (withdrawn by its authors on 15 Oct 2026 at exactly the large-prime-ideal step).
3. Proposition 1.4: a power-saving large-prime tail X^{1−δ} for d = 4…8 (density itself stated without rate). The method is
   Reuss's number-field factorisation + approximate determinant framework, extended (adaptive auxiliary primes, quartic
   surface/curve geometry, exact parameter certificate).
4. Corollary 1.3 for factor degrees up to k+2 (k = 2 with factors ≤ 3 is Booker–Browning 2016).
5. The Lean formalization proves the whole k = d−2 statement for all d ≥ 4 **without Browning**: `density_ge_four` dispatches d ≥ 5
   to `density_ge_five` (MediumDegree.lean; d ≥ 9 via `density_ge_nine`, HighDegree.lean) and quartics to `quartic_dyadic_tail`
   (power saving δ = 3/1000). The paper and the Lean take different routes for d ≥ 9 — relevant to the coordinator's replay.

**Not new:** Corollary 1.2 for d ≥ 9 (Browning 2011; Heath-Brown 2006 for d ≥ 10; Nair 1976 for d ≥ 24) apart from the sign/content
normalisation (Lemma 2.3); part (i) of #978 (Hooley 1967).

**A page must credit:** Erdős [Er53 p. 425], [Er65b §6 p. 219], [Er81h p. 178] (the paper omits Er81h); Hooley 1967; Nair 1976;
Heath-Brown 2006 Thm 16; Browning 2011 (Xiao 2017 Thm 9.1 reproof); Heath-Brown 2013 (binomials); Reuss 2015 (the framework the
proof follows); Heath-Brown 2012 (n²+1); Bombieri–Pila / Heath-Brown / Salberger (determinant method); Granville 1998 (abc,
conditional); Booker–Browning 2016 (products, uncited by the paper); Firsching / DeepMind (31 Mar 2026) and Bloom's restatement for
the necessity of the local condition; Carella 2023 as an unverified claim and Zapata Ceballos–Jalalvand 2026 as **withdrawn**.
It must also say the result is an OpenAI-model preprint, unrefereed, first public 6 Oct 2026, with no independent replay of its
Lean proof reported anywhere as of today.

## Objection list (classified)

| # | Where | Class |
|---|---|---|
| W1 | §1 Introduction, ZCJ sentence: "this includes n⁴+1" — ZCJ Cor 2.4 claimed every monic quartic with Galois group ≠ S4, A4, incl. x⁴+2; and ZCJ is now withdrawn | EXPOSITION (credit/accuracy) |
| W2 | Cor 1.3 — Booker–Browning 2016 Thm 1.2 (k = 2, factors ≤ 3) not cited | EXPOSITION (credit) |
| W3 | Proof of Cor 1.3, case d = k+1: "the unweighted triple estimates of Reuss [Lemma 3 and its proof, and Section 6] give o_g(X) triples …" — Reuss's §§2–3 are written for integral θ (monic); reduction for primitive non-monic g unstated | GAP (fillable by the monic substitution or by Hooley 1967); does not affect Thm 1.1 / Cor 1.2 / #978 |
| W4 | "Xiao's estimate in [Section 9] is E_B(B^{1−δ}) = o_g(B)" — correct, but lives inside the proof of Thm 9.1 | EXPOSITION |
| W5 | §1 history omits Er81h p. 178; "Erdős proved infinitude for exponent d−1" omits his 2-power exception (harmless under admissibility) | EXPOSITION |
| W6 | Page/FC (not the paper): preamble k ≠ 2^l excludes quartics from part (ii); FC parts.ii inherits it | Record defect, not the paper's |
| W7 | Browning 2011 primary text not obtainable here; Granville Thm 1 not text-checked (scan) | COULD NOT CHECK (secondary attestation adequate; not load-bearing) |

VERDICT: GAP AT Cor 1.3, case d = k+1 (Reuss citation used for non-monic g without the monic reduction — minor, fillable, does not touch Thm 1.1, Cor 1.2 or Erdős #978); Erdős sourcing, the d ≥ 9 citation (Xiao Thm 9.1), the Heath-Brown/Nair/Hooley ranges and the priority claim HOLD AS READ; Browning 2011 primary text COULD NOT be fetched.
