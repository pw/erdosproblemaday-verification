# Erdős #282 — the odd greedy algorithm after the factorial runs out (9 Nov 2026)

Page: https://erdosproblemaday.com/day/282-odd-greedy-after-the-factorial-runs-out

## Claims (labels: (a) elementary, (c) heuristic, (d) computational)
- (d) 3/(500!−1) has exactly 501 odd-greedy terms (numerators 3..501, then 2, 1; the climb breaks at 502 = 2·251).
  3/(2·500!−1) has 519 (climb to 520, ends at the prime 521). 3/(1000!−1): 1011; 3/(2·1000!−1): 1005;
  N = 5000: 5001 and 5001; N = 10000: 10005 and 10005; N = 20000: 20025 and 20013 (all certified, out/certify_big.txt).
- (d) For every 3 ≤ N ≤ 3000, the odd greedy expansions of 3/(N!−1) and 3/(2·N!−1) terminate (out/sweep_3000.txt,
  columns: N, t (1 for N!−1, 2 for 2·N!−1), length, max numerator, last numerator of the initial climb, trace length |
  numerators after the climb). Overshoot of the climb past N ≤ 56; ≤ 22 numerators after the climb. Every row is
  re-derived by certify.py (out/certify_sweep*.txt; 5,996/5,996, 0 problems). How the 5,802 climbs with N ≥ 100 end
  (out/stats2.json, from the certifier's own s, g at the last climb numerator R): 2,930 end the expansion at the prime
  R+1; 1,501 have numerator R+1 cut by a prime factor of the denominator; 1,371 break because R does not divide m.
- (d) Every reduced a/b in (0,1) with odd b < 10,000 terminates (20,263,332 fractions = Σφ(b) over odd b); max 32
  terms, exactly four: 2086/2381, 7734/7829, 7990/8111, 8328/8581. For x < 1/3: 6,754,437 fractions, max 29 (373/6893).
- (d) OEIS A030541–A030546 (Broadhurst 1999): each entry's data is the sequence of the fraction named in the previous
  entry (cyclically). A031285 is correct.
- Credited, not ours: the modular method (K. S. Brown, D. Bailey, D. Eppstein); parity alternation (Pihko, Fib. Quart.
  39 (2001), (2.4)–(2.5)); the families a/(2k+1), k = −1 + t·a(a+1)···(a+n) (Brown; Pihko, Fib. Quart. 48 (2010),
  Thm 2.3); the fixed residues z ≡ 0 / z ≡ −1 (Pihko 2010, proof of Thm 3.5 and Lemma 3.1; Brown kmath454's d ≡ ±1).
- (c) No break-even point is expected: each obstacle past N is a fixed-odds event. Evidence, not proof.

## Instruments
- code/og.c — C/GMP. `gcc -O2 -o og og.c -lgmp`. `./og one a b` (numerators after the hand-off, then length),
  `./og fact 3 N cap trace|- t` (3/(t·N!−1)), `./og scan blo bhi` (all reduced a/b with odd b in range; histogram + FNV
  fingerprint; `OG_THIRD=1` restricts to 3a < b). `OG_FAST=1` selects the O(K) mode. Exact prefix phase for the
  not-used-before rule; after the hand-off b_k is recomputed modulo what each step needs; every division asserted.
- code/check_fixedmod.py — independent Python/gmpy2 engine (one fixed modulus (2·lcm(1..H))^(2K+2), no replay).
- code/certify.py — recomputes a claimed trajectory step by step; claim used only to size the modulus. Exit 0/1/2.
- code/exact_small.py — exact big-denominator arithmetic (N ≤ 19).
- code/run_controls.sh — re-runs every control; output out/controls.txt.
- code/brown_cover.py, code/absorbing.py, code/oeis_rotation.py, code/analyze.py, code/gen_stats.py, code/residue_track.py.
- code/certify_sweep.py + code/gen_stats2.py — certifier re-derivation of every sweep row and the climb-ending classification on the page (out/certify_sweep*.txt, out/stats2.json).

## Reproduce
    cd code && gcc -O2 -o og og.c -lgmp
    for N in $(seq 3 3000); do for t in 1 2; do ./one_n.sh $N $t; done; done   # ~1 core-hour
    ./og scan 1 9999                                                             # ~15 core-minutes
    ./run_controls.sh
