# Erdos problem 1160: exact finite certification at m=11

Audit date: 2026-08-11 UTC

## Certified statement

Let `g(n)` be the number of isomorphism classes of groups of order `n`. This
bundle certifies

```text
sum_{0 <= n < 2048} g(n) = 49,910,538,480
                         < 1,774,274,116,992,170
                         <= g(2048).
```

Here `g(0)=0` is only the OEIS bookkeeping convention, so this is the same
sum as the positive-order sum in the problem.

Therefore the stronger conjecture in Question 22.18 holds at `m=11`. It also
implies the original problem's inequality `g(n) <= g(2048)` for every
`1 <= n <= 2048`.

This is a finite partial result. It does not determine `g(2048)`, prove the
statement for `m >= 12`, or settle either asymptotic conjecture.

## Proof

Conway, Dietrich, and O'Brien tabulate `g(n)` for `0 < n < 2048` and state
that the groups at all orders other than 1024 total 423,171,191. Their 2008
value at 1024 was later corrected.

Burrell proves the corrected value

```text
g(1024) = 49,487,367,289.
```

Burrell identifies the sole error in the earlier enumeration: one immediate
descendant count was recorded as 933 instead of 2800. Consequently

```text
sum_{0 <= n < 2048} g(n)
  = 423,171,191 + 49,487,367,289
  = 49,910,538,480.
```

Eick's 2024 survey gives the exact number

```text
f_2(2048) = 1,774,274,116,992,170
```

of groups of order 2048 having lower 2-central series of length 2, and states
`f_2(2048) <= g(2048)`. The gap from the entire below-2048 sum to this subset
alone is 1,774,224,206,453,690. This proves the displayed strict inequality.

## Independent finite audit

The downloaded OEIS A000001 b-file has one row for every index 0 through 2047
and directly sums to 49,910,538,480.

For a separate reconstruction, GAP 4.12.1 with SmallGrp 1.5.3 returns counts
at 2034 of the 2047 positive orders. Every returned value agrees with the
OEIS file. The 13 unavailable orders are

```text
2002, 2004, 2010, 2016, 2020, 2024, 2025,
2028, 2030, 2034, 2040, 2044, 2046.
```

Their values are parsed from the final appendix rows in the 2008 paper. The
2034 GAP counts plus these 13 appendix counts independently reconstruct all
positive indices through 2047 and produce the same total. The pinned Ubuntu
packages are included, and `reproduce.sh` regenerates and byte-compares the
GAP output.

## Live and novelty gate

The rendered problem and discussion pages were frozen on 2026-08-11. They
show:

- status OPEN;
- zero claimed proofs;
- no current worker;
- three comments, none claiming the `m=11` inequality.

Snapshots of the local site's `src/index.js` and `src/ledger_data.js` have no
exact decimal token `1160` under the regex `(?<![0-9])1160(?![0-9])`.
The larger ledger snapshot does contain incidental `1160` digit substrings
inside unrelated larger decimal values; those are not references to problem
1160.

Targeted live searches for the exact sum, the `m=11` instance of Question
22.18, and a sum comparison with `g(2048)` found no relevant public result.
The frozen search pages record the queries. This is a dated, qualified search
miss, not proof of absolute novelty or absence from unindexed literature.

## Reproduction

Run from this directory:

```bash
./reproduce.sh
```

The script checks every frozen hash, runs two separately written arithmetic
audits, recreates the GAP runtime from pinned packages, regenerates all 2034
available counts, and byte-compares them with the frozen output.

Status at freeze time: proof-level finite result, awaiting hostile external
audit. No PASS or absolute novelty claim is made in this bundle.
