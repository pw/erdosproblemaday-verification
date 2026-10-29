#!/usr/bin/env python3
"""drat-trim negative controls NOT in flipcheck.py (referee_flip, 2026-10-28). Same binary, same invocation shape as
campaign.sh (`drat-trim CNF PROOF -t N`, first '^s ' line). Each control has a positive twin that must verify.
  N1  synthetic: SAT formula (1 2)(-1 2); proof '-2 0' (neither RUP nor RAT on its first literal) then '0'.
      Twin: UNSAT formula (1 2)(-1 2)(1 -2)(-1 -2); proof '1 0' (RUP) then '0'.  Text AND binary encodings.
  N2  real cell, CaDiCaL binary proof re-written with its ADDITION lemmas in REVERSE order (deletions dropped, the
      final empty clause kept last). Twin: the same additions in ORIGINAL order, deletions dropped.
  N3  the real proof of cell A checked against the (also UNSAT) CNF of cell B. Twin: A's proof vs A's CNF.
  N4  (informative) A's CNF with its header clause count cut to 60%: drat-trim then parses only the first 60% of the
      clauses (the rest of the file is NOT read as formula); a VERIFIED here would only mean that prefix is UNSAT.
Usage: drat_negctl.py jA MA jB MB"""
import os, subprocess, sys, tempfile, shutil
H = os.path.expanduser("~/MathDyad/erdos85/h1m")
DT = os.path.expanduser("~/.local/bin/drat-trim"); PY = os.path.expanduser("~/.venv/bin/python")
FLAGS = ["--pairsb", "--slots", "--ph", "--edgeswap"]
jA, MA, jB, MB = sys.argv[1:5]
td = tempfile.mkdtemp(prefix="dneg-", dir="/tmp")
res = []
def run(cmd, timeout=1800):
    return subprocess.run(["bash", "-c", 'ulimit -v 4000000; exec nice -n 19 "$@"', "x"] + cmd,
                          capture_output=True, text=True, timeout=timeout).stdout
def first_s(out):
    for l in out.replace("\r", "").splitlines():
        if l.startswith("s "): return l.strip()
    return "none"
def dt(cnf, pf, t=3600):
    out = run([DT, cnf, pf, "-t", str(t)])
    return first_s(out), out
def check(name, got, want_verified):
    ok = (got == "s VERIFIED") == want_verified
    res.append(ok)
    print(("PASS " if ok else "FAIL ") + f"{name}: {got} (want {'VERIFIED' if want_verified else 'not VERIFIED'})", flush=True)

# ---- N1
def write_bin(path, lemmas):            # lemmas: list of (kind 'a'/'d', [lits])
    with open(path, "wb") as f:
        for kind, lits in lemmas:
            f.write(kind.encode())
            for l in lits + [0]:
                u = 2 * l if l > 0 else (-2 * l + 1) if l < 0 else 0
                while True:
                    b = u & 127; u >>= 7
                    if u: f.write(bytes([b | 128]))
                    else: f.write(bytes([b])); break
sat = os.path.join(td, "sat.cnf"); open(sat, "w").write("p cnf 2 2\n1 2 0\n-1 2 0\n")
uns = os.path.join(td, "uns.cnf"); open(uns, "w").write("p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n")
bad_t = os.path.join(td, "bad.txt"); open(bad_t, "w").write("-2 0\n0\n")
good_t = os.path.join(td, "good.txt"); open(good_t, "w").write("1 0\n0\n")
bad_b = os.path.join(td, "bad.drat"); write_bin(bad_b, [("a", [-2]), ("a", [])])
good_b = os.path.join(td, "good.drat"); write_bin(good_b, [("a", [1]), ("a", [])])
check("N1 twin text  (valid RUP lemma, UNSAT formula)", dt(uns, good_t)[0], True)
check("N1 twin bin   (valid RUP lemma, UNSAT formula)", dt(uns, good_b)[0], True)
check("N1 text: invalid lemma '-2' (not RUP, not RAT on -2) on SAT formula", dt(sat, bad_t)[0], False)
check("N1 bin : invalid lemma '-2' (not RUP, not RAT on -2) on SAT formula", dt(sat, bad_b)[0], False)

# ---- real cells
def emit(j, M, path):
    run([PY, os.path.join(H, "h1mcell.py"), "7", j, "1", "kissat"] + FLAGS + ["--M", M, "--emit", path])
    assert os.path.exists(path)
cA, cB, pA = (os.path.join(td, n) for n in ("A.cnf", "B.cnf", "A.drat"))
emit(jA, MA, cA); emit(jB, MB, cB)
print("cadical A:", first_s(run(["cadical", "-q", "--binary=true", cA, pA])), os.path.getsize(pA), "bytes", flush=True)
def read_bin(path):
    data = open(path, "rb").read(); i = 0; out = []
    while i < len(data):
        kind = chr(data[i]); i += 1; assert kind in "ad", (kind, i)
        lits = []
        while True:
            u = 0; sh = 0
            while True:
                b = data[i]; i += 1; u |= (b & 127) << sh; sh += 7
                if b < 128: break
            if u == 0: break
            lits.append(u >> 1 if u % 2 == 0 else -(u >> 1))
        out.append((kind, lits))
    return out
recs = read_bin(pA)
adds = [r for r in recs if r[0] == "a"]
print(f"proof A: {len(recs)} records, {len(adds)} additions, last record {recs[-1]}", flush=True)
assert adds[-1] == ("a", []), "proof does not end with the empty clause"
body = adds[:-1]
fwd, rev = os.path.join(td, "fwd.drat"), os.path.join(td, "rev.drat")
write_bin(fwd, body + [("a", [])]); write_bin(rev, body[::-1] + [("a", [])])
check("N2 twin: additions in original order (deletions dropped)", dt(cA, fwd)[0], True)
check("N2: same additions in REVERSED order", dt(cA, rev)[0], False)
check("N3 twin: proof A vs CNF A", dt(cA, pA)[0], True)
check("N3: proof A vs CNF B (a different UNSAT cell)", dt(cB, pA)[0], False)
lines = open(cA).read().splitlines()
hdr = lines[0].split(); assert hdr[:2] == ["p", "cnf"]
nc = int(hdr[3]); cut = os.path.join(td, "cut.cnf")
open(cut, "w").write(f"p cnf {hdr[2]} {int(nc * 0.6)}\n" + "\n".join(lines[1:]) + "\n")
v4, o4 = dt(cut, pA)
print(f"INFO N4 header count cut to 60% ({int(nc*0.6)} of {nc}): {v4}; drat-trim says: "
      + "; ".join(l.strip() for l in o4.replace('\r', '').splitlines() if 'parsing input' in l or 'WARNING' in l)[:300], flush=True)
shutil.rmtree(td)
print("RESULT:", "ALL PASS" if all(res) else f"{res.count(False)} FAILED")
