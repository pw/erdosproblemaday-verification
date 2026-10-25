# #371 / OpenAI family 012 replay estimate (06:2xZ 2026-10-22, before any CPU)
- Closure: 1,792 OAI modules (1,456 JointDickman + 216 TwoPointCorrelations + 61 Jacobsthal + 43 PrimeGaps + 16 EgyptianFractions)
  + patched PrimeNumberTheoremAnd (Erdos970.*) + patched StrongPNT (Erdos970.*, 26k-line patch) + LeanArchitect if imported.
- Reference: #416 829 modules / 30 min at W=5; #986 858 modules. Scale ⇒ ~65–100 min at W=5 (lean -j1 each, LEAN_NUM_THREADS=1).
- RAM: ~1.5–8 GiB per lean; gate MemAvailable ≥ 18 GiB per launch; box 39 GiB avail, cadicals 2.3 GiB (34-day, untouchable).
- Disk: Mathlib cache ~6.5 GB + oleans ~1–2 GB; df 36 GB free at start (guard ≥30 GB satisfied).
- leanchecker --fresh after: ~1 h single-thread (comparable closures 3,450–3,620 s); may land after the entry ships → close sentence in place.
