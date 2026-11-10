import math, re
g = 0.5772156649015329
# (e, J, pi_s, E_C[J], E_z5, E_z19, small_model, pair_full, pair_z19, pair_z5)
model = {}
for e, f in ((12,'/tmp/ref912/model_1e12.out'),(13,'/tmp/ref912/model_1e13.out'),(15,'/home/exedev/MathDyad/erdos912/model_1e15.out'),
             (16,'/home/exedev/MathDyad/erdos912/model_1e16.out'),(17,'/home/exedev/MathDyad/erdos912/model_1e17.out'),(18,'/home/exedev/MathDyad/erdos912/model_1e18.out')):
    t = open(f).read(); J = int(re.search(r'Jactual=(\d+)', t).group(1)); m = {}
    for line in t.splitlines():
        w = line.split()
        if w and (w[0] == 'cramer' or w[0].startswith('z=')) and len(w) == 6: m[w[0]] = float(w[2])
    model[e] = (J, m)
pair = {}
for f in ('/tmp/ref912/pair_a.out', '/tmp/ref912/pair_b.out'):
    for line in open(f):
        mm = re.match(r'1e(\d+): pair-only predicted dE\[J\]: full HL = ([\d.]+)  z=19 = ([\d.]+)  z=5 = ([\d.]+)', line)
        if mm: pair[int(mm.group(1))] = tuple(map(float, mm.groups()[1:]))
pis = {12: 78498, 13: 227647, 15: 1951957, 16: 5761455, 17: 17082666, 18: 50847534}
print("e  gap=J-E_C   pairHL  pairHL/gap  z19exact/z19pair  z5exact/z5pair  pairHL*k19/gap  (J-E_z19)/(gap)  (J-E_z19) vs (pairHL-pair19)*k19")
for e in sorted(pair):
    if e not in model: continue
    J, m = model[e]; gap = J - m['cramer']; pf, p19, p5 = pair[e]
    k19 = (m['z=19'] - m['cramer']) / p19; k5 = (m['z=5'] - m['cramer']) / p5
    print(f"{e}  {gap:11.1f}  {pf:10.1f}  {pf/gap:.4f}  {k19:.4f}  {k5:.4f}  {pf*k19/gap:.4f}  {(J-m['z=19'])/gap:.4f}  {J-m['z=19']:.0f} vs {(pf-p19)*k19:.0f}")
print()
print("e  actual ratio  (ratio/sqrt2pi-1)*L   GI-expansion LL/L coefficient check")
for e in (12, 13, 15, 16, 17, 18):
    n = 10**e; L = math.log(n); LL = math.log(L); sc = math.sqrt(n/L); J, m = model[e]
    h = pis[e] + J; r = h / sc
    print(f"{e}  {r:.6f}  {(r/math.sqrt(2*math.pi)-1)*L:.4f}   Cramér-expansion (1 - LL/2L + (1+g+log8)/2L - 1)*L = {(-LL/2 + (1+g+math.log(8))/2):.4f}   HL pair-level asymptotic = {(g+math.log(2*math.pi)-1)/2:.4f}")
