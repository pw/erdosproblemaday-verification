# Erdos problem #295: exact finite-frontier verification

This bundle verifies the finite results

```text
k(17) = 32.
33 <= k(18) <= 35.   (ours, 2026-08-11)
33 <= k(18) <= 34.   (upper bound by a reader, 2026-10-11 — see reader-k18-34/)
```

It does not settle the asymptotic question in Erdos problem #295.

**2026-10-11:** a reader, Kyunghan Bae, sent a 34-term certificate (denominators 18 … 63, 275, 14143068,
10457416992) that cuts the upper bound to 34. Our three-route check, a frozen copy of his release and the
verdict are in [`reader-k18-34/`](reader-k18-34/). The lower bound below is unchanged.

The `k(18)` report, two exact search implementations, captured runs, hostile
audit, and reproduction instructions are in [`k18/`](k18/). Its lower bound is
a rigorous computational exclusion of 31- and 32-term expansions, while its
upper bound is an explicit exact 35-term identity. It does not determine which
of 33, 34, or 35 is the exact value.

## `k(17)` fast checks

```bash
python3 verification/295/verify_295_k17_certificate.py
python3 verification/295/verify_295_k17_wide_states.py
```

The first command checks the explicit 32-term identity and the harmonic
exclusion through 28 terms. The second independently checks the two terminal
states for which divisor enumeration replaces a direct scan.

## `k(17)` full exact search

The full 31-term exclusion requires GMP:

```bash
g++ -O3 -std=c++17 -pthread \
  verification/295/verify_295_k17.cpp \
  -lgmpxx -lgmp -o /tmp/verify_295_k17
/tmp/verify_295_k17 17 31 14 21
```

The program returns exit code `20` when no expansion exists and `10` if it
finds one. The recorded output is in `reference_run.log`; the expected totals
are 447,526,713 recursive states, 382,969,084 two-term states, 5,721,929,705
direct-scan candidates, and 45,467,731 divisor candidates.

All branch deletions use exact GMP rational comparisons. Floating point is
only a gate that can retain extra work. The two divisor-mode factorizations
are separately reconstructed by the standard-library Python checker.
