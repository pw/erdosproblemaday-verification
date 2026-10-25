# Four-seat hostile referee pass — OpenAI "Monochromatic finite sums and products in the positive integers" (family 164, Erdős #172)

Date: 2026-10-11 (erdos cron tick 06:36Z, Fable 5.1 driver). Paper: `openai-164-paper-2026-09-23.pdf` (SHA-256 in `SHA256SUMS`;
byte-identical to the github.com/openai/math blob at fetch time). Nothing mathematical here is ours; the apparatus is.

## Apparatus
One shared brief (`REFEREE_BRIEF.md`: refute, fetch every cited theorem from its current arXiv version, quote the sentence you
object to, list what you verified line by line vs skimmed, verdict HOLDS AS READ / GAP AT / COULD NOT CHECK) and four
tool-equipped Opus seats with DISJOINT scopes, run concurrently, each writing its own file:

| seat | scope | report | verdict |
|---|---|---|---|
| deduction | §2: both principles as stated, Lemma 2.5, §2.5 deduction, Cor 1.2/2.6, parameter graph, Alweiss §4/§5 | `referee_deduction.md` | HOLDS AS READ (4 cosmetic; names 3 uniformity claims for the other seats) |
| prediction | §3–5 (Principle 2.3) + Lemma 7.2; GTZ / Tao–Ziegler 1.23 / Yamada / dense-model inputs vs source | `referee_prediction.md` | HOLDS AS READ (4 cosmetic/unclear; both §5.3 inputs re-checked clause by clause after the formalisation finding) |
| alignment | §6–8 (Principle 2.4): δ trace, Zorin-Kranich Cor 3.7, GT erratum equal-sides, Prop 6.3 / 7.5, Lemma 8.3, §8.5 | `referee_alignment.md` | HOLDS AS READ (7 cosmetic/unclear; δ's complexity-independence traced to Lemma 8.1's free-nilpotent-group pullback + Lemma 7.7 + the pigeonhole (8.23); [37] Cor 3.7 used only combinatorially, no measure bound imported) |
| citations | all 37 references (versions/dates vs arXiv record, DOIs vs Crossref/zbMATH), every §1.1 theorem-number claim vs source, novelty + reception sweep | `referee_citations.md` | ACCURATE except [21]: the seven-colour infinite counterexample is cited to Hindman 1980 while Hindman's own later citations + zbMATH's review place it in Hindman 1984 (erdosproblems.com and our August report cite 1980 too; the 1980 PDF itself unread by either seat — stated by source on the page); 37/37 exist; no earlier proof; third-party Lean formalisation found |

The driver read §2, §4.1, §5.3 (both inverse statements), §6.1, §8.1, Lemma 8.3 and the proof of Principle 2.4 independently
before the seats reported (notes in the daily log). The diff between readers is the instrument: the deduction seat's three
"could not check" items were exactly the items the prediction and alignment seats were briefed to settle.

## Decorrelation
- The other erdos seat of the same hour (launcher 06:32Z) ran ONE whole-paper Opus referee + its own primary-source quotes +
  exact controls (identity (8.2) exhaustive n ≤ 8; Cor 1.2 separation with a negative control) + the Lean audit and kernel
  replay: `~/ErdosProblemADay-main/verification/172/openai-referee/`. Neither seat saw the other's reports before writing.
- Scratch: `scratch/scripts_deduction/check.py` — chain-ordering control (2,000 random chains, 0 violations of B_k ∈ E_{B_d};
  Alweiss's anti-ordered tails as negative control: 2,396/2,396 violations).

## Reproduce
pdftotext the PDF (both `-layout` and plain); hand each seat `REFEREE_BRIEF.md` + its scope paragraph (the four prompts are in `PROMPTS.md`); fetch the sources the reports name into
their own directories; compare quotes.
