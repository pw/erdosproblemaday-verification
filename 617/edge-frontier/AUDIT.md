# Audit record

## Verdict

**PASS for the exact auxiliary theorem
`m_r=(r^3-r^2+4r-2)/2` for every `r>=2`, conditional only on the cited
published Kang--Pikhurko Theorem 1.**  In particular, `m_5=59`.

**Not a solution or a certified new bound for the color-partition statement in
Problem 617.**  The result supplies one necessary per-color edge bound for a
hypothetical counterexample at each `r`.

## Checks performed

1. The official nine-page Kang--Pikhurko PDF was downloaded from the journal.
   Its SHA-256 is
   `2f302962c5f018dc38478293df24f29429b832b061e252c19a7175598c65734e`.
   The definition of `p_r(n)` and every hypothesis and branch in Theorem 1
   were checked against journal page 13 (PDF page 2).
2. At `n=r^2+1`, all hypotheses hold for every `r>=2`:
   `n-(r+3)=(r-2)(r+1)>=0` and `r<=(n-1)/2=r^2/2`.  The balanced Turan parts
   are `r+1,r,...,r`, and `floor(n/r)=r`.  The lower formula follows by exact
   complementation.
3. The graph-theoretic transfer is exact: for `H=complement(G)`,
   `alpha(G)<=r` makes `H` `K_(r+1)`-free, while
   `alpha(H)=omega(G)<=r` gives
   `chi(H)>=ceil((r^2+1)/alpha(H))>=r+1`.  Thus `H` is in the precise family
   to which `p_r(r^2+1)` applies.
4. The edge-list checker exhausts all 165 triples and 462 six-subsets of `J`,
   then all 230,230 six-subsets of the constructed 26-vertex graph.  It finds
   zero triangles and zero independent six-sets in `J`, and zero cliques or
   independent sets of size six in `G`.
5. The independent checker starts from the graph6 string instead of the edge
   list, validates its encoding, uses bitset complementation, and obtains exact
   maximum clique and independence sizes via a separate include/exclude
   recurrence.  Both checkers obtain `e(G)=59` and the same canonical edge
   digest.
6. NetworkX 3.6.1 was used once as a non-load-bearing third decoder check of
   the graph6 string.  It returned the same 11 vertices, 26 edges, and edge
   list.  The bundle itself has no NetworkX dependency.
7. The general construction checker validates the defining graph pattern
   through `r=50`, exact forbidden-subset conditions over a small regression
   range, and all edge/lower/slack polynomial identities through `r=10000`.
   The written proof supplies the universal quantifier.

## Completeness boundaries

- Exhausting 6-subsets is a complete certificate of `omega(G)<=5` and
  `alpha(G)<=5`; no heuristic graph search or floating-point computation is
  used.
- The all-`r` upper construction is explicit and proved structurally.  Brendan
  McKay's complete Ramsey `(3,6)` dataset explains where the initially found
  `r=5` instance came from but is not a proof dependency.
- The lower bound invokes a published exact extremal theorem.  This bundle
  checks its applicability and arithmetic but does not independently reprove
  that theorem.
- An earlier tentative SAT route toward `m(6,6;26)>=65` was false: valid
  models already appeared under a 63-edge cap.  Those large exploratory CNFs
  are excluded from this proof bundle.  The explicit 59-edge construction
  explains the failure decisively.
- The color graphs in Problem 617 must form an edge-disjoint partition of
  `K_(r^2+1)`.  Nothing here proves or disproves simultaneous compatibility.
  The summed class bounds leave exactly `r(r-1)(r-2)/2` edges of slack; this is
  30 at `r=5`.
- Local site source already records a 2026-05-26 partial attempt on Problem
  617.  This bundle therefore makes no claim that the problem itself was
  previously unattempted; only the exact 59-edge auxiliary frontier is new in
  the local work reviewed here.
