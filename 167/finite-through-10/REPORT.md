# Erdős problem #167 — a finite constructive census through ten vertices

Date: 2026-08-12 UTC

## Result and rigor level

**PROVED (computer-assisted finite result).** Every finite simple graph on at
most ten vertices satisfies Tuza's triangle packing/covering inequality

\[
\tau(G)\le 2\nu(G),
\]

where \(\nu(G)\) is the maximum number of pairwise edge-disjoint triangles and
\(\tau(G)\) is the minimum number of edges meeting every triangle.

This is not a solution of the unrestricted Erdős problem. It is an exhaustive
finite extension with a compact, definition-level checker. No novelty or
priority claim is made.

## Mandatory live gate

The problem page and its complete one-comment discussion were fetched through
a Bright Data cloud browser on 2026-08-12. The live state was:

- open (the site labels it `FALSIFIABLE`);
- `0 claimed proofs for this problem`;
- `Interested in collaborating: None`;
- `Currently working on this problem: None`;
- `I am working on formalising the results on this problem: None`.

The only comment points to Haxell's 1999 \((66/23)\nu\) upper bound, which the
page already records. A targeted local scan found no banked Problem 167 report
or site entry. The present work did not collide with any current worker.

## What the complete checker actually certifies

For each connected unlabeled graph \(G\) of a fixed order \(n\le10\),
`verify_167.cpp` constructs two objects:

1. a family \(P\) of pairwise edge-disjoint triangles;
2. a set \(C\subseteq E(G)\) meeting every triangle;

and then checks directly, from the graph definition, that

\[
|C|\le2|P|.
\]

This is enough without proving that \(P\) or \(C\) is optimal: by definition,
\(|P|\le\nu(G)\) and \(\tau(G)\le|C|\), hence

\[
\tau(G)\le|C|\le2|P|\le2\nu(G).
\]

The construction is deterministic. It tries eleven elementary greedy triangle
orders and retains the largest resulting packing. It then repeatedly selects an
edge meeting the largest number of uncovered triangles. Remarkably, on every
non-triangle-free connected graph through order ten, this first greedy cover
already had size at most twice the retained packing: the fallback exact cover
search was present but never had to branch (`max_cover_search_nodes=1`). The
checker nevertheless reconstructs and validates both objects before accepting a
graph.

Nauty's `geng -c` supplies one graph6 representative of every connected
isomorphism class. Connected graphs suffice because both \(\nu\) and \(\tau\)
add over connected components. The property is invariant under graph
isomorphism.

## Complete census

| order | connected classes | triangle-free | certified nontrivial | constructed pairs with \(|C|=2|P|\) | graph6 seeded FNV-style-64 |
|---:|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 0 | 0 | `9b428d00c6017909` |
| 2 | 1 | 1 | 0 | 0 | `cc139250709993e3` |
| 3 | 2 | 1 | 1 | 0 | `3bcf2663e2ca6e9d` |
| 4 | 6 | 3 | 3 | 1 | `81e4df91e80afafd` |
| 5 | 21 | 6 | 15 | 2 | `7bb99b2c36e01bea` |
| 6 | 112 | 19 | 93 | 5 | `8f4594637f40648c` |
| 7 | 853 | 59 | 794 | 19 | `4a0b9705dbe3814d` |
| 8 | 11,117 | 267 | 10,850 | 99 | `e2e93eabc219c0c3` |
| 9 | 261,080 | 1,380 | 259,700 | 583 | `44e6512280961203` |
| 10 | 11,716,571 | 9,832 | 11,706,739 | 4,807 | `38c1f219f45f740c` |

In total: 11,989,764 connected isomorphism classes, including 11,978,195
classes containing at least one triangle.

The final column is a deterministic stream checksum produced by the checker's
FNV-1a update rule with the custom initial seed `1469598103934665603`. It is
therefore a seeded FNV-style checksum, not standard FNV-1a-64 (whose offset
basis is different).

The last-but-one column records equality for the particular constructed pair.
The independent exact audit shows that through order nine these are exactly the
true equality counts. At order ten, the 4,807 figure is not claimed to count
exact equality \(\tau=2\nu\).

## Independent audit

`independent_audit.py` deliberately uses a different graph6 parser (NetworkX)
and two separate memoized, definition-level optimizers:

- the packing recursion partitions solutions by whether they use a selected
  graph edge;
- the cover recursion branches on the three edges of an uncovered triangle.

It computed exact \((\nu,\tau)\) for every connected unlabeled graph through
order nine. All 273,193 classes passed. The exact nontrivial equality counts for
orders 4 through 9 were respectively

\[
1,2,5,19,99,583,
\]

agreeing exactly with the constructive program.

`audit_order10_sample.py` independently computed exact \((\nu,\tau)\) on the
deterministic nauty residue `0/10007` at order ten: 2,183 connected classes,
1,764 containing triangles, all passed, with 7 exact equality cases. The
sample-stream SHA-256 was
`40cbafe5472c30956f15dffd03f8037bb0156065540d0b604f369573a33836d2`.

Finally, the main checker compiled with both AddressSanitizer and
UndefinedBehaviorSanitizer and reran the complete 11,117-class order-eight
census with identical output and no sanitizer finding.

## Reproduction

Requirements: a C++20 compiler, nauty's `geng` (installed here as
`/bin/nauty-geng`), Python 3, and NetworkX for the independent audit.

```sh
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic verify_167.cpp -o verify_167
for n in 1 2 3 4 5 6 7 8 9 10; do
  /bin/nauty-geng -cq "$n" | ./verify_167
done

python3 independent_audit.py --max-n 9
python3 audit_order10_sample.py
```

The complete order-ten line is the large step (11,716,571 graphs); it completed
comfortably on this VM with only a few MiB of checker memory.

## Scope and literature note

The live page cites Haxell and Kahn--Park. A narrow web search also found
Anish Gupta's very recent preprint,
*Tuza's conjecture for graphs of maximum degree at most seven*
(arXiv:2608.06538). That theorem already implies the result for graphs through
order eight. The present order-nine and order-ten census includes maximum-degree
eight and nine cases, respectively, but this search was not a systematic
literature review. Accordingly this bundle claims only a verified finite result,
not that the order-ten threshold is new.

Sources:

- <https://www.erdosproblems.com/167>
- <https://www.erdosproblems.com/forum/thread/167?order=oldest>
- <https://arxiv.org/abs/2608.06538>
