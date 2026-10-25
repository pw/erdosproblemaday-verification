# Erdős 352 / Koizumi lattice model: exact `f(21)=41`

This directory certifies the finite statement `f(21)=41`, where every triple
in an `N`-avoiding subset of `Z^2`, with repetitions allowed, satisfies

```text
|area(p,q,r)-N| > diameter(p,q,r).
```

It does not prove the uniform estimate `f(N)=O(N)` and therefore does not
solve the original continuous problem.

## Reproduce

```bash
python3 erdos352_n21_verify.py --min-n 21 --max-n 21 --json
sha256sum -c SHA256SUMS
```

Run the assertion-based checker with ordinary `python3`, never `python3 -O`.

The embedded 41-point witness has 12,341 repeated triples; every exact integer
margin is positive and the minimum is 5. The upper checker exhausts all 188
normalized diameter cases and 26,250 fixed-high branches, reconstructs 26,438
coloring certificates, and directly audits 14,588,044 same-color pairs. The
global upper bound is 41, tight at `B=(5,5)` and `B=(6,4)`. Its
certificate-stream digest is:

```text
cd5c1d7f245d3412ee966bd4ffbf138f06f6d5213d57ab589b9563001ae9bca3
```

`reference_upper_n21.json` is the output of the independent public upper
implementation at commit
`7a4a19468771766cb4f20e10dfa5cf770cc2487b`. It separately reproduces 188
diameter cases, 153 cases with high points, 26,250 fixed-high branches, and
the exact upper total 41, tight at the same two directions.

The lower witness was posted previously by BorisAlexeev and appears in the
public witness repository at commit
`09e5c5393943c881ab60118aa32fe5660539c8d5`; its source JSON is included and
no priority claim is made for it.
