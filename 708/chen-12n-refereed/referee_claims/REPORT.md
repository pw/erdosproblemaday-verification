# Hostile referee (Claude Opus 5.5 seat, 2026-11-12) — Chen's #708 claims, commit dc150fd

Brief: refute; quote objections; printed section numbers. No Lean build by this seat (another process replayed it).

**Task 1 — Barrier, Proposition 18.9: HOLDS; Remark 18.10: HOLDS WITH FIX.**
S is the atom form (§15): S(n) = Σ α_{p,j}[p^j | n]; "all weights 1" ⇒ α_{p,1} = 1, α_{p,2} = 0, so S(p²) = 1 and
squares add (1−c)^+ = 0: the stated equality is right. Exactly 21 primes in 503..641 (neighbours 499, 643);
641/503 = 1.2744 < √2; m = 631·641 = 404471; I = [P−202235, P+202235]. Direct enumeration at c = 19/10: [1,m] has
14398 points with S = 1 and 210 with S = 2 ⇒ left = 21 = C(21,2)/10; in the window only P has S ≥ 2, S(P) = 21 ⇒ right
= 20; 21 > 20, the S-form fails as claimed.
OBJECTION: Remark 18.10 (sec_h883.tex l.179–181, also l.6–8): "Proposition 18.9 shows that the hinge inequality
itself cannot go below c=2, so the present route cannot give a bound below 4n". The route applies the bound to w_z:
"Σ_a w_z(a) ≤ cn+Σ_{k≤m}(w_z(k)−c)^+ ≤ …" (sec_chain19.tex l.66–69); the Lean hypothesis of
`bound_of_hinge`/`g_le_12n_of_hinge` is `hingeSum (w z) c 0 m ≤ hingeSum (w z) 1 x m`; Conjecture 8.1 is in w_z form.
In w_z form squares count: on the paper's instance left = (210+20)/10 = 23, right = 46 — it does not refute the
inequality the route uses. FIX (exact): 60 consecutive primes 1049..1483 (1483/1049 = 1.4137 < √2), m = 2196323,
window centred at P: w_z form 1829/10 = 182.9 > 145 (S-form 177 > 59). Conclusion survives; restate with ≥ ~60 primes.

**Task 2 — Theorem 1.3 (§5, Lemmas 5.1–5.2), 2n when a_n ≥ 8n³: HOLDS.** C = m/(2n) gives C ≥ m^{2/3}, C² ≥ m,
C ≥ 4n²; packing/split and per-prime bookkeeping sound. Lean: `Covers D B := B ⊆ Icc (x+1) (x+m) ∧ ∏A ∣ ∏B`
(m = A.max', n = A.card, A ⊆ ℕ_{≥2}); `long_interval` states exactly the theorem. In the FinalCheck closure (180
project modules; none contains sorry / native_decide / axiom / extern) on the path Final.g_le_81n → linear_bound →
conditional_81 → long_interval; `reference_g_le_12` does not use it (bound_of_hinge uses ksplit3).
Brute force (own exact DP, witnesses re-checked ∏B mod ∏A = 0): n=2, 2500 instances (a_n 64..2000; x up to 10^15 and
near multiples of lcm): worst 2. n=3, 1500 instances (a_n 216..3000): worst 3; 55 adversarial ES pair-product instances
with a_n ≥ 216: worst 4. None above 2n. Controls: agrees with subset enumeration on 400 tiny cases; reproduces Prop 7.1's
5 and 6 and Prop 16.7's 2. (A random short-interval mutation test gave 0 failures — weak; the targeted controls carry it.)

**Task 3 — statement audit: HOLDS.** `g_le c`: ∀ Finset A ⊆ ℕ, (∀a, 2 ≤ a), M ∈ A, ∀a ≤ M, ∀ x : ℕ, ∃ B ⊆ Icc(x+1)(x+M),
|B| ≤ c·|A| ∧ ∏A ∣ ∏B. Sceptic's flags: x ∈ ℕ only (windows containing 0 trivial; negative windows reflect — not in
Lean); abstract says "some g", Lean uses ≤ (intro l.88–90 adopts "at most"; exact reading impossible when a_n < 12n);
toolchain v4.34.0-rc1. `reference_g_le_12` only rewrites A.max' = M. Chain: hinge97 → weighted_hinge97 (atoms → capped →
weighted via the peel) → g_le_12n_of_hinge → g_le_12n. The 11n results are conditional on the unproved Hinge883.

**Task 4 — §17 exact recomputation: HOLDS.** λ(1−2ΓH*/K) = 718539/573440 exactly (excess 1739/573440 over 5/4);
D0+ρT = 97/10; λ·19/100 = 969/1000. All 29 scales of Lemma 17.9 from the printed formulas: A_{4,4} = 0.024679503;
per-L sums (8…512) 0.128710365, 0.025772699, 0.005664228, 0.001024465, 0.000149657, 0.000020676, 0.000002410, each
below the paper's bound; total ∈ [186024001631, 186024001632]·10⁻¹² < 187/1000.

Scripts/logs in this folder (barrier*.py, longcheck*.py, imports.py + finalcheck_closure.txt, h97_scales.py).
