# Source under audit
- OpenAI, *Weighted dilation graphs, smooth shifted primes and totient fibers*, 24 September 2026. Family 011 of the 6 October 2026 release (the family's other PDF, *The Poisson–Dirichlet law for prime predecessors*, cites this paper's Theorems 3.5/4.1 as inputs and is NOT audited here).
- Path in github.com/openai/math (main, fetched 2026-10-11 18:02Z): `preprints/Weighted-Dilation-Graphs-Smooth-Shifted-Primes-and-Totient-Fibers-September-24-2026/paper.pdf`
- 68 pages, PDF page number = printed page number. SHA-256 in `../paper.sha256` (351692885d112277e969901e75fe56eeee0d263d5d5847d0b980fe2c8c7744c0). Companion PDF SHA-256 4b54d35506a1928022ac21e6d270d30f6533423ddc5990975270a1e39a87bce7.
- Local copies: `~/MathDyad/erdos821/openai-011/`; working dir `/tmp/oaimath/011/` (paper.txt = `pdftotext -layout`, paper_plain.txt = plain).
- No Lean for this family in the release (`lean/formalization.yaml` has no entry; CONTENTS.md lists two PDFs only). Formal Conjectures: `FormalConjectures/ErdosProblems/821.lean` (snapshot in `../world/`).
