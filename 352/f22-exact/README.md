# Erdős 352 / Koizumi lattice model: exact `f(22)=44`

This directory certifies the finite statement `f(22)=44`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n22_verify.py --min-n 22 --max-n 22 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 44-point witness has 15,180 repeated triples; every exact integer
margin is positive and the minimum is 32. The upper checker exhausts all 207
normalized diameter cases and 33,218 fixed-high branches, reconstructs 33,425
coloring certificates, and directly audits 23,388,468 same-color pairs. The
global upper bound is 44, tight at `B=(7,2)`. Its certificate-stream digest is:

```text
64858529dc55172b3d9abba0595768f3f7da04517be5129e51cb265f777f55d0
```

`reference_upper_n22.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces 207
diameter cases, 170 cases with high points, 33,218 fixed-high branches, and
the exact upper total 44, tight at the same direction.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
