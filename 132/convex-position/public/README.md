# Problem 132: the convex-position theorem

This package audits the following published partial result:

> Every set of `n >= 5` planar points in convex position has a
> non-diameter distance occurring among at most `n` unordered pairs.

Together with the Hopf--Pannwitz diameter bound, this supplies the two
low-multiplicity distances asked for in Problem 132 when every point is a
vertex of the convex hull. It does not cover arbitrary planar point sets or
the stronger growth question, so Problem 132 remains open.

The theorem is Clemen--Dumitrescu--Liu, Theorem 1.2. Its proof combines the
Altman--Fishburn classification of convex polygons with the minimum possible
number of distinct distances and a short pair count. `REPORT.md` reconstructs
that argument; `SOURCES.md` records official URLs, observed hashes, theorem
locations, and the source boundary.

This public package intentionally contains no third-party PDF, publisher
image, site-source snapshot, or scraped live page. Run `./reproduce.sh` to
check the exact arithmetic and cyclic multiplicities in normal Python,
`-O`, and `-OO` modes, and to run controlled negative tests.
