# Erdős #1034 — Flynn Bettens's exact constant (36 − 5√3)/66, refereed (2026-11-24)

Page: https://erdosproblemaday.com/day/1034-bettens-exact-constant-refereed · submission: /submission/j8gq7z

## Claim (Bettens, Zenodo 23223509, 7 October 2026, CC-BY-4.0)
Let h(n) be the largest integer such that every n-vertex graph with more than n²/4 edges has a triangle T with at
least h(n) vertices outside T adjacent to at least two vertices of T. Then lim h(n)/n = (36 − 5√3)/66
= 0.4142385751841759… More precisely every such graph has a triangle with |Y⁺(T)| ≥ c*n (T's own three vertices
included), so h(n) ≥ ⌈c*n⌉ − 3; and a six-clique Ma–Tang-type construction shows lim sup h(n)/n ≤ c*.

## What is here
- `deposit/` — the five files of the Zenodo record, byte-identical (MD5s match Zenodo's): paper `proof.pdf`,
  `certificate.json.gz`, `verification_model.json`, the author's `verify.py`, `README.md`. CC-BY-4.0, © F. Bettens.
- `their-verifier-run/theirs_verify.log` — the author's verifier, run here unchanged
  (`python3 -I verify.py certificate.json.gz verification_model.json --workers 4`, nice 19, from /tmp):
  CERTIFICATE VERIFIED, 1:02.96 wall, 54 MB.
- `second-verifier/` — a clean-room verifier written by a separate Claude instance from the paper and the data
  format only (never opened `verify.py`). nauty basis; identity exact over Q(√3) on all 1044 graphs by two
  counting routes sharing no code (route B agrees term by term with route A), plus three random 62-bit primes at
  both √3 roots; PSD by exact largest-diagonal-pivot elimination (all 82 pass, 22 exactly singular); all signs
  exact; mutation, convention and planted-matrix controls. `run_all.sh` reruns it. Summary: `seats/second_verifier.md`.
- `semantic/` — `semantic_check.py` (ours, written without either verifier's code): evaluates every term of
  identity (31) as a graphon integral on random 0/1 step graphons with rational part weights, exactly over Q(√3);
  D is computed from its definition, not from the model. `run_main.log`: 24/24 random graphons (4–6 parts),
  residual exactly 0. Controls (`run_slack/matrix/beta/cstar.log`, 4 trials each): slack of the empty 7-vertex
  graph +1e−6, block-5 entry (0,1) +1/1000, β +1/1000, c* +1/1000 — the residual is nonzero in 15 of 16 trials; the
  one miss (matrix, trial 3) is a graphon in which one of the two flags joined by the changed entry (block 5's
  basis vector 1) has zero density, so the entry contributes nothing (the block's type does occur there). One
  equation per graphon, and the 24 graphons together give weight to only 361 of the 1,044 seven-vertex graphs (a
  graphon with ≤ 6 parts cannot produce a twin-free graph): this is evidence that the descriptors mean what the
  paper says, not a proof of the coefficient identity (the two verifiers above check that). (Found by the blind
  read of the page draft; our first explanation of the miss was wrong.)
- `construction/` — `construction.py`: the six-clique construction (S independent, joined to B = m equal cliques).
  Brute force over all triangles equals the formula |S| + max clique at n = 40, 66, 90, 120; best admissible
  max|Y⁺|/n at n = 10³…10⁶ for m = 5, 6, 7 (m = 6: 0.416, 0.4145, 0.41425, 0.414240 → c* = 0.414239).
- `small-graphs/` — `ymin.c` over `nauty-geng` output: every graph on 5 ≤ n ≤ 10 vertices with more than n²/4 edges
  (2,331,184 at n = 10) has a triangle with |Y⁺| ≥ ⌈c*n⌉ + 1 (6 at n = 10). Low power (the bound bites only for large n);
  Mantel control: no triangle-free graph appears.
- `seats/referee.md` — hostile referee (Claude, Opus 5.5): HOLDS WITH FIXES, five wording fixes, no gap; code
  audit of `verify.py` with 15 mutations; tightness at the six-clique graphon W*.
- `seats/world.md` — the record (database, Formal Conjectures, Ma–Tang note, searches). erdosproblems.com not read.

## Reproduce
```
python3 -I deposit/verify.py deposit/certificate.json.gz deposit/verification_model.json   # ~1 min
python3 semantic/semantic_check.py deposit 2 24            # minutes; needs numpy
bash second-verifier/run_all.sh                            # reads ../deposit; rerun from this bundle tested 24 Nov
gcc -O2 -o ymin small-graphs/ymin.c && nauty-geng -q 10 26:45 | ./ymin
python3 construction/construction.py
```
No human has reviewed this proof.
