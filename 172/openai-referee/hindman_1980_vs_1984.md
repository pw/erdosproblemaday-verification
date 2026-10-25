# Where is Hindman's seven-cell counterexample? (1980 "two counterexamples" vs 1984 "pairwise sums and products")

Raised 2026-10-11 by the citations referee seat of the parallel session: the OpenAI paper's §1.1 says "Hindman constructed a
finite coloring of N with no infinite set whose terms, pairwise sums and pairwise products all have one color [21]", with
[21] = N. Hindman, *Partitions and sums and products—Two counterexamples*, J. Combin. Theory Ser. A 29 (1980) 113–120.

## Evidence gathered (all fetched 2026-10-11)
- **zbMATH Open, review of Hindman, *Partitions and pairwise sums and products*, JCTA 37 (1984) 46–60**
  (DOI 10.1016/0097-3165(84)90018-9, zbmath.org/3861171), verbatim: "A seven cell partition of N is constructed with the
  property that no infinite set has all of its pairwise sums and products in any one cell. A related Ramsey theory
  question is shown to have different answers for two and three cell partitions."
- **zbMATH Open, record of the 1980 paper** (DOI 10.1016/0097-3165(80)90052-7, zbmath.org/3691339): no review text in the
  API (`editorial_contributions: []`), MSC 05A17/11P81/03E05.
- **Griffin, arXiv:2605.24751 (May 2026), p.1:** "In [9], Hindman constructed a seven cell partition of N such that there is
  no infinite set with its pairwise sums, pairwise products, and the infinite set being monochromatic", where
  [9] = "Partitions and pairwise sums and products – two counterexamples, JCTA 29 (1980), no. 1, 113–120" — a hybrid of
  the two titles attached to the 1980 locator.
- **erdosproblems.com/172** cites [Hi80] for "false (with 7 colours) if we ask for an infinite A" (our August read of the
  live page); OpenAI's paper cites the same locator; **our own August /report/172** wrote that the 1980 DOI "has exactly
  the seven-colour infinitary counterexample described on the live page" with a (b) label — that line is now suspect and
  is being re-checked against the 1980 PDF (ScienceDirect 403s from this box; see below).
- Alweiss (arXiv:2307.08901) attributes the infinite-sequence negative result to 1979 (per the search summary; not
  re-read here).

## Status
UNRESOLVED pending the 1980 paper's text: the 1984 review places the seven-cell construction in 1984; whether the 1980
"two counterexamples" ALSO contain it (an earlier form) is exactly what only the 1980 PDF can say. Until then the honest
sentence is: "zbMATH's review places the construction in the 1984 paper; the 1980 paper is the locator everyone cites,
ourselves included." The point is COSMETIC for the theorem and for the paper's proof; it matters for our own record.

## Update 07:5xZ (from the parallel seat's Mac-Chrome / Wayback pass — `seats/hindman_pdfs/NOTE.md`)
- **1984 abstract VERIFIED VERBATIM** against a Wayback snapshot of the ScienceDirect page (capture 20240423065713):
  "A seven cell partition of N is constructed with the property that no infinite set has all of its pairwise sums and
  products in any one cell. A related Ramsey Theory question is shown to have different answers for two and three cell
  partitions." (Matches zbMATH's review above.)
- **1980 paper still UNREAD**: ScienceDirect serves a Cloudflare Turnstile even to a real Chrome on the home IP (two
  tries; captcha rule — stopped, one-click ask staged for Patrick on Handoff /links); no Wayback snapshot; no abstract on
  Crossref / Semantic Scholar / OpenAlex; Elsevier coredata says `openaccess=1` but needs an API key.
- ⚠ A web-search summarizer, reading the live ScienceDirect snippet, claimed the 1980 abstract describes BOTH a two-cell
  FP∪FS counterexample AND a seven-cell pairwise-sums-and-products partition. UNVERIFIED. If true, the OpenAI paper's [21]
  and erdosproblems.com's [Hi80] are simply correct and 1984 is a second treatment — which is why the live entry's line
  stays hedged ("later citations and the 1984 abstract place it in 1984; the 1980 PDF unread") and our August item stays
  at (c), not "wrong", until a person reads the 1980 PDF.
