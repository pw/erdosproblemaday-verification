#!/usr/bin/env python3
"""drive_v11 = drive2 with ENDPOINTS = the v1.1 InventoryNonzero module and BIG guarded for an empty strata set.
Independent cold replay of the Erdős #85 order-49 capstone closure (lean-genius @ 2029149d7e42).

Our own scheduler, not the authors' run.py: one `lean -j1` per module in dependency order into an
EMPTY output root, Mathlib/package oleans from the pinned cache, the H3 triple-search runtime compiled
from source into a plugin (as their runner does), the 13 H7 positive-triple certificate modules
(include_str of the published packed LRAT) run one at a time.

Memory safety (the box also runs 35-day cadical campaigns + an interactive SAT run):
  * every Lean child gets oom_score_adj=1000 => any OOM victim is ours, never theirs;
  * every Lean child gets `-M <MB>` (Lean's own allocation cap);
  * a job only launches if MemAvailable - reservations(running) >= FLOOR + reservation(job);
  * a watchdog SIGKILLs our largest Lean child if MemAvailable < KILL_GB, then stops scheduling.
Resumable: a module whose fresh olean exists and whose steps.tsv row says rc=0 for the same
source sha256 is skipped. steps.tsv is append-only.

Usage: drive2.py <proofs_dir> <out_dir> [workers] [--dry]

drive2 (2026-10-19 15Z seat) = drive.py + two changes, nothing else:
  * CRITICAL-PATH ORDER: ready modules sorted by the H7 strata closure first (strata are serialised and
    ~10 h here), then by longest remaining path measured with the AUTHORS' per-module elapsed times
    (their attempt-2 RUN.json); drive.py sorted alphabetically, which put every strata module last.
  * ADOPTION: Lean jobs left running by a previous driver (their own sessions survive the driver) are
    adopted instead of killed: polled until exit, then judged from the log (/usr/bin/time's MAXRSS line
    present, no 'Command exited with non-zero status' / 'terminated by signal', no diagnostic) + a
    non-empty olean; pass => row with note 'adopted (rc inferred from log)'; fail => re-queued.
  * (16:5xZ fix) finished jobs are retired BEFORE readiness is computed (drive.py did it after launching, so each
    freed slot went to a long part before the finished module's dependents were ready), and a ready strata-closure
    (critical) module may take ONE slot beyond WORKERS when no critical module is running.
  * (17:5xZ fix) while the biggest certificate is ready but cannot start, nothing else is launched (else the small
    certificates keep refilling memory and starve it).
--dry prints the adopted set and the first 25 of the ready order, launches nothing.
"""
import functools, hashlib, json, os, re, signal, subprocess, sys, threading, time
sys.setrecursionlimit(20000)
from pathlib import Path

PROOFS = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 5
DRY = "--dry" in sys.argv
TOOLBIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin"
ENDPOINTS = ["Proofs.Erdos85OneHighV2InventoryNonzero"]   # drive_v11 (2026-10-28): v1.1 nonzero cone only
RUNTIME = "Proofs.Erdos85H3TripleCompletionRuntime"
INIT = "initialize_Proofs_Erdos85H3TripleCompletionRuntime"
BIG_ALONE_GB = 36       # (22:2xZ) MemAvailable needed to start BIG with nothing else of ours running
FLOOR_GB, KILL_GB = 12, 9   # drive.py: 18 — with MemAvailable ~38 GB the 22 GB strata job could never launch
STRATA_RE = re.compile(r'include_str\s+"Certificates/strata-lrat/')

FRESH = OUT / "lean"
LOGS = OUT / "logs"
STEPS = OUT / "steps.tsv"
for d in (FRESH / "Proofs", FRESH / "Archive/Wiedijk100Theorems", LOGS):
    d.mkdir(parents=True, exist_ok=True)

pkg_libs = sorted(str(p) for p in (PROOFS / ".lake/packages").glob("*/.lake/build/lib/lean"))
ENV = {"PATH": f"{TOOLBIN}:/usr/bin:/bin", "HOME": str(OUT / "home"), "LANG": "C.UTF-8",
       "LEAN_PATH": os.pathsep.join([str(FRESH)] + pkg_libs)}
(OUT / "home").mkdir(exist_ok=True)
if not DRY:
    (OUT / "driver.pid").write_text(str(os.getpid()) + "\n")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def src_of(m):
    if m.startswith("Archive."):
        return PROOFS / ".lake/packages/mathlib" / (m.replace(".", "/") + ".lean")
    return PROOFS / (m.replace(".", "/") + ".lean")


def imports(m):
    s = src_of(m).read_text(encoding="utf-8")
    return re.findall(r'^\s*(?:public\s+)?import\s+(?:all\s+)?([\w.]+)', s, re.M)


# ---- closure + dependency graph (project modules + the one Archive module) ----
deps, stack = {}, list(ENDPOINTS)
while stack:
    m = stack.pop()
    if m in deps:
        continue
    ds = [i for i in imports(m) if i.startswith("Proofs") or i.startswith("Archive")]
    deps[m] = ds
    stack += ds
proj = [m for m in deps if m.startswith("Proofs")]
print(f"closure: {len(proj)} project modules + {len(deps) - len(proj)} Archive", flush=True)
strata = {m for m in proj if STRATA_RE.search(src_of(m).read_text(encoding="utf-8"))}
print(f"H7 strata-certificate modules: {len(strata)}", flush=True)
PRIO_ROOTS = ["Proofs.Erdos85OneHighV2Cnf", "Proofs.Erdos85OneHighV2CapacityInventory",
              "Proofs.Erdos85OrderFortyNineSevenHighT0CanonicalEmptyCubeCnf",
              "Proofs.Erdos85OrderFortyNineSevenHighT0EmptyCountingCore"]
prio, st = set(), [r for r in PRIO_ROOTS if r in deps]
while st:
    x = st.pop()
    if x not in prio:
        prio.add(x)
        st += deps[x]
print(f"priority modules (emitter/inventory closures): {len(prio)}", flush=True)
triple_parts = {m for m in proj if re.fullmatch(r"Proofs\.Erdos85H3TripleCompletionPart\d{3}", m)}
print(f"H3 triple parts (plugin): {len(triple_parts)}", flush=True)
THEIR_RUN = Path.home() / ("MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01/"
                           "release_cold_build_20261011/attempt2-evidence/RUN.json")
THEIRS = {}
for k, v in json.load(open(THEIR_RUN))["completed"].items():
    THEIRS[k if k.startswith(("Proofs.", "Archive.")) else "Proofs." + k] = float(v["elapsed_seconds"])
crit = set()
_st = list(strata)
while _st:
    x = _st.pop()
    if x not in crit:
        crit.add(x)
        _st += deps[x]
rdeps = {m: [] for m in deps}
for m, ds in deps.items():
    for d in ds:
        rdeps[d].append(m)


@functools.lru_cache(None)
def tail(m):
    """longest path from m (inclusive) to an endpoint, in the authors' seconds"""
    return THEIRS.get(m, 60.0) + max([tail(u) for u in rdeps[m]] or [0.0])


print(f"strata closure (critical): {len(crit)} modules; their strata seconds "
      f"{round(sum(THEIRS.get(m, 0) for m in strata))}", flush=True)

done = {}
if STEPS.exists():
    for line in STEPS.read_text().splitlines()[1:]:
        f = line.split("\t")
        if len(f) >= 4 and f[1] == "0":
            done[f[0]] = f[3]
else:
    STEPS.write_text("module\trc\telapsed_s\tsrc_sha256\tmaxrss_kb\tolean_sha256\twarnings\tnote\n")
lock = threading.Lock()


def record(row):
    with lock:
        with open(STEPS, "a") as f:
            f.write("\t".join(str(x) for x in row) + "\n")


def obj_of(m):
    return FRESH / (m.replace(".", "/") + ".olean")


def is_done(m):
    return m in done and done[m] == sha(src_of(m)) and obj_of(m).exists()


def mem_avail_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1048576
    return 0.0


STRATA_FILE_RE = re.compile(r'include_str\s+"(Certificates/strata-lrat/[^"]+)"')


@functools.lru_cache(None)
def reservation(m):
    """expected PEAK anon GB. Strata: scaled from the packed LRAT size (authors: the 1.6 GB t1_rep0 cert
    peaked ~20 GB); everything else 1 GB (measured: H3 parts hold 0.39 GB anon, the rest is shared olean mmap)."""
    if m in UNCAPPED:
        return 24.0     # (00:0xZ 10-20) hit 16 GB RSS capped; reserve enough that the driver does not pack around it
    if m not in strata:
        return 1.0
    f = STRATA_FILE_RE.search(src_of(m).read_text(encoding="utf-8")).group(1)
    gb = (src_of(m).parent / f).stat().st_size / 1e9
    # 18:5xZ recalibration from MEASURED peaks (max RSS − ~6.6 GB shared olean mmap): t3_rep2 0.151 GB → ~4.0 GB anon,
    # t2_rep0 0.243 → ~5.5, t2_rep1 0.283 → ~6.7 ⇒ ≈ 1 + 21·gb for the small ones. t1_rep0 (1.6 GB) is capped at 15:
    # authors' measured peak '~20 GB' (RSS incl. ~6 GB file) and its anon was flat at ~4.95 GB for minutes after load
    # (sublinear), so linear scaling (~34) is wrong; if it does exceed this, the watchdog / earlyoom would take it
    # whether or not small jobs run beside it (they hold ~0.4 GB anon each).
    return max(1.5, min(15.0, 1.0 + 21.0 * gb))   # tiny certs measured ~0.6 GB anon; 3.0 floor starved the box


def anon_gb(pid):
    """RssAnon of the lean grandchild under /usr/bin/time <pid> (0 if not started yet)"""
    try:
        kids = open(f"/proc/{pid}/task/{pid}/children").read().split()
        return max([int(open(f"/proc/{c}/status").read().split("RssAnon:")[1].split()[0]) for c in kids] or [0]) / 1048576
    except Exception:
        return 0.0


def outstanding():
    """reservation not yet materialised, summed over running + adopted jobs"""
    tot = 0.0
    with lock:
        items = [(m, p.pid if p is not None else None) for m, p in running.items()] + \
                [(m, pid) for m, (pid, _) in adopted.items()]
    for m, pid in items:
        held = anon_gb(pid) if pid else 0.0
        if m == BIG and pid:
            # (21:0xZ fix) t1_rep0 outgrew its 15 GB reservation (23.3 GB anon); keep a 2 GB growth margin on top of
            # whatever it holds, so the driver stops backfilling before the watchdog has to act
            tot += max(reservation(m) - held, 2.0)
        else:
            tot += max(0.0, reservation(m) - held)
    return tot


def cap_mb(m):
    # (21Z 10-19) BIG gets NO Lean --memory cap: the authors' accepted cold build ran it uncapped (RUN.json: plain
    # `lean -j1`, 7,831 s, 110 GiB container, 64 GiB budgeted per large certificate); ours reached 23.5 GiB anon and
    # still growing under a 30000 MB cap — an artificial ceiling that would fail it hours in. The box-level guards
    # (watchdog sparing BIG, earlyoom preferring the adj-1000 parts) bound it instead. 0 = omit the flag.
    if m == BIG or m in UNCAPPED:
        return 0
    return 30000 if m in strata else 16000


# (00:0xZ 10-20) a module that hits OUR Lean --memory cap is re-run ONCE uncapped, as the authors built it (RUN.json:
# plain `lean -j1`, no --memory). Specimen: T0CanonicalCnfSatisfaction, a kernel `decide` over 49x49 pairs, threw
# '(kernel) excessive memory consumption detected' at 16000 MB after 482 s; theirs passed in 296 s uncapped. A capped
# failure is a statement about our flag, not about the proof; the uncapped rerun is the test.
UNCAPPED = set()
MEMCAP_RE = re.compile(r"excessive memory consumption|memory exception|out of memory")


running = {}          # module -> Popen
adopted = {}          # module -> (pid, start_epoch)
stop = threading.Event()
failed = []


def preexec():
    os.setsid()
    with open("/proc/self/oom_score_adj", "w") as f:
        f.write("1000")
    os.nice(19)


def preexec_big():          # (21Z 10-19) earlyoom must prefer the small parts over the 6-9 h critical module
    os.setsid()
    os.nice(19)


def run_one(m):
    src, obj = src_of(m), obj_of(m)
    obj.parent.mkdir(parents=True, exist_ok=True)
    if obj.exists():
        obj.unlink()        # never trust a leftover from a killed run
    cmd = ["/usr/bin/time", "-f", "MAXRSS_KB=%M", "lean", "-j1"] + ([f"--memory={cap_mb(m)}"] if cap_mb(m) else [])
    lib = OUT / "libH3TripleRuntime.so"
    if m in triple_parts:
        cmd.append(f"--plugin={lib}={INIT}")
    rel = os.path.relpath(src, PROOFS) if m.startswith("Proofs") else str(src)
    cmd += [rel, "-o", str(obj)]
    cfile = OUT / "H3TripleRuntime.c"
    if m == RUNTIME:
        cmd += ["-c", str(cfile)]
    log = LOGS / (m + ".log")
    t0 = time.time()
    with open(log, "w") as lf:
        lf.write("$ " + " ".join(cmd) + "\n")
        lf.flush()
        p = subprocess.Popen(cmd, cwd=PROOFS, env=ENV, stdout=lf, stderr=subprocess.STDOUT,
                             preexec_fn=preexec_big if m == BIG else preexec)
        with lock:
            running[m] = p
        rc = p.wait()
    with lock:
        running.pop(m, None)
    el = round(time.time() - t0, 1)
    text = log.read_text(errors="replace")
    rss = (re.findall(r"MAXRSS_KB=(\d+)", text) or ["?"])[-1]
    note = ""
    if rc == 0 and re.search(r"\berror:|declaration uses 'sorry'|\bsorryAx\b", text):
        rc, note = 97, "diagnostic"
    if rc == 0 and (not obj.exists() or obj.stat().st_size == 0):
        rc, note = 98, "no-olean"
    if rc == 0 and m == RUNTIME:
        prc = subprocess.run(["leanc", "-O3", "-DLEAN_EXPORTING", "-shared", "-fPIC", str(cfile), "-o", str(lib)],
                             env=ENV, capture_output=True, text=True)
        (LOGS / "plugin.log").write_text(prc.stdout + prc.stderr)
        if prc.returncode != 0 or INIT not in cfile.read_text(errors="replace"):
            rc, note = 96, "plugin-build"
        else:
            note = "plugin sha256 " + sha(lib)
    warn = len(re.findall(r"\bwarning:", text))
    capped = cap_mb(m)
    if rc != 0 and capped and m not in UNCAPPED and MEMCAP_RE.search(text):
        UNCAPPED.add(m)
        requeue.add(m)
        record([m, rc, el, sha(src_of(m)), rss, "-", warn,
                f"OUR --memory={capped} cap hit (not a finding); re-queued UNCAPPED"])
        return rc
    if rc != 0 and m in requeue:
        record([m, rc, el, sha(src_of(m)), rss, "-", warn, "watchdog-killed; re-queued"])
        return rc
    record([m, rc, el, sha(src_of(m)), rss, sha(obj) if rc == 0 else "-", warn, note])
    if rc != 0:
        failed.append(m)
        stop.set()
    return rc


requeue = set()        # modules killed by the watchdog that must run again (not failures)
hold_until = [0.0]     # no new launches before this epoch (set after a watchdog kill)


def _rss_of(pid):
    rss = 0
    try:
        rss = int(open(f"/proc/{pid}/status").read().split("VmRSS:")[1].split()[0])
        for c in open(f"/proc/{pid}/task/{pid}/children").read().split():
            rss = max(rss, int(open(f"/proc/{c}/status").read().split("VmRSS:")[1].split()[0]))
    except Exception:
        pass
    return rss


def watchdog():
    while not stop.is_set() or running:
        a = mem_avail_gb()
        if a < KILL_GB:
            with lock:
                victims = list(running.items()) + [(m, type("P", (), {"pid": pid})()) for m, (pid, _) in adopted.items()]
            best, best_rss = None, -1
            for m, p in victims:
                if p is None:
                    continue
                try:
                    rss = int(open(f"/proc/{p.pid}/status").read().split("VmRSS:")[1].split()[0])
                except Exception:
                    rss = 0
                # /usr/bin/time is the direct child; the lean process is its child: kill the group
                try:
                    for c in open(f"/proc/{p.pid}/task/{p.pid}/children").read().split():
                        rss = max(rss, int(open(f"/proc/{c}/status").read().split("VmRSS:")[1].split()[0]))
                except Exception:
                    pass
                if rss > best_rss:
                    best, best_rss = (m, p), rss
            if best:
                # (21:0xZ 10-19 fix) never take BIG while a smaller job of ours exists: t1_rep0 is 6-9 h of the critical
                # path and sat at 23 GB anon, so 'largest RSS' always named it. A killed small job is re-queued and the
                # driver keeps going (pauses launches 5 min); only killing BIG stops the run.
                if best[0] == BIG:
                    small = [(m, p) for m, p in victims if p is not None and m != BIG]
                    if small:
                        best = max(small, key=lambda mp: _rss_of(mp[1].pid))
                        best_rss = _rss_of(best[1].pid)
                    else:       # (22:2xZ) BIG alone: do not shoot it ourselves; earlyoom (10%) is the honest limit
                        print(f"WATCHDOG MemAvailable {a:.1f} GB < {KILL_GB} with only {BIG} running: NOT killing "
                              f"(rss {best_rss} kB)", flush=True)
                        time.sleep(60)
                        continue
                print(f"WATCHDOG MemAvailable {a:.1f} GB < {KILL_GB}: killing {best[0]} (rss {best_rss} kB)", flush=True)
                if best[0] != BIG:
                    requeue.add(best[0])
                    hold_until[0] = time.time() + 300
                os.killpg(best[1].pid, signal.SIGKILL)
                record([best[0], "WATCHDOG", "-", "-", best_rss, "-", "-", f"MemAvailable {a:.1f} GB"
                        + ("; re-queued" if best[0] != BIG else "")])
                if best[0] == BIG:
                    stop.set()
                time.sleep(15)
        time.sleep(2)


_clk = os.sysconf("SC_CLK_TCK")
_boot = float(open("/proc/stat").read().split("btime ")[1].split()[0])
for pd in os.listdir("/proc"):
    if not pd.isdigit():
        continue
    try:
        argv = open(f"/proc/{pd}/cmdline", "rb").read().split(b"\0")
    except Exception:
        continue
    if not argv or argv[0] != b"/usr/bin/time" or b"-o" not in argv:
        continue
    o = argv[argv.index(b"-o") + 1].decode()
    if not o.startswith(str(FRESH) + "/") or not o.endswith(".olean"):
        continue
    mod = o[len(str(FRESH)) + 1:-len(".olean")].replace("/", ".")
    if mod in deps:
        st0 = float(open(f"/proc/{pd}/stat").read().rsplit(")", 1)[1].split()[19]) / _clk + _boot
        adopted[mod] = (int(pd), st0)
print(f"adopted {len(adopted)} in-flight jobs: {sorted(adopted)}", flush=True)


def judge_adopted(m, st0):
    obj, log = obj_of(m), LOGS / (m + ".log")
    text = log.read_text(errors="replace") if log.exists() else ""
    rss = (re.findall(r"MAXRSS_KB=(\d+)", text) or [None])[-1]
    bad = (rss is None or re.search(r"Command exited with non-zero status|Command terminated by signal", text)
           or re.search(r"\berror:|declaration uses 'sorry'|\bsorryAx\b", text)
           or not obj.exists() or obj.stat().st_size == 0)
    el = round(time.time() - st0, 1)
    warn = len(re.findall(r"\bwarning:", text))
    if bad:
        record([m, 95, el, sha(src_of(m)), rss or "?", "-", warn, "adopted job failed/unfinished; re-queued"])
        return False
    record([m, 0, el, sha(src_of(m)), rss, sha(obj), warn, "adopted (rc inferred from log)"])
    return True


pending = {m for m in deps if not is_done(m)}
for _m in pending:      # (00:0xZ 10-20) a previous run's capped memory failure goes straight to the uncapped rerun
    _lg = LOGS / (_m + ".log")
    if _lg.exists() and MEMCAP_RE.search(_lg.read_text(errors="replace")):
        UNCAPPED.add(_m)
print(f"uncapped on resume: {sorted(UNCAPPED)}", flush=True)
BIG = max(strata, key=reservation) if strata else None   # drive_v11: cone has no strata certificates
big_hold_noted = [False, 0.0]
if not DRY:
    threading.Thread(target=watchdog, daemon=True).start()
if DRY:
    print("reservations (strata):", {m.split('SevenHigh')[-1]: round(reservation(m), 1) for m in sorted(strata)})
    print(f"MemAvailable {mem_avail_gb():.1f} GB, outstanding {outstanding():.1f} GB")
    rd = sorted((m for m in pending if all(d not in pending for d in deps[m]) and m not in adopted),
                key=lambda m: (m not in crit, m not in strata, -tail(m), m))
    print(f"pending {len(pending)}; ready {len(rd)}; first 25:")
    for m in rd[:25]:
        print(f"  {m}  crit={m in crit} tail={tail(m):.0f}")
    sys.stdout.flush()
    os._exit(0)
print(f"pending {len(pending)} of {len(deps)}", flush=True)
threads = {}
while (pending or running or adopted) and not (stop.is_set() and not running and not adopted):
    # retire finished threads FIRST (drive.py retired after launching, so a freed slot went to a long job before the
    # finished module's dependents became ready — the critical chain then waited for the next long job each step)
    for m, t in list(threads.items()):
        if not t.is_alive():
            threads.pop(m)
            if m in requeue:
                requeue.discard(m)      # watchdog victim: stays pending, runs again
            else:
                pending.discard(m)
    for m, (pid, st0) in list(adopted.items()):
        if not os.path.exists(f"/proc/{pid}"):
            adopted.pop(m)
            requeue.discard(m)          # an adopted watchdog victim is re-queued by judge_adopted's False
            if judge_adopted(m, st0):
                pending.discard(m)
    if stop.is_set() or time.time() < hold_until[0]:
        time.sleep(2)
        continue
    with lock:
        busy = set(running) | set(adopted)
    reserved = outstanding()
    ready = sorted((m for m in pending if all(d not in pending for d in deps[m]) and m not in threads
                    and m not in adopted),
                   key=lambda m: (m not in crit, m not in strata, -tail(m), m))
    launched = False
    hold_small = False   # a ready certificate module blocked on memory: drain, don't backfill
    # (17:5xZ fix) BIG = the largest certificate (t1_rep0, ~6-9 h here, the whole critical path). While it is ready but
    # cannot start, launch NOTHING new (drive2 v2 let the nine small certificates keep refilling memory, which would have
    # starved it for ~5 h). If none of our jobs is running and it still does not fit, fall back to normal scheduling
    # and say so (an external tenant is holding the memory; a human has to look).
    # (22:2xZ) the 17:5xZ HOLD-ALL-for-BIG block is gone: BIG now waits for everyone else (see the loop below)
    for m in ready:
        # (22:2xZ 10-19) BIG runs LAST and ALONE: under the 30000 MB Lean cap it was doomed (RSS 26.1 GiB at ~35% done,
        # +3.2 GiB/h; lean::check_memory throws at 30000<<20 bytes of current RSS), and uncapped it may need ~40+ GiB,
        # which this 62 GB box only has with nothing else of ours running (the authors used a 110 GiB container).
        if m == BIG:
            if busy or any(x != BIG for x in ready):
                continue
            if mem_avail_gb() < BIG_ALONE_GB:
                if not big_hold_noted[0]:
                    print(f"{time.strftime('%H:%M:%SZ', time.gmtime())} {BIG} ready but MemAvailable "
                          f"{mem_avail_gb():.1f} < {BIG_ALONE_GB} GB with nothing of ours running: waiting "
                          f"(external tenants hold the memory — look at ps)", flush=True)
                    big_hold_noted[0] = True
                continue
            print(f"{time.strftime('%H:%M:%SZ', time.gmtime())} {BIG} launching ALONE, uncapped "
                  f"(MemAvailable {mem_avail_gb():.1f} GB)", flush=True)
        # one extra slot for a critical-path (strata-closure) module, so the chain never queues behind long parts
        crit_running = sum(1 for x in busy if x in crit)
        if len(busy) >= WORKERS and not (m in crit and crit_running == 0 and len(busy) < WORKERS + 1):
            continue
        if m in strata and any(x in strata for x in busy) and reservation(m) + max(
                [reservation(x) for x in busy if x in strata]) > 26:
            continue          # never two big certificates at once
        if hold_small and m not in strata:
            continue
        if mem_avail_gb() - reserved < FLOOR_GB + reservation(m):
            if m in strata and reservation(m) > 5.0:   # only a BIG blocked certificate is worth draining for
                hold_small = True
            continue
        t = threading.Thread(target=run_one, args=(m,))
        threads[m] = t
        with lock:
            running[m] = None
        busy.add(m)
        reserved += reservation(m)
        t.start()
        launched = True
    time.sleep(1 if launched else 3)
for t in list(threads.values()):
    t.join()
status = "FAILED " + ",".join(failed) if failed else ("STOPPED" if stop.is_set() else "COMPLETE")
print("DRIVER", status, flush=True)
(OUT / "STATUS").write_text(status + "\n")
sys.exit(0 if status == "COMPLETE" else 3)
