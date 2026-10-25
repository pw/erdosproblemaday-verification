# Reader submission u2udx4 (as received, 2026-10-22 16:59:06Z)

- Problem: 531 · Name: Atakan Akbaba · Claim: partial · Consent to publish: yes
- Links: https://github.com/nakata-app/erdos-531-folkman · .../witnesses/w396.txt · .../verify/check.c ·
  https://github.com/teorth/erdosproblems/pull/490
- Repository HEAD at review: see submitted/REPO_HEAD.txt (ca25843, 2026-10-22 19:57 +0300)

Body (verbatim):

> F(4) >= 397 (explicit witness, independently checkable)
>
> Statement worked on: F(k) = least N such that every 2-colouring of {1,...,N} contains a k-element set A whose
> nonempty subset sums are all the same colour (Erdős #531, Folkman). Convention: A counts only when sum(A) <= N
> (the colouring is defined on {1,...,N} only) and the elements of A are distinct.
>
> Result (label: lower bound): a 2-colouring of {1,...,396} with no set A = {a<b<c<d}, a+b+c+d <= 396, whose 15
> nonempty subset sums are monochromatic. Hence F(4) >= 397.
>
> How to check it: witnesses/w396.txt (SHA-256 a0ca6789…3c3d). `./check witnesses/w396.txt` prints
> `N=396 tested=40781268 mono=0` …
>
> Method: computer search extending the witness one value at a time … min-conflicts/tabu local search up to
> N = 380; Configuration Checking with aspiration from N = 381; seeded recolouring at walls from N = 387.
>
> What is ours: the witness chain w200-w396, the search code and the checkers. What is not: the problem, the
> convention check against your F(3) = 54 report.

Tools declared: DeepSeek (V4 family) drove the search agent and produced the witness chain; Claude (Claude Code)
wrote their verifiers and maintains the repository.
