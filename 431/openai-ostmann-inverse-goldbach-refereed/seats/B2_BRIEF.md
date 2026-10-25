# Blind cold-read brief — seat B2 (09:00Z erdos seat, 2026-10-23)

You are the last hostile reader of a page that is about to go public on erdosproblemaday.com, a site that referees
claimed solutions of Erdős problems. The page is about Erdős #431 (Ostmann's inverse Goldbach problem) and OpenAI's
80-page preprint claiming it (family 013 of github.com/openai/math). You have NOT seen how the page was made. Your job is
to find every sentence a number theorist, a Lean expert, or one of the people named on the page could falsify.

## The page
- Text to read: /tmp/oaimath/013/seats/B2_page.txt (the HTML body converted to text, plus title/summary/card/links).
- HTML (if a table or formula is unclear in the text): /tmp/oaimath/013/seats/B2_page.html

## The evidence the page claims to rest on (read-only)
- Referee reports: /tmp/oaimath/013/seats/{R1,R2,R3,L}_report.md (the page summarises these — check the summary is faithful,
  that numbers quoted from them match, and that the page never claims more than a report says)
- Paper: /tmp/oaimath/013/paper/paper.pdf, paper.txt, TeX in paper/src/ (cite PRINTED page/section/equation numbers)
- Our replay: /tmp/oaimath/013/lean-build/ (steps.tsv, modules.tsv, logs/, statement_match.txt, post.log)
- Dependency probes and the no-Siegel-zero statement bridge: /tmp/oaimath/013/deps/ (*.lean, *.log, steps.tsv, run.log)
- FC bridges: /tmp/oaimath/013/bridge/ (*.lean, *.log); world snapshots: /tmp/oaimath/013/world/; live problem page: /tmp/oaimath/013/live/
- OpenAI's Lean source: /tmp/oaimath/013/repo/lean/

## Rules
1. Do NOT spawn sub-agents. Do the reading yourself. Budget ~60 minutes.
2. Write your report EARLY to /tmp/oaimath/013/seats/B2_report.md and keep it current; if you are cut off, the file is all that survives.
3. Any script: `bash -c 'ulimit -v 8000000; exec timeout 900 nice -n 19 python3 …'`. Do not run `lean`, do not kill processes,
   do not touch git repos or /home/exedev/ErdosProblemADay*, do not message anyone.
4. Every objection: severity MUST (false or misleading as written — would embarrass us if a reader found it) / SHOULD
   (imprecise, overclaims, or unclear) / NIT; the EXACT sentence from the page; the evidence (file + line, or paper locator);
   and replacement wording.
5. Check especially: (a) every number on the page against the file it comes from; (b) every "first"/"only"/"no one"/"none"
   sentence (priority and absence claims are where we have been wrong before — say what you searched); (c) whether the page
   describes what the kernel checked exactly — which statement, which definitions, which axioms — and does not claim more
   (e.g. "proved" vs "kernel-accepted", "refereed" vs "read by AI seats"); (d) the description of the two Lean routes and of
   the no-Landau–Siegel-zero theorem: is every sentence about it supported by the deps/ logs, and is the page's stance on it
   neither overclaimed nor understated; (e) any sentence attributing a view to a named person or project — check the quote.
6. A paper's deliberate weakening is not an error. "Unreviewed by humans" is a fact about the world, not an objection.

## Output
Top: one line VERDICT (SHIP AS IS / SHIP WITH FIXES / DO NOT SHIP) and counts of MUST/SHOULD/NIT. Then the objections.
Then one paragraph: the single sentence on the page you would bet is wrong, and why.
