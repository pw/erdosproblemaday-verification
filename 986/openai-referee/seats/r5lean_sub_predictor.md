# r5lean sub-seat: predictor (paper vs Lean)

## 0. Top-level statement (d=4)
- Geometry/FourFinitePredictor.lean:32-49 `eventually_four_finite_predictor`: hypotheses Range η σ D R, L₀=L η σ D, 0≤b≤Cb·D·σ^{6β}, 0<τ≤σ^{-800β}, X⊆U, T⊆UT, |X|≤|T|, q·e(X,T)≤τ|X||T|, q^5 e^{-b}≤|X||T|. Conclusions: failure mass p none ≤ 3e^{-q}; every W in support: CaptureBound X U (9/100000) (|X|·e^{10P}) W; cost ≤ 30100·q·P·(log(|U|/|X|)+log(|UT|/|T|)+P).
- Matches paper thm:predictor for d=4 (τ ≤ σ^{-200·2^{2}β}=σ^{-800β}); explicit constants c=9e-5, C=10 (size), C=30100 (msg), failure 3e^{-q}. Orientation is a HYPOTHESIS (|X|≤|T|), not a bit sent (paper says orientation costs one bit) — harmless if the caller orients.
- Proof is `filter_upwards [eventually_four_certified]` + coordinate transport (projectiveEquiv e) — FourHeader.lean:121-166.

## 1. d=4 architecture (Geometry/DimensionFourHighProtocol.lean:166-347 `eventually_four_local_complete`)
Branch tree (all inside one public index type FourPublicIndex; branch choice br is existential, i.e. part of the message, header cost ≤40q — FourHeader.lean:13):
1. |X| ≤ 100qP → base enumeration (`baseFinite`, `smallFinite_cost`), lines 268-280. = paper "Small sets".
2. "Low": |X| ≤ q^2 e^{P/10000} (⇔ g_1 ≤ χ_0). g := log|X|−3σ/2 (= paper g_0); plane peel with threshold t=⌈n^{4/3}q^{-1}e^{-g/5}⌉ performed iff P/10000<g (lines 281-291). Small cells (all ≤|S|/25) → `eventually_four_low_protocol` score; else large plane cell → `plane_branch` (d=2 recursion via `eventually_plane_public`).
3. "High": g := log|X|−2σ (= paper g_1) > P/10000: hyperplane peel threshold q^2 then plane peel with condition P/10000<g+σ/2 (= g_0>χ_0) and same K_p (lines 314-326). Small cells → `eventually_four_high_protocol`; large plane cell → plane_branch (d=2); large hyperplane cell → `eventually_three_flat_finite_predictor` (d=3 recursion), lines 343-347.
=> SAME ROUTE as paper Sections predictor-setup (greedy peel order hyperplane-then-plane, .04n' cell rule, recursion on large cell). Peel thresholds and on/off conditions match the paper exactly (q^2; K_p = n^{4/3}q^{-1}e^{-g_0/5}; χ_0=P/10000).
- Small-cell criterion: Lean `(CH i).card ≤ |S|/25` (= .04 n'), large cell gives |X| ≤ 100|X∩flat| (= |S_0| ≥ .01n). Matches.
- τ usage: the score protocols (low and high) need only τ≤σ^{-200β} (hτ200, line 247-249, used at 292,330); plane recursion gets τ≤σ^{-400β}; 3-flat recursion gets the full τ≤σ^{-800β}. Paper requires sqrt τ ≤ σ^{-200·2^{j-2}β} for the reduced pair; Lean passes τ itself and the sub-predictors must take sqrt internally — CHECK below.
