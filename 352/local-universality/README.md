# Frozen scope verdict

**Verdict: rigorous structural partial progress; Erdős problem 352 remains
open.**

The proved all-`N` lemma says that, for every nonzero `d in Z^2` with
`100|d|<=N`, some fixed-high branch contains an explicit arithmetic-
progression clique

```text
H-d, H-2d, ..., H-Ld,       L=floor(N/(20|d|)).
```

Here an *oriented fixed-high branch* has `O=0` and an arbitrary integral
diameter endpoint `B`; the family is not quotiented by D4. Consequently, no
single homomorphism of `Z^2` with image of size `O(N)`, used unchanged on
every oriented branch at that `N`, properly colors them all for all
sufficiently large `N`. In particular, this rules out one branch-independent
lattice-coset coloring of index `O(N)` across the oriented family.

It does **not** rule out a homomorphic coloring common only to the chosen
D4-normalized representatives: normalizing a branch also transports the
coloring kernel. Nor does it rule out colorings chosen adaptively from the
branch data `B,H`, supply an `O(N)` coloring or cover, prove `f(N)=O(N)`, or
solve #352.

Files:

- `REPORT.md`: construction, proof, consequence, and precise claim boundary;
- `check_local_universality.py`: exact integer audit;
- `CHECK_OUTPUT.txt`: frozen replay output;
- `SHA256SUMS`: hashes of those three files plus this README.

Run the assertion-based checker with ordinary `python3`, never `python3 -O`:

```text
python3 check_local_universality.py
```
