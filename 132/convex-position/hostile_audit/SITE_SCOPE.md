# Live and site scope audit

Observation time: 2026-08-11 UTC.

## Live record

Fresh independent Jina-rendered retrievals were made from:

- `https://www.erdosproblems.com/132`
- `https://www.erdosproblems.com/latex/132`
- `https://www.erdosproblems.com/forum/thread/132`
- `https://www.erdosproblems.com/forum/thread/132/proof-claims`

Observed SHA-256 values:

- main Markdown: `c5d47165ac84b0096f8081b945815ef4bf50105d9edf67325065287e94f8f3f7`
- LaTeX Markdown: `8e495ad8213e91db759a4e498eec2966916bd2538ea15de164e4c2b30a14b140`
- discussion Markdown: `ec15a13fc103aa327af06d175c95e1e1550eb1ab880fcd11e429d1b3e38e560a`
- proof-claims Markdown:
  `b66320882e0e69f90a1ac266dc878c22ff961ae7a9404dcdee9678500c1ca961`

The main and proof-claim hashes are byte-identical to the input bundle's
same-day final rechecks.  They show `OPEN` and "No proof claims have been
submitted yet."  The live problem-page counter reports five informal comments;
these are not registered/dedicated proof claims.  The discussion includes
claims about finite small orders and a separate construction, but no registered
general proof.  Those comments are neither audited nor used here.

The live page already reports the Clemen--Dumitrescu--Liu convex partial
result.  This audit provides no reason for a site edit, status change, or
deployment.

## Local publication site

Repository: `/home/exedev/ErdosProblemADay`

At the independent check:

- HEAD: `953c5a50896d05fdec69f81ad8e5a8df976d63ce`
- `src/index.js` SHA-256:
  `b3d3d82d1606df0e5b340849f52e16656639053d7e16a1e7a13839aa103542a4`
- `src/ledger_data.js` SHA-256:
  `9ad7647dcd9ee51b2e08233e77d0a0c21b1321033b923c13ac50a563c6a9c052`
- worktree: both listed source files were already modified by unrelated work;
  an unrelated untracked verification directory was also present.

An independent structured-number and sentinel search found no Problem 132
object, `2505.04283`, theorem DOI, paper title, or defining non-diameter
phrasing in either file.  The one generic `distance multiplicity` occurrence
is in unrelated Problem 1207 material.

The input snapshot of `ledger_data.js` is still byte-identical.  Its
`index.js` snapshot has SHA-256
`08e988d080d5317adf768ba827b4f21397699b30d28cc749807616b6753a3b76`
and is no longer the current file, because unrelated site work advanced HEAD.
Both the frozen and current index inventories pass the no-132 search.

## Upstream problem database

Repository: `/home/exedev/erdos_scratch/upstream_erdosproblems`

- HEAD: `6929b78952e18c11d5cb28fe9438081ee1d49448`
- `data/problems.yaml` SHA-256:
  `10ab3644baed80fecabe3b32ecf334231b243acebdda5a2783fb8423350763b9`
- Problem 132 status: `open`
- OEIS field: `N/A`

## Scope boundary

The only approved mathematical sentence is `CLAIM.txt`.  In particular, do
not publish any of these conclusions:

- "Problem 132 is solved."
- "The theorem holds for arbitrary planar point sets."
- "The number of qualifying distances tends to infinity."
- "Every individual order n >= 7 remains open."
- "The audit proves two new distances beyond the diameter."

No site file was edited, committed, or deployed.
