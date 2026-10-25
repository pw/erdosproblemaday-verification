# Hostile independent audit: Erdos #708, `c_10=2`

Date: 2026-08-11 UTC

## Inputs

Frozen original candidate:

```text
559fb04614bcd9e9d0d7e852ec9cb3da7ac27721f1622e0a1d471821c17a726c  erdos708_c10_candidate.md
e5eeed59f4be5073f4773c559943d03c912dcc8207b96586750b51c649938f2b  erdos708_c10_graph_valuation_audit.py
```

Proposed aligned replacement audited:

```text
3fcb356f84011a7e107db955ec31b9956eb60a1e97b2908e9ae8b496e8f6d024  erdos708_c10_aligned_repair.md
b6cd123061afe0de2a6b303892a63a37eb0aaf289c0e3dc5620540c8e746f4a3  erdos708_c10_aligned_repair_audit.py
27e4ba6cba9eb6e4a5f2174ef4e529e67826ef01d5224469e31bb554c582f9d7  erdos708_c10_aligned_repair_audit.out
```

## Verdict

- **Frozen candidate: GAP.** Lines 462-466 use an invalid product-divisibility
  inference in the aligned case.
- **Aligned replacement: PASS.** I found no gap in the exceptional-layer,
  certificate-robustness, or forbidden-midpoint arguments.
- **Combined proof: mathematically PASS with two editorial corrections below,**
  conditional on the external `c_8`, `c_9`, and lower-bound inputs explicitly
  assumed by the candidate. The finite runs are bug detectors; the uniform
  written arguments are what cover arbitrary integers and valuations.

## Fatal gap in the frozen Section 8

Take `M=10`, `A={1,...,10}`, `I=(0,20)`, and `b_0=10`. The nine distinct
points

```text
C = {1,2,3,4,6,7,9,10,12}
```

have product `3*9!`. Thus `9!` divides `prod(C)`, `10` divides `prod(C)`, and
`b_0` belongs to `C`, but `10*9!` does not divide `prod(C)`. The residual
factor is 10, whose only multiple in `I` is the already-used point `b_0`.
Therefore even an arbitrary unused padding point cannot repair this cover.
This refutes the implication used by the frozen argument; it does not refute
the theorem after the replacement.

## Aligned replacement audit

The corrected injection was checked algebraically and independently in code.
For type (22a), exactness follows from endpoint difference `a`. For types
(22b) and (22c), odd-prime exactness follows from differences `4a` and `2a`.
At `p=2`, the only surplus is a type-(22c) edge with odd `b_0/a`; its endpoint
gcd is exactly `2a`, so it appears at exactly the one extra level
`v_2(a)+1`. Such a label satisfies `2a>M`, and all such symmetric edges form a
matching. No other exceptional layer occurred in the arithmetic exhaustion.

The robustness reduction is sound. At an endpoint level with divisible vertex
set `W`, deleting an anomalous demanded edge retains both endpoint
contributions. A proper induced level of a no-core nine-edge graph or `K_3,3`
has excess at most one, so one deletion removes all deficit. At the full
no-core level, a deletion destroys only one side of the fixed `4+5`
partition. For `K_3,3`, choose a row-column pairing disjoint from the global
exceptional matching; each exceptional edge then lies in exactly one of the
three `K_2,2` blocks. This leaves at least `3-|Y|` blocks at a full level.
Assignments are made only to blocks contained in the actual label-level graph,
so their accumulated factors retain the advertised label support.

Every forbidden-`b_0` placement count also checks:

- A factor dividing `k` distinct labels below `M` satisfies `kd<=M-1`, giving
  at least `2k` multiples in the open interval.
- The one-defect case has at least 12 multiples against nine forbidden points.
- In a hard eight-edge core, a four-edge support has at least eight multiples.
  If all were in the seven selected points plus `b_0`, every core vertex would
  be divisible. The complementary four-block has a nonexceptional edge because
  an exceptional matching on six vertices has size at most three; this forces
  a fifth label and at least ten multiples.
- In a no-core nine-edge graph, the five-block factor has at least ten
  multiples. If the four-block factor were trapped in the seven vertices plus
  `b_0`, the complementary five-block likewise contains a nonexceptional edge,
  forcing a fifth supported label.
- In `K_3,3`, the strict counts are 8 per individual factor, 14 for a common
  pair factor, and 18 for a common triple factor. Together with the proved
  nine-point progression lemma, these establish Hall outside `b_0`.

Thus the replacement constructs nine points avoiding `b_0`, after which
adjoining `b_0` supplies a fresh factor divisible by `M` without valuation
reuse.

## Independent checks

`independent_audit.py` does not import either supplied checker. It reports:

```text
all-edge-submask critical kernels:
  q=2,e=8: 1 K_2,4 labelling and 9 K_3,3-e labellings
  q=2,e=9: 96 K_3,4 labellings
  q=2,e=10: 210 (3,5) and 2040 (4,4) labellings
  q=3,e=9: 1 K_3,3
  q=3,e=10: 1 K_2,5 and 54 minimal K_3,4-minus-two labellings
aligned no-core graph/exceptional-matching pairs: 3888
K_3,3 exceptional matchings: 34
corrected-injection instances through M=150: 894
K_2,5 capped valuation vectors: 279936
full-residue AP checks: 1490468
concrete K_2,5 interval configurations: 317
actual small c10/c9 interval instances: 3000
exhaustive aligned b_0-avoiding instances, 10<=M<=16: 48048
```

The supplied frozen checker and supplied repair checker were also rerun and
matched their recorded successful outputs.

## Exact editorial corrections

1. Candidate lines 309-326 include the 12 same-column deletions of `K_3,4`
   among the three-defect minimal kernels. Those graphs contain a proper
   `K_3,3`, so only the 54 same-row/disjoint deletions can be inclusion-minimal.
   The displayed same-column certificate is valid, so checking this extra case
   is harmless; describe it as redundant rather than minimal.
2. Candidate lines 426-429 omit the `n_2=n_3=0` branch in the `K_2,5`, `t=2`
   argument. In that branch `n_1=5`; choosing `m_0=1` gives `C=5`, contradicting
   `4C-1<=9`. Add this sentence. The existing argument handles every other
   branch.

No concurrency, integer-width, or nondeterminism issue applies to the Python
checkers. All enumerations are single-threaded exact integer computations.
