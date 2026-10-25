# Independent asymptotic audit for equations (2)--(5)

Date: 2026-08-11 UTC

## Verdict

**PASS for corrected v2.** Every displayed exponent and sign in equations
(2)--(5) follows from the derivation below. The original v1 rendering of (2)
was false as written because an operator was missing between its `n^2` and
`n log n` terms. V2 inserts the required `+`. No other sign or term changes.

## Middle-rank full-support factor

Let

\[
F_p(m,r)=\sum_{j=0}^m(-1)^j{m\choose j}{m-j\brack r}_p.
\]

This is the exact full-support subspace count in equation (1). A union bound
over the `m` coordinate hyperplanes gives, for `r=floor(m/2)`,

\[
1-\frac{F_p(m,r)}{{m\brack r}_p}
\le m\frac{{m-1\brack r}_p}{{m\brack r}_p}
=m\frac{p^{m-r}-1}{p^m-1}=o(1).
\]

The Gaussian product formula is

\[
{m\brack r}_p
=p^{r(m-r)}
\frac{\prod_{i=m-r+1}^{m}(1-p^{-i})}
     {\prod_{i=1}^{r}(1-p^{-i})}.
\]

When both `r` and `m-r` tend to infinity, the quotient tends to
`1/prod_{i>=1}(1-p^{-i})`. Hence

\[
\log_2 F_p(m,\lfloor m/2\rfloor)
=\log_2(p)\left\lfloor\frac{m^2}{4}\right\rfloor+O_p(1)
=\frac{\log_2p}{4}m^2+O_p(1).
\]

The floor changes the exponent by zero for even `m` and by `-1/4` for odd
`m`, so it is absorbed by `O_p(1)`. The quadratic sign is positive.

## Ambient-product factor

For equation (2), `q=0` and `m=n/p`. Base-2 Stirling gives

\[
\log_2(t!)=t\log_2t-t\log_2e
+\frac12\log_2(2\pi t)+O(1/t).
\]

Therefore

\[
\begin{aligned}
\log_2\frac{n!}{m![p(p-1)]^m}
={}&n\log_2n-m\log_2m-m\log_2[p(p-1)]\\
&-(n-m)\log_2e+\frac12\log_2(n/m)+O_p(1/n)\\
={}&\left(1-\frac1p\right)n\log_2n\\
&-\left[\left(1-\frac1p\right)\log_2e
+\frac1p\log_2(p-1)\right]n+O_p(1).
\end{aligned}
\]

The intermediate `(n/p) log_2 p` from `-m log_2 m` cancels the
`-(n/p) log_2 p` in `-m log_2[p(p-1)]`; no linear `log_2 p` term remains.
The `n log n` coefficient is positive. Both displayed linear corrections are
subtracted. Adding the middle-rank factor yields exactly

\[
\frac{\log_2p}{4p^2}n^2
+\left(1-\frac1p\right)n\log_2n
-\left[\left(1-\frac1p\right)\log_2e
+\frac1p\log_2(p-1)\right]n+O_p(1),
\]

which is corrected equation (2).

For `p=2`, its coefficients become

\[
\frac1{16},\qquad \frac12,\qquad
-\frac12\log_2e,
\]

because `log_2(p-1)=0`. Exponentiating gives equation (3), and
`r=floor(m/2)=floor(n/4)` confirms the stated exact order. Thus all three signs
and every term in (3) are correct.

## Even and odd rank laws

The ambient framework factor is independent of rank, so it cancels from the
rank distribution. For `m=2s` and `r=s+k`,

\[
r(m-r)=s^2-k^2.
\]

Moving `k` away from the middle lowers the exponent by `k^2`; this proves the
negative sign in the weight `p^{-k^2}` in (4).

For `m=2s+1` and `r=s+k`,

\[
r(m-r)=s(s+1)-k(k-1).
\]

This proves the weight `p^{-k(k-1)}` in (5), including both signs inside the
quadratic. It also explains the two equal central modes `k=0,1`.

For each fixed `k`, the full-support probability tends to one, while the
Gaussian product quotient tends to the same positive constant. Uniformly in
rank,

\[
{m\brack r}_p\le
\frac{p^{r(m-r)}}{\prod_{i\ge1}(1-p^{-i})}.
\]

After division by the middle exponent, this is a summable majorant
proportional to `p^{-k^2}` in the even case and `p^{-k(k-1)}` in the odd case.
Dominated convergence supplies exactly the theta normalizers displayed in
(4) and (5). Both limiting laws are tight, so
`R_m=m/2+O_Pr(1)` has the correct center and sign.

## Scope

This audit validates only the elementary asymptotic deductions for the
explicit p-orbit family. It does not turn the restricted order law into a law
for uniformly random subgroups of `S_n`, does not supply a global second-order
upper bound, and does not determine `f(19)`.
