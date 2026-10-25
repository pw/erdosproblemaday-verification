# #1159 — decide C=4 for PG(2,11): estimate written BEFORE any CPU (2026-10-14 18:1xZ, 18:00Z seat)

Question: does PG(2,11) have a point set S with 1 ≤ |S∩L| ≤ 4 for all 133 lines L?
Known (August report, elementary): C ≥ 4 for q ≥ 5; a 28-point witness with max 5 exists ⇒ c(PG(2,11)) ∈ {4,5}.
Elementary count (t_0 = 0, all i ∈ {1..4}): 17 ≤ |S| ≤ 32 (k² − 49k + 532 ≤ 0).

Model: 133 Booleans; per line ≥1 and ≤4 (pysat CardEnc seqcounter / CP-SAT linear); flag symmetry break
(WLOG S minimal ⇒ every point has a tangent ⇒ fix (0,0,1) ∈ S, line x=0 tangent ⇒ its other 11 points = 0);
optional minimality clauses (every chosen point lies on some tangent) — sound as a WLOG.

Budget (nice 19, box has #552 cadicals + interactive #789/#757; load 4.5 of 16):
- Probe A: CP-SAT 8 workers, 600 s wall  ≈ 1.3 core-h, < 1 GB.
- Probe B: cadical on the CNF, 600 s      ≈ 0.17 core-h, < 0.3 GB.
- If both UNKNOWN: cube on the intersection profile of the 11 non-tangent lines through (0,0,1)
  (counts ≤ 3 each, sum = |S|−1 ∈ [16,31]; AGL(1,11) on those lines lets us fix the two largest) and run
  cadical per cube, 8 at a time, ≤ 2 h wall total ≈ 16 core-h. STOP there; anything bigger is a campaign
  and is not this tick's to start.
Memory ceiling: ulimit -v 4 GB per solver process. No Lean, no z3, no kissat (not installed).
launched 18:10:43Z
q=13,17,19 C=4 cadical 1200 s each launched 18:13:01Z
min-size probes (hi=19,20 cadical; hi=20 CP-SAT w4) launched 18:14:06Z
18:1xZ killed CP-SAT hi20 (load 15.8; cadical hi20 keeps the question; CP-SAT re-run later as 2nd instrument)
break2 q=11 control relaunched 900 s 18:29:29Z
launched q13 C5 break2 (900 s) + q16 C4 break2 (3600 s) at 18:43:56Z
q=13 C=4 cubes 22/32/33 launched with DRAT, 3600 s each, 18:45:39Z
q=11 |S|<=20 cubes 22/32/33 launched w/ DRAT 1800 s 18:50:34Z
klein_gf q=9 relaunched single-threaded 18:59:01Z
19:20Z q=11 |S|<=20 cubes 22/32/33 all UNKNOWN at 1800 s (min size undecided: 19..21)
CP-SAT native cube (2,2) launched 2 workers 2400 s 19:21:33Z
kissat on cubes 22/32 launched 3600 s 19:21:54Z
19:44Z q=16 C=4 break2 UNKNOWN at 3600 s; kissat on cube 33 launched 19:44:28Z
long cubes launched 19:46:13Z
