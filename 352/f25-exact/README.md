# Erdős 352 / Koizumi lattice model: exact `f(25)=52`

This directory certifies the finite statement `f(25)=52`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n25_verify.py --min-n 25 --max-n 25 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 52-point witness has 24,804 repeated triples; every exact integer
margin is positive and the minimum is 25. The upper checker exhausts all 263
normalized diameter cases and 58,662 fixed-high branches, reconstructs 58,925
coloring certificates, and directly audits 70,784,474 same-color pairs. The
global upper bound is 52, uniquely tight at `B=(7,3)`. Its certificate-stream
digest is:

```text
da9e4abb06fc00a51d58ff40e255889c7d9c3cafe502276e97d52260be3f5a3a
```

`reference_upper_n25.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces the
same diameter and fixed-high counts and the exact upper total 52.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
