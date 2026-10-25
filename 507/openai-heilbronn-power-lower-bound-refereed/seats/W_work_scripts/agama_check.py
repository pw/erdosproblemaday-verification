import itertools, math
def minarea(pts):
    best = float('inf')
    for a, b, c in itertools.combinations(pts, 3):
        A = abs((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))/2
        best = min(best, A)
    return best
R = 0.5  # Agama's compression circle has radius < 1/2 (diameter G<1)
for s in [9, 10, 21, 22, 41, 42]:
    m = s - 1
    ring = [(R*math.cos(2*math.pi*j/m), R*math.sin(2*math.pi*j/m)) for j in range(m)]
    with_c = minarea(ring + [(0.0, 0.0)])
    no_c = minarea(ring)
    formula = 2*R*R*math.sin(math.pi/m)**2*math.sin(2*math.pi/m)
    claim = math.log(s)/(s*math.sqrt(s))
    print(f"s={s:3d} m={m:3d} min(ring+centre)={with_c:.3e} min(ring)={no_c:.3e} formula={formula:.3e} claimed log s/s^1.5={claim:.3e}")
