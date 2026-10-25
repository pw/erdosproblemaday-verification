# Provenance

All access and computation dates below are 2026-08-11 UTC.

## Live problem page

provenance/bright196.txt is the rendered text obtained through the Bright Data browser path from:

https://www.erdosproblems.com/196

It records OPEN, zero claimed proofs, no current worker, Adenwalla interested in collaborating,
three comments, and a formalised statement. provenance/bright196forum.txt is the rendered discussion
thread and includes the 2025 clarification of the monotonicity convention:

https://www.erdosproblems.com/forum/discuss/196

The captures are evidence of the displayed state at access time, not a continuing status guarantee.

## Local collision gate

provenance/site_index_20260811.js and provenance/site_ledger_data_20260811.js are byte-for-byte
snapshots of:

/home/exedev/ErdosProblemADay/src/index.js
/home/exedev/ErdosProblemADay/src/ledger_data.js

Their expected hashes are embedded in code/audit_site_collision.py and independently recorded in
MANIFEST.sha256. The checker parses only structured n:, problem:, and Erdos-problem URL fields and
also checks the exact framework phrase list stated in REPORT.md.

## Primary sources

1. J. A. Davis, R. C. Entringer, R. L. Graham, G. J. Simmons, On permutations containing no long
   arithmetic progressions, Acta Arithmetica 34 (1977), 81-90.
   Locator: https://doi.org/10.4064/aa-34-1-81-90
   Frozen file: sources/degs1977.pdf

   This PDF is scanned. sources/degs1977_ocr_scan_1.txt lines 30-38 distinguish the doubly infinite
   four-term construction from the finite M(n) count for three terms. OCR scan 5 lines 44-51 states
   the singly infinite four-term question. The PDF image is authoritative because OCR symbols are
   noisy.

2. Timothy D. LeSaulnier and Sujith Vijay, On Permutations Avoiding Short Progressions, arXiv
   1004.1740; Discrete Mathematics 311 (2011), 205-207.
   Locator: https://arxiv.org/abs/1004.1740
   Frozen file: sources/lesaulnier_vijay_2010.pdf

   Extracted-text lines 54-65 state that the unrestricted four-term question remains open and prove
   odd-common-difference avoidance. The exact finite values on lines 49-51 are M(n) for three-term
   avoidance, not theta_4(n).

3. Jesse Geneson, Forbidden arithmetic progressions in permutations of subsets of the integers,
   arXiv 1803.06334; Discrete Mathematics 342 (2019), 1489-1491.
   Locator: https://arxiv.org/abs/1803.06334
   Frozen file: sources/geneson_2018.pdf

   Extracted-text lines 178-204 define theta_k(n) and prove recursive lower bounds. Lines 335-340
   retain the positive-integer four-term question as open.

4. Sarosh Adenwalla, Avoiding Monotone Arithmetic Progressions in Permutations of Integers, arXiv
   2211.04451 v7; Discrete Mathematics 347 (2024), article 114183.
   Locator: https://arxiv.org/abs/2211.04451
   Frozen file: sources/adenwalla_2024.pdf

   Extracted-text lines 65-76 summarize restricted-difference and doubly infinite results. Lines
   903-915 explicitly list the positive-integer four-term question as open.

5. Collier Gaiser and Paul Horn, Subsequence Sums in Permutations, arXiv 2605.29011, submitted
   27 May 2026.
   Locator: https://arxiv.org/abs/2605.29011
   Frozen file: sources/gaiser_horn_2026.pdf

   Extracted-text lines 115-123 say that the monotone four-term positive-integer question remains
   unknown after the recent work cited there.

The extracted .txt files were generated with Poppler pdftotext 24.02.0. The six DEGS OCR derivatives
were generated from 250-DPI page images with Tesseract 5.3.4, page segmentation mode 3.

## Negative sequence/literature search

Searches used exact initial and tail fragments of the computed table, theta_4(n), and the quoted
definition of monotone four-term AP avoidance. Web-indexed OEIS searches returned no match. Direct
OEIS access was blocked by its automated-access controls in this environment. These are negative
search observations only; they do not establish priority or definitive absence.

The inspected primary-source chain spans the foundational 1977 paper, the 2011/2019/2024 papers
cited by current work, and a May 2026 paper explicitly describing the problem as unknown.
