# List every cube of Kirtchakov's k(3,4) chain with its make_structured.py arguments,
# derived from verify_chain.py (I3L3, TT4F, cube_name) exactly as REGENERATE.md's regen_layer.py does.
import sys, os
sys.path.insert(0, os.getcwd())
from verify_chain import I3L3, TT4F, cube_name
for N in (21, 22, 23, 24):
    for p in range(max(0, N - 16), 9):
        for q in range(p, 9):
            s = N - 1 - p - q
            if not 0 <= s <= 7:
                continue
            for i, pf in enumerate(I3L3[p]):
                for j, qf in enumerate(I3L3[q]):
                    for k, sf in enumerate(TT4F[s]):
                        print(cube_name(N, p, q, s, i, j, k), N, p, q, s, pf, qf, sf)
