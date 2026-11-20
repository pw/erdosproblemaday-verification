# Hostile referee on the core claim (separately briefed AI seat, Claude Opus 5.5, 20 Nov 2026)
Verdict: nothing FATAL, no GAP. The claim survives: |A_min| = 5,078,661,103 with n = 563T, m = 89,517T.
- (1),(2) hold: every divisor d of s is ≤ ΛT and y-smooth, so d ∈ A iff d > T; largest proper divisor is s/P⁻(s).
  Integer t > T/p ⇔ t > ⌊T/p⌋. Core formula needs only Λ ≥ y; Λ ≤ q is needed only for M(n) = |A|. T = 2^6·3·41·358026287 is not 557-smooth.
- Brute force of the whole chain on 5 tiny bands (two with Λ not prime, one with W ≥ q²): B(A) = B(A_min) as bitsets,
  max A_min ≤ n, M(n) = |A|, M(WT) equals the rough-u identity (`tiny_referee.py`).
- core.c: DFS in nondecreasing prime order visits each t once; (a, j) split double-counts nothing; t = p counted iff p² > T;
  128-bit products. Agrees with brute force on 6 NEW sets: (11,12,4000)→143, (17,19,2500)→270, (3,5,30000)→11,
  (23,25,1500)→337, (2,3,29999)→1, (19,20,777)→204; edge (7,8,7)→10.
- FIX (outside the claim's range): for T < y, core.c omits t = 1 (primes in (T, y]) and Ψ(T) overcounts. Documented.
- Independent recount `indep_referee.c` (smooth t ≤ T, then primes in (⌊T/t⌋, P⁻(t)] by prime-count table): agrees with brute
  force on 12 small cases incl. T < y; full scale y = 557: core 5,078,661,103, Ψ(T) 5,127,326,864, all 12 per-prime counts equal.
- Mutant (lo = T/P[np−1]) reproduces 445 ≠ 202.
- Certification: re-ran e488m 557 563 1000000 2818382931264 89517, byte-identical log; W = 159·563 < 563²; rough u count
  8566 = 1 + π(89516) − π(562); exact test Λ·M_lo > 2W·A_up. Ratio lower bounds from logged integers: 2.00111010 (R=10^6),
  2.00112675 (R=1,985,362), 2.00104705 (first program, scanW3a_out.txt line 254). Certifying the band certifies its core.
- All seven exact Ψ(T) inside the first program's brackets; y = 211, 523, 557 inside the second program's.
- README fixes applied: ≥ 2.00112 (not 2.00113), "seven" bands, T ≥ y precondition.
