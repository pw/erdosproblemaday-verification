# Check (3.41): 1_{distinct performed values} = sum_pi mu(pi) 1_{C_pi}, over collections pi of disjoint blocks
# (size>=2) of POTENTIAL addresses; C_pi = all addresses in pi performed and equal within blocks.
# Also check (3.42): sum_{r(pi)=r} |mu(pi)| = e_r(0,1,...,A-1) <= A^{2r}.
import itertools, random
from math import factorial, prod
def collections(addrs):
    """all collections of disjoint blocks of size >= 2 from addrs"""
    addrs = list(addrs)
    if not addrs:
        yield []; return
    a, rest = addrs[0], addrs[1:]
    yield from collections(rest)                       # a in no block
    for k in range(1, len(rest) + 1):                  # a in a block with k others
        for others in itertools.combinations(rest, k):
            rem = [x for x in rest if x not in others]
            for c in collections(rem):
                yield [(a,) + others] + c
def mu(pi): return prod((-1) ** (len(B) - 1) * factorial(len(B) - 1) for B in pi)
def r(pi): return sum(len(B) - 1 for B in pi)
rnd = random.Random(7); bad = 0; trials = 0
for A in range(1, 8):
    cols = list(collections(range(A)))
    for _ in range(60):
        performed = {a for a in range(A) if rnd.random() < 0.8}
        val = {a: rnd.randint(1, 3) for a in performed}
        lhs = 1 if len(set(val.values())) == len(val) else 0
        rhs = sum(mu(pi) for pi in cols
                  if all(a in performed for B in pi for a in B) and all(len({val[a] for a in B}) == 1 for B in pi))
        trials += 1; bad += (lhs != rhs)
    # (3.42)
    for rr in range(0, A):
        s = sum(abs(mu(pi)) for pi in cols if r(pi) == rr)
        er = sum(prod(c) for c in itertools.combinations(range(A), rr)) if rr else 1
        assert s == er, (A, rr, s, er)
        assert s <= A ** (2 * rr)
        assert all(sum(len(B) for B in pi) <= 2 * rr for pi in cols if r(pi) == rr)
print(f"(3.41) checked on {trials} random realized paths with A<=7 potential addresses: failures = {bad}")
print("(3.42) sum_{r(pi)=r}|mu(pi)| == e_r(0..A-1) <= A^{2r}, and #addresses <= 2r: verified for A<=7")
# negative control: drop the (h-1)! factor
bad2 = 0
for _ in range(200):
    A = 5; performed = set(range(A)); val = {a: rnd.randint(1, 2) for a in performed}
    lhs = 1 if len(set(val.values())) == len(val) else 0
    rhs = sum(prod((-1) ** (len(B) - 1) for B in pi) for pi in collections(range(A))
              if all(len({val[a] for a in B}) == 1 for B in pi))
    bad2 += (lhs != rhs)
print(f"negative control (drop (|B|-1)! in mu): failures = {bad2}/200")
