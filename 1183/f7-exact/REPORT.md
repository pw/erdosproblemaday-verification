# Erdős Problem 1183: the exact finite values `f(7)=4`, `F(7)=7`

Date: 2026-08-12 UTC

## Result

Let `f(n)` be the analogous quantity for families closed under both union and
intersection, and let `F(n)` be the largest integer such that every red-blue colouring of the
subsets of `[n]` contains a monochromatic union-closed family of at least
`F(n)` sets. Then

\[
\boxed{f(7)=4,\qquad F(7)=7}.
\]

This is a finite computer-assisted result. It does not settle the asymptotic
questions in Problem 1183 and makes no novelty or priority claim.

The project previously proved

\[
f(1),\ldots,f(6)=1,2,2,3,3,4,
\qquad
F(1),\ldots,F(6)=1,2,2,3,4,5.
\]

Thus this result extends that exact table by one case.

## Live collision gate

The problem page and its complete ten-comment discussion were fetched through
Bright Data on 2026-08-12. The live state was:

- `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- `Interested in collaborating: None`;
- no formalisation worker.

The comments concern recent asymptotic partial arguments, not this finite
value. Frozen page and forum transcripts are included as `LIVE_PAGE.txt` and
`LIVE_FORUM.txt`.

## Lower bound: every colouring contains seven sets

Represent a subset of `[7]` by its seven-bit integer mask. Introduce one
Boolean variable `x_A` for each of the 128 subsets, with `x_A=true` meaning
red. Swapping the two colours lets us fix the empty set blue, so the CNF starts
with `-x_empty`.

For every selected seven-member union-closed family `L`, a clause excludes it
from being monochromatic:

- if `L` is tested as red, the clause is `OR_{A in L} not x_A`;
- if `L` is tested as blue, the clause is `OR_{A in L} x_A`.

`lower_core.cnf` contains the symmetry unit and 42,034 such clauses. The
standard-library checker parses every clause and verifies directly that:

1. it has seven distinct masks in `[0,127]`;
2. those masks are closed under bitwise union;
3. all seven literals have the sign claimed above; and
4. no family clause is duplicated.

There are 22,232 red-family clauses and 19,802 blue-family clauses. CaDiCaL
proves this CNF unsatisfiable. The included binary DRAT proof is independently
replayed by `drat-trim`; the frozen transcript ends `s VERIFIED`, with 35,488
of the 42,035 input clauses in its final core and no RAT lemmas.

Consequently every two-colouring, after the harmless colour swap, contains at
least one of these explicitly definition-checked monochromatic seven-member
families. Hence `F(7)>=7`.

The public certificate hashes are:

```text
lower_core.cnf   7b1c05b745e0ca661232a1d478c855bcb4685f0d00abb291066efe9be9eda5fb
lower_core.drat  92db723a46d0db7dabebef7c3633bfd4dfca6ca6d26fdcfabb2fed216aaa0fa5
```

## Upper bound: a rank colouring with maximum seven

Colour ranks `3,4,6` red and ranks `0,1,2,5,7` blue. The checker independently
performs an exact closure-propagating include/exclude search and obtains colour
maxima `6` and `7`. Here is also a short elementary proof.

### Red families

Let `R` be red and union-closed. It contains at most one six-set, since two
distinct six-sets have blue union `[7]`.

If there is no six-set, there is at most one four-set. If that four-set `T`
exists, every selected three-set must lie inside `T`, giving at most four
three-sets and five sets total. If there is no four-set either, two selected
three-sets would have a union of rank four, five, or six: the first and last
are absent by assumption, while rank five is blue. Hence there is then at
most one three-set.

Now suppose the unique six-set is `S`. Every other member lies inside `S`.
The complements in `S` of selected four-sets are disjoint pairs, so there are
at most three. Write `b` for their number and `a` for the number of selected
three-sets.

- If `b=3`, the complementary pairs partition `S`. A three-set would have to
  meet each pair in zero or two points, impossible because its size is odd;
  hence `a=0`.
- If `b=2`, the two complementary pairs leave one pair. The only possible
  three-sets are one complementary pair plus one leftover point, and their
  pairwise compatibility gives `a<=2`.
- If `b=1`, writing the complementary pair as `P`, a three-set is either a
  three-subset of `S\P` or `P` plus one point. The former contribute at most
  four; if one of the latter occurs, it is compatible with only one of the
  former. Thus `a<=4`.
- If `b=0`, two selected three-sets must be disjoint, so `a<=2`.

In every case `a+b<=5`; including `S` gives at most six red sets.

### Blue families

Let `B` be blue and union-closed. It has at most one two-set `E`, since the
union of two distinct two-sets has red rank three or four. Complements of
selected five-sets are pairwise disjoint pairs, so there are at most three.

If no `E` is selected, there is at most one singleton and hence at most
`1+1+3+1=6` sets, counting the possible bottom and top.

If `E` is selected, every selected singleton lies in `E`. A selected five-set
either contains `E`, or is exactly `[7]\E`; the intermediate case has a red
six-set as union with `E`.

- If `[7]\E` is present, no singleton is allowed. At most two further
  five-sets occur, giving at most six sets total.
- Otherwise, all five-set complements are disjoint pairs in the five points
  outside `E`, so there are at most two. With at most two singletons, bottom,
  `E`, and top, the total is at most seven.

The bound occurs. In mask notation one blue family is

```text
0, 1, 2, 3, 31, 103, 127.
```

Therefore this colouring has no monochromatic union-closed family larger than
seven, proving `F(7)<=7`.

## The exact lattice-closed value `f(7)=4`

The eight members of a maximal chain in `2^[7]` are closed under union and
intersection. Every red-blue colouring gives at least four of them one colour,
and every subchain is still closed under both operations. Thus `f(7)>=4`.

For the reverse inequality, colour ranks `0,2,3,5` red and ranks `1,4,6,7`
blue. The standard-library verifier runs a second exact include/exclude search,
now propagating both union and intersection. Its colour maxima are exactly
`4,4`, with witnesses

```text
red:   0, 3, 7, 31
blue:  1, 15, 63, 127.
```

The recursion records every excluded mask as forbidden, rejects a branch if
closure would force a forbidden or oppositely coloured mask, and prunes only
when the chosen closure plus all remaining candidates cannot beat the current
best. It therefore exhausts every monochromatic sublattice.

As a simpler independent check, `audit_lattice_upper.cpp` enumerates every
five-set of seeds in both colour classes: 21,111,090 red choices and 2,118,760
blue choices. It generates each seed set's full union/intersection closure and
finds zero closures staying monochromatic. Any sublattice of size at least five
contains five seeds whose closure stays inside it, so this directly proves the
same upper bound. Hence `f(7)=4`.

## Reproduction

On x86-64 Linux:

```sh
./reproduce.sh
```

The script verifies the closed SHA-256 manifest, runs the definition-level
checker, compiles and runs the independent five-seed audit, and replays the
DRAT proof. The default verification takes about 20 seconds on this VM.
`drat-trim` is the same audited executable already
distributed with the project's Problem 813 certificate; its hash is bound by
this bundle's manifest.

## Scope

This exact case gives no uniform asymptotic mechanism. The open questions ask
for the growth of `f(n)` and `F(n)`, including superpolynomial lower and
subexponential upper behaviour for `F`. A fixed `n=7` certificate cannot
address that wall.

PARTIAL: Exact exhaustive certificates prove the finite values `f(7)=4` and `F(7)=7`; the asymptotic Erdős-Ulam problem remains open.
