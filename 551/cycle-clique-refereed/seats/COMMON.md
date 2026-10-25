# Common brief — refereeing OpenAI's "Cycle–clique Ramsey numbers" (25 Sep 2026; Erdős #551, the Erdős–Faudree–Rousseau–Schelp conjecture)
You are a HOSTILE referee seat for erdosproblemaday.com (Patrick White + Claude). Your job is to REFUTE, not to admire.
Claim: R(C_m, K_n) = (m−1)(n−1)+1 for all m ≥ n ≥ 3 except (3,3) (where R = 6).
Materials (read-only; do not modify anything outside /tmp/oaimath/189/seats/):
- Paper PDF: /tmp/oaimath/189/paper.pdf (sha256 366fc1d9…, 41 pp). LaTeX source (easier to read, same text):
  /tmp/oaimath/189/repo/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/build/sections/*.tex
  PRINTED section numbers (cite THESE, never the .tex file names): §1 intro · §2 minimal counterexample (02-reduction.tex) ·
  §3 large clique (03-clique-layers.tex + 03-clique-rotations.tex; §3.1 paths of prescribed length, §3.2 closing through the BFS tree) ·
  §4 k = 3,4 (04-small.tex) · §5 from size to independence (05-size.tex) · §6 optimal path systems (06-paths.tex; §6.1, §6.2) ·
  §7 short paths between representatives (07-growth.tex) · §8 excluding large cliques (08-terminal.tex; §8.1–8.4) ·
  §9 finite path-system argument (09-finite-patterns.tex = §9.1, 09-finite-rules.tex = §9.2–9.3, 09-finite-packing.tex = §9.4–9.5,
  09-finite-results.tex = §9.6) · Appendix A implementations (10-implementation.tex). Lemma numbers: take them from the PDF
  (pdftotext text at /tmp/oaimath/189/paper.txt; when a formula looks garbled render the page:
  `pdftoppm -f N -l N -r 110 -png /tmp/oaimath/189/paper.pdf /tmp/oaimath/189/seats/pg` and look before filing anything).
- Verification code + data: /tmp/oaimath/189/repo/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/verification/ (two Python checkers,
  certificates.jsonl, expected-output.txt). The main seat is ALREADY running `verify.py` (both checkers, unmodified) in /tmp/oaimath/189/finite/run1 —
  do not re-run that whole thing; you may run modified COPIES in your own directory.
- OpenAI's Lean formalization: /tmp/oaimath/189/repo/lean/OAI/Combinatorics/Ramsey/CycleClique/ (443 files); comparator
  /tmp/oaimath/189/repo/lean/ComparatorChallenges/CycleCliqueRamsey.lean. A kernel replay is being run separately by the main seat — do NOT build anything.
- The main seat has ALREADY read §2, §3 and §4 line by line and found them correct; you need not repeat that unless your section depends on a
  precise statement there (then quote the statement you rely on).
Rules:
- Every objection QUOTES the sentence it objects to and says exactly what is wrong and whether it is FATAL (the theorem fails as proved),
  a GAP (a step not justified as written but plausibly fixable — say how), or EXPOSITION (wording only).
- Verdict line at the top of your report: HOLDS AS READ / HOLDS WITH FIXES / GAP AT <place> / COULD NOT CHECK <what>.
- Small computations are welcome (python3, networkx, sympy installed; pysat if present); every script runs under
  `bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 …'`. One core at a time. No SAT campaigns, no Lean builds. Do not spawn sub-agents.
- Do not contact anyone or post anything. Write ONLY under /tmp/oaimath/189/seats/.
- Write your report to the path named in your seat brief AS YOU GO (partial reports are valuable if you are cut off), then reply with the verdict line
  + a 10-line summary.
