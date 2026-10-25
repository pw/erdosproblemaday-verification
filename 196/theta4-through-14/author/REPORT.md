# Erdos problem 196: exact finite 4-AP-avoider counts through n=14

Access and computation date: 2026-08-11 UTC.

## Claim labels

- **(a) elementary-rigorous:** a complete proof is given here.
- **(b) rigorous-modulo-source:** a statement is attributed to an inspected primary source.
- **(c) search-limited:** a negative literature or sequence search, not a novelty theorem.
- **(d) computational-only:** an exact finite computation within the stated software trust boundary.

The infinite problem remains open. The result of this run is an exact finite enumeration, not a
solution or asymptotic advance.

## 0. Mandatory gates

### Live page

The rendered live page <https://www.erdosproblems.com/196> was opened through the Bright Data
browser path. It displayed:

- status: **OPEN**;
- **0 claimed proofs for this problem**;
- **Currently working on this problem: None**;
- **Interested in collaborating: Adenwalla**;
- three comments;
- formalised statement: yes.

The current statement is:

> Must every permutation of the positive integers contain a monotone four-term arithmetic
> progression? Equivalently, must some four values in arithmetic progression occur in increasing
> or decreasing order of position?

Thus the requested live stop condition did not fire.

### Local-source collision audit

I parsed problem numbers only from structured `n:`, `problem:`, and Erdos-problem URL fields. The
current files contained 72 and 532 distinct numeric references, respectively, but neither contained
196. In both files, each of the following framework phrases had zero case-insensitive occurrences:

`monotone arithmetic progression`, `monotone 4-term`, `monotone 3-term`, `monotone ap`,
`permutation avoiding`, `permutations avoiding`, `4-ap-free permutation`, `3-ap-free permutation`,
and `HasMonotoneAP`.

The audited source identities were:

| file | SHA-256 |
|---|---|
| `ErdosProblemADay/src/index.js` | `b7111451218492db6756cc88dde0a8b98700d4c6f47e476171a02950b6d9af8b` |
| `ErdosProblemADay/src/ledger_data.js` | `9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052` |

No site source was edited.

## 1. Primary-source audit

1. **(b)** J. A. Davis, R. C. Entringer, R. L. Graham, and G. J. Simmons,
   ["On permutations containing no long arithmetic progressions"](https://doi.org/10.4064/aa-34-1-81-90),
   *Acta Arithmetica* 34 (1977), 81-90. The paper defines and studies the exact finite count only
   for permutations avoiding monotone **three**-term progressions. It constructs a doubly infinite
   ordering of the positive integers avoiding monotone four-term progressions and explicitly leaves
   the singly infinite problem open.

2. **(b)** Timothy D. LeSaulnier and Sujith Vijay,
   ["On Permutations Avoiding Short Progressions"](https://arxiv.org/abs/1004.1740), published in
   *Discrete Mathematics* 311 (2011), 205-207. They construct a permutation of the positive
   integers with no monotone four-term progression of odd common difference and derive density
   bounds. They do not give the exact finite table below.

3. **(b)** Jesse Geneson,
   ["Forbidden arithmetic progressions in permutations of subsets of the integers"](https://arxiv.org/abs/1803.06334),
   *Discrete Mathematics* 342 (2019), 1489-1491. Section 4 defines
   \(\theta_k(n)\), the number of permutations of \([n]\) avoiding monotone \(k\)-term arithmetic
   progressions, and proves recursive lower bounds. It does not tabulate exact \(\theta_4(n)\).

4. **(b)** Sarosh Adenwalla,
   ["Avoiding Monotone Arithmetic Progressions in Permutations of Integers"](https://arxiv.org/abs/2211.04451),
   *Discrete Mathematics* 347 (2024), paper 114183. The paper improves density constructions and,
   for every fixed \(t\), avoids all four-term progressions whose common difference is not divisible
   by \(2^t\). It still leaves the unrestricted positive-integer problem open and does not supply
   this exact finite enumeration.

5. **(b)** Collier Gaiser and Paul Horn,
   ["Subsequence Sums in Permutations"](https://arxiv.org/abs/2605.29011), submitted 27 May 2026.
   Its introduction explicitly says that, despite the 2011, 2019, and 2024 work, it is still unknown
   whether the positive integers have a permutation without a monotone four-term AP.

The exact downloaded PDFs inspected in this run had SHA-256 hashes:

| source | SHA-256 |
|---|---|
| Davis-Entringer-Graham-Simmons 1977 | `70314d0c59395825c2e13eb2d34449d876f112e8b63c05e97584ecb081621c3e` |
| LeSaulnier-Vijay arXiv | `46662dfb1b596a8568617a8ced810d440691c1c705c17e3c77fc48add3499c6e` |
| Geneson arXiv | `09045fdb29aaa20c8f7932db6b85febeb66794e4f2961870ea9b8f147cb51be6` |
| Adenwalla arXiv v7 | `b07b8924676b28b180f4f738d6a122219aa227f33481274dfcce2deed2b88ebb` |
| Gaiser-Horn arXiv | `363eb2c2f7e9b901322e4a682c9cda2246af7d738f9270ea99efb1edf1147f0a` |

**(c)** Exact-prefix, exact-tail, `theta_4(n)`, and quoted-definition searches found no published
table matching the values below. Web searches of OEIS-indexed pages likewise returned no match; the
direct OEIS search endpoint was blocked by its robots policy in this environment. This is a search
miss, not a claim of publication priority or definitive absence from OEIS.

## 2. Exact finite frontier

Let \(\theta_4(n)\) be the number of permutations \(p\) of \([n]\) for which no four values
\(a,a+d,a+2d,a+3d\) occur in increasing or decreasing positional order.

**(d)** The exact values computed in this run are:

| n | 4-AP subsets in [n] | theta_4(n) | theta_4(n) / n! |
|---:|---:|---:|---:|
| 1 | 0 | 1 | 1 |
| 2 | 0 | 2 | 1 |
| 3 | 0 | 6 | 1 |
| 4 | 1 | 22 | 0.916666666667 |
| 5 | 2 | 102 | 0.85 |
| 6 | 3 | 564 | 0.783333333333 |
| 7 | 5 | 3,336 | 0.661904761905 |
| 8 | 7 | 22,266 | 0.552232142857 |
| 9 | 9 | 168,864 | 0.465343915344 |
| 10 | 12 | 1,307,470 | 0.360303681658 |
| 11 | 15 | 11,066,766 | 0.277245821308 |
| 12 | 18 | 101,361,722 | 0.211610403807 |
| 13 | 22 | 949,812,334 | 0.152530779085 |
| 14 | 26 | 9,471,574,188 | 0.108646017921 |

The first five values also have immediate hand checks. For \(n\leq3\), every permutation avoids.
For \(n=4\), only the identity and reverse order fail, giving 22. For \(n=5\), each of the two
four-term APs is monotone in ten permutations; their bad sets intersect in exactly the identity and
reverse order, giving \(120-10-10+2=102\).

## 3. Why the optimized enumeration is exact

### Endpoint recursion

**(a)** Build a permutation from left to right, and suppose a value \(x\) is appended. Any newly
created forbidden progression must end at this new position. Since its values are monotone, \(x\)
must be either its largest or smallest value.

- If \(x\) is largest, rejection is necessary and sufficient when, for some \(d\geq1\), the already
  placed values \(x-3d,x-2d,x-d\) occur in that positional order.
- If \(x\) is smallest, rejection is necessary and sufficient when, for some \(d\geq1\), the already
  placed values \(x+3d,x+2d,x+d\) occur in that positional order.

All forbidden progressions not using \(x\) were excluded earlier. Induction on the prefix length
therefore proves that the recursion visits every avoiding permutation exactly once and no forbidden
permutation.

### Complement orbits

**(a)** Value complementation \(x\mapsto n+1-x\) is a fixed-point-free involution on ordered
two-distinct-value prefixes and preserves the avoidance property. The optimized program computes
one lexicographically canonical prefix from every complementary pair and doubles its subtree count.
This is an exact bijection, not a heuristic symmetry reduction.

### Incidence identity

Let
\[
 q=\left\lfloor\frac{n-1}{3}\right\rfloor,
 \qquad
 A_4(n)=\sum_{d=1}^{q}(n-3d)
       =qn-\frac{3q(q+1)}2.
\]

**(a)** A fixed four-element AP has 24 relative orders, exactly two of which are monotone. Hence a
uniform random permutation has expected monotone-AP count \(A_4(n)/12\), and the total number of
AP-permutation incidences is
\[
 n!\,A_4(n)/12.
\]
The independent verifier recomputes this total while enumerating all permutations through \(n=9\).

## 4. Reproduction and trust boundary

Files:

- `code/count_avoiders.cpp`: endpoint recursion plus a direct `next_permutation` implementation;
- `code/independent_verify.py`: separate Python exhaustive enumeration and incidence check.

Build and run:

```bash
./reproduce.sh
```

The C++ run used `g++ (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0`. It directly enumerated all
permutations by a structurally different checker through \(n=10\), agreeing term by term with the
endpoint recursion. In the frozen reference run, the \(n=14\) recursion took 153.529 seconds and
the full C++ process took 166.09 seconds. It exited with status zero after reporting no cross-check
mismatch. The Python implementation independently agreed through \(n=9\), also with exit status
zero and no assertion failure. Exact outputs are under `logs/`.

Artifact hashes:

| artifact | SHA-256 |
|---|---|
| `code/count_avoiders.cpp` | `7ee1a073ad2869beb5d2dd8cd2df07ce4ea009132b57228994e4d92c0e6796c8` |
| `code/independent_verify.py` | `8ffdcddde29f76733fa29d3e1b86cfd1e33caba1fb38fd5cf16e5ce177c5d08f` |
| reference binary on this VM | `7d646c337b6b7f72fb684561d8b1da69600c3ebbc1400a52aae23c826ab29a6a` |

The claims through \(n=14\) are **(d)** because exhaustive software enumeration remains part of the
trust boundary. The recursion and symmetry reductions themselves are **(a)**.

## 5. Exact GAP to problem 196

The finite table does not decide the infinite problem.

**(b)** Davis-Entringer-Graham-Simmons already construct a doubly infinite ordering of the positive
integers avoiding monotone four-term APs. Restricting that order to \([n]\) proves
\(\theta_4(n)>0\) for every \(n\), without any computation. Thus nonzero finite counts, even for
arbitrarily large \(n\), cannot be promoted to a solution.

**(a)** A compactness limit of compatible finite orders produces an AP-avoiding total order on the
positive integers, but it need not have order type \(\omega\). It may have elements with infinitely
many predecessors, as a two-sided order does. Problem 196 specifically needs a singly infinite
permutation, which is equivalent to controlling this order-type obstruction in addition to local AP
avoidance.

The precise missing ingredient is therefore a coherent family of finite avoiding orders in which
every fixed integer eventually has a bounded, stable set of predecessors, or another argument that
turns an AP-avoiding non-well-order into an order of type \(\omega\). The exact counts do not supply
that coherence.

**GAP:** exact finite counts through \(n=14\), with independent checks; no implication for the
existence or nonexistence of an AP-free singly infinite permutation.
