# Seat S: provenance probe - can the file be reproduced from the stated recipe? (does not affect validity)
p, n, c, d = 3889, 216, 1331, 640
D = [1,2,4,8,9,13,21,23,26,27,30,32,35,36]
g = next(g for g in range(2, p) if all(pow(g, (p-1)//f, p) != 1 for f in (2, 3)))
z = pow(g, (p-1)//n, p)
roots = {pow(z, i, p) for i in range(n)}
assert len(roots) == n
R = sorted((c*x + d) % p for x in roots)
full = sorted(p*b + x for b in D for x in R)
fileset = sorted(int(t) for t in open("/tmp/oaimath/191b/pack/wroblewski2921.txt").read().split())
print("recipe size", len(full), "min", full[0], "max", full[-1])
# try: shift so that some window of 2921 consecutive elements starts at 0
for i in range(len(full) - 2920):
    w = [x - full[i] for x in full[i:i+2921]]
    if w == fileset:
        print("file = recipe elements", i, "..", i+2920, "shifted by", full[i]); break
else:
    print("file NOT a shifted window of the recipe")
st = set(full)
print("recipe 3-AP-free:", not any((x+y) % 2 == 0 and (x+y)//2 in st for i, x in enumerate(full) for y in full[i+1:]))
Ds = set(D); print("block index set 3-AP-free:", not any((x+y)%2==0 and (x+y)//2 in Ds for i,x in enumerate(D) for y in D[i+1:]))
spans = [(full[i+2920] - full[i], i) for i in range(len(full) - 2920)]
best = min(spans)
print("min span over 2921-windows:", best, " file span:", spans[0])
i = best[1]; w = [x - full[i] for x in full[i:i+2921]]
print("best window: 5 smallest", w[:5], "6th", w[5], " k =", 2*w[-1]+1)
rw = sorted(w[-1] - x for x in w); print("reflected best window: 5 smallest", rw[:5], "6th", rw[5])
