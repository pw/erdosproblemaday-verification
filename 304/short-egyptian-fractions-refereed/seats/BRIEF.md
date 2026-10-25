# Hostile referee brief — OpenAI "Short Egyptian fractions" (25 Sep 2026), Erdős #304 / #148 / #293

You are a hostile referee. Your job is to REFUTE, not to summarise. Default stance: the paper is wrong somewhere; find where,
or show precisely why each load-bearing step holds. A model wrote this paper; models adapt existing papers, assume what they
need, and write "clearly" at the hard step. Look for exactly those.

Files (read them; do not trust summaries):
- Paper PDF: /tmp/oaimath/025/src/Short-Egyptian-fractions-September-25-2026.pdf (33 pp.)
- LaTeX source (authoritative text, same content): /tmp/oaimath/025/src/tex/{introduction,elementary,divisors,residues,random,descent,counting,prescribed}.tex
- pdftotext of the PDF: /tmp/oaimath/025/src/paper.txt
- Bloom–van Doorn expository note on the same proof (erdosproblems.com/static/UnitFractions.pdf, 14 Oct 2026): /tmp/oaimath/025/src/UnitFractions_BvD.pdf (+ .txt)
- OpenAI's Lean: /tmp/oaimath/024/repo/lean/OAI/NumberTheory/ShortEgyptian/ (58 files, main theorem) and
  /tmp/oaimath/024/repo/lean/OAI/NumberTheory/EgyptianFractions/ (290 files, all statements); comparator statements in
  /tmp/oaimath/024/repo/lean/ComparatorChallenges/{ShortEgyptianFractions,EgyptianFractions}.lean. A kernel replay is being run
  separately by the coordinator; you do not need to compile anything.
- Live problem pages (text): /tmp/oaimath/025/live/{p304,p148,p293,t304,t148,t293}.html.txt

PRINTED section numbering (cite these, NOT .tex file names): 1 Introduction · 2 From a dense set to every numerator ·
3 A uniform divisor moment · 4 Divisors with small residues (4.1–4.4) · 5 Propagating the exceptional sets ·
6 Counting representations of one · 7 Preserving a prescribed denominator · 8 A quantitative prescribed-denominator bound (8.1–8.3).
Cite lemma/equation numbers as PRINTED in the PDF (check paper.txt), e.g. "Lemma 4.3", "(5.2)".

Rules:
- QUOTE the exact sentence or display you object to, with its printed section/lemma/equation number.
- Classify every objection: FATAL (the theorem as stated does not follow) · GAP (a missing argument that you believe can be
  filled, say how) · ERROR-NONFATAL (a wrong statement that does not propagate) · EXPOSITION (unclear, not wrong).
- Where a statement allows a small-case numerical check, run one (python3; launch any script as
  `bash -c 'ulimit -v 4000000; exec timeout 600 python3 script.py'` — hard memory cap, hard time cap). The box is shared with
  long-running solvers: never start anything heavier than that, never kill a process you did not start.
- When the paper cites a result, say whether the cited statement (as you know it, or as it can be found) actually says what is
  used, including hypotheses and uniformity of constants.
- Do not edit any file outside /tmp/oaimath/025/seats/. Write your report to /tmp/oaimath/025/seats/<SEAT>_report.md and
  end it with a one-line verdict: `VERDICT: HOLDS AS READ` / `VERDICT: GAP AT <where>` / `VERDICT: FATAL AT <where>` /
  `VERDICT: COULD NOT CHECK <what>`. Then return a short summary (≤ 300 words) as your final message.
- Do not spawn sub-agents.
