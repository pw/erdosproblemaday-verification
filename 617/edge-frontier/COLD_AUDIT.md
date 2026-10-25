# Cold audit: Problem 617 auxiliary edge frontier

Audited independently on 2026-08-11 UTC.

## Verdict

**PASS** for

\[
m_r=\min\{e(G):v(G)=r^2+1,\ \omega(G)\le r,\ \alpha(G)\le r\}
   =\frac{r^3-r^2+4r-2}{2}
\]

for every integer `r >= 2`, conditional only on Kang--Pikhurko Theorem 1.
This gives `m_5=59`.  It does not settle or improve the known parameter range
of Erdos Problem 617; it is a necessary per-color condition for a balanced
coloring, not a simultaneous color-partition theorem.

## Source and quantifier audit

- A fresh download from the official journal URL is byte-identical to
  `kang_pikhurko_2005.pdf`, with SHA-256
  `2f302962c5f018dc38478293df24f29429b832b061e252c19a7175598c65734e`.
- The paper defines `G_(n,r)` as the `n`-vertex, `K_(r+1)`-free graphs with
  chromatic number greater than `r`, and `p_r(n)` as their maximum edge count.
- Theorem 1 says, for every `r >= 2` and `n >= r+3`, that
  `p_r(n)=t_r(n)-2` when `r>(n-1)/2`, and
  `p_r(n)=t_r(n)-floor(n/r)+1` when `r<=(n-1)/2`.
  The equality case belongs to the second branch.
- At `n=r^2+1`, `n-(r+3)=(r-2)(r+1)>=0` and
  `r<=(n-1)/2=r^2/2`.  This includes the boundary case `r=2`, where equality
  holds in the branch condition.

## Mathematical audit

- For `H=complement(G)`, `alpha(G)<=r` gives `omega(H)<=r`, and hence
  `H` is `K_(r+1)`-free.  Also `alpha(H)=omega(G)<=r`, so
  `chi(H)>=ceil((r^2+1)/alpha(H))>=r+1`.  Thus `H` lies in exactly the family
  covered by `p_r(r^2+1)`.
- The balanced Turan parts are `r+1,r,...,r`; `floor((r^2+1)/r)=r`.
  Complementing the cited upper bound gives
  `e(G)>=C(r+1,2)+(r-1)C(r,2)+r-1`, which expands to the stated formula.
- In the construction of `J`, every `x in X` loses one of its two edges to
  `y_1,y_2`, and both deletion types occur.  The only within-part edge is
  `y_1y_2`, so `J` is triangle-free.  An independent set meeting
  `Y-{y_1,y_2}` cannot meet `X` and has size at most `r`; one contained in
  `X union {y_1,y_2}` also has size at most `r`.  Since `X` is independent,
  `alpha(J)=r`; since `J` has an edge and no triangle, `omega(J)=2`.
- For `G=(r-2)K_r dot-union complement(J)`, the vertex count is `r^2+1`,
  the edge count is the stated polynomial, and disjoint-union identities give
  `alpha(G)=(r-2)+omega(J)=r` and `omega(G)=r`.
- At `r=2`, `J` is a 5-cycle and so is its complement; there are zero `K_2`
  components.  Thus the construction has five edges and clique and
  independence numbers two.  This also explains why the original coloring
  conjecture is false at `r=2`: two complementary 5-cycles use all ten edges.
- A counterexample to Problem 617 would make every color graph have both
  `alpha<=r` (otherwise that color is absent on an `(r+1)`-set) and
  `omega<=r` (a monochromatic `(r+1)`-set misses the other colors).  Summing
  the per-color lower bound leaves exactly
  `C(r^2+1,2)-r*m_r=r(r-1)(r-2)/2` edges of slack, equal to 30 for `r=5`.

## Executable and provenance audit

- `./reproduce.sh` passed under Python 3.12.3.  The direct subset checker and
  the graph6/bitset branch-and-bound checker both return `e(G)=59`,
  `omega(G)=alpha(G)=5`, and edge digest
  `a4e18b2679353aeda7fe389f74edea4bfbba49105da0d0c2b37da510f9a2064a`.
- NetworkX 3.6.1 independently decoded the graph6 string and returned
  `(v(J),e(J),omega(J),alpha(J))=(11,26,2,5)` and
  `(v(G),e(G),omega(G),alpha(G))=(26,59,5,5)`.
- A fresh McKay dataset download has the stated SHA-256, has 30,395 records,
  and contains the frozen graph6 record exactly once.  The dataset is
  provenance only; the witness is checked from its frozen encodings.
- `verify_general.py` is a sound finite regression checker.  Its finite range
  is not evidence for the universal quantifier; the structural written proof
  supplies that quantifier.  The two `r=5` checkers are meaningfully
  independent in encoding and search method, while necessarily checking the
  same labeled witness.
- `sha256sum -c SHA256SUMS` passed before this audit note was added.

## Nonblocking corrections applied after audit

1. In `README.md`, the displayed justification
   `omega(G)=max(r,alpha(J))=r` invokes a `K_r` component that does not exist
   when `r=2`.  It now says: for `r>=3` the maximum over the components is
   `r`, while for `r=2` the sole component is `complement(J)` and has clique
   number `alpha(J)=2`; hence `omega(G)=r` in all cases.
2. The scope now states explicitly that Problem 617 begins at `r>=3`, while
   `r=2` is included only in the auxiliary theorem.  It also records the
   complementary 5-cycle coloring that makes the original statement false at
   `r=2`.
3. The scope language treats the formula as an auxiliary result derived using
   the 2005 extremal theorem and makes only a local scope claim.  It does not
   assert literature priority.

None of these changes affects the theorem or the `r=5` value.
