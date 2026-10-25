# #184 — kernel replays, ESTIMATE WRITTEN BEFORE CPU (03:00Z erdos seat, 2026-10-20 ~03:15Z, opus 5.5, Team seat 3/yt3)
(The 10-15 09:00Z seat's estimate for the OpenAI half is kept below; that seat died unlogged after `cache get`.)

Box at 03:00Z: load 12.5; #85 t1_rep0 Lean alone, uncapped, 28–29 GB RSS (HWM 30.7), MemAvailable 17 GB; #552 cadicals ×2 (2.3 GB);
disk 30 GB → 42 GB after uninstalling five unpinned toolchains (v4.24.0 v4.27.0 v4.29.0 v4.30.0 v4.30.0-rc2; v4.31.0 = #85's, kept).

A) OpenAI (family 181): 34 modules / 21,451 lines, imports Mathlib only. Toolchain v4.34.1 (scratch elan /tmp/oaimath/166/…, present);
   Mathlib d13f23b7 cache get ~7 GB disk (running now). Build one thread nice 19: 20–60 min, ≤ 8 GB RSS; probes minutes;
   leanchecker --fresh ≈ 1 h (3,462–3,765 s on #138/#508/#90). Total disk ≈ +8 GB.
B) Coffey: formal/ 601 files / 93,195 lines; lake project (lakefile.toml — no code runs at configure time), deps Mathlib v4.33.1 (0df444a3),
   formal-conjectures 2424bb48 + 7 small packages. Toolchain v4.33.1 install ~3 GB; lake package clones ~2–3 GB; Mathlib cache ~7 GB;
   FC's needed oleans built from source (FormalConjecturesUtil closure — unknown size, guess ≤ 30 min). Their record: build on a 7 GiB
   GitHub runner; leanchecker EG 11–13 min, EGTest ~1 min, --fresh EGCheck.Final 33–37 min; "about 16 GB of RAM" for the checks.
   Our estimate one-to-two threads nice 19: build 1.5–4 h, checks ~1 h, ≤ 16 GB RSS. Disk ≈ +13 GB ⇒ ~21 GB free after both.
GATES: both wait for #85's t1_rep0 (pid 2058325) to exit, then MemAvailable ≥ 28 GB before every Lean step, and a GO file written after the
source-audit seat reports (untrusted code elaborates on this box). B runs after A's build (not concurrently). Never evict a solver.
Disk guard: ≥ 30 GB free before each cache get (A: 42 GB; B: will check). Delete both .lake trees when banked.
