# Blind read — the #978 entry page, checked against the files (erdos cron seat, 2026-10-22)

You are a hostile copy-and-fact checker. You have NOT seen how this page was made. Your job: find every sentence on the page
that is false, overstated, unsupported by the files, internally inconsistent, or misleading to a mathematician reading it cold.
A mathematician who finds a hole should find the page already saying where to look; if the page claims more than the files
support, that is a MUST-FIX.

The page text (rendered, as a reader sees it): /tmp/oaimath/020/entry/entry_rendered.txt
The page source (HTML inside a JS object): /tmp/oaimath/020/entry/entry978.js
(One sentence is a deliberate placeholder, LEANCHECKER_SENTENCE: it will report the result of `leanchecker --fresh` over the
closure plus the bridge, which is still running. Ignore it.)

The files the page rests on (read them; do not trust the page's summary of them):
- Paper: /tmp/oaimath/020/paper/paper.txt (pdftotext of OpenAI's PDF — beware: pdftotext moves exponents and √ onto other lines;
  check the LaTeX in /tmp/oaimath/020/paper/src/build/sections/*.tex before calling a formula wrong; printed section numbering:
  12-certificate.tex is Appendix A, 13-cyclotomic.tex is §12)
- Live problem page + forum: /tmp/oaimath/020/live/{p978.txt,p978_thread.txt,p978_claims.txt,p978_latex.txt} (fetched 22 Oct 2026);
  teorth DB: /tmp/oaimath/020/live/teorth_problems.yaml (entry number "978")
- OpenAI repo clone (commit 1581d4c, git history available, blob:none: use `git -C /tmp/oaimath/024/repo show HEAD:<path>`);
  the 63-file Lean closure + comparator copied to /tmp/oaimath/020/repo/lean/
- Replay: /tmp/oaimath/020/lean-build/{steps.tsv,modules.tsv,driver.log,statement_match.txt,mut/MUTATIONS.txt,mutate_matcher.sh,
  post.log,probes.json,drive.py,all_order.txt} and logs/ (ax_PowerFreeValues.log, cmp_PowerFreeValues.log, neg.log, mod_*.txt)
- Bridge: /tmp/oaimath/020/bridge/{Bridge978.lean,Bridge978.log,FC_978.lean,FC_Powerfree.lean,FC_Density.lean,FC_SHA.txt,AxBridge.log,
  AxMutSorry.log,BridgeMutSorry.lean/.log,BridgeMutExp.lean/.log,BridgeMutNoLocal.lean/.log,verbatim_check.py,verbatim.log,verbatim_mut.log}
- Computations: /tmp/oaimath/020/compute/ (euler.gp/out, tail.gp/out, sieve_count.py/out, sieve_count_mut_nolift.py, sieve_count_mut.out);
  seat M2's factorisation runs: /tmp/oaimath/020/seats/M2_work/{sqf.gp,out_w*_c*.txt}
- Our July report on #978: /home/exedev/MathDyad/runs/erdos978_wave7y.md
- Seat reports: /tmp/oaimath/020/seats/{M1,M2,L,W}_report.md (+ *_work/); W's downloads in seats/W_work (Erdős page images/pdfs,
  arXiv texts in W_work/arx, scripts in W_work/scripts)

Check, at minimum:
1. Every number on the page (module counts, lines, minutes, GiB, mutation counts, dates, PR/issue numbers, arXiv ids, commit hashes,
   tree hashes, densities, counts 75,670 / 151,346 / 756,674 / 98,090 / 196,180 / 980,831 / 65,353, margins 0.0019350, 1.5·10⁻⁸,
   434, 609, 25, 5·10⁻⁴, 3/1000, 1/2000, 0.00059, 24979/25000, 3122/3125) against the file that produced it.
2. Every attribution: what is OpenAI's, Erdős's, Hooley's, Nair's, Heath-Brown's, Browning's, Reuss's, Booker–Browning's,
   Zapata Ceballos–Jalalvand's, Carella's, FC's / Firsching's, DeepMind's, ours. Anything the page calls "ours" or "first" that the
   files show was done elsewhere first is a MUST-FIX. In particular test the sentence "As far as we can find, this is the first
   reported kernel replay" — search yourself (GitHub, the web) for any earlier replay or rebuild of OpenAI's PowerFree Lean.
3. Every mathematical statement in the page's own words (Theorem 1.1/Cor 1.2/1.3/Prop 1.4 as summarised; the argument paragraph;
   the "Lean does not follow the paper" paragraph; the bridge paragraph incl. the claim that FC's parts.ii literally excludes
   degrees 4 and 8; the ρ(p²) formula; the Erdős quotes) against the paper, the Lean, the FC file, the scripts and Erdős's pages.
4. Labels (a)/(b)/(c)/(d) and the "Where to look for a hole" list: are they honest given that the Lean is green?
5. Placeholders, leftover tokens, broken links (check the URLs; github/arxiv should resolve), and sentences a cold reader could misread.

Rules: quote the exact sentence you object to; classify MUST-FIX / SHOULD-FIX / NIT; give the corrected sentence when you can. You may
run small scripts (`bash -c 'ulimit -v 4000000; exec timeout 600 python3 …'`); never start anything heavier, never run lean/lake,
never kill a process you did not start, do not edit any file outside /tmp/oaimath/020/seats/ (scratch in seats/B_work/). Write your
report to /tmp/oaimath/020/seats/B_report.md and return a short summary (≤ 250 words) listing the MUST-FIX items. Do not spawn sub-agents.
