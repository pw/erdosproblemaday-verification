#!/usr/bin/env python3
"""H1 sample check for submission jhpvtq (#85): for each sampled orbit
  1. emit its CNF with the authors' Lean emitter (Proofs/Erdos85OneHighV2CnfEmit.lean, run interpreted
     with `lean --run` against OUR fresh build of its imports) and require sha256 == their receipt;
  2. solve it with the solver family that did NOT produce that orbit's certificate
     (bank + historical: produced by Kissat 4.0.4 -> we use CaDiCaL 1.7.3; census: produced by
     CaDiCaL 3.0.1 -> we use Kissat 4.0.4); verdict only, no proof (proofs run to tens of GB).
Detached, nice 19, at most PAR solver processes, each capped at CAP seconds. Results appended to
results.tsv; a solver that prints neither s SATISFIABLE nor s UNSATISFIABLE is recorded as UNKNOWN.
Usage: h1_sample_solve.py <sample_dir> [PAR] [CAP]
"""
import hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path

D = Path(sys.argv[1]).resolve()
PAR = int(sys.argv[2]) if len(sys.argv) > 2 else 3
CAP = int(sys.argv[3]) if len(sys.argv) > 3 else 14400
PROOFS = Path("/tmp/erdos85-1019/repo/proofs")
FRESH = Path("/tmp/erdos85-1019/build/lean")
TOOLBIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin"
KISSAT = Path.home() / "MathDyad/tools/kissat/build/kissat"
CADICAL = "/usr/bin/cadical"
libs = [str(FRESH)] + sorted(str(p) for p in (PROOFS / ".lake/packages").glob("*/.lake/build/lib/lean"))
ENV = {"PATH": f"{TOOLBIN}:/usr/bin:/bin", "HOME": str(D / "home"), "LANG": "C.UTF-8", "LEAN_PATH": os.pathsep.join(libs)}
(D / "home").mkdir(exist_ok=True)
S = json.loads((D / "sample.json").read_text())
RES = D / "results.tsv"
if not RES.exists():
    RES.write_text("tag\tset\tprofile\tcnf_sha256_ours\tcnf_match\tsolver\tverdict\tseconds\tnote\n")
lock = threading.Lock()
sem = threading.Semaphore(PAR)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nice():
    os.nice(19)
    with open("/proc/self/oom_score_adj", "w") as f:
        f.write("1000")


def one(r):
    t = r["tag"]
    cnf = D / f"{t}.cnf"
    tbl = D / f"{t}.table.json"
    with sem:
        if not cnf.exists() or sha(cnf) != r["cnf_sha256"]:
            with open(cnf, "wb") as out, open(D / f"{t}.emit.log", "w") as log:
                rc = subprocess.run(["lean", "--run", "Proofs/Erdos85OneHighV2CnfEmit.lean", "emit", str(r["profile"]), str(tbl)],
                                    cwd=PROOFS, env=ENV, stdout=out, stderr=log, preexec_fn=nice).returncode
            if rc != 0:
                with lock, open(RES, "a") as f:
                    f.write(f"{t}\t{r['set']}\t{r['profile']}\t-\tEMIT_FAIL\t-\t-\t-\trc={rc}\n")
                return
            # `lean --run` elaborates the emitter file first and prints its compile-time messages (two deprecation
            # warnings + a note, 340 bytes) to STDOUT ahead of the DIMACS. Strip everything before the header line;
            # the stripped prefix must contain no DIMACS-looking line.
            raw = cnf.read_bytes()
            i = raw.index(b"p cnf ")
            assert i == 0 or raw[i - 1:i] == b"\n"
            (D / f"{t}.prefix.txt").write_bytes(raw[:i])
            cnf.write_bytes(raw[i:])
        ours = sha(cnf)
        match = ours == r["cnf_sha256"]
        if not match:
            with lock, open(RES, "a") as f:
                f.write(f"{t}\t{r['set']}\t{r['profile']}\t{ours}\tMISMATCH\t-\t-\t-\treceipt {r['cnf_sha256']}\n")
            return
        if r["set"] == "census":
            name, cmd = "kissat-4.0.4", [str(KISSAT), "-q", "-n", str(cnf)]
        else:
            name, cmd = "cadical-1.7.3", [CADICAL, "-q", "-n", str(cnf)]
        t0 = time.time()
        try:
            p = subprocess.run(["timeout", str(CAP)] + cmd, capture_output=True, text=True, preexec_fn=nice)
            out = p.stdout
        except Exception as e:
            out = f"exception {e}"
        el = round(time.time() - t0, 1)
        v = "UNSAT" if "s UNSATISFIABLE" in out else ("SAT" if "s SATISFIABLE" in out else "UNKNOWN")
        (D / f"{t}.solve.log").write_text(out[-5000:])
        with lock, open(RES, "a") as f:
            f.write(f"{t}\t{r['set']}\t{r['profile']}\t{ours}\tMATCH\t{name}\t{v}\t{el}\t\n")
        cnf.unlink()   # 13 MB each; re-emittable


done = set()
for line in RES.read_text().splitlines()[1:]:
    f = line.split("\t")
    if f[6] in ("UNSAT", "SAT") or f[4] == "MISMATCH":
        done.add(f[0])
ths = [threading.Thread(target=one, args=(r,)) for r in S["rows"] if r["tag"] not in done]
for th in ths:
    th.start()
for th in ths:
    th.join()
print("DONE", flush=True)
