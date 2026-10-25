# Problem 156: exact A382397 values through 136

These bundles certify

```text
a(66) = a(67) = 6,
a(n) = 7 for 68 <= n <= 101,
a(n) = 8 for 102 <= n <= 136.
```

Here `a(n)` is the minimum size of a maximal Sidon subset of `{1,...,n}`.
This extends the finite OEIS A382397 table; it does not solve the asymptotic
Erdos problem.

## Extension from 103 through 136

The newest certificate is in [`extension_103_136/`](extension_103_136/). It
contains two complete max-135 seven-mark searches, complete searches through
six marks, direct checks of all 35 upper witnesses, and a hostile audit with a
third seven-mark implementation and independent one-tree enumeration through
six marks. Reproduce it with:

```bash
cd extension_103_136
./reproduce.sh
```

## Extension from 96 through 102

The new certificate is in [`extension_96_102/`](extension_96_102/). It adds a
complete seven-mark enumeration, three size-at-most-six enumerators, direct
witness checks, frozen logs, and an independent hostile audit. Reproduce it
with:

```bash
cd extension_96_102
sha256sum -c SHA256SUMS
./reproduce.sh
```

The exhaustive seven-mark run checks every normalized ruler with diameter at
most 101. An independent unpruned audit visits all
`C(101,6)=1,267,339,920` raw seven-mark combinations. Both find longest
blocked run 101 at `{0,24,27,35,39,41,75}` on `[-17,83]`. This gives the
seven-mark upper bounds through 101 and rules out seven marks at 102. The
eight-mark set `{10,33,38,42,59,69,71,89}` is directly verified maximal in
`{1,...,102}`.

## Original certificate through 95

The proof and completeness reduction are in [report.md](report.md). That is an
editorially corrected public copy; the hash-frozen original and its manifest
are preserved as `erdos156_A382397_exact_66_95_audit_2026-08-11.md` and
`erdos156_A382397_exact_66_95_manifest_2026-08-11.sha256`. The two C++
programs use different central representations: positive differences in
`verify_156_a66.cpp`, and unordered pair sums in
`audit_156_size6_sums.cpp`. The Python witness checker directly verifies all
30 original upper certificates.

Reproduce the diameter-94 lower-bound enumeration and witnesses with:

```bash
sha256sum -c erdos156_A382397_exact_66_95_manifest_2026-08-11.sha256

g++ -std=gnu++20 -O3 -Wall -Wextra -DVERIFY_156_N=95 \
  verify_156_a66.cpp -o /tmp/verify_156_differences
/tmp/verify_156_differences

g++ -std=c++20 -O3 -Wall -Wextra \
  audit_156_size6_sums.cpp -o /tmp/verify_156_sums
/tmp/verify_156_sums

python3 check_156_witnesses_66_95.py
```

The `*.log` files preserve the original runs. Three hostile audits rebuilt the
enumerators, reproduced all reported counts under ASan/UBSan, checked the
blocking reduction separately, and directly tested all 2,207 outside
insertions across the 30 witnesses. The frozen `audit2/` bundle adds a third
unpruned enumerator which checks each insertion directly from positive
differences. All audits passed.
