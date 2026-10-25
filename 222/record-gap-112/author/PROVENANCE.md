# Provenance audit for Erdos problem 222

Audit date: 2026-08-11 UTC.

## Live problem state

`live_page_20260811.txt` is a Bright Data browser capture of
<https://www.erdosproblems.com/222>.  At access time it displayed:

- status `OPEN`;
- 0 comments;
- 0 claimed proofs;
- `Currently working on this problem: None`;
- the problem of bounding consecutive differences in the increasing sequence
  of integers that are sums of two squares.

The body cites Erdos (1951), Richards (1982), Dietmann--Elsholtz--Kalmynin--
Konyagin--Maynard (published 2023), and Bambah--Chowla (1947).  Those are
asymptotic results.  The finite computation here makes no improvement to any
asymptotic bound.

## Current OEIS frontier

The following files were downloaded from the official OEIS b-file URLs on
2026-08-11:

- `oeis_A297350_bfile_20260811.txt`: starts of record gaps between sums of two
  squares, 43 rows, last row `(43, 99951600293)`;
- `oeis_A357018_bfile_20260811.txt`: record numbers of consecutive
  nonrepresentable integers, 43 rows, last row `(43, 106)`;
- `oeis_A256435_bfile_20260811.txt`: first differences between sums of two
  squares, through its listed 20,000 rows.

Thus the last record in the current published record tables starts at
99,951,600,293 and has difference 107, equivalently 106 interior integers.
The right endpoint 99,951,600,400 is independently checked by

```text
99951600400 = 77520^2 + 306500^2.
```

`oeis_http_headers_20260811.txt` freezes the successful HTTP responses.  In
particular, the A297350 b-file returned `content-length: 441` and a
`last-modified` date of 2018-02-08.  This is evidence about the retrieved file,
not a claim that no unpublished computation exists.

The corresponding official entry descriptions, checked live, were:

- A297350: "Start of record gaps between sums of two squares";
- A357018: "Records in the number of consecutive integers not expressible as
  sums of 2 squares";
- A256435: "First differences of sums of two squares".

## Primary-source checks

- `sources/erdos_1951_13.pdf` is the seven-page author archive scan of P.
  Erdos, *Some problems and results in elementary number theory*, Publ. Math.
  Debrecen 2 (1951), 103--109, DOI `10.5486/PMD.1951.2.2.04`.  Pages 103--104
  define this sequence and state the lower-gap result cited by the live page.
  `sources/erdos_1951_publisher_page.html` freezes the journal metadata.
- `sources/richards_crossref.json` gives the registered metadata for Ian
  Richards, *On the gaps between numbers which are sums of two squares*,
  Advances in Mathematics 46(1) (1982), 1--2, DOI
  `10.1016/0001-8708(82)90051-2`.
- `sources/dekkm_crossref.json` gives the registered five-author metadata for
  *Longer Gaps Between Values of Binary Quadratic Forms*, IMRN 2023(12),
  10313--10349, DOI `10.1093/imrn/rnac130`.
  `sources/dekkm_arxiv_1810.03203.pdf` and its XML metadata freeze the earlier
  two-author arXiv version.  The journal metadata, not the earlier author list,
  is used when describing the final paper.

No source in this list supplies or claims the finite endpoint reported here.
The finite proof does not depend on their asymptotic theorems.
The original Bambah--Chowla scan was not located on a stable institutional
host during this audit; its bibliographic data and upper-bound attribution were
cross-checked in the live page, current OEIS entry, and later primary papers.
It is contextual only and is not an input to the finite claim.

## Novelty search and its limit

Live web searches on 2026-08-11 included the exact strings
`"133858454292"`, `"133858454404"`, both endpoints together, and combinations
of `gap 112`, `111 consecutive`, and `sums of two squares`.  No relevant indexed
occurrence was returned.  Searches for the old endpoint returned A297350.
This is a documented search miss, not proof of priority or global novelty.

## Local site collision gate

`site_snapshot/` freezes the exact `src/index.js` and `src/ledger_data.js`
versions audited.  `audit_site_gate.py` and `site_gate_20260811.log` establish:

- no #222 problem-number field, hash reference, problem phrase, or problem URL;
- no A297350, A357018, or A256435 reference;
- no record-gap or consecutive-difference phrase for sums of two squares;
- no proposed endpoint.

The broad phrase "sum(s) of two squares" occurs only inside entries 661, 723,
and 955.  Entry 661 uses represented integers to count distance values, entry
723 mentions a projective-plane order obstruction, and entry 955 cites a
structured target set for an aliquot-sum problem.  None studies consecutive
sums of two squares or finite record gaps.  These contexts are disclosed rather
than silently treated as zero broad-word overlap.
