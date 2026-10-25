# Erdős problem #51: can a least inverse totient have unbounded ratio?

## Outcome

Let

\[
M(a):=\min\{n\geq 1:\varphi(n)=a\}
\]

when \(a\) is a totient. I did not obtain an infinite family with
\(M(a)/a\to\infty\). The investigation instead gives a fairly sharp account of
why the most natural constructions fail, an exact conditional construction
principle, and some reproducible finite data.

The central obstruction is this identity:

\[
\frac{M(a)}{a}
 =\frac{M(a)}{\varphi(M(a))}
 =\prod_{p\mid M(a)}\frac{p}{p-1}. \tag{1}
\]

Consequently,

\[
\log \frac{M(a)}a
 =\sum_{p\mid M(a)}\frac1p+O(1), \tag{2}
\]

where the \(O(1)\) is absolute. Thus the desired divergence is equivalent to

\[
\sum_{p\mid M(a)}\frac1p\longrightarrow\infty. \tag{3}
\]

This immediately reverses one tempting intuition in the prompt: forcing all
prime factors of a preimage to lie in a sparse, fast-growing set cannot work
when that set has convergent reciprocal sum. Large primes make \(n\) large,
but they make \(\varphi(n)\) almost equally large. Prime-power exponents do not
enter (1) at all.

At the same time, to prove that a chosen preimage is *minimal*, one must rule
out all ways of replacing several of its prime-power factors by fewer shifted
primes \(q\) with \(q-1\mid a\). This is where nonsparse supports are especially
vulnerable. In short:

- ratio divergence needs many not-too-large prime divisors;
- minimality is easiest to certify when the allowed prime divisors are sparse
  and rigid.

That conflict appears in every construction tested below.

The most useful positive reduction comes from Erdős's 1958 “prime replicator”
theorem. For fixed \(a\), almost every prime \(p\) has

\[
\varphi^{-1}(a(p-1))=p\,\varphi^{-1}(a).
\]

Hence, if one can recursively select such primes \(p_j\) with
\(\sum_j1/p_j=\infty\), then

\[
a_j=a_0\prod_{i\leq j}(p_i-1)
\]

is a solution to problem #51. Erdős's theorem is not uniform in the changing
value \(a_j\), however, and supplies no such divergent path. This isolates a
precise missing ingredient rather than merely saying that “minimality is
hard.”

## 1. Status and distinction from Carmichael's conjecture

The problem is still listed as open as of 25 July 2026. It occurs in Section 9
of Erdős's 1995 paper *Some of my Favourite Problems in Number Theory,
Combinatorics, and Geometry*. Immediately after asking it, Erdős calls
Carmichael's multiplicity-one question a “more significant problem.” They are
indeed different:

- Carmichael asks whether some fiber \(\varphi^{-1}(a)\) has cardinality one.
- Problem #51 asks about the *least element* of a fiber, with no restriction on
  its cardinality.

Erdős proved that if one value has exactly \(k\) preimages, then infinitely many
values do. The mechanism behind that theorem essentially multiplies every
preimage by a new prime. As shown in Section 6 below, this changes the least
preimage ratio only by \(p/(p-1)\), which tends to \(1\). Thus even a
counterexample to Carmichael's conjecture would not by itself give the family
wanted here.

The current discussion page also records a January 2026 attempted proof based
on

\[
a_k=\prod_{i\leq k}(p_i-1),\qquad n_k=\prod_{i\leq k}p_i.
\]

The asserted minimality is false. The exact failure is analyzed in Section 4,
including the case \(k=15\), where \(a_k+1\) is prime and is therefore the
least preimage.

## 2. What a large ratio actually requires

For any \(n\),

\[
\frac n{\varphi(n)}
 =\prod_{p\mid n}\left(1-\frac1p\right)^{-1}.
\]

Moreover,

\[
-\log(1-1/p)=\frac1p+O(1/p^2),
\]

and \(\sum_p1/p^2<\infty\). This proves (2) uniformly over every finite prime
support.

Three consequences are worth making explicit.

### 2.1 Exponents cannot create the blowup

Replacing \(p\) by \(p^e\) changes both \(n\) and \(\varphi(n)\) by the same
factor \(p^{e-1}\). It can affect which other preimages exist, but it contributes
only the single factor \(p/(p-1)\) to the ratio.

### 2.2 A fast-growing allowed support is self-defeating

If all prime divisors of the proposed least preimages lie in a fixed set
\(\mathcal P\) with

\[
\sum_{p\in\mathcal P}\frac1p<\infty,
\]

then (2) gives a uniform bound on \(M(a)/a\). In particular, exponentially or
superexponentially growing prime supports cannot solve the problem.

### 2.3 Fixed smooth structures for \(p-1\) are also too sparse

Fix primes \(q_1,\ldots,q_r\). Consider every possible prime of the form

\[
p=1+q_1^{e_1}\cdots q_r^{e_r},\qquad e_i\geq0.
\]

Even without using primality,

\[
\sum_{e_1,\ldots,e_r\geq0}
 \frac1{1+q_1^{e_1}\cdots q_r^{e_r}}
 \ll \prod_{i=1}^r\left(\sum_{e_i\geq0}q_i^{-e_i}\right)<\infty.
\]

Thus taking all \(p\) for which \(p-1\) is supported on a fixed finite set of
small primes can never produce an unbounded totient ratio.

The same observation disposes of an infinite Fermat-prime strategy. If
\(F_i=2^{2^i}+1\), then \(\sum_i1/F_i<\infty\). For the first consecutive
Fermat primes one can say more:

\[
\begin{aligned}
n_r&=\prod_{i=0}^rF_i=2^{2^{r+1}}-1,\\
\varphi(n_r)&=\prod_{i=0}^r(F_i-1)=2^{2^{r+1}-1},\\
\frac{n_r}{\varphi(n_r)}
 &=2-2^{\,1-2^{r+1}}<2.
\end{aligned}
\]

So even infinitely many Fermat primes would not help with #51.

## 3. Exact structure of an inverse-totient fiber

Suppose

\[
n=\prod_p p^{e_p},\qquad \varphi(n)=a.
\]

Then

\[
a=\prod_{e_p>0}p^{e_p-1}(p-1). \tag{4}
\]

This gives two elementary but decisive restrictions.

### Lemma 1: shifted-divisor restriction

Every prime \(p\mid n\) satisfies

\[
p-1\mid a,
\]

and, more precisely,

\[
\varphi(p^{e_p})=p^{e_p-1}(p-1)\mid a.
\]

Thus the only possible prime divisors of any preimage of \(a\) are

\[
\mathcal Q(a)=\{d+1:d\mid a,\ d+1\text{ is prime}\}. \tag{5}
\]

This finite set is the basis of exact inverse-totient algorithms.

### Lemma 2: block replacement

Write \(n=uv\) with \((u,v)=1\). If there is a \(w<u\) such that

\[
\varphi(w)=\varphi(u),\qquad (w,v)=1,
\]

then \(n\) is not the least preimage of \(\varphi(n)\), since

\[
\varphi(wv)=\varphi(w)\varphi(v)=\varphi(n)
\]

and \(wv<n\).

It is not enough to show that each individual prime-power block looks
efficient. One must rule out replacements of *every collection* of blocks.

A particularly common replacement occurs for a squarefree block
\(u=\prod_{p\in T}p\). Put

\[
D_T=\varphi(u)=\prod_{p\in T}(p-1).
\]

If \(D_T+1=q\) is prime and \(q\) is coprime to the complementary block, then
\(q\) replaces all of \(u\). For \(|T|\geq2\),

\[
q=1+\prod_{p\in T}(p-1)<\prod_{p\in T}p=u.
\]

For example,

\[
\varphi(3\cdot5\cdot7)=48=\varphi(5\cdot13),
\qquad 65<105.
\]

This is the exact defect in the naïve product construction.

There is also an unavoidable parity deletion:

\[
\varphi(2m)=\varphi(m)\quad(m\text{ odd}).
\]

Hence a least preimage is never \(2\bmod4\). This already invalidates any
claimed minimum that is \(2\) times an odd number.

### Global shifted-prime compression

Two useful special cases are:

1. If \(a+1\) is prime, then

   \[
   M(a)=a+1,
   \]

   because every nontrivial preimage is greater than \(a\).

2. If \(a=de\), with \(d+1\) and \(e+1\) distinct primes, then

   \[
   M(a)\leq(d+1)(e+1)
   \]

   and

   \[
   \frac{M(a)}a\leq
   \left(1+\frac1d\right)\left(1+\frac1e\right). \tag{6}
   \]

When \(d,e\) are both large, (6) puts the least ratio extremely close to \(1\).
Smooth, divisor-rich choices of \(a\) create many opportunities for precisely
this kind of compression.

### Exact finite minimization

Equations (4) and (5) give a finite multiplicative knapsack:

- for every \(p=d+1\in\mathcal Q(a)\), the possible “contributions” are
  \((p-1)p^{e-1}\mid a\);
- the corresponding costs are \(p^e\);
- choose at most one exponent for each \(p\);
- require the contributions to multiply to \(a\);
- minimize the product of the costs.

The verifier accompanying this report implements that dynamic program. It is
not a heuristic enumeration over a bounded range: it considers every possible
prime-power component allowed by (4), so its reported minima are exact.

## 4. Failure of \(a_k=\prod_{i\leq k}(p_i-1)\)

Let \(p_i\) be the \(i\)-th prime and define

\[
a_k=\prod_{i=1}^k(p_i-1),\qquad
N_k=\prod_{i=1}^kp_i.
\]

Certainly \(\varphi(N_k)=a_k\), but this says nothing about minimality. Exact
minimization gives:

| \(k\) | \(p_k\) | \(a_k\) | proposed \(N_k/a_k\) | exact \(M(a_k)\) | exact \(M(a_k)/a_k\) |
|---:|---:|---:|---:|---:|---:|
| 3 | 5 | \(8\) | \(3.750000\) | \(15=3\cdot5\) | \(1.875000\) |
| 4 | 7 | \(48\) | \(4.375000\) | \(65=5\cdot13\) | \(1.354167\) |
| 5 | 11 | \(480\) | \(4.812500\) | \(527=17\cdot31\) | \(1.097917\) |
| 6 | 13 | \(5760\) | \(5.213542\) | \(5917=61\cdot97\) | \(1.027257\) |
| 8 | 19 | \(1658880\) | \(5.847132\) | \(1661809=769\cdot2161\) | \(1.001766\) |
| 10 | 29 | \(1021870080\) | \(6.331229\) | \(1021943953=18433\cdot55441\) | \(1.000072\) |
| 12 | 37 | \(1103619686400\) | \(6.723999\) | \(1103621790529=995329\cdot1108801\) | \(1.000001907\) |
| 14 | 43 | \(1854081073152000\) | \(7.056197\) | \(1854081159307777=41803777\cdot44352001\) | \(1.000000046\) |
| 15 | 47 | \(85287729364992000\) | \(7.209593\) | \(85287729364992001\) | \(1+1/a_k\) |

For \(k=15\),

\[
a_k+1=85287729364992001
\]

is prime, so its minimality is immediate, without computation.

The proposed ratios grow because \(N_k\) contains all small primes. Exactly
that rich factorization makes \(a_k\) very smooth and gives it many divisor
splits \(a_k=de\) for which \(d+1,e+1\) are prime. The intended many-prime
preimage is compressed into two primes, and eventually into one.

This phenomenon is not a minor issue about the removable factor \(2\). Even
after omitting \(2\), the replacement

\[
3\cdot7\rightsquigarrow13
\]

inside \(3\cdot5\cdot7\) already produces \(5\cdot13<3\cdot5\cdot7\).

## 5. Can large exponents force the small primes?

Exponents can sometimes certify that one small prime must occur, but the ratio
then stays constant.

For example, put

\[
a_e=2\cdot3^e.
\]

Every odd prime \(q\) in a preimage satisfies

\[
q-1\mid2\cdot3^e,
\]

so \(q=2\cdot3^j+1\) for some \(0\leq j\leq e\). Since
\(v_2(a_e)=1\), a preimage can contain only one odd prime. It follows that the
only two possible mechanisms are:

- \(q=3\), used to exponent \(e+1\), giving \(3^{e+1}\);
- \(q=2\cdot3^e+1\), if this number is prime.

For every \(e=6t+1\) with \(t\geq1\),

\[
2\cdot3^e+1
\]

is a composite multiple of \(7\). Hence

\[
M(2\cdot3^e)=3^{e+1},\qquad
\frac{M(2\cdot3^e)}{2\cdot3^e}=\frac32.
\]

So exponent forcing is real, but one forced prime contributes only one bounded
Euler factor.

Trying to do this for many small primes requires ruling out primes

\[
q=d+1
\]

for a large lattice of smooth divisors \(d\mid a\), as well as primes that
merge several desired contributions at once. Even the much narrower question
whether there is a fixed \(m\), \((m,6)=1\), for which every

\[
2^k3^\ell m+1
\]

is composite is open Erdős problem #203. A proof of minimality for a
many-prime construction generally needs control at least comparable to this,
and usually stronger because all divisors and all subset mergers must be
handled. This does not prove that the exponent route is impossible, but it
pinpoints why it quickly reaches unresolved shifted-prime questions.

## 6. Prime replicators: an exact conditional construction

For a totient \(a\), call a prime \(p\) a *replicator* of \(a\) if

\[
\varphi^{-1}(a(p-1))
 =\{pn:n\in\varphi^{-1}(a)\}. \tag{7}
\]

Erdős proved in 1958 that, for each fixed \(a\geq2\), all but
\(o(x/\log x)\) primes \(p\leq x\) are replicators of \(a\). In particular,
there are infinitely many at every fixed stage.

If \(p\) replicates \(a\), then (7) gives

\[
M(a(p-1))=pM(a)
\]

and therefore

\[
\frac{M(a(p-1))}{a(p-1)}
 =\frac{M(a)}a\frac p{p-1}. \tag{8}
\]

This yields a clean conditional answer to #51.

### Conditional construction criterion

Start with any totient \(a_0\). Suppose distinct primes \(p_1,p_2,\ldots\)
can be chosen so that \(p_j\) replicates

\[
a_{j-1}=a_0\prod_{i<j}(p_i-1)
\]

and

\[
\sum_{j=1}^{\infty}\frac1{p_j}=\infty. \tag{9}
\]

Then, setting

\[
a_j=a_0\prod_{i\leq j}(p_i-1),
\]

repeated use of (8) gives

\[
\frac{M(a_j)}{a_j}
 =\frac{M(a_0)}{a_0}
  \prod_{i\leq j}\frac{p_i}{p_i-1}\longrightarrow\infty.
\]

Thus (9) would construct the required set \(A=\{a_j:j\geq1\}\).

### Why Erdős's theorem alone does not give (9)

The theorem has the quantifier pattern

\[
\text{for every fixed }a,\quad
\text{almost every prime }p\text{ replicates }a.
\]

After a prime is selected, however, \(a\) changes. The threshold after which
the exceptional set is small may depend arbitrarily badly on the new \(a\).
There is no uniform bound ensuring that the next replicator is small enough
for its reciprocal to contribute to a divergent series.

Abstractly, a tree can have density-one children at every node while requiring
all children to exceed a node-dependent, superexponential threshold. Every
infinite path in such a tree has convergent reciprocal sum. This is precisely
the logical gap here.

What is needed is a uniform or iterative form of the replicator theorem strong
enough to produce a divergent-harmonic path. The fixed-\(a\) theorem does not
currently provide it.

This also explains the Carmichael result. Replication preserves the number of
preimages, but by (8) it preserves the least-preimage ratio up to a factor
tending to \(1\). Multiplicity propagation and ratio blowup are genuinely
different tasks.

## 7. Exact finite experiments

All computations here are reproducible with
[`erdos51_totient_preimage_gap_verify.py`](erdos51_totient_preimage_gap_verify.py).

### 7.1 Record least-preimage ratios through \(n=50{,}000{,}000\)

A totient sieve was run through \(n=50{,}000{,}000\). Scanning \(n\) in
increasing order makes every first occurrence of a totient value a globally
least preimage: no larger, unscanned integer can invalidate that fact.

Apart from \(M(1)=1\), the successive ratio records are:

| least preimage \(n\) | \(a=\varphi(n)\) | factorization of \(n\) | \(n/a\) |
|---:|---:|---|---:|
| \(3\) | \(2\) | \(3\) | \(1.500000000000\) |
| \(15\) | \(8\) | \(3\cdot5\) | \(1.875000000000\) |
| \(255\) | \(128\) | \(3\cdot5\cdot17\) | \(1.992187500000\) |
| \(11985\) | \(5888\) | \(3\cdot5\cdot17\cdot47\) | \(2.035495923913\) |
| \(4158795\) | \(2037248\) | \(3\cdot5\cdot17\cdot47\cdot347\) | \(2.041378860109\) |

The scan is evidence only, not an asymptotic argument. Its useful feature is
structural: the records begin with Fermat primes and then append primes

\[
47=2\cdot23+1,\qquad347=2\cdot173+1
\]

whose \(p-1\) has a new large prime marker.

### 7.2 An exact finite forced-marker chain

The divisor-knapsack computation extends this pattern far beyond the dense
scan. For the successive supports

\[
\{3,5\},\ \{3,5,17\},\ldots,
\{3,5,17,47,347,1187,1367,5387\},
\]

the squarefree product \(n\) is exactly \(M(\varphi(n))\):

| last appended prime | exact least preimage \(n\) | \(\varphi(n)\) | \(n/\varphi(n)\) |
|---:|---:|---:|---:|
| \(5\) | \(15\) | \(8\) | \(1.875000000000\) |
| \(17\) | \(255\) | \(128\) | \(1.992187500000\) |
| \(47\) | \(11985\) | \(5888\) | \(2.035495923913\) |
| \(347\) | \(4158795\) | \(2037248\) | \(2.041378860109\) |
| \(1187\) | \(4936489665\) | \(2416176128\) | \(2.043100090177\) |
| \(1367\) | \(6748181372055\) | \(3300496590848\) | \(2.044595771063\) |
| \(5387\) | \(36352453051260285\) | \(17776474638307328\) | \(2.044975384091\) |

At the last stage,

\[
\begin{aligned}
n&=3\cdot5\cdot17\cdot47\cdot347\cdot1187\cdot1367\cdot5387,\\
\varphi(n)
 &=2^{12}\cdot23\cdot173\cdot593\cdot683\cdot2693.
\end{aligned}
\]

Every prime after \(17\) is a safe prime:

\[
\begin{aligned}
47&=2\cdot23+1,&347&=2\cdot173+1,\\
1187&=2\cdot593+1,&1367&=2\cdot683+1,\\
5387&=2\cdot2693+1.
\end{aligned}
\]

The new large factor of \(p-1\) makes \(p\) the cheapest individual carrier
of that factor. The exact inverse computation additionally checks that no
collection of carriers can be merged more cheaply.

This is a genuine finite near-construction, but its apparent strength is also
its fatal asymptotic weakness. Brun's upper-bound sieve gives

\[
\#\{p\leq x:p\text{ and }(p-1)/2\text{ prime}\}
\ll\frac{x}{(\log x)^2}.
\]

Partial summation, or a dyadic decomposition, then gives

\[
\sum_{\substack{p\ \mathrm{safe}\\p\geq3}}\frac1p<\infty. \tag{10}
\]

Therefore an infinite construction obtained only by appending safe primes
would still have bounded

\[
\prod_p\frac p{p-1}.
\]

The marker structure that makes finite minimality plausible makes the support
too thin for (3).

## 8. Why a proof of minimality is the real burden

For a proposed

\[
n=\prod_{p\in S}p^{e_p},\qquad a=\varphi(n),
\]

checking \(\varphi(n)=a\) is the easy half. A valid construction must also
exclude:

1. deletion of a redundant factor \(2\);
2. a prime \(a+1\);
3. two-prime factorizations \((d+1)(a/d+1)\);
4. replacement of any subset of the intended prime-power blocks;
5. primes \(q=d+1\) carrying high powers of several desired small primes at
   once;
6. competing factorizations using powers \(q^f\).

These are not isolated accidents. They are all manifestations of the exact
factorization equation

\[
a=\prod_q q^{f_q-1}(q-1). \tag{11}
\]

The naïve product construction specifies one factorization of (11), while
minimality asks that every other factorization have at least as large a
product of prime-power costs.

An obvious way to try to rule out mergers is to assign superincreasing large
marker primes to the factors \(p-1\). Whenever that strategy gives the desired
rigidity, however, the \(p\)'s themselves are forced to grow so rapidly that
their reciprocal sum converges. Conversely, using enough small primes to make
(3) diverge creates a dense divisor lattice in \(a\), hence many
shifted-divisor and subset-merger candidates.

This is the precise sense in which the natural requirements pull in opposite
directions.

## 9. What would turn this into a genuine construction?

The cleanest remaining target is the replicator criterion of Section 6. Any
one of the following would be sufficient:

- a uniform version of Erdős's prime-replicator theorem that permits a
  recursively chosen chain with divergent reciprocal sum;
- an explicit nonsparse class of primes for which simultaneous replication
  can be proved;
- a direct family \(a_k\) together with a structural theorem showing that
  every factorization (11) contains a prescribed prime support \(S_k\) with
  \(\sum_{p\in S_k}1/p\to\infty\).

By contrast, the following cannot suffice:

- merely making the witnessing \(n_k\) enormous with large exponents;
- restricting its primes to a fixed smooth or fast-growing class;
- showing only that each individual intended prime factor is locally cheapest;
- invoking a fixed multiplicity, including multiplicity one, without control
  of the prime support of the least preimage.

## 10. Bottom line

No explicit infinite set \(A\) was constructed. The strongest useful negative
finding is that the proposed rigidity mechanism and the required ratio growth
are antagonistic:

\[
\boxed{\quad
\frac{M(a)}a\to\infty
\iff
\sum_{p\mid M(a)}\frac1p\to\infty,
\quad}
\]

whereas the standard ways of forcing a prime factor—Fermat structure, fixed
smooth \(p-1\), safe-prime markers, or superincreasing markers—produce prime
sets with convergent reciprocal sum.

The prime-replicator theorem gives a precise conditional construction and
shows exactly what additional uniformity is missing. The finite safe-marker
chain demonstrates that nontrivial minimality certificates do exist and
reaches \(2.044975\ldots\), but continuation using only the same safe-prime
marker mechanism can never diverge: those rigid primes are too sparse.

This supports the current heuristic that the ratios of least preimages may in
fact be bounded, while also showing why proving such a bound would require a
strong theorem about replacing collections of small prime divisors without
changing a totient value.

## References

1. P. Erdős, [*Some of my Favourite Problems in Number Theory,
   Combinatorics, and Geometry*](https://doi.org/10.11606/resimeusp.v2i2.74798),
   Resenhas 2 (1995), 165–186; problem #51 appears in Section 9.
2. P. Erdős,
   [*Some of my new and almost new problems and results in combinatorial
   number theory*](https://doi.org/10.1515/9783110809794.169), in *Number
   Theory* (Eger, 1996), de Gruyter, 1998, 169–180.
3. T. F. Bloom, [Erdős problem #51](https://www.erdosproblems.com/51) and its
   [discussion thread](https://www.erdosproblems.com/forum/thread/51).
4. P. Erdős, [*Some remark on Euler's \(\varphi\)
   function*](https://eudml.org/doc/206104), Acta Arith. 4 (1958), 10–19;
   the replication result is proved on pp. 15–18.
5. K. B. Stolarsky and S. Greenbaum,
   [*A Ratio Associated with \(\varphi(x)=n\)*](https://www.fq.math.ca/Scanned/23-3/stolarsky.pdf),
   Fibonacci Quarterly 23 (1985), 265–269; this states Erdős's result in
   “prime replicator” language.
6. M. A. Alekseyev,
   [*Computing the inverses, their power sums, and extrema for Euler's totient
   and other multiplicative functions*](https://arxiv.org/abs/1401.6054),
   Journal of Integer Sequences 19 (2016), Article 16.5.2.
7. T. F. Bloom, [Erdős problem #203](https://www.erdosproblems.com/203), the
   shifted-smooth-prime obstruction mentioned in Section 5.
8. R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., Springer, 2004,
   problems B36 and B39.
