# #1159 entry draft (prose; numbers in [[...]] are filled from runs/)

## Problem
erdosproblems.com/1159: is there a constant C such that every finite projective plane has a blocking set S
(1 ≤ |S ∩ L| for every line L) with |S ∩ L| ≤ C for every line? Write c(Π) for the least max-intersection over
blocking sets of Π. Erdős–Silverman–Stein 1983: c(Π) ≪ log q. Green's list (after Problem 68): speculates no
such C along sufficiently large primes; "if q is not prime then, in many cases, there can be such sets".

## What was known
- Lower bound, every plane of order q ≥ 5: c ≥ 4 (Bruen–Fisher 1974 Thm 6(iv); Béres–Illés 1993; the count
  proof is in our /report/1159: with intersections in {1,2,3} the number of 2-secants is −s² + (3q+4)s − 3(q²+q+1),
  negative for all s once q ≥ 5).
- Exact: c = 3 for q = 2,3,4; c = 4 for q = 5, 7 (certificates in /report/1159), q = 3^r (Bruen–Fisher cubic pair), 
  so q = 9, 27, 81, …
- q = 11: 4 ≤ c ≤ 5 in our August report (60 s UNKNOWN at C = 4).
- Illés–Pisinger 1997 (DIKU 97-13 = J. Heuristics 7 (2001) 59–76), simulated annealing, 7 ≤ q ≤ 607, >38 CPU-days:
  best max-intersection found ξ(B): 4 at q = 7, 8, 9, 11; 5 at q = 13, 16, 17, 19; 6 at 23–43; 7 at 47–79;
  8 at 81–131; 9 at 137–223; 10 at 227–361; 11 at 367–563; 12 at 569–607. ξ/ln q < 2 throughout. For q = 11 their
  Table 3 gives |B| = 21 with secant spectrum (n1,n2,n3,n4) = (84, 0, 28, 21); the sets themselves were not printed
  ("available from the authors upon request"). Their lower-bound side is the same B(4) obstruction. So c(PG(2,11)) = 4
  was implicit in 1997; it was not in our August report (which cited only the Hungarian 1993 record).

## New here
1. c(PG(2,11)) = 4 with an explicit certificate: two solvers (cadical 14 s, CP-SAT 36 s) independently returned
   21-point sets; both have spectrum (84, 0, 28, 21) — IP97's spectrum — and are projectively equivalent
   (168 projectivities carry one onto the other). Verified by two independent incidence implementations.
2. The witness is Klein's configuration. Its stabilizer in PGL(3,11) has order 168, is simple (every nontrivial
   normal closure is the whole group), hence ≅ PSL(2,7); the 21 points are exactly the centres of its 21 involutions
   (harmonic homologies); the 21 four-secants are their axes; centre(σ) ∈ axis(τ) ⟺ στ = τσ, checked on all 420
   ordered pairs; the 28 three-secants are the remaining lines through ≥ 3 centres. This is the (21₄) configuration
   of Klein (1879) / Grünbaum–Rigby, which lives in PG(2,q) whenever −7 is a square (−7 ≡ 2² mod 11).
   Counting: a 21-set of type (1,3,4) with n4 = 21, n3 = 28 meets exactly 21q − 98 lines, which equals q² + q + 1
   only for q ∈ {9, 11} — so q = 11 is the largest order in which Klein's configuration can block.
3. Minimum size at q = 11: [[hi19 / hi20 verdicts]].
4. Larger orders: [[q = 13, 16, 17, 19, 23 verdicts]] — each SAT verdict is an exact value c(PG(2,q)) = 4
   beating IP97's heuristic 5 (or 6).

## Not claimed
The general question; anything about non-Desarguesian planes; IP97's values beyond our verified range remain
heuristic upper bounds; whether c(PG(2,q)) = 4 for all q or grows is exactly what is open.

## Labels
(a) the lower bound; (d) every certificate (two independent checkers; witnesses printed); (a)+(d) the group
identification (finite computation over an explicit list of 168 matrices); (b) literature attributions.
