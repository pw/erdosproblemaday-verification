#!/usr/bin/env python3
"""Run every partial cube (slots 0 and k-1) for the #792 n=15 patterns k in KS with a worker pool; resume-safe.
Each cube runs in its own process (z3 is single-threaded, nice 19). Results append to cube_campaign.log as
CUBE lines (same format as cube792.py); on restart, cubes already logged are skipped. Any SAT cube is re-checked
exactly by cube792 and printed as a WITNESS line; a 'unknown' (timeout) cube is logged and retried at the end with
a longer cap. Final SUMMARY line per k: unsat/sat/unknown counts vs the cube count."""
import sys, os, subprocess, itertools, time, argparse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cube792

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "cube_campaign.log")

def done_cubes():
    out = {}
    if not os.path.exists(LOG): return out
    for line in open(LOG):
        m = re.match(r"CUBE n=(\d+) k=(\d+) t=(\d+) cube=(\S+) atoms=\d+ status=(\w+)", line)
        if m: out[(int(m.group(2)), m.group(4))] = m.group(5)
    return out

def run_cube(n, k, t, cube_str, timeout_ms):
    cmd = ["nice", "-n", "19", os.path.expanduser("~/.venv/bin/python"), os.path.join(HERE, "cube792.py"), str(k),
           "--n", str(n), "--t", str(t), "--cube", cube_str, "--timeout-ms", str(timeout_ms)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    line = [l for l in p.stdout.splitlines() if l.startswith("CUBE")]
    return line[0] if line else f"CUBE n={n} k={k} t={t} cube={cube_str} atoms=0 status=error rc={p.returncode} {p.stderr.strip()[-200:]}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=15); ap.add_argument("--t", type=int, default=7)
    ap.add_argument("--ks", type=str, default="4,5,6,7"); ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout-ms", type=int, default=7200000); ap.add_argument("--retry-timeout-ms", type=int, default=28800000)
    a = ap.parse_args()
    ks = [int(v) for v in a.ks.split(",")]
    todo = []
    done = done_cubes()
    for k in ks:
        for cb in cube792.partial_cubes(a.n, k, [0, k - 1]):
            cs = ",".join("_" if v is None else str(v) for v in cb)
            if done.get((k, cs)) in ("unsat", "sat"): continue
            todo.append((k, cs))
    print(f"campaign: {len(todo)} cubes to run ({len(done)} already logged), workers={a.workers}", flush=True)
    with open(LOG, "a") as log, ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_cube, a.n, k, a.t, cs, a.timeout_ms): (k, cs) for (k, cs) in todo}
        for f in as_completed(futs):
            line = f.result(); print(line, flush=True); log.write(line + "\n"); log.flush()
    # retry unknowns with the long cap, one at a time per worker
    done = done_cubes()
    retry = [(k, cs) for (k, cs), st in done.items() if st not in ("unsat", "sat") and k in ks]
    if retry:
        print(f"retrying {len(retry)} unknown/error cubes at {a.retry_timeout_ms} ms", flush=True)
        with open(LOG, "a") as log, ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = {ex.submit(run_cube, a.n, k, a.t, cs, a.retry_timeout_ms): (k, cs) for (k, cs) in retry}
            for f in as_completed(futs):
                line = f.result(); print(line, flush=True); log.write(line + "\n"); log.flush()
    done = done_cubes()
    with open(LOG, "a") as log:
        for k in ks:
            total = len(cube792.partial_cubes(a.n, k, [0, k - 1]))
            st = [done.get((k, ",".join("_" if v is None else str(v) for v in cb))) for cb in cube792.partial_cubes(a.n, k, [0, k - 1])]
            s = f"SUMMARY n={a.n} k={k} t={a.t} cubes={total} unsat={st.count('unsat')} sat={st.count('sat')} other={total - st.count('unsat') - st.count('sat')} at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"
            print(s, flush=True); log.write(s + "\n")

if __name__ == "__main__":
    main()
