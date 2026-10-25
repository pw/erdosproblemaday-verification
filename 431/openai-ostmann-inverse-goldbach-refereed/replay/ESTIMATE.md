# #431 (OpenAI family 013, Ostmann) kernel replay — estimate written BEFORE launch (06:2xZ 2026-10-23, 06:00Z erdos seat)
- Closure from the targets (Ostmann.Complete, Ostmann.Main, ComparatorChallenges.OstmannComplete/OstmannPrimes): 7,582 modules
  = OAI 7,518 (Ostmann 7,335 + Jacobsthal 135 + PrimeGaps 48) + PNT+ 34 + BernoulliRegular 20 (AINTLIB) + StrongPNT 7 + Common 1 + 2 comparators.
  (7,716 Ostmann files exist; 381 are not imported by the targets — e.g. MainWithout* variants, All.lean.)
- Reference: cert-machine kernel-run 38019899278 OstmannComplete: 12,167 lake jobs in 3,528 s (Azure), Ostmann modules 2.5–5 s each in its log tail, maxRss 8.30 GB.
  Our #970 run: 829 modules, Σ per-module wall 7,562 s (9.1 s/module), max RSS 7.39 GB.
- Plan: W=4, nice 19 / ionice idle-ish, launch gates MemAvailable ≥ 22 GB and disk free ≥ 8 GB. Box at launch: 37 GB available, two #552 cadicals (2.3 GB, 38 d old), load ~8.
- Expected: Σ 30,000–70,000 CPU-s ⇒ 2–5 h wall at W=4. Oleans: unknown at this scale (#970: ~1–2 GB per 850) ⇒ 5–15 GB; disk 28 GB free after cache get ⇒ the disk gate may pause it; then free /tmp/claude-1000 old session dirs.
- Then: comparator challenge modules (in the closure), pp.all statement probes vs ComparatorChallenges, --trust=0 #print axioms, sorry negative control, FC erdos_431 bridge; leanchecker --fresh only if disk allows (~1 h, 8 GB).
- After banking: rm -rf /tmp/erdos0300/lean/mathlib4/.lake (7 GB) and lean-build/out per the disk guard.
