# Independent hostile audit: Erdos problem 773 finite frontier

Audit date: 2026-08-11 UTC.

Target:

`/home/exedev/erdos_scratch/erdos773_n69_frozen_2026-08-11`

## Verdict

**PASS for the stated conditional mathematical result.** Conditional on the
published A390813 prefix values being valid upper bounds through 68, the
bundle proves

```text
a(69) = 32 and a(70) = 33.
```

The two displayed witnesses give unconditional lower bounds at 69 and 70.
I found no model, search-completeness, rollback, pruning, cube-cover, or exit
status defect.

**GAP only in auxiliary packaging/documentation.** `README.md` cites an
`audit_model.py` that is not in the bundle, and one sentence understates the
external premise as just `a(68)=32` even though the DFS uses the full prefix
table. Neither issue invalidates the correctly stated headline theorem or the
freshly reproduced exhaustive run.

## External premise

On 2026-08-11 I independently fetched the live OEIS b-file. It was
byte-for-byte equal to the frozen file and had SHA-256

```text
dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916
```

It contains exactly rows 1 through 68, ending `67 32` and `68 32`. The live
OEIS entry defines the sequence as the maximum Sidon subset of the first `n`
positive squares and still labels the table `n=1..68`. This verifies what is
currently published and the frozen byte provenance; it does not independently
prove that the earlier computational values are mathematically exact.

The live Erdos problem page was also checked through an anti-bot browser. It
still says `OPEN`, links A390813, reports zero claimed proofs, and gives a last
edit date of 24 April 2026.

The DFS actually needs the published values `a(k)` as upper bounds at the
prefixes where it prunes. Exact equality at every prefix is a sufficient but
stronger premise. The reduction that forces index 69 uses only `a(68)<=32`;
the subsequent search uses the earlier prefix bounds too.

## Logical reduction

Map each selected square to its positive index. A collision is a pair of
distinct unordered index pairs `(i,j)` and `(r,s)` with
`i^2+j^2=r^2+s^2`. A chosen index set is invalid exactly when it contains the
union of the vertices in one such collision.

Two independent enumerations, one grouping pairs by their sum and one
quadratically comparing every pair of unordered pairs, produce the same 712
distinct supports at `N=69`: 21 triples and 691 quadruples. Supports cannot
have size two because two distinct normalized unordered pairs cannot have the
same two vertices.

If a valid 33-set in `[69]` omitted 69, it would be a 33-set in `[68]`,
contradicting `a(68)<=32`. Thus it is enough to fix 69 and search for 32 more
indices. Ruling out size 33 also rules out every larger size by heredity: any
larger Sidon set contains a Sidon 33-subset.

The size-32 witness at 69 has 528 distinct unordered sums. The size-33 witness
at 70 has 561. Once `a(69)=32` is known, deleting 70 from any valid set in
`[70]` gives `a(70)<=a(69)+1=33`, so the second witness proves equality.

## Source audit

The audited source is `dfs_hypergraph_coloring.cpp`, SHA-256

```text
eb21d0f429881f61dd5148ab2a41da3fb6b57d1513ea2db656ae3ae69883e933
```

### Support completeness

Lines 412-447 enumerate every normalized unordered pair `1<=i<=j<=69`, group
all representations by exact integer sum, compare every two representations,
deduplicate their vertex unions, and build incidence lists. This is exactly
the forbidden-support characterization. All arithmetic is far below signed
`int` overflow. The hard-coded count check is only a sanity check; completeness
comes from the loops.

### DFS state and rollback

At entry to `search(k, selected_below_69)`, vertices above `k` have been
decided. For every support without an excluded vertex, `support_selected`
counts selected vertices. One remaining vertex contributes a block; two
remaining vertices contribute a pair conflict.

The include branch at lines 354-396 updates every live incident support:

- old remaining count 3 becomes a pair conflict;
- old remaining count 2 becomes a blocked last vertex;
- old remaining count at most 1 is rejected as an internal error;
- reverse rollback removes exactly the transition it added before decrementing
  `support_selected`.

Reference counts make overlapping supports safe. `chosen[k]` remains set
while `remaining_one` and `remaining_two` identify the post-selection
vertices, and it is cleared only after all include updates are undone.

The exclude branch at lines 398-407 increments and later decrements
`support_excluded`. It intentionally does not delete an existing block or pair
for that support. This is sound under descending assignment: any such retained
constraint necessarily contains the newly excluded vertex `k`, which lies
outside the next prefix `1..k-1`. The masks therefore cannot use it below the
branch. When the exclusion is rolled back, every lower decision has also been
rolled back, so the retained count is again current. This was the most subtle
state invariant; I found no missing update.

### Prefix and blocking bounds

At lines 333-345, reaching 32 chosen lower indices returns SAT. Otherwise the
remaining need is positive. Any valid extension within `1..k` is itself a
square-Sidon subset of that prefix, so `prefix_max[k]` is a sound upper bound
under the stated premise. Removing individually blocked vertices gives another
obvious cardinality upper bound. Forced cube bits only remove choices; ignoring
forced-zero bits in these bounds makes them weaker, never unsound.

### Pair-conflict clique cover

A live support with exactly two unassigned vertices means no valid extension
can select both, so every valid extension is an independent set in the current
pair-conflict graph. Lines 273-317 greedily remove disjoint cliques. Each added
vertex is intersected with every prior clique member's neighborhood, so a
completed partition into `q` conflict cliques proves an extension has size at
most `q`.

The early return at lines 281-283 occurs when the number of started parts
reaches `needed`. At that point the returned value need not be a complete-cover
upper bound, but the caller prunes only when the result is strictly below
`needed`. Thus early return is a safe `could not prune` sentinel. The source
comment should describe that nuance, but there is no soundness bug.

### Cubes and process semantics

Cube characters force `x_68,x_67,...` in descending order. The set

```text
00, 010, 011, 100, 101, 110, 111
```

is prefix-free and covers all eight assignments to `(x_68,x_67,x_66)` exactly
once; `00` covers `000` and `001`. The executable returns 10 for SAT, 20 for
UNSAT, 2 for input errors, and 3 for internal invariant failures. The full
reproducer temporarily disables shell `errexit`, records the child status, and
requires exactly 20 plus a strict one-line UNSAT log for every cube.

## Independent execution

`sha256sum -c SHA256SUMS` passed for all 37 listed payload files. The directory
contains 38 files including the manifest itself and is read-only. The archive
expanded byte-for-byte to the directory.

The fast `./reproduce.sh` audit passed. A fresh build with the documented
compiler and flags was byte-identical to the frozen release binary. I then ran
all seven cubes afresh into this separate audit directory. Every process exited
20, every status was `UNSATISFIABLE`, and every deterministic counter matched
the frozen run:

```text
nodes           171546643
prefix_prunes     4255758
blocked_prunes      32738
color_calls      167258147
color_prunes      75651370
```

I also built `ERDOS773_AUDIT` and ASan+UBSan variants. On eight independently
seeded 26-bit cubes, both agreed with a separately rebuilt direct sum-based DFS.
The raw cases included searches of 142,754 and 128,106 nodes; no incremental
invariant or sanitizer failure occurred. A scratch-only target-31 build
exercised SAT exit 10 and emitted a size-32 witness with 528 directly verified
distinct sums.

The scratch `independent_check.py`:

- reconstructs supports by two different enumeration strategies;
- exhaustively proves support avoidance equals the raw distinct-sum definition
  on all 65,536 subsets through `N=16`;
- directly rechecks both published witnesses;
- asks CP-SAT, CaDiCaL, and Glucose for a full 33-set counterexample under the
  published prefix bounds.

The bounded general-purpose probes found no counterexample but ended UNKNOWN:

```text
CP-SAT     60.004 s   1843268 branches   1025610 conflicts
CaDiCaL    20.238 s   250000-conflict budget
Glucose    32.591 s   250000-conflict budget
```

An earlier eight-worker CP-SAT probe was also stopped UNKNOWN after about 12
minutes. These probes are counterexample attempts only and are not counted as
proof; the proof is the reviewed and freshly repeated finite DFS cover.

## Packaging and wording gaps

1. `README.md:114-116` says `audit_model.py` performs an independent model
   check, but the script is absent from the frozen directory and manifest.
   The CNF/LP inputs described by `audit_model.log` are absent too. That log is
   therefore historical evidence, not a reproducible check from this bundle.
   Include its script and inputs, or remove/relabel the reference and log.
2. `README.md:18-20` says the upper proof depends on the published exact
   `a(68)=32` input. The forcing reduction does, but the exhaustive DFS also
   prunes with `a(k)` for earlier `k`. Replace this with: "The upper proof
   depends on the published prefix values `a(1),...,a(68)` as upper bounds;
   this bundle does not independently prove those earlier upper bounds."
3. The source comment at lines 269-272 calls every return from
   `clique_cover_bound` an upper bound. Its early `return needed` is a safe
   no-prune sentinel, not necessarily a completed-cover bound. Clarifying the
   comment would make the proof logic easier to audit.
4. `audit_coloring_invariants.log`, `crosscheck_dfs_variants.log`, and
   `audit_model.log` are checksummed but not regenerated by `reproduce.sh`.
   The first two can be treated as auxiliary historical tests; the full script
   does regenerate the actual seven-cube proof, so this is not a core gap.

## Principal hashes

```text
archive             6cc935660bc809462f8dcd97d6ae3b7fbe4662b8edaca4644e167e5fe98377fa
manifest            26147bd46934590c0a3c34e7aa1650c6c4c5ab43fb9d4e1e70192c107cf81816
README              1e3da49c99cb4dfc7ced51f31cf393d50788741934e528eb095e322a09d70200
OEIS b-file         dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916
DFS source          eb21d0f429881f61dd5148ab2a41da3fb6b57d1513ea2db656ae3ae69883e933
DFS binary/fresh    e9d471fb6df395f0807c21efc2fffbda64403511cd92b8098bb9100eaaa5655a
reproduce.sh        fc5c74284e64d9b0b9813e63dbf7f5c7333fd8f3564c29a9d965113e804281d4
independent checker 8b1728a5016d275a631acbc485eaf4c909ce1716160f53e6174ad630d1aa3720
```
