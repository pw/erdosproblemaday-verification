# Hostile referee brief — Erdős #1159, 2026-10-14 (18:00Z seat)

You are refereeing a claimed result for erdosproblemaday.com. Your job is to REFUTE it. Quote the sentence you object to.
Do not trust any file's self-description; recompute.

## The claims (as they will appear on the page)
C1. In PG(2,q), q ≥ 5, every blocking set has a line meeting it in ≥ 4 points (literature; one-paragraph count in
    /report/1159). So c(PG(2,q)) ≥ 4 for q ≥ 5.
C2. The 21 points listed in runs/witnesses_q11_c4.json (either key) form a blocking set of PG(2,11) meeting every line
    in 1, 3 or 4 points, spectrum (n1,n2,n3,n4) = (84,0,28,21). Hence c(PG(2,11)) = 4.
C3. Its setwise stabilizer in PGL(3,11) has order 168 and is simple (so ≅ PSL(2,7)); the 21 points are the centres of
    its 21 involutions; the 21 four-secants are their axes; centre(σ) ∈ axis(τ) iff στ = τσ. It is Klein's (21_4)
    configuration. The two solver witnesses are projectively equivalent.
C4. A 21-set of type (1,3,4) with n4=21, n3=28 meets exactly 21q − 98 lines; = q²+q+1 iff q ∈ {9,11}.
C5. PENDING — skip.
C6. PENDING — skip. (Current evidence: at q=13 the orbit-union models in runs/orbitzoo_q13.log are INFEASIBLE for every symmetric reduction, and plain cadical is UNKNOWN at 1,200 s — a cube campaign for an UNSAT certificate is running; do not assess yet.)
C7. Literature: Illés–Pisinger, DIKU 97-13 (= J. Heuristics 7 (2001) 59–76), Table 1 gives best-found max-intersection
    4 at q=7,8,9,11; 5 at q=13,16,17,19; 6 at 23..43 …; Table 3 gives for q=11 |B|=21, spectrum 84/0/28/21. The PDF is at
    /tmp/erdos1159_lit/illes_pisinger_97-13.pdf (text: .txt beside it). Green's list: remark under Problem 68
    (/tmp/erdos1159_lit/green.txt around line 1540).

## What to do
1. Write YOUR OWN PG(2,q) (do not import model1159.py) — e.g. via homogeneous coordinates and a dot product — and
   re-verify every witness JSON in runs/ (q=11 both keys; any runs/witness_q*.json). Report |S| and the full spectrum.
2. Re-derive C1 from scratch (three count identities). Check the quadratic and its discriminant.
3. Recompute the stabilizer of the q=11 witness YOUR way (e.g. brute force over PGL(3,11) via frame images, or via
   nauty on the point–line incidence graph with S coloured) and test simplicity or otherwise identify the group.
   Check the involution-centre claim and the commuting criterion.
4. Check C4 by algebra and against the spectrum.
5. Check the symmetry-breaking argument in model1159.py (flag break; `--break2` second flag): is each step a sound WLOG?
   Try to construct a counter-scenario (a solution killed by the break with no equivalent surviving solution).
6. Read the IP97 text and confirm every number in C7; flag any misreading of their convention (they define covering
   number of the PLANE as 1 + min max-intersection, and ξ(B) as max collinear points of B).
7. Novelty: is "the optimum at q=11 is Klein's configuration" already in print? Search. Is c(PG(2,13)) etc. known?
Deliver: VERDICT (HOLDS AS READ / HOLDS WITH FIXES / GAP AT …), a numbered list of objections each quoting the sentence,
and the scripts you wrote (save under ~/MathDyad/erdos1159/referee/). Be adversarial; "I could not break it" must come
with what you tried.
