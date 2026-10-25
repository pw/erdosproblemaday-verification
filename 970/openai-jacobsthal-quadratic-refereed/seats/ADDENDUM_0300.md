# Addendum (03:00Z seat, 2026-10-23) — read after BRIEF.md; these rules override it where they differ

The first panel (00:00Z) died on a subscription session limit before any seat wrote a report. So:

1. **Do NOT use the Agent tool / spawn sub-agents of any kind.** Do the reading yourself. (The last panel's Lean-mapping
   seat spawned eight sub-agents and the whole panel died in twenty minutes.)
2. **Write your report EARLY and keep it current.** Within your first ~15 minutes create
   `/tmp/oaimath/021/seats/<LETTER>_report.md` with a skeleton (scope, "IN PROGRESS", what you have read so far), and update it
   after each lemma/section you finish. If you are cut off, the file on disk is the only thing that survives.
3. Budget: aim to finish in about 60–90 minutes of work. Depth on the load-bearing steps beats breadth on exposition.
4. Context you can rely on (verified by us, do not redo): OpenAI's Lean 4 formalization (819 OAI modules, 850-module closure)
   was kernel-replayed here — 850/850 built, the comparator theorems `erdos_970_quadratic` and `erdos_970_iterated_log`
   depend only on [propext, Classical.choice, Quot.sound], statements match the comparator files, `leanchecker --fresh` rc 0.
   So the THEOREM is machine-checked; your job is the PAPER: is its argument, as written, correct and complete? Where the
   paper and the Lean could differ in route, that is worth one sentence, but do not read the Lean unless your scope says so.
5. Earlier files you may reuse (read-only): `/tmp/oaimath/021/compute/` (loss_terms.py — a recomputation of Prop 6.3's
   first-omission loss terms; its tail-majorant line overflowed, fix with logs/mpmath if you need it), `/tmp/oaimath/021/seats/W_work/`
   (fetched sources: cited/, src/ arXiv PDFs, live erdosproblems pages, OpenAI doc 021.md, FC's 970.lean, code-search hits).
6. Cite PRINTED locators only (Lemma 8.4, eq. (8.12), p. 47). PDF page N ↔ `pdftotext -f N -l N -layout paper.pdf -`.
