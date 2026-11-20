# Erdős #488 — how many generators does a known counterexample need? (20 Nov 2026, ours, label (d))

Every known counterexample is a smooth band A = {s in (T, ΛT] : all prime factors of s are ≤ y}, y < Λ ≤ q (next prime),
with n = ΛT and m = W·T. Replacing A by its divisibility-minimal elements A_min leaves the set of multiples unchanged and
does not raise max A, so A_min is a counterexample with the same n and m, and no element of it divides another.

**Which members are minimal.** s ∈ A has a proper divisor in A iff its largest proper divisor s/P⁻(s) exceeds T
(P⁻ = smallest prime factor; every divisor of s above T lies in A). So
|A_min| = Σ_{p ≤ y} #{ t ∈ (T/p, T] : every prime factor of t lies in [p, y] }  (s = p·t).

**Result.** `core.c` counts this exactly by depth-first enumeration of all y-smooth numbers up to T, for seven bands the
11 Nov certifier accepted (`core_y*_T*.txt`, `core_y211.txt`):

| y | Λ | T | n = ΛT | |A_min| (exact) | Ψ(T) exact |
|---|---|---|---|---|---|
| **557** | **563** | **2,818,382,931,264** | **1.59·10^15** | **5,078,661,103** | 5,127,326,864 |
| 523 | 541 | 3,548,133,892,336 | 1.92·10^15 | 5,345,203,928 | 5,537,434,764 |
| 211 | 223 | 562,341,325,190,349 | 1.25·10^17 | 5,833,636,733 | 10,554,476,178 |
| 607 | 613 | 3,162,277,660,168 | 1.94·10^15 | 6,712,529,809 | 6,492,641,832 |
| 709 | 719 | 2,238,721,138,568 | 1.61·10^15 | 7,564,133,965 | 6,774,514,811 |
| 887 | 907 | 1,318,256,738,556 | 1.20·10^15 | 8,285,734,803 | 6,746,317,971 |
| 1009 | 1013 | 1,096,478,196,143 | 1.11·10^15 | 8,969,727,104 | 6,935,462,096 |

So the 557-smooth band's core is a counterexample with **|A| = 5,078,661,103**, no element dividing another,
n = 563T = 1,586,749,590,301,632, m = 89,517·T. Certified: first program (11 Nov scan, ratio ≥ 2.001047) and the
independently written second program `e488m` (route C of `../explicit-counterexample/`), re-run today at two resolutions:
ratio ≥ 2.00111 (R = 10^6) and ≥ 2.00112 (R = 1,985,362) — `second_certifier/log_m_R*_y557.txt`. The y = 211 and
y = 523 bands are also re-certified by the second program (`second_certifier/`).

**Controls.** `controls.txt`: `brute.py` builds three small bands, removes every member with a proper divisor in the band
(full divisor check), and agrees with `core.c` (54, 202, 45). A mutant counting with T/(largest prime) instead of
T/(smallest prime) gives 445 ≠ 202. The enumeration also yields Ψ(T) exactly; all seven values lie inside the
brackets the 11 Nov certifier printed, and the y = 211, 523, 557 values inside the second program's brackets.

**Scope.** These seven bands come from a scan that minimised n, not |A_min|; a scan aimed at |A_min| would likely do
somewhat better. The kernel-checked lower bound is |A_min| ≥ 5 (Jig problem 398, statements 2/4/7/11), ≥ 8 if Ewing's
candidate holds. Build: `gcc -O2 -fopenmp core.c -o core`; run `./core y T` (requires T ≥ y: for T < y it omits the primes in (T, y] and Ψ is off — the referee seat found this; all runs here have T ≫ y) (≈ 1–3 min each with 8 threads).

**Independent recount (referee seat, 20 Nov).** `indep_referee.c`, written separately, lists each smooth t ≤ T and counts the
primes in (⌊T/t⌋, P⁻(t)] from a prime-count table; it agrees with brute force on 12 small cases (including T < y) and at
full scale gives |A_min| = 5,078,661,103 and Ψ(T) = 5,127,326,864 for y = 557, with all 12 printed per-prime counts equal to
`core.c`'s. The referee also re-ran `e488m 557 563 1000000 2818382931264 89517` (byte-identical log) and checked the
multiples identity and B(A) = B(A_min) by brute force on five tiny bands. `core_mut.c` is the deliberately broken control.
