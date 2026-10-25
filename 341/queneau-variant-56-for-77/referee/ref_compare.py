#!/usr/bin/env python3
"""Compare a greedy output file with a closed-form file (both: one integer per line, <= LIMIT).
Prints the first offending integer (smallest t in the symmetric difference) or MATCH.
Exit 0 = match, 1 = mismatch, 2 = cannot see (empty / limit not reached)."""
import sys
g_path, c_path, L = sys.argv[1], sys.argv[2], int(sys.argv[3])
G = [int(x) for x in open(g_path)]
C = [int(x) for x in open(c_path)]
if not G or not C:
    print("CANNOT SEE: empty input"); sys.exit(2)
G = [x for x in G if x <= L]; C = [x for x in C if x <= L]
if max(G) < L - 1000 or max(C) < L - 1000:
    print(f"CANNOT SEE: max greedy {max(G)}, max closed {max(C)} far below limit {L}"); sys.exit(2)
sg, sc = set(G), set(C)
diff = sorted(sg ^ sc)
if not diff:
    print(f"MATCH on [1,{L}]: {len(G)} elements, last {G[-1]}"); sys.exit(0)
t = diff[0]
print(f"MISMATCH on [1,{L}]: {len(diff)} differing integers; first offending t = {t} "
      f"(in greedy: {t in sg}, in closed form: {t in sc}); t = 49*{t//49} + {t%49}")
sys.exit(1)
