#!/usr/bin/env python3
"""Third instrument (labelled as such): per-host target and SOS coefficients from MY implementation versus the
author's verify_clebsch_tangent_certificate.py functions (loaded by path, run with python -I). Author's values are
x720-normalised sums over orderings divided by 720."""
import importlib.util, sys, json
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/erdos1800/seats/cert'); import myverify as mv
spec = importlib.util.spec_from_file_location('author', '/tmp/erdos1800/claim/erdos-128-sparse-halves/verify_clebsch_tangent_certificate.py')
au = importlib.util.module_from_spec(spec); spec.loader.exec_module(au)
import networkx as nx
eps, terms = mv.load_cert()
graphs = [nx.from_graph6_bytes(c.encode()) for c in au.HOST_GRAPH6]
ahosts = [au.adjacency(g) for g in graphs]
idx = au.collect_flag_indices(ahosts)
C = mv.coords()
# my adjacency for the same labelled hosts
myhosts = [[[1 if (a[u] >> v) & 1 else 0 for v in range(6)] for u in range(6)] for a in ahosts]
E = mv.Expansion(myhosts, C)
bad_t = bad_s = 0
for h, a in enumerate(ahosts):
    mats = au.host_moment_counts(a, idx)
    s_auth = sum(w * au.square_coefficient(mats[b], v) for b, w, v in terms)
    t_auth = au.target_coefficient(a, eps)
    c4, m3, rho = E.parts[h]
    t_mine = c4 - m3 + (Fr(3, 64) + eps) * rho
    s_mine = sum(w * mv.quad(E.G[h][b], v) for b, w, v in terms)
    bad_t += (t_auth != t_mine); bad_s += (s_auth != s_mine)
    # per-term, per-block agreement too
    for b, w, v in terms:
        assert au.square_coefficient(mats[b], v) == mv.quad(E.G[h][b], v), (h, b)
print(f'per-host target coefficient: author == mine on {38 - bad_t}/38 hosts')
print(f'per-host SOS coefficient   : author == mine on {38 - bad_s}/38 hosts (and per term on all 34x38 pairs)')
