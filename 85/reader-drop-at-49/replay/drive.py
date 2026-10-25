#!/usr/bin/env python3
"""Independent cold replay of the Erdős #85 order-49 capstone closure (lean-genius @ 2029149d7e42).

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

Usage: drive.py <proofs_dir> <out_dir> [workers]
"""
import hashlib, os, re, signal, subprocess, sys, threading, time
from pathlib import Path

PROOFS = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 else 5
TOOLBIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin"
ENDPOINTS = ["Proofs.Erdos85OrderFortyNineCapstoneH3", "Proofs.Erdos85FiniteDropCapstone"]
RUNTIME = "Proofs.Erdos85H3TripleCompletionRuntime"
INIT = "initialize_Proofs_Erdos85H3TripleCompletionRuntime"
FLOOR_GB, KILL_GB = 18, 9
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


def reservation(m):
    return 22 if m in strata else 2


def cap_mb(m):
    return 30000 if m in strata else 16000


running = {}          # module -> Popen
stop = threading.Event()
failed = []


def preexec():
    os.setsid()
    with open("/proc/self/oom_score_adj", "w") as f:
        f.write("1000")
    os.nice(19)


def run_one(m):
    src, obj = src_of(m), obj_of(m)
    obj.parent.mkdir(parents=True, exist_ok=True)
    if obj.exists():
        obj.unlink()        # never trust a leftover from a killed run
    cmd = ["/usr/bin/time", "-f", "MAXRSS_KB=%M", "lean", "-j1", f"--memory={cap_mb(m)}"]
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
        p = subprocess.Popen(cmd, cwd=PROOFS, env=ENV, stdout=lf, stderr=subprocess.STDOUT, preexec_fn=preexec)
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
    record([m, rc, el, sha(src_of(m)), rss, sha(obj) if rc == 0 else "-", warn, note])
    if rc != 0:
        failed.append(m)
        stop.set()
    return rc


def watchdog():
    while not stop.is_set() or running:
        a = mem_avail_gb()
        if a < KILL_GB:
            with lock:
                victims = list(running.items())
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
                print(f"WATCHDOG MemAvailable {a:.1f} GB < {KILL_GB}: killing {best[0]} (rss {best_rss} kB)", flush=True)
                os.killpg(best[1].pid, signal.SIGKILL)
                record([best[0], "WATCHDOG", "-", "-", best_rss, "-", "-", f"MemAvailable {a:.1f} GB"])
                stop.set()
        time.sleep(2)


threading.Thread(target=watchdog, daemon=True).start()
pending = {m for m in deps if not is_done(m)}
print(f"pending {len(pending)} of {len(deps)}", flush=True)
threads = {}
while (pending or running) and not (stop.is_set() and not running):
    if stop.is_set():
        time.sleep(2)
        continue
    with lock:
        busy = set(running)
        reserved = sum(reservation(x) for x in busy)
    ready = sorted((m for m in pending if all(d not in pending for d in deps[m]) and m not in threads),
                   key=lambda m: (m not in strata, m not in prio, m))
    launched = False
    hold_small = False   # a ready certificate module blocked on memory: drain, don't backfill
    for m in ready:
        if len(busy) >= WORKERS:
            break
        if m in strata and any(x in strata for x in busy):
            continue
        if hold_small and m not in strata:
            continue
        if mem_avail_gb() - reserved < FLOOR_GB + reservation(m):
            if m in strata:
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
    # retire finished threads
    for m, t in list(threads.items()):
        if not t.is_alive():
            threads.pop(m)
            pending.discard(m)
    time.sleep(1 if launched else 3)
for t in list(threads.values()):
    t.join()
status = "FAILED " + ",".join(failed) if failed else ("STOPPED" if stop.is_set() else "COMPLETE")
print("DRIVER", status, flush=True)
(OUT / "STATUS").write_text(status + "\n")
sys.exit(0 if status == "COMPLETE" else 3)
