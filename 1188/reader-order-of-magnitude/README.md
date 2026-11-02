# Erdős #1188: reader submission 8gfcew (Pedro Martins), reviewed 2 November 2026

**Claim.** F(x) is the number of minimal covering systems with distinct moduli in [2, x], as erdosproblems.com/1188
words it (same moduli with different residues count separately). The preprint "The number of minimal covering systems
with distinct moduli" (Zenodo 10.5281/zenodo.23427851, 16 Oct 2026, 34 pp., SHA-256
64039de93e248ef0ae2862a107c568c10a787b432e4272c7100144c65fe69d0d; not included here) proves:

- (c₁ + o(1)) x log x ≤ log F(x) ≤ (1 − log 2) x log x + 1.5x, with c₁ = 0.0672 and the upper bound valid for all x ≥ 2;
- log F(x) ≥ x/2 − 3x/log x for all x ≥ 40.

Hence F(x) = x^Θ(x).

**Verdict: VERIFIED** (see erdosproblemaday.com/submission/8gfcew). The leading constant is open.

## Who checked what

Each seat is an AI (Claude Opus 5.5) with tools, separately briefed to refute (`BRIEF_COMMON.md`). We ran none of the
submitter's code. His Section 8 "verification supplement" is not in the Zenodo record.

| Folder | Scope | Verdict |
|---|---|---|
| `seatA/` | Thm 1.3 (local lemma), Cor 1.4, Thm 1.5, Prop 7.2; Construction 3.1, Prop 3.2, Thm 1.2, Prop 7.1 | HOLDS WITH NOTES |
| `seatB/` | Section 4 (split construction, splitting trees, Thm 4.8, constants) and Section 6 | HOLDS WITH NOTES |
| `seatC/` | Section 8 tables: exact F(x) for x ≤ 24, k(x) | partial at snapshot: see `seatC/STATUS.md` |
| `seatW/` | prior art: Snyder's July Lean claim, the teorth DB, Formal Conjectures, the literature, Er80 p. 95 | HOLDS WITH NOTES |
| `host/` | the reviewing seat: line-by-line read of Props 3.2, 4.3, 4.7; explicit ranges; Examples 3.3, 4.4, 4.5 | — |

The `REPORT.md` files were saved by the host from each seat's final message, because the harness does not let seats write
`.md` files. Scripts and outputs are the seats' own.

## Main numbers, each from two routes

- **Upper bound, finite range.** The paper checks 2 ≤ x ≤ 81,796. We checked every integer up to 10⁸ (`seatA/upper.py`)
  and up to 400,000 (`host/explicit.py`). Max of (Υ(x) − (1 − log 2) x log x)/x = 0.5418, at x = 50. No violations.
- **Lower bound, finite range.** The paper needs 40 ≤ x < e²⁰. We checked every step endpoint up to X ≈ 10¹⁶ plus every
  integer up to 10⁷ (`seatA/lower.py`), and every step below e²⁰ (`host/explicit.py`). The tightest point is x = 928,
  with margin 0.0604x. No violations.
- **Constructions.**
  - Construction 3.1 was built literally and checked exactly over ℤ/L: all 96 data at P = 5 and all 69,120 at P = 7 give
    valid, pairwise distinct systems (`seatA/construction.py`).
  - Examples 4.4 and 4.5 were rebuilt from the construction rules, and the printed residues reproduce. All 6,720 paddings
    of 4.4 and all 120 orderings of 4.5's I-part-35 group are valid (`host/examples.py`, `seatB/split.py`).
  - 48 random Construction 4.2 instances are exhaustive over periods up to 12,252,240 (`seatB/random_split.py`).
  - Two large instances were checked, with 46,984 and 78,654 classes (`seatB/large.py`).
  - Negative controls fail as they must: a dropped class, a redundant class, a repeated modulus, a deleted leaf,
    a duplicate padding, a padding not dividing M_F(q), and a τ breaking τ(ι(16)) = 16.
- **Constants.** We computed Dickman ρ two ways, with controls ρ(2) = 1 − log 2 and ρ(3) (`seatB/constants.py`).
  - κ₁ = 0.012679471691.
  - C₁(0.225) = 0.067219355825 and C₂(0.2175) = 0.212875840462.
  - Lower Riemann certificate at mesh 10⁴: C₁ ≥ 0.0672115579 and C₂ ≥ 0.2128359667. This is high-precision floating
    point, not interval arithmetic. The control at mesh 2000 correctly fails to certify.
- **Printed systems.** The 18-class system with moduli ≤ 48 (Section 8.6) and the 14-class system on the divisors of
  216 (Table 7) are minimal distinct coverings (`host/printed_systems.py`).

## Not done

- Snyder's Lean was read, not built.
- Rosser–Schoenfeld's equation numbers were not checked (a bot wall). The inequalities as quoted were checked numerically.
- No interval arithmetic.
- No human referee.
