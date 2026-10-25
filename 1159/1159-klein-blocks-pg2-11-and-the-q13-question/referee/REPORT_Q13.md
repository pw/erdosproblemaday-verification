# Hostile referee report #2: Erdős #1159, the q = 13 chain

Referee seat started 19:10Z on 2026-10-14 and finished at about 19:29Z. All scripts and outputs are in `referee/q13/`. Nothing outside `referee/` was edited. I imported none of the author's scripts and built PG(2,13) myself (`q13/pg.py`).

## VERDICT on the chain as written: **SOUND**

This verdict is about the chain only. The lower half of "c(PG(2,13)) = 5" still rests on three refutations that had not finished when I stopped: cubes 22, 32 and 33, which also need `drat-trim` to verify their proofs.

When I stopped (about 19:28Z, roughly 2,390 s into the run), CaDiCaL was still working on all three. **Each was started with `cadical -t 3600`**, so it has a hard one-hour limit that runs out at about **19:45:18Z**. For comparison, the q = 11 `hi20` cubes 22, 32 and 33 all ended `c UNKNOWN` at their own 1,800 s limit.

If the q = 13 runs hit the limit, the lower bound is **unproven**, not refuted. Before anything is written up, the author must report exactly how the three logs end (`s UNSATISFIABLE` or `c UNKNOWN`) and what `drat-trim` says.

I could not break any step of the reduction:

1. Any blocking set of PG(2,13) meeting every line in at most 4 points can be reduced to a minimal one.
2. The minimal one can be put in the normal form of one of the six cubes.
3. Each cube's CNF says exactly what the docstring says.
4. The three trivial cubes are refuted by verified DRAT proofs.

## 1. Count bound (re-derived from scratch)

Let k = |S| and let t_i be the number of lines meeting S in exactly i points, for i = 1, …, 4. Then:

- Σt_i = q²+q+1 = 183
- Σ i·t_i = k(q+1) = 14k
- Σ i(i−1)·t_i = k(k−1)

For i in {1, …, 4} each term (i−1)(4−i) is at least 0, so Σ(i−1)(4−i)t_i ≥ 0. Expanding:

- −(k²+13k) + 5·14k − 4·183 ≥ 0
- which is k² − 57k + 732 ≤ 0
- so 19.54 ≤ k ≤ 37.46, giving **20 ≤ |S| ≤ 37**. ✔

As a finer check, I searched by brute force for nonnegative integers (t₁, …, t₄) satisfying the three identities. They exist for exactly k = 20, …, 37: all 18 values, with no gaps (`q13/counts13.py`, `counts13.out`).

Both bounds also hold for a minimal subset, so "take S minimal" is compatible with the CNF's `≥ 20`. A minimal subset is still blocking and still has at most 4 points per line, so the count bound applies to it.

Optional strengthening: Blokhuis's theorem says a nontrivial blocking set of PG(2,p), p prime, has at least 3(p+1)/2 points. That gives 21 here. It is not needed.

**Size floor of the pencil at P0.** L0 is a tangent, so |S| = 1 + (further points on the 13 non-L0 lines through P0) ≤ 1 + c1 + 12·c2. By cube:

| Cube (c1,c2) | 1 + c1 + 12·c2 | Below 20? |
|---|---|---|
| (1,1) | 14 | yes |
| (2,1) | 15 | yes |
| (3,1) | 16 | yes |
| (2,2) | 27 | no |
| (3,2) | 28 | no |
| (3,3) | 40 | no |

This is the one-line reason why cubes **11, 21 and 31 are UNSAT: they cannot reach the size floor of 20.** The same argument gives c1 ≥ 2 and c2 ≥ 2, and it shows c2 = 0 is impossible, since then |S| ≤ 4.

## 2. WLOG chain, with explicit group elements and in the stated order

Points are column vectors and g acts by v ↦ gv. My verdict on each step:

| Step | Group element used (explicit) | What it must preserve | Checked |
|---|---|---|---|
| 0. Take S minimal | — | Max ≤ 4, blocking, 20 ≤ \|S\| ≤ 37 (§1) | ✔ Every point now has a tangent |
| 1. (P0, L0) → ((0,0,1), x=0) | A with A⁻¹ = [u \| r \| P0], where r ∈ L0∖P0 and u ∉ L0 | — | ✔ Flag-transitive |
| 2. Max line L1 = [a:1:0] → y=0 | (x,y,z) ↦ (x, y+ax, z): elation, axis x=0, centre P0 | P0, x=0 | ✔ Fixes x=0 pointwise; maps y = −ax to y=0 |
| 3. Q1 = (1,0,t) → (1,0,0) | (x,y,z) ↦ (x, y, z−tx): elation, axis x=0, centre P0 | P0, x=0, y=0 = max | ✔ **Fixes every line through P0**, so all pencil counts are unchanged and y=0 stays a max line |
| 4. Tangent M1 = [0:b:c] at Q1 → z=0 | (x,y,z) ↦ (x, y, z+(b/c)y): elation, axis **y=0**, centre P0 | P0, x=0, y=0 max, Q1 | ✔ **Fixes every line through P0**, fixes y=0 pointwise (so Q1 stays), and c ≠ 0 because M1 ≠ y=0 |
| 5. Second-max line L2: y=μx (μ ≠ 0) → y=x | diag(1, μ⁻¹, 1) | P0, Q1, x=0, y=0, z=0 | ✔ Fixes all three axes. It permutes the lines y=μ′x (μ′ ≠ 0) among themselves, so the multiset of counts is unchanged: y=0 stays max and every other line stays ≤ c2 |
| 6. If c1 ≥ 2, Q2 = (1,0,t) → (1,0,1) | diag(1, 1, t⁻¹) | All of the above, plus y=x | ✔ Fixes every line through P0, both axes and y=x. It is the last step, so nothing comes after it to undo it |

The two "shears" are both elations with centre P0, one with axis x=0 and one with axis y=0. That is why they do not disturb the pencil at P0. This answers each of the brief's order questions with "yes, preserved":

- Fixing y=x as second-max commutes with the earlier steps.
- The elation used for Q1 preserves the max property of y=0.
- The shear used for M1 preserves the max property of y=0.
- (1,0,1) ∈ S survives, because nothing comes after it.

**Coverage.**
- c1 ≤ 3, because a line has at most 4 points.
- c2 ≤ c1 by definition.
- c2 ≥ 1, because c2 = 0 gives |S| ≤ 4.
- So the six cubes {(c1,c2) : 1 ≤ c2 ≤ c1 ≤ 3} cover every case.
- The CNF does not state "others ≤ c1" or "y=0 is max"; both follow from c2 ≤ c1.
- I found no configuration that slips through.

**I ran the chain mechanically rather than trusting it** (`q13/chain13.py`). For every choice at every step — every P0 with a tangent, every tangent L0, every max L1, every Q1, every tangent M1, every second-max L2, every Q2 — it applies the explicit matrices above. After each step it re-asserts everything fixed before it, in the docstring's order.

- **q = 13, C = 5, on the author's 34-point witness** (minimalised to 33 points, still max 5): **17,340 normalisations, all passing every re-check**. They land in cubes (4,3) and (4,4).
- **q = 11, C = 4, on Klein's 21-point set** (rebuilt from scratch, `klein11.py`): **24,192 normalisations, all landing in cube (3,3)**.

## 3. The DIMACS files, read with my own parser (`q13/dimacs_check.py`, `dimacs_check.out`)

**Method.**
- Checked `cube_q13_c4.points.json` against my own PG(2,13) as a set (183 points).
- Mapped variables 1..183 to points in file order.
- Split every clause into exactly one of three groups: (a) unit clauses, (b) clauses over point variables only, (c) components joined by shared auxiliary variables (union-find over variables > 183). These groups use up every clause.
- Because the components share no auxiliary variables, the CNF projected onto the point variables equals the AND of the projections of the individual components.
- I identified each component's point set geometrically. I then found its meaning with SAT tests: for each count k, fix the inputs and ask whether the component is satisfiable.
  - Every 13-point component was tested on all 2¹³ assignments.
  - All 183 line components share one canonical clause structure, and one representative was tested on all 2¹⁴ assignments.
  - The two 183-point counters were sampled at every k: 3 random subsets per k, and 40 per k near the thresholds.
- The 183 line components cover all 183 distinct lines (`line_components_distinct.out`).
- No empty clauses, tautologies or duplicate literals, and every header matches (`clause_hygiene.out`).

**Results, identical in form across all six cubes:**
- **Unit clauses.** Positive units are (0,0,1) and (1,0,0), plus (1,0,1) exactly when c1 ≥ 2: absent in cube 11, present in 21, 22, 31, 32 and 33. The 26 negative units are exactly (x=0 ∖ (0,0,1)) ∪ (z=0 ∖ (1,0,0)). There are no units on auxiliary variables.
- **Point-only clauses.** The 183 line clauses, each with 14 positive literals. In addition, where a bound equals 1, the "at least 1" is a single 13-literal clause on that line minus (0,0,1): y=0 and y=x in cube 11, y=x in cubes 21 and 31.
- **Components:**
  - 183 × (full line, n=14, **≤ 4**)
  - 1 × (ALL183, **≥ 20**)
  - 1 × (ALL183, **≤ 37**)
  - y=0 [key (0,1,0)] **minus (0,0,1)**, n=13: **≤ c1 and ≥ c1** (the ≥1 is the plain clause in cube 11)
  - y=x [key (1,12,0), i.e. x+12y=0] **minus (0,0,1)**, n=13: **≤ c2 and ≥ c2** (plain clause when c2=1)
  - each of the **11** other pencil lines [keys (1,m,0), m = 1..11] **minus (0,0,1)**: **≤ c2** in every cube (11/21/31: ≤1; 22/32: ≤2; 33: ≤3)
- **Nothing else.** x=0 gets no cardinality block, because its points other than P0 are negative units. Every cardinality block excludes (0,0,1). The CNFs say exactly what the docstring says.

## 4. DRAT proofs for the trivial cubes (`q13/drat_trivial.out`)

`drat-trim` reports `s VERIFIED` on all three, each against the CNF file on disk:

| Cube | Verification time | Core lemmas | Why UNSAT |
|---|---|---|---|
| 11 | 1.12 s | 1,054 of 42,741 | Size floor 14 < 20 |
| 21 | 1.58 s | 1,099 of 43,265 | Size floor 15 < 20 |
| 31 | 0.31 s | 1,274 of 47,130 | Size floor 16 < 20 |

The SHA-256 hashes of the CNFs and proofs are recorded in the .out file.

Timestamps:
- The q = 13 CNFs were written at 18:41:57Z.
- The three big CaDiCaL runs started at about 18:45:18Z, so after the CNFs were written.
- The trivial proofs are dated 18:45.

As instructed, I did **not** run `drat-trim` on the large proofs 22, 32 and 33.

## 5. Third model (`q13/cube33_cpsat.py`, `cpsat_cube33.log`)

My model is CP-SAT with native linear constraints, built from my own PG(2,13) with no CNF. It covers cube (3,3) at q = 13, C = 4, sizes 20..37. It ran with 1 worker, `nice -n 19`, `ulimit -v 4000000`, and an 880 s time limit.

**Result: `UNKNOWN` after 880.1 s** (138,927 conflicts, 2.14M branches). That is neither a confirmation nor a refutation. No SAT witness was produced, so there is nothing to check pointwise.

Controls on the same model (`cpsat_controls.out`):

| Control | Expected | Got |
|---|---|---|
| q=11, C=4: Klein normal form fixed, cube (3,3) | accepted | OPTIMAL |
| Same form fixed, cube (3,2) | rejected | INFEASIBLE |
| q=13, C=5: witness normal forms fixed, cubes (4,4) and (4,3) | accepted | OPTIMAL |
| (4,4) form in cube (4,3) | rejected | INFEASIBLE |
| (4,4) form at C=4 | rejected | INFEASIBLE |

**Calibration.** The same single-worker model, unfixed, at q = 11 cube (3,3), **failed to find Klein's known solution within 120 s** (UNKNOWN). So this instrument is weak on search, and its q = 13 UNKNOWN carries no weight in either direction.

A file note: `q13/CONTROL_q11_klein_fixed_cube33_witness.json` comes from a **q = 11 control** and is not a q = 13 result. A first control run wrote it under a generic name and I renamed it. No q = 13 SAT file exists.

## 6. Literature (sub-search: `q13/lit_search.md`; I re-checked the load-bearing items myself)

- **"No blocking set of PG(2,13) has all line intersections ≤ 4": NOT FOUND in any source we could open.** This is a statement about coverage, not proof that no such source exists. Several primary sources could not be opened; they are listed in lit_search.md §G and include the 2001 J. Heuristics version and the full text of Béres–Illés 1993.
  - The search found no published "every (k,4)-arc of PG(2,13) has an external line".
  - Hamed's Sussex thesis census of (k,4)-arcs in PG(2,13) has at least 9 external lines in every listed distribution. That thesis says its census is not exhaustive.
  - On available evidence, a proof that c(PG(2,13)) ≥ 5 would be new.
- **c(PG(2,13)) ≤ 5 already has an explicit published witness**, which is a prior-art objection to the entry (objection 1 below).
  - Illés–Pisinger's solution file is `hjemmesider.diku.dk/~pisinger/output.c.gz`. The gzip header says it is `erdos.out`, dated 6 Dec 1997; sha256 is `1ed42458…8885`. I downloaded it myself; the excerpt is `q13/ip97_q13_block.txt`.
  - For q = 13 it lists a planar difference set and a **24-point** blocking set with `gam = 5`, y = 117/9/33/18/6.
  - My re-check (`ip24_check.out`):
    - The difference set is planar.
    - In the cyclic model the set has spectrum {1:117, 2:9, 3:33, 4:18, 5:6} under all four incidence conventions.
    - Transported to standard coordinates (`q13/ip24.json`), my own PG(2,13) confirms it is blocking, max 5, minimal (all 24 points have tangents), and passes the three counting identities.
- Illés–Pisinger's Table 1 value of 5 at q = 13 is indeed only an upper bound from simulated annealing (10 restarts, best |B| = 24), with no claim of optimality.
- The lit search reports that Illés–Pisinger's "Result 1" (quoting Béres–Illés) gives the window 19.5 ≤ |B| ≤ 37.5 at q = 13, ρ = 4. That is the same count bound as §1. **I could not re-open the PDF** (the URL now returns HTML), so cite it only after reading it yourselves.
- The author's 34-point witness (`runs/witness_q13_c5_b2.json`) re-verified pointwise in my own PG(2,13): |S| = 34, spectrum {1:52, 2:47, 3:34, 4:22, 5:28}, blocking, max 5, contains no line, identities hold. 33 of 34 points have a tangent. Dropping the tangentless point (1,11,7) gives a minimal 33-point set, still max 5.

## Numbered objections

1. **Prior art for the upper half.** Brief: *"so c(PG(2,13)) = 5, with the 34-point max-5 witness runs/witness_q13_c5_b2.json for the upper half"*. Illés–Pisinger published an explicit **24-point** max-5 blocking set of PG(2,13) in 1997 (`erdos.out`, verified above); it is smaller, minimal, and has only six 5-secants. The upper half is not ours and must be credited to them. The 34-point set may be kept only as an independent re-derivation. ENTRY_DRAFT already cites their Table 1 value of 5 at q = 13; it must also say that the set itself is published and checkable.
2. **Status, not soundness.** The three nontrivial runs carry `-t 3600`. If any one ends `c UNKNOWN` at about 19:45Z, the sentence *"every blocking set of PG(2,13) has a line meeting it in ≥ 5 points"* has no proof. The q = 11 `hi20` analogues all timed out at 1,800 s. Do not let the conclusion get ahead of the three `s UNSATISFIABLE` lines and their three `s VERIFIED` lines.
3. **The docstring omits minimality.** `cubes1159.py`: *"P0=(0,0,1) in S, L0 (x=0) tangent at P0; … Q1=(1,0,0) in S (elation); M1 (z=0) tangent at Q1 (shear)"*. A tangent at Q1 is not something you can choose: Q1 is forced to lie on L1. Only minimality of S guarantees the tangent exists. README and the brief say "S minimal"; the docstring should too, together with the note that the count bound 20..37 survives passing to a minimal subset. This is a documentation fix, not a logical gap.
4. **Unnamed group elements.** *"Q1=(1,0,0) in S (elation)"* and *"M1 (z=0) tangent at Q1 (shear)"*. The docstring should name them as the table in §2 does: z ↦ z−tx (axis x=0) and z ↦ z+(b/c)y (axis y=0), both with centre P0. The one-line reason the order is harmless is that **both fix every line through P0**. That sentence is what answers the order questions, and it is missing.
5. **Notation.** *"(diag(l,b,m) is transitive on lines y=mx, m!=0)"* uses m both as the slope and as a diagonal entry. *"(residual diag(l,l,m) scales b)"* uses b, which the docstring never defines (it means the third coordinate of the second point (1,0,b)). This is cosmetic.
6. **Trivial cubes need no DRAT.** Cubes 11, 21 and 31 die on the arithmetic 1+c1+12c2 < 20 (14, 15, 16). The write-up should give that one line; the DRAT proofs then merely confirm it.
7. **Positive controls exist only at q = 11.** The brief asks about the author's constructive control, `normalform_control.py`. It is a q = 11 control; at q = 13, C = 4 none is possible if the claim is true. The C = 4 CNFs cannot hold the max-5 witness. On its own that would not be enough. **It is now enough**, because §3 verifies the q = 13 CNFs exactly, component by component, and §2 runs the group elements at q = 13 on real configurations. The author should cite the direct semantic check, not the q = 11 control, for the q = 13 encoding.

## What I tried and could not break

- **Order of normalisations.** All four of the brief's questions came out "preserved". The elations and diagonals above fix every line through P0 (or permute the non-axis ones), so the max and second-max structure cannot move.
- **Hunting a max-4 configuration outside every cube.** The coverage argument is complete. Running every choice on two real configurations (17,340 normalisations at q = 13 and 24,192 at q = 11) produced no failure.
- **Wrong lines or wrong points in the CNF.** I checked whether point (0,0,1) is inside a pencil block, whether y=x is the right line, whether any line is missing or duplicated, and whether units sit in the wrong places. All six files are clean (§3).
- **Off-by-one in the size bounds.** None: the integer feasibility search gives exactly 20..37.
- **An independent model** (CP-SAT, 15 min, 1 worker): UNKNOWN, and it is a weak instrument (see the q = 11 calibration).

## Files (`referee/q13/`)

- `pg.py` — my PG(2,q).
- `counts13.py` / `.out` — count bound and size floors.
- `dimacs_check.py` / `.out` — CNF decomposition and semantics.
- `line_components_distinct.out`, `clause_hygiene.out`.
- `drat_trivial.out`.
- `chain13.py` (`Q=` env var), `chain13.out`, `chain11_klein.out` — explicit WLOG chain.
- `nf_q13c5_*.json`, `nf_q11c4_*.json` — normal forms.
- `klein11.py` / `.json`.
- `cube33_cpsat.py`, `cpsat_cube33.log`, `cpsat_controls.out` — third model.
- `witness13.py` / `.out` — author's witness check.
- `ip24.json`, `ip24_check.out`, `ip97_q13_block.txt` — published Illés–Pisinger witness.
- `lit_search.md`.
