# Erdős problem #778 — wave w014

Date of live check: 2026-07-28 (UTC)

## Claim labels

- **(a) elementary-rigorous:** proved here from definitions, with no external theorem.
- **(b) rigorous-modulo-named-theorem:** depends on the accurately cited theorem.
- **(c) plausible/structural-unverified:** heuristic, extrapolation, or search diagnosis only.
- **(d) computational-only:** exhaustive computation or direct source/page inspection.

## Result at a glance

**(a)** Bob wins the unresolved biased game \(\operatorname{Clique}_{(1,2)}(n)\) for \(n=4,5\). Explicit elementary strategies are given below.

**(d)** Exact minimax search proves that Bob also wins \(\operatorname{Clique}_{(1,2)}(n)\) for \(n=6,7\). In fact, for every \(4\le n\le7\), the search certifies the stronger statement that Bob can keep Alice's final graph triangle-free.

**(a)** The biased game at the excluded value \(n=3\) is an Alice win: both final clique numbers are \(2\), so Bob does not obtain the strict inequality required of the stronger player.

**(c)** These finite cases do not settle the uniform question. The computation at \(n=8\) exceeded the imposed few-minute budget, and triangle avoidance cannot be a uniform strategy.

## Step 0: mandatory live-page audit

**(d)** I fetched [the live page](https://www.erdosproblems.com/778) with the Bright Data browser path, then separately opened [its discussion thread](https://www.erdosproblems.com/forum/discuss/778). At access time the page showed:

- status **OPEN**;
- **1 comment**;
- **0 claimed proofs**;
- “Interested in collaborating: None”;
- “Currently working on this problem: None”.

Thus the stop condition was not triggered.

### Verbatim live statement

> Alice and Bob play a game on the edges of $K_n$, alternating colouring edges by red (Alice) and blue (Bob). Alice goes first, and wins if at the end the largest red clique is larger than any of the blue cliques.
>
> Does Bob have a winning strategy for $n\geq 3$? (Erdős believed the answer is yes.)
>
> If we change the game so that Bob colours two edges after each edge that Alice colours, but now require Bob's largest clique to be strictly larger than Alice's, then does Bob have a winning strategy for $n>3$?
>
> Finally, consider the game when Alice wins if the maximum degree of the red subgraph is larger than the maximum degree of the blue subgraph. Who wins?

### Results and comment shown on the live page

**(d)** The page attributes the following results to Malekshahian and Spiro:

> Malekshahian and Spiro [MaSp24] have proved that, for the first game, the set of \(n\) for which Bob wins has density at least \(3/4\) - in fact they prove that if Alice wins at \(n\) then Bob wins at \(n+1,n+2,n+3\).
>
> Similarly, for the third game they prove that the set of \(n\) for which Bob wins has density at least \(2/3\), and prove the stronger statement that if Alice wins at \(n\) then Bob wins at \(n+1,n+2\).

**(d)** The sole comment, by StijnC on 2025-08-09, says:

> The paper of Malekshahian and Spiro had the condition that \(n\) is sufficiently large (\(n\ge 46\) or \(n \ge 18\)), but the exact statement is verified. Some particular behaviour is listed in [CP25].
>
> The first two questions should have an affirmative answer. Also in the third question, Bob should win.

The page explicitly warns that comments are not verified.

## Primary-source literature audit

**(d)** The original source metadata is verified as R. K. Guy, “A Miscellany of Erdős Problems,” *American Mathematical Monthly* 90 (1983), 118–120, [DOI 10.1080/00029890.1983.11971168](https://doi.org/10.1080/00029890.1983.11971168).

**(b)** A. Malekshahian and S. Spiro, [“On a clique-building game of Erdős,” arXiv:2410.18304](https://arxiv.org/abs/2410.18304), revised 2026-05-11 and now published in *Journal of Graph Theory*, [DOI 10.1002/jgt.70061](https://doi.org/10.1002/jgt.70061), proves the \(3/4\) and \(2/3\) density results. Its current Theorem 3 gives Bob the biased clique game for sufficiently large \(n\) in a range which in particular includes \((1,4)\), not the requested \((1,2)\).

**(b)** S. Cambie and M. Provoost, [“On edge-colouring-games by Erdős, and Bensmail and Mc Inerney,” arXiv:2505.03497v2](https://arxiv.org/abs/2505.03497), proves:

- Proposition 9: Bob wins the unbiased clique game for \(3\le n\le8\), and the \(n\mapsto n+3\) implication is valid without a large-\(n\) restriction;
- Theorem 8: Bob wins \(\operatorname{Clique}_{(1,3)}(n)\) for every \(n\ge4\);
- a conjecture that Bob wins the maximum-degree game on \(K_n\) except at \(n=2,3\), together with exact small computations through \(K_8\).

**(d)** I inspected their public [edge-colouring-games repository](https://github.com/Algorithmic-Graph-Theory-Group/edge-colouring-games) at commit `b698f00193f901fc444f3515e303c5eec256ef33`. The verifier written here is independent: it imports neither that code nor nauty.

**(d)** Searches by exact problem text, title, arXiv identifier, \(\operatorname{Clique}_{(1,2)}\), and citations found the two sources above but no later primary source claiming the \((1,2)\) problem or the whole problem solved. This is a reported search miss, not a proof of novelty or absence.

## Two exact reformulations

Let \(R\) be Alice's final graph. Since every edge receives exactly one colour, Bob's graph is \(\overline R\).

**(a) Clique reformulation.**

\[
  \omega(B)=\omega(\overline R)=\alpha(R).
\]

Consequently:

- in the unbiased game Alice wins exactly when \(\omega(R)>\alpha(R)\);
- in the \((1,2)\) game Bob wins exactly when \(\alpha(R)>\omega(R)\), while Alice wins when \(\omega(R)\ge\alpha(R)\);
- Alice receives exactly
  \[
  r_n=\left\lceil\binom n2/3\right\rceil
  \]
  edges in the \((1,2)\) game, including the prescribed short last turn.

Thus the second question is exactly a \((1:2)\) Maker–Breaker game in which Alice/Maker tries to create the monotone property

\[
  \mathcal F_n=\{G\subseteq K_n:\omega(G)\ge\alpha(G)\}.
\]

Adding a red edge cannot decrease \(\omega\) or increase \(\alpha\), so this really is monotone.

**(a) Maximum-degree reformulation.**

For every vertex \(v\),

\[
 d_B(v)=n-1-d_R(v),
\qquad
\Delta(B)=n-1-\delta(R).
\]

Hence Alice wins the third game exactly when

\[
  \Delta(R)+\delta(R)>n-1,
\]

and Bob wins exactly when \(\Delta(R)+\delta(R)\le n-1\). This isolates that question as an online degree-balancing problem.

## Explicit strategy at \(n=4\)

**(a)** Let Alice's first edge be \(uv\), and let \(xy\) be the unique edge disjoint from it. Bob takes \(xy\) and any other free edge. Alice's second and final edge must meet \(uv\), because \(xy\) is unavailable. Her two red edges therefore form a \(P_3\), so \(\omega(R)=2\). The three vertices consisting of the two leaves of that \(P_3\) and the remaining isolated vertex form a blue triangle. Thus \(\omega(B)=3>2\).

The standalone checker exhausts all 72 labelled continuations of this strategy.

## Explicit strategy at \(n=5\)

Alice has four moves, and Bob has three two-edge responses; Alice's fourth move is the last edge of the board.

Call a free edge a **threat** if Alice taking it would complete a red triangle.

**(a)** Bob uses this strategy:

1. after Alice's first move, take any two free edges;
2. after Alice's second and third moves, take every current threat, then fill any unused part of the two-edge quota arbitrarily.

There is at most one threat after Alice's second move. After Alice's third move there are at most two unclaimed threats:

- if her first two edges meet, Bob already took their closing edge, and the third edge creates at most two new red \(2\)-paths;
- if her first two edges are disjoint, the third edge creates at most two red \(2\)-paths.

After Bob's third response every threat is blue. Alice's final edge therefore cannot complete a red triangle. Hence \(R\) is triangle-free and has four edges.

**(a)** Such an \(R\) has \(\alpha(R)\ge3\). Indeed, assume instead that \(\alpha(R)\le2\). Triangle-freeness makes every neighbourhood independent, so every degree is at most \(2\). If some vertex had degree at most \(1\), it would have at least three non-neighbours; to avoid an independent triple with that vertex, those non-neighbours would have to form a triangle, contradiction. Thus every degree would equal \(2\), forcing \(|E(R)|=5\), not \(4\). Therefore

\[
  \omega(R)=2<3\le\alpha(R)=\omega(B),
\]

and Bob wins.

The standalone checker exhausts 280 terminal labelled branches of the stated deterministic version of this strategy and records that the maximum number of live threats is \(2\).

## Exact computation for \(n=6,7\)

### Result

**(d)** The exact results are:

| \(n\) | Alice's final edge count | winner of \(\operatorname{Clique}_{(1,2)}(n)\) | stronger triangle-avoidance result |
|---:|---:|:---:|:---:|
| 3 | 1 | Alice | Bob, but this only yields a clique tie |
| 4 | 2 | Bob | Bob |
| 5 | 4 | Bob | Bob |
| 6 | 5 | Bob | Bob |
| 7 | 7 | Bob | Bob |

**(d)** “Triangle-avoidance result: Bob” means that the exact minimax value of the ordinary \((1:2)\) triangle Maker–Breaker game on \(E(K_n)\) is a Breaker/Bob win.

**(a)** For \(n=6,7\), this stronger certificate implies the desired result without any further computation. A triangle-free red graph has \(\omega(R)=2\). In any red/blue colouring of \(K_6\), choose a vertex \(v\); at least three of its five incident edges have one colour. If any edge among their other endpoints has that colour there is a monochromatic triangle with \(v\); otherwise those three endpoints form a triangle of the other colour. Thus \(R(3,3)\le6\). Applied to a triangle-free \(R\) on at least six vertices, this gives \(\alpha(R)\ge3\), and hence

\[
  \omega(B)=\alpha(R)\ge3>2=\omega(R).
\]

### Solver and correctness

**(a)** A position is represented by disjoint bit masks \((R,B)\) on the lexicographically ordered edges of \(K_n\). At an Alice node, Bob has a forced win iff every legal Alice batch leads to a Bob-win child. At a Bob node, Bob has a forced win iff some legal Bob batch leads to a Bob-win child. At a full board the program evaluates the clique numbers directly by enumerating vertex subsets. This is precisely backward induction for a finite perfect-information game.

The core recurrence is:

```python
if full_board:
    return omega(blue) > omega(red)       # biased game
if alice_to_move:
    return all(solve(red | move, blue) for move in alice_batches)
else:
    return any(solve(red, blue | move) for move in bob_batches)
```

**(a)** Two monotone cutoffs are exact. If the current blue clique is already larger than the largest clique obtainable even after giving every free edge to red, Bob has won. If the largest clique obtainable after giving every free edge to blue is no larger than red's current clique, Bob cannot win. The inequalities are changed from strict to weak in the unbiased game exactly as required by its tie rule.

**(a)** In symmetry mode, each child is replaced by a canonical representative under a permutation of vertices. The program first performs colour refinement on the three edge colours (red, blue, free), then explicitly enumerates every ordering inside every remaining vertex cell and chooses the least bit encoding. Isomorphic positions therefore have the same representative, and no non-isomorphic positions are identified.

**(d)** Search statistics for the direct Erdős objective:

| \(n\) | canonical states evaluated | distinct generated children | wall time on this VM |
|---:|---:|---:|---:|
| 3 | 2 | 1 | <0.001 s |
| 4 | 9 | 13 | 0.001 s |
| 5 | 9 | 50 | 0.006 s |
| 6 | 500 | 3,021 | 0.24 s |
| 7 | 7,488 | 83,248 | 9.0 s |

**(d)** Search statistics for the stronger triangle-avoidance objective:

| \(n\) | canonical states evaluated | distinct generated children | wall time on this VM |
|---:|---:|---:|---:|
| 4 | 7 | 9 | 0.001 s |
| 5 | 9 | 50 | 0.006 s |
| 6 | 714 | 3,845 | 0.31 s |
| 7 | 51,327 | 453,942 | 40.6 s |

### Independent checks

**(d)** Disabling every symmetry reduction gives the same biased-game winners. In particular:

- \(n=6\): 30,979 labelled states and 150,900 generated children;
- \(n=7\): 2,542,089 labelled states and 19,337,345 generated children, 132 CPU-seconds, peak RSS 3,498,676 KiB.

This independently removes the canonical-labelling routine from the \(n=7\) result.

**(d)** The same engine reproduces the published small outcomes: Bob in the unbiased clique game for \(3\le n\le7\), Alice in the maximum-degree game at \(n=3\), and Bob in the maximum-degree game for \(4\le n\le6\). Labelled, non-symmetry runs agree through \(n=6\).

**(d)** An exhaustive terminal census for the biased game is:

| \(n\) | red edges | all labelled terminal red graphs | labelled Alice targets \(\omega\ge\alpha\) | unlabelled target types |
|---:|---:|---:|---:|---:|
| 3 | 1 | 3 | 3 | 1 |
| 4 | 2 | 15 | 3 | 1 |
| 5 | 4 | 210 | 70 | 2 |
| 6 | 5 | 3,003 | 600 | 3 |
| 7 | 7 | 116,280 | 13,335 | 12 |

The minimax result says Bob can hit every target despite their existence.

## Why two standard approaches stop

### Beck's potential criterion is already inconclusive in the small cases

Let \(\mathcal M_n\) be the attainable inclusion-minimal red edge sets satisfying \(\omega\ge\alpha\), omitting sets larger than Alice's final quota.

**(b)** Beck's biased Erdős–Selfridge criterion, in the form quoted as Theorem 11 by Malekshahian–Spiro, would prove a \((1:2)\) Breaker win if

\[
  \Phi_n=\sum_{F\in\mathcal M_n}3^{-|F|}<\frac13.
\]

**(d)** Exhaustive enumeration gives:

| \(n\) | number of minimal targets by edge size | \(\Phi_n\) |
|---:|:---|:---|
| 4 | \(3\) of size \(2\) | \(1/3\) |
| 5 | \(10\) of size \(3\) | \(10/27\) |
| 6 | \(60\) of size \(4\) | \(20/27\) |
| 7 | \(105\) of size \(5\), \(105\) of size \(6\) | \(140/243\) |

All fail the strict \(<1/3\) hypothesis, even though Bob wins. Thus this unweighted potential criterion cannot supply the missing uniform proof.

### Triangle avoidance cannot extend uniformly

**(b)** C. Glazik and A. Srivastav, [“A new bound for the Maker–Breaker triangle game,” arXiv:1812.01382](https://arxiv.org/abs/1812.01382), restate the Chvátal–Erdős Maker strategy: Maker wins the \((1:q)\) triangle game when

\[
q<\sqrt{2n+2}-\frac52.
\]

For \(q=2\), this holds for every \(n\ge10\). Therefore Bob cannot keep Alice triangle-free uniformly. A proof of the original problem must allow red triangles and exploit the full comparison \(\alpha(R)>\omega(R)\).

## The precise remaining wall

**(a)** The second question is reduced exactly to finding a Breaker strategy against the monotone family

\[
\mathcal F_n=\{G:\omega(G)\ge\alpha(G)\}.
\]

**(c)** The missing lemma is a strategy or potential which couples clique growth to independence-number growth: Bob must permit the small red cliques that Alice can eventually force while guaranteeing a strictly larger independent set in her final graph. Separate “block Alice's clique” and “build Bob's clique” strategies currently need bias \(3\) or \(4\), as the cited papers show.

**(d)** The \(n=8\) Python search was stopped after 196.38 CPU-seconds with no result and peak RSS 433,088 KiB. This was not counted as evidence either way.

**(c)** A crude orbit-layer proxy (the raw labelled layer count divided by \(n!\)) grows from about \(5.20\times10^4\) at the largest \(n=7\) layer to \(8.63\times10^6\) at the largest \(n=8\) layer, a factor about \(166\). For the present Python implementation, a realistic completion estimate is roughly \(0.3\)–\(1\) core-hour and several GiB, with substantial uncertainty because pruning is outcome-dependent. A nauty-backed bottom-up C solver or a separately checkable strategy certificate is the appropriate next computation; it was not run under this task's CPU limit.

No finite table here supplies a uniformity step, and the problem remains open.

## Reproduction

The standalone checker is [`erdos778_wavew014_verify.py`](./erdos778_wavew014_verify.py). It uses only the Python standard library.

Main exact table and the two elementary strategy checks:

```bash
python runs/erdos778_wavew014_verify.py
```

Stronger triangle-avoidance computation:

```bash
python runs/erdos778_wavew014_verify.py --triangle-avoidance
```

Labelled cross-checks through \(n=6\), all three live-page games, and terminal census:

```bash
python runs/erdos778_wavew014_verify.py \
  --max-n 6 --cross-check --all-three --targets
```

The expensive labelled \(n=7\) cross-check:

```bash
python runs/erdos778_wavew014_verify.py \
  --max-n 7 --deep-cross-check
```

Minimal-target potential census:

```bash
python runs/erdos778_wavew014_verify.py \
  --min-n 4 --max-n 7 --potential
```

Every completed command ends with `ALL CHECKS PASSED`; assertions contain all reported exact winners, target counts, elementary branch counts, and potential fractions.

PARTIAL: Bob wins the biased \(1{:}2\) clique game for every \(4\le n\le7\); \(n=4,5\) have elementary strategies and \(n=6,7\) have exact stronger triangle-avoidance certificates, but no uniform \(n>3\) argument is obtained.
