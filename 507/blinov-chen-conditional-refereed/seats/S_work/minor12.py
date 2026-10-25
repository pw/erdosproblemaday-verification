# Seat S: check that, with Blinov's top-row layout (row 1 = 1,r,r,... below the first norm word T; row 2 = tag digits
# at the tag positions and r elsewhere below T), the (1,2)-minor c1*c2' - c2*c1' = 0 mod B^T forces equal labels.
# Exhaustive over label pairs for a toy (r=7, 5 tags), norm residues at positions >= T random per label.
# mutation droptag: the last label coordinate is not written in row 2 (must produce violations)
# Usage: python3 -I minor12.py <tags comma> <T> [normbelow]
import sys, random, itertools
tags = [int(x) for x in sys.argv[1].split(",")]; T = int(sys.argv[2]); mut = sys.argv[3] if len(sys.argv) > 3 else ""
r, B = 7, 1009; P = T + 4                               # B prime > r; look at P digits (mod B^P >= mod B^T)
rng = random.Random(1)
normpos = set(range(T, P)) | ({tags[-1] - 1} if mut == "normbelow" else set())
pref = list(itertools.product(range(r), repeat=len(tags)-1)); rng.shuffle(pref)
labels = [p + (x,) for p in pref[:60] for x in range(r)]   # includes pairs differing only in the last coordinate
def dig(x): return r if x % r == 0 else x % r
def col(lab):
    row1 = [1 if p == 0 else (dig(rng.randrange(r)) if p in normpos else r) for p in range(P)]
    row2 = [dig(lab[tags.index(p)]) if (p in tags and not (mut == 'droptag' and p == tags[-1])) else (dig(rng.randrange(r)) if p in normpos else r) for p in range(P)]
    return sum(x * B**i for i, x in enumerate(row1)), sum(x * B**i for i, x in enumerate(row2))
cols = {lab: col(lab) for lab in labels}
m = B**T; viol = 0; pairs = 0
for l1, l2 in itertools.combinations(labels, 2):
    (a1, b1), (a2, b2) = cols[l1], cols[l2]; pairs += 1
    if (a1 * b2 - b1 * a2) % m == 0: viol += 1
print(f"tags={tags} T={T} mut={mut}: distinct label pairs {pairs}, with (1,2)-minor = 0 mod B^T: {viol}")
