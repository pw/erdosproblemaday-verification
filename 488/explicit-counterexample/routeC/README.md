# Route C: independent rigorous bounds for the Erdos #488 pair test

Everything here was written from scratch (nothing from `MathDyad/erdos488/` was read).
Files: `e488c.c` (full-period test, (y,T)), `e488m.c` (finite-m test, (y,Lambda,T,W)), `check.py`, `mcheck.py`,
`table.py`, `scanR*.py`, `run_targets.sh`, `run_m.sh`, and all `log_*.txt` / `check_*.txt` outputs.
Build: `gcc -O3 -march=native -fopenmp -o e488c e488c.c -lquadmath -lm` (same for e488m).
Every run: `OMP_NUM_THREADS=6 bash -c 'ulimit -v 12000000; exec timeout 3000 nice -n 10 ./e488c ...'`.

## 1. Method: an integer log-lattice with multiplicative slack

Fix a resolution R (an integer, ~10^6) and give each prime p <= y the integer weight
w_p = round(R ln p) (computed in `__float128`). For a P-smooth s = prod p^{k_p} put W(s) = sum k_p w_p (an integer).
Let rho_p = w_p / (R ln p), rho_max = max_p rho_p, rho_min = min_p rho_p. They differ from 1 by <= ~2.6e-7
(R=10^6) or ~5.3e-8 (R=1985362, chosen by a scan so that R ln p is close to an integer for the small primes).
Because every w_p lies between rho_min R ln p and rho_max R ln p, for every smooth s

    rho_min * R ln s  <=  W(s)  <=  rho_max * R ln s.                                   (*)

(Sum (*) over the prime factors with multiplicity; no bound on the number of prime factors is needed.)
The numbers c_j = #{P-smooth s : W(s) = j} are computed EXACTLY by the unbounded-knapsack DP
(a[0]=1; for each p: a[i] += a[i-w_p], ascending i) in uint64 with overflow detection on every addition
(and on the prefix sums); unique factorisation means multisets of primes = integers. Any overflow aborts the run
(never happened; `overflow 0` in every log). The DP is parallelised in layers of width w_p (layer m only reads layer m-1).

Safe constants: rho_max_s = rho_max (1+1e-20), rho_min_s = rho_min (1-1e-20). (*) holds with rho_max_s, rho_min_s in
place of rho_max, rho_min. `logq` is accurate to a few units of 2^-113 ~ 1e-34 relative, so the 1e-20 margins absorb all
rounding in computing rho and in the products rho*R*ln x (magnitudes <= 1e8, absolute error < 1e-24 << margin*value).
`check.py` recomputes rho_max/rho_min independently with mpmath (60 digits) and verifies that the C constants enclose them.

### One-sided inequalities (all derived from (*), with rho_max, rho_min meaning the _s versions)

Let N(L) = sum_{j<=L} c_j.
1. **Psi upper**: s <= x  =>  W(s) <= rho_max R ln x  =>  W(s) <= floor(rho_max R ln x). So Psi(x) <= N(floor(rho_max R ln x)) =: Psi_up(x).
2. **Psi lower**: if W(s) <= L with L = floor(rho_min R ln x), then R ln s <= W(s)/rho_min <= L/rho_min <= R ln x, so s <= x.
   So Psi(x) >= N(floor(rho_min R ln x)) =: Psi_lo(x). (Exact integer boundary points can be lost; that only weakens the bound.)
3. **|A| = Psi(qT) - Psi(T)** (resp. Psi(Lambda T) - Psi(T)) **<= Psi_up(qT) - Psi_lo(T) =: A_up** (and >= Psi_lo(qT) - Psi_up(T) =: A_lo, used only in controls).
4. **Tail (the delta lower bound).** delta = Pi * sum_{s>T} 1/s, Pi = prod(1-1/p). I do NOT use delta = 1 - Pi*S(T): that
   cancels catastrophically (delta ~ 1e-5..1e-3 while Pi*S ~ 1). Instead lower-bound the tail directly by a finite partial sum over lattice points:
   - Set L' = floor(rho_max R ln T) + 1. If W(s) >= L' then R ln s >= W/rho_max >= L'/rho_max > R ln T, so s > T. Hence {W >= L'} is a SUBSET of {s > T}.
   - For every s, 1/s = exp(-R ln s / R) >= exp(-W(s)/(rho_min R)) by (*).
   - So  sum_{s>T} 1/s >= sum_{j=L'}^{J} c_j exp(-j/(rho_min R))  for any cutoff J (dropping terms is allowed: all terms are >= 0).
   J is taken as R (ln T + E), E=40..55 (tail pieces printed per 1/8 of E; the last piece is <= 5e-7 of the total in every target, <= 1e-8 for y<=1021, so the cutoff loses almost nothing; the inequality does not depend on that).
5. delta_lo = Pi_lo * tail_lo where Pi_lo = (prod (p-1)/p computed in quad) (1-1e-20), tail_lo = (computed sum)(1-1e-20).
6. ratio_lo = delta_lo * n / A_up (n=qT), certified iff delta_lo*n > 2*A_up (the program tests it in quad; all certified margins are >= 3e-3, vs rounding 1e-20).
7. Extra bounds used as controls only: S_up = sum_{j<=floor(rho_max R ln T)} c_j exp(-j/(rho_max R)) >= S(T) and S_lo = sum_{j<=floor(rho_min R ln T)} c_j exp(-j/(rho_min R)) <= S(T)
   (same argument: the index sets are supersets/subsets of {s<=T}; 1/s <= exp(-W/(rho_max R)) and >= exp(-W/(rho_min R))).

### Floating-point error (explicit)
- All c_j, N(L), A_up are exact integers; no floating point enters Psi/A_up except the *index* floor(rho R ln x), covered by the margins above.
- The exp-sums are in `__float128` (113-bit mantissa, u = 2^-113 ~ 9.6e-35). exp(-j/D) is computed by `expq` at the start of each block of 64 terms and then multiplied by r = expq(-1/D)
  term by term. Relative error of a term: <= (exponent-argument error ~ 100 u) + (expq, <= ~2 u) + (<= 64 products, 64u) < 300 u ~ 3e-32. Summation of <= 1.2e8 positive terms (chunked, then chunk sums added):
  relative error <= 1.2e8 * u ~ 1.2e-26. Total relative error < 1e-25, far below the 1e-20 safety factors (1-1e-20) / (1+1e-20) applied to every sum and to delta_lo, ratio_lo. The conclusions use margins of 1e-3 or more.
- Pi: <= 2*309 quad operations, relative error < 7e-32, covered by (1-1e-20).
- Caveat stated honestly: `expq`/`logq` accuracy is the documented libquadmath behaviour (<= few ulp), not formally proven here; the controls below (agreement with exact values to 1e-5..1e-6, and with the exact integer values) are consistent with it.

### Finite-m test (e488m)
With A = {smooth a: T < a <= Lambda T}, y <= Lambda <= q, n = Lambda T, W > Lambda, m = W T, the fact supplied by the coordinator is
M_A(WT) = sum over rough u < W of (Psi(floor(WT/u)) - Psi(T)) (rough = no prime factor <= y; here every u<W with smallest prime factor > y, found by a sieve: u=1 and primes in [q,W) since W<q^2).
(floor(WT/u) >= T because u < W.) Bounds: M_lo = sum_u max(0, Psi_lo(floor(WT/u)) - Psi_up(T)), M_up = sum_u (Psi_up(floor(WT/u)) - Psi_lo(T)); both valid termwise by items 1-2.
|A|_up = Psi_up(Lambda T) - Psi_lo(T). Counterexample iff n*M_A(m) > 2*m*|A| <=> Lambda*M > 2*W*|A| (T cancels); certified iff the EXACT 128-bit integer inequality
Lambda*M_lo > 2*W*A_up holds. ratio_lo = n M_lo / (m A_up) = Lambda M_lo / (W A_up), printed from exact integers. Prefix counts N(L) are stored as a uint64 prefix array (checked for overflow). 
Nothing else is used from Liu's lemma; `mcheck.py tiny` verifies the formula and the bounds against a brute-force that builds M_A(WT) as the literal union of multiples of A up to WT (11 tiny cases with W<q^2, all bracketed).

## 2. Controls

All outputs: `check_*.txt`, logs `log_ctrl_*`, `log_tiny_*`, `log_mctrl_*`.

**Full-period controls (exact values from the task), R=10^6, E=40** (`check_given_251.txt`, `check_given_509.txt`): all of Psi(T), Psi(qT), |A|, S(T), tail=1/Pi-S, delta, exact ratio
are bracketed (ratio_lo below exact ratio) -> PASS:

| y | T | exact ratio | ratio_lo (ours) | rel. gap | A_up vs exact |A| |
|---|---|---|---|---|---|
| 251 | 1e4 | 1.215608530 | 1.215601532 | 5.8e-6 | 310368 vs 310367 |
| 251 | 1e6 | 1.355149932 | 1.355142409 | 5.6e-6 | 5934693 vs 5934681 |
| 251 | 1e8 | 1.485739100 | 1.485728229 | 7.3e-6 | 87826512 vs 87826323 |
| 509 | 1e10 | 1.664615510 | 1.664599016 | 9.9e-6 | 6513876787 vs 6513858878 |

(For T=1e6 only the ratio is given, so S was backed out from the 10-digit ratio: a weaker check, still passes with 1e-5-wide bounds.)
S(T) is bracketed too, e.g. y=251,T=1e8: S in [9.91419125, 9.91420945] contains 9.914200348.

**Brute-force tiny controls** (`check_tiny_y{7,11,13}.txt`; Fractions for S, exact enumeration for Psi, A): y in {7,11,13}, T in {1,7,100,999,1000}; every bound brackets the exact value. PASS.
(Tiny T show larger gaps, up to 3%, because there the floor at integer lattice points matters; this is a weakness of the bound, not of rigor.)

**Negative control (checker can fail)**: `./e488c -u 251 100 30 ...` = deliberately UNSAFE variant: floor weights (w_p <= R ln p) with rho forced to 1 and no margins, at coarse R=100.
That is the correct *upper*-bound direction used as a lower bound. Result (`check_negctrl_unsafe.txt`): Psi(T) "lower" 5637 > exact 5508 -> VIOLATED, and Psi(n), |A|, S, tail, delta all VIOLATED;
the reported "ratio_lo" exceeds the exact ratio for T=1e4 (1.21632 > 1.21561) and T=1e8 (1.48611 > 1.48574): the unsafe variant would have over-claimed. The SAFE code at the same R=100 (`check_negctrl_safe_sameR.txt`)
still brackets everything (ratios 1.116, 1.211, 1.287: loose but true). Same story for the finite-m code: `./e488m -u 61 67 200 ...` -> Psi(T)/|A|/M all VIOLATED (`check_m_negctrl.txt`), safe at R=200 passes.

**Finite-m control** (y=61, Lambda=67, T=1e12, W=2876; exact |A|=64844856, Psi(T)=19413722, M=4242568187, ratio 1.524190400) (`check_m_control.txt`):

| R | Psi(T) bounds | |A| bounds | M bounds | ratio bounds |
|---|---|---|---|---|
| 1,000,000 | [19413676, 19413752] | [64844657, 64845068] | [4242532382, 4242607918] | [1.5241725535, 1.5242093513] |
| 1,985,362 | [19413711, 19413729] | [64844800, 64844910] | [4242559634, 4242578640] | [1.5241860578, 1.5241954715] |

All bracket the exact values. PASS.

## 3. Targets, full-period test (R=10^6, E=40; second discretisation R=1201097, E=55 for y<=1021 and E=45 for y=2039 -- E=55 made the uint64 DP overflow for y=2039, which the overflow guard caught and aborted, log `log_target_R1201097_2039_E55_OVERFLOW_aborted.txt`)

delta_lo, ratio_lo = delta_lo * n / A_up with n = qT. All "certified yes". Wall times (6 threads, shared loaded box): the DP+sums run, including all T of the same y.
Logs: `log_target_R1e6_*`, `log_target_R1201097_*`; `table.py` prints these tables. `selfconsistent` = tail_lo <= 1/Pi - S_lo and 1/Pi - S_up <= 1/Pi - S_lo (a cross-check between tail and S).

| y | T | q | A_up (R=1e6) | delta_lo (R=1e6) | ratio_lo (R=1e6) | ratio_lo (R=1201097) | certified | runtime (R=1e6) |
|---|---|---|---|---|---|---|---|---|
| 509 | 1e16 | 521 | 12360868990588 | 4.82810986143e-6 | 2.035006794 | 2.035024632 | yes | 14.6 s |
| 1021 | 1e15 | 1031 | 32659880163738 | 6.46558267377e-5 | 2.041041089 | 2.041057751 | yes | 25.2 s (shared with next row) |
| 2039 | 1e15 | 2053 | 220150888342403 | 2.21855028281e-4 | 2.068891825 | 2.068909052 (E=45) | yes | 37.3 s (shared with next row) |
| 2039 | 2e14 | 2053 | 79852766203158 | 3.92753321232e-4 | 2.019523197 | 2.019539012 (E=45) | yes | " |
| 1021 | 3e14 | 1031 | 16220862725683 | 1.05222875977e-4 | 2.006393623 | 2.006409633 | yes | " |

A_up at R=1201097: 509/1e16: 12360846987971; 1021/1e15: 32659829070665; 1021/3e14: 16220840193443. The two discretisations agree to ~1e-5 relative (the true ratio lies above both lower bounds); the lower bounds move upward as R grows, as expected.
Slack: ratio_lo is below the true ratio by ~6e-6..1e-5 relative (measured on controls of similar size), so margins above 2 are not marginal; the thinnest is (1021, 3e14) at 2.0064.

## 4. Targets, finite-m test (Lambda integer, A in (T, Lambda T])

certified iff the exact integer test Lambda*M_lo > 2*W*A_up holds. ratio = n M / (m |A|).

| # | y | Lambda | T | W | A_up (R=1e6) | M_lo (R=1e6) | ratio_lo (R=1e6) | ratio_lo (R=1985362) | certified |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 401 | 409 | 12589254117941 | 52761 | 172012150997 | 44401086479555 | 2.000989272 | 2.001006628 | yes |
| 2 | 251 | 256 | 72057594037927936 (2^56) | 22616 | 1828060724788 | 343241458094730 | 2.125363852 | 2.125388349 | yes |
| 3 | 251 | 256 | 281474976710656 (2^48) | 24415 | 156997287557 | 29866041696775 | 1.994659430 | 1.994679749 | **no** |
| 4 | 401 | 409 | 15000000000000 | 52761 | 188435153331 | 48768078784384 | 2.006245203 | 2.006262970 | yes |

(Rough counts: 5308, 2472, 2657, 5308 values of u; all W < q^2. Runtime 3-4 s each at R=1e6, 6-25 s at R=1985362.)
Target 3 is NOT certified, and in fact rigorously NOT a counterexample: the same code also gives a one-sided UPPER bound ratio_up = Lambda*M_up/(W*A_lo) (M_up = sum_u (Psi_up(floor(WT/u)) - Psi_lo(T)), A_lo = Psi_lo(Lambda T) - Psi_up(T), both valid by items 1-2).
For target 3: ratio in [1.994659430, 1.994714706] (R=1e6) and [1.994679749, 1.994694955] (R=1985362) < 2, so n*M < 2*m*|A| is proven. Intervals for the others (R=1985362): #1 [2.001006628, 2.001020072], #2 [2.125388349, 2.125407485], #4 [2.006262970, 2.006276466].
Target 1 is the thinnest certified one (margin 1.0e-3 above 2 at R=1e6, 1.0e-3 at R=1985362; slack ~1e-5).

## 5. Things I doubt / limits
- Rigor rests on (a) libquadmath accuracy (documented, not proven; margins are 10^10 times the plausible error), (b) the supplied "Fact" (multiples iff P-part > T) and Liu's Lemma 12(iii), which I only brute-force-checked on tiny cases (union-of-multiples brute force agreed, `check_m_tiny.txt`), (c) correctness of my C code, supported by controls on exact values at 5 (y,T) full-period points, 1 finite-m point, tiny brute force, and a failing negative control.
- The tail sum is truncated at ln s = ln T + E (dropping positive terms is safe); the last pieces are <= 1e-6 of the total (see `tail_piece_*` in logs), so the bound is not noticeably weakened.
- (The y=61 finite-m control also brackets the exact ratio from both sides, see table.)
- Full-period controls use only n = qT; the finite-m runs use Lambda possibly < q (Lambda=256 for y=251): the DP does not care (any integer n).

## 6. Additional finite-m targets (y=1009, Lambda=1013=q, W=250347 < q^2; 21900 rough u: 1 and the primes in [1013, W))

Same code (`e488m`), logs `log_m_R1000000_t{5,6}_y1009.txt` and `log_m_R1985362_t{5,6}_y1009.txt`. Exact integer test Lambda*M_lo > 2*W*A_up holds in all four runs (`exact_test_lhs_gt_rhs 1`; overflow 0).
ratio_up = Lambda*M_up/(W*A_lo) is a rigorous upper bound on the true ratio.

| # | T | R | A_up | M_lo | ratio_lo | ratio_up | certified |
|---|---|---|---|---|---|---|---|
| 5 | 1200000000000 | 1,000,000 | 570685059287 | 282582848343356 | 2.003624574 | 2.003669335 | yes |
| 5 | 1200000000000 | 1,985,362 | 570684240806 | 282584653575673 | 2.003640247 | 2.003653193 | yes |
| 6 | 1100000000000 | 1,000,000 | 541177125271 | 267548832549725 | 2.000463735 | 2.000509612 | yes |
| 6 | 1100000000000 | 1,985,362 | 541176237451 | 267550575584668 | 2.000480050 | 2.000492944 | yes |

Both bounds exceed the coordinator-supplied lower bounds (2.003562825 and 2.000402962), consistent with ours being tighter; the true ratio lies in [2.003640247, 2.003653193] (#5) and [2.000480050, 2.000492944] (#6) using the finer run.

Target 7 (y=1009, Lambda=1013, T=1096478196143, W=251224 < q^2; n = 1110732412692859; 21970 rough u). Logs `log_m_R*_t7_y1009.txt`.

| # | T | R | A_up | M_lo | ratio_lo | ratio_up | certified |
|---|---|---|---|---|---|---|---|
| 7 | 1096478196143 | 1,000,000 | 540118768524 | 267945345576020 | 2.000346671 | 2.000392477 | yes |
| 7 | 1096478196143 | 1,985,362 | 540117890011 | 267947084226568 | 2.000362905 | 2.000375465 | yes |
