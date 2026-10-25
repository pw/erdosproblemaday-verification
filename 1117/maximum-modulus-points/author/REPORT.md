# Strict-gate report: Erdos Problem 1117

Audit date: 2026-08-11 UTC

## 1. Verdict

**PASS, but only for a partial literature update and an elementary exact
polynomial subtheorem.**

The publication-safe claims are exactly these:

1. **[b, primary-theorem dependent]** Pardo-Simon and Sixsmith,
   arXiv:2607.09462v1, Theorem 1.1, prove that there is an entire function of
   finite order in the Eremenko-Lyubich class B for which
   `limsup_(r->infinity) v_f(r)=infinity`. This strengthens the already-known
   affirmative answer to the first half of Problem 1117.
2. **[a, elementary]** If
   `p(z)=sum_(j=m)^d a_j z^j`, with `a_m a_d != 0` and `d>m`, then for every
   `r>0` the number `v_p(r)` of maximum-modulus points on `|z|=r` satisfies
   `v_p(r)<=d-m`. The bound is sharp for every `r>0`, simultaneously, for every
   binomial `p(z)=A z^m+B z^d` with `A B != 0`.

**GAP:** The second half of Problem 1117 asks for one non-monomial entire
function with `liminf_(r->infinity) v_f(r)=infinity`. It remains open. Neither
the 2026 preprint nor the polynomial theorem proves it.

No site file was edited or deployed.

Claim labels in this report:

- **[a]** proved here from elementary facts;
- **[b]** rigorous modulo the accurately quoted named primary theorem;
- **[c]** search or interpretation statement, not a completeness theorem;
- **[d]** exact computational/source-snapshot check, not an asymptotic proof.

## 2. Reconstructed problem

For an entire function `f` and `r>0`, put

```text
M(r,f) = max_{|z|=r} |f(z)|,
M(f)   = {z in C : |f(z)|=M(|z|,f)},
v_f(r) = #(M(f) intersect {z:|z|=r}).
```

When `f` is a monomial, every point is a maximum-modulus point, so the problem
excludes monomials. For a non-monomial entire function, `v_f(r)` is finite for
each fixed positive radius. Problem 1117 asks two different questions:

```text
(1) Can limsup_(r->infinity) v_f(r) be infinite?
(2) Can liminf_(r->infinity) v_f(r) be infinite?
```

The distinction is load-bearing. Part (1) only needs arbitrarily large counts
on selected circles. Part (2) requires the count to be large on every
sufficiently large circle.

## 3. Strict eligibility gate

### 3.1 Exact-number absence

The frozen site snapshots are:

- `sources/site_index_20260811.js`;
- `sources/site_ledger_data_20260811.js`.

The scanner checks both article schemas used by the site, `problemNum: N` and
legacy/offsite rows `{n:N,...}`. Problem 1117 occurs in neither snapshot.

At capture time the site checkout was at commit
`7cf9bd43c89f1d9e144535ce447264b8d28cd95a`; `src/ledger_data.js` had an
uncommitted change made outside this audit. The SHA-256 snapshot in the manifest,
not the mutable checkout, is the frozen authority.

### 3.2 Defining-framework absence

Literal scans of both full snapshots find none of:

```text
maximum modulus point
maximum-modulus point
maximum modulus set
maximum-modulus set
maximum curve
```

Thus the defining object here, the angular maximizer set on each circle and its
cardinality, is absent.

The following thematic adjacencies are disclosed rather than hidden:

- **#513** studies the scalar ratio between the largest Taylor term and
  `M(r,f)`. It uses the maximum modulus as a number but does not define or count
  its angular maximizers.
- **#517** studies values assumed by Fabry-gap entire functions. It is a value
  preimage/Picard problem, not a maximum-modulus-point problem.
- **#1040** cites a different Erdos-Herzog-Piranian paper about polynomial
  lemniscates and transfinite diameter. It does not use the 1968 counting
  function.

These are real subject adjacencies. They are not the substantive defining
framework of Problem 1117.

### 3.3 Live gate

The Bright Data snapshot in `sources/live_1117_20260811.json` captured the main
page, LaTeX page, newest-first discussion, proof-claim page, and history page at
2026-08-11T18:33:52Z. It records:

```text
status                         OPEN
claimed proofs                 0
proof-claim page               No proof claims have been submitted yet.
Currently working              None
Interested in collaborating    None
formalisation worker           None
```

The one comment only supplies the arXiv link for the 2024 paper. It is not a
proof claim.

The frozen scratch inventory has no other top-level directory whose name
contains `1117`. A full text scan outside this bundle found exactly two passive
mentions: the earlier negative gate report lists 1117 among rejected candidates,
and a broad `live_pages.json` cache contains its page text. Neither is a target
proof/computation bundle. Both hits and their classification are frozen in
`sources/scratch_collision_scan_20260811.json`.

### 3.4 Upstream and OEIS

The frozen `teorth/erdosproblems` metadata is at upstream commit
`6929b78952e18c11d5cb28fe9438081ee1d49448`. Its Problem 1117 row says
`state: open`, `formalized: no`, and `oeis: N/A`. Targeted OEIS web searches for
the exact maximum-modulus-points phrase returned no result. There is no
sequence lookup or OEIS value used in the result.

## 4. Current primary literature

### 4.1 What the live page says

The live page was last edited 29 December 2025. It says:

- Herzog and Piranian (1968) answered part (1) affirmatively;
- Glucksam and Pardo-Simon (2024) obtained an approximate affirmative result
  toward part (2);
- part (2) remains open.

The page cannot include a preprint posted in July 2026 unless edited later, and
the frozen history confirms no such later edit.

### 4.2 2024 approximate result

The frozen current arXiv source is arXiv:2208.11154v2, published in the
`Journal of Mathematical Analysis and Applications` in 2024. Its construction
provides, on every sufficiently large circle, many separated arcs where the
function comes arbitrarily close to its maximum modulus, with low-modulus arcs
between them. The source explicitly says the method is **unable to conclude**
that those near-maximum arcs contain an unbounded number of actual maximum
points. It therefore does not settle part (2).

### 4.3 July 2026 finite-order result

The arXiv API snapshot taken on 11 August 2026 identifies
arXiv:2607.09462v1, posted 10 July 2026, as the current version of:

> A finite-order answer to a problem of Erdos on maximum modulus points

Theorem 1.1 states, with the quantifiers needed here:

```text
There is an entire function f in class B, of finite order, such that
limsup_(r->infinity) v_f(r)=infinity.
```

The end of its proof gives the more concrete selected-radius conclusion
`v_f(exp(x_n)) >= 2n+1`, with `x_n -> infinity`. The same paper explicitly says
that the second part remains open and that its construction gives no useful
control of `v_f(r)` away from prescribed radii.

Therefore this is a strict strengthening of the solved **limsup** half, not a
solution of the **liminf** half. It is also an arXiv v1 preprint; this report
does not describe it as peer reviewed.

The paper's Theorem 1.2, which interpolates prescribed maximum-modulus points
on pairwise distinct circles, also does not imply multiple maximizers on every
large circle.

### 4.4 Polynomial literature

The bundle includes arXiv:2007.07529v1, later published as Pardo-Simon and
Sixsmith, *The maximum modulus set of a polynomial* (2022). It constructs
polynomials with prescribed discontinuities or singleton components of their
maximum-modulus sets and proves finiteness of discontinuities. The targeted
source inspection did not locate the support-span bound below.

**[c]** This search fact is not a novelty theorem. The elementary polynomial
bound may be known or implicit elsewhere, and no originality claim is made.

## 5. Sharp polynomial frontier

### Theorem [a]

Let

```text
p(z) = sum_(j=m)^d a_j z^j,
```

where `a_m a_d != 0` and `d>m`. For every `r>0`,

```text
v_p(r) <= d-m.
```

For every `m<d` and every nonzero complex `A,B`, the binomial

```text
p(z) = A z^m + B z^d
```

has `v_p(r)=d-m` for every `r>0`. Hence the maximum possible value at any
fixed radius among polynomials of support span `s=d-m` is exactly `s`.

### Proof

Fix `r>0` and write `z=r exp(i theta)`. Set

```text
H(theta) = |p(r exp(i theta))|^2.
```

Expanding gives the real trigonometric polynomial

```text
H(theta) = sum_(j,k=m)^d
           a_j conjugate(a_k) r^(j+k) exp(i(j-k)theta).
```

Put `s=d-m`. The Fourier coefficient of frequency `s` is

```text
a_d conjugate(a_m) r^(d+m),
```

because `j-k=s` has the unique supported solution `(j,k)=(d,m)`. It is
nonzero. Thus `H` has exact trigonometric degree `s` and is nonconstant.

Its derivative `H'` is a nonzero trigonometric polynomial of degree `s`.
After multiplying by `exp(i s theta)`, it becomes an ordinary polynomial in
`exp(i theta)` of degree at most `2s`. A nonzero ordinary polynomial of degree
at most `2s` has at most `2s` distinct roots, so `H'` has at most `2s`
distinct zeroes modulo `2 pi`.

Let `q=v_p(r)`. Each global maximum of `H` is a zero of `H'`. Between every
two cyclically consecutive global maxima, `H` is strictly below its maximum
somewhere and attains an interior minimum, which is another zero of `H'`.
This also works when `q=1`, using the single complementary arc around the
circle. Hence `H'` has at least `2q` distinct zeroes. Therefore

```text
2q <= 2s,
q <= s = d-m.
```

For sharpness, factor the harmless common phase from a binomial on the circle:

```text
|A r^m exp(i m theta) + B r^d exp(i d theta)|
= |A r^m + B r^d exp(i(d-m)theta)|.
```

By equality in the triangle inequality this is maximal exactly when the two
summands have the same argument. The equation fixes
`exp(i(d-m)theta)` and has exactly `d-m` solutions modulo `2 pi`. Thus every
positive circle contains exactly `d-m` maximum-modulus points. QED.

### Independent finite sanity check [d]

`verify_polynomial_frontier.py` uses exact integer arithmetic to exhaust all
coefficient vectors in `{-1,0,1}` through nominal degree 7 that have at least
two nonzero coefficients, at radii `1,2,3,5`. It verifies that the extreme
Fourier harmonic is exactly the endpoint product and that its degree equals
the support span. It separately verifies the root-of-unity phase count for
spans 1 through 40.

This program checks the load-bearing algebra. It is not substituted for the
analytic zero-count proof above.

## 6. Why this does not solve the open half

A fixed non-monomial polynomial has a fixed finite support span, so the theorem
actually shows that its `v_p(r)` is uniformly bounded. Polynomial examples can
never make either limiting count infinite.

The elementary entire examples `exp(z^N)` have exactly `N` maximum points on
every positive circle, but `N` is fixed for each function. Choosing a different
function for every desired count does not produce one function whose count
tends to infinity.

The 1968 and 2026 constructions make the count large on selected radii, which
is enough for `limsup`. Approximate near-maximal arcs on every large radius do
not force actual equal maxima. That exact-equality stability gap is the current
wall for `liminf`.

## 7. Publication-safe scope

Safe wording:

> Problem 1117 remains open in its liminf form. A July 2026 preprint of
> Pardo-Simon and Sixsmith strengthens the known affirmative limsup result by
> constructing a finite-order class-B entire function with unbounded numbers
> of maximum-modulus points on selected circles. Independently, a
> non-monomial polynomial whose nonzero exponents span `d-m` has at most
> `d-m` such points on every circle, sharply attained by binomials.

Unsafe wording, expressly rejected:

- "Problem 1117 is solved."
- "The number tends to infinity for the 2026 construction."
- "The 2026 paper proves the liminf half."
- "The polynomial theorem is new to the literature."
- "The live page is current through July 2026."

## 8. Reproduction and frozen contents

Run:

```bash
./run_all.sh
```

The command verifies exact-number and defining-framework absence, live status
and activity fields, upstream OPEN/OEIS metadata, the load-bearing primary
source strings and quantifiers, the exact finite algebra checks, and every
SHA-256 entry in `MANIFEST.sha256`.

The manifest covers the report, scripts, live snapshots, site/upstream
snapshots, arXiv API results, and frozen primary PDFs/source archives. The
manifest does not list itself, avoiding self-reference.
