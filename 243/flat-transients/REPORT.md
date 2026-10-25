# Erdős Problem 243: exact modular dynamics and arbitrarily long flat transients

Date checked: 2026-08-12

## Outcome

This is rigorous partial progress, not a proof or counterexample to Problem 243.

For every prescribed length `L` and every nonzero integer `h`, there is a
positive rational number whose pseudo-greedy gap numerators are

```text
e_1 = e_2 = ... = e_L = h,   e_{L+1} = e_{L+2} = ... = 0.
```

The construction works with either sign of `h`, has no rounding ties, and
gives a strictly increasing integer sequence satisfying all the hypotheses of
Problem 243. By taking its scale large, the first `L` nonzero gaps can be made
arbitrarily small individually and in total.

Consequently, no uniform fixed-window argument based only on small gaps can
force a zero, a sign change, an exit from the small-gap band, or (for negative
`h`) a decrease of the integer numerator `c_n`. Any complete proof needs a
genuinely global or scale-sensitive ingredient.

There is also a simple global sufficient condition:

> If the negative gap mass `sum_n max(-epsilon_n, 0)` is finite, then the gap
> sequence is eventually zero.

In particular, absolute summability of the gaps implies termination.

## Status and source boundary

- The current public page <https://www.erdosproblems.com/243> lists the problem
  as open. The live collaboration gate checked on 2026-08-12 showed **0 proof
  claims**, **no current worker or collaborator**, and **7 comments**. None of
  those visible comments contained this construction.
- Junya Koizumi, *Irrationality of the reciprocal sum of doubly exponential
  sequences*, <https://arxiv.org/abs/2504.05933>, Theorem 16, reformulates the
  problem as the eventual vanishing of the pseudo-greedy gap sequence under
  the hypothesis `epsilon_n -> 0`.
- The state variables below are those of Koizumi's Lemma 15. The modular
  one-step formula and the flat-transient construction were not located in a
  text search of that paper or in the currently visible page comments. That is
  only a search report, not a novelty or priority claim.
- Local source snapshot used for checking:
  `koizumi_2504.05933.pdf`, SHA-256
  `b27a16281cfe52b2c76264e088f2b1c61623e1caba6b23e5506d19cfaa929190`.
  The third-party PDF need not be redistributed with a verification bundle.

## Problem and pseudo-greedy state

Problem 243 asks whether every strictly increasing sequence of positive
integers `(a_n)` satisfying

```text
a_{n+1}/a_n^2 -> 1,                    sum_n 1/a_n is rational
```

must eventually satisfy

```text
a_{n+1} = a_n^2 - a_n + 1.
```

For a positive rational remainder `x_n=c_n/d_n`, keep the unreduced positive
integers `c_n,d_n` and define `e_n` to be the centered residue

```text
e_n == d_n (mod c_n),       -c_n/2 <= e_n < c_n/2.
```

The half-open interval agrees with nearest-integer rounding in which a half
integer rounds upward. Then

```text
a_n     = (d_n-e_n)/c_n + 1,
c_{n+1} = c_n-e_n,
d_{n+1} = d_n a_n,
epsilon_n = e_n/c_n.
```

These are exact integer identities; no reduction of `c_n/d_n` is needed.

## Exact one-step modular dynamics

Put `m=c_{n+1}=c_n-e_n`. Since

```text
d_n = c_n(a_n-1)+e_n
```

and `c_n == e_n (mod m)`, one has

```text
d_n == e_n a_n (mod m),
d_{n+1}=d_n a_n == e_n a_n^2 (mod m).
```

Therefore the next centered residue is exactly

```text
e_{n+1} = centered_residue(e_n a_n^2, c_n-e_n).              (1)
```

If

```text
q_n = (e_n a_n^2-e_{n+1})/(c_n-e_n),
```

then the quotient is integral and direct substitution gives

```text
a_{n+1} = a_n(a_n-1)+q_n+1.                                 (2)
```

Equations (1)-(2) permit exact modular exploration without materializing the
doubly exponential denominators.

## Flat-transient theorem

**Theorem.** Let `L>=1` and let `h` be any nonzero integer. There is a reduced
positive rational `r=c_1/d_1` whose pseudo-greedy state satisfies

```text
e_j=h  for 1<=j<=L,             e_j=0 for every j>=L+1.
```

More explicitly, choose a prime

```text
p > (L+2)|h|
```

and define

```text
c_j = p+(L+1-j)h       (1<=j<=L),
c_{L+1}=p,
P_j = product_{k=j}^L c_k,
P=P_1.
```

Because `p>L` and `p` does not divide `h`, the coefficient
`h^(L-1)L!` is invertible modulo `p`. Choose a positive, sufficiently large
integer `T` in the residue class

```text
h^(L-1)L! T == -1 (mod p),                                  (3)
```

and put

```text
d_1=PT+h,                    r=c_1/d_1.
```

Taking a sufficiently large representative of the class in (3), for example
one with `T>=2`, is harmless.

### Proof of the constant prefix

We prove by induction that

```text
d_j == h (mod P_j)                  (1<=j<=L).                (4)
```

The case `j=1` follows from `d_1=PT+h`. Suppose (4) holds. Since
`c_j` divides `P_j`, the residue of `d_j` modulo `c_j` is `h`. Moreover,

```text
c_j >= min(p-L|h|,p) > 2|h|,
```

so `h` is strictly inside the centered interval and is the unique centered
residue: there is no tie. Thus `e_j=h`. Also

```text
a_j=(d_j-h)/c_j+1 == 1 (mod P_{j+1}),
```

and consequently

```text
d_{j+1}=d_j a_j == h (mod P_{j+1}).
```

Finally `c_{j+1}=c_j-h`, giving the displayed formula for every `c_j` and
completing the induction.

### Proof of the zero tail

Modulo `p`,

```text
P = product_{t=1}^L (p+t h) == h^L L!,
```

so (3) gives

```text
d_1=PT+h == h(h^(L-1)L!T+1) == 0 (mod p).
```

Every later `d_j` is a multiple of `d_1`. At state `L+1` the numerator is
`c_{L+1}=p`, hence the centered residue of `d_{L+1}` modulo `p` is zero.
Once `e_j=0`, both `c_j=p` and divisibility `p|d_j` persist, so every later
residue is zero. This proves the theorem.

## Admissibility for Problem 243

All side conditions can be checked exactly.

- **Positive state and no ties.** The choice of `p` gives
  `c_j>2|h|>0` throughout the nonzero prefix and at the terminal state.
  Also `d_1=PT+h>0` for `T>=2`; all later denominators are positive.
- **Reduced initial rational.** Since `c_1` divides `P`,
  `gcd(c_1,d_1)=gcd(c_1,h)=gcd(p,h)=1`.
- **Strict increase.** Writing `P_2=product_{j=2}^L c_j`, with the empty
  product equal to one, gives `a_1=P_2T+1>=3`. Every centered gap satisfies
  `-1/2<=epsilon_n<1/2`, and Koizumi's exact recurrence is

  ```text
  a_{n+1}=a_n^2/(1-epsilon_n)-a_n+1-epsilon_{n+1}.
  ```

  Therefore, for `a_n>=3`,

  ```text
  a_{n+1} > (2/3)a_n^2-a_n+1/2 > a_n.
  ```

  Induction proves strict increase.
- **Required asymptotic.** From state `L+1` onward, `epsilon_n=0`, so
  `a_{n+1}=a_n^2-a_n+1` exactly and `a_{n+1}/a_n^2 -> 1`.
- **Rational reciprocal sum.** At the first zero state,
  `d_n=c_n(a_n-1)`, so the remaining rational is `1/(a_n-1)`. The zero-gap
  tail telescopes via

  ```text
  1/a_n = 1/(a_n-1)-1/(a_{n+1}-1).
  ```

  Hence the full reciprocal sum is exactly the initial rational `c_1/d_1`.

Thus these are genuine admissible Problem 243 sequences which eventually obey
the claimed recurrence. They are deliberately long transients, not
counterexamples.

## Quantitative corollary and the obstruction to fixed windows

**Corollary.** Given `L>=1`, `eta>0`, `delta>0`, and either sign
`sigma in {-1,+1}`, there is an admissible sequence with

```text
sign(e_j)=sigma,      0<|epsilon_j|<eta             (1<=j<=L),
sum_{j=1}^L |epsilon_j| < delta,
epsilon_j=0                                         (j>=L+1).
```

Take `h=sigma` in the theorem and then take `p` so large that

```text
min_{1<=j<=L} c_j > max(1/eta, L/delta).
```

The two inequalities follow immediately from `|epsilon_j|=1/c_j`.

This rules out any **uniform** finite-window assertion whose only hypotheses
are smallness of the gaps (even small total mass), convergence to zero,
absolute summability, or weak eventual one-sidedness, and whose conclusion is
that within that fixed window there must be:

- a zero gap;
- a sign change;
- an exit from the prescribed small-gap band; or
- a decrease of `c_n` (choose `h<0`, when `c_{j+1}=c_j+|h|`).

The word “uniform” matters. A bound depending on the arithmetic scale or on
additional state information is not excluded.

The examples are eventually zero and hence satisfy both weak conditions
`epsilon_n>=0` eventually and `epsilon_n<=0` eventually. This says only that
those conditions do not bound the transient length; it says nothing about an
eventually negative, never-zero orbit.

## A global termination criterion

Write

```text
epsilon_n^- = max(-epsilon_n,0).
```

**Proposition.** If

```text
sum_n epsilon_n^- < infinity,
```

then `e_n=epsilon_n=0` for all sufficiently large `n`.

**Proof.** The exact numerator recurrence gives

```text
c_{n+1}=c_n(1-epsilon_n).
```

A nonnegative gap can only decrease `c_n`. At a negative gap,
`log(1-epsilon_n)=log(1+epsilon_n^-)<=epsilon_n^-`. Consequently

```text
c_N <= c_1 exp(sum_n epsilon_n^-) =: M
```

for every `N`. If `e_n<0`, integrality gives `-e_n>=1`, hence

```text
epsilon_n^- = (-e_n)/c_n >= 1/M.
```

Finite negative mass therefore permits only finitely many negative `e_n`.
After the last one, `(c_n)` is a nonincreasing sequence of positive integers,
so it eventually becomes constant. Since `e_n=c_n-c_{n+1}`, this forces
`e_n=0` eventually. QED.

Consequences:

- `sum_n |epsilon_n|<infinity` implies eventual zero.
- An eventually nonnegative gap sequence terminates; this is also Koizumi's
  Proposition 19(2), corresponding to the known Badea regime.
- Any counterexample to the pseudo-greedy reformulation must have
  `sum_n epsilon_n^-=infinity`. Because a counterexample also has
  `epsilon_n->0` and can never hit the absorbing value zero, its positive
  integer `c_n` must in fact tend to infinity: integrality gives
  `|epsilon_n|=|e_n|/c_n >= 1/c_n` whenever `e_n` is nonzero.
- No conclusion about eventual nonpositivity alone is claimed.

## Exact verification

Run the self-contained, standard-library checker:

```bash
python3 verification/243/flat-transients/check_243.py
```

It performs the following independent exact checks.

1. It compares the modular recurrence with direct `Fraction`/integer
   pseudo-greedy simulation for 1,000 random rationals and eight steps each.
2. It verifies (1)-(2) for 320,760 valid finite states.
3. It verifies the construction for 80 combinations of both signs,
   `1<=L<=100`, including direct rational replay, strict increase, the first
   zero, and the exact telescoping sum for the tractable cases.
4. It verifies 72 rational `(eta,delta)` bounds with both signs.
5. It constructs and independently replays a 1,000-step certificate with
   `h=-1`, every nonzero `|epsilon_j|<10^-6`, followed by zero.

Expected output:

```text
random_direct_vs_modular=PASS trials=1000 steps=8
finite_transition_box=PASS states=320760
construction_grid=PASS cases=80
eta_delta_grid=PASS cases=72
large_certificate: L=1000 h=-1 p=1001003 c0=1000003 digits(P)=6001 trace_sha256=54814b022d6fa9ae977a7e40937296ddeaf03804dbfa706dbbf93605b32a8481
ALL EXACT CHECKS PASSED
```

The large trace digest hashes newline-separated records
`index,c,e,a_mod_(c-e)` for states `0,...,1000`. Its huge denominator is never
trusted implicitly: a second replay carries `d_n` modulo the remaining product
`c_n c_{n+1}...c_{1001}` and does not use formula (1).

Exploratory hostile searches are recorded in `search.py` and the two JSON
logs. Among 5,000 random initial states constrained by `e_1=-1`, and 10,000
random initial states with arbitrary nonzero centered `e_1`, all hit zero
within 100 tested steps (observed maxima 15 and 18). This finite experiment is
not evidence of termination at scale and is not used in any proof.

## Exact claim boundary

Proved here:

- the one-step centered-residue recurrence;
- arbitrary finite constant-residue prefixes of either sign, with an
  explicitly engineered zero tail;
- arbitrarily long, arbitrarily small, arbitrarily low-mass nonzero gap
  windows inside fully admissible sequences;
- termination under finite negative gap mass.

Not proved here:

- Problem 243 or Koizumi's Conjecture 6;
- existence of an infinite nonzero small-gap orbit;
- termination under eventual nonpositivity;
- any uniform bound that is allowed to depend on the arithmetic scale;
- novelty or historical priority of the construction.

PARTIAL: Exact dynamics produce arbitrarily long constant nonzero gap transients of either sign (then an absorbing zero tail), refuting uniform small-gap fixed-window strategies, while finite total negative gap mass is proved sufficient for eventual zero.
