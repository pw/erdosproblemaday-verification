# Submission 8a7svk (erdosproblemaday.com/submit, 2026-10-28 20:21Z, consent to publish = yes)

- Problem: 531 · Name: Atakan Akbaba · Claim: partial
- Links: https://github.com/nakata-app/erdos-531-folkman ·
  https://github.com/nakata-app/erdos-531-folkman/blob/main/witnesses/k5_w1513.txt ·
  https://github.com/teorth/erdosproblems/pull/490
- Tools (as stated): DeepSeek and Claude ran the local-search witness chain (search/k5_climb.c); verified independently
  by verify/k5_check.c and verify/k5_dfs.py.
- Repository HEAD at review: d6009ada7d50805c7f764a78f24ae10401c631e4 (2026-10-28T20:11:51Z, "k=5: repair chain extended
  to k5_w1513 (F(5) >= 1514); 1495 breached with heavier budget").

Claim (body, abridged): F(5) ≥ 1514. `witnesses/k5_w1513.txt` is an explicit 2-colouring of {1,…,1513}; no 5-set
{a<b<c<d<e} with a+b+c+d+e ≤ 1513 has all 31 nonempty subset sums the same colour. Convention as in u2udx4 (F(2)=9,
F(3)=54, F(4) ≥ 397 earlier). This is a lower bound only.
