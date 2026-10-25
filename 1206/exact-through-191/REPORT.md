# Erdős problem #1206: exact cube-Sidon table through 191

Access and computation date: 2026-08-12 UTC.

## Conservative result

For

\[
g_3(N)=\max\{|I|:I\subseteq\{1,\ldots,N\},\ \{i^3:i\in I\}
\text{ is Sidon}\},
\]

the previously published exact table on Erdős Problem a Day ended at
\(N=131\), with \(g_3(131)=111\).  Definition-level exhaustive computation
now proves every next value through \(N=191\):

| inclusive range for \(N\) | exact transversal number \(\tau_N=N-g_3(N)\) | exact value |
|---:|---:|---:|
| 132–133 | 21 | \(g_3(N)=N-21\) |
| 134–137 | 22 | \(g_3(N)=N-22\) |
| 138–143 | 23 | \(g_3(N)=N-23\) |
| 144–155 | 24 | \(g_3(N)=N-24\) |
| 156–160 | 25 | \(g_3(N)=N-25\) |
| 161–164 | 26 | \(g_3(N)=N-26\) |
| 165 | 27 | \(g_3(165)=138\) |
| 166–171 | 28 | \(g_3(N)=N-28\) |
| 172–173 | 29 | \(g_3(N)=N-29\) |
| 174–179 | 30 | \(g_3(N)=N-30\) |
| 180–185 | 31 | \(g_3(N)=N-31\) |
| 186–191 | 32 | \(g_3(N)=N-32\) |

In particular,

\[
\boxed{g_3(191)=159.}
\]

This is only an exact finite extension.  It does not prove the requested
linear asymptotic lower bound, and it does not address the coherence needed
for an infinite positive-density set.

## Fresh live-page collision gate

The live page and both forum routes were fetched through Bright Data on
2026-08-12, before doing the mathematics:

- <https://www.erdosproblems.com/1206>
- <https://www.erdosproblems.com/forum/discuss/1206>
- <https://www.erdosproblems.com/forum/thread/1206/proof-claims>

The rendered live page said `OPEN`, `0 claimed proofs for this problem`,
`Currently working on this problem None`, and `Interested in collaborating
None`.  It was last edited 08 April 2026 and displayed two comments.  The
discussion route contained only Kevin Barreto's comment about Tait's
\(N^{8/9}\) lower bound and Woett's comment about the 1729 counterexample to a
different comparison question.  The separate proof-claims route said `No
proof claims have been submitted yet.`  Thus the no-collision gate did not
fire.

## Exact reduction and proof model

For each sum \(s\), let

\[
\mathcal P_N(s)=\{\{a,b\}:1\le a\le b\le N,\ a^3+b^3=s\}.
\]

Construct a hypergraph \(H_N\) on \([N]\) with one edge \(P\cup Q\) for every
two distinct \(P,Q\in\mathcal P_N(s)\).  A root set \(I\) has Sidon cubes if
and only if it contains no edge of \(H_N\).  Therefore

\[
g_3(N)=N-\tau(H_N),
\]

where \(\tau\) denotes the minimum vertex-cover/transversal size.  This is an
identity at the definitions, not a solver model assumption.

For each table row \([L,R]\) with displayed \(\tau\), the bundle proves both
endpoints:

1. `verify_exact.cpp` recomputes \(H_L\) from integer cube sums and
   exhaustively proves that no cover of size \(\tau-1\) exists.
2. It checks an explicit size-\(\tau\) cover of \(H_R\), then independently
   inserts every unordered sum from its complementary root set into a fresh
   integer map and rejects any repetition.

Because \(H_L\subseteq H_N\subseteq H_R\) whenever \(L\le N\le R\), these two
endpoint checks prove the whole interval.

The lower search has no solver dependency.  It branches on every
non-dominated vertex of a currently uncovered edge.  Its only eliminations
are:

- a greedy family of pairwise vertex-disjoint edges, which is a valid lower
  bound on the number of additional cover vertices;
- domination inside the branch edge: if every uncovered edge containing
  \(v\) also contains \(w\), any solution using \(v\) can replace it by \(w\);
- memoization of an identical set of uncovered edges already proved
  impossible with at least as much remaining budget.

These rules preserve exhaustive coverage.  The full run visits 12,893,491
recursive states at the twelve lower endpoints.

## Independent arithmetic and upper-certificate audit

`audit_definition.py` is a separate Python implementation.  It reconstructs
the equal-sum groups from scratch, checks every upper cover, and again checks
every complementary set directly by all unordered cube sums.

At \(N=191\), it obtains:

- 18,336 unordered root pairs;
- 18,212 distinct sum values;
- 124 values with two representations;
- 124 collision edges, every one of size four;
- 164 vertices occurring in at least one collision edge.

For the canonical lexicographically sorted edge list, with one comma-separated
edge per line and no final newline, SHA-256 is

```text
644dadc2aa52bddd902f03811acff745e129add6406fac5a09be5099852fb081
```

The two implementations share only the displayed witness data and expected
final counts/digest; their pair enumeration, edge construction, and direct
Sidon checks are separate code.

## Reproduction

From this directory:

```bash
./verify.sh
```

Requirements are Python 3 and a C++17 compiler; there are no third-party
Python modules and no SAT/ILP dependency.  On the production VM, the frozen
run ended with:

```text
FINAL N=191 pairs=18336 sums=18212 collision_groups=124 edges=124 max_representations=2
ALL CHECKS PASSED; exact table g3(N) for 132<=N<=191; exhaustive_calls=12893491 seconds=163.373
```

## Suggested ledger wording

`PARTIAL: Exact exhaustive computation extends the cube-Sidon table from
N=131 through N=191, ending at g_3(191)=159. A dependency-free C++ search
proves every lower endpoint and explicit covers plus an independent Python
arithmetic audit prove every upper endpoint. The linear-density and infinite
questions remain open.`
