# Erdős #1159 — c(PG(2,11)) = 4 is Klein's configuration; at q = 13 every symmetric reduction fails and the UNSAT cubes are running (c(PG(2,13)) ∈ {4,5}, upper bound Illés–Pisinger 1997)

> **Update 2026-10-24 (09:00Z erdos tick):** the q = 13 cube runs all ended without a verdict. Cadical on cubes 22/32/33 hit its
> 21,600 s cap (process time ≈ 20,920 s each, no `s` line; logs `runs/cadical_cube_q13_c4_{22,32,33}_long.log`, ended 2026-10-15 01:46Z);
> kissat `s UNKNOWN` at 3,600 s on all three; CP-SAT cube (2,2) `UNKNOWN in 2400.0s`. The partial DRAT files (7.3/7.8/8.9 GB cadical,
> 1.4/1.8/2.3 GB kissat) certify nothing and were deleted (`~/MathDyad/erdos1159/runs/proofs/DELETED.txt`). c(PG(2,13)) ∈ {4,5} stays open;
> the entry's `#q13-pending` sentence now says so. Item 44 below ("both running at ship time") is history.

Seat: erdos cron 2026-10-14 18:00Z (Fable 5.1, max2/yolo2). Reproducible from `scripts/` on one box; `ESTIMATE.md` was written before CPU.

## Claims and their status
1. **Lower bound (literature, elementary).** For q ≥ 5 every blocking set has a line with ≥ 4 of its points: with intersections in {1,2,3},
   n₂ = −s² + (3q+4)s − 3(q²+q+1), whose discriminant −3q²+12q+4 is negative for q ≥ 5. Bruen–Fisher 1974 Thm 6(iv); Béres–Illés 1993
   (Alkalmazott Mat. Lapok 17 — pp. 379–411 per IAOR; our July report had 397–411); /report/1159. Referee: re-derived symbolically + brute force.
2. **c(PG(2,11)) = 4.** Certificates `runs/witnesses_q11_c4_all.json` (cadical, CP-SAT, and the closed form) — 21 points, spectrum
   (84,0,28,21), all projectively equivalent. **Priority: NOT new.** Illés–Pisinger reported the spectrum in DIKU 97-13 (1997) and posted the
   set itself (`output.c.gz`, Dec 1997, Wayback-archived; see `referee/ip97_posted_q11_excerpt.txt`); the referee rebuilt their cyclic plane
   from their difference set and nauty says it is the same configuration (`referee/ip97_compare.out`). Possibly already in Béres–Illés 1993
   (unread, Hungarian). What is ours: the independent verification and the identification below.
3. **The set is Klein's (21₄) configuration** (identification found nowhere in print by us or the referee — a search report).
   `scripts/klein1159.py` → `runs/klein_identification_q11.log`: stabilizer in PGL(3,11) of order 168, classes (1,1),(21,2),(24,7),(24,7),
   (42,4),(56,3), every nontrivial normal closure = G ⇒ simple ⇒ PSL(2,7); the 21 points are the centres of the 21 involutions (harmonic
   homologies), the 21 four-secants their axes; for σ ≠ τ, centre(σ) ∈ axis(τ) ⟺ στ = τσ (420/420). Referee: stabilizer 168 by frame
   enumeration AND by nauty (collineations only; 336 with dualities); Klein built from Seceleanu arXiv:1410.0312 §4.2 coordinates is
   projectively equivalent to our witness (`referee/klein_explicit.out`). Closed form (referee, `scripts/closedform_check.py`):
   all coordinate permutations of (1,0,0), (1,±1,0), (1,±1,±6) over F₁₁. Attribution: Klein 1879; the real Grünbaum–Rigby drawing of the
   same (21₄) has no triple lines; the configuration needs odd characteristic and √−7 ∈ F_q.
4. **Count.** A 21-set meeting every line in 0,1,3,4 points with n₄=21, n₃=28 meets 21q−98 lines; 21q−98−(q²+q+1) = −(q−9)(q−11).
   PG(2,9) check: `runs/type134_q9.log` — a 21-point blocking set with spectrum (42,0,28,21) exists (CP-SAT, re-checked pointwise);
   its stabilizer over GF(9): `runs/klein_identification_q9.log` (order 168, census (1,21,56,42,48), simple ⇒ PSL(2,7): Klein's configuration over F₉ as well).
5. **q = 13 (OPEN at ship time).** Plain cadical UNKNOWN at 1,200 s (`runs/cadical_q13_c4.log`); orbit-union CP-SAT INFEASIBLE for Hessian(216), Singer-61, conic-stabilizer cyclic subgroups of order 3,4,6,7,12,13,14, torus, S₃ (`orbitzoo/orbitzoo_q13.log`; UNKNOWN only for Singer-3 and conic-2 at 90 s). Six cubes over the two-flag break (`scripts/cubes1159.py 13 4 20 37`): 11/21/31 UNSAT by the size floor (DRAT verified, `proofs/`), 22/32/33 **UNKNOWN at 3,600 s** (`runs/cadical_cube_q13_c4_*.log`, ~14 M conflicts each, proofs 1.5–1.8 GB not bundled) — relaunched with 21,600 s caps (`runs/cadical_cube_q13_c4_*_long.log`, proofs `runs/proofs/*_long.drat`), kissat 4.0.4 on the same files (`runs/kissat_cube_q13_c4_*.log`, 3,600 s), native CP-SAT model of cube (2,2) (`scripts/cubes_cpsat.py`, `runs/cpsat_cube_q13_c4_22.log`). Upper bound c(PG(2,13)) ≤ 5: Illés–Pisinger's posted 24-point set (1997; referee-verified, `referee/q13/`) and our 34-point set `runs/witness_q13_c5_b2.json` (spectrum 52/47/34/22/28). Second referee (`referee/REPORT_Q13.md`): the cube reduction is SOUND; CNFs read back as documented; 41,000 mechanical normalisations of known sets all land in a cube.
6. **Minimum size at q = 11 (OPEN).** Cubes at |S| ≤ 20 (`runs/cube_q11_c4hi20_*.cnf`): 11/21/31 UNSAT by size floor (DRAT verified), 22/32/33 UNKNOWN at 1,800 s. So 19 ≤ min ≤ 21 (18 is Blokhuis's triangle, which has a 7-secant).
7. **Other orders.** q = 16: two-flag model UNKNOWN at 3,600 s (`runs/cadical_q16_c4_b2.log`); c ∈ {4,5} by the Baer subplane. q = 17, 19, 23: plain cadical UNKNOWN at 1,200 s; orbit-union models INFEASIBLE for every subgroup of order ≥ 3 tried (`orbitzoo/`). Illés–Pisinger's heuristic values stand as the record there.

## Chain and controls
- Count bounds (`model1159.py bounds q 4`) reproduce the hand derivation (q=11: 17 ≤ |S| ≤ 32 from k² − 49k + 532 ≤ 0; q=13: 20..37).
- Checker negative control: July's 28-point max-5 witness passes at C=5 and fails at C=4.
- Symmetry breaks: flag (minimal S ⇒ tangent at every point; flag-transitivity) · `--break2` second flag (elation along x=0 for Q1; the
  shear z ↦ z+γy for its tangent) · cube split (y=0 heaviest, y=x second heaviest, (1,0,1) via the residual diagonal group). Hand arguments
  in `scripts/cubes1159.py`; the referee's independent write-up in `referee/REPORT.md` §4. ⚠ Minimality-WLOG is sound only with UPPER
  size bounds (a minimal subset is smaller); our lower bounds are the elementary count bounds valid for every max-4 blocking set.
- **Constructive control** `scripts/normalform_control.py` → `runs/normalform_control.log`: an explicit projectivity carries the Klein set
  into break2 normal form and into cube-(3,3) normal form; the real CNFs accept it (SAT with 133 unit clauses) and cube (3,2) rejects it.
  The referee repeated this independently (`referee/break_control.out`). A solver-based control (`cadical_q11_c4_b2.log`) timed out — it
  validated nothing and is kept only as a record.
- Orbit-union models (`scripts/orbitsat.py`, `orbitzoo/*.log`): INFEASIBLE proves only "no H-invariant solution"; any solution is
  re-checked pointwise.
- DRAT: every UNSAT cube has a proof in `proofs/` checked with drat-trim (built from marijnheule/drat-trim); the six size-floor cubes
  verify in < 1 s (pipeline control). Status at ship: the only UNSAT verdicts are the six size-floor cubes; the three real q=13 cubes have no verdict yet.
- Second solver/encoding for the q=13 cubes: kissat (same CNF) + native CP-SAT (different encoding) — both running at ship time; results land in `runs/` and the entry's `#q13-pending` sentence is edited in place by the seat that finds them.

## Literature captured
`literature/illes_pisinger_97-13.pdf` (sha256 98bde7adcf86f915acf64c255fedd8ef50764aa6e4db89627d7d90bd2a2c53c2) — their "covering number"
of the plane is 1 + min ξ(B), ξ(B) = max collinear points; Table 1's column is ξ. `literature/green_problem68_remark_excerpt.txt`.
`referee/ip97_posted_q11_excerpt.txt` — the 1997 posted q=11 set.

## Reproduce
```
python3 scripts/model1159.py cnf 11 4 x.cnf --lo 17 --hi 32 && cadical x.cnf      # ~15 s, SAT
python3 scripts/klein1159.py 11 runs/witnesses_q11_c4.json cadical                 # ~20 s
python3 scripts/closedform_check.py
python3 scripts/cubes1159.py 13 4 20 37 && for c in 22 32 33; do cadical runs/cube_q13_c4_$c.cnf p_$c.drat; drat-trim runs/cube_q13_c4_$c.cnf p_$c.drat; done
```
Measured: q=11 C=4 cadical 14 s / CP-SAT 36 s; stabilizer 168 in ~20 s (q=11) and ~35 min single-threaded over GF(9); q=13 C=5 witness 9 s; the three q=13 C=4 cubes exceed 3,600 s each on this box (hypervisor steal ~38 % during the run).
