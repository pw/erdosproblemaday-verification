# Problem 708: verification for `c_11 = 2`

This bundle supports the exact sibling constant

```text
c_11 = 2.
```

The parent conjecture `g(n) <= 2n` remains open.

The written proof is [`c11_proof.md`](c11_proof.md). It depends on the
published `c_10` package in the parent directory and adds three new pieces:

- [`c11_new_kernels.md`](c11_new_kernels.md) classifies the eleven-edge
  two- and three-defect cores and gives their prime-power support blocks.
- [`c11_placement_lemma.md`](c11_placement_lemma.md) proves the four-factor
  Rado placement needed for `K_3,4-e`.
- The integrated proof supplies the joint endpoint/repair Hall argument and
  the aligned exceptional-matching step.

The mathematical snapshot audited independently has SHA-256
`6a49dabc87e9020446490ab6b1ce54215ce6f9c1fe2534e739d7b2eb1c9c4f6c`.
It is preserved byte-for-byte at
[`audit/inputs/erdos708_c11_candidate.md`](audit/inputs/erdos708_c11_candidate.md).
The public proof changes only its title/status and closes two omitted display
math delimiters; its mathematical text is otherwise identical.

Run the finite checks with:

```bash
python3 verify_c11_placement.py
python3 verify_c11_new_kernels.py
python3 verify_c11_full.py
python3 verify_c11_independent.py
```

[`audit/AUDIT_REPORT.md`](audit/AUDIT_REPORT.md) records the integrated hostile
PASS. The complete frozen audit lives under [`audit/`](audit/), including its
own manifest, original filenames, inputs, logs, and `run_all.sh`. Its
independent checker reconstructs the inherited cores, exhausts the abstract
Hall contraction, verifies the aligned support certificates, and rebuilds an
exact seven-private-prime lower instance. The 907 minimal-core exceptional
matchings versus the supplied checker's 954 are fully reconciled: the extra
47 are redundant same-column controls containing a smaller `K_3,3` core.

[`audit/LOWER_BOUND_PROVENANCE.md`](audit/LOWER_BOUND_PROVENANCE.md) spells out
the prime-number-theorem choice which makes the private-prime construction
tend to ratio two for every fixed number of padding primes. Its sentence that
the then-public smoke verifier stopped at `n=10` is frozen audit history; this
promotion extends that verifier through `n=11`. The finite instance is
corroboration, not the limiting argument.

The top-level filenames are shorter public aliases. The exact historical
`erdos708_c11_*` names referenced by the proof and companion reports are
preserved under `audit/inputs/`.

The graph programs are finite structural certificates and stress tests. The
written Hall, progression, Rado, prime-power layer, and PNT arguments cover
arbitrary intervals and valuations; bounded loops do not replace them.
