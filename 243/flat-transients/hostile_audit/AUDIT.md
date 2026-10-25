# Hostile audit of the Problem 243 flat-transient bundle

Audit date: 2026-08-12

## Verdict

**PASS.** I found no mathematical overclaim or checker defect in the frozen
core bundle.  The modular recurrence, the construction for every finite
`L` and either sign of nonzero `h`, its absorbing zero tail, reducedness,
strict increase, rational reciprocal sum, the `(eta,delta)` corollary, and
the finite-negative-mass proposition all survive independent verification.

The claim boundary is appropriate: this is a rigorous obstruction to a
uniform fixed-window proof strategy, not a solution or counterexample to
Problem 243.  The source report also explicitly avoids a novelty claim.

Frozen inputs audited:

```text
dda1168ea80a3083784f2ebb1e85baefa77ddebdcb9a2b0e564b5185940c5726  REPORT.md
a968caae28d6f9c0577091e1f413e4e7ba34b79a69344d8ec45a65aa52e6f034  check_243.py
eaf268f460d3ca8a02029a634e20e8ae7243c459a6c23f6fe976c65f042e23b4  check_243.log
1b89fe843d398879ce2e3c338308ada835fe26efc564bda98dea14fdf78350a2  MANIFEST.md
```

I reran `check_243.py` cleanly under Python 3.12.  Its output agrees byte for
byte with `check_243.log`, including the 1,000-step trace hash
`54814b022d6fa9ae977a7e40937296ddeaf03804dbfa706dbbf93605b32a8481`.

## Independent derivation

For a state `x_n=c_n/d_n`, write

```text
d_n = c_n(a_n-1)+e_n,
-c_n/2 <= e_n < c_n/2.
```

Then `c_{n+1}=c_n-e_n` and `d_{n+1}=d_na_n`.  Modulo
`m=c_n-e_n`, one has `c_n == e_n`, and hence

```text
d_{n+1}
  = (c_n(a_n-1)+e_n)a_n
  == e_n a_n^2                       (mod m).
```

Taking the unique centered representative gives the reported next-residue
formula.  Substituting
`d_{n+1}=m(a_{n+1}-1)+e_{n+1}` gives

```text
a_{n+1}=a_n(a_n-1)
          +(e_n a_n^2-e_{n+1})/m+1.
```

This derivation does not require `c_n,d_n` to remain coprime.  The independent
checker tests 197,505 finite states (including `a=1` where positive and all
lower half-ties) and 25,000 transitions from random unreduced states.

## Construction, including the terminal congruence

Let

```text
c_j=p+(L+1-j)h,  1<=j<=L;       c_{L+1}=p,
P_j=product(c_j,...,c_L),        d_1=P_1T+h.
```

The strict bound `p>(L+2)|h|` gives `c_j>2|h|`, so `h` is always the
unique centered residue and no rounding tie occurs.  If
`d_j == h (mod P_j)`, then

```text
a_j=(d_j-h)/c_j+1 == 1 (mod P_{j+1}),
d_{j+1}=d_ja_j       == h (mod P_{j+1}).
```

This proves the constant prefix for either sign.  At the terminal prime,

```text
P_1 == h^L L! (mod p),
d_1 == h(h^(L-1)L!T+1) (mod p).
```

Because `p>L` and `p` does not divide `h`, the coefficient in the chosen
congruence for `T` is invertible; therefore `p|d_1`, and hence
`p|d_{L+1}`.  The next centered residue is zero.  Zero is absorbing.

The audit stresses the negative-sign lower boundary with
`L=512,h=-1,p=521`, for which `c_1=9`, as well as the positive sign and the
published `L=1000,h=-1,p=1001003` certificate.  Its long replay carries the
true denominator only modulo the product of all future numerators and uses
`d_{n+1}=d_na_n` directly; it does not call or assume the claimed
`e_na_n^2` recurrence.

## Reducedness, admissibility, and exact sum

Since `c_1|P_1`,

```text
gcd(c_1,d_1)=gcd(c_1,h)=gcd(p,h)=1.
```

Thus the initial rational is reduced.  Positivity follows from
`c_j>2|h|` and a positive representative `T`; moreover
`a_1=P_2T+1>=3`.

The exact pseudo-greedy identity is

```text
a_{n+1}=a_n^2/(1-epsilon_n)-a_n+1-epsilon_{n+1}.
```

Since `-1/2<=epsilon_n<1/2`, for `a_n>=3` its right side is strictly greater
than `(2/3)a_n^2-a_n+1/2`, which is greater than `a_n`.  Hence the integer
sequence is strictly increasing.  After the first zero it follows the exact
Sylvester recurrence and its squared-ratio tends to one.

At the first zero state, `x_n=c_n/d_n=1/(a_n-1)`, and

```text
1/a_n=1/(a_n-1)-1/(a_{n+1}-1).
```

The tail therefore telescopes to the current remainder.  Independent direct
big-integer simulations for 24 constructions, both signs and `1<=L<=7`,
verify the exact full sum `sum 1/a_n=c_1/d_1` and strict increase across the
transition into the zero tail.

## Quantifiers and the fixed-window claim

With `h=+1` or `h=-1`, choosing the prime scale so that

```text
min_j c_j > max(1/eta,L/delta)
```

gives all `L` nonzero gaps the chosen sign, each magnitude below `eta`, and
total magnitude below `delta`.  The resulting full orbit also converges to
zero, is absolutely summable, and is eventually weakly of either sign
(because it is eventually zero).  Taking `h<0` makes `c_n` increase throughout
the window.  Thus the report's fixed-window obstruction is valid with its
stated word **uniform** and its stated restriction to hypotheses carrying no
additional scale/state information.  It does not rule out scale-dependent or
genuinely global arguments.

## Finite negative gap mass

From `c_{n+1}=c_n(1-epsilon_n)`, discard the nonpositive logarithmic
increments coming from `epsilon_n>=0`; at a negative gap,
`log(1+epsilon_n^-)<=epsilon_n^-`.  If
`S=sum epsilon_n^-<infinity`, this yields the uniform bound

```text
c_n <= c_1 exp(S)=M.
```

Every negative gap has an integral nonzero numerator, so its mass is at least
`1/c_n>=1/M`.  Only finitely many negative gaps can occur.  Thereafter
`c_n` is a nonincreasing sequence of positive integers, hence eventually
constant, which is exactly eventual `e_n=0`.  The absolute-summability
corollary follows immediately.

The stronger sentence about a hypothetical counterexample also checks out.
Such an orbit can never hit zero (zero is absorbing), so integer `e_n` is
nonzero at every index and

```text
|epsilon_n|=|e_n|/c_n >= 1/c_n.
```

Therefore `epsilon_n->0` forces the entire sequence `c_n->infinity`, not just
a subsequence.  Adding this one-line inequality to the publication would make
the sentence maximally transparent, but it is not a correction.

## Independent artifacts

Run:

```bash
python3 audit_243.py
```

The frozen independent output is in `audit_243.log`.  This audit does not
import any producer file or depend on any third-party package.
