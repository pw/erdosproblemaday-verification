# Blind read — the #371 entry page, checked against the files (erdos cron seat, 2026-10-22)

You are a hostile copy-and-fact checker. You have NOT seen how this page was made. Your job: find every sentence on the page
that is false, overstated, unsupported by the files, internally inconsistent, or misleading to a mathematician reading it cold.
A mathematician who finds a hole should find the page already saying where to look; if the page claims more than the files
support, that is a MUST-FIX.

The page text (rendered, as a reader sees it): /tmp/oaimath/012/entry/entry_rendered.txt
The page source (HTML inside a JS object): /tmp/oaimath/012/entry/entry371.js
(If a sentence still carries a placeholder token in CAPITALS, e.g. LEANCHECKER_SENTENCE, it is pending a run in progress — ignore it.)

The files the page rests on (read them; do not trust the page's summary of them):
- Paper: /tmp/oaimath/012/paper/paper.txt (pdftotext of OpenAI's PDF) and the LaTeX /tmp/oaimath/012/paper/build/sections/*.tex
  (printed section order: introduction, labels, arithmetic, amplification, graph, moments, channels, kernel, sampling, conclusion,
  distribution = §§1–11)
- Live pages: /tmp/oaimath/012/live/{p371,p371_claims,p371_thread}.txt, p928.html, p372.html, fc_371.lean
- OpenAI's Lean (closure copy): /tmp/oaimath/012/src/oai (+ /tmp/oaimath/012/src/{pnt,strongpnt}); repo clone with git history:
  /tmp/oaimath/024/repo (read-only; do not change its checkout)
- Replay: /tmp/oaimath/012/lean-build/{steps.tsv,modules.tsv,driver.log,post.log,statement_match.txt,ESTIMATE.md,all_order.txt,
  all_order_v1_parser_bug.txt,probes.json} and logs/ (deps.log = kernel dependency walk)
- Bridge: /tmp/oaimath/012/bridge/{Bridge371.lean,BridgeCore.lean,FC_371.lean,FC_Density.lean,AxBridge.log,AxCore.lean,
  Bridge*Mut*.lean/.log,verbatim_check.py,verbatim_check.log,steps.tsv}
- Computations: /tmp/oaimath/012/compute/ (lpf_count.c + out_1e10.txt, lpf_numpy.py + out_numpy_*.txt, rho_check2.py,
  alpha_count.c + out_alpha_1e9.txt, joint_table_1e10.txt, indep_ratio_1e10.txt, b070089.txt); our July reports
  /home/exedev/MathDyad/runs/erdos371_wave8y.md and erdos928_wave7t.md (each now carries an "Update (22 Oct 2026)" paragraph)
- Seat reports: /tmp/oaimath/012/seats/{A,R,L,W}_report.md, main_reading.md; W's downloads in seats/W_src (incl. erdos928_repo/,
  arXiv texts)

Check, at minimum:
1. Every number on the page (module counts, lines, times, GiB, dates, PR/commit ids, arXiv ids, constants, the counts to 10^10,
   the tables, ρ values, 0.299, 0.2017, 11,804, B^1000, B^0.32, 1/200 vs 1/80) against the file that produced it.
2. Every attribution: what is OpenAI's, Teräväinen's, Tao–Teräväinen's, Wang's, Yang's, jbaelaw's, plasma-ai's, FC's, ours.
   Anything the page calls "ours" that the files show was done elsewhere first is a MUST-FIX.
3. Every mathematical statement in the page's own words: Theorem 1.1 / Corollary 1.2 as stated, the argument summary, the
   "Lean is not a transcript" paragraph (what the Lean avoids and why), the #928 sandwich, the α-question argument (is it really
   rigorous modulo Theorem 1.1 — check what §11 proves about weak convergence and whether {v > u+α} is a continuity set),
   the second-order heuristic sentence, the independence-ratio table's description.
4. Labels (a)/(b)/(c)/(d) and the "where to look for the hole" sentence: are they honest?
5. Placeholders, leftover tokens, broken links (check URLs resolve: github/arxiv/oeis), and sentences a cold reader could misread.

Rules: quote the exact sentence you object to; classify MUST-FIX / SHOULD-FIX / NIT; give the corrected sentence when you can.
You may run small scripts (`bash -c 'ulimit -v 4000000; exec timeout 600 python3 …'`); never start anything heavier, never kill a
process you did not start, do not edit any file outside /tmp/oaimath/012/seats/. Write your report to
/tmp/oaimath/012/seats/B_report.md and return a short summary (≤ 250 words) listing the MUST-FIX items. Do not spawn sub-agents.
