# Erdos Problem 1131: exact four-node minimum

Release date: 2026-08-11 UTC. This is the corrected public-package v3. The
read-only v1 and v2 packages are preserved separately.

## Theorem

For four distinct nodes `x_1,...,x_4` in `[-1,1]`, let `l_k` be the
Lagrange fundamental polynomials and put

```text
I(x_1,...,x_4) = integral[-1,1] sum_k l_k(x)^2 dx.
```

Let `y_0` be the unique real root in `(0,1)` of

```text
21 y^3 + 9 y^2 + 3 y - 1 = 0.
```

Then the global minimum is attained, uniquely up to reordering, at

```text
{-1, -sqrt(y_0), sqrt(y_0), 1}.
```

Numerically,

```text
y_0       = 0.18547209365357910331967400696002633439156697013327...
sqrt(y_0) = 0.43066471140967552383441044480079043898546086346402...
min I     = 1.7107581074011449036290981882769809089928915425385...
```

The minimum is the unique real root of

```text
165375 L^3 - 519750 L^2 + 491040 L - 146912 = 0.
```

This is a finite partial result. It does not resolve the asymptotic problem.

## Proof

### 1. Existence below 2

Use an orthonormal basis `q_0,...,q_3` for the polynomials of degree at most
3 in `L^2[-1,1]`, and let `Q_ij=q_j(x_i)`. Solving for the coefficient
vectors of the four Lagrange polynomials gives

```text
I = trace((Q^T Q)^(-1)).                                      (1)
```

The determinant of `Q` is a nonzero basis constant times the Vandermonde
product. When two nodes coalesce, the smallest singular value of `Q` tends
to zero, so (1) tends to infinity. Compactness of the sorted node simplex
therefore gives a distinct-node minimizer. The Fejer-Legendre nodes
`{-1,-1/sqrt(5),1/sqrt(5),1}` have exact value `12/7<2`; hence the global
minimum is attained and is below 2.

### 2. Both endpoints occur

For a fixed node system write `S(x)=sum_k l_k(x)^2`. Under the affine node
change `x_i(s)=c+s(x_i-c)`, a change of variables gives

```text
I_c(s) = s integral[c+(-1-c)/s, c+(1-c)/s] S(u) du,
I_c'(1) = I-(1-c)S(1)-(1+c)S(-1).                            (2)
```

Strictly outside the node hull, the fundamental polynomial belonging to the
nearest extreme node is a product of three factors greater than 1. Thus
`S(-1)>1` when `-1` is not a node, and `S(1)>1` when `1` is not a node.
If neither endpoint occurs, take `c=0` in (2); if only `1` occurs, take
`c=1`; reflection handles the remaining case. A sufficiently small expansion
is feasible and has derivative less than `I-2<0`, contradicting minimality.
Every minimizer therefore contains both endpoints.

### 3. Fixed endpoints force symmetry

Write the nodes as

```text
{-1,h-a,h+a,1},    0<a<1,    |h|<1-a.
```

Direct exact integration gives

```text
I(h,a)-I(0,a) = 8 h^2 P(a,h)/D(a,h),                         (3)
```

where

```text
D = 105 a^2(a-1)^2(a+1)^2
    (a-h-1)^2(a-h+1)^2(a+h-1)^2(a+h+1)^2
```

is positive in the stated domain, and

```text
P = 119a^10 -259a^8h^2 -131a^8
    +161a^6h^4 +268a^6h^2 -138a^6
    -21a^4h^6 -87a^4h^4 -354a^4h^2 +202a^4
    +6a^2h^6 +43a^2h^4 +108a^2h^2 -61a^2
    -h^6 +11h^4 -19h^2 +9.
```

Set `z=h^2/(1-a)^2`, so `0<=z<1`. As a cubic in `z`, `P` has Bernstein
coefficients

```text
b0 = (1-a^2)^2 A0,
b1 = 2(1-a)^2(a^2+6a+1)A1/3,
b2 = 8a(1-a^2)^2 A2/3,
b3 = 64a^2(1-a^2)^2(7a^2-7a+2),

A0 = 119a^6+107a^4-43a^2+9,
A1 = 49a^6+63a^5+46a^4-18a^3-19a^2+3a+4,
A2 = 49a^4+63a^3-73a^2+13a+4.
```

They are all positive for `0<a<1`. For `A0`, the quadratic
`107y^2-43y+9` has discriminant `-2003`, and the remaining term is
`119a^6>0`. For `A1,A2`, substitute `t=a/(1-a)>0`; the coefficient lists of
`(1+t)^8 A_i(t/(1+t))` are respectively

```text
[4,35,114,155,56,16,224,320,128],
[4,45,130,122,4,45,214,196,56].
```

Finally, `7a^2-7a+2=7(a-1/2)^2+1/4`. Positivity of the Bernstein basis and
all four coefficients gives `P>0`, so (3) is strict unless `h=0`.

### 4. The remaining variable

For the nodes `{-1,-a,a,1}`, exact integration gives

```text
I(0,a) = 4(35a^6-28a^4+23a^2+2)
         /(105a^2(a-1)^2(a+1)^2),

dI(0,a)/da = -16(21a^6+9a^4+3a^2-1)
             /(105a^3(a-1)^3(a+1)^3).
```

On `0<a<1`, the derivative has the sign of
`q(a^2)=21a^6+9a^4+3a^2-1`. The polynomial
`q(y)=21y^3+9y^2+3y-1` is strictly increasing for `y>=0` and changes sign
between 0 and 1. The objective tends to infinity at both endpoints, so its
single critical point is its unique minimum. Eliminating `y` gives the
displayed cubic in `L`.

For completeness, the exact discriminants are

```text
disc(21y^3+9y^2+3y-1) = -20736,
disc(165375L^3-519750L^2+491040L-146912)
    = -19439210456064000000.
```

Each is negative, so each cubic has exactly one real root. This proves the
two unique-real-root clauses used above and in the theorem statement.

## Verification

First install the pinned dependencies in an out-of-tree environment as shown
in `ENVIRONMENT.md`. After verifying the published outer archive hash, run
the exact certificate with that environment's interpreter:

```text
PYTHON=/tmp/erdos1131-public-venv/bin/python ./run_all.sh
```

Add the independent numerical smoke check with:

```text
PYTHON=/tmp/erdos1131-public-venv/bin/python ./run_all.sh --with-numeric
```

The bare system `python3` is not claimed to contain the dependencies. If the
pinned environment is already activated, `./run_all.sh` is equivalent.

Before executing mathematical Python from the bundle, `run_all.sh` verifies
the SHA-256 of `MANIFEST.sha256` against `MANIFEST.sha256.pin`, preflights the
type of every listed member, authenticates `verify_manifest.py`, and runs that
verifier with Python isolated/safe-path flags. The authenticated verifier then
hashes the full payload and enforces exact closed-world membership. It rejects
missing files, extra files, malformed manifests, symlinks, and all non-regular
members. Every Python entry point requires isolated/safe-path execution and
explicitly rejects `-O`, `-OO`, and `PYTHONOPTIMIZE`; no verdict uses `assert`.

`verify_exact.py` derives the objective from the Lagrange basis, performs the
integrations exactly, verifies (1)-(3), the Bernstein transforms, derivative,
discriminants, root isolations, and resultant. `verify_numeric.py` compares
high-precision direct quadrature with an orthonormal Legendre Gram matrix.

No optimizer is included in this public bundle. Numerical optimization in v1 was only a
non-proof smoke test and is not evidence for the theorem. The exact checker
is the certificate; the optional numerical checker is also non-proof.

The pin file is an in-archive bootstrap, not a signature. A coordinated edit
of the pin and manifest is detected only by checking the separately published
deterministic-tar SHA-256. The outer archive hash is the release trust root.

## Novelty and license

See `SOURCES.md`. In particular, the full 1997 article and its prior
references have not been checked for an exact small-`n` theorem. This package
makes no novelty or priority claim.

Original code and documentation in this bundle are available under the MIT
License in `LICENSE`, subject to the precise scope in `NOTICE`. External
papers and Python packages are not included.
