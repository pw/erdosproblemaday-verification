# Hostile referee report — Erdős #1159, claims C1, C2, C3, C4, C7 (C5, C6 skipped as PENDING)

Referee seat, 2026-10-14. Everything below was recomputed with my own code in this directory (own PG(2,p),
own checker, own stabilizer by frame enumeration, nauty cross-check, own closed-form Klein construction).
I did not import model1159.py / equiv1159.py / klein1159.py. I read model1159.py and cubes1159.py only to audit
the symmetry breaks (brief step 5) and plane_gf.py only for its GF(9) integer encoding.

## VERDICT: HOLDS WITH FIXES

The mathematics of C1–C4 holds, and every number C7 attributes to Illés–Pisinger is in their text. One fix is
load-bearing for the page: **the explicit q = 11 certificate is not new.** Illés and Pisinger posted their actual
21-point set for q = 11 on the web in 1997. I recovered it from the Wayback Machine, and it is the same
configuration as both solver witnesses (nauty isomorphism of the coloured incidence structures, plus a
negative control). So "c(PG(2,11)) = 4 with an explicit certificate" was public in Dec 1997 / Jan 1998. What is
left as possibly new is narrower: identifying that set as Klein's configuration, plus an independent re-verification.
I did not find that identification in print anywhere, but a search is not a proof of absence (see §5).

## 1. Numbered objections (each quotes the sentence objected to)

1. **Novelty of the certificate is refuted.** ENTRY_DRAFT: *"the sets themselves were not printed ("available
   from the authors upon request")"*, *"So c(PG(2,11)) = 4 was implicit in 1997"* and *"New here 1.
   c(PG(2,11)) = 4 with an explicit certificate"*. The paper itself does not print the sets. But IP97's
   concluding remarks (text line ~865) say *"A generator of the instances as well as our results can be found
   at the internet ... http://www.diku.dk/~pisinger/erdos.html"*. That page (archived 1999–2004, "Last Update:
   January 5, 1998") has a section "Found solutions" linking `output.c.gz`, *"the best found blocking sets, as
   well as the corresponding difference sets"*. The archived copy is
   `web.archive.org/web/20001003134338/http://www.diku.dk:80/~pisinger/output.c.gz` (gzip mtime
   6 Dec 1997, sha256 1ed42458…8885). It contains the q = 11 block verbatim
   (`ip97_posted_q11_excerpt.txt`): difference set {3,16,24,27,31,33,43,74,75,97,111,131}, solution
   {5,13,22,26,27,33,39,40,50,74,78,80,84,89,92,94,96,99,107,112,114}, y[1]=84, y[3]=28, y[4]=21.
   `ip97_compare.py` rebuilds their cyclic plane by their own eqs (2)–(4) and checks D is a planar difference
   set mod 133 (True). It gives their B the spectrum {1:84, 3:28, 4:21}. Under nauty, (their plane, B) is
   **isomorphic** to (PG(2,11), our cadical witness) and to (PG(2,11), our cpsat witness), while a one-point-swap
   negative control is not. Their B has |Aut| = 168.
   **Fix:** "c(PG(2,11)) = 4 has been explicit since 1997: Illés–Pisinger's posted q = 11 set (output.c.gz),
   which we identify as Klein's configuration." Then demote New-here item 1 to "independent re-derivation and
   re-verification."
2. ENTRY_DRAFT: *"ξ/ln q < 2 throughout."* False at q = 7. IP97 Table 1 prints ψ = 2.06 for q = 7
   (4/ln 7 = 2.056), and their own text says *"less than 2 for all problems q ≥ 8"*. **Fix:** "for 8 ≤ q ≤ 607".
3. C3: *"centre(σ) ∈ axis(τ) iff στ = τσ."* As written it is false for σ = τ: σ commutes with itself, but a
   homology's centre is not on its axis (checked, 0 of 21). The ENTRY's "checked on all 420 ordered pairs"
   already means distinct pairs. **Fix:** add "for σ ≠ τ".
4. C4: *"A 21-set of type (1,3,4) with n4=21, n3=28 meets exactly 21q − 98 lines; = q²+q+1 iff q ∈ {9,11}."*
   In standard terminology (Tallini Scafati) a set "of type (1,3,4)" has no external lines, so it meets all
   q²+q+1 lines and the sentence is self-defeating. The algebra is right. **Fix:** "a 21-set meeting every line
   in 0, 1, 3 or 4 points, with n3 = 28, n4 = 21 (hence n2 = 0, since 3·28 + 6·21 = 210 = C(21,2)), meets
   exactly 21q − 98 lines."
5. ENTRY_DRAFT: *"This is the (21₄) configuration of Klein (1879) / Grünbaum–Rigby, which lives in PG(2,q)
   whenever −7 is a square."* Two problems:
   (a) **Even q.** In characteristic 2, −7 = 1 is always a square, but the configuration collapses. The
   literature coordinates give 7 or 6 distinct "quadruple" points at q = 2 (`klein_char2.out`), and involutions
   are elations there, not homologies. The claim needs "q odd". In characteristic 7 it exists (49 distinct
   points) but does not block: spectrum {0:8, 3:28, 4:21} at q = 7.
   (b) **Grünbaum–Rigby.** Their configuration is a real realization. By Sylvester–Gallai it must have
   2-point lines, so it cannot carry the 28 three-point lines (n2 = 0) that make the set block. It shares only
   the combinatorial (21₄) part. **Fix:** attribute the 21-point/49-line object to Klein. For the definition
   over arbitrary fields, cite Seceleanu, arXiv:1410.0312 §4.2. That paper credits Grünbaum–Rigby 1990 with the
   F₇ version.
6. C7: *"Table 3 gives for q=11 |B|=21, spectrum 84/0/28/21."* The numbers are correct. In DIKU 97-13 the body
   text calls these tables "Table 4-6" (line ~542), while the captions read Tables 3–5. I did not check the
   J. Heuristics numbering. **Fix:** cite "DIKU 97-13, table captioned 'Table 3: Geometrical properties'".
7. **Priority risk, not refuted.** ENTRY_DRAFT: *"it was not in our August report (which cited only the
   Hungarian 1993 record)"*. Béres–Illés 1993 ran a greedy for every prime q ≤ 89 and for q = 8, 9, 16 (IAOR
   abstract). IP97 says that for q = 11 the greedy "was just few minutes". I could not read their table. If it
   shows 4 at q = 11, then c(PG(2,11)) = 4 dates to 1993. Bibliographic nit: IAOR lists *Alkalmazott Matematikai
   Lapok* 17(3/4) as pp. **379–411**; the August report says 397–411.
8. Process (brief step 5; relevant to C5/C6, not to C1–C4). The author's `--break2` "control" at q = 11
   (`cadical_q11_c4_b2.log`) returned **UNKNOWN after 900 s**, so it validated nothing.
   `runs/witness_q11_c4_b2.json` is an **empty list** and must not be presented as a witness. I supplied the
   missing control. `break_control.py` maps the Klein set by explicit projectivities into the normal form each
   break demands, then fixes all 133 point variables as assumptions in the actual CNF files:
   - `pg11_c4_b2.cnf` and `pg11_c4.cnf` accept it.
   - `cube_q11_c4_33.cnf` accepts the cube-normal-form image (c1 = c2 = 3).
   - Cubes 11, 21 and 31 reject it.
   - Image-minus-a-point is rejected (negative control).

## 2. Recomputed numbers (own code; compare runs/klein_identification_q11.log — all agree)

**Witnesses** (`check_witnesses.out`, own incidence; three count identities asserted). |S| = 21, spectrum
(n1,n2,n3,n4) = (84,0,28,21), blocking, max 4, 133 lines, for each of:
- witnesses_q11_c4.json [cadical]
- witnesses_q11_c4.json [cpsat]
- witness_q11_c4_orbit_perm.json
- witness_q11_c4_orbit_singer7.json
- witness_q11_type134_n21.json

Other witness files:
- witness_q11_c4_b2.json: EMPTY.
- witness_q13_c5_b2.json: |S| = 34, spectrum {1:52, 2:47, 3:34, 4:22, 5:28}, blocking, max 5.
- q = 9 type-134 witness: checked in the author's galois encoding with my own arithmetic, cross-checked on all
  81 products/sums. Spectrum {1:42, 3:28, 4:21}; collineation-equivalent to Klein over GF(9); PΓL-stabilizer 336.

Checker negative controls: deleting any of 3 points creates an empty line, and adding a point changes the spectrum.

**C1** (`counts.out`, sympy)
- n2 = −s² + (3q+4)s − 3(q²+q+1), which matches the report.
- Discriminant in s is −3q² + 12q + 4, with roots q = 2 ± 4/√3. So it is negative for every q ≥ 5 (q = 5 gives −11).
- Integer brute force: type {1,2,3} is feasible only for q ≤ 4, at sizes q=2: 3–7, q=3: 5–8, q=4: 7–9.
- Attribution checked against the primary PDF: Bruen–Fisher, Pacific J. Math 53 (1974), Theorem 6(iv), *"when
  n ≥ 5, some line of π must contain at least 4 points of S."*

**C2.** Both witnesses verified, and C1 gives the lower bound, so c(PG(2,11)) = 4.

**C3**

| Quantity | Value |
|---|---|
| Stabilizer order, frame enumeration over 143,640 ordered 4-tuples | 168 |
| Stabilizer order, nauty on the 266-vertex incidence graph, colours (S / other points / lines) — collineations only, = PGL since 11 is prime | 168 |
| Element-order census | {1:1, 2:21, 3:56, 4:42, 7:48} |
| Conjugacy classes (size, order) | (1,1), (21,2), (24,7), (24,7), (42,4), (56,3) |
| Normal closures of the 5 nontrivial classes | all 168 ⇒ simple |
| Derived subgroup order | 168 (perfect) |
| Sylow-7 subgroups | 8 |

- Involutions: 21. Each fixes exactly 13 points: one line pointwise plus one isolated point (homology).
- The centres are 21 distinct points, and they equal S.
- The axes are 21 distinct lines, and they equal the set of 4-secants. No centre lies on its own axis.
- Commuting test: centre(σ) ∈ axis(τ) ⟺ στ = τσ on all 420 ordered pairs with σ ≠ τ, 0 mismatches, 84 incidences.
- The 3- and 4-secants cover all 210 pairs of S exactly once.
- G-orbits: transitive on S (21), on the 3-secants (28) and on the 4-secants (21).

Dualities, kept separate from collineations:
- Colouring S ∪ {4-secants} together gives |Aut| = 336. One generator swaps points and lines, i.e. a correlation
  carries S onto its axes.
- Abstract (21₄) Levi graph: |Aut| = 672 including dualities, 336 point-preserving.
- Abstract 21 points + 49 lines: |Aut| = 336.
- So the abstract configuration has more symmetry than the projective stabilizer (PGL(2,7) vs PSL(2,7)). That
  is consistent with Klein, where the outer automorphisms are not collineations; over C they are antiholomorphic.

**Klein identification by an independent route** (`klein_explicit.out`)
- I built Klein's configuration from Seceleanu's explicit coordinates (arXiv:1410.0312 §4.2): with roots c, c̄
  of t²+t+2, the 21 quadruple points are all coordinate permutations of (1:0:0), (1:±1:0) and (1:±1:±c̄).
- At q = 11, for both roots (c = 4, 6), **168 projectivities** carry our cadical witness onto these 21 points.
  This is the identification, from the literature side rather than from group theory.
- Closed form at q = 11 (c = 4, c̄ = 6), hand-checkable, spectrum {1:84, 3:28, 4:21}:
  {(0,0,1), (0,1,0), (0,1,1), (0,1,10), (1,0,0), (1,0,1), (1,0,10), (1,1,0), (1,1,5), (1,1,6), (1,2,2),
  (1,2,9), (1,5,1), (1,5,10), (1,6,1), (1,6,10), (1,9,2), (1,9,9), (1,10,0), (1,10,5), (1,10,6)}.
  I recommend the page print this instead of, or beside, the solver dump.
- All q = 11 witness files are mutually equivalent (`equiv_all_q11.out`). Projectivities from cadical onto
  cpsat, orbit_perm and orbit_singer7: 168 each.

**C4** (`counts.out`, `klein_explicit.out`)
- n1 = 21q − 147; lines met = 21q − 98. Then 21q − 98 − (q²+q+1) = −(q−9)(q−11), so q ∈ {9, 11}.
- Pair check: 3·28 + 6·21 = 210 = C(21,2).
- On actual Klein sets the formula holds wherever the set is non-degenerate:

  | q | Spectrum | Lines met |
  |---|---|---|
  | 7 | {0:8, 3:28, 4:21} | 49 = 21·7 − 98 |
  | 9 | {1:42, 3:28, 4:21} | blocks |
  | 11 | {1:84, 3:28, 4:21} | blocks |
  | 23 | — | 385 |
  | 29 | — | 511 |
  | 37 | — | 679 |
  | 43 | — | 805 |

  All match 21q − 98. So "q = 11 is the largest order in which Klein's configuration can block" stands, and the
  q = 9 case is realized too.
- Side fact: without fixing (n3, n4), a blocking 21-set with n2 = 0 is count-feasible for every q from 7 to 13.
  It is the pair (28, 21) that pins q ∈ {9, 11}.

## 3. C7 line by line (DIKU 97-13 text, /tmp/erdos1159_lit/illes_pisinger_97-13.txt)

**Conventions in IP97 §2:**
- **Blocking set:** "B intersects every line but contains no line".
- **ξ(B):** "the maximum number of collinear points of B", called "the covering number of the blocking set B".
- **Plane covering number:** τ(Π(q)) = 1 + min_B ξ(B), the smallest τ with property B(τ) (strict "< τ").
- **Our c(Π):** equals min_B ξ(B). The no-line clause is irrelevant once q ≥ 4, since max ≤ 4 < q+1 for q ≥ 4.

**The Table 1 column is ξ(B), not τ.** Check via ψ = ξ/ln q: q = 7 gives 4/1.946 = 2.06, as printed; q = 11
gives 4/2.398 = 1.67, as printed.

**Every Table 1 value in C7 matches:**

| ξ | Orders q in Table 1 |
|---|---|
| 4 | 7, 8, 9, 11 |
| 5 | 13, 16, 17, 19 |
| 6 | 23, 25, 27, 29, 31, 32, 37, 41, 43 |
| 7 | 47–79 |
| 8 | 81–131 |
| 9 | 137–223 |
| 10 | 227–361 |
| 11 | 367–563 (Tables 1–2) |
| 12 | 569–607 |

**Other figures:**
- q = 11 row: |B| = 21, ξ = 4, t = 54 s.
- Table 3 (captioned), q = 11 row: 84, 0, 28, 21. **Matches.**
- "More than 38 days" of CPU and 7 ≤ q ≤ 607 match.
- Footnote 4 says "available from the authors upon request". It is superseded by their own web page; see
  objection 1.

**Journal version** (Crossref): T. Illés, D. Pisinger, J. Heuristics 7(1) (2001) 59–76,
doi:10.1023/A:1026517829321. **Matches.**

**Green's list, line ~1557:** a set in PG(2,q) meeting every line in at least 1 and at most 1000 points;
*"If q is not prime then, in many cases, there can be such sets ... as q ranges over sufficiently large primes it
is speculated that no such set exists."* It sits in the comments to Problem 68. **Matches** the ENTRY.

**Side remark:** IP97's heuristic values at q = 27 (6) and q = 81 (8) are worse than Bruen–Fisher's proved
ξ ≤ 4 for 3^r, r ≥ 2. IP97 themselves cite that result as "B(5)". So "IP97 best" is not "best known" at
prime-power q. Keep the "beating IP97's heuristic" phrasing in C6 honest about this.

## 4. Symmetry breaks (brief step 5)

**Flag break: sound.** WLOG S is minimal (a minimal blocking subset keeps max ≤ C and only lowers |S|), so every
point has a tangent. PGL(3,q) is flag-transitive.

**`--break2`: sound.** (P0, L0) is a tangent flag and Q1 ≠ P0 has a tangent M1. P0 ∉ M1 because M1 ∩ S = {Q1}.
So P0, R = L0 ∩ M1 and Q1 are non-collinear, and PGL(3,q) is transitive on ordered triangles. Hence
((0,0,1), x=0, (1,0,0), z=0) can be imposed simultaneously.

**`cubes1159.py` chain: sound.**
- The flag stabilizer is transitive on the q non-L0 lines through P0 (elations with centre P0 and axis L0
  realize this).
- Then the stabilizer of P0, L0, Q1, namely [[a,0,0],[0,b,0],[0,c,m]], acts on L0∖{P0} by
  t ↦ (c + mt)/b, which is transitive. So M1 → z=0.
- Then diag(a,b,m) maps y = μx to y = (bμ/a)x, so L2 → y = x.
- Then diag(l,l,m) scales t on y = 0, so (1,0,t) → (1,0,1).
- c2 ≥ 1 is forced because |S| ≥ q+1 > C+1.

**Two caveats:**
- Minimality-WLOG is valid only with *upper* size bounds. A `--lo` above the elementary count bound would be
  unsound unless another run covers the gap.
- These arguments were checked on the actual CNFs only through my positive controls (objection 8). They are not
  a proof that the UNSAT cubes are correct; that needs the DRAT proofs in runs/proofs, which C5/C6 will rest on.

## 5. Novelty search (C3's identification)

**IP97 (DIKU text):** never mentions a stabilizer, automorphism group, 168, PSL(2,7) or Klein. Its only uses of "symmetry" concern the cyclic incidence matrix (line ~303) and the annealer revisiting "symmetrical solutions" (line ~846).

**Searches** (WebSearch, standard and extended), on terms including:
- "Klein configuration blocking set PG(2,11)", "PSL(2,7) orbits PG(2,q) 21 points"
- "Klein arrangement finite field / positive characteristic", "blocking set PG(2,11) 21 points PSL(2,7)"

found no source connecting Klein's configuration to blocking sets or to Erdős #1159.

**Closest hits:**
- Seceleanu 2014 defines Klein over any field (commutative-algebra context, no blocking).
- Indaco–Korchmáros on PSL(2,7)-invariant 42-arcs.
- Dover on blocking semiovals in PG(2,11) (26 points).

**Unread, so residual risk:**
- Grünbaum–Rigby 1990, which per Seceleanu introduces the F₇ version.
- Béres–Illés 1993 (Hungarian).
- The J. Heuristics text, which may differ from DIKU 97-13.

**Label:** "identification not found in print (search report)", not "new".

## 6. What I tried and could not break

1. **Independent incidence and counts.** My own PG(2,11) (axioms asserted, all line pairs meet once) and my own
   spectrum checks on every witness file, with the three count identities asserted and negative controls on the
   checker.
2. **Hunting for an extra symmetry.** Two independent stabilizer computations (frame-image enumeration;
   collineation-only nauty) both give 168. The dualities found (336 with S ∪ 4-secants coloured together) are
   correlations, not collineations, so they do not inflate C3.
3. **Hunting for a non-simple group.** Full group table: closure, inverses, classes, normal closures, derived
   subgroup, Sylow-7 count. All agree with PSL(2,7). A simple group of order 168 is unique.
4. **Hunting for a centre/axis mismatch.** Each involution's fixed-point set computed directly (13 points = axis +
   centre). Centres equal S, axes equal the 4-secants, and the commuting criterion holds on all 420 distinct
   pairs. The only failure is the σ = τ quantifier (objection 3).
5. **A different Klein.** I built Klein from published coordinates rather than from our group. It is
   projectively equivalent to the witness (168 maps, both roots c).
6. **C1 / C4 by sympy and integer brute force,** including the discriminant's real roots and the exact
   q-range. C4 checked on actual Klein sets for q = 7, 9, 11, 23, 29, 37, 43, and the char-2 degeneration.
7. **Literature numbers.** Every IP97 number in C7 and the ENTRY checked against the text. ξ-vs-τ settled
   numerically via ψ. Journal citation confirmed by Crossref. Bruen–Fisher Thm 6(iv) read in the PJM PDF.
   Green's remark read in the text.
8. **Break soundness** (step 5): attacked each WLOG step for a configuration that could be lost, and found none.
   Confirmed by assumption-checks on the shipped CNF files.

## Files
| File | Purpose |
|---|---|
| rpg.py | own PG(2,p), projectivities from frames |
| check_witnesses.py / .out | all witness files |
| stabilizer.py / .out | frame-enumeration stabilizer, group ID, involutions, commuting, equivalences |
| stabilizer_q11.json | the 168 matrices |
| nauty_check.py / .out | collineations vs dualities, abstract configuration automorphisms |
| equiv_all_q11.py / .out | all q = 11 files mutually equivalent |
| counts.py / .out | C1, C4 algebra |
| klein_explicit.py / .out, klein_explicit_lib.py, klein_char2.py / .out, klein_q11_closed_form.py / .out | literature-coordinate Klein over F_q |
| check_q9.py / .out | author's q = 9 witness in their encoding |
| ip97_compare.py / .out, ip97_posted_q11_excerpt.txt | IP97's own posted q = 11 set ≅ our witness |
| break_control.py / .out | break2 / cube positive controls on the actual CNFs |
