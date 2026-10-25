# What was done with the hostile referee's report (REPORT.md, 2026-10-15 ~01:1xZ)

Verdict received: GAP AT the spectral/structural characterisation (two-frequency claim false); HOLDS WITH FIXES elsewhere.

| # | Finding | Action |
|---|---------|--------|
| A1 | 4f₁ + 9f₂ ≡ 0: the module is cyclic (g = 0.28459193622), "two-frequency quasicrystal" false | Title, summary, headline, body ¶3, README rewritten around the single rotation g; `spectrum.py` v3 adds an integer-relation search among candidate generators (|c| ≤ 50) and the explicit rank-1 reduction; the first draft's error is stated in the entry |
| A2 | not a rotation coding either (agreement 0.967–0.974 at convergents); "model set" unsupported | The phase instruments (`phase.py`, `phase_arcs.py`, `phase_core.py`) measured what the rotation does and does not explain: cores exact, deep complement exact, edge zones ≈ 10% at ~49% membership; "model set/quasicrystal" removed; the reading is labelled (c) and the mechanism (edges complete the sumset) is stated with its data |
| A3 | statistics of the test (chance null, 1 vs 2 bins, parabolic refinement, long-period periodic sets) | v3 locates peaks exactly and excludes sidelobes; both tolerances are reported; the long-period caveat is in the entry's "not claimed" and in the spectrum log's footer; S13's rank corrected to 2 (the S13 sentence) |
| A4 | "no peak at a rational frequency" uncomputed | Sentence deleted; the m = 328 coincidence (26·328 = 8,528, a convergent denominator) is explained by the rotation |
| A5 | "no rail/no shield" true only for m ≤ 400; 31,821 has 79% empty classes | Scoped to m ≤ 400 (+ the m ≤ 10,000 census on [10⁷,10⁸]); the near-period moduli are discussed as the rotation not having wrapped; title changed |
| A6 | factor complexity sample-limited; "zero entropy" unsupported | Exponent and "zero entropy" removed; `analyze.py` v2 reports the second-half p(k)/windows |
| A7 | discrepancy at 10⁷ inside the transient and ≈ random; post-transient 215 vs ~890; S13 worse than random | `analyze.py` v2 computes post-transient discrepancy with three random comparators; body quotes 215 vs 480–1,060; S13 "same type" withdrawn |
| A8 | autocorrelation not overlap-normalised | `analyze.py` v2 normalises by overlap and reports exact agreement at the 60 strongest candidates; the 10⁸ sentence uses exact agreement |
| A9 | mismatch-uniformity sentence had no artefact | `mismatch_residues.py` + log; sentence removed from ¶3 (kept in the bundle as a measurement) |
| A10 | Calkin–Erdős misquoted; their S_α theorem relevant; Steinerberger | Exact quote; the never-complete theorem is now the frame of the mechanism paragraph |
| B12 | period-test wording ("no period at all") | Title/summary/body state the exact scope; membership-period bound derived with the discrepancy |
| C14 | "no Li-type shield below 49" false as stated | Everywhere: "for every doubling cycle of three or more rails"; two-rail survivors described |
| C13 | referee's extensions (independent encoder; unions of cycles 320/0 SAT; MaxSAT min 17 at 49) | Added to ¶4 with credit; artefacts in `referee/` |
| C15 | predecessor-rail diagonal; D+P in avoid; incomplete modulus list; 16 vs 15 cycles | Fixed in ¶4 |
| D17 | controller periodicity over-claimed | "showed a period ≤ 9 on [2¹⁵,2¹⁶) — detected, not certified"; headline/summary say "periodic in every test" |
| E19 | driver still reads a crash (rc 1) as not certified | `certify.py` wraps its body: any exception → exit 3; driver accepts only rc 1 with a stdout ending "NOT CERTIFIED"; every survivor re-run through the standalone path (`census_controls.log`) |
| F20 | "smallest seed on record" | "by largest element"; {3,5,8,10,13} named as five elements |
| F21 | "the seven" reading | Attributed to the convergent denominator 7 of g |
| F22 | README chain pointers stale | README chain rewritten |

## Blind consistency read (entry/BLIND_READ.md, 53 findings, ~03:3xZ)
All 53 applied: census total 16,376 (seven resisting seeds, six sequences); the "intermediate fractions" claim replaced by the measured
‖qg‖ picture (the ladder does not track ‖qg‖; 383/2,291/6,237 are better approximations but not records); four flat cores + one fully
fuzzy arc with exact counts; "exact" → "to within a few dozen exceptions per million"; bounds stated at the data's exact edge (term
7,810,617 = integer 49,993,396; membership periods ≤ 2.49·10⁷; 1,537 defined); slug and card de-overclaimed
(`/day/341-the-last-seed-in-12-through-1e8`); SAT breakdown completed to 94; 27 initial contents defined; labels keyed and used
consistently ("Our conjecture, label (c)"); scope "[13]" → "[49]"; Calkin–Erdős credited for the instance, not the general case; the
rules and which rule E's results use stated once; gap shares for every survivor; notation and wording items.
