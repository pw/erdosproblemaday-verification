# Problem 1109 source and novelty check

Access date: 2026-08-11 (UTC).

## Live problem status

The rendered page at <https://www.erdosproblems.com/1109> was fetched through
a browser session because plain datacenter requests returned HTTP 403. It
reported:

```text
OPEN
0 claimed proofs for this problem
Interested in collaborating  None
Currently working on this problem  None
This page was last edited 03 December 2025.
```

Its statement is: let `f(N)` be the largest size of
`A subseteq {1,...,N}` such that every member of `A+A` is squarefree; estimate
`f(N)`, in particular asking whether `f(N) <= N^(o(1))`, or even a power of
`log N`. The page states Konyagin's current bounds

```text
log log N (log N)^2 << f(N) << N^(11/15+o(1)).
```

## OEIS comparison

The rendered OEIS pages and b-files for A392164 and A392165 were re-opened on
the access date. A392164 defines the same function and its linked table ended
at `N=425`. A392165 listed 39 record indices and ended

```text
..., 889, 1003, 1055, 1067, 1103.
```

The exact downloaded files used for comparison are

```text
8b310617ac471f133d13575fdaae89f75644ab4914ceabf244c6f5bf1733bf14  oeis_A392164_bfile_accessed_2026-08-11.txt
db9fdc992230ab6e7f5996cb55e5d334d4bac13014711dc1f34de64316b08dbe  oeis_A392165_bfile_accessed_2026-08-11.txt
```

Exact-phrase web searches for the five proposed terms, for `f(1407)` with
squarefree sumsets, and for `A392165 1407` found no matching mathematical
source. This is a dated search result, not a theorem that the values have
never been computed privately or in an unindexed source.

## Primary literature

The downloaded scan
<https://renyi.hu/~p_erdos/1987-13.pdf> is:

```text
179cf92b5b70a179290e00c78d03a0ec5de7d008f4189c37ed99077389f3dae3  erdos_sarkozy_1987_13.pdf
```

It is P. Erdos and A. Sarkozy, "On divisibility properties of integers of
the form a+a'", *Acta Mathematica Hungarica* 50 (1987), 117-122. Its first
page formulates the condition for every `a,a' in A`, so the diagonal case is
included, and states their original logarithmic lower and
`N^(3/4) log N` upper bounds and conjectural `N^epsilon`/polylogarithmic
scale.

The current improvement was checked against S. V. Konyagin, "Problems on
the set of squarefree numbers", *Izvestiya: Mathematics* 68:3 (2004),
493-520, DOI `10.1070/IM2004v068n03ABEH000486`, on its official Math-Net.Ru
record. The abstract uses `a+a'` for all `a,a' in A`; the article is the
source of the `11/15+o(1)` upper exponent and the currently quoted lower
bound.

## Site provenance

The local ErdosProblemADay source already contains the entry
`1109-squarefree-sumset`, dated 2026-07-24. It discusses the analytic
problem and does not claim an exact extension of A392165. Therefore this
bundle's novelty scope is a later exact finite update to an existing site
attempt, not a first attempt at Problem 1109 and not progress on the parent
asymptotic exponent.

