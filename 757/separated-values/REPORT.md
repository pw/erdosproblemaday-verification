# Erdős #757 — four additional exact finite values

The sharpened finite lower bound in the wave-7k report is

\[
f(n)\ge n-\left\lfloor\frac{8n-6}{17}\right\rfloor,
\]

rigorous modulo the named Gyárfás--Lehel and Henning--Yeo theorems. Combining
it with explicit scale-separated unions gives

\[
\boxed{f(17)=10,\qquad f(24)=14,\qquad f(26)=15,\qquad f(28)=16.}
\]

These values do not require resolving \(f(16)\).

## Elementary separated-union lemma

Let \(X,Y\subseteq\mathbb R\) be finite \((4,5)\)-sets with minima zero. Put
\(D_X=\max X\), \(D_Y=\max Y\), and let \(\delta_Y\) be the least positive
gap between elements of \(Y\). Choose

\[
q\delta_Y>D_X,\qquad t>D_X+qD_Y,
\]

and set \(C=X\cup(t+qY)\).

Because \(qD_Y\ge q\delta_Y>D_X\), the three kinds of sums lie in

\[
[0,2D_X],\qquad [t,t+D_X+qD_Y],\qquad
[2t,2t+2qD_Y],
\]

respectively, and these intervals are disjoint. Mixed sums are unique because

\[
x+qy=x'+qy'\implies q(y-y')=x'-x,
\]

whose two sides have incompatible nonzero magnitudes. Thus \(C\) is weak
Sidon. A mixed AP would equate a mixed pair sum to a diagonal sum in one of
the two pure-sum intervals, also impossible. Hence the AP hypergraph of \(C\)
is the disjoint union of those of the two blocks, and is linear; equivalently,
\(C\) is a \((4,5)\)-set.

For the Sidon number, any Sidon subset of \(C\) restricts to Sidon subsets in
the two blocks, so \(h(C)\le h(X)+h(Y)\). The union of maximum component
Sidon sets is Sidon by the same sum separation, proving equality.

The verifier does not rely solely on this proof: it tests the live
\(|B-B|\ge11\) predicate on every quadruple, all distinct-element pair sums,
the complete AP list, and an explicit union Sidon witness.

## Explicit constructions

Use scale \(q=1000\) and \(t=D_X+1000D_Y+1\). From the already verified
\(A_3,A_{12},A_{14}\), concatenate as follows:

| \(n\) | blocks | \(t\) | component \(h\) | construction \(h\) | finite lower bound |
|---:|---|---:|---:|---:|---:|
| 17 | \(A_{14}+A_3\) | 195057 | \(8+2\) | 10 | 10 |
| 24 | \(A_{12}+A_{12}\) | 720721 | \(7+7\) | 14 | 14 |
| 26 | \(A_{14}+A_{12}\) | 721057 | \(8+7\) | 15 | 15 |
| 28 | \(A_{14}+A_{14}\) | 1057057 | \(8+8\) | 16 | 16 |

The resulting coordinates are:

```text
n=17, A14+A3, t=195057:
{0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
 195057,292057,389057}

n=24, A12+A12, t=720721:
{0,97,161,194,227,322,374,454,521,534,547,720,
 720721,817721,881721,914721,947721,1042721,1094721,1174721,
 1241721,1254721,1267721,1440721}

n=26, A14+A12, t=721057:
{0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
 721057,818057,882057,915057,948057,1043057,1095057,1175057,
 1242057,1255057,1268057,1441057}

n=28, A14+A14, t=1057057:
{0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
 1057057,1193057,1257057,1300057,1303057,1306057,1329057,
 1343057,1355057,1380057,1457057,1585057,1653057,2113057}
```

The exact live-predicate histograms are:

| \(n\) | quadruples | \(|B-B|=11\) | \(|B-B|=13\) |
|---:|---:|---:|---:|
| 17 | 2380 | 182 | 2198 |
| 24 | 10626 | 420 | 10206 |
| 26 | 14950 | 506 | 14444 |
| 28 | 20475 | 600 | 19875 |

For completeness, the named-theorem lower-bound arithmetic is:

| \(n\) | \(m\le n-2\) | \(5n+3m\le8n-6\) | \(\tau\le\lfloor(8n-6)/17\rfloor\) | \(h=n-\tau\ge\) |
|---:|---:|---:|---:|---:|
| 17 | 15 | 130 | 7 | 10 |
| 24 | 22 | 186 | 10 | 14 |
| 26 | 24 | 202 | 11 | 15 |
| 28 | 26 | 218 | 12 | 16 |

Reproduce with:

```bash
python3 -I verify_concatenated_exact_values.py
```

The seven live comments, current Ma--Tang v2 TeX, companion checker, and
targeted exact-value/coordinate web searches did not mention these four
finite equalities. That is only a targeted search miss, not a proof of
novelty or a priority claim. These values are straightforward consequences
of the named published ingredients plus the explicit blocks.

This is an exact finite corollary. It does not improve the asymptotic interval
\(9/17\le c_*\le4/7\).
