# Lower-bound provenance for `c_11 >= 2`

The integrated candidate cites the private-prime padding theorem published
with the earlier `c_5` result.  The public finite verifier currently exercises
that construction only through `n=10`; a finite `n=11` instance is useful
corroboration but cannot by itself prove a limiting lower bound of two.  This
note records the uniform prime-selection step explicitly.

Fix `r >= 0`, put `n=4+r`, and fix `c<2`.  Choose `eta>0` so small that

```text
2/(1+5 eta) > c.
```

For sufficiently large `X`, the prime number theorem supplies primes

```text
u in (X,(1+eta)X),
v in ((1+2eta)X,(1+3eta)X),
w in ((1+4eta)X,(1+5eta)X).
```

It also supplies at least `r` primes in the fixed positive-relative-width
interval

```text
((1+eta)(1+3eta)X^2+r, (1+2eta)(1+4eta)X^2).
```

Call them `q_1,...,q_r`.  The displayed bounds imply

```text
uv+r < q_j < vw,   u>r,   and   2u/w>c
```

once `X` is large.  Thus this supplies the prime data for every fixed `r` and
arbitrarily close ratios; finite examples are not being used to infer the
limit.

Use the Chinese remainder theorem to choose `t` satisfying

```text
t = 1                         (mod uw),
tuw = v+1                     (mod v^2),
tuvw = j                      (mod q_j),  1<=j<=r,
```

and put `x=tuvw`.  In the open interval

```text
I=(x-uv,x+uv)
```

the point `x` is the unique multiple of each of `uv,uw,vw`; `x-v` is the
unique multiple of `v^2` and has exact `v`-valuation two; and `x-j` is the
unique `q_j`-multiple.  The inequality `q_j>uv+r` proves the last uniqueness.
Because `j<=r<u<v<w`, each `x-j` is coprime to `u`, `v`, and `w`.  Distinct
`q_j` have distinct unique multiples.

Take

```text
A={uv,v^2,uw,vw,q_1,...,q_r},  M=vw.
```

Every point of `I` other than `x` is divisible by at most one of `u,v,w`.
If a cover omits `x`, the target `u^2 v^4 w^2` needs at least one `u` point,
one `w` point, and three `v` points, since only `x-v` can contribute two
copies of `v`.  If it uses `x`, the residual `u v^3 w` needs at least four
further single-colour points.  The four-label core therefore always needs
five points.  Each private prime additionally forces its distinct neutral
point `x-j`, so the full product needs at least `5+r=n+1` points.

The bad interval has length `2uv` and

```text
length(I)/M = 2u/w > c.
```

Any subinterval of length `cM` is also bad.  Since `c<2` was arbitrary, this
proves `c_n>=2` for every fixed `n>=4`, in particular `c_11>=2`.

The independent checker in this audit additionally reconstructs the explicit
`r=7`, `(u,v,w)=(101,103,107)` instance without importing the public script.
Its exact capped-valuation DP finds minimum cover size 12 for eleven labels.

