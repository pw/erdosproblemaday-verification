#!/usr/bin/env python3
"""#85 H1 campaign: checks for the VERIFIED flip (2026-10-28 09Z erdos seat).

Independent of tally.py and campaign.sh's done-test. Four parts, each prints PASS/FAIL; exit 0 only if all pass.
  A  tally by a different route: key sets compared as sets (not counted), both modes; distinct CNF hashes; no
     VERIFIED row with an empty proof; the drat key set == the kissat key set == classes_all.tsv.
  B  re-emit a seeded random sample of cells with the campaign's exact flags (campaign.sh FLAGS) and require the
     16-hex CNF hash recorded by the DRAT pass: the formulas drat-trim checked are the ones h1mcell.py emits.
  C  drat-trim negative controls, same binary, same invocation shape as campaign.sh (binary DRAT from CaDiCaL):
     C1 positive: fresh CNF + proof -> 's VERIFIED'
     C2 the same proof against the --drop-c4 formula of the same cell (satisfiable; shown SAT by Kissat here)
        -> must NOT print 's VERIFIED'  (no refutation of a satisfiable formula can be valid)
     C3 text proof with the last 25% of its lines removed -> must NOT verify
     C4 proof consisting only of the empty clause, against the real (UNSAT) CNF -> must NOT verify
     C5 the lrat-check trap shape in DRAT mode: formula '1 2 0', proof '0' -> must NOT verify
     C6 a tiny timeout (-t 1) on a large proof -> must NOT print 's VERIFIED' (the campaign takes the first '^s ' line)
Usage: flipcheck.py [sample_size] [seed]
"""
import hashlib, os, random, re, subprocess, sys, tempfile
H = os.path.expanduser("~/MathDyad/erdos85/h1m"); os.chdir(H)
DT = os.path.expanduser("~/.local/bin/drat-trim")
PY = os.path.expanduser("~/.venv/bin/python")
FLAGS = ["--pairsb", "--slots", "--ph", "--edgeswap"]          # = campaign.sh FLAGS
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261028
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""), flush=True)
    if not ok: fails.append(name)
def capped(cmd, timeout=None):
    return subprocess.run(["bash", "-c", 'ulimit -v 4000000; exec "$@"', "x"] + cmd,
                          capture_output=True, text=True, timeout=timeout)
def first_s(out):
    for l in out.replace("\r", "").splitlines():
        if l.startswith("s "): return l.strip()
    return "none"

# ---------- A
classes = set()
for l in open("classes_all.tsv"):
    f = l.rstrip("\n").split("\t")
    if len(f) >= 2 and f[0] != "": classes.add((f[0], f[1]))
drat_done, kis_done, hashes, empty_proof = {}, set(), {}, 0
for l in open("runs/campaign_drat.tsv"):
    f = l.rstrip("\n").split("\t")
    if len(f) == 7 and f[2] == "s UNSATISFIABLE" and f[3] == "s VERIFIED":
        drat_done[(f[0], f[1])] = f[4]
        if int(f[5]) <= 0: empty_proof += 1
for l in open("runs/campaign_kissat.tsv"):
    f = l.rstrip("\n").split("\t")
    if len(f) == 4 and f[2] == "UNSAT": kis_done.add((f[0], f[1]))
check("A1 classes_all has 13,351 distinct keys", len(classes) == 13351, str(len(classes)))
check("A2 DRAT-verified key set == classes", set(drat_done) == classes,
      f"{len(set(drat_done) & classes)} common, {len(classes - set(drat_done))} missing, {len(set(drat_done) - classes)} stray")
check("A3 Kissat-UNSAT key set == classes", kis_done == classes,
      f"{len(kis_done & classes)} common, {len(classes - kis_done)} missing, {len(kis_done - classes)} stray")
check("A4 distinct CNF hashes among DRAT-verified cells", len(set(drat_done.values())) == len(drat_done),
      f"{len(set(drat_done.values()))} distinct of {len(drat_done)}")
check("A5 no VERIFIED row with an empty proof file", empty_proof == 0, str(empty_proof))
sat_rows = [l for f in ("runs/campaign_drat.tsv", "runs/campaign_kissat.tsv") for l in open(f)
            if re.search(r"\t(s )?SAT", l)]
check("A6 no SAT row in either pass", not sat_rows and not os.path.exists("runs/ALARM_SAT"), str(len(sat_rows)))

# ---------- B
rng = random.Random(SEED); sample = rng.sample(sorted(drat_done), N)
bad = []
with tempfile.TemporaryDirectory(dir="/tmp") as td:
    for j, M in sample:
        cnf = os.path.join(td, "c.cnf")
        capped(["nice", "-n", "19", PY, "h1mcell.py", "7", j, "1", "kissat"] + FLAGS + ["--M", M, "--emit", cnf])
        h = hashlib.sha256(open(cnf, "rb").read()).hexdigest()[:16]
        if h != drat_done[(j, M)]: bad.append((j, M, h, drat_done[(j, M)]))
        os.remove(cnf)
check(f"B  {N} re-emitted cells (seed {SEED}) hash-equal the DRAT pass's CNFs", not bad, f"{N - len(bad)}/{N}" + (f" {bad[:3]}" if bad else ""))

# ---------- C
j, M = sorted(drat_done)[0]
td = tempfile.mkdtemp(dir="/tmp", prefix="flipc-")
cnf, cnf_d, pf, pft = (os.path.join(td, x) for x in ("c.cnf", "dropc4.cnf", "p.drat", "p.txt"))
capped(["nice", "-n", "19", PY, "h1mcell.py", "7", j, "1", "kissat"] + FLAGS + ["--M", M, "--emit", cnf])
capped(["nice", "-n", "19", PY, "h1mcell.py", "7", j, "1", "kissat"] + FLAGS + ["--drop-c4", "--M", M, "--emit", cnf_d])
r = capped(["nice", "-n", "19", "cadical", "-q", "--binary=true", cnf, pf]); s1 = first_s(r.stdout)
v1 = first_s(capped(["nice", "-n", "19", DT, cnf, pf, "-t", "3600"]).stdout)
check("C1 positive: cadical UNSAT + drat-trim VERIFIED on a fresh cell", s1 == "s UNSATISFIABLE" and v1 == "s VERIFIED", f"{j} {s1} / {v1}")
KIS = os.path.expanduser("~/MathDyad/tools/kissat/build/kissat")   # = h1mcell.py BIN; NOT on PATH (first run: "kissat none")
sd = first_s(capped(["nice", "-n", "19", KIS, "-q", cnf_d]).stdout)
v2 = first_s(capped(["nice", "-n", "19", DT, cnf_d, pf, "-t", "3600"]).stdout)
check("C2 same proof vs the satisfiable drop-C4 formula is rejected", sd == "s SATISFIABLE" and v2 != "s VERIFIED", f"kissat {sd} / drat-trim {v2}")
capped(["nice", "-n", "19", "cadical", "-q", "--binary=false", cnf, pft])
lines = open(pft).read().splitlines(); cut = os.path.join(td, "cut.txt")
open(cut, "w").write("\n".join(lines[: int(len(lines) * 0.75)]) + "\n")
v0 = first_s(capped(["nice", "-n", "19", DT, cnf, pft, "-t", "3600"]).stdout)
v3 = first_s(capped(["nice", "-n", "19", DT, cnf, cut, "-t", "3600"]).stdout)
check("C3 text proof verifies whole, rejected with its last 25% removed", v0 == "s VERIFIED" and v3 != "s VERIFIED", f"whole {v0} / cut {v3} ({len(lines)} lines)")
e = os.path.join(td, "empty.txt"); open(e, "w").write("0\n")
v4 = first_s(capped(["nice", "-n", "19", DT, cnf, e, "-t", "600"]).stdout)
check("C4 empty-clause-only proof vs the real CNF is rejected", v4 != "s VERIFIED", v4)
t5c, t5p = os.path.join(td, "t.cnf"), os.path.join(td, "t.txt")
open(t5c, "w").write("p cnf 2 1\n1 2 0\n"); open(t5p, "w").write("0\n")
v5 = first_s(capped([DT, t5c, t5p]).stdout)
check("C5 SAT formula '1 2 0' + proof '0' is rejected in DRAT mode", v5 != "s VERIFIED", v5)
# C6: the largest proof among a few mid-size cells, checked with -t 1
rows = [l.rstrip("\n").split("\t") for l in open("runs/campaign_drat.tsv")]
rows = [f for f in rows if len(f) == 7 and f[3] == "s VERIFIED"]
mid = sorted(rows, key=lambda f: int(f[5]))[len(rows) * 9 // 10]      # 90th-percentile proof size
cnf6, pf6 = os.path.join(td, "c6.cnf"), os.path.join(td, "p6.drat")
capped(["nice", "-n", "19", PY, "h1mcell.py", "7", mid[0], "1", "kissat"] + FLAGS + ["--M", mid[1], "--emit", cnf6])
capped(["nice", "-n", "19", "timeout", "3600", "cadical", "-q", "--binary=true", cnf6, pf6])
out6 = capped(["nice", "-n", "19", DT, cnf6, pf6, "-t", "1"]).stdout
v6 = first_s(out6)
check("C6 -t 1 on a 90th-percentile proof does not print 's VERIFIED'", v6 != "s VERIFIED",
      f"{v6!r}; proof {os.path.getsize(pf6)} bytes; tail: {out6.strip().splitlines()[-1] if out6.strip() else ''}")
for p in (cnf, cnf_d, pf, pft, cut, e, t5c, t5p, cnf6, pf6):
    try: os.remove(p)
    except FileNotFoundError: pass
os.rmdir(td)
print("RESULT:", "ALL PASS" if not fails else "FAILED " + ", ".join(fails))
sys.exit(0 if not fails else 1)
