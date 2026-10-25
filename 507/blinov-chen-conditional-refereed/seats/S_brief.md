# Seat S — refute OUR additions (the panel's own new claims)
Read /tmp/oaimath/191b/seats/BRIEF_common.md first (context, rules, report format). Report: /tmp/oaimath/191b/seats/S_report.md;
work dir S_work/. These claims are ours, made during this referee; a wrong one would go out under our name. Be harder on
them than on the authors. Seat G's report (/tmp/oaimath/191b/seats/G_report.md) and code (G_work/) are where claim 1 came from.

Claim 1 (seat G, "Finding 1"): a sharpening of OpenAI's Lemma sam:proportional in Blinov's construction:
  Pr(π(u)=π(v)) ≤ 2C·M^{−k}·s^{−1}·(hq)^6·N^{−3}, C the residue-blind constant, M = L3/r, s = |S| = wq.
  Proof sketch: (α) integer proportionality ⇒ all 2×2 minors of (u|v) vanish ⇒ (Λ²G_h invertible) all minors of the
  digit columns (c|c′) vanish mod h ⇒ c′₃ ≡ c′₁c₁⁻¹c₃ (mod h) ⇒ the k third-row digits of c′ are determined
  (digits in [1,L3], L3 < B) ⇒ prob ≤ M^{−k}; (β) mod q, v_q lies on the line through 0 and u_q (0 ∉ V), which meets the
  cap V in ≤ 2 points ⇒ prob ≤ 2/s; (γ) independence of the mod-h and mod-q draws given (G_h, V) and the residue-blind
  lift count conditional on residues. Check every step: does c′₁ (row 1) really fix c′₃ uniquely? what if c′₁ is not
  a unit? are labels/digits of u and v independent as needed (two DIFFERENT samples, possibly equal labels)? is the event
  π(u)=π(v) (including u = v) contained in (α)∧(β)? is the conditioning legitimate given the shared G_h, V?
Claim 2 (ours): the 2,921-element set /tmp/oaimath/191b/pack/packing178077.txt (= {bt(a)·163 + l : 0 ≤ a < 127,
  l ∈ O23}, O23 = [0,1,3,7,8,10,18,21,22,25,27,30,48,56,58,61,62,65,67,70,77,80,81], bt = binary digits read in base 3)
  is 3-AP-free with max 178,077; with tags = its five smallest elements (0,1,3,7,8) and norm words = the other 2,916
  (smallest 10), Blinov's construction runs unchanged with k′ = 2·178,077+1 = 356,155. Check: AP-freeness (your own
  code), the matching property and tag exclusion with THIS set, and every place in Blinov's patch/notes and in Chen §2 that
  uses the specific binary-ternary set or the specific tags (0,1,3,4,9) — "twelve binary coordinates", "centered squared
  norm 12", "a < 10", "k ≥ 20", "below degree ten", the fresh-position condition v = k−1−a > a, U_a ≠ 0 with |U_a| < r.
  Does anything else depend on the set's structure?
Claim 3 (ours): with claim 1, take N = h·q·B^u (any integer u ≥ 0 keeps hq | N and N ≥ h). Then the pair term of the
  deletion is ≪ r^γ·B^{20.5k + 0.5 − 1.5u}·(constants) and → 0 iff 3u ≥ 41k + 2 (for γ < 1 near 1); the bad-triple term is
  unchanged (it does not depend on N); n_r ≍ r^{γ+X} with X = 60k + 9u + 3; γ = X/(X+1); η = 2/(X+2).
  At k = 408,781: u = 5,586,675, η = 2/74,806,940. At k′ = 356,155: u = 4,867,453, η = 2/65,176,382 ≈ 3.07·10⁻⁸
  (Chen: 2/100,866,719 ≈ 1.98·10⁻⁸). Recompute EXACTLY (python Fractions), and re-check every step of §§6–8 where N's
  size matters with this smaller N (it is smaller than Blinov's (hq)^4 and Chen's): λ3 ≤ 4N, zero-determinant cases,
  shell counts, log N = O(log r), interpolation (two-sided n_r bounds, non-integer exponent). Coordinator's script:
  /tmp/oaimath/191b/compute/ours.py. Is the sup over this method 2/(183k+8)? Is u−1 really insufficient?
Write the verdict per claim (HOLDS / HOLDS WITH FIXES / BROKEN) and an overall line. Toy-check claim 1 numerically
(small B, k, r, q; enumerate) with a mutation that must break it.
