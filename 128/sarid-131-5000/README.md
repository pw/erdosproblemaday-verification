# Erdős #128 — referee bundle for Amir Sarid's "Sparse halves in triangle-free graphs: a bound of 131/5000" (2026-10-12)

**Claim refereed.** Sarid (4 Aug 2026; posted to the erdosproblems.com/128 proof-claims tab 7 Aug 2026; repo
`aimir/erdos-128-sparse-halves` @ `ba85f319`): every triangle-free graph on n vertices has ⌊n/2⌋ vertices spanning ≤ (131/5000)n²
edges, conditional on Balogh–Clemen–Lidický Theorem 2(a) (D₂ ≤ n²/23.5 for n large). Previous best: Razborov 27/1024.

**Verdict.** **HOLDS AS READ** (math, cert, lean seats; host hand-check) with one external **GAP, disclosed by the author**: Balogh–Clemen–Lidický Theorem 2(a), the max-cut input, exists only as a proof sketch in a six-page EuroComb 2021 extended abstract (no journal version, no public certificate — sources seat). So β ≤ 131/5000 is label (b): rigorous modulo BCL 2(a). Not ours; #128 stays OPEN; the unconditional record remains Razborov's 27/1024. Kernel replay of the Lean: GREEN (standard axioms, statement MATCH, both negative controls behave) — see below. Two errors on the live erdosproblems.com/128 page found (sources seat), staged for Patrick, nothing sent.

**Chain.** Lemma 2.1 (β ≤ β*) → split at ρ = 7/22 → [ρ ≥ 7/22] Lemma 3.2 (edge splitting, = Razborov Prop 1.1) + Prop 3.1 (C₄ certificate,
γ = 3/64 + 2·10⁻¹¹, tight at Clebsch) → Prop 3.3 (79203/3025000 < 131/5000) · [ρ < 7/22] BCL 2(a) + Lemma 2.2 (blow-up) → Cor 4.2 →
Lemma 4.3 (some vertex has S_x ≥ 4μ³) → Lemma 4.4 (one-step saving ≥ 4L(α)μ³) → §4.2 (two halves) → Lemma 4.5 (max at a* = 88/417 < 131/5000).

**Labels.** (b) rigorous modulo BCL Thm 2(a) — itself an announced, computer-assisted bound in a EuroComb 2021 extended abstract with no public
certificate and no journal version (sources seat); (d) the C₄ certificate and the Lean; (a) everything else.

## Instruments (what was recomputed, by which route)
| step | author | ours |
|---|---|---|
| Lemmas 2.1–4.5 arithmetic | hand | host hand-check (`own/NOTES.md`) + math seat exact rationals + grid/local maximiser (`seats/math/`) |
| Lemma 4.3 / 4.4 | proof | math seat: 207 + 14,800 randomised cases with mutation controls (`seats/math/lemma43_44.py`), exact-equality cases found and broken on purpose |
| C₄ certificate | `verify_clebsch_tangent_certificate.py` | rerun (`own/author_verifier_rerun.log`); independent verifier (`seats/cert/myverify.py`); exact count on all triangle-free graphs ≤ 10 vertices (`own/c4probe.py`, mutation control) |
| Lean | author's `lake build` + axiom audit | source audit (`seats/lean/`), kernel replay (`replay/`: build, AxiomAudit, Probe (statement shape by `Iff.rfl`/`one_mul`), sorry negative control, wrong-shape negative control, `statement_match.txt`) |
| BCL dependence | quoted | sources seat (`seats/sources/`): extended abstract only, no certificate; `own/efps_variant.py`: n²/18 in its place gives ≥ 0.0299 |
| world | — | teorth db, Formal Conjectures, arXiv, openai/math: no newer bound, no reaction, not in print |

## Reproduce
- `~/.venv/bin/python -I own/c4probe.py 10` (≈10 s) · `python3 -I claim/verify_clebsch_tangent_certificate.py` (14 s, needs networkx)
- `seats/cert/myverify.py` (independent verifier; see its REPORT.md for controls)
- `replay/run.sh` (Mathlib v4.30.0 @ c5ea0035 — the claim's pin — toolchain v4.30.0; on this box the packages were hard-linked from a sibling project; elsewhere `lake exe cache get`)

## Layout
`own/` host instruments · `claim/` the paper, certificate, verifier, README at ba85f319 (sha256 in COMMIT.txt) · `live/` erdosproblems.com captures
(12 Oct 2026) · `seats/` briefs + the four reports with their scripts/logs · `replay/` kernel replay artefacts · `SHA256SUMS`.

## Kernel replay status (`replay/`)
Run 1 (2026-10-12 18:18Z): `lake build` killed at `HostCheckpoints.Host27.Chunk0` — `Lean exited with code 143` at ~19:50Z (about 5,500 s in; lake reported the
failed build at 11,951 s after the other running chunks finished); cause = the box's earlyoom sent SIGTERM to two `lean` processes at 19:50Z (`replay/earlyoom_2026-10-12.log`), not a proof failure. Run 2 (2026-10-13 09:06Z, resumed from the 674 oleans already built):
`build` rc 0 (9,157 jobs) · `axioms` rc 0: the five audited declarations (`provider_of_eventual`, `sparse_half_131_5000`, `formalConjectures_131_5000`,
`checkedC4FlagCertificateProvider`, `certificate_all_triangleFree_masks`) each depend on exactly `[propext, Classical.choice, Quot.sound]` · `probe` rc 0 (endpoint
type printed with pp.all; Formal-Conjectures shape by `Iff.rfl`) · `negcontrol` rc 0 with `sorryAx` present (as required) · `wrongshape` rc 1 (as required) ·
`statement_match.txt` = MATCH. `leanchecker --fresh Erdos128` was started by the driver and deliberately killed (memory headroom for the #3 replay running on the
same box; the `143 60s` row); `replay/leanchecker_after_3.sh` re-ran it once that build landed: started 2026-10-13 09:50:08Z (nice 19, cores 8–15), **rc 0 after 12,796 s**
(`steps.tsv` row `leanchecker_fresh 2026-10-13T13:23:24Z 0 12796s`; `leanchecker_fresh.log` is empty — leanchecker prints nothing on a pass). Negative control run
the same day (`replay/leanchecker_negcontrol.log`): `lake env leanchecker --fresh Erdos128.NoSuchModuleXYZ` exits 1 in 15 s with `Could not find any oleans`, so the
instrument can fail. The entry's pending sentence was closed 2026-10-13 ~15:3xZ (15:00Z cron seat).
