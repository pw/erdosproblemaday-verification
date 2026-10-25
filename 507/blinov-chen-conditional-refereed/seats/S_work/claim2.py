# Seat S: independent check of the packing claims (claim 2 + Wroblewski addendum).
# Usage: python3 -I claim2.py <setname> [mutation]
#   setname: bt163 (generate {bt(a)*163+l}) | file:<path>
#   mutation: none | ap (insert a 3-AP) | tagonnorm (move a tag onto a norm word)
#             | tagabovenorm (make a norm word smaller than the largest tag) | l0missing (drop 0)
import sys
O23 = [0,1,3,7,8,10,18,21,22,25,27,30,48,56,58,61,62,65,67,70,77,80,81]

def bt(a):  # binary digits of a read in base 3
    v, p = 0, 1
    while a:
        v += (a & 1) * p; a >>= 1; p *= 3
    return v

def load(name):
    if name == "bt163":
        return sorted(bt(a) * 163 + l for a in range(127) for l in O23)
    assert name.startswith("file:")
    xs = [int(t) for t in open(name[5:]).read().split()]
    return xs

def ap_free(S):
    """True iff no x<y in S with (x+y)/2 in S.  Returns (ok, witness)."""
    st = set(S); L = sorted(S)
    for i, x in enumerate(L):
        for y in L[i+1:]:
            if (x + y) & 1 == 0 and (x + y) // 2 in st:
                return False, (x, (x + y) // 2, y)
    return True, None

def main():
    name = sys.argv[1]; mut = sys.argv[2] if len(sys.argv) > 2 else "none"
    S = load(name)
    fails = []
    def check(cond, msg):
        if not cond: fails.append(msg)
    if mut == "ap":          # replace the largest element by 2*m - x for two members -> forces an AP
        x, m = S[5], S[200]
        S = sorted(set(S[:-1]) | {2*m - x})
    if mut == "l0missing":
        S = [x + 1 for x in S]               # shift: 0 no longer in set (row-1 position 0 becomes a foreign tag)
    S = sorted(S)
    check(len(S) == len(set(S)) == 2921, f"size {len(S)} distinct {len(set(S))}")
    ok, wit = ap_free(S)
    check(ok, f"3-AP found {wit}")
    tags = S[:5]; norm = S[5:]
    if mut == "tagonnorm":
        tags = tags[:4] + [norm[0]]          # a tag placed on a norm position
    if mut == "tagabovenorm":
        # keep the set, but declare tags = smallest four + the 7th element; norm = rest (norm word below a tag)
        tags = S[:4] + [S[6]]; norm = [x for x in S if x not in tags]
    mx = max(S); k = 2 * mx + 1
    print(f"set={name} mut={mut} |S|={len(S)} min={S[0]} max={mx} k={k} tags={tags} first_norm={min(norm)} |norm|={len(norm)}")
    check(len(norm) == 2916, f"norm words {len(norm)} != 2916")
    check(S[0] == 0, "0 not in set (row-1 position 0 is then not covered by AP-freeness)")
    check(max(tags) < min(norm), f"max tag {max(tags)} >= first norm word {min(norm)} (tagged-moment needs a < first norm word)")
    check(sorted(tags) == tags, "tags not increasing in s")
    # positions
    row1 = {0: "tag"}
    for c in norm: row1[c] = row1.get(c, "") + "norm"
    row2 = {}
    for t in tags: row2[t] = row2.get(t, "") + "tag"
    for c in norm: row2[c] = row2.get(c, "") + "norm"
    check(all(v in ("tag", "norm") for v in row1.values()), "row-1 position used twice (tag and norm)")
    check(all(v in ("tag", "norm") for v in row2.values()), "row-2 position used twice (tag and norm)")
    ell = {k - 1 - 2 * c: c for c in norm}
    check(len(ell) == len(norm), "row-3 positions not injective")
    check(all(0 <= p < k for p in list(row1) + list(row2) + list(ell)), "position outside [0,k)")
    check(min(ell) == 2 * (mx - max(norm)) and min(ell) >= 0, "ell range")
    # every designated triple summing to k-1
    hits = {"matched": 0, "norm-norm-unmatched": 0, "tag-involved": 0}
    bad = []
    for p1, t1 in row1.items():
        for p2, t2 in row2.items():
            p3 = k - 1 - p1 - p2
            if p3 in ell:
                c3 = ell[p3]
                if t1 == "norm" and t2 == "norm" and p1 == p2 == c3:
                    hits["matched"] += 1
                elif t1 == "norm" and t2 == "norm":
                    hits["norm-norm-unmatched"] += 1; bad.append((p1, p2, p3))
                else:
                    hits["tag-involved"] += 1; bad.append((t1, p1, t2, p2, p3))
    print("triples with sum k-1:", hits, "examples:", bad[:3])
    check(hits["matched"] == 2916 and len(bad) == 0, "matching property / tag exclusion FAILS")
    # tagged-moment structure: fresh position v=k-1-a > a for every tag a, k >= 2*span
    for a in tags:
        check(k - 1 - a > a, f"fresh position fails for a={a}")
    check(k >= 2 * (max(tags) + 1), "k < 2*span")
    if fails:
        print("FAIL:", *fails, sep="\n  ")
        sys.exit(1)
    print("ALL CLAIM-2 CHECKS PASSED")

if __name__ == "__main__":
    main()
