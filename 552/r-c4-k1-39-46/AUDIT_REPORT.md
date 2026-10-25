# Hostile audit of the candidate proof R(C4,K1,39)=46

Date: 2026-08-11 UTC.

Audited upstream: `zach7036/c4-star-ramsey`, commit
`86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33`, tree
`347a884913671c9f9a060de868de8fdd63d4f6a1`.

## Verdict

**PASS for the exact finite theorem `R(C4,K1,39)=46`.** The proof genuinely rules out every
simple 46-vertex `C4`-free graph of minimum degree at least seven. The decisive argument is a
universal spectral/moment proof with an exact rational dual certificate. It does not rely on the
repository's uncertified SAT result lines.

**GAP for peer-reviewed or established-literature status.** The repository calls itself not yet
peer-reviewed and requests review. The live Erdos page still displayed `OPEN`, zero claimed proofs,
and no current worker. A second public, unreviewed repository also claims the same value using LRAT
artifacts, but it is outside this audit. This audit establishes mathematical validity of the checked
finite theorem; it is not journal peer review, a priority finding, or an audit of either that second
claim or the Zach repository's separate `f(51)` and `f(83)` claims.

## 1. Exact custody and provenance

The upstream commit and tree are frozen three ways: a clean `git archive` extraction under
`upstream_ro/`, the exact archive tar, and a Git bundle containing its history. At capture time,
GitHub and `git ls-remote` both returned the requested commit as `HEAD` and `main`. The commit is
unsigned; cryptographic custody identifies the public bytes but is not evidence for the proof.

Radziszowski DS1.18 records the established interval

`46 <= R(C4,K1,39) <= 47`

and the adjacent established value `R(C4,K1,40)=47`; it says the consecutive exact values were
known through parameter 38. Thus the lower bound 46 was already established. Relative to that
published interval, the candidate contributes the upper bound 46. The earlier Boza `/46` cell is
not used: the separate table audit identified its wheel-index error.

The Zhang-Broersma-Chen equality uses `S_{n+1}` and `W_n=K1+C_n`. Consequently the same
order-40 wheel is `W_39` in their rim-length convention and `W_40` under a wheel-order convention.
No ambiguous subscript or same-index Boza convention is imported.

## 2. Lower bound: direct certificate PASS

The frozen `lower_bound_45.json` has 45 vertices and 147 distinct edges. An independent
standard-library checker found 21 vertices of degree six and 24 of degree seven. It checked every
vertex pair for two common neighbours and independently scanned all four-vertex cyclic orders;
both counts of `C4` were zero.

On 45 vertices, minimum degree six means complement degree at most `44-6=38`, so the complement
contains no `K1,39`. Therefore `R(C4,K1,39)>45`, proving the lower bound 46 without trusting the
claimed polarity-graph provenance. Duplicate-edge, edge-deletion, and C4-creating insertion
mutations were all rejected.

## 3. Universal reduction to one rigid structure

Assume for contradiction that `G` is a 46-vertex `C4`-free graph with `delta(G)>=7`. For a vertex
`v`, let `m_v` count edges inside `N(v)`, let `f_v` count vertices at distance at least three, and
put `S_u=N(u)\N[v]` for `u in N(v)`.

`C4`-freeness makes `G[N(v)]` a matching and makes the sets `S_u` pairwise disjoint. Counting the
distance partition gives the exact identity

`sum_{u in N(v)} d(u) = 45 + 2m_v - f_v`.                                      (1)

If `d=d(v)`, then `m_v<=floor(d/2)` and every neighbour has degree at least seven. Hence

`7d <= 45+d`,

whose only integral solution with `d>=7` is `d=7`. This applies to every vertex, so `G` is
7-regular. Equation (1) now gives

`f_v=2m_v-4`,

and `m_v<=3`, leaving only `(m_v,f_v)=(2,0)` or `(3,2)`.

The `(2,0)` case is impossible. In the more general odd-regular parity lemma, choose a matched pair
`u1,u2` inside `N(v)`. Every `x in S_{u1}` has `k-1` remaining neighbours, at most one in each
block and none in `S_{u2}`. It must therefore have exactly one neighbour in its own block. Thus
`G[S_{u1}]` is 1-regular on `k-2` vertices, impossible when `k` is odd. For `k=7`, the block has
five vertices.

Consequently every vertex has `(m_v,f_v)=(3,2)`. There are exactly 46 edge-disjoint triangles.
Six incident edges at each vertex lie in triangles and the seventh does not, so the non-triangle
edges form a perfect matching `M` with 23 edges.

Every quantifier above is local and applies to an arbitrary vertex. There is no symmetry choice,
search completeness assumption, or omitted graph class in this reduction.

## 4. Deficiency graph and spectral support

Let `A` be the adjacency matrix and let `D` join distinct pairs having no common neighbour. Each
row of `A^2` has diagonal entry seven and 42 off-diagonal ones, so `D` is a simple cubic graph and

`A^2 = 6I + J - D`.                                                            (2)

Regularity gives `AJ=JA=7J`, so `A` and `D` commute and admit a common orthonormal eigenbasis. On
the 45-dimensional space perpendicular to the all-one vector, if `theta` and `mu` are paired
eigenvalues, then

`theta^2=6-mu`.

Every eigenvalue of a cubic graph lies in `[-3,3]`; hence each nonprincipal eigenvalue of `A` lies
in

`[-3,-sqrt(3)] union [sqrt(3),3]`.                                             (3)

This also excludes extra principal eigenvalues and therefore covers disconnected candidates.

## 5. Exact moments

Let `s_j` be the `j`th power sum of the 45 nonprincipal eigenvalues. Direct trace counts and (2)
give

`(s_0,s_1,s_2,s_3,s_4)=(45,-7,273,-67,1785)`.                                 (4)

For the fifth moment put `P=6I-D`. Since `DJ=3J`,

`A^4=P^2+52J`, and `A^5=AP^2+364J`.

Thus

`s_5=-12 tr(AD)+tr(AD^2)+364*46-7^5`.

An edge contributes to `tr(AD)` exactly when it lies in no triangle. The matching `M` gives
`tr(AD)=46`.

For an edge `uv`, write `F_u` for the two vertices at distance at least three from `u`. Then

`N_D(u)={M(u)} union F_u`, and `N_D(u) intersect N_D(v)=F_u intersect F_v`.

Double-counting over the 161 edges yields

`tr(AD^2)=2*kappa`,

where `kappa` counts vertices whose two `F`-vertices are adjacent. Hence `0<=kappa<=46` and

`s_5=T-615`, with `T=2*kappa in [0,92]`.                                      (5)

The wording "distance exactly three" in the candidate is harmless: each far vertex has degree
seven but only the other far vertex outside the distance-two blocks, so it must meet a block and is
indeed at distance three. The proof and double count also work with "at least three."

The audit rederived the general fifth-moment identity using pure-Python integer matrices on the
stored `(10,3)`, `(15,4)`, `(26,5)`, and `(34,6)` regular `C4`-free controls. All matched exactly.

## 6. Exact dual certificate

An especially transparent certificate, independent of the main Sympy root-isolation script, is

`q(x)=(2x+5)^2(3x+5)(4904x^2-38072x+85705)/26468750`,

and `Q(x)=1-q(-x)`. On the negative interval in (3), `q<=0`: `3x+5<0` and the remaining
non-square factor is positive. On the positive interval, `q<=1`, because

`1-q(x)=(3-x)(2x-5)^2(14712x^2+101560x+210075)/26468750 >= 0`.

Therefore `sum q(theta)<=N_+<=sum Q(theta)`, where `N_+` is the integer number of positive
nonprincipal eigenvalues. Substitution of (4)-(5), entirely in rational arithmetic, gives for every
`0<=T<=92`

`sum q(theta) >= 21 + 15497/378125 > 21`,

`sum Q(theta) <= 22 - 1574082/13234375 < 22`.

Thus `21<N_+<22`, impossible. This proves that the assumed graph does not exist.

The independent checker expands both polynomial factorizations, checks all 93 integral `T` values
(a conservative superset of the even feasible values), and has two negative controls: weakening
the bound to `T<=200` breaks the upper certificate, and replacing `sqrt(3)` by `1.73` breaks the
repository's tight main polynomial exactly as warned.

## 7. Ramsey conclusion

The verified 45-vertex graph gives `R(C4,K1,39)>=46`. The universal contradiction above says every
46-vertex graph contains a `C4` or its complement contains `K1,39`, giving the reverse inequality.
Therefore

`R(C4,K1,39)=46`.

## 8. Supplied computation boundary

Both the system environment and a newly created environment with the exact pinned dependencies
ran `run_all_verifiers.py` successfully. The main certificate uses exact Sympy real-root isolation;
all load-bearing values are rational or algebraic, not floating point. The audit's independent
certificate uses arbitrary-precision Python integers and `Fraction` only and passes unchanged under
`python -O`.

The SAT corroboration is not independently certified. `results.jsonl` contains 144 bare `UNSAT`
statuses but no CNF hashes, DRAT/LRAT files, or checked solver proofs; `verify.py` only parses those
statuses. The audit freshly rebuilt and solved subcases 0-2 as UNSAT and reran both encoder controls,
but did not elevate the remaining status lines to proof artifacts. This is **non-load-bearing**
because Sections 3-6 already prove universal nonexistence without SAT.

Python/Numpy integer ranges are safe in the supplied small matrix powers, and the exact audit has no
fixed-width arithmetic. Multiprocessing appears only in the non-load-bearing SAT driver; its parent
serializes result writes.

## 9. Live state and publication-safe scope

The contemporaneous Bright Data capture for Problem 552 displayed `OPEN`, zero claimed proofs, and
`Currently working on this problem: None`. Two public GitHub repositories nevertheless explicitly
claim the exact value: the Zach spectral/moment candidate audited here and
`suitedaces/ramsey-c4-star39`, whose README calls its LRAT computation unreviewed and says its large
proof files are not in Git and its Zenodo deposit is unpublished. The latter was not audited here.
Safe reporting must state the live-page state and must not imply that the audited repository is the
only current claimant or establish priority.

Publication-safe statement:

> At public Git commit `86a1c505...`, an unreviewed candidate proof gives
> `R(C4,K1,39)=46`. An independent hostile audit reconstructed the universal reduction, exact
> moment identity, rational dual certificate, and lower witness and found them valid. This is a
> separately proved exact finite result, not a consequence of Boza's erroneous table cell and not
> yet peer-reviewed.

Consequences that may be stated with the same unreviewed/audited qualification:

- the 46-vertex minimum-degree-seven witness sought in the existing #552 finite report does not
  exist;
- combined with the established value `R(C4,K1,40)=47`, `F(46)=7` in the Problem 85
  translation;
- by the star-wheel theorem, `R(C4,K1+C39)=46`; this graph is Zhang's `W_39`, or `W_40` when
  wheels are indexed by total order.

This does **not** solve the asymptotic question in Problem 552, the eventual-monotonicity question
in Problem 85, establish novelty/priority, or validate the repository's `f(51)` and `f(83)` claims.
Any site correction must attribute the closure to this separately audited proof, not to Boza v1/v2.
