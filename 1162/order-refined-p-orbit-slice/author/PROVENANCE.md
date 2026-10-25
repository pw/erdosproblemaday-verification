# Provenance

Access date for every web source: 2026-08-11 UTC.

- `live_page_1162_20260811.txt`: rendered `document.body.innerText` from
  `https://www.erdosproblems.com/1162`, fetched with Bright Data because
  datacenter `curl` received Cloudflare HTTP 403.
- `roney_dougal_tracey_2025.pdf`: `https://arxiv.org/pdf/2503.05416`.
- `roney_dougal_tracey_2025.tex`: source from
  `https://export.arxiv.org/e-print/2503.05416` (v1, 2025-03-07).
- `arxiv_2503.05416_metadata.xml`: official arXiv API metadata.
- `holt_2010_enumerating_subgroups.pdf`: author-hosted copy linked by the
  official OEIS A005432 record; title, author, venue, and table agree with the
  Crossref record DOI `10.1090/conm/511/10041`.
- `oeis_A005432_20260811.seq`: official `oeis/oeisdata` GitHub export at path
  `seq/A005/A005432.seq`, fetched from `main`. Its header is dated 2026-04-19;
  the path's latest export commit returned by GitHub was
  `1655db1982f93ba44dd2956905a27ba9e4530a00` (2026-05-04).
- Jeff Ketchersid's public 2026 `parallel_sn_19.tar.xz` archive (SHA-256
  `7f27ae1a11f2ded8d720af289510a1569f277bf8041d45ac71eeaf7f5d47610a`)
  was inspected only to distinguish A000638 from A005432. It is retained as
  provenance but is not an input to the theorem or verifier.
- `arxiv_2606.17488.pdf` is a forward-citing paper returned by citation search.
  Its topic is unrelated to the order distribution in symmetric groups; it is
  retained only to make that negative literature check auditable.

Searches used the arXiv API, Crossref API, OEIS records, the current live page,
and forward-citation metadata. A search miss is not evidence of novelty.

## Corrected v2

This directory was cloned from the preserved v1 bundle after its manifest was
verified. V2 changes only the report/reproduction layer and adds the independent
asymptotic audit; the frozen primary sources and exact enumeration programs are
unchanged. The v1 identity is recorded in the correction note at the start of
`REPORT.md`. No site source or deployment was modified.
