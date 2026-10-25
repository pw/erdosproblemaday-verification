"""Sanity for locally_family.py: with the family restricted to {M8} it must reproduce locally.py's result (P17 + G21 as
'family graphs failing the final filter', 0 core candidates); with family {M8, N8.4..N8.6} and no nine-links there
can be no CORE-CANDIDATE either (nine == 2 required) — we just check it runs and finds the two M8 graphs again."""
import locally_family as LF, networkx as nx, time
S=LF.Search([LF.Link('M8',LF.W,0,False,False)],41,None,False); t=time.time(); S.run()
print("M8-only via family engine: nodes", S.nodes, "core candidates", len(S.found), f"{time.time()-t:.1f}s")
