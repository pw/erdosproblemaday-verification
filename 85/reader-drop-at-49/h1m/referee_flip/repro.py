#!/usr/bin/env python3
"""Re-run whole DRAT-pass cells from scratch (referee_flip, 2026-10-28): emit with the campaign flags, CaDiCaL binary
DRAT, drat-trim; compare CNF sha256[:16], proof BYTE COUNT (CaDiCaL is deterministic on identical input, so an equal
size means the logged run is the same computation) and verdict to campaign_drat.tsv. Cells drawn with a seed of mine,
restricted to logged wall < maxwall s to bound cost. Usage: repro.py n seed maxwall"""
import hashlib, os, random, subprocess, sys, tempfile, shutil
H = os.path.expanduser("~/MathDyad/erdos85/h1m")
DT = os.path.expanduser("~/.local/bin/drat-trim"); PY = os.path.expanduser("~/.venv/bin/python")
FLAGS = ["--pairsb", "--slots", "--ph", "--edgeswap"]
n, seed, maxwall = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(H, "runs/campaign_drat.tsv"))]
pool = [r for r in rows if float(r[6]) < maxwall]
pick = random.Random(seed).sample(pool, n)
def run(cmd):
    return subprocess.run(["bash", "-c", 'ulimit -v 4000000; exec nice -n 19 "$@"', "x"] + cmd,
                          capture_output=True, text=True, timeout=3600).stdout
def first_s(out):
    for l in out.replace("\r", "").splitlines():
        if l.startswith("s "): return l.strip()
    return "none"
bad = 0
for r in pick:
    td = tempfile.mkdtemp(prefix="repro-", dir="/tmp"); cnf, pf = os.path.join(td, "c.cnf"), os.path.join(td, "p.drat")
    run([PY, os.path.join(H, "h1mcell.py"), "7", r[0], "1", "kissat"] + FLAGS + ["--M", r[1], "--emit", cnf])
    h = hashlib.sha256(open(cnf, "rb").read()).hexdigest()[:16]
    s1 = first_s(run(["cadical", "-q", "--binary=true", cnf, pf])); sz = os.path.getsize(pf)
    v = first_s(run([DT, cnf, pf, "-t", "10800"]))
    ok = (h == r[4] and str(sz) == r[5] and s1 == "s UNSATISFIABLE" and v == "s VERIFIED")
    bad += not ok
    print(("OK  " if ok else "BAD ") + f"j={r[0]} M={r[1]} hash {h} vs {r[4]} | proof {sz} vs {r[5]} | {s1} / {v}", flush=True)
    shutil.rmtree(td)
print(f"RESULT: {n - bad}/{n} cells reproduce hash, proof size and VERIFIED")
