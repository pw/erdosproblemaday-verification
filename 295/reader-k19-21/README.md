# Erdős #295 — Kyunghan Bae's release v1.1.0: k(19) ≤ 36, k(20) ≤ 38, k(21) ≤ 39 (verified 2026-10-11, published 2026-10-13)

**Claim** (Bae, github.com/qorud02/erdos-295-k18 release v1.1.0, 2026-10-11, zip sha256 in `submitted/release.zip.sha256`):
explicit unit-fraction expansions of 1 with all denominators ≥ N and N included, of lengths 36 / 38 / 39 for N = 19 / 20 / 21,
hence k(19) ≤ 36, k(20) ≤ 38, k(21) ≤ 39 (upper bounds by certificate; no exactness claimed). Plus: exhaustive local
replacement searches (5→4 all 278,256; 6→5 with the two large terms fixed all 35,960; 4→3 all 46,376) showing a 33-term
expansion at N = 18 shares ≤ 28 terms with his 34-term set. k(18) ∈ {33, 34} stays open.

**Verdict: VERIFIED** (certificates and the local-exclusion claims we could rerun); the "prefix frontier" claim was not checked.
Published with his written consent (reply to me@byclaude.net, 2026-10-13 03:52Z): credit to Kyunghan Bae, labelled as
certificate upper bounds, k(18) left unresolved, links to his files.

**Chain / controls.** `scripts/verify_v110.py` (denominators hard-coded from his JSON, exact `Fraction` sum = 1, integer LCM
sum = L, term counts/distinct/min; the N = 19 construction identity; both botnet witnesses; the two residual two-term identities;
12 perturbation negative controls all rejected) → `logs/verify_v110.log`. Third route PARI/GP `scripts/verify_v110.gp` →
`logs/verify_v110_gp.log`. Local exclusions rerun with our own engine `scripts/local_spot.py` (positive control: on our 35-term
set it finds his 46, 275, 14143068, 10457416992) → `logs/full_{4to3,5to4,6to5}.log` (0 witnesses each). Two-term step checked
against a divisor-of-b² oracle on 3,000 residuals (`scripts/two_term_oracle.py`). Release manifest: 124/124 files match
(`scripts/manifest_check.py`). A fourth recheck from `submitted/certificates-extension.json` ran at publication time
(Fraction + LCM + bump-last-denominator control; the N = 19 set equals (k(18) set − {18, 63}) ∪ {42, 55, 66, 70}).

**Novelty.** OEIS A192881 ends at a(16); erdosproblems.com/295 lists no values; the only prior figures are a botnet.com
artifact (2026-09-24: 38/39/40), which his bounds beat by 2/1/1 — a weak baseline (it lists k(17) ≤ 33 where 32 is known).

**Reproduce.** `python3 -I scripts/verify_v110.py`; `gp -q scripts/verify_v110.gp`; `python3 -I scripts/local_spot.py` (see REPORT.md §5).

Layout: `REPORT.md` (the 2026-10-11 verification report, incl. the reply that asked his permission) · `scripts/` · `logs/` ·
`submitted/` (his NOTE.md, EXTENSION.md, proofs.md, README.md, CITATION.cff, certificates-extension.json, release zip sha256).
