# Seat T — §§3–5: Theorem 3.1 (triangle mass from cross mass): Lemmas 3.2, 3.3, 4.1, 5.1, 5.2, 5.3, Proposition 5.4, proof of Theorem 3.1, (5.10)
Read /tmp/oaimath/184/seats/COMMON.md first. Report: /tmp/oaimath/184/seats/T_report.md. Work dir: /tmp/oaimath/184/seats/T_work/.
This is the new heart of the proof. Attack it hardest.
1. Lemma 3.2 (preservation under maps injective on directed edges) and Lemma 3.3 (peeling, (3.2)–(3.4), s_u ≥ τ, h_u ≥ τ s_u): every claim.
2. Lemma 4.1: kernels P_u, Q_u, K_u^j = P_u Q_u^j; reversibility w.r.t. π_u; the density bound (4.5); the sets S_i(v) and the weight bound
   w(S_R) ≤ e^{20x²}; the claim (4.8) by induction (is the "x w_z" bound for K^i(v,z) used for z inside N(u) only? does the step sum really give ≤ x^{-4}?);
   the two uses of (3.1) (parameters 20x² and x — are both sets' weights ≤ e^{parameter}?); the bound (4.9) (does e^{-x} ≤ x^{-7} hold for x ≥ 32?);
   H_R ≤ A_C log x; the entropy-increment identity (4.11) and why stationarity of π_u under Q_u makes the average telescope; the TV bound and the passage
   from μQ to the ordered triangle law (the claimed EXACT identity). Check that a single index j works for all u simultaneously.
3. Lemma 5.1 (shared rejection sampling) incl. the disagreement bound and finite support.
4. Lemma 5.2: the law identity (u,v,y) = (u,y,v), E ℓ = H_j, ℓ ≥ −log x, Markov on ℓ + log x, and H_j ≤ A_C log x for the j chosen.
5. Lemma 5.3: the construction of H′ — is it a SIMPLE graph? Are groups well defined when Y_{u,v} is inadmissible? the neighbourhood bound (5.2)/(5.4);
   the triangle-survival characterization (necessary AND sufficient); the union bound (three corners + six incidences) and a_C = 6(B_C + A_C + 1);
   "some label vector has triangle mass ≥ its expectation".
6. Proposition 5.4 and the iteration proving Theorem 3.1: is X(C) well defined by (5.6) (log X/√X decreasing for X ≥ e²)? (5.8) when H has no edges;
   the factor (1 − a_C log x/√x) ∈ [0,1]; the geometric sums (5.9) with x_{i+1} = √x_i; the displayed iterate "T_k ≥ …" — check whether the PRINTED
   intermediate expression is exactly what iterating (5.8) gives, or only a weaker/stronger form (an EXPOSITION-level slip is still worth recording;
   say whether the final ½T_0 − M_0 survives); 3T_k ≤ e^X M_k; C_△(C) = 2(1 + e^{X(C)}/3).
7. NUMERICS: build random small weighted graphs satisfying the hypotheses loosely (you cannot verify (3.1) for all x cheaply — instead check the
   mechanical lemmas): reversibility, (4.5), monotonicity H_0 ≤ H_1 ≤ … (4.6)/(4.11) exactly, the identity in Lemma 5.2 E ℓ = H_j, Lemma 5.1's bound by
   simulation, and the exact μP vs μQ identity used at the end of §4. A counterexample to ANY displayed identity is the prize.
8. Is anything here circular with §2 (e.g. does Theorem 3.1 secretly need the maximizer equations after splitting)? The paper says no — confirm.
