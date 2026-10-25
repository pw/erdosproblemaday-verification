# Erdős #295 — reader submission `urbtgs`: a 34-term certificate, k(18) ≤ 34

**Claim (Kyunghan Bae, submitted 2026-10-11 12:08Z through erdosproblemaday.com/submit, consent to publish):**
the 34 distinct integers

```text
18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
38, 39, 40, 43, 44, 45, 46, 48, 50, 52, 54, 63, 275, 14143068, 10457416992
```

are all ≥ 18 and their reciprocals sum to exactly 1, so k(18) ≤ 34. With our August lower bound
(`../k18/`, exhaustive exclusion of 31- and 32-term expansions) this gives **33 ≤ k(18) ≤ 34**,
replacing the 33 ≤ k(18) ≤ 35 our `/day/295-k17-exact` entry carried since 2026-08-11.

**Verdict: VERIFIED** (published at https://erdosproblemaday.com/submission/urbtgs).

## Chain of verification (ours; none of the submitter's code was executed)

1. `verify_reader_k18_34.py` — written from scratch, imports nothing from the submission. Route 1:
   exact rational sum (`fractions.Fraction`) = 1. Route 2: integer LCM route, L = 6209352774424800
   (matches the claimed LCM) and Σ L/d = L. Also: 34 terms, distinct, strictly increasing, min 18; the
   five-for-four surgery against our 35-term identity (1/42 + 1/640 + 1/337280 + 1/1735650 + 1/68479214496
   = 1/46 + 1/275 + 1/14143068 + 1/10457416992 = 577164227639/22744881957600), removed five ⊂ our set,
   added four ∉ our set, (ours − removed) ∪ added = submitted set. **Negative control:** the last
   denominator +1 is rejected by both routes (exit 2 if it were not). Output: `verify_reader_k18_34.log`.
2. `verify_reader_k18_34.gp` — the same facts in PARI/GP (a second language and bignum library):
   `verify_reader_k18_34_gp.log`.
3. A hostile referee pass by a separately briefed Opus agent with tools, instructed to refute:
   VERIFIED. Its own checker (`referee/cert_check.py`, running gcd-reduced sum, five negative controls) agrees; it re-proved
   `proofs.md` §2 and §3 and ran 113,224 / 300,000 random controls (`referee/lemma_controls.py`, zero violations); its own
   search written from the lemma text (`referee/ref_search.py`) reproduced the submitter's counters AND, in plain mode, our
   published 31/32-term counters (`referee/run_18_3*_plain*.json`, `counts_summary.txt`) — a third implementation of our
   lower bound; solution sets with/without his pruning identical on N=2–10 and 23,095 random residual states
   (`referee/enum_*.py`). Objections: four wording sentences in his note (attribution of the lower bound, "independently
   reproduced", "checked exactly without a cap" describing code not run), none mathematical. Full report: `referee/REFEREE.md`.
4. Novelty (2026-10-11): OEIS A192881 ends at a(16) = 30 (revision 58, 2026-05-30); erdosproblems.com/295
   gives no value at N = 18; arXiv (30 newest unit-fraction / Egyptian-fraction papers) and the OpenAI
   2026-10-06 release (family 025 is about O(log log b) terms; their "295" is Kadison–Ringrose) say nothing
   about k(18). Web search for the specific denominators found nothing. Since the certificate starts at 18,
   it also gives a(18) ≤ 34 for A192881.

## What is whose

- The 34-term construction is the submitter's (his note discloses that OpenAI Codex agents found it
  working for him). Label: (a) elementary — a finite identity.
- The lower bound k(18) ≥ 33 is ours (`../k18/`, 2026-08-11), label (d) computer-assisted. He reports
  reproducing the 32-term exclusion with his own search, which adds two pruning lemmas (a p-adic
  forced-denominator condition and a quadratic bound x² − ax + b ≥ 0 on the two-term tail), so his node
  counts (814,918) are not comparable to ours (14,678,224). We did not run his search; the published lower
  bound rests on our own two engines, as before.

## `submitted/`

Byte-for-byte copies of the release files fetched from
`https://raw.githubusercontent.com/qorud02/erdos-295-k18/v1.0.0/<file>` (22 files, every one matching the
sha256 in the author's own `manifest-sha256.json`; see `MANIFEST_CHECK.txt`) plus the Zenodo record
(DOI 10.5281/zenodo.23297810). `proofs.md` is in Korean. Kept for the record only.

## Reproduce

```bash
python3 -I verification/295/reader-k18-34/verify_reader_k18_34.py   # exit 0
gp -q verification/295/reader-k18-34/verify_reader_k18_34.gp < /dev/null
(cd verification/295/reader-k18-34 && sha256sum -c SHA256SUMS)
```
