# Problem 708 verification

The site article proves the sibling constants

```text
c_4 = c_5 = c_6 = c_7 = c_8 = c_9 = c_10 = c_11 = 2.
```

The parent conjecture `g(n) <= 2n` remains open. The upper proofs use the
interval injection of van Doorn, Li, and Tang
([arXiv:2603.28636](https://arxiv.org/abs/2603.28636)); the lower bounds use
the private-prime padding construction recorded in the article.

For the `c_9` step:

- `verify_c9_graph_layers.py` exhausts the seven-vertex graph classification,
  the fixed repair partitions, and the `K_3,3` layer certificate.
- `verify_c9_cold_audit.py` independently discovers valid repair partitions,
  checks 117,649 `K_3,3` valuation vectors, tests literal interval instances,
  and rebuilds the nine-point lower obstruction.
- `verify_c9_independent_audit.py` uses bit-mask graph representations and
  brute-force partition discovery; it checks 1,572,864 seven-vertex valuation
  vectors and 22,620 small arithmetic intervals.
- `verify_cn_ge_2_padding.py` exercises the private-prime construction through
  `n=11`, where its exact valuation DP finds minimum cover size 12.

For the new `c_10` step, see [`c10/README.md`](c10/README.md). Its proof and
three independent finite checkers cover the nested Hall reduction, all new
two- and three-defect graph kernels, the exceptional `K_2,5` repair, and the
corrected aligned-endpoint argument. The audit also preserves a counterexample
to an invalid first aligned draft and verifies the replacement.

For the new `c_11` step, see [`c11/README.md`](c11/README.md). It covers the
eleven-edge two- and three-defect classifications, the `K_3,4-e` Rado
placement, the joint endpoint/repair Hall contraction, and the aligned
exceptional-matching certificates. A separate hostile checker reconstructs
the inherited cores and the exact seven-private-prime lower instance.

Run the Round 6 through Round 8 checks with:

```bash
python3 verify_c9_graph_layers.py
python3 verify_c9_cold_audit.py
python3 verify_c9_independent_audit.py
python3 verify_cn_ge_2_padding.py
python3 c10/verify_c10_graph_layers.py
python3 c10/verify_c10_aligned_repair.py
python3 c10/verify_c10_cold_audit.py
python3 c11/verify_c11_placement.py
python3 c11/verify_c11_new_kernels.py
python3 c11/verify_c11_full.py
python3 c11/verify_c11_independent.py
```

The graph programs are finite structural certificates and stress tests. The
arbitrary-valuation and interval conclusions still rely on the written
prime-power layer and placement arguments in the article; the scripts do not
replace those proofs.
