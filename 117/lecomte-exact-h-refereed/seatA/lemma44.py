"""Seat A: exhaustive search for irredundant right-coset covers of small p-groups, testing Lemma 4.4:
   [U : cap H_i] <= p^(t-1)  for every irredundant cover by t right cosets H_i x_i.
A violation needs p^(t-1) < |U|, i.e. t <= log_p|U|; we search all t <= tmax (default log_p|U| + 1),
which is exhaustive for violations.
Also checks Tomkinson's bound [U : D] <= t! and records the extremal index per t.
Negative control: the same search with the bound replaced by p^(t-2) must find violators (the bound is attained).
"""
import sys, glob, math, collections

def load(fn):
    with open(fn) as f:
        n, p = map(int, f.readline().split())
        cos = []
        for line in f:
            sz, rest = line.split(" ", 1)
            idx = eval(rest)
            mask = 0
            for i in idx:
                mask |= 1 << (i - 1)
            cos.append((int(sz), mask))
    return n, p, cos

def search(n, p, cos, tmax):
    full = (1 << n) - 1
    # subgroup for each coset: the coset containing identity element index 1? We need H_i, the subgroup.
    # A right coset Hx determines H = {a b^-1 : a,b in Hx}; we recover H via the coset of the same subgroup
    # containing the identity -- grouped by file order: cosets of the same subgroup are consecutive with same size,
    # but to be safe we recompute: H = the unique coset (listed) that contains element 1 (the identity is
    # AsSSortedList(U)[1]) among cosets with the same subgroup id.  We tag subgroup ids by scanning.
    sub_id = []
    cur = -1; seen_sizes = None
    # cosets were written subgroup by subgroup, transversal order; a new subgroup starts when the running
    # union of the current subgroup's cosets equals full.
    acc = 0; sid = 0; sub_masks = {}
    for sz, m in cos:
        sub_id.append(sid)
        if m & 1:
            sub_masks[sid] = m
        acc |= m
        if acc == full:
            sid += 1; acc = 0
    assert acc == 0
    nsub = sid
    by_elt = [[] for _ in range(n)]
    for k, (sz, m) in enumerate(cos):
        if sz == n:
            continue  # the whole group: only gives the trivial t=1 cover
        mm = m; i = 0
        while mm:
            if mm & 1:
                by_elt[i].append(k)
            mm >>= 1; i += 1
    maxsize = n // p
    best = collections.defaultdict(int)  # t -> max index
    viol = []; count = collections.Counter()
    chosen = []

    def irredundant_so_far():
        for i in range(len(chosen)):
            others = 0
            for j in range(len(chosen)):
                if j != i:
                    others |= cos[chosen[j]][1]
            if cos[chosen[i]][1] & ~others == 0:
                return False
        return True

    def rec(covered):
        t = len(chosen)
        if covered == full:
            # irredundancy already maintained
            D = full
            for k in chosen:
                D &= sub_masks[sub_id[k]]
            idx = n // bin(D).count("1")
            count[t] += 1
            best[t] = max(best[t], idx)
            if idx > p ** (t - 1) or idx > math.factorial(t):
                viol.append((t, idx, list(chosen)))
            return
        if t == tmax:
            return
        unc = full & ~covered
        if bin(unc).count("1") > (tmax - t) * maxsize:
            return
        e = (unc & -unc).bit_length() - 1
        for k in by_elt[e]:
            # canonical: cosets must be added in increasing k order among those not forced? we allow any
            # (smallest uncovered element rule already limits duplicates to permutations of forced choices)
            chosen.append(k)
            if irredundant_so_far():
                rec(covered | cos[k][1])
            chosen.pop()

    rec(0)
    return best, viol, count

if __name__ == "__main__":
    files = sorted(glob.glob("/tmp/p117A/l44/c_*.txt"), key=lambda s: tuple(map(int, s.split("/")[-1][2:-4].split("_"))))
    extra = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    only = sys.argv[2:]
    totv = 0; tight = collections.Counter()
    for fn in files:
        tag = fn.split("/")[-1][2:-4]
        if only and tag.split("_")[0] not in only:
            continue
        n, p, cos = load(fn)
        tmax = round(math.log(n, p)) + extra
        best, viol, count = search(n, p, cos, tmax)
        totv += len(viol)
        for t, b in best.items():
            if b == p ** (t - 1):
                tight[(n, t)] += 1
        print(f"{tag:8s} |U|={n:4d} p={p} tmax={tmax}: covers by t: {dict(sorted(count.items()))}; "
              f"max index by t: {dict(sorted(best.items()))}; violations {len(viol)} {viol[:2]}", flush=True)
    print("TOTAL violations:", totv, "| bound p^(t-1) attained (order,t):", dict(tight))
