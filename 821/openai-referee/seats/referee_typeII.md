# Referee report, seat typeII: Section 6 (PDF pp. 45–53), the Type II estimate (Theorem 6.1)

Reader: Claude (Opus 5.5), hostile seat. I read Section 6 from the rendered PDF pages 44–53, and the Theorem 5.1 statement and (5.1)–(5.5) from pp. 35–36. I also read §1–2 (architecture, Convention 2.1, Lemmas 2.5 and 2.8) and the parts of §7 that fix b_*, j** and apply Theorem 6.1 (pp. 53, 56, 60–61).
Scratch scripts are in /tmp/oaimath/011/work_typeII/ (bij.py, part.py, aq.py), all run at nice 19.

## Verdict for this scope

**HOLDS AS READ, conditional on Theorem 5.1 exactly as stated.** I checked Section 6 line by line, including every step the brief lists. Its reduction of Theorem 6.1 to Theorem 5.1 is correct:

- The weight bounds (6.4) hold.
- The Rankin discard (6.6) holds.
- The slot-allocation induction and (6.7) hold.
- The Fourier separations hold.
- Cauchy–Schwarz in (e,n) and the diagonal bound (6.14) hold.
- The determinant parametrization (6.15)–(6.20) is a genuine bijection under the stated conditions.
- The endpoint identification (6.22)–(6.23) is exact.

The off-diagonal lands inside Theorem 5.1's hypotheses for every k with 0 < |k| ≤ c·L^{K0+Cs}, of either sign. The discrepancy-bearing first endpoint F_0 is built from the original α, with its restriction m ≍ U. β is removed by Cauchy–Schwarz before any correlation is formed. The residual c_r enters only through Theorem 5.1's bounded-c_r slot, which needs no hypothesis on c_r.

No step needs discrepancy of β or of c_r. I found nothing FATAL and no mathematical GAP in Section 6. The objections below are COSMETIC or UNCLEAR (exposition).

**What I could not check:** whether Theorem 5.1 is true (other seats). Section 6 transfers essentially all of the parity-breaking content of Theorem 6.1 onto Theorem 5.1; see Remark R1.

---

## Answer to the seat's main question

**Q1. Does the Cauchy–Schwarz in (e,n) pay for the diagonal, with constants independent of K_0?**

Yes. Written out:

    |B_0| ≤ ( Σ_{e∈[EL^{-Cs},E], n≍V} |a_e(e)|²|β_n|² )^{1/2} ( Σ_{e,n} η_e(e/E)η_n(n/V) |S(e,n)|² )^{1/2},
    S(e,n) = Σ_{m≍U, h≥1, mn=2eh+1} α_m a_h(h).

- The first factor is ≤ 2E · O(V) · L^{2C_a+2C}, so C_3 = 2C_a + 2C + O(1). This uses η ≥ 1 on the original ranges and η ≥ 0 elsewhere.
- On the diagonal, m = m' forces h = h', since mn = 2eh+1 = 2eh'+1.
- Fix v = mn. There are at most τ(v) pairs (m,n), and e runs over divisors of w = (v−1)/2. The sum is Σ_{e|w} τ(w/e)² = Σ_{d|w} τ(d)² ≤ τ(w)³ ≤ τ(v−1)³.
- With |a_h(h)|² ≤ L^{O(1)} τ(h)², |α|² ≤ L^{2C}, Cauchy and Lemma 2.5 give 𝒩_diag ≪ x L^{C_5}.

The constants C_3, C_4 (= C_s from the rescaled lower edge of η_e), C_5, C_a, C_f and C_F depend only on C, Ψ, the group data and the band data. None depends on K_0.

The diagonal's contribution to |B_0| is x·L^{(−K0+C3+C5)/2}. After multiplying by L^{C_f}, this is ≤ x L^{−D*−1} as soon as

    K_0 ≥ C_3 + C_5 + 2C_f + 2D_* + 2.

There is no cycle.

**Q2. Does the off-diagonal land in Theorem 5.1 for every k?**

Yes. For each k with 0 < |k| ≤ c·L^{K0+Cs}, each character χ mod 2|k| and each truncated frequency vector:

- **Character modulus:** 2|k| ≤ L^{K0+Cs+1}. Both m and m' are odd and W-rough with W = exp(√L) > 2|k|, so they are units mod 2|k|. Hence (6.19) is exact orthogonality.
- **Range of Z:** z = m'h ∈ [c·x·L^{K0}, c·x·L^{K0+Cs}], within x·L^{±C} for C ≥ K_0 + C_s + O(1).
- **Frequencies:** a_1 = ϱ + ξ_3 and a_2 = −ϱ, with |ϱ| ≤ L and |ξ_i| ≤ P·L = L^{C8+1}.
- **Endpoint twists:** σ_0 = ϱ − ξ_2 for F_0 and ξ_1 + ϱ for G_0. The σ_1 slot holds −σ, which is in fact 0 (Objection 2). The residual |c_r| ≤ L^{C_a}.
- **Rough-integer interval:** I_** = [x^{τ*}, x^{η*}] with 0 < τ_* < η_* < b_*/4 ≤ 1/8.
- **Cutoff:** ψ̃_Z(t) = tψ_Z(t), a fixed bump.

Negative k is allowed by Theorem 5.1, and its sum over "z > 0, z+k > 0" is exactly h ≥ 1, h' ≥ 1 (since h = z/m' with m' | z).

The endpoint built from α_{m'} sits at z and appears conjugated, as F_0 must. Its sequence is α·1_{m≍U}, exactly the "restricted sequence" for which Theorem 6.1 assumes the discrepancy condition.

The second endpoint G_0 is also built from α, not β. So even a weaker Theorem 5.1, requiring discrepancy at both endpoints, would suffice here. Section 6 does not exploit the "arbitrary second endpoint" freedom at all.

---

## Objections

**1. COSMETIC. Wrong labels for internal results** (§6.3 p.49, §6.4 p.50, §6.6 pp.51–52).
- Quoted: "by Cauchy's inequality and Theorem 2.5."; "Collecting by v = mn and using Theorem 2.5, we obtain"; "This uses only Theorem 2.5."; "Fourier inversion, as in Theorem 2.8, consequently represents this cutoff".
- The paper has no Theorem 2.5 or Theorem 2.8. These are Lemma 2.5 (fixed divisor moments) and Lemma 2.8 (Fourier separation).
- The uses match those lemmas' statements: Σ_{n≤Y} τ(n)^k ≪ Y(log 2Y)^{C_k}, and smooth separation with derivative bounds C_j·L^{C(j+1)}.
- Fix: relabel.

**2. COSMETIC. A twist on the exceptional slot with no source** ((6.12), p.49).
- Quoted: "H(t) = Σ_{pr=t} 1_{p∈I∗∗, P−(p)>W} p^{iσ} c_r".
- The exceptional slot is never processed: "Allocate all of u_P and the exceptional integer slot to h." So (6.9) assigns it no σ_t.
- Its only phase comes from h^{iϱ}, which (6.12) already factors out as "a_h(h) = h^{iϱ} W_ℓ(h)H(h_*)". So σ = 0 here.
- Harmless: (5.3) allows p^{iσ_1} with any |σ_1| ≤ L^C, including 0.
- Fix: set σ = 0 or say it is a dummy.

**3. COSMETIC. What "good" refers to** (§6.2 p.47 and §6.3 p.48).
- Quoted: "Call the remaining slot tuples good." and "On a good tuple the factors assigned to h before the procedure starts have product at most x^{b∗/2}."
- Goodness is the condition u_P ≤ x^{b*/4} on the group part of u, not a property of the slot tuple. It should read "pairs (u_P, slot list)".
- The x^{b*/2} needs two inputs: goodness (u_P ≤ x^{b*/4}) and the hypothesis η_* < b_*/4 (exceptional integer ≤ x^{η*} < x^{b*/4}). The second is used silently.
- Verified: x^{b*/4} · x^{η*} < x^{b*/2}, so the available prime-slot logarithm is ≥ (1 − b_*/2)L + O(1) > log E.
- This also answers the brief's question of why b_*/2 when §6.2 discards only u_P > x^{b*/4}: the exceptional integer supplies the other x^{b*/4}.

**4. UNCLEAR (exposition, not a gap in §6). Uniformity of Theorem 5.1 in k and Z** (p.36 versus §6.6 p.52).
- Theorem 5.1 says: "The bound is uniform over the indicated sequences, intervals, characters, frequencies, and cutoffs."
- Section 6 sums that bound over about L^{K0+Cs} shifts k and O(T) dyads Z: "Consequently each separated unweighted correlation is O(ZL^{−D0})".
- This needs the implied constant in (5.5) to be uniform over 0 < |k| ≤ L^C and xL^{−C} ≤ Z ≤ xL^C. Both are quantified in the hypothesis ("Suppose 0 < |k| ≤ L^C is integral, xL^{−C} ≤ Z ≤ xL^C"), so uniformity is the natural reading, but k and Z are missing from the uniformity list.
- Fix: add "shifts and scales" to that sentence. Whether §5's proof is uniform in k (for example in the comparison shifts kD_AD_B and the arc parameters) is for the §5 seat.

**5. COSMETIC. Notation collisions.**
- N denotes the number of processed slots in §6.3, N = 2R in §3, and the Cauchy sum 𝒩 in §6.4.
- C_0 is the tilted per-group constant in §6.2 and also the group-count constant in Definition 3.1.
- P = L^{C8} in §6.6 sits beside 𝒫 (the group primes).
- "Theorem 3.11" in §5.2 is presumably Corollary 3.11 (outside my scope).
- None of these causes a mathematical error.

**6. COSMETIC. Theorem 6.1's statement versus the brief's paraphrase.**
- §6.1 uses s_j = s'Lλ^{−j} with general λ > 1, with (6.1) reading (r_0−1)c_1/λ ≥ c_2 + 1, and assumes c_2 s' < 1/4.
- §7 specialises to λ = 2, c_1 = 1, c_2 = 6/5, s' = 1/(r_0(c_1+c_2)), with (7.1) ≡ (6.1) at λ = 2 and c_2 s' < δ < 1/4. These are consistent.
- In §7, c_− = 20 and c_+ = 40, from j_x = the largest j with c_1 s_j ≥ 20T. So C_s = (c_2+1)c_+ = 88 is fixed.

No objection reaches GAP or FATAL.

---

## Remarks (context, not objections)

**R1. Where the strength lives.**
- β is arbitrary, so Theorem 6.1 is equivalent to Σ_{n≍V} |Σ_{m≍U} A((mn−1)/2) Ψ(·) α_m| ≪ x L^{−D*} (take β_n = sgn of the inner sum).
- Formally, with α = λ·1_{P⁻>W}·1_{[U,2U)} and β = λ·1_{[V,2V)}, it would give cancellation in Σ_u A(u)Ψ(u/x) λ(2u+1) #{m | 2u+1 : m ∈ [U,2U), P⁻(m) > W, (2u+1)/m ≍ V}. That is a Chowla-type (parity-sensitive) statement along the sequence 2u+1. This assumes λ·1_{P⁻>W} satisfies (5.4) at the required level B, which I expect from Siegel–Walfisz-type input but did not prove.
- Section 6 converts this into Theorem 5.1 faithfully, so all of the parity-breaking content must come from Theorem 5.1. In the application each endpoint carries an unsigned long W-rough factor 1_{p∈I**} (σ = 0, Objection 2), and that factor is what §5 uses on the major arcs. So Theorem 5.1 is not directly a two-point Chowla statement for λ.
- For calibration: Pilatte (arXiv:2310.19357v3, abstract, read from the local copy) proves Σ_{n≤x} λ(n)λ(n+1)/n ≪ (log x)^{1−c} and says this "appears to be best possible with current methods". Theorem 5.1 claims an arbitrary power-of-log saving per dyad for its marked, convolution-shaped correlations.
- I could not build α satisfying (5.4) together with a β that defeats Theorem 6.1. Characters of polylog conductor q > L^B on m with β = χ̄ or χ are killed by the equidistribution of u mod q through its large slot primes, so they are not counterexamples. Refuting Theorem 6.1 means refuting Theorem 5.1.

**R2. Where the coprimality in the converse comes from.**
- My toy check (bij.py; e, n < 60; |k| ≤ 20) shows that without roughness the forward map does produce gcd(m,k) > 1: 108,900 of 654,584 tuples. Example: e = n = 1, m = 3, m' = 9, h = 1, h' = 4, k = 3.
- Dropping gcd(m,k) = 1 in the converse produces 209,357 tuples with m ∤ 2eh+1.
- With gcd(m,k) = 1, all 177,452 tuples were recovered, with 0 failures.
- In the paper, P⁻(m) > W > c·L^{K0+Cs} ≥ |k| makes the coprimality automatic in both directions. The paper's sentence "The coprimality (m, k) = 1 is necessary to this converse" is correct.
- Shifts too large for W-roughness to give coprimality (|k| > W) would make e < U/W < ½EL^{−Cs}, so η_e kills them. Restricting to the range (6.17) is legitimate.

---

## Line-by-line checks (the deliverable)

**Verified line by line, with recomputation:**

1. **(6.3)–(6.4).**
   - The exceptional slot is one fixed position, so a list determines its entry p, and #lists(v) = Σ_{p|v, p∈I**, P⁻(p)>W} #(prime-slot lists of v/p).
   - The bands are disjoint, so v/p fixes the multiset per band. The orderings number at most r_0!/Π mult! ≤ r_0! per band, and (r_0−1)! for band j**.
   - Hence a_Q(v) ≤ τ(v)·Π_j(r_0!)/Π_j(r_0!) · (1/r_0) ≤ τ(v)/r_0 ≤ τ(v).
   - Toy check (aq.py): the maximum of a_Q/τ over 3000 random products was 0.0033.
   - Harmonic sum: Π_j (1/r_0!)(Σ_{Q_j} 1/p)^{r_0}, with one slot replaced by Σ_{n∈I**, W-rough} 1/n ≤ η_*L + 1. That gives O(1)^{O(T)} · O(L) = L^{O(1)}.
   - W_ℓ ≤ L^{O(1)} since sup_{t≥ℓ} q^{t−ℓ}(t)_ℓ/v_−^ℓ < ∞ (q < 1) over O(T) groups.
   - j_x = (log(L/T) + O(1))/log λ = O(T), so (r_0!)^{jx+1} and (2C_F)^N are fixed powers of L.
2. **Theorem 6.1's statement.**
   - Ranges: log E > 0 needs U ≥ x^{b*}; the initial bound needs U ≤ x^{1−b*}.
   - η_* < b_*/4 is used exactly twice: in the initial bound, and for η < 1/4 in (5.3).
   - The discrepancy hypothesis on the restricted sequence matches (5.4) verbatim, with t ↔ u.
   - There is indeed no hypothesis on β.
   - §7 numerics:
     - (7.10) imposes c_2 s' 2^{−j**} < b_*/4 by taking j** large after b_1.
     - Example: δ = 0.1, r_0 = 6, b_1 = 0.01, j** = 7 gives τ_* ≈ 5.9e−4, η_* ≈ 7.1e−4 < b_*/4 ≈ 8.3e−4 < 1/4.
     - In §7.5 the dyads are p ≥ x^{b1} ≥ x^{b*} and m ≤ x^{1−b1}, which are within [x^{b*}, x^{1−b*}].
3. **§6.2.**
   - The tilted per-group identity: Σ_S q^{|S|−ℓ}(|S|)_ℓ Π_{p∈S} a_p = Π_p(1+qa_p) · Σ_{distinct ordered} Π a_{p_i}/(1+qa_{p_i}), with a_p = Σ_{k≥1} p^{−k(1−θ)} = (p^{1−θ}−1)^{−1}. Re-derived.
   - p^θ ≤ e because log p ≤ L^d, so a_p ≤ 2e/p.
   - The bound is ≤ e^{2eq·v_+}(2e·v_+)^ℓ =: C_0. Rankin with x^{θb*/4} = exp(¼b_* L^{1−d}).
   - The W-rough divisor count is ≤ 2^{Ω(W-rough part)} ≤ 2^{log(2u+1)/log W}.
   - Σ_{u≍x} ≤ 2x Σ_u (·)/u, with u_P and u_* factoring.
   - 1 − d > 0.53 > 1/2. The final bound holds.
4. **§6.3 induction.**
   - Initial bound: shown above.
   - A take step needs γ > 0, i.e. R_i > v_i.
   - A skip step needs γ < 1, i.e. R_i < v_i + s_{j(i)} ≤ (c_2+1)s_{j(i)}.
   - A later band holds ≥ r_0 − 1 prime slots of logarithm ≥ c_1 s_{j(i)}/λ each, totalling ≥ (c_2+1)s_{j(i)} by (6.1).
   - In the final band the terminal allowance applies.
   - Hence 0 ≤ log E − log e ≤ (c_2+1)s_{jx} ≤ C_s·T.
   - On good tuples R_i/s_{j(i)} ≤ r_0c_2λ/(λ−1) + c_2 + 1 (= 16.6 with §7 constants).
   - Simulation (part.py): 4000 random tuples with §7 constants, L ∈ {1e4,…,1e8}, random, always-take and always-skip choices on 0 < γ < 1. Zero violations. The maximum of (log E − log e)/((c_2+1)s_{jx}) was 0.964 and the maximum R_i/s_{j(i)} was 13.5.
5. **Smooth transitions.**
   - f_1 = ργ and f_0 = ρ(1−γ). On a good tuple every positive-weight prefix keeps the arguments where ρ = 1, so the branch sum telescopes to 1.
   - On other tuples the branch mass is ≤ Π ρ ≤ 1.
   - The sharp indicator of (6.7) is redundant on good tuples. Elsewhere it is absorbed into the (6.6) error by absolute values.
6. **(6.9).**
   - Re-derived: Π_i exp(iξ_i(R_i − v_i)/s_{j(i)}) = exp(i log E Σ ξ_i/s_{j(i)}) · Π_t p_t^{iσ_t}, with σ_t as displayed.
   - Σ_i 1/s_{j(i)} ≤ r_0λ/((λ−1)c_−T), so |σ_t| ≪ L/T.
   - Truncation error 2^N N C_M C_F^{N−1} L^{−M}, with 2^N C_F^N = L^{O(1)} (N = O(T)).
7. **(6.10).** A(u) ≤ L^{C'_A}τ(u); at most τ(2u+1) pairs (m,n); then Cauchy and Lemma 2.5.
8. **(6.11)–(6.12).** I re-derived the factorisation of each pattern into a_e(e) and a_h(h) = h^{iϱ}W_ℓ(h)H(h_*). The coefficient bounds, (eh)_* = eh_* and W_ℓ(eh) = W_ℓ(h) hold: e consists of band primes only, and shared primes between e and h are harmless. h_P is unrestricted after extending back to all tuples, which gives exact invariance under multiplication by group primes.
9. **(6.13)–(6.14).** As in Q1.
10. **§6.5.** Re-derived: 2e | m' − m (n is a unit mod 2e), h' − h = kn, mh' − m'h = k(mn − 2eh) = k, and (6.17).
    - Converse: e = (m'−m)/(2k) is a positive integer; (6.18) m(h'−h) = k(2eh+1); (m,k) = 1 for large x; n = (2eh+1)/m; m'n = 2eh'+1.
    - The two maps are mutually inverse (both compositions checked), so it is a bijection between
      - {(e,n,m,m',h,h') : all ≥ 1, the two equations hold, m ≠ m', m and m' W-rough}, and
      - {(k,m,m',h,h') : k ≠ 0, mh' − m'h = k, m' ≡ m (mod 2|k|), (m'−m)/(2k) > 0, all ≥ 1, W-rough},
      when |k| < W, which the η_e support enforces.
    - e ≥ 1 is forced. k < 0 corresponds to m' < m. h, h' ≥ 1 is equivalent to z, z+k > 0.
    - Toy-verified (R2). (6.19) and (6.20) re-derived.
11. **§6.6 derivatives.**
    - e/E = U(e^{t2} − e^{t1})/(2kE), so every derivative is O(U/(|k|E)) ≤ O(L^{K0}).
    - n/V = Z e^{t3}(e^{−t1} − e^{−t2})/(kUV) + e^{−t1}/(UV), so derivatives are O(Z/(|k|UV) + (UV)^{−1}).
    - Chain rule: C_7 = C_4 + max(K_0, C_6) + O(1). Then P = L^{2C7} and |F̂(ξ)| ≪_j (1+|ξ|/P)^{−j}.
    - ∫|F̂| ≪ P³ and ∫_{|ξ|>PL} |F̂| ≪ P^j(PL)^{3−j} = P³L^{3−j}, so j > A + 3C_8 + 3 suffices.
12. **Absolute-control paragraph.** The triple-convolution count is ≤ τ(z_*)², and Σ τ^4 W_ℓ² ≪ ZL^{O(1)}. The 1/φ(q_k) character average does not inflate the bound.
13. **Endpoint identification (6.22)–(6.23), by direct substitution.**
    - At z = m'h: Σ_{m'h=z} ᾱ_{m'} χ̄(m') m'^{iξ2} a_h(h) = z^{iϱ} W_ℓ(z) · Σ_{m'pr=z_*} ᾱ_{m'} χ̄(m') m'^{i(ξ2−ϱ)} 1_p p^{iσ} c_r = z^{iϱ} W_ℓ(z) · conj(F_0(z)).
    - At z+k = mh': Σ α_m χ(m) m^{iξ1} conj(a_h(h')) = (z+k)^{−iϱ} W_ℓ(z+k) G_0(z+k).
    - Together with z^{iξ3} from the Fourier factor, the summand is ψ_Z(z/Z) z^{i(ϱ+ξ3)} (z+k)^{−iϱ} conj(F_0(z)) G_0(z+k) W_ℓ(z) W_ℓ(z+k), up to the unimodular phases U^{−iξ1}, U^{−iξ2}, Z^{−iξ3} and the E-phase. This matches the paper's formula.
    - The coupling between the two sides was only through the congruence and the cutoffs, both now separated, so the z and z+k factors are independent sums.
    - Both endpoints are invariant (they depend on v_* only) and have exactly the form (5.3).
14. **Final normalisation.** Σ ψ_Z(z/Z)(…) = Z Σ ψ̃_Z(z/Z)(…)/z. The bookkeeping is N_off ≪ L^{K0+Cs} · T · L^{3C8} · xL^{C6} · L^{−D0}. Choosing D_0 after (K_0, C_s, C_6, C_8, A) gives O(xL^{−A}). Then |B_0| ≪ xL^{−D*−Cf−1} and (6.5) follows.
15. **Remark 6.2's order** (table below): no cycle. B depends on K_0 through Theorem 5.1's C ≥ max(K_0 + C_s + 1, C_6, C_8 + 2, C_a, C), and K_0 does not depend on B.

**Skimmed or not checked:**
- The proof of Theorem 5.1 (§§3–5, other seats). I took Theorem 5.1 as stated.
- §7's verification that α = I_γ − B_γ satisfies the restricted discrepancy hypothesis (Theorem 7.3).
- Whether Theorem 5.1's implied constant is uniform in k and Z (Objection 4).
- The constants in Lemma 2.5 itself. Its proof is standard and was read but not re-derived.

---

## Citation table (Section 6)

Section 6 cites no external result. Its internal dependencies:

| Cited | Paper's use in §6 | What the cited statement says | Status |
|---|---|---|---|
| "Theorem 2.5" (p.6 Lemma 2.5) | Σ_{u≍x} τ(u)τ(2u+1), Σ τ(v)τ(v−1)³, Σ τ(z_*)^4 ≪ xL^{O(1)} | "Σ_{n≤Y} τ(n)^k ≪_k Y(log(2Y))^{C_k}" | MATCH (label wrong: Lemma) |
| "Theorem 2.8" (p.7 Lemma 2.8) | Fourier separation of the localized cutoff in (t1,t2,t3) | "F smooth, supported in a fixed bounded box… derivatives of order j bounded by C_j L^{C(j+1)}… restricting each Fourier frequency to … L^{C'} leaves an error O_A(L^{−A})" | MATCH; §6.6 also gives its own explicit tail (verified) |
| Theorem 5.1 / (5.3)–(5.5) (pp.35–36) | Applied to each (k, χ, ξ, Z) | (5.3): F_0(n) = Σ_{mpr=n_*} α_m χ_0(m) m^{iσ0} 1_{p∈I_p, P⁻(p)>W} p^{iσ1} c_r, with \|α\|,\|c\| ≤ L^C, α W-rough, I_p ⊂ [x^τ, x^η], 0 < τ < η < 1/4, mod χ_0 ≤ L^C, \|σ_i\| ≤ L^C; "(5.4) on the α of at least the first endpoint"; (5.5) with conj(F_0(z)) G_0(z+k) W_ℓ W_ℓ, 0 < \|k\| ≤ L^C, xL^{−C} ≤ Z ≤ xL^C, \|a_i\| ≤ L^C | MATCH on every hypothesis (see Q2); k- and Z-uniformity implicit (Obj. 4) |
| Theorem 6.1 hypothesis on α versus (5.4) | identical | "Σ_{m∈I} α_m χ(m) m^{it}/m ≤ L^{−B} (I ⊂ [1,x²], mod(χ) ≤ L^B, \|t\| ≤ L^B)" | MATCH |
| Pilatte 2310.19357v3 (context only, R1) | not cited in §6 | abstract: "Σ_{n≤x} (1/n) λ(n)λ(n+1) ≪ (log x)^{1−c} … best possible with current methods" | read from local copy refs/Pilatte |

---

## Parameter-dependency table (Section 6)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Verified |
|---|---|---|---|---|---|
| a,b,c,d, v_±, q, ℓ, group counts | §3/§5 data, first | none | W_ℓ, (6.6), Thm 5.1 | x | yes |
| c_1,c_2,s',λ,c_±,r_0 | §6.1 (§7: λ=2, c_1=1, c_2=6/5, c_−=20, c_+=40), first | δ (via c_2 s' < δ) | bands, (6.1), C_s | x, K_0 | yes |
| j**, τ_*, η_* | first (§7: after b_1, (7.10)) | b_*, band data | I_**, τ and η of Thm 5.1 | K_0 | yes |
| b_* | first (§7: b_1/3) | b_1 | ranges, discard x^{b*/4}, η_* < b_*/4 | K_0 | yes |
| C, D_*, Ψ | first | none | coefficient bound, target | K_0 | yes |
| C'_A | (6.4) | group and band data | (6.4), (6.10) | K_0 | yes |
| θ = L^{−d}, C_0, C_1, C_2 | §6.2 | d, q, ℓ, v_±, C, C'_A | discard | splitting precision, K_0 | yes |
| γ, ρ, C_F | §6.3 | band data (ρ's support ⊂ [−c_2, r_0c_2λ/(λ−1)+c_2+1]) | transitions | K_0 | yes |
| C_s = (c_2+1)c_+ | §6.3 | c_2, c_+ | e range, k range, η_e edge | K_0 | yes |
| M (truncation) | §6.3 | target saving | error terms | K_0 | yes |
| C_f, C_a | (6.11)–(6.12) | C_F, r_0, λ, c_−, Ψ | expansion mass, coefficients | K_0 | yes |
| C_3, C_4, C_5 | §6.4 | C, C_a, C_s, divisor moments | (6.13)–(6.14) | K_0 | yes |
| K_0 | §6.4, after the above | ≥ C_3 + C_5 + 2C_f + 2D_* + 2 | E = UL^{−K0} | none required | yes |
| k range, q_k | §6.5 | K_0, C_s | Thm 5.1 modulus and shift | none | yes |
| C_6 | §6.6 | K_0, C_s | Z range | allowed to depend on K_0 | yes |
| C_7, C_8 (P = L^{C8}) | §6.6 | C_4, K_0, C_6 | Fourier tails, frequencies ≤ L^{C8+1} | allowed to depend on K_0 | yes |
| D_0 | §6.6, after K_0, C_6, C_8, A | all of the above | Thm 5.1 saving | none | yes |
| C (in Thm 5.1) | §6.6 | max(C, C_a, K_0+C_s+1, C_6, C_8+2) | Thm 5.1 input | none | yes |
| B | last | D_0, C (Thm 5.1), τ_*, η_*, group data | discrepancy hypothesis | not S (cell precision) | consistent with Remark 6.2 |
| S (cell precision, §7) | after B | none in §6 | proxies | B, K_0 (needs proxy coefficient bound uniform in S) | consistent; §7's job |

No cycle. Every constant claimed independent of K_0 (C_3, C_4, C_5, C_f, C_a, C_s, C_F, the ρ range) is independent of K_0 on inspection. No J appears in Section 6.

---

## Hedge-word census, Section 6

"For completeness" (§6.6 derivative regularity) was checked; "Direct substitution" (endpoint identification) was checked; "The same estimate applies" (uniform transition and cutoff errors) was checked. The 12 instances of "hence/therefore/consequently" were all followed and hold.
