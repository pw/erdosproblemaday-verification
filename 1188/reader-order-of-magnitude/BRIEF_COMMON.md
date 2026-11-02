# Common brief: referee seats for reader submission 8gfcew (Erdős #1188)

Reader Pedro Martins submitted (2026-11-01) a claim to have SOLVED Erdős Problem #1188, with a 34-page preprint:
  src/minimal_covering_systems-1.pdf   (Zenodo 10.5281/zenodo.23427851, 16 Oct 2026; text in src/paper.txt via pdftotext -layout)
His submission text (row.json "body") summarises it. Problem as worded on erdosproblems.com/1188:
  F(x) = number of minimal distinct covering systems with all moduli in [1,x]: classes a_i mod n_i, distinct moduli
  1 < n_1 < ... < n_k <= x, union = Z, no proper subfamily covers Z. Same moduli + different residues count separately.
  Estimate F(x). Known before: F -> infinity (Hough), F >> log x (van Doorn), F >= exp((log x)^{3-o(1)}) (BBMST, JEMS 2024),
  trivially log F = O(x log x).
His claims: log F(x) = Theta(x log x), precisely (c1+o(1)) x log x <= log F(x) <= (1-log 2) x log x + 1.5x (all x>=2), c1 = 0.0672.

Your job is to REFUTE, not to confirm. Read the actual proofs. When you object, QUOTE the sentence you object to and cite the
PRINTED theorem/section/page number. pdftotext garbles formulas (drops overlines, flattens subscripts/parentheses):
before you file any defect that rests on a formula, render that page (`pdftoppm -f N -l N -r 150 -png src/minimal_covering_systems-1.pdf /tmp/<you>_pN`)
and read the image. A disagreement between the paper and its own displayed formula means suspect the extraction first.

Rules of the box (shared 16-core machine; two long-running cadical solvers belong to someone else, never touch them):
 - every scratch script runs as: nice -n 19 bash -c 'ulimit -v 8000000; exec timeout 3600 python3 script.py'
   (timeout bounds time, ulimit bounds memory; unbounded memoisation is the usual way to blow the box up)
 - at most 3 concurrent processes of yours; no SAT campaigns longer than 30 minutes; no Lean builds.
 - work only inside your seat directory referee/<SEAT>/ (scratch/ subdir for code). Do not edit anything outside it.
 - a checker you write must have a POSITIVE control (accepts a known-good object, e.g. the minimal distinct covering
   system {0 mod 2, 0 mod 3, 1 mod 4, 5 mod 6, 7 mod 12}) and a NEGATIVE control (rejects a known-bad one, e.g. drop a
   class, or add a redundant one) and you must show both outputs in your report.

Deliverable: referee/<SEAT>/REPORT.md with
  VERDICT: HOLDS | HOLDS WITH NOTES | GAP | FALSE   (for YOUR scope only)
  then: each finding with severity (fatal / gap / slip / exposition), the quoted sentence, printed location, and why;
  then: what you checked and how (scripts, outputs, controls), so another reader can reproduce it.
Finish with a 5-line summary as your final message.
