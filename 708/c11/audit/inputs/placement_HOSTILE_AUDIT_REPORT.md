# Hostile audit: Erdos 708 c11 placement lemma

Date: 2026-08-11 UTC

## Verdict and scope

**PASS, for the standalone `K_(3,4)-e` placement lemma only.**

I found no mathematical gap in the claim that an admissible tuple

```text
q_(01,a), q_(02,b), q_(12,c), q_(12,d)
```

has four distinct representatives outside the seven kernel vertices for some
`a,b in {1,2,3}` and distinct `c,d in {0,1,2,3}` satisfying

```text
not (a=b and a in {c,d}).
```

This verdict does not assert `c_11=2`, does not certify the new deficit-two or
deficit-three eleven-edge kernels, and does not certify an aligned-endpoint
argument.

There is one non-fatal editorial ambiguity.  At candidate lines 323-326, if
`a=b=j` and the three selected `C` columns do not contain `j`, the proof should
say to discard any one of the three `C` blocks.  The remaining two automatically
avoid `j`.  The existing sentence explicitly says what to discard only when
column `j` is present.  This is not a mathematical gap.

The audited candidate is frozen at

```text
1fac030bc7a14cf059d52f047edd4b25c1daf629f1e4d0021ca61732f2f51c1d
```

under `inputs/erdos708_c11_placement_candidate.md`.  `MANIFEST.sha256` fixes
the candidate, all other supplied inputs, this report, the independent code,
and the run logs.

## Proof reconstruction

### Strict multiple counts

For `Z(q)=q Z intersect (x,x+2M)`, spacing alone gives

```text
|Z(q)| >= ceil(2M/q)-1.
```

If `q` divides `k` distinct positive labels at most `M`, their distinct
positive quotients force `kq<=M`, hence `|Z(q)|>=2k-1`.  The `-1` is necessary
when both open endpoints are multiples and `2M/q` is integral; no closed-end
count is used silently.

For a confined block on row pair `i,k`, set `D=|L_i-L_k|` and `m=D/q`.
The `m-1` internal multiples of `q` can contain only the third row vertex from
`F`; all others lie in the common outside set `T`.  Thus

```text
m <= t+2,  P_m subset {third row} union T.
```

If an occurring `m_0` is fixed, `D/m_0` divides both labels in every block
whose denominator `m` divides `m_0`.  The supports are in distinct columns, so
for `C_(m_0)=sum_(m|m_0)n_m` it divides `2C_(m_0)` distinct labels.  Since the
`m_0` block is confined,

```text
4C_(m_0)-1 <= 7+t.
```

The equality cases are load-bearing and are valid:

* At `t=0`, `C=2` gives at least seven multiples inside the seven-point set
  `F`.  Therefore every kernel vertex is divisible.  All eleven exact
  differences are then divisible, requiring at least 21 multiples, still
  inside `F`, a contradiction.  Consequently the true bound here is `C<=1`.
* At `t=4`, the only extra numerical possibility is `C=3`.  It gives at least
  eleven multiples inside the eleven-point set `F union T`.  Equality again
  makes all seven kernel vertices divisible, so all eleven labels are
  divisible and at least 21 multiples are required.  This contradicts the
  same confinement.  Thus `C<=2` here as well.

Exact rational enumeration confirms every remaining denominator case.  For
`t=1`, three blocks cannot fit.  For `t=2` or `3`, every profile of at least
three blocks contains denominators 2 and 3, so its midpoint and trisection
points occur.  With `t=2`, four blocks have the unique profile `(2,2,3,3)`.
For `t=4` when the third row is outside the selected row interval, the same
midpoint/trisection triple must lie in `T` itself.

### Konig ranks

Applying Konig to an alleged rank failure gives a cover with `h` left block
occurrences and `t` common outside points.  Every undeleted occurrence is
confined to that same `T`.  Exhausting all 120 numerical cover profiles gives
exactly the claimed bounds:

```text
r(A)>=1, r(B)>=1, r(C)>=3, r(A union B)>=2,
r(A union C)>=4, r(B union C)>=4,
r(A union B union C)>=5.
```

The exceptional `r(C)<=2`, `t=2` profile is sound.  Four confined `C` blocks
force `n_1=0` and `n_2=n_3=2`.  The third row is a midpoint or trisection point.
The corresponding repeated `q_*` divides all three row vertices and two right
vertices.  Those five vertices induce at least five existing edges, including
when one selected column is column zero.  Thus `q_*` has at least nine interval
multiples, all in the nine-point `F union T`; every kernel vertex is therefore
divisible.  The resulting eleven supported labels require 21 multiples, a
contradiction.

The mixed and full-rank cases use only two geometry facts.  Only one row pair
can contain its third row, and two midpoint/trisection triples sharing a row
leave at least four points after removal of the two third-row vertices.  For
`t=4`, the two adjacent row intervals are disjoint and contribute six internal
points to a four-point `T`.  These cover all deletion allocations; no equality
case is skipped.

### Rado selection and discard

Apply Rado to the five sets `A,B,C,C,C` in the transversal matroid.  All 31
nonempty subfamilies are covered by the seven rank inequalities above.  The
result is one `A`, one `B`, and three distinct `C` occurrences with a joint
five-point matching.

If `a!=b`, retain any two selected `C` blocks.  If `a=b=j`, retain any two
selected `C` blocks whose columns are not `j`; three distinct columns among
four always contain at least two such columns.  This includes both branches:
discard column `j` when selected, or discard an arbitrary `C` when `j` is not
selected.  Independence is hereditary, so the retained four blocks keep four
distinct outside representatives and satisfy the admissibility condition.

## Independent checks

`independent_check.py` imports none of the supplied programs and uses Hall
subfamily enumeration rather than their augmenting-path matcher.  Its default
run checked:

```text
151,280 exact open-interval counts, including sharp endpoint cases
all confined denominator profiles through t=4
46,620 exact integer-coordinate geometry triples (minimum union 4)
120 Konig cover profiles
17 positive-excess induced levels and the advertised 45-tuple interface
all 31 Rado subfamilies and all 36 (1,1,3) discard patterns
35,948 finite interval modes
2,108 literal exact-difference kernels, with labels allowed to be < M
```

The literal sweep used `11<=M<=48`, `-2M<=floor(x)<=14M`, and both possible
integer-point patterns for integer and noninteger `x`.  It also checked the two
named kernels separately, including `M=70,x=805`, where one `C` neighborhood is
empty.  No rank or placement counterexample was found.

Run:

```bash
./run_all.sh
```

The finite checks are corroboration.  The written count, equality, Konig, and
Rado arguments above are what cover arbitrary `M`, positions, and valuations.

## Remaining full-c11 dependencies

The following are outside this PASS and remain necessary for a complete
`c_11=2` upper proof:

1. A separately audited four-defect valuation/divisibility certificate and its
   integration into the generic Hall reduction.  This audit checked only that
   the advertised 45 admissible tuples agree with the placement lemma's
   interface.
2. Classification, layer certificates, and placement for every genuinely new
   inclusion-minimal eleven-edge Hall-deficit-two and Hall-deficit-three
   kernel.  Nothing about those cases is inherited by this report.
3. In the aligned injection, robustness of every needed ten-label certificate
   under the exceptional two-adic matching.
4. An endpoint-safe aligned construction of ten cover points avoiding the
   unique midpoint multiple of `M`.  The published `c_10` aligned proof places
   only nine labels away from that midpoint and cannot be reused without this
   new step.

The published private-prime padding theorem already supplies `c_n>=2` for
`n>=4`; the dependencies above concern the new `c_11<=2` argument.
