# Erdos problem 1131: literature and novelty-boundary audit

Frozen: 2026-08-11 UTC.

## Verdict

* `PASS` for publication of the finite exact `n=4` theorem as a rigorously
  certified partial result, provided it is described as an exact certificate
  rather than as discovery of the optimizer or its decimal value.
* `GAP` for any claim that the exact theorem, critical polynomial, or minimum
  polynomial is new. The complete 1997 article could not be inspected through
  the publisher's nominally open full-text route, so no priority claim is
  justified.
* The `n=4` numerical minimum is definitely prior work: Brutman--Toledano's
  official abstract says that they numerically found high-precision minimum
  values for every `n=3,...,100`. Their computation also necessarily found a
  numerical optimizing configuration; without the table in hand, do not quote
  its digits or say exactly how it was tabulated.

The safe contribution statement is:

> Brutman and Toledano (1997) numerically computed high-precision minima for
> `n=3,...,100`, so the four-node optimizer and minimum were already known
> numerically. Here we give an independently checkable exact global certificate
> for `n=4`, including algebraic characterizations of the optimizer and minimum.
> We make no claim of priority for the exact formulas.

## The 1997 primary record

L. Brutman and D. Toledano, "An extremal problem of Erdos in interpolation
theory," *Computers & Mathematics with Applications* 34(12) (1997), 37--47,
DOI `10.1016/S0898-1221(97)00232-0`, PII `S0898122197002320`.

Primary locators:

* DOI: <https://doi.org/10.1016/S0898-1221(97)00232-0>
* Publisher record: <https://www.sciencedirect.com/science/article/pii/S0898122197002320>
* Elsevier API metadata: <https://api.elsevier.com/content/article/pii/S0898122197002320>
* Crossref record: <https://api.crossref.org/works/10.1016%2FS0898-1221%2897%2900232-0>

The official abstract explicitly characterizes the work as numerical. It says
that the authors used an optimization technique to find high-precision minimal
values for `n=3,...,100`, then used Richardson extrapolation to obtain two
asymptotic terms and disprove the 1994 conjecture. It separately describes an
analytic node description as heuristic and practically near-optimal.

Accordingly, the abstract supports:

* prior numerical data at `n=4`;
* a numerical optimizer/minimum computation, not merely an upper bound;
* asymptotic numerical extrapolation and a heuristic node model.

The abstract does **not** claim an exact algebraic equation at `n=4`, an exact
first-order system, a proof that the reported numerical point is the global
minimum, or uniqueness. Absence from an abstract is not proof of absence from
the article; those questions remain unresolved in this audit.

## Full-text acquisition boundary

The publisher metadata returned:

```
openaccessArticle=true
openaccessType=Full
openArchiveArticle=true
openaccessUserLicense=http://www.elsevier.com/open-access/userlicense/1.0/
```

Crossref also records the version-of-record open-access license beginning
2013-07-17 and supplies Elsevier text-mining links. Anonymous API retrieval,
however, returned only minimized metadata. A real anti-bot browser completed
the ScienceDirect PDF JavaScript challenge, but the final handoff went through
Elsevier identity authorization and ended at HTTP 403. No article PDF or XML
body was obtained or retained.

An Internet Archive scan of the complete issue was also identified at
<https://archive.org/details/sim_computers-mathematics-with-applications_1997-12_34_12>.
Its OCR and PDF are marked private/print-disabled, and were not bypassed or
downloaded. The issue metadata reports journal pages 37--47 within a 165-leaf
scan, but gives no lawful anonymous access to those leaves.

Local source-snapshot hashes (temporary source bytes were not copied into this
audit directory):

```
14bccef80015a5cc115577b7bb7bdb09d3cc53c755b5856aef9967b0d26d7f4e  Elsevier minimized XML metadata (1971 bytes)
f19bf1f09ae7daad57e919791781d0f10b52e07e4748064abdba5d740c446f5a  Crossref JSON record (6225 bytes)
d1eed99ca8152d899071a53e4ecba87801ef3315c552e4f3ddf5cc772bf069d5  Internet Archive BookReader metadata (85097 bytes)
```

The Internet Archive metadata reports, but this audit did not retrieve, its
whole-issue OCR hash `sha1:7bb3ad4934b322ca0647dc163f8dee2373271ebb`
and whole-issue PDF hash `sha1:532780f57753237cb504aec2888fd2c1bff22792`.

## References cited in 1997

The publisher/Crossref reference list has 16 entries. The most relevant prior
items are Fejer (1932), Erdos (1961, 1968, 1995), Szabados (1966), Balazs
(1978), and Erdos--Szabados--Varma--Vertesi (1994). None has a title indicating
an exact small-`n` solution of this integral problem. That is only a triage
observation; the cited works were not exhaustively re-audited for hidden
small-case calculations.

## Current problem page and comments

Primary locators:

* <https://www.erdosproblems.com/1131>
* <https://www.erdosproblems.com/forum/thread/1131?order=oldest>
* <https://www.erdosproblems.com/forum/thread/1131?order=newest>

As indexed in August 2026, the page remains `OPEN`, carries no current-worker
tag, and has five comments. The comments materially affect wording:

* On 7 April 2026, Alfaiz pointed to `[BrTo97]`.
* On 26 April 2026, Liam Price linked a GPT-5.5 Pro claimed disproof of the
  proposed asymptotic.
* On 27 April 2026, Nat Sothanaphan replied that a standard check found no issue
  and explicitly noted that Brutman--Toledano had already supplied numerical
  evidence against the asymptotic.

Thus `zero claimed proofs` is not an accurate unqualified description of the
live record. A precise gate statement is: "No formal proof record or current
worker tag was present; comments already contained an asymptotic claimed
disproof and the 1997 literature pointer." None of those comments states the
exact finite `n=4` certificate audited here.

## Later source check

R. Zeraoulia's non-peer-reviewed 2026 preprint is at
<https://www.preprints.org/manuscript/202601.0875>. It does not cite
Brutman--Toledano. It is not usable as verification of the finite theorem: its
equation (32) asserts `I_n=2-2/n` for the Legendre-integral nodes, whereas direct
exact integration at `n=4` gives `12/7`, not `3/2`. The preprint is also
explicitly conditional at its main endpoint-universality step.

Exact-string searches on 2026-08-11 found no indexed mathematical hit for any
of:

```
21 a^6 + 9 a^4 + 3 a^2 - 1
0.4306647114096755
165375 L^3 - 519750 L^2 + 491040 L - 146912
```

This is a search-limited negative, not evidence of novelty.

## Compared frozen theorem

Compared against
`/home/exedev/erdos_scratch/audit_erdos1131_n4_exact_20260811`:

```
7e23d005c821296425a1150dfdcd57aa1cc496a5e8e692f5aada11afaaa04b59  README.md
2f545afd2af1b807f01074c426a7c12eedbf36463c4820a8012cd276ac76b5db  MANIFEST.sha256
1fc5aaed3d178132e4f5c81d878e846eb60390cb9ed3a16fc80a2360780e60a8  verification.log
```

The theorem's mathematical scope is compatible with the literature record:
it is an exact finite partial result and does not settle the asymptotic problem.
The only required publication edits are the conservative attribution above and
the corrected live-comment gate wording.
