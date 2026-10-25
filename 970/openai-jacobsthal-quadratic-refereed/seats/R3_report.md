# R3 report — §10 (stops), §11 (assembly), Appendix A, Appendix B + Lean comparator statements

STATUS: COMPLETE (first full version 2026-10-23; numerics in /tmp/oaimath/021/seats/R3_work/)

## 1. VERDICT for this scope

**HOLDS AS READ** for §10, §11, App. A and App. B, *conditional on* the inputs from other scopes that these sections
cite (Prop 6.3 reference margin (11.1); Prop 5.3 coupling; Prop 5.5 (i)–(iii) occupation/compact-history/tail;
Lemma 5.2 high states; Lemma 4.8 marked visits; Lemma 6.5 local reference; Prop 7.2 regular boxes; Lemma 7.1 witness;
Prop 8.2 inverse; Cor 9.3 hard endpoints; Lemmas 2.1–2.3). I checked that each cited statement, *as stated*, gives what
§10/§11 take from it, and that §10/§11 use them inside their stated ranges and in a consistent order of constants.
No FATAL, no GAP, no FIXABLE objection found. Six EXPOSITION remarks below.

The deduction Thm 1.2 ⇒ Thm 1.1 (§11.2, pp. 72–73) is correct, including arbitrary prime sets, primes ≤ z not dividing n,
arbitrary translations, q > Y, and the bounded range of k. The Lean comparator statements are faithful to Thm 1.1 (and to
the weaker k² form) — see §6.

Note: the brief's "Theorem A.1" is printed as **Lemma A.1** (Completion with a unit residue restriction), p. 74.

## 2. Objections

None at FATAL / GAP / FIXABLE level. EXPOSITION only:

E1 (§11.2, eq. (11.10), p. 73). "For each fixed $A_0$, (11.8) gives $\frac{k(1+X/\log X)}{Y\log w/L^2}=\frac1{A_0}+o(1)$."
Correct, but the o(1) decays only like ≈2 log M/M (it comes from log w = log L − 2 log log L ~ M). Numerically (script
deduction_sweep.py): R(k)·A0/e^γ, where R = k(1+X/log X)/(YV0/B²), is 2.49 at log k = 10³, 1.37 at 10¹⁰, 1.20 at 10²⁰,
1.02 at 10³⁰⁰. With the paper's choice A0 = 2C1/c0 (i.e. A0 = 2e^γ·ρ, ρ = C1/c in YV0/B² units) the needed inequality
ρR < 1 holds for all log k > 9.5·10³; with A0 = 1.5e^γρ only for log k > 2.4·10⁷; with A0 = 1.05e^γρ only for
log k > 10⁹⁹ — essentially independent of ρ (ρ = 1, 10, 10³ tried). Harmless (constants are not effective, the bounded range is closed by m_k = (k+1)2^k+1),
but worth one sentence. Also worth stating: Y = A0²k²ℓ²/(M²L²) < A0²k²/M² exactly (L > ℓ), so h(k) ≤ A0²k²/M² needs no o(1).

E2 (§11.2, eq. (11.9), p. 73). The deletion constant is named $C_1$, the same letter as the absolute constant of
Lemma 2.3, eq. (2.6). They are different constants. Rename.

E3 (Lemma 10.4, eq. (10.10), p. 63). "$\ge e^{-\gamma}(.94-o(1))$" — true as P→∞, but the approach is from below and slow.
Exact computation for E = all primes < P (the worst case I found; 2 ∈ E forces 2 | d0): S(P) = .4932, .5016, .5070,
.5108, .5136 for P = 10⁴…10⁸; deficit from the limit e^{−γ}·.95 = .5334 is ≈ 0.364/log P (deficit·log P = .370, .366, .365, .364, .364),
so S(P) ≥ .94e^{−γ} = .5278 only once log P ≳ 65. Other E (odd primes, empty, {2}, big half, small primes) are already above
the line at P = 10⁴. Harmless because P = w^b ≥ w^{b0−1} → ∞; the Markov step's constant (≈100·Σ log t/(t−1)² ≈ 120)
is what makes the o(1) slow.

E4 (Prop 10.5 proof, p. 67). "Since the $J_p$'s vary by at most $1+\xi$ within the whole bin, for $\xi\le1$ we have
$\sum_{p\notin\mathcal G}T_p\le 2C_U\eta V_{\rm all}(P)\sum J_p$" — correct (complement ≤ η·#bin, max J ≤ (1+ξ) min J),
but the argument uses #-fraction ≤ η and should say so; as written it reads as if it used a J-weighted fraction.

E5 (Prop 10.6 proof, "Identifying the tag", p. 68). The step "the fraction of its harmonic measure with all those
alignments is at most $(1-\eta/(1+\xi))^{c_7\log w}$" is legitimate because "every search prime aligns to A/D" is a
*product* event in the full-box measure and the hard endpoints are a subset of it (the paper says so: "without asserting
independence after conditioning on hardness"). A reader would be helped by stating explicitly that the exceptional set is
indexed by (box, candidate, list rational) and is a property of the box's bins, not of the path — that is what makes the
union over ≤ H_e·F rationals per box and the sum against C_K^box/B² valid.

E6 (typesetting, whole paper incl. pp. 64, 67, 68, 71–72). Every `\cref` to a lemma/proposition/corollary prints as
"Theorem N.M" because the environments share the theorem counter without cleveref being told their names — e.g. p. 64
"Hence Theorem 10.4 and (10.13) give" (it is Lemma 10.4), "Theorem 7.2" ×9 (Proposition 7.2), "Theorem 10.3" (Lemma 10.3),
"Theorem 9.1" (a lemma). In my scope the printed text therefore cites non-existent theorems; locators in this report use
the environment's real name. Fix: `\crefname{lemma}{Lemma}{Lemmas}` etc., or aliascnt.

## 3. What I checked and how

Read line by line (TeX source): §10 in full — Def 10.1 (+ owner uniqueness via (10.2)), Def 10.2, the right-endpoint
admission remark, (10.5); Lemma 10.3 (subbins, common interval (10.12)-(10.13), factorisation m = ±d0ℓ', sign pieces and
short-interval PNT, the lift classes mod Q = D·rad D with proportion 1/D, the p-sieve with g(t)=1/(t−1), Siegel–Walfisz
remainder ratio, assembly of .94/2.22·.95 > .402 ⇒ .39, upper bound C_U); Lemma 10.4 (V/U coupling, E(V−U)=1/(t−1)²,
Markov, t=2 case); Prop 10.5 (group partition, invariance of stop status under replacement within the aligning subset —
earlier prefixes, tag position, all-prefix alignment, representative tests, admission via r ≥ r^rep and x ≤ x^rep with H
increasing, multiplicity one; hypothetical p satisfy (10.6); Lemma 6.5 ⇒ (10.20); .39−.05=.34 > .33); Prop 10.6 (tag
identification in full-box product measure, wrong-tag overlap via (10.2), marked visit via Lemma 4.8 + Prop 5.3 + Prop
5.5(ii) + Lemma 5.2, visit precedes compact endpoint since gap > 6b0 > K, verification of (i)–(iii) of Def 10.2 from Prop
7.2 (i),(ii),(v) and slack 2.09–2.13 ⊂ 2.06–2.16). §11.1 (error budget: K, ε, C_K, β, then K*, H_e, ϑ/C_len, C'_K, σ, F,
variance ⇒ C_s, η, b0, b1/b0, ξ, z — checked against the order required by Props 7.2, 10.5, 10.6, Cor 9.3; checked the
sign bookkeeping against identity (3.7) and Lemma 3.1; 5/8·c_L ≥ c_L/2). §11.2 (full deduction, incl. inclusion–exclusion
for bounded k: m∏(1−1/p) − 2^r ≥ m/(k+1) − 2^k > 0 at m_k). Also read for interface: §3 entire; statements of Lemmas
2.1–2.3, 4.8 (and its renewal proof), 5.2, 5.3, 5.5, 6.5, Prop 7.2, Cor 9.3; the two places Lemma A.1 / Brun–Titchmarsh are
used in §9 (p. 59–60), the large-sieve use in §8 (p. 48) and the Bézout use (p. 44), the Buchstab-limit use in §4.

Appendix A: Lemma A.1 read in full — (c,N)=1, reduction p = lv, Fourier identity (A.12) normalisation, restricted
Kloosterman sum via orthogonality mod T0, gcd bound (h+jH,N) ≤ T0(h,N), S(0,0)=φ(N)/φ(T0), φ(N)=T0φ(H), the four
frequency cases, the gcd-weighted sum ≤ τ(N)log 2N, and the application range (R^{4/5}<N≤R^{1+o(1)}, Y2≤3N ⇒ R^{3/5+o(1)}).
Use in §9 checked: H ∈ (R^{4/5}, R𝒵^{11}], block length X ≪ R, Y2 ≤ 3H, unit right side, l ≤ R^{1/10} squarefree coprime
to HT1, (T1,HT0)=1 by Remark A.2; error sum over l is R^{4/5+o(1)}. Within range.

Appendix B: B.1 (M_n ≤ 1/n!, Laplace transform ODE, Euler integral via (1−s/n)^n), B.2 (arc argument, constant
δ^{-1} + 4πJ; separation Q^{-2}; the §8 use has separation ((1+ξ)U)^{-2} — within range), B.3 (Sylvester degree count
Σ(m+i)+Σ(n+j)−Σk = mn; coordinate changes; coprimality remarks incl. inflection polynomial degree ≤ 3d−4), B.4 (progression
coordinates, τ(l)^{C1} ≤ τ_k(l), Mertens with q/φ(q)); its §9 use has H/q ≥ R^{1/5−o(1)} ≥ J0. All used within range.

Numerics (all with ulimit -v 8 GB, nice 19; scripts + outputs in R3_work/):
- deduction_sweep.py: cancellation-free evaluation (log R = −δ − log log X + 2 log B − log V0, δ = log A0 + log ℓ − e log M;
  exact V0 up to w ≤ 2·10⁶, Mertens beyond) of R(k), of the paper's form (11.10), of Y·M²/(A0²k²) (→1 from below:
  .56 at 10⁵ … .993 at 10³⁰⁰), and thresholds (E1). CONTROLS that must fail and do: z = A0 k ℓ/M^{1.5} and /M² ⇒ R·A0/e^γ
  grows (5.9→26.8, 20→704 over log k = 10⁵…10³⁰⁰); z = A0 k ℓ (no /M) ⇒ R → 0 like 1/M, i.e. the /log log k in z is
  exactly the trade that buys the (log log k)^{-2}. (A first version of the script had a cancellation bug — log ℓ − M
  instead of log ℓ − log M — which produced nonsense; caught by hand-computing one point, fixed, re-run.)
- checks_10_A_B.py: §10 constants (f(2.18)=.27045 < .29697 bound < .30; H6−log6 = .658 < .66; e^{.66}=1.935 < 1.95;
  log 1.18 = .16551 ≤ cubic .16574 < .166; .94/2.22 = .42342; ×.95 = .40225 > .402; f increasing on [2,4]); Lemma 10.4
  exact sums for 7 choices of E at P = 10⁴, 10⁵ with CONTROL exponent .5 (falls to .24–.25 < target, as it must);
  Lemma A.1 brute force on 60 random toy instances (H ∈ {6,…,36}, T0 | rad H, T1 ∈ {1,7,11,13,77}, l coprime, random
  real intervals): max |C_l − main| / (τ²log²√(NT0)(1+X/lN+Y2/N)) = .0011; large instance rel. err −4.6·10⁻⁴; CONTROL
  (main term without 1/φ(T0)) off by a factor up to 6.9 — fails as it must; Lemma B.1 by integrating the delay equation:
  ω(4..12) = .561458–.561460 vs e^{−γ} = .561459; CONTROL 1.01·e^{−γ} differs by 5.6·10⁻³.
- lemma104_large.py: S(P) for E = all primes, P = 10⁴…10⁸ (E3).

## 4. What I could NOT check (outside scope, used as black boxes)

- Prop 6.3 (the margin c_L/B² in (11.1)); Lemma 6.5's proof (P_e/V(b) = f(r/b)+O(1/b)+o(1) on [b0,b1]) — §10's
  .33 bound (10.20) rests entirely on it.
- Prop 5.5(ii)/(iii) and Prop 5.3 proofs (compact-history transfer C_K·P(𝒜), tail, coupling with N h → 0) — §10.6's
  missing-visit bound and §11's (11.2), (11.3) rest on them. I checked only that the marked-visit event is an event of the
  same tilted chain (Remark 4.7, p. 22, confirms) and that the visit lies within N* = O((log B)³) steps.
- Lemma 4.8 relies on Lemma 4.3 (regeneration: iid cycles, E G < ∞, tight initial segment) — not checked.
- Prop 7.2, Prop 8.2, Cor 9.3 proofs — in particular that C_s, F, C_K^box are independent of small fixed ξ (asserted
  there; §10/§11 use exactly that and nothing more).
- Lemma 2.1 (fundamental lemma, cited to Sofos 2023 Lemma 2.8) and Lemma 2.2 (iv) (short-interval PNT) — sources not read.
- Weil/Kloosterman bound for composite moduli (cited to Lichtman 2022 Lemma 7.1) — standard (Iwaniec–Kowalski Cor. 11.12
  form), not re-derived.

## 5. Where a hole is most likely to hide in this scope

Prop 10.5's group argument (p. 67): the comparison only works if, after fixing all primes but the tag prime, *every*
prime of the owner-aligning subset 𝒢 yields a stop with the same labels and tag position, so that the averaged lower bound
(10.7) over the whole bin can be cut down to 𝒢 at cost 2C_Uη. If any stop condition depended on the actual tag prime
beyond its alignment (e.g. admission tested on actual gaps near threshold, or a "first stop" earlier on the branch that
appears for some replacements), the group would be a proper, prime-dependent subset of 𝒢 and the averaging would fail —
the classes a_p are arbitrary, so only the *full* aligned subset is guaranteed to carry the average. I checked each
condition: tag position (earlier primes fixed), all-prefix alignment (replacement aligns), length/representative
safety/window (labels only), admission (representative safety with actual gap ≥ representative gap and H increasing — this
needs no Δ at all), ordering/distinctness (tag-bin multiplicity one), earlier stops (same truth values). It holds. The
second candidate, Prop 10.6's tag identification, is safe because it bounds a product event in full-box measure rather
than conditioning on hardness.

## 6. Lean comparator statements (Jacobsthal.lean, JacobsthalImproved.lean — only these two files read)

`IsJacobsthalBound k m := ∀ n : ℕ, 0 < n → n.primeFactors.card ≤ k → ∀ a : ℤ, ∃ i : ℕ, i < m ∧ (a + i).natAbs.Coprime n`
says: every block {a, a+1, …, a+m−1} of m consecutive integers, at an arbitrary integer start a (negative allowed),
contains an integer coprime to n, for every n ≥ 1 with ω(n) = #primeFactors(n) ≤ k. That is exactly j(n) ≤ m for all such
n, i.e. h(k) ≤ m with the paper's h(k) = sup_{n≥1, ω(n)≤k} j(n); the convention gcd(0,n) = n (Nat.Coprime 0 n ↔ n = 1)
agrees with the usual one, and ω(1) = 0 matches `primeFactors 1 = ∅`. `JacobsthalIteratedLog := ∃ C > 0, ∀ k > 0, ∃ m,
IsJacobsthalBound k m ∧ m ≤ C·k²/(log log(3k))²` is Theorem 1.1 verbatim (k ≥ 1; for k ≥ 1, log(3k) ≥ log 3 > 1 so
log log(3k) > 0 and no division-by-zero/negative-log artefact arises; at k = 1 the denominator is (0.094)² ≈ 0.0088, which
only makes the bound weaker). `JacobsthalQuadratic` is the same with C·k², i.e. Jacobsthal's h(k) ≪ k². Both statements
say exactly what the paper claims; the ∃ m form is equivalent to a bound on h(k) since IsJacobsthalBound is monotone in m.
