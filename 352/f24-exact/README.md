# Erdős 352 / Koizumi lattice model: exact `f(24)=48`

This directory certifies the finite statement `f(24)=48`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n24_verify.py --min-n 24 --max-n 24 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 48-point witness has 19,600 repeated triples; every exact integer
margin is positive and the minimum is 25. The upper checker exhausts all 243
normalized diameter cases and 48,626 fixed-high branches, reconstructs 48,869
coloring certificates, and directly audits 49,876,704 same-color pairs. The
global upper bound is 48, tight at `B=(7,2)`, `B=(7,3)`, `B=(7,4)`, and
`B=(8,1)`. Its certificate-stream digest is:

```text
4bdd9d9f9bad728c22531e753711fe126971ce3eb29d52937c818add3b15202b
```

`reference_upper_n24.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces the
same diameter and fixed-high counts and the exact upper total 48.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
