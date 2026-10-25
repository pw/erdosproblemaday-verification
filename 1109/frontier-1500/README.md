# Problem 1109 exact frontier bundle

Frozen 2026-08-11. This bundle proves the next five record indices of OEIS
A392165 and the exact value of the squarefree-sumset extremal function through
1500:

```text
1255 -> 40
1277 -> 41
1293 -> 42
1335 -> 43
1407 -> 44
```

The full proof, novelty scope, witnesses, and source provenance are in
`erdos1109_exact_frontier_report.md`. The concise scratch-only publication
copy is `erdos1109_site_entry_draft_2026-08-11.md`.

Three exact clique implementations support the finite upper bounds:

* custom C++ coloring search: 41,526,965 nodes, all prefixes through 1500;
* Ubuntu Cliquer 1.21: all 163 eligible last-vertex decisions after 1103,
  digest `6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84`;
* official PMC commit `06594a0ee1cde5a04f1679aff28072668da96062`:
  the same 163 decisions, digest
  `cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3`.

`check_1109_external_audits.py` cold-regenerates every graph in both external
formats, checks all hashes and witnesses, recomputes both digests, and compares
all decisions with the primary log. The recorded run exited 0.

Run the fast integrity and cold audit (about 30 seconds on the original VM):

```sh
./reproduce_1109.sh quick
```

`primary`, `pmc`, `cliquer`, `sanitizer`, and `all` modes perform progressively
more expensive fresh solver runs. The all-reverse Cliquer reproduction can
take hours depending on ordering and hardware.

`erdos1109_manifest_2026-08-11.sha256` covers every frozen file in the bundle
except the manifest itself. The `order_races` directory is non-load-bearing
operational provenance; its own README distinguishes the one completed exact
alternate run from races cancelled after the matching reverse result landed.

This is an exact finite extension only. Problem 1109's asymptotic question
remains open, and the ErdosProblemADay site had already attempted it on
2026-07-24.

