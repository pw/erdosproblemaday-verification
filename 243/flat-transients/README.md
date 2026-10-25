# Problem 243: exact flat-transient construction

This bundle supports a rigorous partial result for Erdős Problem 243. In
Koizumi's pseudo-greedy formulation, for every length `L >= 1` and every
nonzero integer `h`, it constructs a positive rational whose centered gap
numerators satisfy

```text
e_1 = ... = e_L = h,       e_n = 0 for n >= L+1.
```

Either sign is possible. The nonzero normalized gaps can simultaneously be
made arbitrarily small and have arbitrarily small total mass. The bundle also
proves that finite total negative gap mass forces eventual zero. These are
finite/global structural results, not a solution or counterexample to the
open problem.

## Contents

- `REPORT.md` gives the exact modular recurrence, the construction and proof,
  its admissibility for Problem 243, the fixed-window obstruction, and the
  negative-mass termination proposition.
- `check_243.py` is a self-contained standard-library exact checker. It
  compares two dynamics implementations, audits 320,760 finite states, tests
  both-sign construction grids, and verifies a 1,000-step small-gap example.
- `check_243.log` is the frozen clean output.
- `hostile_audit/` contains an independent audit when present.
- `SHA256SUMS` pins the bundle artifacts.

## Reproduce

From this directory:

```bash
python3 check_243.py
sha256sum -c SHA256SUMS
```

The checker uses Python assertions as fail-closed checks. Use ordinary
`python3`, not `python3 -O`. No third-party package or floating-point
arithmetic is used.

The primary source used for the reformulation is Junya Koizumi,
*Irrationality of the reciprocal sum of doubly exponential sequences*,
[arXiv:2504.05933](https://arxiv.org/abs/2504.05933), especially Lemma 15 and
Theorem 16. The paper itself is not redistributed here.
