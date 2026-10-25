import sys, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from own_block_enc import encode
from pysat.solvers import Solver
for E, lab in (([1]*6, "e=1 fixed canonical matching"), (None, "internal edges FREE (no case fixing)")):
    cl, vid, fx, N, blk = encode(4, 3, E=E, c4=True)
    t = time.time()
    with Solver(name="cadical153", bootstrap_with=cl) as S:
        S.conf_budget(3_000_000)
        r = S.solve_limited()
    print(f"referee encoder k=5, {lab}, C4 on, no SB, no Lemma D: {r} ({time.time()-t:.1f}s, {len(cl)} clauses)", flush=True)
