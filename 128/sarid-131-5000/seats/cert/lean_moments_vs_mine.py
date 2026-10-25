#!/usr/bin/env python3
"""Lean's literal per-host moment tables (HostChecks/Host{k}.lean, hostTables{k}, entries <i,j,count over 720 orders>)
versus 720 x the SYMMETRISED Gram matrices of MY implementation (u4: average over all canonical assignments, no
tie-break).  Entrywise equality for u4 is a sharper test of the tie-break-uniformity argument (REPORT F2) than
agreement of quadratic forms."""
import re, sys
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/erdos1800/seats/cert'); import myverify as mv
D = '/tmp/erdos1800/claim/erdos-128-sparse-halves/lean/Erdos128/C4Certificate/'
hd = open(D + 'HostData.lean').read()
masks = [int(x) for x in re.search(r'def hostMasks : List Nat := \[([^\]]*)\]', hd).group(1).split(',')]
order = ['s0_root0', 's2_root0', 's2_root1', 'u4_root0', 'u4_root1', 'u4_root3', 'u4_root7', 'u4_root12', 'u4_root13', 'u4_root30']
C = mv.coords()
tot_entries = bad = 0; nz = 0
for k, m in enumerate(masks):
    src = open(D + f'HostChecks/Host{k}.lean').read()
    body = src[src.index(f'def hostTables{k} : MomentTables := mkMomentTables'):]
    body = body[:body.index('theorem')]
    lists = re.findall(r'\[([^\[\]]*)\]', body)
    assert len(lists) == 10, (k, len(lists))
    thm = re.search(rf'theorem momentTables_host{k} : momentTables \(maskOfNat (\d+)\) = hostTables{k}', src)
    assert thm and int(thm.group(1)) == m
    adj = mv.adj_from_mask(m, 6)
    for b, L in zip(order, lists):
        lean = {}
        for i, j, c in re.findall(r'⟨\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*⟩', L):
            lean[(int(i), int(j))] = int(c)
        G = mv.square_matrix(adj, b, C); n = len(G)
        for i in range(n):
            for j in range(n):
                mine = (G[i][j] + G[j][i]) / 2 * 720
                tot_entries += 1
                if mine != lean.get((i, j), 0): bad += 1
                if mine: nz += 1
print(f'hosts parsed: {len(masks)}; matrix entries compared: {tot_entries} (nonzero {nz}); mismatches: {bad}')
