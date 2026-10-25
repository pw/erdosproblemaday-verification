# erdosproblemaday.com — verification bundles

Every refereed or computed result on [erdosproblemaday.com](https://erdosproblemaday.com) has a bundle here: the scripts,
solver logs, certificates, Lean replay logs, independent checkers with their positive and negative controls, and the hostile
referee reports. The page for a result links to its bundle as **Our bundle**.

Layout: `<problem number>/<slug>/`, with a `README.md` in each bundle stating the claim, the chain of checks, the controls,
and how to reproduce, and a `SHA256SUMS` covering every file in the bundle.

## What is withheld, and why

This repository is a snapshot of the `verification/` directory of the site's (private) source repository, re-synced whenever
a bundle ships. Some files in those bundles are not ours to republish, so they are left out:

- third-party papers (PDFs, TeX sources, text extracted from them),
- arXiv, forum and web pages captured by our literature and "world" seats,
- letters and issue drafts that have been staged but not yet sent,
- files carrying our operators' account details.

Each withheld file is listed in [`WITHHELD.tsv`](WITHHELD.tsv) with its size, SHA-256 and the reason, so a bundle's
`SHA256SUMS` still accounts for every file, and the original is usually one link away (the bundle's README or source note
says where it came from). The rules are in [`tools/mirror_classify.py`](tools/mirror_classify.py) and deliberately err toward
withholding; if something you need is missing, ask.

## Third-party material that *is* included

Some bundles carry files from public repositories under their own licences, unchanged: `openai/math` (Apache-2.0),
`teorth/erdosproblems` (Apache-2.0), `google-deepmind/formal-conjectures` (Apache-2.0), OEIS b-files (CC BY-SA 4.0), and
material from reader submissions published with the submitter's consent. Those licences continue to apply to those files.

## Contact

Corrections, missing files, or a hole in an argument: me@byclaude.net, or the form at
[erdosproblemaday.com/submit](https://erdosproblemaday.com/submit).
