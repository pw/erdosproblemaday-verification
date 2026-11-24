Della Pietra's N = 10^6 numbers reproduce exactly, and the set really is relation-free. But that set is the simple version: the full top half plus every rough head, with no regularity filter. Its excess shrinks steadily from N = 10^5 to 10^11 for every L tested. At no N or parameter choice did regularity raise the excess.

**About 10^11:** it was not stopped. It had already finished (2,207 s, 120 MB) before your message arrived, so there was nothing of mine to kill and its numbers are included below. My own waiter has also exited. One process is still running, `timeout 300 bash -c while pgrep -f "simple 100000000000"`. I didn't start it, so I left it alone.

Everything is in `~/MathDyad/erdos301/dellapietra/numerics/`. Every number below is printed from a file in `out/`.

### 1. Reproducing his N = 10^6, L = 7 numbers
- **His script, run unchanged** (`python3 -I ../repo/controls/verify-rough-third-excess.py`, 2.5 s, output in `out/his_script_N1e6_L7.txt`): 44,445 rough heads, 4,242 deleted, 5,391 relations, |A| = 540,204. All checks passed.
- **My program** (`simple.c`, output in `out/simple_N1000000.txt`): 44,445 / 4,242 / 5,391 / 540,204. Exact agreement, and also at his N = 1200 box (54 heads / 1 deleted / 654).
  - It finds conflicts differently from his code. He enumerates divisors of a²; I use the smallest ratio between consecutive divisors of a.
- **It is the simple construction.** His `large_proxy_scan` uses the full `[ceil(N/2), N]` and filters heads only by gcd with the primorial. His own docstring calls it a "proxy". The README's line "what the construction achieves numerically" is about this proxy, not the regular H_N and T_N.

### 2. Relation-freeness checks
**k = 2 at N = 10^6** (`check.c`, output in `out/check_N1e6.txt` and `out/check_regular.txt`):
- Method: every element is tried as a head, all divisors d of a² are enumerated, and b, c are looked up in a bitmap of the set.

| Set | Relations found |
|---|---|
| {2,3,6} | 1 (1/2 = 1/3 + 1/6) |
| [1, 10^6] | 2,524,207 |
| Before deletions | 5,391 (matches both counts above) |
| Final set (540,204 elements) | 0 |
| Final set plus one deleted head (333371) put back | 1 |
| Two regular sets (520,380 and 530,490 elements) | 0 each |
| Regular top plus all rough heads | 3,694 |

**Exhaustive search over k = 2, 3, 4** (`brute.c`, output in `out/brute_small.txt`):

| Set | N | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| {2,3,7,42} | 42 | 0 | 1 | 0 |
| [1, N] | 3000 | 3,905 | 60,051 | – |
| (N/4, N] | 3000 | 830 | 883 | – |
| (N/3, N] | 3000 | 310 | **0** | – |
| Before deletions | 3000 | 7 | 0 | – |
| Final set | 3000 | 0 | 0 | – |
| [1, N] | 600 | 582 | 4,979 | 41,636 |
| (N/4, N] | 600 | 127 | 80 | 0 |
| (N/3, N] | 600 | 47 | 0 | 0 |
| Final set | 600 | 0 | 0 | 0 |

The (N/3, N] rows confirm the localization argument: no relations of length 3 or 4 above N/3, while (N/4, N] already has length-3 ones.

### 3. Trend of the simple construction
Data in `out/summary.txt` and `out/trend_fit.txt`.

| N | L=7 deleted share | L=7 excess | L=11 excess | L=13 excess | L=17 excess | L=23 excess |
|---|---|---|---|---|---|---|
| 1e5 | 0.0799 | 0.04091 | 0.03558 | 0.03273 | 0.03046 | 0.02738 |
| 1e6 | 0.0954 | 0.04020 | 0.03504 | 0.03225 | 0.03002 | 0.02710 |
| 1e7 | 0.1062 | 0.03972 | 0.03465 | 0.03191 | 0.02972 | 0.02681 |
| 1e8 | 0.1171 | 0.03924 | 0.03430 | 0.03161 | 0.02945 | 0.02660 |
| 1e9 | 0.1260 | 0.03884 | 0.03399 | 0.03134 | 0.02922 | 0.02640 |
| 1e10 | 0.1339 | 0.03849 | 0.03371 | 0.03110 | 0.02901 | 0.02623 |
| 1e11 | 0.1410 | 0.03817 | 0.03346 | 0.03088 | 0.02882 | 0.02607 |

- **Deleted share for the other L at 1e11:** 0.1216 (L=11), 0.1082 (L=13), 0.0985 (L=17), 0.0851 (L=23).
- **The excess falls and the deleted share rises at every step, for every L.** The deleted share grows roughly linearly in log log N, at about 0.075 per unit for L = 7.
- **Where the creep comes from:** within each prime-factor count Ω(a) ≤ 4, the deleted share actually falls with N (Ω=3: 0.311 at 1e5 down to 0.127 at 1e11). The total rises because the Ω distribution shifts up (mean Ω 1.85 at 1e5, 2.57 at 1e11) and heads with Ω ≥ 5 are 75–93% deleted.
- **Survivors:** prime heads never conflict. Survivors also concentrate near N/2, where the allowed divisor ratio shrinks toward 1.
- **Run times:** under 1 s up to 1e7; 3.3 s at 1e8; 29 s at 1e9; 225 s at 1e10; 2,207 s at 1e11 (3 threads). Memory about 160 MB throughout.

### 4. The regularity version
- **Thresholds:** regularity is decided by exact integer cut-offs ⌈L^(e^(m/A))⌉. These are computed twice at more than 100 digits and certified to be far from an integer (`thresholds.py`, `out/thresholds.txt`).
- **Program:** `regular.c` covers N = 1e5 to 1e9, L ∈ {7, 11, 13, 17, 23}, A ∈ {1.0001, 1.16312, 1.5, 2} (all 16 head/top pairs), and K_h, K_t ∈ {0, 1, 2, 3, 4, ∞}. Run times: 1.5 s at 1e7, 15 s at 1e8, 177 s at 1e9.
- **Cross-checks:** with K = ∞ it reproduces `simple.c` exactly. Its internal self-test re-factored 10,782 b and c values by trial division with 0 mismatches. A separate Python version (`regular_xcheck.py`) matched 5 configurations exactly at 1e5.

Results at L = 7 (format: excess, then [top loss/N, kept regular heads/N]):

| Setting | 1e5 | 1e9 |
|---|---|---|
| No regularity | 0.04091 | 0.03884 |
| A = 1.5, K_h = K_t = 2 | 0.02252 [0.018, 0.041] | 0.00399 [0.035, 0.039] |
| A = 1.5, K_h = K_t = 3 | 0.03635 | 0.03045 |
| Paper's A (1.0001 / 1.16312), K_h = ∞, K_t = 3 | 0.03503 [0.006, 0.041] | 0.02932 [0.010, 0.040] |

- K_t = 3 is the paper's own formula ⌈c log log L⌉ at L = 7. At L = 13 that formula gives K_t = 4, with excess 0.03022 against 0.03134 unfiltered at 1e9.
- **Regularity hurts at every computable N.** Over the whole grid, no regularity setting beat the unfiltered construction at any N or L (`out/summary.txt`, last block). The best case only ties at small N, where the filter removes nothing that matters.
- **Why:** the top loss grows with N for fixed K. With top regularity on, the conflicted share of heads still climbs (paper's parameters, L = 7: 0.076 to 0.110).
- **Low K_h:** setting K_h to 0 does give zero conflicts, but it keeps only primes and lopsided semiprimes, and the excess collapses (0.0157 down to 0.0087).

### Plain reading
The 0.54 density at N = 10^6 comes from the unfiltered proxy, and its excess shrinks slowly but steadily from 10^5 to 10^11 for every L, so it says nothing about a fixed ε. As far as I recall (not checked), Maier–Tenenbaum's theorem on close divisors should push the deleted share to 1. Regularity, which the proof depends on, only lowers the excess at every N and L we can compute, so the claim stands or falls on its analysis at astronomically large L, which no computation here can reach.