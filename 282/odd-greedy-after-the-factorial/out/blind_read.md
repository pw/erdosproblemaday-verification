# Blind read of the draft page (Opus, with tools), 2026-11-09 ~10:00Z — objections and what we did

1. Climb-ending labels wrong for ~1,311 climbs (always took the break at R+1; when the step from R is not the ramp
   step, the climb broke at R, e.g. 3/(2·10!−1) breaks at the prime 13). FIXED: endings now classified from
   certify.py's own recomputed s, g at R (certify_sweep.py, gen_stats2.py); every sweep row re-derived.
2. "N! alone cannot pay for … checked all 2,712" was vacuous (every number past N has an over-demanded prime).
   REMOVED (and composite_check.py dropped from the bundle).
3. Brown's 50! count of 6 holds only for m = 50!/2 (our script prints 4 of 10 for m = 50!); "up to 100" -> "between
   50 and 100". FIXED.
4. Bloom did not confirm the 1980 book's wording ("Although this is not made clear in [ErGr80], I assume …"). FIXED.
5. 2086/2381's numerators peak at 115,811, not ~1.2·10^7. FIXED.
6. Table tails truncated to 8 entries. FIXED (full tails).
7. Corrupted-claims count stale. FIXED (109, every position of five claims).
8. "100 times further" is 10× in b (100× in fractions). FIXED.
9. Brown table: differences at p−2 are not all explained by "residue 0 is favourable"; 41 of 44 rows match. FIXED
   (all 44 rows now checked by brown_cover.py).
10. Pihko Thm 3.5 under #282's rule fails at p = 3 (2/3 -> 2,1,2,1): say p ≥ 5. FIXED.
11. Brown quote "4,5,6,...,500"; "favorable". FIXED.
12. Squares variant wording ("believe not — perhaps it fails to terminate almost always"). FIXED.
13. Heuristic overclaimed ("fixed odds", "do not improve"); covered share varies 18–66%; mean overshoot grows with
    N. FIXED (rewritten with the band means 5.3 / 7.2 / 6.8, max 56).
14. z ≡ 0 bullet ignored other primes; at kp the result is k/(…), not a unit fraction. FIXED.
15. Bailey's "exhaustive computer search" must be addressed. FIXED (range not recorded).
16. N ≤ 3000 rested on og alone for most N. FIXED: certify.py re-derives every sweep row.
Also: labels (c)/(d) now defined on the page.

# Second blind read of the revised page (Opus, with tools), ~10:50Z — all applied
- Table and the 5,802-climbs sentence: no objections (all cells/counts match stats2.json; 8 rows re-run identical;
  every cut is by a prime whose square does not divide R+1; no climb ends at a composite).
- Band means 7.2/6.8 -> 7.1/6.7; "max in any band 56" -> overall max 56 at N = 2,146; "as prime gaps do" dropped
  ("tends to grow"); the five tabulated primes named. Brown: only the 50! count separates m = N!/2 from m = N!;
  "residue 0" -> "m ≡ 0". Bloom: "he assumes". Stein credit attributed to the problem page. Verification paragraph:
  "among them", "about 1,400", controls/cert-sweep scripts named; controls.txt regenerated after the Brown upgrade.
