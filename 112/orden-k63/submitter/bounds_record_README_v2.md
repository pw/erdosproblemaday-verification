# New bounds on the Erdős-Rado number k(6,3): 30 <= k(6,3) <= 32 (Erdős problem #112)

**Author:** Tyler Satchel Orden, Independent researcher, ORCID 0009-0004-9205-7422.

k(n,m) = r(I_n, L_m) is the least k such that every oriented graph on k vertices contains n pairwise non-adjacent vertices or a transitive tournament on m vertices (for m = 3, a transitive triangle x -> y, y -> z, x -> z). Erdős problem #112 asks for its value. The known values k(3,3) = 9, k(4,3) = 15 and k(5,3) = 23 all equal n^2 - n + 3, which is also the best published upper bound (Ihringer, Rajendraprasad and Weinert, Discrete Math. 344 (2021) 112268); the best lower bound stated there for n = 6 is 18, and 26 follows at once from their 22-vertex graph plus a disjoint directed triangle. The best earlier lower bound is 29, due to Daniel Kirtchakov (Zenodo, 11 August 2026, https://doi.org/10.5281/zenodo.21890619), from the circulant Cay(Z_28, {3,8,10,12,17}), which our circulant search found independently on 7 November 2026 (his record is earlier); so the bounds before this record were 29 <= k(6,3) <= 33.

**This record shows 30 <= k(6,3) <= 32,** so the pattern n^2 - n + 3 fails at n = 6.
- Lower bound: witness_n29_m6_anneal.txt is an oriented graph on 29 vertices (140 arcs) with no transitive triangle and no 6 independent vertices. `python3 check_witness.py witness_n29_m6_anneal.txt` checks both exhaustively; witness_n29_m6_anneal.check.txt is the output of the original checker.
- Upper bound: PROOF.md, a counting argument on the lemmas of Ihringer, Rajendraprasad and Weinert plus one small computation (Lemma B: every {I_4, L_3}-free oriented graph on 14 vertices has all degrees 6), which verify_small.c reruns in seconds; lemmaA_nodeg6.log is a SAT cross-check of Lemma A. A separate AI agent (Claude) that had not written the proof checked it, found it correct and re-derived Lemma B three ways; the proof has not been peer reviewed.

**Disclosure:** Claude (Anthropic), a large language model, assisted this work under my direction: it wrote and ran the search and checking code, found the 29-vertex graph and the proof of the upper bound, checked both and the literature, and assisted with the writing throughout; the text is my own and I take full responsibility for it.

**License:** the data and text are CC BY 4.0; the code is MIT.
