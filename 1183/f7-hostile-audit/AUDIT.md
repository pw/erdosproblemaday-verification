# Hostile audit: Erdős Problem 1183, exact `f(7)=4` and `F(7)=7`

Date: 2026-08-12 UTC

## Verdict

**PUBLISH.** I found no mathematical, certificate, provenance, scope, or
packaging blocker in the final producer bundle.

Audited producer target:

```text
bundle directory              /tmp/erdos1183_f7_exact
SHA256(SHA256SUMS)            7bb52e939edf5f79369b29e3fad24c8f9e18ba9cf691349690cfbf012fc5b26a
SHA256(REPORT.md)             f11654c92a00732c405113362421c969fa14b9b0d078ba3a86e8a8eb2ee42bf2
SHA256(lower_core.cnf)        7b1c05b745e0ca661232a1d478c855bcb4685f0d00abb291066efe9be9eda5fb
SHA256(lower_core.drat)       92db723a46d0db7dabebef7c3633bfd4dfca6ca6d26fdcfabb2fed216aaa0fa5
```

The final `./reproduce.sh` replay passed from the closed bundle.

## Live gate and provenance

I independently fetched the live page and oldest-first forum through Bright
Data after ordinary retrieval was rejected. The independent page capture is
byte-identical to the frozen `LIVE_PAGE.txt` (SHA-256
`657f2da0fc0c75520a6bbc34b0a98553a140fa19ea0f4d97b68824b675f6b3b3`).
The forum capture differs only in MathJax/layout whitespace; after deleting
whitespace, both have SHA-256
`ff40a0bcc8c0ca9ded2283dddd660a5643e3bdf1a2f9066ed95caea713593300`.

Both independently show `OPEN`, zero claimed proofs, no current worker, no
collaborator, no formalisation worker, and ten comments. The ten comments
discuss asymptotic manuscripts and checks; none claims either finite value.
Targeted web searches found no matching `f(7)`/`F(7)` claim for this problem.
The report makes no novelty or priority claim.

The prior table through `n=6` is genuinely present in the project's published
ledger and in MathDyad commit `964e423274492ca7e0530ba4e37fbdb0e82282b5`.
The earlier checker has SHA-256
`2179c5bbb3ac567dace8dc33d052e7f3353f5c1e0525f6c9efa878cc570d396f`
and independently replayed to the stated two rows.

## `F(7)` lower bound

I parsed the DIMACS independently rather than trusting the producer parser.
The first clause is exactly `-1`, so variable 1 (the empty mask) is fixed
blue. This is without loss of generality under a global colour swap. Every
remaining clause has exactly seven distinct, in-range masks, a uniform sign,
and a family closed under bitwise union. Canonicalisation found no duplicate
signed family. Counts are exactly:

```text
42,035 total clauses = 1 symmetry unit + 42,034 family clauses
22,232 all-negative clauses forbidding all-red families
19,802 all-positive clauses forbidding all-blue families
```

Thus unsatisfiability of this CNF has precisely the claimed implication. A
fresh direct CaDiCaL run returned `UNSATISFIABLE`. The included binary
`drat-trim` replay returned `s VERIFIED`. I also compiled the previously
published Problem 813 `drat-trim.c` from source to a different executable and
replayed this proof; it again returned `s VERIFIED`, with 35,488 input clauses
and 135,485 lemmas in the final RUP core and zero RAT lemmas.

## `F(7)` upper bound

For the rank colouring red on ranks `3,4,6`, the displayed witnesses are
correct and union-closed. I checked the elementary case split in the report:

- without a six-set, the amended four-set/no-four-set split is complete;
- with the unique six-set `S`, complements of selected four-sets are disjoint
  pairs in `S`; the four cases `b=0,1,2,3` give `a+b<=5`;
- in blue, there is at most one selected two-set, five-set complements are
  disjoint pairs, and the two subcases according as `[7]\\E` is selected give
  totals at most six and seven.

A clean-room closure-propagating C++ search, with a different state
representation and recursion, independently returned exact colour maxima
`6,7`. It was also run under ASan/UBSan and libstdc++ debug mode.

Together with the lower certificate, this proves `F(7)=7`.

## `f(7)`

The lower bound is elementary: among the eight members of a maximal Boolean
chain, four have one colour, and every subchain is closed under union and
intersection.

For the upper bound, the displayed red ranks `0,2,3,5`, blue complement, and
the two four-member chain witnesses are correct. The clean-room exact search
returned maxima `4,4`.

As a separate audit, `hostile_audit.cpp` enumerates every five-subset of both
colour classes and computes its generated union/intersection closure with a
frontier algorithm independent of the producer implementation. Results:

```text
blue:  2,118,760 five-seed choices; 0 monochromatic closures
red:  21,111,090 five-seed choices; 0 monochromatic closures
```

This is a complete upper certificate: if a monochromatic sublattice had at
least five members, any five of its members would generate a closure contained
in that sublattice. Hence `f(7)=4`.

## Correction history and scope

The first frozen draft compressed the no-six/no-four red subcase into an
ambiguous pronoun. During this audit it was replaced by the explicit two-case
argument now in `REPORT.md`; the target hashes above are for the corrected and
replayed bundle. There are no outstanding corrections.

The `PARTIAL` label is accurate. These two fixed finite values do not settle
either asymptotic question in Problem 1183. The x86-64 limitation of the
included DRAT checker is disclosed, all substantive artifacts and frozen
outputs are manifest-bound, and the reproduction script checks the complete
manifest before executing anything.

## Independent audit output

Compile and run from this audit directory:

```sh
g++ -O2 -std=c++20 -Wall -Wextra -Wpedantic -Werror \
  hostile_audit.cpp -o hostile_audit
./hostile_audit /tmp/erdos1183_f7_exact/lower_core.cnf
```

The expected transcript is `OUTPUT.txt`.
