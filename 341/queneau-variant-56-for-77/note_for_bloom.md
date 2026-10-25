Subject: Erdős #341 — Queneau's distinct-summand variant is not always periodic either (a seed, a short proof)

Dear Thomas,

Problem 341's page links to Problem 7 of Ben Green's list, which poses Dickson's greedy-gap question for both
rules — summands allowed to coincide (the #341 statement, settled negatively by Zhiheng Li's August seed) and
Queneau's rule, where the two earlier terms must be distinct — and marks both open. Li's seed is eventually periodic
under Queneau's rule, so his counterexample does not transfer.

It transfers with one change. Replace 77 by 56:

   A = {1, 2, 3, 5, 7, 13, 22, 27, 28, 32, 36, 40, 47, 48, 52, 56, 63, 71, 81, 89, 97}.

Under Queneau's rule (next term = least integer above the last that is not a sum of two distinct earlier terms) the
greedy extension of A has a gap sequence that is not eventually periodic; the same seed is also a second
counterexample under Dickson's rule. The proof is Li's shield mod 49 with a new three-rail controller whose blocks
of quotients are [8^k+1, 2·8^k], [4·8^k, 8·8^k], [2·8^k, 4·8^k]; the three sumset identities are a one-page interval
calculation, written out here:

   https://erdosproblemaday.com/day/341-queneau-variant-not-periodic-either

with every script, both greedy runs to 10^7 (an independent greedy on the integers matches the closed form at every
integer), and the referee reports in the linked bundle. Nothing here touches van Berkel–Bosma's conjectures for
two-term starts.

If this is worth a line on the page ("the i<j variant also fails"), the page above has the statement; I'd be glad to
hear of any gap.

Best,
Patrick White
