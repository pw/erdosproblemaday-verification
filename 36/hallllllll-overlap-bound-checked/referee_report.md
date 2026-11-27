# Referee seat report: Erdős #36 (minimum overlap), submission 44a4n7 (reader "Hallllllll"), 27 Nov 2026

Seat: a separate Claude instance (Opus 5.5), briefed to refute, with tools; erdosproblems.com not read.
Saved verbatim-in-substance by the main seat (subagents cannot write their own report files).

Verdict: the construction holds exactly. U = 2462273619527794579322422405079 / 6465103708838880000000000000000
≈ 0.38085601258978320 is correct and is a valid upper bound for the minimum overlap constant modulo the published
Swinnerton-Dyer theorem (proof in Haugland 1996). In Lean at the submitted tag it is unconditional only for the
continuous constant; the step to the Erdős constant is a hypothesis (WhiteBridge), as the reader says.

1. Setup (VERIFIED, read). h = a_i/D on 9,408 cells of width 2/9408 on [0,2), D = 52428700000000 = 524287·10^8;
   g = 1 − h on [0,2), 0 outside; H(s) = ∫ h(x) g(x−s) dx. Same as White (2022) eq. (1.1) shifted to [0,2), Haugland
   2016 eq. (1), AlphaEvolve's formulation. White: "A key step in Haugland's method is a theorem of Swinnerton-Dyer
   proving that (1.1) is in fact also µ, see [3] for the proof" ([3] = Haugland, J. Number Theory 58 (1996)).
2. Lean statements (read, not built): Admissible; continuousConstant := sInf {sup of overlaps}; WhiteBridge :=
   Tendsto (M n / n) atTop (𝓝 continuousConstant); witness_supremum_exact : sSup (range (overlap h (complement h))) = U;
   continuous_upper_bound : continuousConstant ≤ U; discrete_upper_bound_of_white (hc : Tendsto … (𝓝 c)) (white :
   WhiteBridge) : c ≤ U (hc redundant given WhiteBridge). No sorry / native_decide / axiom / unsafe / implemented_by
   in any v1.0.0 file. Later commit 31ded31 (main, 07:57Z) adds discrete_limsup_le_continuous, discrete_upper_bound
   (limsup M(n)/n ≤ U, no bridge premise) and whiteBridge : WhiteBridge — UNVERIFIED here (not built).
3. Recomputation (VERIFIED): T_k = Σ a_i (D − a_{i−k}) for all 18,817 lags, exact, by 20-bit int64 split convolution;
   H(kw) = 2·T_k/(N·D²); H piecewise linear with corners at multiples of w. max T = 4924547239055589158644844810158
   ⇒ U exactly; argmax only k = −2284 (s = −571/1176); second best k = −3052 (s = −763/1176), lower by 2.7e-13.
   Side conditions exact (0 ≤ a_i ≤ D, 2Σa = N·D; support cells 1010–8399; 1,324 cells equal 1). Direct-definition
   spot checks at 9 lags; Σ_k T_k identity; exact off-grid integration at 8 shifts ≤ U; float FFT max diff 2.2e-16.
   Lean Data.lean heights identical to construction.json; all 18,815 certificate digits equal our T_k.
   Their verify.py and audit_verify.py: PASS here.
4. Controls: Haugland 2016 19-step 0.381112263316104816 (all digits), 51-step 0.3809268534330870 (within 5.6e-17),
   15-step 0.38153154825 (≈ 0.38153155); AlphaEvolve 95-step 0.380923035108450 (≤ 0.380924, identical to their numpy
   formula). Negative: mass shift changes U by 4.0e-15; +1 above D, value >1, negative all flagged; wrong convention
   (g = 1 outside) gives 1.0 for Haugland's 51-step; f = 1 on [1/2,3/2) gives exactly 1/2.
5. Parent: ArDrive/Arweave file byte-identical to repo sources/frontier_parent.txt (sha256 89916aef…), Arweave block
   time 2026-11-25 19:45:40Z, title tag "erdos-minimum-overlap-large 0.380856013736"; Compute Substrate proposal
   0x61ac9b02… in domain frontier.erdos-minimum-overlap-large. P = 123113681346619/323255185441944 exactly (4,704
   cells over 524287); P − U = stated gain exactly. Child re-optimized on the doubled grid: 5,396 of 9,408 cells
   differ from the parent doubled, by up to 3.2e-6. EinsteinArena #1 "Leon" (2026-11-27 03:02Z) identical to this
   construction; previous #1 "Blob" 0.38085625978 (gain ≈ 2.5e-7). vs AlphaEvolve ≈ 6.7e-5; vs Haugland ≈ 7.1e-5.
6. Their CI run 45928864419 (their instrument): passed on 045d628 with Lean v4.36.0; standard axioms for
   admissible_h, grid_supremum, witness_supremum_exact, continuous_upper_bound, discrete_upper_bound_of_white;
   packed_certificate depends on no axioms; leanchecker (not --fresh) over 8 modules exit 0.
7. Objections: (1) "WhiteBridge, the published discrete-limit characterization in White (2022), equation (1.1)" —
   the theorem is Swinnerton-Dyer's (proof in Haugland 1996); (1.1) is the continuous definition (their PROOF.md
   says this correctly). (2) "continuous_upper_bound [is] unconditional" — true, but it bounds the continuous
   constant. (3) Uniqueness of the maximum VERIFIED, margin 2.7e-13. Nothing false found.
