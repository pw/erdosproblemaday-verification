#!/usr/bin/env python3
"""How robust is PROOF.md's census criterion 'no period <= 8,192 on [16,384, 32,768)' for the PROVED seed?
Apply that criterion (smallest P <= Pmax with W[q] == W[q+P] for all q in [lo, Q-P)) to the closed-form rails of
Theorem 1 (rule Q) and Theorem 2 (rule D), with window start lo = 16384 and lo = 16385."""
import importlib.util, sys
spec = importlib.util.spec_from_file_location('cf', 'ref_closed_form.py'); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
Q, Pmax = 32768, 8192
for kind in ('Q', 'D'):
    Y0, Y1, Y2 = cf.controller(kind, Q)
    W = [(q in Y0) | ((q in Y1) << 1) | ((q in Y2) << 2) for q in range(Q)]
    for lo in (16384, 16385):
        per = next((P for P in range(1, Pmax + 1) if all(W[q] == W[q + P] for q in range(lo, Q - P))), 0)
        distinct = sorted(set(W[lo:Q]))
        print(f"controller {kind}: window [{lo},{Q}): smallest period <= {Pmax} = {per or 'none'}; "
              f"distinct rail patterns in window = {distinct}; positions where W changes: "
              f"{[q for q in range(lo+1, Q) if W[q] != W[q-1]]}")
