# Erdős #188 — exact finite certificates for the two known lower bounds, an audit of the 2026 upper bound, and what the ℓ₆ search did and did not do

**Problem** (erdosproblems.com/188). Colour the plane red/blue with no two red points at distance 1. Let k₁₈₈ be the least
k such that some such colouring has no k blue points in arithmetic progression with common difference of length 1 (an ℓ_k, in
the notation E² → (ℓ₂, ℓ_k) of Erdős–Graham–Montgomery–Rothschild–Spencer–Straus).

**State of the problem on 2026-10-14** (snapshots: `logs/erdosproblems_page_188_2026-10-14.txt`, `logs/erdosproblems_forum_188_2026-10-14.txt`,
`logs/state_sources_2026-10-14.txt`):
* Lower bound: k₁₈₈ ≥ 6 — Tsaturian 2017 (E² → (ℓ₂, ℓ₅)); before that ≥ 5 — EGMRSS 1975, Theorem 1′ (E² → (ℓ₂, ℓ₄)).
* Upper bound: k₁₈₈ ≤ 6330 — Currier–Mody–Xie–Zhang, arXiv:2606.17194 (v1 15 Jun 2026, v2 31 Aug 2026), Theorem 1.2.
  Before that, Conlon–Fox 2019 Theorem 1.1 (|K| > 10^{4n} log₂ R, n = 2, K = ℓ_m, R = m) gives m ≈ 3.16·10⁹ as stated
  (the forum's 2.15·10⁹, A. Sagdeev, Feb 2026, reads the log as natural; CMXZ quote 10¹⁰). The page's "k ≤ 10000000 ('more or
  less')" is Erdős–Graham's unproved remark. **The main page still carries 10⁷; the 6330 is only in the forum (Alfaiz, 17 Sep 2026).**
* teorth database: `open` (tracker row in `logs/state_sources_2026-10-14.txt`). Proof-claims tab: none. Not in the OpenAI
  2026-10-06 catalogue (grep in the same log).

## 1. What is in this bundle

### 1a. Exact finite certificates of the two lower bounds (ours as verification; the theorems are EGMRSS's and Tsaturian's)
A finite point set P ⊂ ℝ² with the hypergraph {unit-distance pairs} ∪ {unit-spaced collinear k-runs} has no colouring with
red independent and blue run-free iff the CNF
    (¬rᵢ ∨ ¬rⱼ) for every unit pair,  (r₁ ∨ … ∨ r_k) for every k-run
is UNSAT; restricting any plane colouring to P satisfies every clause, so UNSAT proves E² → (ℓ₂, ℓ_k) for all plane colourings.
Two WLOG facts reduce the problem further:
* **(W1)** a colouring with no blue ℓ_k has a red point (an ℓ_k is all blue otherwise); translate it to the origin. The unit
  clause `origin red` is sound.
* **(W2)** for any d > 1/2 the rotation ρ_d about the origin by θ_d with 2d·sin(θ_d/2) = 1 moves every point at distance d by
  exactly 1. If P is a point at distance d from the red origin, P and ρ_d(P) are at distance 1, so one of them is blue; composing
  the colouring with ρ_d⁻¹ if necessary (an isometry fixing the red origin) we may assume **P itself is blue**. One such
  assumption only — it spends the one rotation freedom. (This is exactly the final step of Tsaturian's proof, with d = 5.)
Points are the unit triangular lattice ℤ[ω] (ω = e^{2πi/3}) and its images under rotations about lattice points by ±θ_d;
cos θ_d = 1 − 1/(2d²), sin θ_d = √(4d²−1)/(2d²); we use d with d² a norm in ℤ[ω] so that lattice points at distance d exist.
θ_{√3} is the Moser-spindle angle (cos = 5/6), e^{iθ_{√3}} = (5 + √−11)/6; the real coordinates of θ_{√3}-rotated points lie in ℚ(√3, √11) (θ₃-rotated points, present in the full instances but in no core, lie in ℚ(√3, √35)).

| theorem | instance (`config188.py` flags) | size | cadical | minimal core (`mus188.py`) | exact check |
|---|---|---|---|---|---|
| E² → (ℓ₂, ℓ₄) [EGMRSS75 Thm 1′] | `--R 10 --k 4 --ds sqrt3 --centers 0 --origin-red` | 1,099 pts · 3,108 pairs · 2,682 ℓ₄ | UNSAT | **15 points** (8 lattice + 7 rotated by +θ_{√3} about 0), 11 unit pairs, 4 ℓ₄, origin red | PASS |
| E² → (ℓ₂, ℓ₅) [Ts17 Thm 1.1] | `--R 12 --k 5 --ds sqrt3,3 --centers 3 --origin-red --blue 5,0` | 76,861 pts · 519,756 pairs · 227,151 ℓ₅ | UNSAT 1.3 s | **111 points** (46 lattice + 65 rotated by ±θ_{√3} about 9 lattice points), 95 unit pairs, 29 ℓ₅, origin red, (5,0) blue; radius 5.21 | PASS |
| E² → (ℓ₂, ℓ₅), second encoding | `--R 12 --k 5 --ds sqrt3,3 --centers 6 --rot-radius 4 --origin-red --blue 5,0` | 30,625 pts · 208,056 pairs · 94,077 ℓ₅ | UNSAT 0.4 s | **69 points** (30 lattice + 39 rotated by ±θ_{√3} about 7 lattice points), 63 unit pairs, 16 ℓ₅, origin red, (5,0) blue; radius 6.02 | PASS |

`verify_core.py` rebuilds every core point **exactly** (sympy) from its provenance (lattice coordinates + rotation word); checks
that every pair clause is a pair at squared distance exactly 1, every run clause has exactly k points, exactly collinear and
unit-spaced in order, and the unit clauses are the origin (positive) and one lattice point ≠ 0 (negative); asserts that the
geometrically checked clauses are exactly the propositional core; re-solves the core with a second solver (minisat22); checks
minimality (every single-clause deletion is SAT — 16/16, 126/126, 81/81); and runs two negative controls (rebuilding every rotated
point with the wrong angle makes 1/11, 29/95, 19/63 pair clauses fail the unit test; a corrupted run fails). The hostile referee seat also
re-derived all three cores with an independent Fraction-arithmetic checker on the basis {1, √3, √11, √33} (`referee/`, with both referee reports).
Full instances: minisat22 and glucose4 return UNSAT on all three (`controls/controls.log`); cadical's DRAT proofs (252 / 2,459 /
4,654 bytes) pass drat-trim (`s VERIFIED`, same log). `config188.py` with the flags above regenerates the instances byte-identically.

The 15-point certificate is **not** EGMRSS's own figure (theirs runs ℓ₄'s along the sides of an equilateral triangle on the circle
of radius √3 and argues by cases over its vertices): here the red origin makes the eight unit-circle points of the two lattice
copies blue; the lattice point (2,1) at distance √3 lies on two ℓ₄'s, each ending at a point at distance √7, and the two
far ends are a unit pair, which forces (2,1) red; its θ_{√3}-image is forced red the same way; the two are at distance 1.
The ℓ₅ certificates use only the Moser angle θ_{√3} — the same angle Tsaturian's Lemmas 2.2 and 2.3 use (his "red centre,
rotate the three points by 1" steps are rotations at circumradius √3), plus W2 with d = 5, which is his final step. We also
supplied the θ₃ generator (cos 17/18); it is never used in any core. What is new is only the shape: a single finite configuration
of 69 (or 111) points inside radius ≈ 6 of the red point, with its UNSAT proof checked by a third party, instead of six lemmas.
Minor: Tsaturian's Lemma 2.2 should read "side length 3" (not √3), and its proof's "Suppose that blue points A, B, C" should read red.

Controls on the apparatus (`controls/`): the bare lattice is SAT (`lat_k5`; for every k ≥ 3 by hand — red = one class of the
proper 3-colouring of ℤ[ω] has no red ℓ₂ and no blue ℓ₃ on any lattice line); rotations about the origin only are SAT for k = 5, 6
with or without W1 (`t0_*`); the no-red-T₃ branch of Tsaturian's proof closes on the bare lattice already at R = 8 (`noT3.py`: origin red, (5,0) blue, no red
T₃, R = 8, 10, 12 all UNSAT — his Lemma 2.6 says that branch's lattice colouring exists and is unique, and in it points at distance 5
share a colour, which the W2 assumption contradicts), while the red-T₃ branch needs the rotations; with θ₅ copies added and **no** W2 unit the ℓ₅ instance
(`ladder1` `c3_k5`) is UNSAT too (7.9 s) — the θ₅ generator internalises W2. Matched ℓ₅ instances at centre radius 4 with
rot-radius 4: UNSAT with (5,0) blue in 0.28 s, SAT with (6,0) blue, SAT with no W2 (`logs/controls5.log`); (6,0) blue stays SAT
at centre radius 6 — the 5-periodic lattice patterns of Tsaturian's Lemmas 2.5/2.6 allow it.

### 1b. Audit of Currier–Mody–Xie–Zhang Theorem 1.2 (k₁₈₈ ≤ 6330) — HOLDS AS READ
`cmxz_audit.py` / `logs/cmxz_audit.log` recompute every constant of §3.1 independently: the lattice spanned by (3/2, 0) and
(3/4, √3/4) is hexagonal with spacing √3/2 (the pdf's √ is lost by text extraction; the statement is right), Voronoi hexagons of
diameter exactly 1·(1−ε); |z(D)| = 18 (cells within distance 1: rings at centre distance 0.866, 1.5, 1.732; the √7 ring has gap
1.32 > 1); wall-line spacing 0.4330 ≥ 1/3 and 69.3m ≤ 100m lines; Milnor–Thom count (50·100m²/4)⁴ = 2⁴5¹⁶m⁸ (exact);
Janson/Suen exponent −μ+Δe^{2δ} = −0.0155711…·m with p = 1/19 (the maximiser of p(1−p)¹⁸; E[XᵢXᵢ₊₁] = 0 because adjacent points
are at distance 1, at most 3m pairs at index distance 2–4 each ≤ p²(1−p)¹⁸, δ ≤ 8p(1−p)¹⁸, dependency graph valid by their Lemma
2.7); and the crossover: with the exponent rounded to 0.01557 as the paper prints it, the expected number of all-blue admissible
collections is < 1 exactly from m = 6330; with the unrounded exponent from m = 6329. The proof is purely probabilistic — no explicit
colouring is exhibited.

**Remark (a tightening that falls out of the same proof).** The progression has three degrees of freedom. Parametrise it by
(x₁, y₁, t = tan(θ/2)), so q_j = (x₁ + (j−1)(1−t²)/(1+t²), y₁ + (j−1)·2t/(1+t²)); for a wall line F(x,y) = ax + by + c the sign of
F(q_j) equals the sign of (1+t²)(ax₁ + by₁ + c) + (j−1)(a(1−t²) + 2bt), a polynomial of degree 3 in (x₁, y₁, t). Theorem 2.5 (as
the paper states it, from Matoušek Thm 6.2.1) with D = 3, N = 3, M = 100m² ≥ N bounds the realisable sign patterns by (5000m²)³
instead of (1250m²)⁴. The parametrisation misses θ = π, but every θ = π progression read backwards is a θ = 0 progression with
the same cell set, and the all-blue event depends only on the set, so the union bound loses nothing. The same Lemma 3.2 then
gives **E² ↛ (ℓ₂, ℓ₄₉₁₇)**, i.e. k₁₈₈ ≤ 4917 (3 ln(5000m²) − 0.0155711m is +0.005 at 4916, −0.009 at 4917). Not claimed, for
orientation only: the exact line count 69.3m would give 4840, and optimising p against the full exponent (p ≈ 0.0416, rate −0.01607)
a little more. Label (b):
rigorous modulo Theorem 2.5 as stated. This is bookkeeping, not an idea; the real losses are elsewhere (§3).

### 1c. The ℓ₆ search (k₁₈₈ ≥ 7?) — none found, nothing refuted
The same apparatus with k = 6 and matched ℓ₅ twins (`logs/ladder1.log`, `logs/probe6.log`, `logs/ladder3.log`, `logs/controls5.log`).
All runs: R = 12 unless noted, origin red, `nice 19`, cadical:

| configuration | W2 point | ℓ₅ twin | ℓ₆ |
|---|---|---|---|
| d ∈ {√3,3,5}, centres ≤ 1, full patches, R = 10 | none | SAT 0.4 s | SAT 0.8 s |
| d ∈ {√3,3,5}, centres ≤ 2, full patches, R = 10 | none | SAT 6.1 s | SAT 34.7 s |
| d ∈ {√3,3,5}, centres ≤ 3, full patches, R = 10 | none | **UNSAT 7.9 s** | unresolved at 1800 s (cap) |
| d ∈ {√3,3}, centres ≤ 3, rot-radius 4 | (6,0) | SAT 0.4 s | **SAT after 5,439 s** (10800 s cap; `l6/l6_c3_b6_long.sol`, rechecked from coordinates by `l6/check188sol.py`: 0 violations, k = 5 control fires 1,542) |
| d ∈ {√3,3}, centres ≤ 4, rot-radius 4 | none | SAT 0.4 s | SAT after 981 s |
| d ∈ {√3,3}, centres ≤ 4, rot-radius 4 | (6,0) | SAT 0.4 s | unresolved at 1200 s |
| d ∈ {√3,3}, centres ≤ 4, rot-radius 4 | (5,0) | **UNSAT 0.3 s** | unresolved at 10,800 s (cap) |
| d ∈ {√3,3}, centres ≤ 6, rot-radius 4 | (6,0) | SAT 0.7 s | unresolved at 3600 s (cap) |
| d ∈ {√3,3}, centres ≤ 6, rot-radius 4 | (5,0) | **UNSAT 0.4 s** (the 69-point core) | unresolved at 3600 s (cap) |
| d ∈ {√3,3}, centres ≤ 8, rot-radius 4 (57,469 points) | (6,0) | not run | unresolved at 3600 s (cap) |

What this says. Every ℓ₆ instance that resolved is SAT at a size where its ℓ₅ twin is SAT too, so it carries no information
about ℓ₆ specifically. The informative instances — the three whose ℓ₅ twin is UNSAT in 0.3–8 s — are ≥ 2,500 times harder for
cadical (the easy SAT took 981 s against 0.39 s for its twin) and unresolved at 1200–1800 s; with longer caps (03:00Z seat, 14 Oct) the radius-3 (6,0) instance is SAT (5,439 s; a valid ℓ₆-free patch, independently rechecked), the radius-4 (5,0) instance unresolved at 10,800 s (cap), and the radius-6 pair timed out at 3,600 s — the longer runs are logged in `l6/`; the sentence that follows was written before they landed and is kept as written
and one is queued. **Nothing here certifies k₁₈₈ ≥ 7, and nothing here refutes an ℓ₆ analogue of Tsaturian's lattice rigidity**
— a satisfying patch is a colouring of a finite set, not of the lattice, and the matched instances are open. The precise
statement is: no certificate was found among these configurations within these time limits. For the record, the ℓ₆-free patches
that were found (`l6_stats.py`, `logs/l6_stats.log`) have red density 0.22–0.25 on the base lattice, longest blue run 5 in each
of the three directions, 31/50/78 distinct red √3-triangles, and no lattice period ≤ 12 — a description of three patches, not a
structural statement.

## 2. Reproduce
```
P=~/.venv/bin/python   # numpy, scipy, sympy, python-sat
$P config188.py --R 10 --k 4 --ds sqrt3 --centers 0 --origin-red --out egmrss_k4 && cadical -q egmrss_k4.cnf      # UNSAT
$P config188.py --R 12 --k 5 --ds sqrt3,3 --centers 6 --rot-radius 4 --origin-red --blue 5,0 --out ts3_c6_k5 && cadical -q ts3_c6_k5.cnf   # UNSAT
$P mus188.py ts3_c6_k5 && $P verify_core.py ts3_c6_k5.core.json     # exact check, PASS
$P describe_core.py ts3_c6_k5.core.json                             # canonical description
$P noT3.py && $P cmxz_audit.py                                      # controls; the CMXZ constants
```
`instances/` holds the exact CNFs solved (gzipped where large); `cores/*.core.json` are the certificates with exact provenance;
`cores/*.describe.json` list every point; `controls/` the control instances and the second-solver + drat-trim log.

## 3. What is NOT claimed, and where the problem stands
* Nothing here changes the headline: 6 ≤ k₁₈₈ ≤ 6330 in print, ≤ 4917 by the remark above. The certificates re-prove known theorems.
* CMXZ's 6330 is loose in two independent places: the Milnor–Thom count (m⁸, or m⁶ with three variables; a direct count of
  the cell-sequences a unit progression can trace in a hexagonal tiling is presumably much smaller — a heuristic, not a result),
  and — far more — the per-point exponent 0.0156, which is what a 2%-density random red set gives (p(1−p)¹⁸ ≤ 0.0199, while
  1/7 is the density ceiling for red cells in this tiling). A structured red set of density 0.15–0.2 whose every unit
  progression is forced to hit it within a few hundred steps would put k₁₈₈ in the low hundreds; proving that for ALL lines and
  all phases is a 3-parameter covering statement that becomes finite for a periodic red set (interval branch-and-bound over
  (x, y, θ) on the torus). A red set that is one piece per period of a lattice Λ fails outright — for the shortest period
  vector λ, lines in direction λ at perpendicular offset avoiding the pieces exist whenever det Λ/|λ| exceeds the width of a piece
  across that direction — so the construction needs many pieces per period, placed so no direction is left open. That is the
  next real move on the upper side and it is not a cron-tick job.
* Lower side: §1c — none found, nothing refuted; of the three matched instances one is SAT (radius 3, no certificate possible there), one timed out at its 10,800 s cap, one (radius 6, the 69-point core's) timed out at 3,600 s.
