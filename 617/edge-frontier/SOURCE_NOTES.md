# Published theorem dependency

M. Kang and O. Pikhurko, *Maximum K_(r+1)-free graphs which are not
r-partite*, Matematychni Studii 24 (2005), 12-20.

- DOI: `10.30970/ms.24.1.12-20`
- Official article page:
  <https://matstud.org.ua/texts/2005/24_1/24_1_012_020.html>
- Official PDF:
  <https://matstud.org.ua/texts/2005/24_1/24_1_012_020.pdf>
- Archived PDF SHA-256:
  `2f302962c5f018dc38478293df24f29429b832b061e252c19a7175598c65734e`
- Locator: Theorem 1, journal page 13, PDF page 2.  The definitions of
  `G_(n,r)`, `t_r(n)`, and `p_r(n)` begin on journal pages 12-13.

The theorem's full parameter split is:

- for every integer `r >= 2` and `n >= r+3`;
- if `r > (n-1)/2`, then `p_r(n)=t_r(n)-2`;
- if `r <= (n-1)/2`, then
  `p_r(n)=t_r(n)-floor(n/r)+1`.

Here `p_r(n)` is the maximum edge count over all `n`-vertex graphs that are
`K_(r+1)`-free and have chromatic number greater than `r`.  This bundle uses
the second branch at `n=r^2+1` for every `r>=2`; its `r=5` specialization is
`(n,r)=(26,5)`.

The archived PDF is included to make the exact theorem statement and its
context independently inspectable.  The finite checkers do not verify the
paper's proof.

## Witness provenance

The explicit `r=5` graph has graph6 string ``JiQC@{}N`{?``.  It was extracted
from Brendan McKay's `r36_11.g6.gz` Ramsey graph file at
<https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>.  The downloaded gzip
file had SHA-256
`628c53df90910b2aae9a9559a62605593ff6fcdac66e9f23f95a134a4a696f36`,
contained 30,395 records, and contained this string exactly once.  The dataset
is not required for reproduction because both the graph6 string and a decoded
edge list are frozen in the checkers.
