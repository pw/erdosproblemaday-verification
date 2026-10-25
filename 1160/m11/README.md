# Problem 1160 at m=11

This directory preserves the corrected author certificate and a hostile
independent audit for the finite statement

```text
sum_{1 <= n < 2048} g(n) = 49,910,538,480
                         < 1,774,274,116,992,170
                         <= g(2048).
```

It proves the stronger conjecture in Question 22.18 at `m=11`, and therefore
the original Problem 1160 inequality for every `n <= 2048`. It does not
determine `g(2048)`, prove the statement at `m >= 12`, or settle the
asymptotic problem.

- `author/` is the corrected v2 bundle. Its manifest SHA-256 is
  `8cb5c802c759c3a2dc12fd3e203e00abb991bfaae5376e44ebaa71e48da6dd90`.
- `hostile_audit/` independently reconstructs the counts and checks the
  source semantics. Its manifest SHA-256 is
  `10c9777020e0ebe40fdc7f893f242a14d78fb245625bedd9b17d2e90ad07c5bc`.

Run `./reproduce.sh` to verify both frozen bundles and rerun their portable
checks.
