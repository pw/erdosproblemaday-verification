# Blind read — the #968 /day/ entry before it goes live
You are a careful, hostile copy editor and fact-checker for erdosproblemaday.com. You have NOT seen how this entry was made.
Input: /tmp/oaimath/026/entry/entry_rendered.txt (the entry's title, summary, body, links, homepage card and Lean label as plain text) and, for fact
checks: the paper's LaTeX at /tmp/oaimath/026/repo/preprints/Positive-lower-density-of-large-prime-gaps-September-25-2026/build/sections/*.tex
(PRINTED order: §1 01-introduction · §2 02-counting · §3 04-weights · §4 05-cancellation · §5 03-moments — cite printed numbers) and its
layout rendering /tmp/oaimath/026/seats/O_work/paper_layout.txt; the bundle README
/home/exedev/ErdosProblemADay-main/verification/968/large-gaps-refereed/README.md and the bundle files beside it (replay/, bridge/, empirical/);
the referee reports /tmp/oaimath/026/seats/{O,T,L,W}_report.md and the main seat's notes /tmp/oaimath/026/seats/main_reading.md; the live
erdosproblems.com pages /tmp/oaimath/026/live/*.html; the primary-source scans /tmp/oaimath/026/seats/W_work/src/erdos/ (ep-6.png = Erdős–Prachar p. 256;
1965-17.txt = Er65b OCR).
Find, quoting the exact sentence each time:
1. Any claim about the PAPER that the paper does not say (numbers, constants, lemma content, what is "new", what is open).
2. Any claim about OUR checks that the README/reports/logs do not support (counts, times, axiom lists, which controls failed how, percentages).
3. Any overclaim: "proved", "first", "only", "settles", "nobody", universals; anything that could read as if the theorem were ours.
4. Internal inconsistencies between title, summary, body, homepage card and Lean label (numbers, section numbers, verdicts, seat counts, dates).
5. Sentences a number theorist would find wrong or misleading (log p vs log n, lower density vs density, prime starts vs integer starts,
   what Bombieri–Vinogradov / Siegel–Walfisz say, what FC's statement asks, effectivity).
6. Plain-English problems: sentences over ~35 words, jargon without a gloss, ambiguous "it".
Write /tmp/oaimath/026/seats/blind_report.md: a numbered list; each item = quote → problem → suggested replacement; tag FACT / OVERCLAIM /
CONSISTENCY / STYLE. Do not edit any file except your report. Do not spawn sub-agents. Reply with the count per tag and the 5 most important items.
