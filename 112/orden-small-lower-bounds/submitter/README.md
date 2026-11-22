# New lower bounds for small Erdős-Rado numbers k(7,3), k(8,3), k(6,4) and k(3,6) (Erdős problem #112)

**Author:** Tyler Satchel Orden, Independent researcher, ORCID 0009-0004-9205-7422.

## The problem

k(n,m) = r(I_n, L_m) is the least k such that every oriented graph on k vertices contains n pairwise non-adjacent vertices (an independent set of size n) or a transitive tournament on m vertices. Erdős problem #112, after Erdős and Rado, asks for these numbers. An oriented graph has no loops and at most one arc between any two vertices. For m = 3 a transitive tournament is a transitive triangle x -> y, y -> z, x -> z.

So an oriented graph on N vertices with no independent set of size n and no transitive tournament on m vertices shows k(n,m) >= N + 1. Each result below is such a graph.

## Results

| Bound | Witness | Vertices, arcs | Previous best public bound |
|---|---|---|---|
| k(7,3) >= 39 | witness_k73_ge39_N38 (bicirculant on Z_19 x {0,1}) | 38, 228 | 37 |
| k(8,3) >= 47 | witness_k83_ge47_N46 (bicirculant on Z_23 x {0,1}) | 46, 322 | 46 |
| k(6,4) >= 78 | witness_k64_ge78_N77 (circulant on Z_77) | 77, 1232 | 65 |
| k(3,6) >= 71 | witness_k36_ge71_N70 (circulant on Z_70) | 70, 1610 | 68 |
| k(3,6) >= 70 | witness_k36_ge70_N69 (circulant on Z_69; a second, weaker witness) | 69, 1656 | 68 |

These are new lower bounds. The previous best public bounds were 37, 46, 65 and 68, all from one repository (see "Previous bounds" below). The known upper bounds for m = 3 are k(7,3) <= 45 and k(8,3) <= 59 (k(n,3) <= n^2 - n + 3, Ihringer, Rajendraprasad and Weinert, 2021).

What each witness satisfies, as computed by both checkers (checks.out):

| Witness | Largest independent set | Largest transitive tournament | Degrees |
|---|---|---|---|
| N38 for k(7,3) | 6 | 2 (no transitive triangle) | in and out 6 |
| N46 for k(8,3) | 7 | 2 (no transitive triangle) | in and out 7 |
| N77 for k(6,4) | 5 | 3 | in and out 16 |
| N70 for k(3,6) | 2 | 5 | in and out 23 |
| N69 for k(3,6) | 2 | 5 | in and out 24 |

## The witnesses

Each witness is defined by connection sets. The file `<name>.def.txt` gives the definition; `<name>.txt` is the arc list.

- **witness_k73_ge39_N38.** Vertices Z_19 x {0,1}; vertex (x,i) is numbered 19i + x. Arc (x,i) -> (x+s mod 19, j) for every s in S_ij, with S_00 = {5, 6, 16, 17}, S_01 = {16, 17}, S_10 = {5, 6}, S_11 = {10, 11, 16, 17}.
- **witness_k83_ge47_N46.** Vertices Z_23 x {0,1}; vertex (x,i) is numbered 23i + x. Arc (x,i) -> (x+s mod 23, j) for every s in S_ij, with S_00 = {2, 5, 11, 19}, S_01 = {4, 10, 18}, S_10 = {0, 8, 17}, S_11 = {2, 11, 19, 20}.
- **witness_k64_ge78_N77.** Vertices Z_77; arc x -> x+s mod 77 for every s in S = {3, 11, 14, 19, 20, 22, 30, 35, 36, 40, 44, 46, 52, 64, 68, 75} (16 elements).
- **witness_k36_ge71_N70.** Vertices Z_70; arc x -> x+s mod 70 for every s in S = {1, 2, 7, 8, 14, 15, 16, 17, 21, 24, 26, 29, 30, 32, 37, 39, 45, 47, 48, 52, 60, 61, 64} (23 elements).
- **witness_k36_ge70_N69.** Vertices Z_69; arc x -> x+s mod 69 for every s in S = {16, 19, 27, 30, 32, 33, 35, 41, 43, 44, 46, 48, 49, 51, 55, 57, 58, 59, 60, 62, 63, 64, 65, 67} (24 elements).

In each circulant, S and -S are disjoint, so the graph is oriented. The checkers test this for every graph anyway.

**Arc list format.** Plain text. The first line is "N A": N vertices, numbered 0 to N-1, and A arcs. Then A lines "u v", each meaning the arc u -> v. Vertices are 0-indexed, lines are sorted, and there are no comments.

## How to check (a few seconds)

You need a C compiler and Python 3; no libraries.

```
sh run_checks.sh > my_checks.out 2>&1
diff my_checks.out checks.out
```

run_checks.sh (1) rebuilds every arc list from its connection sets with build_witnesses.py and compares it with the file in this folder; (2) runs knm_check.c on each witness (each must PASS); (3) runs negative controls, the same graphs tested for a smaller n or m, and one graph with an extra arc (each must FAIL); (4) runs positive controls, three published graphs (each must PASS); (5) runs second_check.py on each witness.

One witness at a time:

```
cc -O2 -o knm_check knm_check.c
./knm_check 38 7 3 witness_k73_ge39_N38.txt
python3 -I second_check.py 38 7 3 witness_k73_ge39_N38.txt
```

The arguments are N, n, m and the arc list.

The two checkers were written separately, from the definition only, and share no code with each other or with the search programs:
- **knm_check.c** checks that the graph is oriented (no loop, no 2-cycle, no repeated arc). It computes the exact independence number by branch and bound, and the exact size of the largest transitive subtournament by extending chains from their unique source. It also counts transitive triangles directly. Exit code 0 means PASS.
- **second_check.py** checks orientedness again. It then counts, by plain enumeration with no bounding, all independent sets of sizes n-1 and n and all transitive tournaments on m-1 and m vertices. A witness needs 0 independent n-sets and 0 transitive m-tournaments.

The positive controls are Bermond's 8-vertex graph (k(3,3) >= 9), the 14-vertex graph of Ihringer, Rajendraprasad and Weinert (k(4,3) >= 15) and Kirtchakov's 28-vertex circulant (k(6,3) >= 29).

Both checkers read the header line "N A" and stop with an error if it does not match. The header reading was added on 2026-11-20 for this record; nothing else in the checkers changed.

## Previous bounds and their sources

- **k(7,3) >= 37, k(8,3) >= 46, k(6,4) >= 65, k(3,6) >= 68:** rsvaultpudgy-create, "erdos-112-lower-bounds", GitHub repository, https://github.com/rsvaultpudgy-create/erdos-112-lower-bounds. It has a single commit (d305711817), dated 11 November 2026. Its description reads "AI-generated, unrefereed". Its witnesses are circulants on 36, 45, 64 and 67 vertices. Read through the GitHub API on 19 and 20 November 2026; there were no later commits.
- **k(6,3):** 29 <= k(6,3) (D. Kirtchakov, Zenodo, 11 August 2026, https://doi.org/10.5281/zenodo.21890619; this record also determines k(3,4) = 21). Then 30 <= k(6,3) <= 32 (T. S. Orden, https://doi.org/10.5281/zenodo.24064871; Lean 4 proof, https://doi.org/10.5281/zenodo.24237180).
- **Upper bounds for m = 3:** k(n,3) <= n^2 - n + 3 (F. Ihringer, D. Rajendraprasad and T. Weinert, New bounds on the Ramsey number r(I_m, L_n), Discrete Math. 344(3) (2021) 112268, https://doi.org/10.1016/j.disc.2020.112268).
- **Other sources searched, 19 and 20 November 2026:** Zenodo records through DataCite, GitHub, OpenAlex, the plasma-ai Erdős problems ledger, a web search, and the erdosproblems.com forum thread for problem #112 (https://www.erdosproblems.com/forum/thread/112, read by the author on 20 November 2026). None gave a bound for these four cases above the ones listed here.

## Provenance

The graphs were found by computer searches run by AI agents (Claude, Anthropic) under the author's direction, on a second machine. They were checked here by two separately written programs. The arc lists in this record were rebuilt from the connection sets by build_witnesses.py, and they match the search output arc for arc.

This record has not been peer reviewed.

It contains no Lean files. A Lean build of these bounds on this machine has not been done.

## Files

| File | What it is |
|---|---|
| README.md | this file |
| witness_*.txt (not .def.txt) | the five arc lists |
| witness_*.def.txt | the connection-set definition of each witness |
| control_*.txt, control_*.def.txt | three published graphs, used as positive controls |
| build_witnesses.py | builds every arc list from its connection sets |
| knm_check.c | checker 1 (C) |
| second_check.py | checker 2 (Python, no libraries) |
| run_checks.sh | runs everything |
| checks.out | output of run_checks.sh, 2026-11-20 |
| LICENSE_MIT.txt | license of the code |
| SHA256SUMS.txt | SHA-256 of every other file |

## AI disclosure

Claude (Anthropic), a large language model, assisted this work under my direction: it ran the computer searches that found the graphs, wrote the code that rebuilds and checks them, checked the graphs and the literature, and assisted with the writing throughout; the text is my own and I take full responsibility for it.

## License

The data and text are CC BY 4.0. The code (build_witnesses.py, knm_check.c, second_check.py, run_checks.sh) is MIT; see LICENSE_MIT.txt.

## Other references

- J.-C. Bermond, Some Ramsey numbers for directed graphs, Discrete Math. 9(4) (1974) 313-321, https://doi.org/10.1016/0012-365X(74)90077-6.
- Erdős problem #112, https://www.erdosproblems.com/112.
