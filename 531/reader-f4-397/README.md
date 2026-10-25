# Problem 531: reader submission u2udx4 — F(4) ≥ 397 (Atakan Akbaba)

Reviewed 2026-10-22. Verdict: **VERIFIED** (as a certificate: F(4) ≥ 397).

## The claim

F(k) = least N such that every 2-colouring of {1,…,N} has a k-set A whose nonempty subset sums are all one
colour (live statement, erdosproblems.com/531). Convention (Erdős–Spencer 1989; BENTW 2017; our July report):
the sums must lie in {1,…,N}, i.e. sum(A) ≤ N; A is a set, so its elements are distinct. The submission gives an
explicit colouring of {1,…,396} with no monochromatic 4-set, hence F(4) ≥ 397 — up from the 201 in our own
July report (/report/531). Repo github.com/nakata-app/erdos-531-folkman, HEAD ca25843 at review.
We ran none of the submitter's code.

`submitted/w396.txt` is byte-identical to the repository file (SHA-256 a0ca6789…3c3d). Note on format: the file is
395 characters, a newline, then the 396th character (it is w395.txt with `1` appended after w395's trailing
newline). A reader that takes only the first line gets N = 395. Both our checkers skip newlines and read 396
colours; colour(396) = 1.

## Two checks (our code, `checks/`)

1. `fs4_direct.c` — enumerates every a<b<c<d with a+b+c+d ≤ N, forms the 15 nonempty subset sums, counts
   monochromatic sets by colour. Output: `N=396 eligible=40781268 mono=0 mono0=0 mono1=0`.
2. `fs_extend.py` — a different algorithm: it GROWS monochromatic sets (A extends by d > max A iff d and every
   s+d, s ∈ FS(A), lie in A's colour class and sum ≤ N) and counts them for k = 1..4; the number of eligible
   k-sets comes from an independent partition DP. Output: eligible_4 = 40,781,268; monochromatic 1-, 2-, 3-sets
   (colour 0 / colour 1): 192/204, 4,364/5,139, 9,833/12,655; monochromatic 4-sets 0/0.

## Controls (`controls_out/controls.txt`)

- All-zero colouring of [396]: 40,781,268 monochromatic (= every eligible set). All-zero of [60]: both
  instruments 16,390.
- 12 random colourings of [396] (p = 0.3, 0.45, 0.5): both instruments give identical monochromatic counts
  (2,086 to 365,511).
- All 396 single-bit flips of w396: identical counts from both instruments, 0 disagreements. 372 flips create a
  monochromatic 4-set; 24 positions can be flipped alone: 15, 101, 107, 120, 121, 122, 129, 131, 185, 187, 188,
  191, 192, 276, 278, 280, 284, 306, 356, 367, 373, 384, 388, 392.
- 397 is a wall for this colouring: colour 0 at 397 creates 35 monochromatic sets (e.g. {8,15,163,211}),
  colour 1 creates 140 (e.g. {1,6,37,353}).
- Known values through the grower (`known/`): the [8] colouring 00101110 has no monochromatic 2-set and all
  2^9 colourings of [9] have one (F(2) = 9); our July [53] colouring has no monochromatic 3-set and both
  extensions to 54 have one (consistent with F(3) = 54, whose upper bound is the July LRAT certificate).
- Every witness in the submitter's repository (w331, w372–w396) checks clean with `fs4_direct`.

## Novelty

No value of F(4) found in the literature (Erdős–Spencer 1989, Taylor 1981, BENTW 2017, Balogh–Lavrov–Shakan–
Wagner 2019), in OEIS (no Folkman-number entry; 1, 9, 54 matches only unrelated sequences), or on
erdosproblems.com/531 (0 comments, 0 proof claims, 22 Oct 2026). Prior best we know: F(4) ≥ 201, our July report.
The submitter's PR teorth/erdosproblems#490 (open) records the same bound.

## Hostile referee

A separately briefed Opus seat, told to refute and kept away from our checkers, returned **HOLDS WITH CAVEATS**
(`referee/`). Its own instruments: `bitcheck.py` (per-colour bitmask: candidate c's for a monochromatic pair
{a,b} are `K & K>>a & K>>b & K>>(a+b)`, candidate d's the AND of `K>>s` over the 8 subset sums of {a,b,c}, so
the sum ≤ N bound enforces itself), `npbrute.py` (numpy brute force), `partcount.py` (eligible 4-sets =
partitions of m−10 into parts ≤ 4: 40,781,268 at N = 396, 2,535,064 at N = 200 = our July count). Both checkers:
0 monochromatic on w396; all-zero and all-one give 40,781,268; 372 of 396 single flips flagged, e.g. flip 200 →
A = (11,39,111,150) monochromatic; colour(396) = 0 instead → 10 sets, e.g. (8,21,163,204). We re-ran
`bitcheck.py` ourselves (strip mode: 0; first-line-only mode: N = 395, 0).

Convention, quoted from the rendered page of Erdős–Spencer 1989 (`referee/es-1.png`): "For S⊂N the sumset P(S)
is defined as the set of all sums a₁+⋯+a_t, t arbitrary, a_i distinct elements of S. Let F(k) denote the least
n so that if [n] (={1,…,n}) is two colored there is a k-set S with P(S)⊂[n] and P(S) monochromatic." BENTW
(arXiv:1703.02473v2) says the same. The only reading under which the witness fails is multisets (4,457
monochromatic, first (1,6,6,37)), which both sources exclude.

Caveats (none touch the bound): (i) the file layout above — the referee asks for a 396-byte single-line file;
its SHA-256 would be 2a57e17ea0bea652699a3149c5ac9c0ca71bdf77029b9f52a7fbb5c53ca11f2e (`referee/w396.norm.txt`;
we reproduced the hash). (ii) The repository README's sentence that every witness w200–w396 (149 files) "was
re-checked with … verify/f4_check.c … every file reports mono_cubes=0" is not supported by `validation.log`:
the log has 146 OK lines, its lines are in another checker's format (`N=394 mono=0 OK zero`; early ones `N= OK
zero`), not f4_check's `N=%d mono_cubes=%lld`, and most are dated 16–17 Oct, before commit 31cde83 (18 Oct
11:04 +0300) changed `int lo=0, hi=1;` to `int lo=0, hi=0;` — with `hi` pre-set to 1, f4_check could only ever
flag a set monochromatic in colour 0. We confirmed all three from the repository. w396 itself is verified
directly here, so this affects the repository's narrative, not the result.

## Reproduce

    gcc -O2 -o fs4_direct checks/fs4_direct.c && ./fs4_direct submitted/w396.txt      # ~1 s
    python3 checks/fs_extend.py submitted/w396.txt 4                                   # ~0.5 s

## Scope

A lower bound only. Nothing here bounds F(4) from above (no finite upper bound below Taylor's tower is known
to us); the asymptotic question of #531 is untouched.
