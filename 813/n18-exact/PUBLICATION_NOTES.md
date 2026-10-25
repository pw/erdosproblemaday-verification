# Publication handoff

## Theorem text

Let `h(n)` be the least clique order forced in every `n`-vertex graph in
which every seven vertices contain a triangle.  Then

\[
h(18)=5.
\]

Indeed, an 18-vertex graph witnessing `h(18)<=5` was already checked in the
earlier bundle.  For the reverse inequality, assume a K5-free graph `G` in
which every seven vertices contain a triangle.  A Brooks-colouring argument
gives `Delta(G)>=7`.  Complete neighbourhood censuses exclude degrees at
least 13, and two independent solvers exclude degrees 11 and 12.  If
`7<=d<=12`, four independent neighbours of a maximum-degree root would force
its non-neighbours to be a clique, hence `alpha(G[N(v)])<=3`.  For `d>=9`,
`R(4,3)=9` further gives independence number at most two in the root
non-neighbour graph.  Exact canonical splits then leave 353 cases for d=7,
1,829 for d=8, 179x8,753=1,566,787 for d=9, and
71x8,688=616,848 for d=10.  CaDiCaL returned UNSAT in every case, and exact
coverage auditors found no missing or duplicate index.  Thus no possible
maximum degree remains.

## Required confidence label

Use **PROVED (computer-assisted; solver assertions)** or equivalent wording.
Do not call the full result proof-certificate verified.  The reductions,
censuses, CNF semantics, and exact case coverage are independently audited;
four difficult cases have replayed DRAT proofs.  The complete d=7--d=10
sweeps and the earlier d=11/d=12 sweeps are solver assertions without a
retained proof certificate for every branch.

## Site integration targets

- Replace the `n:813` ledger entry in
  `/home/exedev/ErdosProblemADay/src/ledger_data.js` (currently near line
  333): change verdict `PARTIAL` to `PROVED`, change the gist to the exact
  value with the certificate caveat, and replace the old `4<=h(18)<=5`
  conclusion and `7<=Delta<=10` wall with the theorem and branch table in
  `REPORT.md`.
- Add a clean verification directory such as
  `/home/exedev/ErdosProblemADay/verification/813/n18-exact/`.  The compact
  publication core is `REPORT.md`, `DELTA7_PROOF.md`, `DELTA7_CHECK.py`, the
  files in `tools/`, `branches/`, and `censuses/`, the four audit logs, and
  `MANIFEST.sha256`.  The full raw logs are large and may be distributed as a
  compressed artifact instead of committed individually.
- Keep the existing
  `/home/exedev/ErdosProblemADay/verification/813/n18-degree10/` bundle as the
  prior-stage audit, and link to it for the d=11/d=12 and order-13 census
  results.  A frozen copy is included here under `prior_delta10/`.

No repository files were modified by this handoff.
