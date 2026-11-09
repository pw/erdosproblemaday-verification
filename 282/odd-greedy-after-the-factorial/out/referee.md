# Hostile referee seat (Opus, with tools), 2026-11-09 ~09:30–09:45Z — verdicts as returned

Built two independent engines in /tmp/ref282 (per-prime residue engine padic.py; fully exact engine with the real
used-denominator set, brute.py / brute_scan.py).

- C1 (hand-off): HOLDS. Prefix rule max(nunc, prev+2) is correct because the used set before hand-off is exactly
  3, 5, …, prev with no gaps. Exact engine matches `og scan 1 399` on all 32,364 fractions (checksum c7b9b7b1b5a61c0d).
- C2 (precision): HOLDS for lengths. BUG: og's trace/maxnum omitted the exact-prefix numerators (only 3/5 affected in
  the factorial family; sweep row "3 1 3 4 4 2 | 1"). Fixed after the report: prefix numerators now printed; 996 sweep
  rows re-run, one changed (N = 3, trace length 2 -> 3).
  Identical full traces for N = 30, 100, 251, 500, 501, 1000, 1234, 1777 (both families); rows for 2817, 2986, 2994,
  2999 (t = 2) and both N = 5000 rows reproduced.
  Mutations: parity swap caught; g = 1 caught (BUG exit 3); wrong n offset caught; termination count off by one caught
  by lengths only (traces identical); hand-off threshold 5 -> 3 caught by the scan histogram; fast-path a·s guard
  removal survives (guard never fires on these inputs; not a bug, untested).
- C3 (parity): HOLDS, for every reduced a/b with b odd (x < 1/3 not needed); 32,364 fractions with b < 400, 0 failures.
  Say that length counts the final 1/b.
- C4 (fixed points): HOLDS WITH FIXES. 1,592,907 map checks, 738,891 fixed-point checks, 6,504 prime steps with
  g = p <=> z_{p-1} = 0, 6,365 checks of z_p = -z_{p-1}^2, 0 failures (N = 4..160). Fixes: the map holds whenever
  p ∤ k (not only k < p); "z = -1" means p is not the obstruction, not that the climb passes; the numerator never
  equals p (step gives s = p, g = p, next numerator 1). Applied.
- C5 (numbers): HOLD (501, 519, 1011, 1005; 1000/t=1 ramps to 1012, ends at 1013). Sweep complete, 5,996 rows.
- (iii) 502 explanation: FAILS as first written. "500! has only one 251" is necessary, not sufficient (3/(2·500!−1) also
  has one 251 and passes 502). Mechanism: z mod 251 leaves -1 after 251; for t = 1 it falls into the absorbing 0 at
  numerator 378 and stays, so 251 | b at 501 and g = 251. For t = 2 it never reaches 0 (z = 159 at 520). With two
  copies (N = 502) z stays -1 mod 251. Same shape: N = 750 breaks at 758 = 2·379; 3/(2·1000!−1) at 1006 = 2·503.
  Reproduced independently by residue_track.py (numerator 378; t = 2 residue 159 at 520). Page text rewritten.
