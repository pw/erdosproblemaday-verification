# Blind read — the #952 entry page, checked against the files (erdos cron seat, 2026-10-22)

You are a hostile copy-and-fact checker. You have NOT seen how this page was made. Your job: find every sentence on the page
that is false, overstated, unsupported by the files, internally inconsistent, or misleading to a mathematician reading it cold.
A mathematician who finds a hole should find the page already saying where to look; if the page claims more than the files
support, that is a MUST-FIX.

The page text (rendered, as a reader sees it): /tmp/oaimath/028/entry/entry_rendered.txt
The page source (HTML inside a JS object): /tmp/oaimath/028/entry/entry952.js
(One sentence is a deliberate placeholder, BFS_PENDING_SENTENCE: it will report whether a second program agrees with the first
on all 154 sets for D = √2 and D = 2. Ignore it.)

The files the page rests on (read them; do not trust the page's summary of them):
- Paper: /tmp/oaimath/028/src/paper.txt (pdftotext of OpenAI's PDF — beware: pdftotext moves √ and overlines onto other lines;
  check the LaTeX in /tmp/oaimath/028/src/build/*.tex before calling a formula wrong)
- Live problem page + forum: /tmp/oaimath/028/live/{page0,page1,page2}.txt, p952_0300.html, p952c_0300.html; teorth DB extract
  live/teorth_problems.yaml (entry number "952")
- OpenAI repo clone (commit 1581d4c, git history available): /tmp/oaimath/028/repo
- Replay: /tmp/oaimath/028/lean-build/{steps.tsv,modules.tsv,driver.log,statement_match.txt,mut/MUTATIONS.txt,ESTIMATE.md,post.log,probes.json} and logs/
- Bridge: /tmp/oaimath/028/bridge/{Bridge952.lean,FC_952.lean,FC_SHA.txt,AxBridge.log,AxMutSorry.log,Bridge*Mut*.lean/.log,verbatim*.log}
- Computations: /tmp/oaimath/028/compute/ (sieve_perc.c, bfs_check.py, scan.py, *.log, july_checker_rerun.log)
- Seat reports: /tmp/oaimath/028/seats/{G,S,I,L,W}_report.md, main_reading.md; W's downloads in seats/W_src and seats/W_work
  (Vardi 1998 text: seats/W_work/vardi/vardi.txt; Gethner–Stark: seats/W_src/gethner.txt; FC commit message seats/W_work/fc_3dfd999_msg.txt)
- Our July report on #952 is the `{n:952,` record in /home/exedev/ErdosProblemADay-1022-0300/src/ledger_data.js (field md)

Check, at minimum:
1. Every number on the page (module counts, lines, times, GiB, mutation counts, dates, PR numbers, arXiv ids, commit hashes,
   tree hash, 580, 80, 154, 0.48, 7,113,990, 100, 1,547, 65,535, 1,500, M values, 4,001) against the file that produced it.
2. Every attribution: what is OpenAI's, Gethner–Stark's, Vardi's, Jordan–Rabung's, FC's, the earlier builders', ours. Anything
   the page calls "ours" that the files show was done elsewhere first is a MUST-FIX.
3. Every mathematical statement in the page's own words (the summary of Theorem 1.1/1.2, Prop 2.1's bound, the argument paragraph,
   the "Lean is not a transcript" paragraph's four differences, the miniature paragraph incl. the z ↦ (1+i)z+1 correspondence and
   the parity remark) against the paper, the Lean and the scripts.
4. Labels (a)/(b)/(c)/(d) and the "where to look for the hole" sentence: are they honest given that the Lean is green?
5. Placeholders, leftover tokens, broken links (check the URLs; github/arxiv should resolve), and sentences a cold reader could misread.

Rules: quote the exact sentence you object to; classify MUST-FIX / SHOULD-FIX / NIT; give the corrected sentence when you can. You may
run small scripts (`bash -c 'ulimit -v 4000000; exec timeout 600 python3 …'`); never start anything heavier, never kill a process you
did not start, do not edit any file outside /tmp/oaimath/028/seats/. Write your report to /tmp/oaimath/028/seats/B_report.md and return
a short summary (≤ 250 words) listing the MUST-FIX items. Do not spawn sub-agents.
