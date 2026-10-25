# Hostile audit: Erdős #864 target-20 bundle

Date: 2026-08-12 UTC

Audited bundle: `/tmp/erdos864_target20_audited`

## Verdict

**PUBLISH.** I found no mathematical, coverage, implementation, or integrity
defect that blocks the computational-only claim

```text
F(135)=...=F(152)=19, F(153)=20.
```

One nonblocking wording refinement is recommended before freezing a new
manifest: in `REPORT.md`, replace “Every center from the core's own lower
bound through 151 is searched” by “Every parity-admissible center from the
core's own lower bound through 151 is searched.” Odd core sizes require an
even reflection sum, and the later tables already state this correctly.

## Integrity and replay

- `sha256sum -c SHA256SUMS`: PASS for all 25 manifested payload files.
- `python3 replay_checks.py`: PASS.
- Every top-level payload file other than `SHA256SUMS` is represented in the
  manifest.
- Bundle-manifest SHA-256:
  `2325b08929a2d8cfa1e60c8008ea40eb79b2685e3e2448dc16569c185724e25e`.
- Frozen independent-audit transcript SHA-256:
  `ad32da079c400787744444bd48e6538eca314b0b05c60b6f45668cf00cdaaec3`.
- Direct sliced results SHA-256:
  `399259ad2a677389c4a65c4e8d7d81cab832bc8c5451210e14bf119320a6deb1`.
- Direct whole results SHA-256:
  `bb3c5eb13fe7c5dd839b51909a6f667d6ad6591a21036c67f74fbf2a4359c338`.

I separately parsed all 243 canonical direct `RESULT` rows, ignoring the
bundle's coverage scripts. The parity-admissible center sets were exact:

```text
r=20: T=100..151       (52 centers)
r=19: T=90,92,..,150   (31 centers)
r=18: T=81..151        (71 centers)
r=17: T=72,74,..,150   (40 centers)
r=16: T=64..151        (88 centers)
r=15: T=56,58,..,150   (48 centers)
r=14: T=49..151       (103 centers)
```

There were no duplicate or missing centers, every row had `found=0`, and
every direct `complete_cores` count equaled its `valid_cores` count. The
SHA-256 of my timing-independent semantic serialization of those 243 rows is
`8b1a7015e76b7d085b1340363eebd9afd7cad7fa24df0e63c5251913bda2b848`.

I also rebuilt `search20_direct.cpp` independently and reproduced selected
zero-result slices, including a nonempty-valid-core case (`r=14,T=69`):

```text
orbit_nodes=13443 complete_cores=3 valid_cores=3 extension_nodes=119
```

An independent ASan+UBSan build reproduced the cap-152 positive control with
`found=1`, 18,689 orbit nodes, the frozen witness, expected exit status 2,
and no sanitizer diagnostic.

## Definition, witness, and exact inference

An independent definition-level recount of the proposed normalized witness

```text
0 1 6 10 23 26 34 41 53 55 97 99 111 118 126 129 142 146 151 152
```

found 210 diagonal-inclusive unordered pairs, 201 represented sum values,
and exactly one repeated value: sum 152 with ten representations. Its 190
positive-difference occurrences comprise 90 values of multiplicity two and
10 values of multiplicity one. Translation by one therefore gives a valid
20-set in `[1,153]`. The prior diameter-134 19-set is also rechecked directly
in the bundle.

The finite inference is exact. The published prior result gives `F(135)=19`;
monotonicity gives the lower bound through 152. Exhaustion of every 20-set of
diameter at most 151 gives `F(N)<=19` for `N<=152` (a larger valid set would
contain a valid 20-subset). Finally, deleting 153 from any valid set proves
`F(153)<=F(152)+1=20`, and the translated witness gives equality.

## Completeness reduction

The reflected-core reduction is sound:

1. With no repeated sum, all 190 positive differences are distinct, already
   impossible under diameter 151.
2. If `sigma` is the sole repeated sum, two representations of the same
   positive difference reflect into each other about `sigma/2`; hence every
   positive difference has multiplicity at most two.
3. For `q` representations of `sigma`, the exact reflected core has size
   `2q` without a midpoint or `2q-1` with one. The duplicated-difference
   counts are respectively `q(q-1)` and `(q-1)^2`.
4. Subtracting these from 190 retains exactly core sizes 20 through 14, with
   lower bounds 100, 109, 118, 126, 134, 141, and 148. The next core size 13
   needs diameter at least 154, so no case is omitted.
5. Normalizing the exact core to `[0,T]` makes its lower half a Golomb ruler.
   Relative outliers necessarily lie in `[T-151,151]`; excluding the midpoint
   and reflection partners is exactly the condition that they stay outside
   the exact core. Increasing-order enumeration is exhaustive.

Both sources implement those bounds correctly. In particular, the direct
source includes the even-core endpoint `(T-1)/2`, while the audit reaches the
same endpoint independently through `T>=2*largest+1`. Odd cores visit exactly
the even `T` values. Neither frozen implementation applies the retracted
total-diameter lower bound as a core-center cutoff.

The independent audit's seven valid-core counts agree with the direct
enumeration exactly:

```text
r=20          0
r=19        489
r=18    240837
r=17    758979
r=16  27176695
r=15  11169166
r=14 109972454
```

The programs' extension-node counts appropriately differ because their
outlier traversal state and order differ. The independent audit freezes
additional order-sensitive core digests and ends with exit 0 and the explicit
exhaustion conclusion.

## Publication wording

Keep the labels “computational-only” and “finite exact extension.” Do not
describe this as resolving Problem #864 or its asymptotic conjecture. The
draft MathDyad section uses the correct scope and exact-value inference.
