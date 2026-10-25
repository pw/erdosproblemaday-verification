# Hostile independent audit: Erdos Problem 1160, m=11

Audit date: 2026-08-11 UTC

Audited bundles:

- `/home/exedev/erdos_scratch/erdos1160_m11_20260811`
- `/home/exedev/erdos_scratch/erdos1160_m11_20260811_v2`

## Verdict

**v2: PASS.** The finite mathematical claim, source chain, frozen inputs,
manifest, and read-only reproduction all pass independent checks.

**v1: GAP (presentation only).** Its verifier's final display used `>=` where
the asserted and proved chain was

```text
49,910,538,480 < 1,774,274,116,992,170 <= g(2048).
```

That line was misleading even though the surrounding assertions, report, and
conclusion were correct. v2 replaces it with the full correct chain. No other
mathematical change occurs between the two bundles.

## Exact statement and scope

I downloaded and visually inspected the scan of Va99, Problem 5.71. It states
that, with `g(n)` the number of groups of order `n`, if `n <= 2^m` then
`g(n) <= g(2^m)`. The source-page image is frozen as
`va99_problem_5_71_page.jpg`. This agrees with the current website's exact
LaTeX; the rendered text loses the superscript formatting, so the LaTeX is
the controlling live transcription.

The website also attributes to BNV07, Question 22.18, the stronger conjecture

```text
sum_{n < 2^m} g(n) <= g(2^m)
```

for all sufficiently large `m`, perhaps from `m=7`. The audit establishes
only the single case `m=11`. It does not establish an eventual threshold,
any case `m >= 12`, an exact value of `g(2048)`, or an asymptotic statement.

## Independent count reconstruction

I did not import either supplied Python verifier. `independent_verifier.py`
was written separately and performs these checks:

1. It parses every one of the 2047 positive-order cells in the complete 2008
   Conway-Dietrich-O'Brien appendix. The only disagreement with the current
   OEIS b-file is the known stale entry at order 1024.
2. It regenerates 2043 available order counts with the machine's independent
   GAP 4.14.0 / SmallGrp 1.5.4 route. The only unavailable orders below 2048
   are 2016, 2024, 2025, and 2040; their values are cross-checked against the
   printed appendix.
3. It separately checks the author's pinned GAP 4.12.1 / SmallGrp 1.5.3
   output for 2034 available orders. The five frozen Ubuntu packages match
   the SHA-256 values in authenticated APT metadata.
4. It verifies all current OEIS b-file indices `0..2047`, including the
   bookkeeping convention `g(0)=0`, and confirms that the live b-file is
   byte-identical to the frozen file.

Both GAP routes and OEIS ultimately inherit SmallGroups enumeration data, so
they are not epistemically independent enumerations of billions of groups.
The complete printed-appendix parse plus Burrell's correction is the
decorrelated published-source route. This limitation does not affect the
finite deduction but should not be described as a new classification.

The independently recovered values are:

```text
Conway total at all non-1024 orders below 2048:       423,171,191
Burrell corrected g(1024):                         49,487,367,289
sum_{1 <= n < 2048} g(n):                          49,910,538,480
```

The 2008 printed value for `g(1024)` was 49,487,365,422. Burrell proves the
correct value and identifies the sole enumeration error as a descendant count
recorded as 933 instead of 2800; the difference is exactly 1867.

Burrell's printed Table 3-3 contains a separate one-unit marginal blemish:
the displayed row margins sum to theorem total minus one, and the displayed
column margins sum to theorem total plus one. `check_burrell_table.py`
recomputes this directly. This does not undermine the cited value: the
theorem, explicit `933 -> 2800` correction, GAP count, OEIS entry, and Eick's
later survey agree. v2 now discloses the blemish and does not use either
printed margin.

## The 2048 lower bound

Eick defines `f(n)` as the number of groups of order `n` and `f_2(2048)` as
the number of groups of order 2048 whose lower 2-central series has length 2.
The paper gives

```text
f_2(2048) = 1,774,274,116,992,170
```

and explicitly states `f_2(2048) <= f(2048)` while the full `f(2048)` remains
unknown. Thus this is an exact subclass count, not an estimate being silently
treated as a lower bound. With `g=f`, the certified margin is

```text
1,774,274,116,992,170 - 49,910,538,480
  = 1,774,224,206,453,690 > 0.
```

Therefore

```text
sum_{n < 2^11} g(n) < f_2(2048) <= g(2048).
```

All summands are nonnegative. Hence every `g(n)` for `1 <= n < 2048` is at
most the sum and is strictly below `g(2048)`; at `n=2048`, the original
inequality is equality. There is no `g(0)` off-by-one: OEIS's artificial zero
entry contributes zero and positive-order groups begin at `n=1`.

## Bundle and reproduction audit

The v1 `SHA256SUMS` file has SHA-256
`2289951ca13d7a86e9878ac22b9f9d1d4185589545dca689e5ef1b403221525f`.
It has one unique entry for every non-manifest file and no extra entry.

The v2 `SHA256SUMS` file has SHA-256
`8cb5c802c759c3a2dc12fd3e203e00abb991bfaae5376e44ebaa71e48da6dd90`.
It likewise covers all 30 non-manifest files exactly. A recursive comparison
shows that v2 changes only `verify_erdos1160_m11.py`, `REPORT.md`,
`PROVENANCE.md`, and the corresponding manifest hashes. The mathematical
inputs, source PDFs, b-file, GAP packages, count output, and both audit
programs are otherwise byte-identical.

I ran `./reproduce.sh` from the read-only v2 directory. It validated all
hashes, compiled both bundled verifiers in memory, emitted the corrected
inequality chain, passed both arithmetic audits, rebuilt the pinned GAP
runtime in a temporary directory, regenerated all 2034 available values, and
byte-compared them successfully. Exit status was zero. The independently
written verifier also passed against both v1 and v2. No author-bundle or site
file changed during this audit.

## Live state and novelty wording

Independent live captures on 2026-08-11 showed Problem 1160 as OPEN, with
zero claimed proofs, no current worker, and three comments; none claimed this
`m=11` calculation. The current OEIS b-file and all three current source PDFs
were byte-identical to the frozen copies.

The local publication-surface snapshots `src/index.js` and
`src/ledger_data.js` contain no exact standalone token `1160`. This is a
qualified source-surface gate, not a claim that the digit string never occurs
elsewhere in the repository. Targeted searches found no prior public statement
of the exact finite result. That supports only the bundle's dated search-miss
wording; it does not prove absolute novelty or rule out unindexed literature.

## Reproduce this audit

From this audit directory, run:

```bash
./reproduce_audit.sh /home/exedev/erdos_scratch/erdos1160_m11_20260811_v2
```

Primary logs are `independent_verifier_v2.log`,
`reproduce_v2_readonly.log`, `gap_414_counts.txt`,
`burrell_table_arithmetic.log`, `source_immutability.log`, and
`current_source_pdf_hashes.log`. `AUDIT_SHA256SUMS` inventories the complete
frozen audit directory except itself.
