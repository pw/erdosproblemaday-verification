# A finite counterexample to the density-doubling inequality for sets of multiples

The claim is that a fixed finite set of positive integers can have its multiples become more than twice as common when we count up to a larger endpoint. Both endpoints are at least as large as every member of the set. The proof below constructs such a set using numbers built only from small primes.

For a finite set $A$ of positive integers, let $M_A(x)$ count the integers from 1 to $x$ that are divisible by at least one member of $A$. In symbols,

```math
M_A(x)=\#\{j\in\mathbb N:1\le j\le x,\ \exists a\in A\text{ with }a\mid j\}.
```

Here `#` means “the number of elements,” and `a | j` means “a divides j.” Dividing the covered count by x gives the fraction covered by the set.

The construction below proves that there exist a nonempty finite $A$ and integers $m>n\ge\max A$ for which

```math
\boxed{\quad 2mM_A(n)\lt nM_A(m).\quad}
```

This is a strict reverse of the proposed density-doubling inequality. The proof uses finite counting, unique factorization, and exact integer comparisons.

**Verification status.** The [standalone Lean proof](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean) has passed the local Lean kernel check and Jig’s complete local preflight, including the exact target bridge and axiom audit. Its only axioms are `propext`, `Classical.choice`, and `Quot.sound`. It uses no `sorry`, `native_decide`, or imported statement axiom. **Jig server verification passed on 5 September 2026.** The server also checked that this is the exact negation of the original statement. [Jig statement 40](https://jig.so/p/398?s=40) is verified, the original root is marked **refuted**, and the problem is **closed**. [Server verification run](https://github.com/WoshuaJolk/jig-verifier/actions/runs/33990129375).

## The fixed primes and constants

Let

```math
P=\{p:p\text{ is prime and }p\lt 257\},\qquad S=P\setminus\{2\}.
```

There are 54 primes in $P$, of which 53 belong to $S$. Call a positive integer *P-smooth* if all its prime factors belong to $P$, and define *S-smooth* similarly. In particular, every $S$-smooth integer is odd, and 1 is smooth for either set.

Put

```math
Q=\prod_{p\in S}p,\qquad
\phi=\prod_{p\in S}(p-1)=\varphi(Q).
```

The last equality follows from multiplicativity of Euler’s totient function on distinct primes. The following finite integer comparisons are checked exactly in Lean:

**Equation (1).**

```math
|S|=53,\qquad Q>128,\qquad 3Q\lt 16\phi,
```

and

**Equation (2).**

```math
2^{4096}\,32769^{53}\lt 3^{4096}.
```

These are exact comparisons of explicit finite products and powers; no decimal approximations enter the proof. See the [constant comparison](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L439) and [power comparison](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L125).

## A finite choice of scale

For $j\ge0$, define

```math
H(j)=\#\{d:1\le d\le256^j,\ d\text{ is }S\text{-smooth}\}.
```

Unique factorization identifies each such $d$ with its 53 prime exponents. Every exponent is at most $8j$: if $p^e\mid d$, then

```math
2^e\le p^e\le d\le256^j=2^{8j}.
```

Consequently

**Equation (3).**

```math
H(j)\le(8j+1)^{53},\qquad H(0)=1.
```

There must be an integer $k\lt 4096$ satisfying

**Equation (4).**

```math
2H(k+1)\le3H(k).
```

Otherwise every one of the first 4096 steps would grow by a factor greater than $3/2$. Induction, followed by (3), would give

```math
3^{4096}\le2^{4096}H(4096)
\le2^{4096}32769^{53},
```

contradicting (2).

Choose such a $k$, and set

```math
T=256^k,\qquad h=H(k).
```

Here $T>0$ and $h\ge1$. **The proof establishes the existence of $k$ in the finite range $0\le k\lt 4096$; it does not compute its value.** This is the [finite growth component](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L140).

## The family and the two endpoints

Define

**Equation (5).**

```math
A=\{a:T\lt a\le256T,\ a\text{ is }P\text{-smooth}\},
\qquad n=256T,\qquad m=2TQ.
```

The family $A$ is finite and consists of positive integers. It is nonempty because $2T=2^{8k+1}\in A$. By definition, every member is at most $n$. Since $Q>128$, we also have

```math
m=2TQ>256T=n.
```

The construction uses the entire smooth band $A$. The proposed inequality permits redundant generators, so no divisibility-minimal basis is needed.

## Counting covered integers up to n

The covered integers in $[1,n]$ are exactly the members of $A$. Indeed, if $a\in A$ divides $j\le256T$, write $j=ac$. Then $c$ is positive and less than 257. Every prime factor of $c$ therefore belongs to $P$, so $j$ is $P$-smooth. Also $j\ge a>T$, giving $j\in A$. The converse follows because every member of $A$ covers itself. Thus

**Equation (6).**

```math
M_A(n)=|A|.
```

Write each $a\in A$ uniquely as

```math
a=2^e d,
```

where $d$ is $S$-smooth. Necessarily $d\le256T$. For a fixed $d$, there is at most one admissible exponent in each residue class modulo 8. To see this, suppose $f>e$ and $f\equiv e\pmod8$. Then $f\ge e+8$, and

```math
2^f d\ge256\,(2^e d)>256T,
```

so both numbers cannot belong to $A$.

Therefore the map $a\mapsto(d,e\bmod8)$ is injective, giving

**Equation (7).**

```math
M_A(n)\le8H(k+1)\le12H(k)=12h.
```

The last step is (4). This is the [near-count bound](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L267).

## Counting covered integers up to m

For each $S$-smooth $d\le T$, choose the least exponent $e(d)\ge0$ for which

```math
c_d=2^{e(d)}d>T.
```

Such an exponent exists. Since $d\le T$, minimality gives $e(d)\ge1$ and

**Equation (8).**

```math
2^{e(d)-1}d\le T,
\qquad T\lt c_d\le2T.
```

In particular $c_d\in A$.

Let

```math
R=\{r:0\le r\lt Q,\ \gcd(r,Q)=1\}.
```

There are exactly $\varphi(Q)=\phi$ elements of $R$. Because $Q>1$, each is positive. Consider the map

**Equation (9).**

```math
(d,r)\longmapsto c_d r,
\qquad d\le T\text{ is }S\text{-smooth},\quad r\in R.
```

Every image is positive, at most $2TQ=m$, and covered by $A$, because $c_d\in A$.

The map is injective. Suppose

```math
2^{e(d)}dr=2^{e(d')}d'r'.
```

All prime factors of $d$ belong to $S$, whereas $r'$ is coprime to $Q$, and $d$ is odd. Thus $d$ is coprime to $2^{e(d')}r'$. The equality implies $d\mid d'$. The same reasoning in the other direction gives $d'\mid d$, hence $d=d'$. The selected multiplier $c_d$ is then the same on both sides, and cancellation gives $r=r'$.

There are $h\phi$ pairs in (9), so

**Equation (10).**

```math
M_A(m)\ge h\phi.
```

This is the [far-count injection](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L346). It counts actual integers below the finite endpoint $m$; no limiting density or full-period enumeration is used.

## The strict reverse inequality

Combine (7), (10), and $3Q\lt 16\phi$. Since $T,h>0$,

```math
2mM_A(n)\le 2(2TQ)(12h)=48TQh.
```

```math
48TQh\lt 256T\phi h.
```

```math
256T\phi h\le nM_A(m).
```

Together with (5), this proves a finite nonempty family $A$ and endpoints $m>n\ge\max A$ satisfying the claimed strict reverse inequality. The index $k$ and the resulting family are specified through a proved finite existence argument and are not enumerated.

The assembled Lean source proves both [the existence of this counterexample](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L451) and [the literal negation of the unrestricted density-doubling statement](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean#L484).


## Reproducibility and scope

- Jig problem #398 is Erdős #488. This refutes the corrected **multiples** formulation, not the earlier nonmultiples transcription. The constructed generators all exceed 1.
- Lean `4.33.0`; Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`.
- Source SHA-256: `37d2f3b46b3979d676ad50802fa9e2c08eaaf1cd859dee85271ad3e5ca639fe2`.
- Artifact: `ddb941ea-1245-4e95-9142-52ddf5565dc4`; statement: `3f4e2684-fb49-47d1-beda-5abf549759a9`.
- Server verdict and exact refutation check: [Jig verification run](https://github.com/WoshuaJolk/jig-verifier/actions/runs/33990129375).
- A bounded prior-art search did not locate an earlier matching full refutation. This is not an exhaustive priority certification.


## AI assistance disclosure

This construction and its Lean formalization were produced using GPT-6 Astra agents in Codex, directed by Declan Gessel. Jig ran the independent Lean verification. This explanatory note was also drafted with AI assistance. Human specialist review, historical interpretation, and priority checking are being sought; no completed human peer review is claimed.
