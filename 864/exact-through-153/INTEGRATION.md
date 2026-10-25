# Integration notes

Suggested destination:

```text
verification/864/exact-through-153/
```

Suggested report headline addition:

```text
Computational extension (2026-08-12): two independent reflected-core
enumerations prove F(135)=...=F(152)=19 and F(153)=20.  The new 20-point
witness has diameter 152; every possible exact reflected core under cap 151,
for core sizes 20 through 14, is exhausted.
```

Scope label: **computational-only / finite exact extension**.  Do not describe
this as resolving the asymptotic problem.

The clean bundle to copy is `/tmp/erdos864_target20_audited`.  Run

```bash
python3 replay_checks.py
sha256sum -c SHA256SUMS
```

after copying.  The report explicitly documents the corrected inclusive
even-core endpoint and the caught/retracted scratch slicing shortcut.
