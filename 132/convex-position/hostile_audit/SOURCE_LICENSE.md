# Source and license audit

This is a provenance record, not legal advice.  The conservative packaging
rule is: publish links, hashes, bibliographic metadata, short quotations, and
original audit prose/code; do not republish third-party full text unless the
license affirmatively permits it.

## Clemen--Dumitrescu--Liu Version of Record

- Frozen path: `../bundle_ro/sources/cdliu_published.pdf`
- SHA-256: `7216e1ebb83de3d0b5f3ee06467d676c18b930e7cb1480927ed3b19740c2b422`
- Official repository URL:
  `https://publikationen.bibliothek.kit.edu/1000188330/170672891`
- Fresh 2026-08-11 download: byte-identical.
- License: CC BY 4.0, stated on the VOR's final page and the Springer article
  page.  Redistribution is allowed with attribution, a license link, and an
  indication of changes.

The issue date is October 2025; Springer records online publication and VOR
on 12 November 2025.  Those are different metadata fields, not a conflict in
the theorem's identity.

## Clemen--Dumitrescu--Liu arXiv v5

- PDF SHA-256:
  `d993acd48bebb09a418a0cecf7f38741796dd1cd85952f4d3535c6761b59d7dd`
- Source-tar SHA-256:
  `5a18a501eb7c6052d298909f1bb88b606858d632662bc4e918e9c54e52e0556c`
- `main.tex` SHA-256:
  `d0cb51137a72221d12878fd25021ba0e57e536782cdc1712130ec84424c870a1`
- Official record: `https://arxiv.org/abs/2505.04283v5`
- Fresh 2026-08-11 PDF and source downloads: byte-identical.

The arXiv PDF metadata names the arXiv nonexclusive-distribution license.
That license is not, by itself, an affirmative downstream reuse license for
repacking arXiv's PDF/source bytes.  The journal article content is CC BY, but
the safest public package omits the arXiv PDF/tar/TeX bytes and links to them.

## Altman 1972

- Frozen paths: `../bundle_ro/sources/altman1972.pdf` and `.txt`
- PDF SHA-256:
  `dba78b275aa9337a0f02758681a9bfef0fab1d3d5c61ea8955df4e25f5e6ac6a`
- Official Cambridge URL:
  `https://doi.org/10.4153/CMB-1972-060-0`
- Fresh 2026-08-11 download: byte-identical.

The PDF XMP rights field says it is not for further distribution absent an
applicable license or Cambridge permission.  No permissive reuse license was
located.  The full PDF and its full extracted text therefore create a clear
public-packaging gap; link to the official copy instead.

## Altman 1963

The input retains only a first-page preview screenshot.  The Taylor & Francis
record identifies DOI `10.1080/00029890.1963.11990057` and denied full-text
access without a subscription.  No permissive reuse license was established.
Do not republish the screenshot as affirmatively licensed material; a normal
short quotation with citation is the conservative substitute.

## Fishburn 1995

- Private local verification path:
  `../private_source_cache/fishburn1995_vor.pdf`
- SHA-256: `b63a4ff8d00e4b2fcc7acc68924c0975ffc9d4a640ce7c1962f2781525053935`
- Bytes/pages: `1798795` / `29`
- DOI: `10.1016/0925-7721(94)00020-V`
- Publisher URL:
  `https://www.sciencedirect.com/science/article/pii/092577219400020V`
- License URL:
  `https://www.elsevier.com/open-access/userlicense/1.0/`

The publisher labels the article open archive under the Elsevier user
license.  The current license permits noncommercial access, download, copy,
and text/data mining, but says users may not redistribute, display, or adapt
the article.  The intact PDF is therefore isolated outside the public-safe
audit directory and must not be added to its tarball or a public repository.

## Public-copy decision

`independent_hostile_audit_2_ro/` is safe to copy as original audit prose,
code, hashes, and logs.  It deliberately contains no site snapshot, full
third-party article, extracted full article, or source tar.  Do not copy
`bundle_ro/sources/`, `bundle_ro/provenance/*.png`,
`bundle_ro/site_snapshot/`, or `private_source_cache/` as part of that public
package without separate rights review.
