# Problem 1131: exact four-node minimum

This directory publishes an exact global certificate for the four-node case
of Erdos Problem 1131.

Let `l_k` be the Lagrange fundamental polynomials for four distinct nodes in
`[-1,1]`, and let

```text
I = integral[-1,1] sum_k l_k(x)^2 dx.
```

If `y_0` is the unique root in `(0,1)` of

```text
21 y^3 + 9 y^2 + 3 y - 1 = 0,
```

then the unique minimizing node set, up to reordering, is

```text
{-1, -sqrt(y_0), sqrt(y_0), 1}.
```

The minimum is the unique real root of

```text
165375 L^3 - 519750 L^2 + 491040 L - 146912 = 0.
```

This is a finite partial result. It does not settle the asymptotic question
on the official problem page.

## Contents

- `public/` is the fail-closed exact certificate and optional numerical smoke
  check. It is the extracted content of the deterministic release archive.
- `hostile_audit/` is the independent frozen-byte release audit.
- `literature_audit/` records the conservative prior-work boundary without
  redistributing the 1997 article or any other third-party source.

The public release archive itself is not duplicated in this repository. Its
SHA-256 is

```text
2563c7e927a5f038211716511719473ba713cc03bf3e486efe7ad68b7b5166b7
```

Important inner anchors are:

```text
d518ead8ded0a2962bc0330709042c6dfafbb7e9dcde80d297f2bea5e64bea8a  public/MANIFEST.sha256
aef819af01edb79496186d56d273c766830def3b3383c079267d2569137477d0  hostile_audit/AUDIT.md
a51422a326539fff50c1d173c4c5e01a3e1b0499d33d4c9a634a9a1dd8b60ead  hostile_audit/MANIFEST.sha256
07529cf6b85452c50fb389e6f4509dfd6e9afe15275f4dd336a6f124b1c9deb1  literature_audit/README.md
99f94c52cfc02c60edac29c4c8796ff3efbac2346a9f21aa00996a8fe887e9cf  literature_audit/MANIFEST.sha256
```

## Reproduce

Create the pinned environment outside this closed directory, then run:

```text
python3.12 -m venv /tmp/erdos1131-public-venv
/tmp/erdos1131-public-venv/bin/pip install -r public/requirements-numeric.txt
PYTHON=/tmp/erdos1131-public-venv/bin/python ./reproduce.sh
```

The wrapper verifies the repository-level checksums, runs the public exact and
numerical checks, and verifies both audit manifests.

## Prior work and scope

Brutman and Toledano numerically computed high-precision minima for
`n=3,...,100` in 1997, so the four-node optimizer and minimum were already
known numerically. This package supplies an independently checkable exact
global certificate and algebraic characterization. It makes no claim of
priority for the exact formulas. The complete 1997 body was not available to
the audit, so the package expressly leaves the exact-formula novelty question
unresolved.

No third-party PDF, publisher XML, site snapshot, or installed Python package
is included here. License scope for the original public-bundle code and prose
is stated in `public/LICENSE` and `public/NOTICE`.
