# Notes by the orchestrating seat (09Z erdos tick, 2026-11-23)

1. Correction to referee_paper.md, section 1 ("How small is ε"): the report says ε ≈ exp(−exp(10⁹)). That is
   one exponential too many. The chain it gives (K_h ≈ 2.2·10⁵, q_h^{K_h} ≈ e^{2.0·10⁵}, saving (log L)^{0.000218})
   gives log log L ≈ 9.3·10⁸, i.e. log L ≈ e^{9.3·10⁸}. Since ε = ρ_L/24 ≈ e^{−γ}/(24 log L) ≈ 0.023/log L,
   ε ≈ e^{−9.3·10⁸} ≈ 10^{−4.0·10⁸}. It is L, not 1/ε, that is doubly exponential. The page uses the corrected figure,
   labelled (c), an estimate from the proof's constants (the de la Bretèche–Tenenbaum implied constant is unknown and
   only adds a lower-order term to log log L).
2. The referee's simulation (referee/sim/sim.c) and the numerics seat's program (numerics/simple.c) were written
   separately; they agree exactly at N = 10⁴ … 10⁸, L = 7 (e.g. N = 10⁸: 520,315 heads deleted, |A| = 53,924,131).
3. Lean: the build needed a manual fetch of the pinned Mathlib commit by hash (logs/steps.tsv, 09:13:50Z note).
