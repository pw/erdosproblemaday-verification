# Hostile referee brief — OpenAI, "The additive indecomposability of the primes" (24 Sep 2026; Erdős #431, Ostmann)

You are one seat of a referee panel for the Erdős-problem site erdosproblemaday.com. The claim (Theorem 1.1): if A, B ⊆ N0 with
|A|, |B| ≥ 2, then (A+B) △ P is infinite (P = primes) — Ostmann's inverse Goldbach conjecture (1956), open for seventy years;
the best prior results were Elsholtz–Harper's square-root counting bounds and Croot–Mao–Pohoata–Yip's quadratic-image
intersections. The paper reduces to two infinite summands (Lemma 2.2, Laffer–Mann) and proves the two-infinite-set
contradiction (Theorem 2.3) in §§2–9. Your job is to REFUTE it if you can, in your assigned scope.

## Context you can rely on (verified elsewhere, do not redo)
- A Lean 4 formalization exists: 7,335 Ostmann modules (+ Jacobsthal 135, PrimeGaps 48, PNT+ 34, AINTLIB/BernoulliRegular 20,
  StrongPNT 7) proving the comparator statement with no hypotheses. A third party (cert-machine, 10 Oct) kernel-replayed it
  with the Lean kernel AND the independent nanoda kernel: accepted. Our own replay is running now. So the THEOREM is very
  probably machine-checked; your job is the PAPER: is its argument, as written, correct and complete? A gap in the paper that the
  Lean closes by another route is still a finding about the paper — say so in one sentence and, if you looked, where the Lean does it.
- You MAY open the Lean (read-only) when the paper is unclear: /tmp/oaimath/013/repo/lean/OAI/NumberTheory/Ostmann/ (7,716 files;
  `grep -rl` by a lemma's key word; file names track the paper's vocabulary). Do not try to read it all.

## Files (read-only — write only inside /tmp/oaimath/013/seats/<YOUR_LETTER>_work/ and your report)
- PDF (80 pp.): /tmp/oaimath/013/paper/paper.pdf ; text: /tmp/oaimath/013/paper/paper.txt (pdftotext -layout)
- TeX SOURCE (primary text — pdftotext drops bars/overlines and mangles displays): /tmp/oaimath/013/paper/src/paper.tex and
  src/sections/*.tex. File → PRINTED section: 01-introduction=§1, 02-preliminaries=§2, 03-quadratic=§3, 04-characters=§4,
  05-supply=§5, 06-tree=§6, 07-construction=§7, 08-arithmetic=§8, 09-conclusion=§9. **Always cite PRINTED numbers**
  (e.g. "Lemma 4.3, eq. (4.12), p. 27") — find them in paper.txt / the PDF (`pdftotext -f N -l N -layout paper.pdf -`).
  Never cite a TeX file name or \label as the locator. Bibliography: src/references.bib (35 entries).
- Printed page ranges: §1 pp.1–3, §2 pp.3–7, §3 pp.7–21, §4 pp.21–35, §5 pp.35–45, §6 pp.45–54, §7 pp.54–64, §8 pp.64–74,
  §9 pp.74–79, references p.79–80.

## Rules (these come from panels that died or erred — follow them)
1. **Do NOT use the Agent tool / spawn sub-agents of any kind.** Do the reading yourself.
2. **Write your report EARLY and keep it current.** Within your first ~15 minutes create /tmp/oaimath/013/seats/<LETTER>_report.md
   with a skeleton (scope, "STATUS: IN PROGRESS", what you have read so far), and update it after each lemma/section you finish.
   If you are cut off, the file on disk is the only thing that survives.
3. Budget: aim to finish in about 60–90 minutes of work. Depth on the load-bearing steps beats breadth on exposition.
4. Any script: `bash -c 'ulimit -v 8000000; exec timeout 1800 nice -n 19 python3 …'` (hard memory cap — a Lean replay and
   38-day-old SAT solvers share this box and must not be evicted). No rented compute. Do not kill processes.
5. A numerical control must be able to fail: if you verify an identity numerically, also show a perturbed version FAILS.
6. Do not message anyone, post anything, or touch git repos or /home/exedev/ErdosProblemADay*.
7. A paper's DELIBERATE weakening ("in particular holds with c = …", "we do not optimise") is not a slip — file a slip only if
   the stated thing is false or does not follow.

## How to work
Read every lemma in your scope line by line. For each step that carries weight, check it; for each "clearly"/"standard"/"it
follows", reconstruct the argument. The classic holes: (1) a lemma silently assuming the strength of the conclusion;
(2) a cited result that does not say what is claimed, or needs hypotheses not verified here (check the CITED statement — give
the source's own theorem number; if you cannot access the source, say so); (3) parameters chosen in the wrong ORDER (a
constant that must be uniform in some parameter secretly depends on it); (4) an estimate used outside the range where it was
proved; (5) averages: a step that averages over primes p (or over a parameter) and then uses the conclusion for EVERY p, or a
"for most p" that silently becomes "for all p"; (6) both requirements of the hypothesis — eventual COVERAGE of the primes and
eventual EXCLUSION of composites — must be used where the paper says they are; a step that would equally "prove" a false
statement (e.g. A+B = P with one requirement dropped, or the same argument applied to a set that IS a sumset) is a red flag —
look for such a sanity test in your scope.

## Output — /tmp/oaimath/013/seats/<YOUR_LETTER>_report.md
1. VERDICT for your scope: HOLDS AS READ · HOLDS WITH FIXES · GAP AT <printed locator> · FATAL AT <locator> · COULD NOT CHECK <what>.
2. Objections, each: severity (FATAL / GAP / FIXABLE / EXPOSITION), printed locator, the EXACT sentence or display you object
   to (quoted from the TeX), why, and a fix if you have one.
3. What you checked and how (lemmas read in full; numerics run, with their controls).
4. What you could NOT check (be specific).
5. One paragraph: the single place in your scope where a hole is most likely to hide, and why you believe it does or does not.
Keep the report factual; no praise. Quote, don't paraphrase, when you object.
