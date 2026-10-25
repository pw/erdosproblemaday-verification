#!/usr/bin/env python3
"""H7 (t = 0) check for submission jhpvtq (#85), our assembly code, their receipts as the target.

  phase cubes : emit each of the 28 base cubes with the authors' EmitCube.lean (lean --run, interpreted,
                against OUR fresh build of its imports); require sha256 == inputs.json cube_cnf_sha256.
  phase covers: cover CNF = header + cube body + hsb + cover lines (hsb/cover from OUR compiled h7hsb,
                already hash-matched); require sha256 == receipt; solve with Kissat 4.0.4 (their H7 proofs
                came from CaDiCaL 3.0.1).
  phase leaves: leaf n CNF = header + cube body + hsb + one positive unit per literal of cover line n;
                require sha256 == receipt; solve.  Leaf set = every leaf of WHOLE_CUBE + RANDOM uniform leaves
                over all 377,776 (seed fixed).
Verdict-only solves (no proofs), nice 19, oom_score_adj 1000, PAR workers, CAP seconds each.
Usage: h7_check.py <workdir> <phase: cubes|covers|leaves> [PAR] [CAP]
"""
import hashlib, json, os, random, subprocess, sys, threading, time
from pathlib import Path

W = Path(sys.argv[1]).resolve(); PHASE = sys.argv[2]
PAR = int(sys.argv[3]) if len(sys.argv) > 3 else 3
CAP = int(sys.argv[4]) if len(sys.argv) > 4 else 7200
PROOFS = Path("/tmp/erdos85-1019/repo/proofs")
FRESH = Path("/tmp/erdos85-1019/build/lean")
GEN = Path("/tmp/erdos85-1019/h7gen")           # <cube>.hsb / <cube>.cover from our h7hsb
TOOLBIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.31.0/bin"
KISSAT = str(Path.home() / "MathDyad/tools/kissat/build/kissat")
REC = Path.home() / "MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01/h7_hsb_campaign_20261008/receipts/collected"
INPUTS = json.loads(Path("/tmp/erdos85-1019/h7tools/inputs.json").read_text())
VARS, CUBE_CLAUSES = 17633, 720825
WHOLE_CUBE, RANDOM, SEED = "cube_F6_t14", 200, 20261019
libs = [str(FRESH)] + sorted(str(p) for p in (PROOFS / ".lake/packages").glob("*/.lake/build/lib/lean"))
ENV = {"PATH": f"{TOOLBIN}:/usr/bin:/bin", "HOME": str(W / "home"), "LANG": "C.UTF-8", "LEAN_PATH": os.pathsep.join(libs)}
W.mkdir(parents=True, exist_ok=True); (W / "home").mkdir(exist_ok=True)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def nice():
    os.nice(19)
    with open("/proc/self/oom_score_adj", "w") as f:
        f.write("1000")


def body_of(cube):
    raw = (W / f"{cube}.cube.cnf").read_bytes()
    head, rest = raw.split(b"\n", 1)
    assert head == f"p cnf {VARS} {CUBE_CLAUSES}".encode(), head
    return rest


def solve(path):
    t0 = time.time()
    p = subprocess.run(["timeout", str(CAP), KISSAT, "-q", "-n", str(path)], capture_output=True, text=True, preexec_fn=nice)
    v = "UNSAT" if "s UNSATISFIABLE" in p.stdout else ("SAT" if "s SATISFIABLE" in p.stdout else "UNKNOWN")
    return v, round(time.time() - t0, 2)


if PHASE == "cubes":
    emit = Path("/tmp/erdos85-1019/h7tools/EmitCube.lean")
    names = list(INPUTS["cubes"])
    args = []
    for cube in names:
        args += [str(INPUTS["cubes"][cube]["edge_count"]), cube.split("_t")[1]]
    allf = W / "all_cubes.cnf"
    with open(allf, "wb") as o:
        rc = subprocess.run(["lean", "--run", str(emit)] + args, cwd=PROOFS, env=ENV, stdout=o,
                            stderr=open(W / "emitcube.err", "w"), preexec_fn=nice).returncode
    assert rc == 0, rc
    data = allf.read_bytes()
    hdr = f"p cnf {VARS} {CUBE_CLAUSES}\n".encode()
    chunks = data.split(hdr)
    # `lean --run` prints the emitter file's compile-time messages to STDOUT before the first header; keep them
    # aside, and require that they contain no DIMACS clause line.
    (W / "emitcube.prefix.txt").write_bytes(chunks[0])
    assert not any(l.strip().endswith(b" 0") and l.strip()[:1] in b"-0123456789" for l in chunks[0].splitlines()), "prefix looks like DIMACS"
    assert len(chunks) == len(names) + 1, (len(chunks), len(names))
    out = {}
    for cube, body in zip(names, chunks[1:]):
        (W / f"{cube}.cube.cnf").write_bytes(hdr + body)
        ok = sha_b(hdr + body) == INPUTS["cubes"][cube]["cube_cnf_sha256"]
        out[cube] = ok
        print(cube, "cube sha256", "MATCH" if ok else "MISMATCH", flush=True)
    allf.unlink()
    print("cubes matched", sum(out.values()), "of", len(out))
    sys.exit(0 if all(out.values()) else 1)

receipts = {}
for f in REC.glob("cube_*.receipts.tsv.zst"):
    txt = subprocess.run(["zstd", "-dc", str(f)], capture_output=True, text=True).stdout
    for line in txt.splitlines()[1:]:
        c = line.split("\t")
        receipts[(c[0], c[1])] = c[2]
RES = W / f"{PHASE}.tsv"
if not RES.exists():
    RES.write_text("cube\tleaf\tsha_match\tverdict\tseconds\n")
done = {tuple(l.split("\t")[:2]) for l in RES.read_text().splitlines()[1:] if l.split("\t")[3] in ("UNSAT", "SAT")}
lock = threading.Lock()
cache = {}


def parts(cube):
    if cube not in cache:
        cache[cube] = (body_of(cube), (GEN / f"{cube}.hsb").read_bytes(), (GEN / f"{cube}.cover").read_bytes())
    return cache[cube]


def job(cube, leaf):
    body, hsb, cover = parts(cube)
    nh = hsb.count(b"\n")
    if leaf == "cover":
        data = f"p cnf {VARS} {CUBE_CLAUSES + nh + cover.count(b'\n')}\n".encode() + body + hsb + cover
    else:
        line = cover.splitlines()[int(leaf)].split()
        assert line[-1] == b"0" and all(int(x) < 0 for x in line[:-1])
        units = [str(-int(x)) for x in line[:-1]]
        data = f"p cnf {VARS} {CUBE_CLAUSES + nh + len(units)}\n".encode() + body + hsb + "".join(f"{u} 0\n" for u in units).encode()
    s = sha_b(data)
    match = s == receipts.get((cube, leaf))
    if not match:
        with lock, open(RES, "a") as f:
            f.write(f"{cube}\t{leaf}\tMISMATCH\t-\t-\n")
        return
    p = W / "tmp" / f"{cube}.{leaf}.cnf"
    p.parent.mkdir(exist_ok=True)
    p.write_bytes(data)
    v, el = solve(p)
    p.unlink()
    with lock, open(RES, "a") as f:
        f.write(f"{cube}\t{leaf}\tMATCH\t{v}\t{el}\n")


if PHASE == "covers":
    todo = [(c, "cover") for c in INPUTS["cubes"]]
else:
    todo = [(WHOLE_CUBE, str(i)) for i in range(INPUTS["cubes"][WHOLE_CUBE]["leaves"])]
    allleaves = [(c, str(i)) for c, m in sorted(INPUTS["cubes"].items()) for i in range(m["leaves"])]
    assert len(allleaves) == 377776, len(allleaves)
    todo += [x for x in random.Random(SEED).sample(allleaves, RANDOM) if x[0] != WHOLE_CUBE]
todo = [x for x in todo if x not in done]
print(PHASE, "todo", len(todo), flush=True)
it = iter(todo); itl = threading.Lock()


def worker():
    while True:
        with itl:
            x = next(it, None)
        if x is None:
            return
        job(*x)


ths = [threading.Thread(target=worker) for _ in range(PAR)]
[t.start() for t in ths]; [t.join() for t in ths]
print("DONE", PHASE, flush=True)
