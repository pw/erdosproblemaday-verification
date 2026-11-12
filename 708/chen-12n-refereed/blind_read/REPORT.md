# Blind read of the page draft (Claude Opus 5.5 seat, 2026-11-12) — verdict SHIP WITH FIXES (all applied)

Maths of "Ours" correct; all 13 certificates re-checked (hypotheses, u the only two-prime member, no q_u²/q_v² multiples,
covers valid); table = certs.json; both barrier instances recomputed (23 vs 46; 182.9 vs 145).
MUST-FIX (applied): (1) FinalCheck has two bridge theorems (reference_g_le_12, reference_g_le_19), not four.
(2) g(4) ≤ 28 by Chen's Theorem 1.1 (F(4) = 28), not 48. (3) The shifted-centre device is Erdős–Surányi's own (1959 §4:
"van uvwd-nek olyan többszöröse, amely w²d-nek az őt közrefogó mindkét többszörösétől messzebb van…"; §9 "alkalmas
kongruenciák megoldásával"); ours is applying it to Chen's family. (4) 1959 Theorem IV gives g(k) ≥ k+1 for k ≥ 3, so
g(4) ≥ 5, g(5) ≥ 6 predate Chen; comparison ties at n = 4, 5. (5) Barrier: the threshold floor 2 stands; via Theorem 16.1
it rules out < 4n, via the asymptotic conversion the floor is (3+o(1))n (Wang's audit S03 l.204) — don't endorse "not
below 4n" as a statement about the method.
SHOULD-FIX (applied): comparison phrasing (26 of 32 below 36; 1959 wins at 21, 28, 29; tie 15; last ours-larger n = 90);
"no upper bound beyond g(3) ≤ 4"; "first … as far as he or we could find"; comments suspended site-wide; Lean 11n wording;
Wang's 8.83n + o(n); "Beyond these two repositories…"; GPT-5.6/GPT-6/Qwen; referee "broke no theorem and found one slip",
Prop 18.9 correct as stated, the slip is Remark 18.10; Preil byline (written by Claude Fable 5.1, directed by Preil);
July–August rounds; proof-sketch gaps (m = max A, q_v² − m = q_v(q_v − w_t), s ≢ 0 because u's offset is in the run);
jargon (hinge inequality, w_z, cycle rank, K_{2,t}); credit the K_{2,t} family to the run37 referee; shorter, hedged title.
Reader's scripts: /tmp/e708_reader/chk.py, bar.py (copied here).
