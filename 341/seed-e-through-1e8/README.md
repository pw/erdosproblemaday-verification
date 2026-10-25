# Erdős #341 — the last seed in [12]: E = {1,4,8,10,11,12} through 10⁸, its structure, and why Li's mechanism cannot reach it

Seat: 2026-10-15 00:00Z erdos cron (Fable 5.1, max2/yolo2 sub). Entry: `/day/341-the-last-seed-in-12-through-1e8`.
Claim labels: (a) elementary · (b) rigorous modulo a named theorem · (c) plausible/unverified · (d) computer-assisted.

## Claims

1. **(d) No gap period through 10⁸ (exact scope).** The Dickson-rule greedy extension of E computed exactly to 10⁸ has 15,621,235
   elements; the gap word's suffix from term 7,810,617 has no period ≤ 3,905,308 terms (border array, C and Python; periodic
   controls). Hence no gap period of ≤ 3,905,308 terms begins at or before term 7,810,617 (a ≈ 5·10⁷); a membership
   period q with such an onset induces a gap period ≤ δq + 2·disc, so membership periods up to ≈ 2.5·10⁷ are excluded. July's bound:
   no membership period q ≤ 20,000 beginning at or before 479,993. Nothing is said about longer periods or later onsets.
2. **(d) Structure = a single-rotation coding with five arcs and fuzzy edges.** Residue census: every class mod every m ≤ 400 within
   [0.83, 1.18] of the mean on [5·10⁶, 10⁷] (and over [10⁷, 10⁸] no class modulo any <em>m</em> ≤ 10,000 is empty (the most depleted is 0.436 of the mean at <em>m</em> = 8528, the fullest 1.666 at <em>m</em> = 8528)). Exact (overlap-normalised) agreement: record chain 130/253/636/889/
   1655/9547/27875, best 98.9% for every shift ≤ 4·10⁷. **Spectrum** (`spectrum.py` v3: exact DTFT peak location,
   sidelobes excluded, integer-relation search to |c| ≤ 50; `spectrum_F_E_eq_1e7_v3.log`; the referee's `referee/ref_spectrum.py`): the 40
   largest peaks carry 85% of the variance; the two largest f₁ = 0.438672574, f₂ = 0.138367745 satisfy 4f₁ + 9f₂ ≡ 0 (mod 1) to 0.015 bin ⇒
   cyclic module ℤg, g = −f₁ − 2f₂ = 0.28459193622; 36/40 peaks are multiples of g (3 sidelobes + 1 stray are not); 81–83% of the
   variance on ℤg. CF of g = [0;3,1,1,17,1,1,1,1,2,1,2,1,2,1,12,…], convergent denominators 3,4,7,123,130,253,383,636,1655,2291,6237,8528,
   23293,31821. **Phase picture** (`phase_core.py`, `phase_arcs.py`, logs `phase_core_E_1e7.log`, `phase_arcs_E_1e7.log`): at 1,000-bin
   resolution on [9·10⁶,10⁷]: five core arcs (11.0% of the circle, 34 exceptions in 110,000), deep complement (79.5%, 42 exceptions in
   795,003), edge zones (9.5%, 48.7% membership); same arcs on [2·10⁶,3·10⁶]. The cores are sum-free on the circle but their sumset covers
   only 59% of it; S+S fills the complement at uniform density (recurrence 0 violations on the window) via the edge elements.
   At 10⁸ (`phase_core_E_1e8.log`, windows at 2·10⁷, 5·10⁷, 9.9·10⁷): core 10.8–11.1% with 16–35 exceptions per ~110,000, deep 79.5–79.8%
   with 39–43 exceptions per ~797,000, edge 9.1–9.6% at 49–51%; `census_31821_1e8.log`: mod 31,821 77.9% of classes empty in each of three
   disjoint 3·10⁷ windows with ~3% turnover between windows (drift, not a rule); mod 8,528 28% empty per window and 0 empty in all three.
   `spectrum_F_E_eq_1e8_v3.log`: the (4,9) relation again to 0.015 bin; 85.4% of variance in 40 peaks; 84.7% within 1 bin of module points.
   Post-transient discrepancy: 215 vs 480/1060/765 (random) on [2·10⁶,10⁷]; 1,064 vs 3,482/2,174/2,673 on [2·10⁷,10⁸] (`analyze_1e7.log`,
   `analyze_1e8.log`) — grows, about a third of random. Factor complexity: sample-limited, no exponent claimed.
3. **(c) Conjecture.** E's greedy extension is the coding of an irrational rotation by g on a five-arc window plus a residual confined
   to the arcs' edges; it is not eventually periodic. Not proved. g rational with a huge denominator is indistinguishable from the data.
4. **(d) Li-type shields below 49.** For every pure doubling cycle P = {x·2^i mod M} at every modulus M ≤ 48 (94 cycles, lengths 2–36,
   `shield/cycles_all_below_49.txt`), Li's Lemma 3.1 conditions (cover / avoid incl. D+P / only diagonal rail pairs reach a rail — the
   last enforced as infeasibility when a mixed rail sum lands on a rail) are UNSAT for 79: 50 by (PP) — all 36 cycles of length ≥ 8 and the
   14 four-/six-cycles at M = 5,9,10,15,18,20,25,27,30,35,36,40,45 — and 29 by CaDiCaL incl. all 12 three-rail cycles (M = 7,14,21,28,35,42)
   and all 6 five-rail cycles (M = 31). The 15 SAT instances are the two-rail cycles {M/3, 2M/3}, 6 ≤ M ≤ 48 (M = 3 UNSAT). Controls:
   M = 49 SAT; admits Li's B/D when forced (`shield/shield_sat.py`); UNSAT when B is forbidden. Census = `shield/shield_all_v3.log`
   (v1/v2 kept: v1 capped L ≤ 6 and did not enforce (PP); v2 enforced it on the L ≤ 6 list). Referee extensions (`referee/`): independent
   encoder reproduces 50/29/15; unions of ≥ 2 cycles with one of length ≥ 3, M ≤ 48: 320 instances, none SAT; MaxSAT at M = 49: min
   |D| + 2|B| = 17 = Li's.
5. **(d) Controllers.** Two-rail forced dynamics are M-independent (carries 0,1); from every initial content on q ≤ 1, 2, 3 (16/64/256
   contents, both rules) a period ≤ 9 is DETECTED on [2¹⁵, 2¹⁶) (`shield/census_controllers.log`) — detected, not certified. Control:
   three rails at M = 49 show no period on the same test from 23 of 27 contents (`shield/census2.c`, general carries; the 13/14 Oct
   single-wrap tool agrees); the referee checked the model's rail contents against the real greedy for 1,500 blocks at M = 6 and 49.
6. **(d) Census one step up.** Of the 4,096 seeds with largest element 13, <strong>4,094 certify</strong> — every one at the first stage (greedy to 2·10⁵), the slowest with membership period 743 ({1, 2, 6, 9, 10, 11, 13}) and the latest onset 1,653 ({2, 5, 7, 11, 12, 13}) — and two resist: {3, 5, 8, 10, 13} and {2, 4, 6, 9, 10, 11, 13}. Of the 8,192 seeds with largest element 14, <strong>8,188 certify</strong> — two of them only at the second stage, with the largest certificates in the whole census: {1, 2, 4, 9, 10, 12, 13, 14} has membership period 18,673 from 586,748, and {1, 4, 5, 7, 10, 12, 13, 14} period 87,921 from 677,409 (the finite certificate was checked through 2·677,409 + 87,921 − 2) — and four rows resist: {2, 6, 8, 9, 10, 11, 14}, {3, 6, 8, 9, 12, 14}, {4, 6, 8, 9, 10, 13, 14}, and {3, 5, 8, 10, 13, 14}, which is not new (14 is the greedy's own next term after {3, 5, 8, 10, 13}, so the two seeds generate one sequence). Together with July's [12] that is 16,377 of 16,383 nonempty seeds inside [14] with an all-future certificate, zero tool errors, and <strong>six distinct resisting sequences</strong> — every one with no gap period through 10⁷ at the border-array scope, no residue rail at any <em>m</em> ≤ 400, a sharp-peaked spectrum on a frequency module of rank one or two, and a near-period ladder that never closes. No seed anywhere in the census sat between the two behaviours for long: it certifies by 2·10⁶ or it belongs to the class. What these six seeds have in common beyond that, we do not know; nothing in their elements announces it, and which seeds do this is open.

## Chain (what produced each number)

- `fast341.c` — second bitset generator (carry-form shift-or, loop truncated at N−t). `greedy341.c` — the 13 October generator
  (copied from `~/MathDyad/erdos341/`). Controls: `cmp` byte-identical on E@2e6, E@1e7, Li-equal@1e7, Li-distinct@1e7
  (`controls.log`); July SHA-256 of membership bits through 500,000 reproduced (`analyze_1e7.log`); referee's set-based `ref_greedy.py`.
- `F_E_eq_1e8.log` + `F_E_eq_1e8_elems.u32` (62 MB, kept in `~/MathDyad/erdos341e/`; SHA in `F_E_eq_1e8_elems.sha256`) — the 10⁸ run.
  `analyze.py` (v2: overlap-normalised autocorrelation + exact agreement at the strongest candidates; post-transient discrepancy with
  random comparators; half-word complexity) → `analyze_1e8.log`, `analyze_1e7.log`.
- `verify341.c` — from-scratch recurrence check on windows (iterates over summands). `verify_1e8.log`; controls in `controls.log`.
- `spectrum.py` (v3) → `spectrum_F_*_v3.log`; `phase.py`, `phase_arcs.py`, `phase_core.py` → `phase_*.log`; `mismatch_residues.py` →
  `mismatch_residues_1e7.log`.
- `shield/shield_sat_L.py` + `shield/cycles_all_below_49.txt` → `shield/shield_all_v3.log`; `shield/shield_sat.py` (3-rail-only, with the
  forced-Li and no-B controls); `shield/census2.c` → `shield/census_controllers.log`.
- `census13/census.py` (+ `certify.py`: `L = max(L, M+1)` for proposals with N ≤ max seed; exit 3 on any exception; the driver accepts only a
  clean "NOT CERTIFIED" with rc 1 as a failure) → `census13.tsv`, `census14.tsv`, `survivors13.txt`, `survivors14.txt`, `census_controls.log`
  (incl. the standalone re-run of every survivor). `census13_run1_buggy.tsv` is the first run with the crash-as-unresolved failure.
- `live/` — erdosproblems.com/341, proof-claims tab, forum, pulled 2026-10-15 through the Hetzner box (unchanged since 13 October).
- `lit/` — Green's open-problems list (Problem 7), OEIS negative + positive-control queries.
- `entry/BLIND_READ.md` — the blind consistency read of the rendered page (53 findings, all applied; see `referee/APPLIED.md`).
- `referee/` — the hostile Opus referee's brief, REPORT.md (verdict: GAP in the first draft's two-frequency claim; HOLDS WITH FIXES
  otherwise), its scripts and logs, and `APPLIED.md` listing what was changed in response.

## Reproduce

```
gcc -O3 -march=native -o fast341 fast341.c && ./fast341 10000000 F_E_eq_1e7 0 1 4 8 10 11 12
python3 analyze.py F_E_eq_1e7_elems.u32                      # ~20 s; SHA through 500000 must print 3a045efe…
gcc -O2 -o verify341 verify341.c && ./verify341 F_E_eq_1e7_elems.u32 0 12 4000000 200000   # 0 violations
./verify341 F_E_eq_1e7_elems.u32 0 12 4000000 200000 4000037                                 # negative control: violations
cd shield && ~/.venv/bin/python shield_sat_L.py 49 7 3 && ~/.venv/bin/python shield_sat_L.py 7 1 3      # SAT / UNSAT
./census2 49 7 3 0 1 65536 8000                                                               # 23 of 27 aperiodic
```
