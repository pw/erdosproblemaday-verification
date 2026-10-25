# Provenance audit for Erdős problem #773

Access date: 2026-08-11 UTC.

## Live problem status

The live page <https://www.erdosproblems.com/773> displayed:

- status `OPEN`;
- the question asking whether the maximum square-Sidon subset of
  `{1^2,...,N^2}` has size `N^(1-o(1))`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- 11 comments and a last-edit date of 24 April 2026; and
- OEIS A390813 as the related sequence.

The checked-out upstream tracker at commit
`6929b78952e18c11d5cb28fe9438081ee1d49448` likewise lists #773 as open
and links A390813.

## OEIS finite frontier

The live page <https://oeis.org/A390813> defined `a(n)` as the size of the
largest Sidon subset of the first `n` positive perfect squares.  It labeled
its data link `Table of n, a(n) for n=1..68`; its displayed sequence ends
with

```text
a(64)=31, a(65)=31, a(66)=31, a(67)=32, a(68)=32.
```

The entry credits `a(43)-a(68)` to Christian Sievers on 27 November 2025.
The proof here uses the full displayed prefix as published computational
input: `a(68)=32` forces a hypothetical 33-set at 69 to contain 69, while
the earlier `a(k)` values are upper bounds during the recursive search.
This project did not independently re-prove those earlier upper bounds.

## Prior local attempt

This target is not new to Erdős Problem A Day.  The local `src/index.js`
contains an off-site ledger entry dated 2026-07-25:

```text
#773, Sidon subsets of the squares: No proof of the N^(1-o(1)) bound. Open.
```

The present computation is a distinct finite-frontier extension, not a
first attempt on #773 and not progress on the asymptotic exponent.

## Primary bibliography

Crossref metadata was checked for the two lower-bound papers cited on the
live problem page:

- N. Alon and P. Erdős, "An Application of Graph Theory to Additive Number
  Theory," *European Journal of Combinatorics* 6(3) (1985), 201-203,
  DOI <https://doi.org/10.1016/S0195-6698(85)80027-5>.
- H. Lefmann and T. Thiele, "Point sets with distinct distances,"
  *Combinatorica* 15(3) (1995), 379-408,
  DOI <https://doi.org/10.1007/BF01299744>.

The live page attributes the lower bounds `N^(2/3-o(1))` and `>> N^(2/3)`
to these papers, respectively.  Those asymptotic results are context only;
they are not used in the finite proof.

## Novelty boundary

The audited conditional values at 69 and 70 extend the displayed OEIS table
by two positions.  That is evidence of novelty relative to the public OEIS
frontier accessed above, not proof that the values are absent from all
private computations or all literature.  No global novelty claim is made.
