# Erdős 352 / Koizumi lattice model: exact `f(19)=38`

This directory certifies the finite statement `f(19)=38`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n19_verify.py --min-n 19 --max-n 19 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 38-point witness has 9,880 repeated triples; every exact integer
margin is positive and the minimum is 5. The upper checker exhausts all 156
normalized diameter cases and 16,622 fixed-high branches, reconstructs 16,778
coloring certificates, and directly audits 5,673,504 same-color pairs. The
global upper bound is 38, uniquely tight at `B=(6,3)`. Its certificate-stream
digest is:

```text
2d8b6e3ef793869a9e6a05726e6e7b434efc7b3695d3307343e1b083a4e1822d
```

`reference_upper_n19.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces 156
diameter cases, 123 cases with high points, 16,622 fixed-high branches, and
the exact upper total 38, uniquely at `B=(6,3)`.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
