# Referee report — seat `setup` — 02-setup.tex (§2 "The cyclic model and its coordinate meshes", printed pp. 3–6)

Paper: OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026), sha256 042acea3…
Source read: `build/sections/02-setup.tex` (264 lines, read in full, every line), plus every downstream use of a §2 label
(03-counting l.86–96, 165–196; 05-dichotomy l.59–80, 113–136, 196–293; 06-perturbation l.13–60, 171–180, 282–285; 07 l.65) to
check that the §2 statements carry the hypotheses their users need. Lean consulted as text only (no lean/lake run).

Printed numbering (from the PDF, pdftotext per page): (2.1)=`setup:parameters` p.3; (2.2)=`setup:dilation-definition`;
Lemma 2.1=`setup:dilation` p.4 (eq. (2.3)=`setup:denominator`); Lemma 2.2=`setup:prime` p.4; (2.4)=`setup:q-bounds` p.4;
(2.5)=`setup:mesh-parameters`; (2.6)=`setup:orders`; (2.7)=`setup:cyclic`; (2.8)=`setup:coordinates`; (2.9)=`setup:cut-distance`;
(2.10)=`mesh:definition`, (2.11)=`mesh:intervals` p.5; (2.12)=`setup:labels`; Lemma 2.3=`mesh:width` p.5 ((2.13)=`mesh:width-bounds`);
Lemma 2.4=`mesh:neighbors` p.6; (2.14)=`mesh:truncation-definition`; Lemma 2.5=`mesh:truncated` p.6.

## Verdict for this scope

**HOLDS AS READ.** Every statement in 02-setup.tex is correct, every proof step checks line by line, every "for large k"
assumption made inside §2 holds from an explicit small threshold (all ≤ 7), none depends on r, and each lemma supplies
exactly the hypothesis its downstream users invoke. No FATAL, no GAP. Nine objections, all COSMETIC (one is a typesetting
defect that misnames every cross-referenced lemma in the compiled PDF). The constants 49, 16004D, 1/4, 2 are valid upper/lower
bounds with real slack (measured true values: 4, ≈4000D+1, ≈1, ≈1), so nothing in §2 is tight and nothing in §2 caps c.

## Line-by-line status

| Item (TeX label / printed) | Status |
|---|---|
| §2 preamble l.3–10 (natural logs; absolute O-constants; "no threshold … depends on … r") | VERIFIED LINE BY LINE — no r anywhere in §2 |
| (2.1) `setup:parameters` + l.21 "k large enough that h_0<2M<k" | VERIFIED; exact threshold: holds iff k ≥ 7 (exact integer check k ≤ 10^6 + tail) |
| (2.2) `setup:dilation-definition` | VERIFIED (Lean `dilation` uses `Nat.log p (2*M)` = same exponent) |
| Lemma 2.1 `setup:dilation` incl. (2.3), t = 0, "s is 1 or > h_0" | VERIFIED LINE BY LINE + exhaustive finite check (all 1≤h≤2M, all t mod h, 9 values of k up to 10^6) + failing control |
| Lemma 2.2 `setup:prime` (v_ℓ bound, 4^n/(2n+1), log comparison) | VERIFIED LINE BY LINE; comparison holds exactly for every k ≥ 3, fails at k=1,2 |
| q choice + (2.4) `setup:q-bounds` (both inequalities, both forms) | VERIFIED; checked for EVERY prime P∈(k,2k²], k ≤ 60 (20,099 pairs) + exact integer form + k to 10^40 |
| "q is a prime power, need not be prime"; does anything later need q prime | VERIFIED: no later step uses primality of q (uses enumerated below) |
| gcd(λ,q)=1 (l.90–92) | VERIFIED (needs h_0 < P; h_0 < k for k ≥ 5) |
| (2.5) `setup:mesh-parameters` | definitions; VERIFIED λH_x = H used in 05 l.75 |
| (2.6) `setup:orders` (four estimates) | VERIFIED each; "These follow directly" checked |
| G = ℤ/q^Dℤ, (2.7), "order at least P > k", distinct terms | VERIFIED |
| (2.8) `setup:coordinates` well-defined homomorphisms; representatives x̂∈[0,1)^D, ỹ∈[−1/2,1/2)^D | VERIFIED |
| (2.9) ρ: 0≤ρ≤1/2, 1-Lipschitz | VERIFIED |
| U-partition (exact; H_x^{-1} = k²λ integral) | VERIFIED |
| (2.10) `mesh:definition`, (2.11) `mesh:intervals`: partition of [−1/2,1/2); where 0 and the cut sit | VERIFIED + numerically (literal mesh, k=3..32) |
| (2.12) `setup:labels` | VERIFIED (definition) |
| Lemma 2.3 `mesh:width` (θ bounds, 1−e^{−θ}≥θ/2, e^θ−1≤2θ on [0,1], closure, \|V\|=O(k³log k)) | VERIFIED LINE BY LINE + numerically every cell k=3..32, windows to k=10^12, failing controls |
| Lemma 2.4 `mesh:neighbors` (the 49, the 1/16, Lipschitz step, (1−4H)r_0 ≥ r_0/2) | VERIFIED LINE BY LINE + numerically every cell k=3..32 and windows to 10^12, failing control |
| (2.14) `mesh:truncation-definition` (weak inequality at threshold) | VERIFIED |
| Lemma 2.5 `mesh:truncated` (16004D incl. threshold points and half-open convention) | VERIFIED LINE BY LINE + sliding-arc count k=3..32 + closed form to 10^12 |
| Downstream interfaces (03 count:local cases; 05 drift/path/short/long; 06 multiplicity) | SKIMMED for interface only (hypotheses of §2 lemmas vs. what is used) — all match |

## Line-by-line notes (what was checked, and how)

**Standing threshold (l.21).** D=⌈k^{1/10}⌉ is 2 on [2,1024], so h_0=4 there; 2M=2⌈√k⌉. Exact integer check over k=1..10^6:
"h_0<2M<k" fails exactly for k=1..6 and holds for every 7 ≤ k ≤ 10^6; for k ≥ 10^6, h_0 ≤ (k^{0.1}+1)² ≤ 4k^{0.2} < 2k^{0.5} ≤ 2M and
2M ≤ 2k^{0.5}+2 < k.

**Lemma 2.1 `setup:dilation`.** (a) Each factor ℓ^{⌊log(2M)/log ℓ⌋} ≤ ℓ^{log(2M)/log ℓ} = 2M; at most π(h_0) ≤ h_0 factors ⇒
λ ≤ (2M)^{h_0}. ✓ (b) ℓ^a | h ≤ 2M ⇒ a log ℓ ≤ log 2M ⇒ a ≤ ⌊·⌋ (a integer). ✓ (c) "h | λ whenever h ≤ h_0": every prime of h is
≤ h ≤ h_0 and h ≤ h_0 < 2M, so h is the product of its pairwise-coprime primary parts, each dividing λ — true, but the proof
never writes this sentence (Objection 3). (d) v_ℓ(gcd(h,λt)) ≥ v_ℓ(h) for ℓ ≤ h_0 (the ℓ-part of h divides λ hence λt, and divides
h) ⇒ s has no prime ≤ h_0 ⇒ s = 1 or s ≥ (least prime > h_0) > h_0. ✓ t=0: gcd(h,0)=h, s=1 ✓; negative t fine. Exhaustive check
(all h ≤ 2M, all t mod h) at k ∈ {7,100,1024,1025,10^4,59049,59050,10^5,10^6}: zero violations. **Control**: λ_bad = lcm(1..h_0)
(the Fox–Hunter-style dilation without the full primary part up to 2M) FAILS the s-dichotomy, e.g. k=10^4: (h,t)=(16,1) gives s=2
(2,322 violations); k=10^6: (25,1) gives s=5 (117,266 violations). So the "full primary part" choice is genuinely needed and is
what the lemma uses.

**Lemma 2.2 `setup:prime`.** Legendre: v_ℓ(C(2n,n)) = Σ_a(⌊2n/ℓ^a⌋−2⌊n/ℓ^a⌋), each summand ∈ {0,1} (⌊2x⌋−2⌊x⌋ ∈ {0,1}), zero once
ℓ^a > 2n ⇒ ≤ ⌊log_ℓ 2n⌋ ⇒ ℓ^{v_ℓ} ≤ 2n. ✓ If all primes ≤ k: C(2n,n) ≤ (2n)^{π(k)} ≤ (2n)^k (π(k) ≤ k used silently). ✓
C(2n,n) ≥ 4^n/(2n+1). ✓ **Explicit threshold of the log comparison: k ≥ 3.** Exact integer test 4^{k²} > (2k²+1)(2k²)^k: false at
k=1 (0.288 vs 0.693 in logs), k=2 (3.348 vs 4.159), true for every 3 ≤ k ≤ 400; for k ≥ 400 the RHS log is ≤ (k+1)(log 3+2√k) <
2.07k^{3/2} < (log 4)k². The resulting P ∈ (k, 2k²] is confirmed by direct factorisation of C(2k²,k²) for k=3..12. **Control**: the
same comparison with n = k (instead of k²) fails for every k ≤ 400. (The Lean does not use this proof: `PrimeScale.exists_prime_above`
uses Mathlib's Bertrand, P ≤ 2k — Objection 2.)

**q and (2.4).** q = P^e, e ≥ 1 (P^0 = 1 < k^{ck/D} for k ≥ 2), minimality ⇒ P^{e−1} < k^{ck/D} ⇒ q < P·k^{ck/D} ≤ 2k²k^{ck/D}. ✓
Log form = D·(log of first form). ✓ Checked for every prime P ∈ (k, 2k²], 3 ≤ k ≤ 60 (20,099 pairs; min upper margin 0.0021 at
P = 2k²−1-type primes with e = 1, never negative), exactly in integers (q^{10^5 D} vs k^k) at k ∈ {3,10,30,100,400}, and in
60-digit logs at k = 10^4 … 10^40. **Control**: P' = nextprime(k³) > 2k² violates the upper bound at k = 10, 20, 30 — the bound really
rests on P ≤ 2k² from Lemma 2.2. Uniformity over P (used at 06 l.282–283) holds.

**q prime power, never needs to be prime — every later use checked:** (i) 02 l.109 "every nonzero element … has order at least P > k"
(needs only q a power of P > k); (ii) 05 l.204–210 w_i ∈ q^{−i}ℤ, |w_i| ≥ q^{−i} (any integer q ≥ 2); (iii) 06 l.44–60 "q^a ∣ z,
q ∤ u ⇒ u/q ≢ 0 mod 1" — the paper itself says "it does not require u to be a unit or q to be prime"; (iv) 06 l.47 "λ is a unit modulo
q^D" = gcd(λ,q)=1, needs only P > h_0; (v) 06 l.176–180, 225–230 and 07 l.65 use only log q and N = q^D ≥ k^{ck}. Nothing needs q prime.

**gcd(λ,q)=1.** Primes of λ are ≤ h_0; the only prime of q is P > k > h_0 (h_0 < k holds for k ≥ 5). ✓

**(2.6) `setup:orders`.** D ≤ k^{1/10}+1, M ≤ k^{1/2}+1; log λ ≤ h_0 log 2M ≤ (k^{1/10}+1)² log(2k^{1/2}+2) = O(k^{1/5}log k);
log q ≤ (ck/D)log k + log 2k² ≤ c k^{9/10} log k + log 2k² (D ≥ k^{1/10}). ✓ Measured: log q/(k^{0.9}log k) → 1.0·10^{-5} = c,
log λ/(k^{0.2}log k) = 0.31, 0.17, 0.13, 0.09, 0.05 at k = 10^4,10^6,10^9,10^12,10^20 (bounded, in fact o(1)).

**G, coordinates, ρ.** x_i(n+N) − x_i(n) = q^{D−i} ∈ ℤ for i ≤ D ⇒ well defined; additive ⇒ homomorphisms G → 𝕋; y_i = λx_i likewise.
Distinctness of the k terms: (j'−j)d = 0 with 0 < j'−j < k < P contradicts ord(d) ≥ P. ✓ ρ = dist(·,1/2) ∈ [0,1/2], 1-Lipschitz. ✓

**U.** H_x = H/λ = 1/(k²λ); intervals [aH_x,(a+1)H_x), 0 ≤ a < k²λ, tile [0,1) exactly; their lifts are exactly H_xℤ (this is what 03
l.168 "lattice of spacing H_x" and 05 l.135 use). ✓ Each U-cell is a half-open real interval of length ≤ H ≤ 2H inside [0,1) (what 05
l.113 and 05 l.66 need).

**V-mesh (2.10)–(2.11).** a_ℓ strictly increasing (α > 0, R/m > 0), a_0 = 0, a_m = α(e^R − 1) = α·1/(2α) = 1/2 exactly. Left family
tiles [−1/2, 0), right family tiles [0, 1/2); 2m nonempty cells. The point 0 lies in [1/2 − a_m, 1/2 − a_{m−1}) = [0, 1/2 − a_{m−1})
("the interval on its right") and the cut −1/2 lies in [−1/2, −1/2 + a_1) ("the interval beginning at −1/2"). ✓ No V-cell straddles
the cut in representative coordinates, so every full-label box is a product of half-open real intervals inside [0,1)^D × [−1/2,1/2)^D —
exactly the property used by 05 `dichotomy:path` l.113 (convexity) and by 05/06 when applying `dichotomy:affinity`. Numerically confirmed
on the literal mesh for k = 3..32 (partition, a_m = 1/2 to 10^{-25}, position of 0 and of the cut).

**Lemma 2.3 `mesh:width`.** α ≤ q^{−2} ≤ 1/9 and R ≥ 1 for every k ≥ 2 (R ≥ 1 ⇔ α ≤ 1/(2(e−1)) ≈ 0.291); k²R ≥ 1 gives
k²R ≤ m ≤ k²R+1 ≤ 2k²R ⇒ H/2 ≤ θ ≤ H. ✓ On a left cell ρ(Y) = Y + 1/2 ∈ [a_ℓ, a_{ℓ+1}] on the closure, on a right cell ρ = 1/2 − Y,
so ρ+α ∈ [αe^{ℓθ}, αe^{(ℓ+1)θ}] and |I| = αe^{ℓθ}(e^θ−1) ⇒ 1−e^{−θ} ≤ |I|/(ρ+α) ≤ e^θ−1. ✓ On [0,1]: e^θ−1 ≤ (e−1)θ ≤ 2θ (convexity),
1−e^{−θ} ≥ (1−1/e)θ ≥ θ/2 (concavity) ✓ (exact validity ranges: [0,1.2564] and [0,1.5936]; controls at θ = 1.3, 1.6 fail). θ ≤ H ≤ 1 ✓.
ρ+α ≤ 1/2 + 1/4 ⇒ ≤ 2H ✓. R = log(1+q^{D+1}/2) ≤ (D+1)log q (q^{D+1} ≥ 2) ≤ 2(ck log k + D log 2k²) = O(k log k) ⇒ 2m ≤ 2k²R+2 =
O(k³ log k) ✓ (measured 2m/(k³ log k) → 2.0·10^{-5}). Closure convention: Ī taken on the circle, so the cut-adjacent cells' closures
contain the cut with ρ = 0 — covered by the same formula. Numerically: every cell of the literal mesh for k = 3..32 at both closure
endpoints (ρ is affine on each closed cell, so endpoints suffice): ratio |I|/(H(ρ+α)) ∈ [0.931, 1.039] at k=3, [0.9995, 1.0005] at
k=32, vs the claimed [1/4, 2]; windows at the cut, threshold, zero and random places for k = 1025, 10^6, 10^9, 10^12: ratio = 1.000000
to 6 digits (θ/H = 1 − O(1/(k²R))). Controls: m' = ⌈kR⌉ (wrong growth) violates the upper bound everywhere (ratio ≈ k); a uniform mesh
violates both bounds.

**Lemma 2.4 `mesh:neighbors`.** Y ∈ N(I) ⇒ dist(Y,Y_0) ≤ dist(Y,Ī) + diam Ī ≤ 2w ✓; ρ(Y)+α ≥ r_0 − 2w (1-Lipschitz) ✓; w ≤ 2Hr_0 by
Lemma 2.3 at Y_0 ⇒ ≥ (1−4H)r_0 ✓ ≥ r_0/2 iff H ≤ 1/8 (k ≥ 3) ✓; lower width bound at a point of J̄ ∩ N(I): |J| ≥ (H/4)(r_0/2) =
Hr_0/8 ≥ w/16 (again w ≤ 2Hr_0) ✓. N(I) is a closed arc of length 3w ≤ 6H < 1 ✓; consecutive endpoints inside N(I) bound one whole cell
contained in N(I), hence of length ≥ w/16; b endpoints ⇒ (b−1)w/16 ≤ 3w ⇒ b ≤ 49 ✓. Numerically (literal mesh, every cell, k=3..32,
circular incl. wrap across the cut; windows to k = 10^12): max #endpoints in N(I) = 4, min |J|/w = 0.80 (k=3) → 0.998 (k=32) → 1.0.
The true maximum 4 is attained at the cell [0, 1/2−a_{m−1}) (and its mirror at the cut): its left neighbour has the SAME width w, so the
far endpoint sits exactly at distance w and is counted because N(I) is closed. Control: merging 64 consecutive cells of the paper's mesh
gives 286 endpoints in N(I) and min|J|/w = 0.00094 — the checker flags it.

**(2.14) and Lemma 2.5 `mesh:truncated`.** {ρ ≥ η} is a closed arc; its intersection with an arc of length ≤ 4H < 1 has ≤ 2 components ✓.
Successive endpoints e<e' inside one component bound one cell J ⊂ component; Lemma 2.3 at e (ρ(e) ≥ η) gives |J| ≥ Hη/4 ✓; per component
b_i ≤ 4L_i/(Hη) + 1, ΣL_i ≤ 4H ⇒ ≤ 16/η + 2 ✓; + 2 threshold points; inside {ρ<η} the output is constant ✓; 16/η = 16000D, total
16000D + 4 ≤ 16004D (D ≥ 1) ✓. Half-open convention: at a mesh endpoint V takes the cell starting there; at ρ = η the weak inequality gives
V. "need not equal either neighboring value" is accurate: on the right family, if a mesh endpoint coincides with 1/2−η, the value there is
the cell starting at that endpoint, its left side is the previous cell and its right side is *. Numerically: max breakpoints on a closed
4H-arc (all arcs starting at a breakpoint, k = 3..32) = 63 … 2,733 vs 32,008; closed form for the densest arc (starts at the threshold
point) at k = 10^6, 10^9, 10^12: 16,001 / 32,001 / 64,001 = 4000D + 1, i.e. exactly 1/4 of 16004D (the 1/4 is the slack in the lower
width constant).

**Downstream interface (SKIMMED).** 03 count:local stationary case: target = a + τ + ((z−z_0)/h)b with a ∈ I, |b| ≤ |I|, |z−z_0|/h < 1
⇒ target mod 1 ∈ N(I), real range length ≤ 3|I| < 1 — exactly Lemma 2.4's hypothesis. Rotating case: anchor cell ≤ 2H, |b| ≤ H ⇒ range
≤ 4H < 1 — exactly Lemma 2.5's. 05 short periods: |V(y)| ≤ 2H(ρ+α) with α ≤ q^{−D} ≤ |w_i| — uses Lemma 2.3 and α ≤ q^{−D} only (the
extra 1/q in α is unused, Objection 6). 05 longer periods: y_i(n_j) within (2M/k)L_* ≤ L_* of y_i(n_{j_*}) ∈ I_* ⇒ in N(I_*) ⇒ Lemma 2.4.
05 drift/affinity/06 multiplicity: label boxes have widths ≤ 2H (U: H_x ≤ H; V: Lemma 2.3). All hypotheses match.

## "For sufficiently large k" inequalities inside §2 (each with its explicit threshold; none involves r)

| Where | Inequality needed | Holds for |
|---|---|---|
| l.21 | h_0 < 2M < k | k ≥ 7 (exact, k ≤ 10^6; tail analytic) |
| Lemma 2.2 l.79 | k² log 4 − log(2k²+1) > k log(2k²) | k ≥ 3 (exact integer form) |
| l.91 | h_0 < k < P (⇒ gcd(λ,q)=1) | k ≥ 5 |
| Lemma 2.3 l.185 | α ≤ 1/4, R ≥ 1 (and k²R ≥ 1) | every k ≥ 2 (q ≥ 3) |
| Lemma 2.3 l.194 | θ ≤ 1 | every k (θ ≤ H ≤ 1) |
| Lemma 2.3 l.200 | q^{D+1} ≥ 2 (for R ≤ (D+1)log q) | every k |
| Lemma 2.4 l.221 | H ≤ 1/8 | k ≥ 3 |
| Lemma 2.4 l.226 | 3w ≤ 6H < 1 | k ≥ 3 |
| Lemma 2.5 l.260 | 16000D + 4 ≤ 16004D | D ≥ 1 |
| (used downstream with §2 objects) | 2kH < 1 (05 affinity); 2H(k+1) < 1 (05 l.226); 4H < 1 (03 l.182) | k ≥ 3 |

Finite in number, explicit, absolute. **Prove-too-much:** nothing in §2 constrains c (§2 works verbatim for any constant c > 0; log q =
O(k^{9/10} log k) and |V| = O(k³ log k) hold with c-dependent constants only). The cap on c lives in §6 (rich case: 2c − γ/80 < 0,
i.e. c < γ/160 = 6.25·10^{-5}); not in this seat's scope.

## Objections (numbered)

1. **COSMETIC (exposition, compiled PDF) — every cross-reference to a lemma is printed as "Theorem".** TeX: `These follow directly from
   \Cref{setup:parameters,setup:dilation,setup:q-bounds}.` (l.102) prints (p.4) as "These follow directly from Equations (2.1) and (2.4)
   and Theorem 2.1." — but 2.1 is Lemma 2.1. Likewise `By \Cref{mesh:width} and the Lipschitz property of $\rho$` (l.217) prints "By
   Theorem 2.3", and l.254 prints "by Theorem 2.3 applied at either endpoint". Outside §2 the same defect renders `mesh:neighbors` as
   "Theorem 2.4", `mesh:truncated` as "Theorem 2.5", `setup:prime` as "Theorem 2.2", `count:eligible` (a Definition) as "Theorem 3.3",
   `outer:coloring` (a Proposition) as "Theorem 4.2", `dichotomy:drift` (a Lemma) as "Theorem 5.2" (34 occurrences of "Theorem x.y" in
   the PDF text whose target is a Lemma, Definition or Proposition — x.y ∈ {2.1–2.5, 3.1–3.4, 4.1, 4.2, 5.1–5.3, 6.1, 6.2}; the only
   Theorems are 1.1, 5.5, 6.3, 7.2). A reader looking for "Theorem 2.3" finds only Lemma 2.3. Fix: cleveref
   `\crefname{lemma}{Lemma}{Lemmas}` etc. (shared counter misconfiguration).
2. **COSMETIC (proof/exposition) — `setup:prime` (Lemma 2.2, p.4).** "For all sufficiently large integers $k$" — the threshold is k ≥ 3
   (exact; fails at k = 1, 2). "its value would consequently be at most $(2n)^k$" silently uses π(k) ≤ k. The lemma is strictly weaker
   than Bertrand's postulate (which gives P ≤ 2k for k ≥ 1), and the Lean replaces this proof by Mathlib's Bertrand
   (`PrimeScale.lean` `exists_prime_above`, `Nat.exists_prime_lt_and_le_two_mul`): the human proof and the formal proof differ. Harmless.
3. **COSMETIC (exposition) — `setup:dilation` (Lemma 2.1, p.4).** Statement: "Consequently, $h\mid\lambda$ whenever $h\le h_0$". The
   proof ("Thus the full $\ell$-primary part of $h$ divides $\lambda$ … All prime divisors of $s$ therefore exceed $h_0$. This proves the
   assertions") never states the needed step (all primes of h are ≤ h ≤ h_0, h ≤ h_0 < 2M so the primary-part claim applies, and coprime
   primary parts multiply). One-line fix.
4. **COSMETIC (exposition) — (2.4) `setup:q-bounds`, p.4.** "Minimality gives $k^{ck/D}\le q\le2k^2 k^{ck/D}$": the upper bound needs
   q = P^e with e ≥ 1 (so that P^{e−1} exists and is < k^{ck/D}); true because k^{ck/D} > 1, unstated. (Lean records `exponent_pos`.)
5. **COSMETIC — Lemma 2.3 proof l.185–186.** "For large $k$ we have $\alpha\le1/4$ and $R\ge1$" — true for every k ≥ 2 (q ≥ 3); and
   "$k^2R+1\le2k^2R$" needs k²R ≥ 1 (true since R ≥ 1), unstated.
6. **COSMETIC — (2.5) α = q^{−(D+1)}.** The only use of α's size (05 `dichotomy:step-lattice`: "$|w_i|\ge q^{-i}\ge q^{-D}\ge\alpha$")
   needs α ≤ q^{−D}; the extra factor 1/q is unused (it only enlarges |V| by a factor (D+1)/D). No effect on correctness.
7. **COSMETIC — constants are loose (informational).** Lemma 2.4's "at most 49" has true maximum 4; Lemma 2.5's 16004D has true maximum
   4000D+1 (asymptotically, exactly 1/4 of the bound); Lemma 2.3's [1/4, 2] has true range 1 ± O(H). These are correct bounds; they feed
   only the (CDh)^{6D} constant C in 03, which is absolute either way.
8. **COSMETIC — (2.11) partition claim l.154.** "Since $a_0=0$ and $a_m=1/2$, these $2m$ intervals partition the representative interval"
   also needs a_ℓ strictly increasing (immediate from α > 0, R/m > 0), unstated.
9. **COSMETIC — Lemma 2.5 wording.** "Its value at a breakpoint is also determined, and need not equal either neighboring value." Every
   function's value is "determined"; the intended content (the output is a function of which open sub-arc or which breakpoint the point
   is at, so sign vectors against breakpoint lifts determine it) is what 03 l.193–196 uses. The "need not equal either neighbor" clause is
   correct (example in the notes above).

Hedge-word census for 02-setup.tex: "clearly / similarly / the same argument / it follows" — 0 occurrences; "These follow directly" — 1
(l.102), checked (all four estimates of (2.6) verified above); "Minimality gives" — 1 (l.85, Objection 4); "Consequently/consequently" — 2
(l.36 Lemma 2.1 statement, Objection 3; l.71 setup:prime, Objection 2 — π(k) ≤ k); "hence/therefore/Hence" — 5 (l.48, 49, 80, 190, 256),
each a one-step inference checked in the notes above.

## Citation table (scope: 02-setup.tex has one citation)

| Cited | Paper's claim (02-setup.tex l.29–30) | Source (arXiv 2606.02541v1, the current and only version; local copy refs/arxiv_2606.02541v1.txt) | Verdict |
|---|---|---|---|
| Fox–Hunter [foxHunter2026] | "Least-common-multiple dilations also occur in the cyclic constructions of Fox and Hunter~\cite{foxHunter2026}." | Proof of Lemma 2.10 (p. 8): "Let ℓ = lcm(1, 2, . . . , ⌈1/ε⌉), so ℓ < 2.81/ε . As N is a prime and N ≥ k > 1/ε, ℓ is invertible in ZN . … Let ℓ · I be the dilation of I by ℓ." | MATCH (an lcm dilation in ℤ_N; note the paper's own λ is NOT lcm(1..h_0) but the h_0-smooth part of lcm(1..2M) — my control shows lcm(1..h_0) would break Lemma 2.1, consistent with the paper's "tailored" remark) |

## Finite checks (scripts verbatim, outputs verbatim)

All under /tmp/oaimath/160/seats/setup_checks/, run with `ulimit -v 1000000; timeout 60 python3 <script>`; every run < 16 s and
< 65 MB RSS. Each check has a control that FAILS (or, where marked, an informative control expected to pass).


### `check_prime.py` — Lemma 2.2 `setup:prime` — exact integers. Control: n = k instead of k² must fail for all k.

```python
# Lemma setup:prime (02-setup.tex l.54-82), checked exactly with integers.
# Claim A (l.64-69): v_l(C(2n,n)) = sum_a (floor(2n/l^a) - 2 floor(n/l^a)) <= floor(log_l(2n)).
# Claim B (l.72-75): C(2n,n) >= 4^n/(2n+1).
# Claim C (l.77-79): with n=k^2, k^2 log4 - log(2k^2+1) > k log(2k^2) "for all sufficiently large k";
#   checked EXACTLY as the integer inequality 4^(k^2) > (2k^2+1)*(2k^2)^k, and the first k where it holds.
# Claim D: hence C(2k^2,k^2) has a prime factor P with k < P <= 2k^2 (checked by direct factor search, small k).
# CONTROL (must FAIL): same comparison with n = k instead of n = k^2: 4^k > (2k+1)(2k)^k is false for every k>=1.
import math, sys
from sympy import primerange, factorint

def vl_binom(n, l):           # exact valuation via Legendre
    def vf(x):
        s, p = 0, l
        while p <= x:
            s += x // p; p *= l
        return s
    return vf(2*n) - 2*vf(n)

def floor_log(l, x):          # largest a with l^a <= x
    a, p = 0, l
    while p <= x:
        a += 1; p *= l
    return a

# Claim A, all n <= 300, all primes l <= 2n
bad = 0
for n in range(1, 301):
    for l in primerange(2, 2*n+1):
        v = vl_binom(n, l)
        s = sum((2*n)//l**a - 2*(n//l**a) for a in range(1, floor_log(l, 2*n)+3))
        if v != s or v > floor_log(l, 2*n): bad += 1
print("Claim A (Kummer/Legendre bound), n<=300, all primes l<=2n: violations =", bad)

# Claim B
badB = sum(1 for n in range(1, 401) if math.comb(2*n, n)*(2*n+1) < 4**n)
print("Claim B (C(2n,n)(2n+1) >= 4^n), n<=400: violations =", badB)

# Claim C exact
first = None; fails = []
for k in range(1, 401):
    n = k*k
    holds = 4**n > (2*n+1)*(2*n)**k
    if not holds: fails.append(k)
print("Claim C exact 4^(k^2) > (2k^2+1)(2k^2)^k, k=1..400: fails at k =", fails)
print("  -> holds for every k in [%d, 400]" % (max(fails)+1))
# float version as printed in the paper, for the record
for k in (1, 2, 3, 4, 5):
    L = k*k*math.log(4) - math.log(2*k*k+1); Rr = k*math.log(2*k*k)
    print("  k=%d  k^2log4-log(2k^2+1)=%.4f   k log(2k^2)=%.4f   %s" % (k, L, Rr, L > Rr))
# analytic tail for k >= 400 (exact check covers 3..400):
#  log(2k^2+1) + k log(2k^2) <= (k+1) log(3k^2) = (k+1)(log3 + 2 log k) <= (k+1)(log3 + 2 sqrt k)   [log x <= sqrt x for x>0]
#  for k>=400: k+1 <= 1.0025k and log3 <= 0.055 sqrt k, so RHS <= 1.0025*2.055 k^{3/2} < 2.07 k^{3/2} <= (log 4) k^2  iff sqrt k >= 1.494.
print("  tail: max_x>0 (log x - sqrt x) =", max(math.log(x/100) - math.sqrt(x/100) for x in range(1, 10**6)), "(<0, so log x <= sqrt x)")
print("  tail: 1.0025*(math.log(3)/20 + 2) =", 1.0025*(math.log(3)/20 + 2), " and 2.07/log4 =", 2.07/math.log(4), "<= sqrt(400)=20")
# Claim D: prime factor of C(2k^2,k^2) in (k, 2k^2], k=3..12 (direct)
for k in range(3, 13):
    n = k*k
    fs = factorint(math.comb(2*n, n))
    big = [p for p in fs if p > k]
    assert big and max(big) <= 2*n
print("Claim D: C(2k^2,k^2) has a prime factor in (k,2k^2] for k=3..12: OK")

# CONTROL: n = k instead of n = k^2
ctl = [k for k in range(1, 401) if 4**k > (2*k+1)*(2*k)**k]
print("CONTROL (n=k): k in 1..400 where 4^k > (2k+1)(2k)^k:", ctl, "-> control FAILS for all k (expected)")
```

Output (`out_check_prime.txt`):

```
Claim A (Kummer/Legendre bound), n<=300, all primes l<=2n: violations = 0
Claim B (C(2n,n)(2n+1) >= 4^n), n<=400: violations = 0
Claim C exact 4^(k^2) > (2k^2+1)(2k^2)^k, k=1..400: fails at k = [1, 2]
  -> holds for every k in [3, 400]
  k=1  k^2log4-log(2k^2+1)=0.2877   k log(2k^2)=0.6931   False
  k=2  k^2log4-log(2k^2+1)=3.3480   k log(2k^2)=4.1589   False
  k=3  k^2log4-log(2k^2+1)=9.5322   k log(2k^2)=8.6711   True
  k=4  k^2log4-log(2k^2+1)=18.6842   k log(2k^2)=13.8629   True
  k=5  k^2log4-log(2k^2+1)=30.7255   k log(2k^2)=19.5601   True
  tail: max_x>0 (log x - sqrt x) = -0.6137056388801094 (<0, so log x <= sqrt x)
  tail: 1.0025*(math.log(3)/20 + 2) = 2.060067940969489  and 2.07/log4 = 1.4931893673200771 <= sqrt(400)=20
Claim D: C(2k^2,k^2) has a prime factor in (k,2k^2] for k=3..12: OK
CONTROL (n=k): k in 1..400 where 4^k > (2k+1)(2k)^k: [] -> control FAILS for all k (expected)
[check_prime: 0.91s, maxrss 47948kB]
exit=0
```

### `check_dilation.py` — Lemma 2.1 `setup:dilation` + h_0<2M<k + gcd(λ,P)=1 — exhaustive over h ≤ 2M and t mod h. Control: λ = lcm(1..h_0) must fail.

```python
# Lemma setup:dilation (02-setup.tex l.24-52) + standing threshold h0 < 2M < k (l.21) + gcd(lambda,q)=1 (l.90-92).
# Literal parameters: D = ceil(k^{1/10}), M = ceil(k^{1/2}), h0 = D^2,
#   lambda = prod_{l <= h0 prime} l^{floor(log(2M)/log l)}   (exponent computed EXACTLY as the largest a with l^a <= 2M).
# Checks for each k: (1) log lambda <= h0 log(2M); (2) every prime-power divisor l^a || h (l<=h0) divides lambda, 1<=h<=2M;
#   (3) h | lambda for 1<=h<=h0; (4) s = h/gcd(h, lambda t) is 1 or > h0 for all 1<=h<=2M and ALL residues t mod h
#   (s depends on t only mod h; t=0 included); (5) gcd(lambda, P) = 1 for the least prime P > k.
# CONTROL (must FAIL): lambda_bad = lcm(1..h0) (= exponents floor(log h0/log l), i.e. NOT the full primary part up to 2M).
import math
from sympy import primerange, nextprime

def iroot_ceil(k, r):           # least D with D^r >= k
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); return D, M, D*D

def lam_paper(h0, M):            # floor(log(2M)/log l) = largest a with l^a <= 2M
    lam = 1
    for l in primerange(2, h0+1):
        a = 0
        while l**(a+1) <= 2*M: a += 1
        lam *= l**a
    return lam

def lam_bad(h0):                 # lcm(1..h0)
    return math.lcm(*range(1, h0+1))

def check(k, lam, verbose=True):
    D, M, h0 = params(k)
    ok1 = math.log(lam) <= h0 * math.log(2*M) + 1e-9
    bad2 = bad3 = bad4 = 0; ex4 = None
    for h in range(1, 2*M+1):
        # prime-power parts
        x = h
        for l in primerange(2, min(h0, h)+1):
            if x % l == 0:
                pp = 1
                while x % l == 0: x //= l; pp *= l
                if lam % pp: bad2 += 1
        if h <= h0 and lam % h: bad3 += 1
        for t in range(h):
            s = h // math.gcd(h, lam*t)
            if not (s == 1 or s > h0):
                bad4 += 1
                if ex4 is None: ex4 = (h, t, s)
    P = nextprime(k)
    ok5 = math.gcd(lam, P) == 1
    if verbose:
        print("k=%-8d D=%d M=%d h0=%d 2M=%d lambda=%d log(lambda)=%.2f <= h0*log(2M)=%.2f: %s | primary-part viol=%d  h|lam viol(h<=h0)=%d  s-viol=%d %s | gcd(lambda,P=%d)=1: %s"
              % (k, D, M, h0, 2*M, lam, math.log(lam), h0*math.log(2*M), ok1, bad2, bad3, bad4, ("first "+str(ex4)) if ex4 else "", P, ok5))
    return ok1 and bad2 == 0 and bad3 == 0 and bad4 == 0 and ok5

ks = [7, 100, 1024, 1025, 10**4, 59049, 59050, 10**5, 10**6]
allok = True
for k in ks:
    D, M, h0 = params(k)
    allok &= check(k, lam_paper(h0, M))
print("PAPER lambda: all checks pass for k in", ks, ":", allok)

print("\nCONTROL lambda_bad = lcm(1..h0):")
for k in [100, 10**4, 10**6]:
    D, M, h0 = params(k)
    check(k, lam_bad(h0))

# standing threshold h0 < 2M < k, exact integer arithmetic, k = 1..10^6
fails = [k for k in range(1, 10**6+1) if not (params(k)[2] < 2*params(k)[1] < k)]
print("\nh0 < 2M < k fails for k in", fails[:20], "... (max failing k =", max(fails), ") over 1..10^6")
# for k >= 10^6: h0 <= (k^{0.1}+1)^2 <= 4 k^{0.2} < 2 k^{0.5} <= 2M and 2M <= 2k^{0.5}+2 < k  (both hold once k >= 16)
print("tail: 4*k**0.2 < 2*k**0.5 and 2*k**0.5+2 < k at k=1e6:", 4*1e6**0.2 < 2*1e6**0.5, 2*1e6**0.5 + 2 < 1e6)
```

Output (`out_check_dilation.txt`):

```
k=7        D=2 M=3 h0=4 2M=6 lambda=12 log(lambda)=2.48 <= h0*log(2M)=7.17: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=11)=1: True
k=100      D=2 M=10 h0=4 2M=20 lambda=144 log(lambda)=4.97 <= h0*log(2M)=11.98: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=101)=1: True
k=1024     D=2 M=32 h0=4 2M=64 lambda=1728 log(lambda)=7.45 <= h0*log(2M)=16.64: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=1031)=1: True
k=1025     D=3 M=33 h0=9 2M=66 lambda=2116800 log(lambda)=14.57 <= h0*log(2M)=37.71: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=1031)=1: True
k=10000    D=3 M=100 h0=9 2M=200 lambda=63504000 log(lambda)=17.97 <= h0*log(2M)=47.68: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=10007)=1: True
k=59049    D=3 M=243 h0=9 2M=486 lambda=2667168000 log(lambda)=21.70 <= h0*log(2M)=55.68: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=59051)=1: True
k=59050    D=4 M=244 h0=16 2M=488 lambda=54540918432000 log(lambda)=31.63 <= h0*log(2M)=99.05: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=59051)=1: True
k=100000   D=4 M=317 h0=16 2M=634 lambda=545409184320000 log(lambda)=33.93 <= h0*log(2M)=103.23: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=100003)=1: True
k=1000000  D=4 M=1000 h0=16 2M=2000 lambda=35997006165120000 log(lambda)=38.12 <= h0*log(2M)=121.61: True | primary-part viol=0  h|lam viol(h<=h0)=0  s-viol=0  | gcd(lambda,P=1000003)=1: True
PAPER lambda: all checks pass for k in [7, 100, 1024, 1025, 10000, 59049, 59050, 100000, 1000000] : True

CONTROL lambda_bad = lcm(1..h0):
k=100      D=2 M=10 h0=4 2M=20 lambda=12 log(lambda)=2.48 <= h0*log(2M)=11.98: True | primary-part viol=4  h|lam viol(h<=h0)=0  s-viol=34 first (8, 1, 2) | gcd(lambda,P=101)=1: True
k=10000    D=3 M=100 h0=9 2M=200 lambda=2520 log(lambda)=7.83 <= h0*log(2M)=47.68: True | primary-part viol=31  h|lam viol(h<=h0)=0  s-viol=2322 first (16, 1, 2) | gcd(lambda,P=10007)=1: True
k=1000000  D=4 M=1000 h0=16 2M=2000 lambda=720720 log(lambda)=13.49 <= h0*log(2M)=121.61: True | primary-part viol=283  h|lam viol(h<=h0)=0  s-viol=117266 first (25, 1, 5) | gcd(lambda,P=1000003)=1: True

h0 < 2M < k fails for k in [1, 2, 3, 4, 5, 6] ... (max failing k = 6 ) over 1..10^6
tail: 4*k**0.2 < 2*k**0.5 and 2*k**0.5+2 < k at k=1e6: True True
[check_dilation: 4.93s, maxrss 47772kB]
exit=0
```

### `check_qbounds.py` — (2.4) `setup:q-bounds` and (2.6) `setup:orders` — every prime P∈(k,2k²] for k ≤ 60, exact integer form at five k, logs to 10^40. Control: P > 2k² must break the upper bound.

```python
# (setup:q-bounds) 02-setup.tex l.84-92 and (setup:orders) l.97-101.
# q = least power of P >= k^{ck/D}, c = 1/100000, D = ceil(k^{1/10}).
# EXACT integer form (no floating point):  q >= k^{ck/D}  <=>  q^(10^5 D) >= k^k ;
#                                          q <= 2k^2 k^{ck/D} <=> q^(10^5 D) <= (2k^2)^(10^5 D) * k^k.
# Checked for EVERY prime P in (k, 2k^2] for k = 3..30 (uniformity over the choice in Lemma setup:prime),
# and for the least prime P>k at several larger k. Then log-scale (mpmath, 60 digits) for k up to 10^40.
# CONTROL (must FAIL): a prime P' > 2k^2 (outside Lemma setup:prime's range) -- the upper bound breaks.
import math, mpmath
from sympy import primerange, nextprime
mpmath.mp.dps = 60
C_DEN = 10**5

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r)))) if k < 10**300 else int(mpmath.ceil(mpmath.mpf(k)**(mpmath.mpf(1)/r)))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def least_q(P, k, D):            # least P^e (e>=0) with (P^e)^(C_DEN*D) >= k^k ; uses logs to guess e then exact fix-up
    E = C_DEN * D
    target = k**k
    e = max(0, int(mpmath.floor(mpmath.mpf(k)*mpmath.log(k)/(E*mpmath.log(P)))) - 1)
    while (P**e)**E < target: e += 1
    while e > 0 and (P**(e-1))**E >= target: e -= 1
    return e

def exact_bounds(P, k, D):
    e = least_q(P, k, D); q = P**e; E = C_DEN*D
    lower = q**E >= k**k
    upper = q**E <= (2*k*k)**E * k**k
    return e, lower, upper

def log_bounds(P, k, D):          # same inequalities in log form, 60-digit mpmath, returning margins
    c = mpmath.mpf(1)/C_DEN; lk = mpmath.log(k); lP = mpmath.log(P)
    e = max(1, int(mpmath.ceil(c*k*lk/(D*lP))))
    # minimality fix-up
    while e > 1 and (e-1)*lP*D >= c*k*lk: e -= 1
    while e*lP*D < c*k*lk: e += 1
    m_lo = D*e*lP - c*k*lk
    m_up = c*k*lk + D*mpmath.log(2*k*k) - D*e*lP
    return e, m_lo, m_up

viol = 0; cnt = 0; e_hist = {}; min_lo = None; min_up = None
for k in range(3, 61):
    D = iroot_ceil(k, 10)
    for P in primerange(k+1, 2*k*k+1):
        e, mlo, mup = log_bounds(P, k, D)
        cnt += 1; e_hist[e] = e_hist.get(e, 0) + 1
        if not (mlo >= 0 and mup >= 0 and e >= 1): viol += 1
        min_lo = mlo if min_lo is None else min(min_lo, mlo); min_up = mup if min_up is None else min(min_up, mup)
print("log-form q-bounds, k=3..60, EVERY prime P in (k,2k^2]: %d (k,P) pairs, violations=%d, exponent histogram=%s, min lower margin=%s, min upper margin=%s"
      % (cnt, viol, e_hist, mpmath.nstr(min_lo, 5), mpmath.nstr(min_up, 5)))

for k in [3, 10, 30, 100, 400]:
    D = iroot_ceil(k, 10); P = nextprime(k)
    e, lo, up = exact_bounds(P, k, D)
    print("EXACT integer form k=%d D=%d P=%d e=%d  q^(1e5 D) >= k^k: %s   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: %s" % (k, D, P, e, lo, up))

print("\nlog-scale (mpmath 60 digits): ck log k <= D log q <= ck log k + D log(2k^2); orders of magnitude")
c = mpmath.mpf(1)/C_DEN
for k in [10**4, 10**6, 10**9, 10**12, 10**20, 10**40]:
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D*D
    P = nextprime(k)
    lk, lP = mpmath.log(k), mpmath.log(P)
    e = int(mpmath.ceil(c*k*lk/(D*lP)))
    if e < 1: e = 1
    logq = e*lP
    lo = c*k*lk <= D*logq; up = D*logq <= c*k*lk + D*mpmath.log(2*mpmath.mpf(k)**2)
    # log lambda exactly as sum a*log l for k <= 10^12 (h0 small enough)
    if h0 <= 10**5:
        loglam = mpmath.fsum(mpmath.mpf(int(mpmath.floor(mpmath.log(2*M)/mpmath.log(l))))*mpmath.log(l) for l in primerange(2, h0+1))
        lam_ratio = mpmath.nstr(loglam/(mpmath.mpf(k)**(mpmath.mpf(1)/5)*lk), 4)
    else:
        lam_ratio = "skip"
    alpha_log = -(D+1)*logq
    R = mpmath.log1p(mpmath.exp(-alpha_log)/2)
    m = mpmath.ceil(mpmath.mpf(k)**2*R)
    print("k=1e%-3d D=%-5d e=%-14d lower=%s upper=%s | logq/(k^.9 logk)=%s  loglam/(k^.2 logk)=%s  D/k^.1=%s  M/k^.5=%s  |V|/(k^3 log k)=%s"
          % (round(math.log10(k)), D, e, lo, up, mpmath.nstr(logq/(mpmath.mpf(k)**0.9*lk), 4), lam_ratio,
             mpmath.nstr(D/mpmath.mpf(k)**0.1, 4), mpmath.nstr(M/mpmath.mpf(k)**0.5, 4), mpmath.nstr(2*m/(mpmath.mpf(k)**3*lk), 4)))

print("\nCONTROL: prime P' > 2k^2 (outside Lemma setup:prime)")
for k in [10, 20, 30]:
    D = iroot_ceil(k, 10); Pbad = nextprime(k**3)
    e, lo, up = exact_bounds(Pbad, k, D)
    print("k=%d P'=%d e=%d lower=%s upper=%s  -> %s" % (k, Pbad, e, lo, up, "upper bound FAILS (expected)" if not up else "control did not fail"))
```

Output (`out_check_qbounds.txt`):

```
log-form q-bounds, k=3..60, EVERY prime P in (k,2k^2]: 20099 (k,P) pairs, violations=0, exponent histogram={1: 20099}, min lower margin=3.2188, min upper margin=0.0020618
EXACT integer form k=3 D=2 P=5 e=1  q^(1e5 D) >= k^k: True   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: True
EXACT integer form k=10 D=2 P=11 e=1  q^(1e5 D) >= k^k: True   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: True
EXACT integer form k=30 D=2 P=31 e=1  q^(1e5 D) >= k^k: True   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: True
EXACT integer form k=100 D=2 P=101 e=1  q^(1e5 D) >= k^k: True   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: True
EXACT integer form k=400 D=2 P=401 e=1  q^(1e5 D) >= k^k: True   q^(1e5 D) <= (2k^2)^(1e5 D) k^k: True

log-scale (mpmath 60 digits): ck log k <= D log q <= ck log k + D log(2k^2); orders of magnitude
k=1e4   D=3     e=1              lower=True upper=True | logq/(k^.9 logk)=0.0002512  loglam/(k^.2 logk)=0.3092  D/k^.1=1.194  M/k^.5=1.0  |V|/(k^3 log k)=0.000785
k=1e6   D=4     e=3              lower=True upper=True | logq/(k^.9 logk)=1.194e-5  loglam/(k^.2 logk)=0.1741  D/k^.1=1.005  M/k^.5=1.0  |V|/(k^3 log k)=2.99e-5
k=1e9   D=8     e=1250           lower=True upper=True | logq/(k^.9 logk)=9.929e-6  loglam/(k^.2 logk)=0.1266  D/k^.1=1.007  M/k^.5=1.0  |V|/(k^3 log k)=2.25e-5
k=1e12  D=16    e=625000         lower=True upper=True | logq/(k^.9 logk)=9.906e-6  loglam/(k^.2 logk)=0.09308  D/k^.1=1.01  M/k^.5=1.0  |V|/(k^3 log k)=2.125e-5
k=1e20  D=100   e=10000000000000 lower=True upper=True | logq/(k^.9 logk)=1.0e-5  loglam/(k^.2 logk)=0.05004  D/k^.1=1.0  M/k^.5=1.0  |V|/(k^3 log k)=2.02e-5
k=1e40  D=10000 e=10000000000000000000000000000000 lower=True upper=True | logq/(k^.9 logk)=1.0e-5  loglam/(k^.2 logk)=skip  D/k^.1=1.0  M/k^.5=1.0  |V|/(k^3 log k)=2.0e-5

CONTROL: prime P' > 2k^2 (outside Lemma setup:prime)
k=10 P'=1009 e=1 lower=True upper=False  -> upper bound FAILS (expected)
k=20 P'=8009 e=1 lower=True upper=False  -> upper bound FAILS (expected)
k=30 P'=27011 e=1 lower=True upper=False  -> upper bound FAILS (expected)
[check_qbounds: 5.54s, maxrss 50244kB]
exit=0
```

### `check_elementary.py` — Elementary inequalities of Lemma 2.3 and explicit thresholds of the in-section "large k" assumptions. Controls: θ = 1.3, 1.6 must fail.

```python
# Elementary real inequalities used in Lemma mesh:width (02-setup.tex l.194-197) and the explicit k-thresholds of
# every "for large k" assumption made inside 02-setup.tex.
# (i)  e^t - 1 <= 2t  on [0,1]   (convexity: e^t - 1 <= (e-1) t on [0,1], and e - 1 < 2)
# (ii) 1 - e^{-t} >= t/2 on [0,1] (concavity: 1 - e^{-t} >= (1 - 1/e) t on [0,1], and 1 - 1/e > 1/2)
# CONTROLS (must FAIL): (i) at t = 1.3, (ii) at t = 1.6 -- the hypothesis t <= 1 (i.e. theta <= 1) is genuinely used.
import mpmath, math
mpmath.mp.dps = 40
N = 200000
g1 = min(2*mpmath.mpf(i)/N - mpmath.expm1(mpmath.mpf(i)/N) for i in range(0, N+1, 7)) 
g2 = min(-mpmath.expm1(-mpmath.mpf(i)/N) - mpmath.mpf(i)/(2*N) for i in range(0, N+1, 7))
print("min over grid of 2t-(e^t-1) on [0,1] =", mpmath.nstr(g1, 6), " | chord slope e-1 =", mpmath.nstr(mpmath.e - 1, 8), "< 2")
print("min over grid of (1-e^-t)-t/2 on [0,1] =", mpmath.nstr(g2, 6), " | chord slope 1-1/e =", mpmath.nstr(1 - 1/mpmath.e, 8), "> 1/2")
print("CONTROL t=1.3: e^t-1 <= 2t ?", mpmath.expm1(1.3) <= 2.6, "(e^1.3-1 = %s)" % mpmath.nstr(mpmath.expm1(1.3), 6))
print("CONTROL t=1.6: 1-e^-t >= t/2 ?", -mpmath.expm1(-1.6) >= 0.8, "(1-e^-1.6 = %s)" % mpmath.nstr(-mpmath.expm1(-1.6), 6))
# the largest t for which each holds (where the hypothesis really bites)
t1 = mpmath.findroot(lambda t: mpmath.expm1(t) - 2*t, 1.25); t2 = mpmath.findroot(lambda t: -mpmath.expm1(-t) - t/2, 1.6)
print("e^t-1<=2t holds exactly on [0, %s];  1-e^-t >= t/2 holds exactly on [0, %s]" % (mpmath.nstr(t1, 8), mpmath.nstr(t2, 8)))

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D
print("\nexplicit thresholds for the in-section 'large k' assumptions (checked k = 1..10^5 exactly; each is monotone after):")
conds = {
  "h0 < 2M < k (l.21)": lambda k: iroot_ceil(k,10)**2 < 2*iroot_ceil(k,2) < k,
  "H = k^-2 <= 1/8 (mesh:neighbors)": lambda k: 8 <= k*k,
  "4H < 1 and 3*(2H) < 1 (arcs)": lambda k: 4 < k*k and 6 < k*k,
  "alpha <= 1/4, R >= 1 given q >= P >= k+1 (mesh:width)": lambda k: (k+1)**2 >= 4 and (k+1)**2 >= 2*(math.e - 1) ,
  "prime lemma 4^(k^2)>(2k^2+1)(2k^2)^k [exact k<60 here; 3..400+tail in check_prime.py]": lambda k: 4**(k*k) > (2*k*k+1)*(2*k*k)**k if k < 60 else True,
  "h0 < k (so h0 < k < P, gcd(lambda,q)=1)": lambda k: iroot_ceil(k,10)**2 < k,
}
for name, f in conds.items():
    bad = [k for k in range(1, 10**5 + 1) if not f(k)]
    print("  %-58s fails for k in %s -> holds for all k >= %d" % (name, bad if len(bad) < 12 else str(bad[:12]) + "...", (max(bad) + 1) if bad else 1))
```

Output (`out_check_elementary.txt`):

```
min over grid of 2t-(e^t-1) on [0,1] = 0.0  | chord slope e-1 = 1.7182818 < 2
min over grid of (1-e^-t)-t/2 on [0,1] = 0.0  | chord slope 1-1/e = 0.63212056 > 1/2
CONTROL t=1.3: e^t-1 <= 2t ? False (e^1.3-1 = 2.6693)
CONTROL t=1.6: 1-e^-t >= t/2 ? False (1-e^-1.6 = 0.798103)
e^t-1<=2t holds exactly on [0, 1.2564312];  1-e^-t >= t/2 holds exactly on [0, 1.5936243]

explicit thresholds for the in-section 'large k' assumptions (checked k = 1..10^5 exactly; each is monotone after):
  h0 < 2M < k (l.21)                                         fails for k in [1, 2, 3, 4, 5, 6] -> holds for all k >= 7
  H = k^-2 <= 1/8 (mesh:neighbors)                           fails for k in [1, 2] -> holds for all k >= 3
  4H < 1 and 3*(2H) < 1 (arcs)                               fails for k in [1, 2] -> holds for all k >= 3
  alpha <= 1/4, R >= 1 given q >= P >= k+1 (mesh:width)      fails for k in [] -> holds for all k >= 1
  prime lemma 4^(k^2)>(2k^2+1)(2k^2)^k [exact k<60 here; 3..400+tail in check_prime.py] fails for k in [1, 2] -> holds for all k >= 3
  h0 < k (so h0 < k < P, gcd(lambda,q)=1)                    fails for k in [1, 2, 3, 4] -> holds for all k >= 5
[check_elementary: 2.74s, maxrss 15472kB]
exit=0
```

### `check_mesh.py` — Literal V-mesh, every cell, k = 3..32 (30-digit mpmath): partition, Lemma 2.3, Lemma 2.4 (49 and 1/16), Lemma 2.5. Controls C1 (wrong growth m'=⌈kR⌉), C2 (uniform), C3 (64 cells merged) must report violations.

```python
# The V-mesh of 02-setup.tex, built LITERALLY from (mesh:definition)/(mesh:intervals) for small k, in 30-digit mpmath:
#   D=ceil(k^{1/10}), P = least prime > k, q = least power of P >= k^{ck/D} (c=1e-5), alpha = q^{-(D+1)},
#   R = log(1+1/(2alpha)), m = ceil(k^2 R), a_l = alpha(e^{lR/m}-1), H = k^{-2}, eta = 1/(1000 D).
# Verifies: partition of [-1/2,1/2) (a_0=0, a_m=1/2, strict monotonicity, where 0 and the cut sit);
#   Lemma mesh:width  (1/4)H(rho+alpha) <= |I| <= 2H(rho+alpha) <= 2H at BOTH closure endpoints of every I
#      (rho is affine on each closed interval, so endpoint checks cover all of I-bar), |V| = 2m vs k^3 log k;
#   Lemma mesh:neighbors: for every I, N(I) = {dist(Y, I-bar) <= w}: #mesh endpoints in N(I) <= 49 and min|J| >= w/16
#      over all J with J-bar meeting N(I) (circular, incl. wrap across the cut);
#   Lemma mesh:truncated: max #breakpoints of V_eta on a closed arc of length 4H  <= 16004 D
#      (breakpoints = mesh endpoints with rho >= eta, plus the two threshold points rho = eta; max is attained by
#       arcs starting at a breakpoint, so all such arcs are enumerated).
# CONTROLS (must FAIL the same checker): C1 wrong growth rate m' = ceil(k R) ; C2 uniform mesh of 2m equal cells ;
#   C3 the paper's mesh with 64 consecutive cells merged into one (abrupt scale change).
import math, bisect, sys, time
import mpmath
from sympy import nextprime
mpmath.mp.dps = 30
mpf = mpmath.mpf
HALF = mpf(1)/2

def iroot_ceil(k, r):
    D = max(1, int(round(k ** (1.0/r))))
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); P = nextprime(k)
    c = mpf(1)/10**5; lk = mpmath.log(k); lP = mpmath.log(P)
    e = 1
    while e*lP < c*k*lk/D: e += 1
    q = P**e
    alpha = mpf(1)/mpf(q)**(D+1)
    R = mpmath.log(1 + 1/(2*alpha))
    m = int(mpmath.ceil(mpf(k)**2 * R))
    H = mpf(1)/k**2; eta = mpf(1)/(1000*D)
    return dict(k=k, D=D, P=P, q=q, alpha=alpha, R=R, m=m, H=H, eta=eta)

def paper_endpoints(pr, m=None):
    m = pr['m'] if m is None else m
    al, R = pr['alpha'], pr['R']
    a = [al*(mpmath.exp(l*R/m) - 1) for l in range(m+1)]
    # identity a_m = alpha(e^R - 1) = alpha * 1/(2 alpha) = 1/2 is exact; check numerically, then store it exactly
    assert abs(a[m] - HALF) < mpf(10)**-25, a[m]
    a[m] = HALF
    return a

def mesh_from_a(a):
    # sorted endpoint list E (all in [-1/2,1/2)), intervals [E_i, E_{i+1}) with E_{len} := 1/2 (== -1/2 on circle)
    m = len(a) - 1
    E = [-HALF + a[l] for l in range(m)] + [HALF - a[l] for l in range(m, 0, -1)]
    return E

def rho(x):              # x in [-1/2, 1/2]
    return HALF - abs(x)

def check_partition(a, E):
    m = len(a) - 1
    ok = (a[0] == 0) and abs(a[m] - HALF) < mpf(10)**-25 and all(a[i] < a[i+1] for i in range(m))
    ok = ok and all(E[i] < E[i+1] for i in range(len(E)-1)) and E[0] == -HALF and E[-1] < HALF
    # zero is the LEFT endpoint of an interval (assigned to the interval on its right); the cut -1/2 is E[0]
    iz = bisect.bisect_right(E, mpf(0)) - 1          # index of the interval containing 0 (half-open [E_i,E_{i+1}))
    zero_ok = (E[iz] == 0) and (iz == m)              # 0 is the LEFT end of the interval right of it: [0, 1/2 - a_{m-1})
    return ok, zero_ok, iz

def widths(E):
    return [E[i+1] - E[i] for i in range(len(E)-1)] + [HALF - E[-1]]

def check_width(pr, E, W):
    H, al = pr['H'], pr['alpha']
    worst_lo = None; worst_hi = None; viol = 0; maxw = 0
    n = len(E)
    for i in range(n):
        l = E[i]; r = E[i+1] if i+1 < n else HALF
        for y in (l, r):
            s = rho(y) + al
            lo = W[i] / (H*s); 
            if worst_lo is None or lo < worst_lo: worst_lo = lo
            if worst_hi is None or lo > worst_hi: worst_hi = lo
            if not (H*s/4 <= W[i] <= 2*H*s <= 2*H): viol += 1
        maxw = max(maxw, W[i])
    return viol, worst_lo, worst_hi, maxw

def count_closed(E, A, B):
    # number of points of E in closed real interval [A,B] (A,B possibly outside [-1/2,1/2): wrap)
    def cnt(lo, hi):
        if hi < lo: return 0
        return bisect.bisect_right(E, hi) - bisect.bisect_left(E, lo)
    total = cnt(max(A, -HALF), min(B, HALF))
    if A < -HALF: total += cnt(A + 1, HALF)
    if B >= HALF: total += cnt(-HALF, B - 1)
    # the point 1/2 == -1/2 = E[0]: counted once via -HALF if B>=HALF wrap or A<=-1/2; guard double count
    if A <= -HALF and B >= HALF: total -= 1
    return total

def intervals_meeting(E, A, B):
    # indices i of intervals [E_i, E_{i+1}] (closure) meeting closed real interval [A,B], A,B in [-1/2,1/2]
    n = len(E)
    Ext = E + [HALF]
    i_lo = max(0, bisect.bisect_left(Ext, A) - 1)     # first i with E_{i+1} >= A
    i_hi = min(n-1, bisect.bisect_right(Ext, B) - 1)  # last i with E_i <= B
    return i_lo, i_hi

def check_neighbors(E, W):
    n = len(E); maxcnt = 0; minratio = None; viol = 0
    for i in range(n):
        w = W[i]; l = E[i]; r = E[i+1] if i+1 < n else HALF
        A, B = l - w, r + w
        c = count_closed(E, A, B)
        maxcnt = max(maxcnt, c)
        # closures meeting N(I): pieces of [A,B] reduced into [-1/2,1/2]
        pieces = []
        pieces.append((max(A, -HALF), min(B, HALF)))
        if A < -HALF: pieces.append((A + 1, HALF))
        if B > HALF: pieces.append((-HALF, B - 1))
        mn = None
        for (x, y) in pieces:
            i0, i1 = intervals_meeting(E, x, y)
            rng = range(i0, i1+1)
            cand = [W[j] for j in rng]
            mm = min(cand)
            mn = mm if mn is None else min(mn, mm)
        rt = mn / w
        if minratio is None or rt < minratio: minratio = rt
        if c > 49 or rt < mpf(1)/16: viol += 1
    return viol, maxcnt, minratio

def check_truncated(pr, E):
    eta, H, D = pr['eta'], pr['H'], pr['D']
    B = [x for x in E if rho(x) >= eta]
    B += [-HALF + eta, HALF - eta]
    B = sorted(set(B))
    L = 4*H; mx = 0
    for b in B:
        mx = max(mx, count_closed(B, b, b + L) if b + L < HALF else count_closed(B, b, b + L))
    return mx, 16004*D

def report(tag, pr, a, E, do_trunc=True):
    t0 = time.time()
    W = widths(E)
    okp, zero_ok, iz = check_partition(a, E)
    vw, lo, hi, maxw = check_width(pr, E, W)
    vn, maxcnt, minratio = check_neighbors(E, W)
    line = ("%s k=%d D=%d P=%d q=%d m=%d |V|=%d |V|/(k^3 log k)=%.3f | partition=%s 0 in [0,1/2-a_{m-1}):%s cut=E[0]=%s | "
            "width viol=%d ratio |I|/(H(rho+a)) in [%s, %s] (claim [1/4,2]) max|I|/2H=%s | neighbors viol=%d max#endpoints(N(I))=%d (claim<=49) min|J|/w=%s (claim>=1/16)"
            % (tag, pr['k'], pr['D'], pr['P'], pr['q'], len(a)-1, len(E), len(E)/(pr['k']**3*math.log(pr['k'])), okp, zero_ok, E[0] == -HALF,
               vw, mpmath.nstr(lo, 5), mpmath.nstr(hi, 5), mpmath.nstr(maxw/(2*pr['H']), 5), vn, maxcnt, mpmath.nstr(minratio, 5)))
    if do_trunc:
        mx, bound = check_truncated(pr, E)
        line += " | trunc max#breakpoints on 4H-arc=%d (claim<=%d)" % (mx, bound)
    print(line + "  [%.1fs]" % (time.time() - t0)); sys.stdout.flush()
    return vw, vn

print("== PAPER MESH (literal formulas) ==")
for k in [3, 4, 5, 7, 10, 16, 24, 32]:
    pr = params(k)
    th = pr['R']/pr['m']
    assert pr['alpha'] <= mpf(1)/4 and pr['R'] >= 1 and pr['H']/2 <= th <= pr['H']
    assert pr['k']**2*pr['R'] <= pr['m'] <= 2*pr['k']**2*pr['R'] and pr['R'] <= (pr['D']+1)*mpmath.log(pr['q'])
    a = paper_endpoints(pr); E = mesh_from_a(a)
    report("PAPER", pr, a, E)

print("\n== CONTROLS (each must report violations) ==")
for k in [10, 24]:
    pr = params(k)
    # C1 wrong growth rate
    m1 = int(mpmath.ceil(k*pr['R']))
    a1 = paper_endpoints(pr, m=m1); E1 = mesh_from_a(a1)
    report("C1 m'=ceil(kR)", pr, a1, E1, do_trunc=False)
    # C2 uniform mesh, same number of cells
    m = pr['m']; a2 = [mpf(l)/(2*m) for l in range(m+1)]; E2 = mesh_from_a(a2)
    report("C2 uniform    ", pr, a2, E2, do_trunc=False)
    # C3 merged cells
    a = paper_endpoints(pr); mid = m//2
    a3 = a[:mid] + a[mid+64:]
    E3 = mesh_from_a(a3)
    report("C3 merge-64   ", pr, a3, E3, do_trunc=False)
```

Output (`out_check_mesh.txt`):

```
== PAPER MESH (literal formulas) ==
PAPER k=3 D=2 P=5 q=5 m=38 |V|=76 |V|/(k^3 log k)=2.562 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.93135, 1.0388] (claim [1/4,2]) max|I|/2H=0.23656 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.80374 (claim>=1/16) | trunc max#breakpoints on 4H-arc=63 (claim<=32008)  [0.0s]
PAPER k=4 D=2 P=5 q=5 m=67 |V|=134 |V|/(k^3 log k)=1.510 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.96121, 1.0226] (claim [1/4,2]) max|I|/2H=0.24415 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.88346 (claim>=1/16) | trunc max#breakpoints on 4H-arc=92 (claim<=32008)  [0.0s]
PAPER k=5 D=2 P=7 q=7 m=129 |V|=258 |V|/(k^3 log k)=1.282 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.97848, 1.0183] (claim [1/4,2]) max|I|/2H=0.24605 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.92325 (claim>=1/16) | trunc max#breakpoints on 4H-arc=163 (claim<=32008)  [0.0s]
PAPER k=7 D=2 P=11 q=11 m=319 |V|=638 |V|/(k^3 log k)=0.956 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.98864, 1.009] (claim [1/4,2]) max|I|/2H=0.24753 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.96005 (claim>=1/16) | trunc max#breakpoints on 4H-arc=345 (claim<=32008)  [0.1s]
PAPER k=10 D=2 P=11 q=11 m=651 |V|=1302 |V|/(k^3 log k)=0.565 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.99381, 1.0038] (claim [1/4,2]) max|I|/2H=0.24882 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.98022 (claim>=1/16) | trunc max#breakpoints on 4H-arc=564 (claim<=32008)  [0.3s]
PAPER k=16 D=2 P=17 q=17 m=1999 |V|=3998 |V|/(k^3 log k)=0.352 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.99783, 1.0017] (claim [1/4,2]) max|I|/2H=0.24956 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.99222 (claim>=1/16) | trunc max#breakpoints on 4H-arc=1249 (claim<=32008)  [0.8s]
PAPER k=24 D=2 P=29 q=29 m=5420 |V|=10840 |V|/(k^3 log k)=0.247 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.99904, 1.0008] (claim [1/4,2]) max|I|/2H=0.24978 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.99653 (claim>=1/16) | trunc max#breakpoints on 4H-arc=2157 (claim<=32008)  [2.4s]
PAPER k=32 D=2 P=37 q=37 m=10383 |V|=20766 |V|/(k^3 log k)=0.183 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=0 ratio |I|/(H(rho+a)) in [0.99951, 1.0005] (claim [1/4,2]) max|I|/2H=0.24989 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.99805 (claim>=1/16) | trunc max#breakpoints on 4H-arc=2733 (claim<=32008)  [6.0s]

== CONTROLS (each must report violations) ==
C1 m'=ceil(kR) k=10 D=2 P=11 q=11 m=66 |V|=132 |V|/(k^3 log k)=0.057 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=264 ratio |I|/(H(rho+a)) in [9.3819, 10.353] (claim [1/4,2]) max|I|/2H=2.349 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.82116 (claim>=1/16)  [0.0s]
C2 uniform     k=10 D=2 P=11 q=11 m=651 |V|=1302 |V|/(k^3 log k)=0.565 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=1204 ratio |I|/(H(rho+a)) in [0.15338, 102.23] (claim [1/4,2]) max|I|/2H=0.038402 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=1.0 (claim>=1/16)  [0.2s]
C3 merge-64    k=10 D=2 P=11 q=11 m=587 |V|=1174 |V|/(k^3 log k)=0.510 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=4 ratio |I|/(H(rho+a)) in [0.99381, 91.402] (claim [1/4,2]) max|I|/2H=0.87325 | neighbors viol=2 max#endpoints(N(I))=286 (claim<=49) min|J|/w=0.00094108 (claim>=1/16)  [0.1s]
C1 m'=ceil(kR) k=24 D=2 P=29 q=29 m=226 |V|=452 |V|/(k^3 log k)=0.010 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=904 ratio |I|/(H(rho+a)) in [23.488, 24.486] (claim [1/4,2]) max|I|/2H=5.8724 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=0.92011 (claim>=1/16)  [0.0s]
C2 uniform     k=24 D=2 P=29 q=29 m=5420 |V|=10840 |V|/(k^3 log k)=0.247 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=13616 ratio |I|/(H(rho+a)) in [0.10626, 1295.9] (claim [1/4,2]) max|I|/2H=0.026568 | neighbors viol=0 max#endpoints(N(I))=4 (claim<=49) min|J|/w=1.0 (claim>=1/16)  [2.3s]
C3 merge-64    k=24 D=2 P=29 q=29 m=5356 |V|=10712 |V|/(k^3 log k)=0.244 | partition=True 0 in [0,1/2-a_{m-1}):True cut=E[0]=True | width viol=4 ratio |I|/(H(rho+a)) in [0.99904, 68.803] (claim [1/4,2]) max|I|/2H=0.24978 | neighbors viol=2 max#endpoints(N(I))=133 (claim<=49) min|J|/w=0.012792 (claim>=1/16)  [1.9s]
[check_mesh: 15.17s, maxrss 64300kB]
exit=0
```

### `check_mesh_large.py` — Same mesh at k = 1025, 10^6, 10^9, 10^12 (D = 3, 4, 8, 16) on windows (cut, threshold, zero, 3 random), cancellation-free local coordinates, 80 digits; closed form for Lemma 2.5.

```python
# Same V-mesh at LARGE k (D = 3, 4, 8, 16), where the full mesh (2m ~ 1e7..1e30 cells) cannot be enumerated.
# Windows of cells: at the cut, at the threshold rho = eta, at zero, and 3 random places.  Each window uses a LOCAL
# coordinate in which every endpoint is computed without cancellation (80-digit mpmath):
#   cut window:  s = signed distance from the cut;  left endpoints s = a_j, right endpoints s = -a_j.
#   zero window: u = signed distance from zero;     left endpoints u = -b_j, right endpoints u = +b_j,
#                b_j = 1/2 - a_j = alpha e^{j theta} expm1((m-j) theta)   (exact rewriting since alpha(e^R - 1) = 1/2).
#   middle windows: t = a_j (left family; the mirror cells are isometric images, rho is mirror-invariant).
# On every left cell [a_j, a_{j+1}] in a window: mesh:width at both closure endpoints, and for N(I) = [l-w, r+w]
# the number of endpoints (<= 49) and the min width of cells whose closure meets N(I) (>= w/16); N(I) is asserted to
# lie inside the generated window so the count is complete.
# Closed form for mesh:truncated: densest 4H-arc in {rho >= eta} starts at the threshold point; count =
#   1 + #{j : eta <= a_j <= eta + 4H}.
import math, random, bisect
import mpmath
from sympy import nextprime
mpmath.mp.dps = 80
mpf = mpmath.mpf
random.seed(1)

def iroot_ceil(k, r):
    D = max(int(mpmath.floor(mpf(k)**(mpf(1)/r))), 1)
    while D**r < k: D += 1
    while D > 1 and (D-1)**r >= k: D -= 1
    return D

def params(k):
    D = iroot_ceil(k, 10); P = nextprime(k)
    c = mpf(1)/10**5; lk = mpmath.log(k); lP = mpmath.log(P)
    e = max(1, int(mpmath.ceil(c*k*lk/(D*lP))))
    while e > 1 and (e-1)*lP >= c*k*lk/D: e -= 1
    while e*lP < c*k*lk/D: e += 1
    alpha = mpmath.exp(-(D+1)*e*lP)
    R = mpmath.log(1 + 1/(2*alpha))
    m = int(mpmath.ceil(mpf(k)**2*R))
    return dict(k=k, D=D, P=P, e=e, alpha=alpha, R=R, m=m, theta=R/m, H=mpf(1)/mpf(k)**2, eta=mpf(1)/(1000*D))

def a_of(pr, j):  return pr['alpha']*mpmath.expm1(j*pr['theta'])
def b_of(pr, j):  return pr['alpha']*mpmath.exp(j*pr['theta'])*mpmath.expm1((pr['m']-j)*pr['theta'])   # = 1/2 - a_j
def w_of(pr, j):  return pr['alpha']*mpmath.exp(j*pr['theta'])*mpmath.expm1(pr['theta'])               # = a_{j+1} - a_j

def window_check(pr, j0, j1, kind, pad=60):
    m, H, al = pr['m'], pr['H'], pr['alpha']
    lo, hi = max(0, j0 - pad), min(m, j1 + pad)
    if kind == 'cut':
        pts = sorted(set([a_of(pr, j) for j in range(lo, hi+1)] + [-a_of(pr, j) for j in range(max(1, lo), hi+1)]))
        cell = lambda j: (a_of(pr, j), a_of(pr, j+1))
    elif kind == 'zero':
        pts = sorted(set([-b_of(pr, j) for j in range(lo, hi+1)] + [b_of(pr, j) for j in range(lo, hi+1)]))
        cell = lambda j: (-b_of(pr, j), -b_of(pr, j+1))
    else:
        pts = [a_of(pr, j) for j in range(lo, hi+1)]
        cell = lambda j: (a_of(pr, j), a_of(pr, j+1))
    viol = 0; maxcnt = 0; minrt = None; lo_r = None; hi_r = None; n = 0
    for j in range(max(j0, 0), min(j1, m-1) + 1):
        l, r = cell(j); w = w_of(pr, j); n += 1
        assert abs((r - l) - w) <= mpf(10)**-60 * w + mpf(10)**-75, "width formula mismatch"
        for rho in (a_of(pr, j), a_of(pr, j+1)):             # rho at the two closure endpoints of the left cell j
            s = rho + al; rt = w/(H*s)
            lo_r = rt if lo_r is None else min(lo_r, rt); hi_r = rt if hi_r is None else max(hi_r, rt)
            if not (H*s/4 <= w <= 2*H*s <= 2*H): viol += 1
        Lb, Rb = l - w, r + w
        assert pts[0] < Lb, ("window too small (left)", kind, j)
        assert Rb < pts[-1], ("window too small (right)", kind, j)
        i_l = bisect.bisect_left(pts, Lb); i_r = bisect.bisect_right(pts, Rb)
        c = i_r - i_l
        seg = pts[max(0, i_l - 1): min(len(pts), i_r + 1)]     # endpoints of every cell whose closure meets N(I)
        mw = min(seg[i+1] - seg[i] for i in range(len(seg) - 1))
        rt2 = mw/w
        minrt = rt2 if minrt is None else min(minrt, rt2); maxcnt = max(maxcnt, c)
        if c > 49 or rt2 < mpf(1)/16: viol += 1
    return n, viol, lo_r, hi_r, maxcnt, minrt

for k in [1025, 10**6, 10**9, 10**12]:
    pr = params(k); m = pr['m']
    jeta = int(mpmath.ceil(mpmath.log(1 + pr['eta']/pr['alpha'])/pr['theta']))
    wins = [(0, 200, 'cut'), (jeta - 100, jeta + 100, 'mid'), (m - 200, m - 1, 'zero')] + \
           [(x, x + 100, 'mid') for x in (random.randrange(400, m - 400) for _ in range(3))]
    tot = [0, 0]; LO = HI = MR = None; MC = 0
    for (j0, j1, kind) in wins:
        n, v, lo_r, hi_r, mc, mr = window_check(pr, j0, j1, kind)
        tot[0] += n; tot[1] += v; MC = max(MC, mc)
        LO = lo_r if LO is None else min(LO, lo_r); HI = hi_r if HI is None else max(HI, hi_r); MR = mr if MR is None else min(MR, mr)
    th, al, eta, H = pr['theta'], pr['alpha'], pr['eta'], pr['H']
    n_in = int(mpmath.floor(mpmath.log(1 + (eta + 4*H)/al)/th)) - int(mpmath.ceil(mpmath.log(1 + eta/al)/th)) + 1
    print("k=%-14d D=%-3d e=%-7d m=%s theta/H=%s | %d cells: viol=%d, |I|/(H(rho+a)) in [%s,%s], max#endpoints(N(I))=%d, min|J|/w=%s | densest 4H-arc of V_eta: %d breakpoints vs 16004D=%d (ratio %.3f)"
          % (k, pr['D'], pr['e'], mpmath.nstr(mpf(m), 4), mpmath.nstr(th/H, 8), tot[0], tot[1], mpmath.nstr(LO, 6), mpmath.nstr(HI, 6), MC, mpmath.nstr(MR, 6),
             n_in + 1, 16004*pr['D'], (n_in + 1)/(16004*pr['D'])))
```

Output (`out_check_mesh_large.txt`):

```
k=1025           D=3   e=1       m=2.843e+7 theta/H=0.99999999 | 905 cells: viol=0, |I|/(H(rho+a)) in [1.0,1.0], max#endpoints(N(I))=4, min|J|/w=0.999998 | densest 4H-arc of V_eta: 11933 breakpoints vs 16004D=48012 (ratio 0.249)
k=1000000        D=4   e=3       m=2.065e+14 theta/H=1.0 | 905 cells: viol=0, |I|/(H(rho+a)) in [1.0,1.0], max#endpoints(N(I))=4, min|J|/w=1.0 | densest 4H-arc of V_eta: 16001 breakpoints vs 16004D=64016 (ratio 0.250)
k=1000000000     D=8   e=1250    m=2.331e+23 theta/H=1.0 | 905 cells: viol=0, |I|/(H(rho+a)) in [1.0,1.0], max#endpoints(N(I))=4, min|J|/w=1.0 | densest 4H-arc of V_eta: 32001 breakpoints vs 16004D=128032 (ratio 0.250)
k=1000000000000  D=16  e=625000  m=2.936e+32 theta/H=1.0 | 905 cells: viol=0, |I|/(H(rho+a)) in [1.0,1.0], max#endpoints(N(I))=4, min|J|/w=1.0 | densest 4H-arc of V_eta: 64001 breakpoints vs 16004D=256064 (ratio 0.250)
[check_mesh_large: 2.41s, maxrss 48416kB]
exit=0
```

### `check_mesh_large_control.py` — Control for check_mesh_large.py with the identical checker: wrong growth rate must fail; α' = 1e-3 is expected to pass (Lemmas 2.3/2.4 use only α ≤ 1/4).

```python
# CONTROL for check_mesh_large.py: identical checker (window_check imported from it), mesh built with
# m' = ceil(k R) (theta ~ 1/k: WRONG growth rate) -- MUST report violations.
# Second run (EXPECTED TO PASS): alpha replaced by alpha' = 1e-3. Lemmas mesh:width/mesh:neighbors use only
# alpha <= 1/4; the size of alpha matters only later (dichotomy:step-lattice needs alpha <= q^-D).
import importlib.util, sys, mpmath
spec = importlib.util.spec_from_file_location("cml", "/tmp/oaimath/160/seats/setup_checks/check_mesh_large.py")
src = open("/tmp/oaimath/160/seats/setup_checks/check_mesh_large.py").read()
src = src[:src.index("for k in [1025")]          # import definitions only, not the main loop
ns = {}; exec(compile(src, "cml_defs", "exec"), ns)
for k in [1025, 10**6]:
    pr = ns['params'](k)
    bad = dict(pr); bad['m'] = int(mpmath.ceil(k*pr['R'])); bad['theta'] = pr['R']/bad['m']
    res = [ns['window_check'](bad, 0, 200, 'cut'), ns['window_check'](bad, bad['m']-200, bad['m']-1, 'zero')]
    print("CONTROL wrong growth k=%d: viol=%d (must be > 0), ratio max=%s" % (k, sum(r[1] for r in res), mpmath.nstr(max(r[3] for r in res), 5)))
    alt = dict(pr); alt['alpha'] = mpmath.mpf(1)/1000; alt['R'] = mpmath.log(1 + 1/(2*alt['alpha'])); alt['m'] = int(mpmath.ceil(mpmath.mpf(k)**2*alt['R'])); alt['theta'] = alt['R']/alt['m']
    res = [ns['window_check'](alt, 0, 200, 'cut'), ns['window_check'](alt, alt['m']-200, alt['m']-1, 'zero')]
    print("alpha'=1e-3 k=%d: viol=%d (expected 0: widths/neighbours hold for ANY alpha<=1/4)" % (k, sum(r[1] for r in res)))
```

Output (`out_check_mesh_large_control.txt`):

```
CONTROL wrong growth k=1025: viol=802 (must be > 0), ratio max=1025.5
alpha'=1e-3 k=1025: viol=0 (expected 0: widths/neighbours hold for ANY alpha<=1/4)
CONTROL wrong growth k=1000000: viol=802 (must be > 0), ratio max=1.0e+6
alpha'=1e-3 k=1000000: viol=0 (expected 0: widths/neighbours hold for ANY alpha<=1/4)
[check_mesh_large_control: 1.37s, maxrss 47948kB]
exit=0
```

## What I could not check / limits

- The finite mesh checks are exhaustive only for k ≤ 32 (D = 2); for D ≥ 3 they cover windows (905 cells per k) plus closed forms.
  The lemmas themselves are proved for all k by the line-by-line reading above; the numerics are corroboration with failing controls,
  not the proof.
- Downstream sections were read only at the interface (does each §2 lemma deliver the hypothesis its user cites). Their own arguments
  (count:local's arrangement count, the dichotomy, the LLL, the perturbation) are other seats' scope.
- No lean/lake was run. Lean files read as text: Parameters.lean, PrimeScale.lean, Dilation.lean, AdaptiveMesh.lean,
  ConstructionModel.lean, ScalarAdaptiveMesh.lean (definitions match the paper's: c = 1/100000, D = ⌈k^{1/10}⌉₊, M = ⌈k^{1/2}⌉₊,
  H = 1/k², η = 1/(1000D), λ = ∏ p^{Nat.log p (2M)} over primes ≤ D², α = 1/q^{D+1}, m = ⌈R/H⌉₊, endpoints α(exp(jθ) − 1); the
  constants 49, 1/16 and 16004·D appear verbatim in AdaptiveMesh.lean / AdaptiveMeshCounting.lean / AdaptiveMeshBreakpoints.lean). The
  only divergence found: the Lean takes P from Bertrand (P ≤ 2k) and q as some positive power of P within a factor P of the target, not
  "the least power" — both satisfy (2.4).
