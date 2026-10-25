# Erdős 352 / Koizumi lattice model: exact `f(20)=39`

This directory certifies the finite statement `f(20)=39`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n20_verify.py --min-n 20 --max-n 20 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 39-point witness has 10,660 repeated triples; every exact integer
margin is positive and the minimum is 21. The upper checker exhausts all 172
normalized diameter cases and 21,122 fixed-high branches, reconstructs 21,294
coloring certificates, and directly audits 9,215,235 same-color pairs. The
global upper bound is 39, uniquely tight at `B=(6,4)`. Its certificate-stream
digest is:

```text
bafa932d0529410be48dd4fb8cbd31362ca00bb1188a41699107522f89588996
```

`reference_upper_n20.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces 172
diameter cases, 138 cases with high points, 21,122 fixed-high branches, and
the exact upper total 39, uniquely at `B=(6,4)`.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
