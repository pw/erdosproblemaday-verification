# Erdős #341 — Zhiheng Li's disproof (with GPT-5.6 Sol), refereed — 2026-10-13 (21:00Z erdos cron seat, Fable 5.1)

Entry: `/day/341-li-disproof-refereed`. Problem: extend a finite seed greedily by the least integer not of the form
a_i + a_j, i, j ≤ n (equal indices allowed — Dickson's rule as Erdős–Graham 1980 p.53 state it); are the gaps always
eventually periodic? **Claim refereed: NO** — the seed A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97}
has a non-eventually-periodic gap sequence (Li, 9 Aug 2026, proof-claims tab; Lean 4; Formal Conjectures research-solved
2026-09-18, PR #6070). Verdict: HOLDS AS READ; kernel replay green; FC statement bridged by kernel check; nothing in the
disproof is ours. Refereed at commit `c1d9121` = tag v2.1.0 = Zenodo 10.5281/zenodo.22030579 (the paper cites the v2.0.1
deposit 10.5281/zenodo.22030511; Lean files byte-identical across versions per seat A's world search).

## Chain
1. **Live state** (`live/`): erdosproblems.com/341 + proof-claims tab + comments thread (13 Oct, via Hetzner),
   Formal Conjectures `341.lean` (+ GitHub commit history of the file), Zenodo record 22030511, the Erdős–Graham 1980
   p.53 OCR (`pg-049.txt`) and the Dickson bibliography line, Green's Problem 7 excerpt, plby's re-hosting (`plby/`).
2. **Li's artefacts frozen** (`li/`): paper TeX + PDF, the three Lean files + project files, at commit `c1d9121`
   (`COMMIT.txt`).
3. **Independent reproduction** (`greedy/`): `greedy341.c` — bitset greedy from the seed under either rule
   (`distinct=0` Dickson, `=1` Queneau), writes the element list; `li_eq_1e7.log` (1,224,508 terms ≤ 10^7, census mod 49,
   suffix period probe), `li_dist_1e7.log`, `sq_eq_2e6.log`, `sq_dist_2e6.log`; `ELEMS_SHA256SUMS.txt` for the four
   element files (not committed; ~2 min to regenerate: `gcc -O2 greedy341.c && ./greedy341 10000000 li_eq_1e7 0 <seed>`).
   `check_li.py`: Li's closed-form S (transcribed from his Lean `S`/`Y0`/`Y1`/`Y2`/`D`/`B`) vs the greedy set at every
   n ≤ 10^7 → 0 mismatches; S∩[1,97] = seed; Lemma 3.2 (shield) recomputed; controller identities on [0, 8^7); exit 0
   only if all pass. `mutate_check.py`: four mutations (drop B-residue 48; widen a Y0 block; flip one greedy bit; drop
   14 from P) → each FAIL with the mismatch count printed (204,081 / 4,681 / 1 / shield false).
   `certify.py`: the July finite all-future certificate (/report/341 Lemma [a]) for either rule, with the proposed
   periodic set built from the detected period and the recurrence recomputed on it by FFT sumsets (not from the greedy
   run). Cutoff: equal rule 2N+q−2 (July); DISTINCT rule 2N+2q−2 — the docstring carries the one-case proof change (a
   residue whose only tail representation is a double needs two tail elements of that residue below x). ⚠ The first
   version used 2N+q−2 for both rules; seat B's blind read found the gap and all distinct-rule runs were redone
   (`certify_runs.log`). Results: Li's seed under the DISTINCT rule → CERTIFIED (gap period 693, membership period
   5,733 from N = 3,364, recurrence through 18,192, E+R = Z_q \ R with |E| = 706, |R| = 693, |E+R| = 5,040 residues);
   {1,4,9,16,25} equal rule → CERTIFIED 224/1,176 from 440, recurrence through 2,054 (= July + Kitamura);
   {1,4,9,16,25} distinct rule → CERTIFIED 10/41 from 27, recurrence through 134; negative controls: Li's seed, equal
   rule, the locally visible period 6 → NOT CERTIFIED (violation at 12,845,035; E+R false); distinct rule with the
   wrong period 692 → NOT CERTIFIED (1,207,999 violations). The suffix-period probe in `greedy341.c` originally
   labelled a period "PERIODIC-COMPATIBLE"; relabelled after seat A pointed out the label is meaningless for the infinite
   sequence (logs regenerated with the new label; element files unchanged — `ELEMS_SHA256SUMS*.txt`).
4. **Kernel replay** (`lean-replay/`): `lean_driver.sh` → `steps.tsv`: toolchain v4.33.0-rc1 installed by elan;
   `lake exe cache get` 8,643 files (first attempt died on a full disk — the box hit 0 bytes free mid-download; six
   finished replay trees were deleted and the step rerun, rc 0, 52 s); `lake build` 8,663 jobs, 0 errors (`build.log`:
   Shield 86 s, Erdos341 15 s, Erdos341g 101 s); `Audit341.lean` → `audit.log`: pp.all of `erdos_341_negative` and of
   GreedyExtension / LeastGreedyStep / PrefixPairSum / EventuallyPeriodic / PairSum, plain prints of Seed / S /
   enumeration / gap / enumOf / gapOf, and `#print axioms` for erdos_341_negative, S_is_greedy,
   least_next_rule_after_fixed_seed, gap_not_eventuallyPeriodic, Erdos3417p.theorem_5_1_nonperiodicity — all
   `[propext, Classical.choice, Quot.sound]`; `NegControl341.lean` → `negcontrol.log`: a sorry'd theorem reports
   `sorryAx`; `source_scan.log` empty (no sorry/admit/axiom/native_decide/implemented_by/extern/unsafe/partial/opaque
   in first-party sources); `leanchecker` non-fresh over both modules rc 0 (46 s), missing module rc 1;
   `leanchecker --fresh LeanProject` (single top module = the whole closure incl. Mathlib): **rc 0 after 3,088 s**
   (started 21:27:18Z, landed 22:18:46Z; `steps.tsv` row `leanchecker_fresh_LeanProject`; the log
   `leanchecker_fresh_LeanProject.log` is empty — leanchecker prints nothing on success, as in our #3/#160 replays; the
   missing-module control `leanchecker_neg.log` exits 1 with a message). The first `--fresh` attempt
   (`leanchecker_fresh.log`) failed on a usage error (two modules given), not on the proof. Note the non-fresh
   `leanchecker` replays only the named modules (Erdos341, Erdos341g), so `Erdos341Shield` — the kernel-`decide`d residue
   certificate — is re-checked only by the `--fresh` pass.
   **FC bridge** (`seats/A/bridge/`, replayed by the host: `steps.tsv` rows `bridge_Bridge` rc 0 / `bridge_NegSorry` rc 1 /
   `bridge_NegQueneau` rc 1; logs `bridge_*.log`): `Bridge.lean` states Formal Conjectures' `erdos_341` verbatim with
   `answer(False)` read as `False` and proves it from `least_next_rule_after_fixed_seed` + `gap_not_eventuallyPeriodic` —
   axioms `[propext, Classical.choice, Quot.sound]`; `NegSorry.lean` (sorry in place of the aperiodicity lemma) prints
   `sorryAx`; `NegQueneau.lean` (FC's sumset changed to i < j) fails to typecheck. The host diffed the bridge's statement
   against `live/fc341.lean`: identical modulo the theorem name and `answer(False)`→`False`.
5. **Statement match**: the Lean theorem = GreedyExtension Seed S 97 ∧ (∃ i, enumeration i = 97 ∧ ∀ j ≥ i,
   LeastGreedyStep enumeration j) ∧ ¬EventuallyPeriodic gap, with enumeration = Nat.nth S (0-indexed, i = 20),
   PairSum/PrefixPairSum allowing equal summands/indices, EventuallyPeriodic = ∃ N p, 0 < p ∧ ∀ n ≥ N, f(n+p) = f n.
   Formal Conjectures' `erdos_341` (answer(False)) quantifies a : ℕ → ℤ with IsLeast in ℤ; plby's wrapper
   `not_erdos_341` is over ℕ; the ℤ-cast is not kernel-checked against `erdos_341` itself (noted on the page).
6. **Seats** (`seats/`): A — hostile referee (Opus, tools; `referee_A.md`, `world_search.md`, its own instruments
   `literal_greedy*.c`, `fft_recurrence.py` (0 violations for 97 < t ≤ 134,217,727), `shield_ctrl.py`, `pfamily.py`
   (18 ≤ p ≤ 400), `fft_pfamily.py`, the bridge): HOLDS AS READ, ten EXPOSITION objections, two scope facts (equal
   summands essential — Queneau variant untouched; seed not sum-free — Cameron/Calkin–Finch Conj. 4.2 untouched), family
   threshold not sharp (p ∈ {12,14,15,16,17} pass, 13 fails, p = 7 fails). B — blind consistency read of the rendered page
   (`blindread_B.md`, `distinct_gap.py`): 10 substantive + 20 minor, all applied before deploy (lemma numbers, Zenodo
   version, "closed in the literature", leanchecker coverage, Queneau mechanism, certificate cutoff, square seed vs [12],
   family statement not matched, two credit sentences). `render_final_2026-10-13.txt` = the page as deployed;
   `apply341.py` / `smoke341.mjs` / `render341.mjs` = the ship tooling.

## Reproduce
```
gcc -O2 -o greedy341 greedy/greedy341.c && ./greedy341 10000000 li_eq_1e7 0 1 2 3 5 7 13 22 27 28 32 36 40 47 48 52 63 71 77 81 89 97
python3 greedy/check_li.py 10000000 && python3 greedy/mutate_check.py
git clone https://github.com/LiAlreadyExists/Erdos-341 && cd Erdos-341 && git checkout c1d9121 && lake exe cache get && lake build
lake env lean ../lean-replay/Audit341.lean
```
Memory note: the replay needs ~6.5 GB for `leanchecker --fresh`; the build itself under 4 GB. SHA256SUMS covers every file.
