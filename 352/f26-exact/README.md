# Erdős 352 / Koizumi lattice model: exact `f(26)=52`

This directory certifies the finite statement `f(26)=52`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n26_verify.py --min-n 26 --max-n 26 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 52-point witness has 24,804 repeated triples; every exact integer
margin is positive and the minimum is 12. The upper checker exhausts all 285
normalized diameter cases and 70,850 fixed-high branches, reconstructs 71,135
coloring certificates, and directly audits 103,499,415 same-color pairs. The
global upper bound is 52, tight at `B=(7,3)`, `B=(7,4)`, `B=(8,2)`, and
`B=(8,3)`. Its certificate-stream digest is:

```text
a0a09b5ebee6bcdae77c14f296b0172c2586a95af83250ab0f5237fddb0d827a
```

`reference_upper_n26.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces every
one of the 285 per-diameter rows and the exact upper total 52.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
