# Problem 86: reader submission c3u7pu — a 1,532-edge C4-free subgraph of Q9

Reviewed 2026-10-19. Verdict: **VERIFIED** (as a certificate: ex(Q9, C4) ≥ 1,532).

## The claim

Submission `c3u7pu` (received 2026-10-17, anonymous, consent to publish given) links
github.com/Bil812/erdos86-q9-c4 (tag v1.0 = `d50913a`; HEAD at review `2753ab7`) and claims a lower
bound only: an explicit set of 1,532 edges of Q9 with no 4-cycle. Their declaration says the work was
done end to end by AI agents (DeepSeek Harness, `deepseek-v4.1-flash-1017`). We ran none of their code.

`submitted/` holds the files we checked, byte-identical to the repository
(`edges_q9_1532.txt` sha256 `d701bd18…` as stated in the submission; `q9b_spin_6.txt`, a second
1,532-edge graph; `spins_q9.txt`, the 512-spin configuration).

## Three checks (our code, `checks/`)

1. `check86.py` — parses pairs, requires each to differ in exactly one bit and to be distinct; then
   (A) every one of the C(9,2)·2^7 = 4,608 square 2-faces has at most 3 of its 4 edges, and
   (B) no two vertices share 2 neighbours (C4-free ⟺ codegree ≤ 1). Both graphs: 1,532 edges,
   0 full squares, 0 bad pairs. Control: adding the missing edge of a 3-edge square is rejected by both
   tests. (In Q_n every 4-cycle is a 2-face: two vertices at distance 2 have exactly two common
   neighbours in Q_n.)
2. `check86_np.py` — different parser (regex over the file) and a different method: adjacency matrix A,
   C4-free ⟺ off-diagonal entries of A² ≤ 1. Both graphs: max 1. It also tabulates edges per 2-face:
   784 faces carry 1 edge and 3,824 carry 3, none 0, 2 or 4 — the "odd-square" (fully frustrated)
   signature. The two graphs share 1,024 edges.
3. `mpr_energy.py` — under the fully frustrated coupling of Marinari–Parisi–Ritort (eq. 4:
   J(x, x+e_ν) = (−1)^{Σ_{μ<ν} x_μ}), the submitted spin configuration has exactly the submitted
   1,532 edges as its satisfied bonds, and energy per spin
   E = −(1/√9)·ΣJss / 512 = −760/1536 = −95/192 = −0.4947916…, i.e. −380 on MPR's ×768 scale.

## Priority: the number 1,532 was reported in 1994

E. Marinari, G. Parisi, F. Ritort, *The Fully Frustrated Hypercubic Model is Glassy and Aging at
Large D*, arXiv:cond-mat/9410089 (25 Oct 1994), p. 4 (`sources/mpr95_excerpt.txt`):

> "In D = 9 … we have not been able to access a ground state saturating the −1/2 bound, but we have
> reached a value very close to that, −.494792. … On this scale we have reached a value of −380"

With H = −(1/√D)ΣJ s s and N = 2^D spins, E = −(P − M)/(3·512) with P + M = 2,304 bonds; E = −.494792
gives P = 1,532. Since every plaquette is frustrated, the satisfied bonds meet every square in 1 or 3
edges, so they form a C4-free subgraph. **So a 1,532-edge C4-free subgraph of Q9 was reported to exist in
1994**, as an annealing result in energy units, with no configuration published. Minamoto,
arXiv:2603.29127 v5 (2026-08-28) §6 transcribes that D = 9 value (−0.494792, −380, "four units short" of
the −384 field bound) and leaves g(9) open (Open Problem 7). The submission itself flagged exactly this
possibility ("old statistical-physics computations of fully frustrated Ising ground states for D = 9").

What is new in the submission, as far as we found: the first public **explicit** 1,532-edge certificate
(two of them), at precisely MPR's reported energy.

## Where it sits

- Field bound for odd-square sets (Lemma 9 of Minamoto, after Derrida–Pomeau–Toulouse–Vannimenus):
  g(9) ≤ (2,304 + 768)/2 = 1,536, attained only if every vertex has degree 6. Open whether 1,536 is
  attained; MPR could not reach it. This bounds odd-square sets only, not ex(Q9, C4).
- Upper bound for ex(Q9, C4) from the live erdosproblems.com/86 thread (pawelkwaczynski, 2026-08-27):
  averaging over subcubes, f(9) ≤ (18/8)·f(8) ≤ (18/8)·704 = 1,584.
- So 1,532 ≤ ex(Q9, C4) ≤ 1,584.

## Correction to our own entry

Our /day/86-hypercube-q9-1531 (2026-08-11) said 1,531 improved the public record. Explicit edge lists:
true on that date. The number: false — MPR's 1994 report already implied a 1,532-edge subgraph. The entry
is corrected in place on 2026-10-19. (Our 08-11 audit read Minamoto v4; v1–v4 of arXiv:2603.29127 never mention
Marinari–Parisi–Ritort — checked 2026-10-19 by grepping all four PDFs — so MPR entered the record we read only
with v5 on 2026-08-28. The miss was the 1994 physics paper itself.)

## Reproduce

```
cd checks
python3 check86.py ../submitted/edges_q9_1532.txt 9
python3 check86.py ../submitted/q9b_spin_6.txt 9
python3 check86_np.py ../submitted/edges_q9_1532.txt      # needs numpy
python3 mpr_energy.py ../submitted/spins_q9.txt ../submitted/edges_q9_1532.txt
sha256sum -c SHA256SUMS   # from this directory
```
