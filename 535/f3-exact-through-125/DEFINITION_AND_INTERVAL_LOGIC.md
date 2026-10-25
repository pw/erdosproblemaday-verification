# Independent reconstruction of the claim

The live statement defines `f_r(N)` as the largest cardinality of a subset of
`{1,...,N}` for which no `r`-element subset has one common value for all of its
pairwise greatest common divisors.

For `r=3`, an unordered triple of **distinct** integers `{a,b,c}` is therefore
forbidden exactly when

```text
gcd(a,b) = gcd(a,c) = gcd(b,c).
```

Consequently `f_3(N)` is the independence number of the 3-uniform hypergraph
whose vertices are `1,...,N` and whose edges are exactly those forbidden
triples.  Neither repeated elements nor diagonal gcds occur because the live
word is *subset*, not tuple or multiset.

For an interval `[L,U]`, a definition-level independent `k`-set contained in
`[L]` proves `f_3(N) >= k` for every `N >= L`.  Exhaustive nonexistence of an
independent `(k+1)`-set in `[U]` proves `f_3(N) <= k` for every `N <= U`.
The two inequalities overlap throughout `[L,U]`, proving equality there.

Applied to the proposed rows, the exact proof obligations are:

| interval | lower obligation at `L` | upper obligation at `U` |
|---|---|---|
| 101..107 | independent 14-set in `[101]` | no independent 15-set in `[107]` |
| 108..124 | independent 15-set in `[108]` | no independent 16-set in `[124]` |
| 125..125 | independent 16-set in `[125]` | no independent 17-set in `[125]` |

Thus no value from the older through-100 computation is logically assumed.
