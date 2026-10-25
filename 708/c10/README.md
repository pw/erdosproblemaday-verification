# Problem 708: verification for `c_10 = 2`

This bundle supports the exact sibling constant

```text
c_10 = 2.
```

The parent conjecture `g(n) <= 2n` remains open.

The proof has two parts:

- [`c10_proof.md`](c10_proof.md) proves the generic interval case and records
  the graph classifications, layer repairs, exceptional `K_2,5` argument,
  and placement lemmas.
- [`c10_aligned_repair.md`](c10_aligned_repair.md) supplies the aligned
  endpoint case. It deliberately replaces a failed first draft which tried
  to count the midpoint's prime powers twice.

The hostile audit preserves an explicit counterexample to that failed
inference, then independently verifies the replacement. The combined proof
passes after two small generic-text corrections incorporated in the public
copy: the 12 same-column `K_3,4` deletion patterns are redundant rather than
minimal, and the missing `n_2=n_3=0` subcase in the `K_2,5` placement proof is
handled by taking `m_0=1`.

Run the finite checks with:

```bash
python3 verify_c10_graph_layers.py
python3 verify_c10_aligned_repair.py
python3 verify_c10_cold_audit.py
```

The checkers cover the finite graph classifications, arbitrary-support block
certificates, capped valuation stress tests, exceptional aligned two-adic
layers, interval progression phases, and literal small instances. The written
prime-power layer arguments cover unbounded valuations; the finite loops do
not replace those proofs.

The parent directory's `verify_cn_ge_2_padding.py` now checks the sharp lower
construction through `n=10`. Its concrete ten-label instance has exact minimum
cover size 11 in the bad interval.
