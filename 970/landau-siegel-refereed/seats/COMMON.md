# Common rules for every seat (erdos cron, 2026-10-26 09Z tick) — read before your own brief

Object under review: OpenAI, "Uniform exclusion of Landau–Siegel zeros" (preprint dated 1 Oct 2026, 9 pp., openai/math @1581d4c,
family 003). Claim (Theorem 1): there is an absolute c > 0 such that every real zero β ∈ (0,1) of every primitive nonprincipal real
Dirichlet L-function of conductor q ≥ 3 satisfies (1−β) log q ≥ c. If true this is one of the largest results in analytic number
theory in decades, so the default stance is DISBELIEF: your job is to find what is wrong, and to say plainly if you cannot.

Two of our published pages (erdosproblemaday.com, Erdős #970 and #431) rest on a Lean theorem from this family,
`OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound`. On 2026-10-23 our kernel accepted that proof term against a statement
we wrote (std axioms only). Nobody here has refereed the PAPER or audited the DEFINITIONS. That is this tick.

## Files (read-only unless it is your own work dir)
- PDF: /tmp/oaimath/003/paper/paper.pdf · text: /tmp/oaimath/003/paper/paper.txt (pdftotext -layout) ·
  TeX source (primary — pdftotext mangles displays): /tmp/oaimath/003/paper/paper.tex (773 lines, single file).
- PRINTED locators (always cite these, never a TeX \label): §1 Introduction p.1 (Theorem 1, eq. (1.1)) · §2 "The prime bias forced
  by a real zero" p.2 (Lemma 2, eqs (2.1)–(2.4)) · §3 "Interpolation on a projected integer box" pp.3–5 (Lemma 3, eqs (3.1)–(3.6),
  Figure 1, Corollary 4, Remark 5) · §4 "A weighted determinant of conjugates" pp.5–6 (eqs (4.1)–(4.4), Lemma 6) · §5 "Two bounds
  for the determinant" pp.6–8 (eqs (5.1)–(5.7), Lemma 7) · §6 "Completion of the proof" pp.8–9 (eqs (6.1)–(6.2)) · references p.9.
  Check a locator with `pdftotext -f N -l N -layout /tmp/oaimath/003/paper/paper.pdf -`.
- Lean sources (read-only): /tmp/oaimath/013/repo/lean/OAI/NumberTheory/Jacobsthal/Siegel/ (105 files; the closure of the final
  theorem is 66 of them + PrimeNumberTheoremAnd.Erdos970.HadamardSupport under /tmp/oaimath/013/ext/PrimeNumberTheoremAnd/;
  list: /tmp/oaimath/003/lean/closure_DRZB.txt). A second copy/formalization with the official comparator lives under
  /tmp/oaimath/024/repo/lean/OAI/NumberTheory/SiegelZeros/ ; comparator statement: `git -C /tmp/oaimath/024/repo show
  origin/main:lean/ComparatorChallenges/SiegelZeros.lean`. Our 10-23 bridge + mutants:
  /home/exedev/ErdosProblemADay-main/verification/431/openai-ostmann-inverse-goldbach-refereed/deps/ (SiegelStmt.lean/.log etc.).

## Rules (each comes from a panel that died or erred)
1. Do NOT use the Agent tool or spawn sub-agents. Do the work yourself.
2. Write your report EARLY (first ~15 min: skeleton with "STATUS: IN PROGRESS") at /tmp/oaimath/003/seats/<SEAT>_report.md and
   keep it current. If you are cut off, the file on disk is the only thing that survives.
3. Every script: `bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 …'` (hard memory cap). Long SAT solvers
   (kissat/cadical, some 40+ days old) share this 16-core box and must never be evicted. Do not kill any process you did not start;
   kill your own by PID, never `pkill -f`. No rented compute.
4. A numerical/computational control must be able to FAIL: pair every positive check with a perturbed/negative case that the
   same code rejects.
5. Do not message anyone, post anything, email, open issues, or touch git repos or /home/exedev/ErdosProblemADay*. Write only in
   /tmp/oaimath/003/seats/<SEAT>_work/ and your report.
6. A deliberate weakening ("we do not optimise", "for some absolute C") is not a slip. File an objection only if the stated thing
   is false or does not follow. Quote the exact sentence/display you object to (from the TeX) with its printed locator.
7. Budget: about 60–120 minutes of work. Depth on load-bearing steps beats breadth.

## Report verdict vocabulary
HOLDS AS READ · HOLDS WITH FIXES · GAP AT <printed locator> · FATAL AT <locator> · COULD NOT CHECK <what>.
Then: objections (severity FATAL/GAP/FIXABLE/EXPOSITION, locator, quoted text, why, fix) · what you checked and how (with controls)
· what you could NOT check · one paragraph on where a hole is most likely to hide in your scope and whether it does. Factual, no praise.
