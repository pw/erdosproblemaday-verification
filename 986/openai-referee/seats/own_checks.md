# Own checks — 12:00Z erdos seat (orchestrator), 2026-10-20

## Paper A, Lemma stream-entropy (flags-entropy.tex) — HOLDS AS READ
max atom ≤ 2C0·C(N,ℓ)/M^ℓ (union bound over ℓ position sets × 2 orientations; iid probability M^{-ℓ} for any fixed positions even with repeats).
H ≥ ℓ log M − ℓ log(eN/ℓ) − O(1). log M = 7σ + O(1/q); log(eN/ℓ) = 1 + 4σ + log σ − log ℓ, log ℓ = σ + (1+η) log σ + O(1) for c0k ≤ ℓ ≤ C1k
⇒ log(eN/ℓ) = 3σ − η log σ + O(1) ⇒ H ≥ 4σℓ + ηℓ log σ − O(ℓ). ✓ (paper B: dσ in place of 4σ, log M = (2d−1)σ.)
Conditioning on an event of prob ≥ c: density ≤ C0/c — preserved. ✓

## Paper A, Lemma marking, deficit budget (compression-local.tex eq deficit-budget) — HOLDS AS READ
E H(F_cheap) = H(F|C,Ω) ≥ H(F) − Λ − H(Ω|C); with J0 = 4σ + O(1) and H(Ω|C) ≤ O(k) + (4σ+Δ+O(1))E h:
E[(ℓ−h)J0 − H(F_cheap)] ≤ O(ℓ) − ηℓ log σ + Λ + O(k) + (Δ + O(1)) E h ≤ C(Λ + k + Δqσ) (E h ≤ Cqσ). The −ηℓ log σ is discarded (upper bound). ✓
Update count: |U_l^0| ≤ Q4, each update multiplies by ≤ 1 − 1/(80q) ⇒ ≤ 80q·log Q4 = O(qσ) per l, five l. ✓

## Paper B, §6.1 bounded iteration (06-conclusion.tex end:one-step-budget … end:final-budgets) — HOLDS AS READ (given Lemma comp:step)
Λ0=0, Δ0=(d−1)σ ⇒ D0 = σ^β(1+(d−1)σ^{1−η}) = O(σ^{1−η+β}) ∈ [σ^β, σ^{1−η/2}] ✓.
P = LR ≤ Dσ^{8β}(2σ^β+2) ≤ 4Dσ^{9β} ✓. qPσ/k ≤ CDσ^{9β−η}; qP²w/k ≤ CDσ^{18β−η/2} using w ≤ Cσ^{1+η/2}/D; wσ/k ≤ Cσ^{1−η/2}/(qD) ✓.
Λ'/k ≤ Dσ^{−η/3} needs 18β < η/6: β = η/10^7 ✓ (log(w+2) = O(log σ) absorbed).
D_new ≤ σ^β + Dσ^{β−η/3} + CDσ^{7β−η} ≤ σ^{2β} + Dσ^{−η/4} ✓; admissible since σ^{2β}+σ^{1−3η/4} ≤ σ^{1−η/2} ✓.
T = ⌈8/η⌉: D_T ≤ σ·σ^{−2} + σ^{2β}/(1−σ^{−η/4}) ≤ 2σ^{2β} ✓. Final: Λ*/k ≤ 2σ^{2β−η/3} = o(1); Δ* ≤ CK* = CD_Tσ^{6β} ⇒ Δ*qσ/k ≤ Cσ^{8β−η} = o(1) ✓.
H(F*) ≤ dσℓ* + Λ* + O(k) + O(Δ*qσ) = dσℓ* + O(k) vs ≥ dσℓ* + ηℓ* log σ − O(k), ℓ* ≥ ck ⇒ contradiction ✓.
The whole weight therefore sits on Lemma comp:step (one-step budget, uniform constants) and the description theorem it uses.

## Paper B, §6.2 prime → every t (end:prime-interval, end:lower-slack) — HOLDS AS READ
Chebyshev-type ϑ(x) ≍ x proof is standard and correct as written. x = t/(log t)^{1+η}, q ∈ [c0x, x] ⇒ q(log q)^{1+η} ≤ t(log q/log t)^{1+η} < t
⇒ α(G) < k ≤ t, r(s,t) > ⌊q^d log q⌋ ≥ c t^d/(log t)^{d−1+dη}, d−1 = s−2; η = min{1/20, ε/(2d)} ⇒ (log t)^{ε−dη} absorbs the constant ✓.
Limit: from t^{s−1}/(log t)^{s−2+ε} ≤ r ≤ C t^{s−1}/(log t)^{s−2} and C ≤ (log t)^ε eventually ✓.

## Scope note
Neither paper treats s = 4 (no sentence says why); r(4,t) remains between t³/(log t)^4 (Mattheus–Verstraete; also Bradač's 2s−4) and t³/(log t)^2 (AKS) as far as these papers go.
