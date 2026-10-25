# Provenance search boundary

Access date: 2026-08-11 UTC

## Primary/current sources checked

- Live problem: <https://www.erdosproblems.com/86>
- Live forum: <https://www.erdosproblems.com/forum/thread/86>
- OEIS: <https://oeis.org/A245762>
- arXiv API and PDF: <https://arxiv.org/abs/2603.29127v4>
- Current public certificate repository:
  <https://github.com/rafalwronapl/erdos86-hypercube-c4>

The live pages were captured independently through a rendered browser. The
OEIS b-file and arXiv API/PDF were fetched directly. The GitHub repository was
freshly cloned and `git ls-remote` was checked independently.

## Exact searches

General web searches included:

```text
"1506" "Q9" "C4-free" hypercube
"1506 edges" hypercube C4
"ex(Q_9,C_4)" 1506
"883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c"
site:github.com "q9_edges_1506"
```

Authenticated GitHub code searches included:

```text
"1506" "C4-free" hypercube
q9_edges_1506
883919d0e3c7d571aadd920ad539667338dfdb74efa24e61808fb41754db573c
```

The frozen GitHub JSON outputs are all empty arrays. General search returned
no relevant 1506-edge Q9 construction. The exact witness hash returned no
indexed hit.

## Conclusions and limit

The current identified explicit-certificate baseline is Q9 with 1505 edges at
GitHub commit `74e84382cbbc20b32a2ac679bff977cad3ac5d24`, certificate SHA-256
`0994be825ec39d115b65eb1436eace7c1be324448a6ec116d69c8a7e2a75d338`.

OEIS does not provide an exact Q9 term, and Minamoto v4 stops its new finite
constructions at Q8. The live forum still reports Q9=1505.

This supports comparison with the identified public explicit 1505 frontier.
It does not establish unconditional novelty: search indexing is incomplete,
and private or unpublished constructions cannot be excluded.
