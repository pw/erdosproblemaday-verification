# Hostile audit report: Erdos Problem 1117

Audit date: 2026-08-11 UTC

## Verdict

**PASS, but only as a literature update to the already-solved limsup half and
as an elementary exact polynomial subtheorem.**

The author bundle does not solve the open liminf half. It makes no novelty
claim for the polynomial observation. Those two qualifications are essential.

## Immutable input

The audited author bundle is
`/home/exedev/erdos_scratch/fresh12_erdos1117_maxmod_points_20260811`.
Its `MANIFEST.sha256` has SHA-256
`4332c124aa51e217254c7071fb346bf666f6bc610fa95dcb72d8d0c69a06ff73`.
I independently verified every manifest entry and reran `run_all.sh`; all
checks passed.

The most load-bearing source identities are:

```text
b3b7aa196918b4b78f12c3f5834469419d1bb7252224f6b8475b463d01c2f058  arxiv_2607.09462v1_source.tar
2f0349b3c0764cc420e5d1b76ff3b633c8a39c6b04b8fbfe50e5542773b110d6  arxiv_2607.09462v1.pdf
98a018ca2211c7cb27e8e08314640b7ff1c1750c78f952923f6dd1a52f605876  arxiv_2208.11154v2_source.tar
ce1318d32eb78d3f98f1b3883de7e8293f7ebfff003e91fe6977de962ec0d610  live_1117_20260811.json
362fc1f745e3795e734f5f15bbee46f449551fa9d7d1a7a1527cb221fe69e0d2  site_index_20260811.js
9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052  site_ledger_data_20260811.js
```

## Gate audit

The frozen site files contain neither an article-schema occurrence of Problem
1117 nor any of the defining phrases `maximum modulus point`,
`maximum-modulus point`, `maximum modulus set`, `maximum-modulus set`, or
`maximum curve`. I also repeated the same exact and semantic scans against the
current checkout at commit `7cf9bd43c89f1d9e144535ce447264b8d28cd95a`; they remained clear.

The broad adjacencies are not semantic collisions:

- #513 uses the scalar maximum modulus in a Taylor-term ratio; it does not count
  angular maximizers on a circle.
- #517 is a value-distribution question for lacunary entire functions.
- #1040 concerns areas of polynomial lemniscates and logarithmic capacity.
- #278 contains the English phrase "maximum modulus" only in the unrelated
  arithmetic sense of a largest congruence modulus.

At 2026-08-11 19:01 UTC I independently reopened the live page through Bright
Data. It still displayed `OPEN`, `0 claimed proofs for this problem`,
`Currently working on this problem: None`, and
`Interested in collaborating: None`. The frozen five-page capture additionally
records an empty proof-claim page. Thus the live and site gates pass.

Official arXiv metadata independently reopened on 2026-08-11 still lists only
v1 of arXiv:2607.09462, submitted 10 July 2026. Targeted current arXiv searches
found that paper and the 2024 approximate paper, but no later paper claiming the
liminf conclusion. This last sentence is a search report, not a bibliographic
completeness theorem.

## Primary theorem quantifiers

The TeX source of arXiv:2607.09462v1 defines

```text
v_f(r) = #(M(f) intersect {z : |z|=r})
```

for a non-monomial entire function and states in Theorem 1.1:

```text
There is an entire function f in class B, of finite order, such that
limsup_(r->infinity) v_f(r)=infinity.
```

The quantifier is one function, not a sequence of functions. Class B is defined
in the same source as a class of transcendental entire functions, so the
non-monomial requirement is automatic. At the end of the proof the paper gives
the explicit selected-radius assertion

```text
v_f(exp(x_n)) >= 2n+1 for every n, with x_n -> +infinity.
```

This proves an unbounded limsup. It does not imply a divergent liminf. The paper
itself says both that the second part remains open and that the construction
gives no useful control away from the prescribed radii.

Theorem 1.2 does not bridge that gap: its prescribed points have pairwise
distinct moduli, so it guarantees one selected point on each of many different
circles, not many equal maximizers on each sufficiently large circle.

The 2024 theorem is also correctly scoped. For every epsilon it gives many
components of an epsilon-near-maximum set on every sufficiently large circle.
Its source explicitly says those components might contain only a uniformly
bounded number of actual maximum points and that the authors are unable to
conclude the liminf statement.

## Independent polynomial proof

Let `m,d` be nonnegative integers with `m<d`, and let

```text
p(z) = sum_(j=m)^d a_j z^j,    a_m a_d != 0.
```

For every `r>0`, put `H(theta)=|p(r exp(i theta))|^2` and `s=d-m`.
Then

```text
H(theta) = sum_(j,k) a_j conjugate(a_k) r^(j+k)
                         exp(i(j-k)theta).
```

The frequency `s` can arise only from `(j,k)=(d,m)`, so its coefficient is
`a_d conjugate(a_m) r^(d+m)`, which is nonzero. Therefore `H` is a
nonconstant real trigonometric polynomial of exact degree `s`. Its derivative
is also a nonzero trigonometric polynomial of exact degree `s`. Multiplication
by `exp(i s theta)` turns `H'` into a nonzero ordinary polynomial in
`exp(i theta)` of degree at most `2s`; hence `H'` has at most `2s` distinct
zeros modulo `2 pi`.

Let `q` be the number of global maxima of `H`. Every maximum is critical, so
the preceding finite zero bound first establishes that `q` is finite. List the
maxima cyclically. On every open arc between consecutive maxima there is no
global maximum. The minimum on the corresponding closed arc is therefore
strictly below its endpoint values, lies in the open arc, and is critical.
The open arcs are disjoint, so these give `q` new critical points distinct from
the `q` maxima. Thus `H'` has at least `2q` distinct zeros.

The case `q=1` needs an explicit circle argument and is valid. Choose a lift
`theta_0` of the unique maximum and view the periodic function on
`[theta_0,theta_0+2 pi]`. Its two endpoints represent the same maximum point.
Every interior point represents a different point of the circle and has
strictly smaller value. Hence the minimum of this closed interval is attained
in its interior, is a zero of `H'`, and is distinct modulo `2 pi` from the
maximum zero. This supplies exactly the two critical points required by the
general `2q` count.

Consequently `2q<=2s` and

```text
v_p(r)=q<=s=d-m.
```

For `p(z)=A z^m+B z^d` with `AB!=0`, factoring the common phase gives

```text
|p(r exp(i theta))| = |A r^m+B r^d exp(i s theta)|.
```

Equality in the triangle inequality occurs exactly when
`B exp(i s theta)` has the argument of `A`. That equation fixes
`exp(i s theta)` and has exactly `s` solutions modulo `2 pi`, for every
positive radius and all nonzero complex `A,B`. Thus the bound is sharp.

No regularity, genericity, or real-coefficient assumption is hidden in this
argument. The wording should retain the implicit polynomial convention
`m,d in Z_{>=0}`; making it explicit avoids a purely notational ambiguity.

## Publication-safe scope

Safe conclusion:

> Problem 1117 remains open in its liminf form. Pardo-Simon and Sixsmith's
> July 2026 arXiv v1 preprint strengthens the already-known limsup existence
> result by producing a finite-order class-B example. Separately, a
> non-monomial polynomial with support span `d-m` has at most `d-m`
> maximum-modulus points on every positive circle, with equality for
> binomials.

Do not say that Problem 1117 is solved, that the 2026 count tends to infinity
on all large circles, that the polynomial theorem advances the transcendental
liminf question, that the elementary theorem is new, or that arXiv v1 is peer
reviewed.

## Final disposition

No mathematical gap was found in the narrowly stated claims. The gate,
primary-source quantifiers, support-span proof, complex-coefficient sharpness,
and limsup/liminf distinction all survive hostile audit. **PASS.**

