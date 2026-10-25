p = '/tmp/oaimath/191b/seats/G_work/cap_toy.py'
s = open(p).read()
old_a = "        a = (a1, random.randrange(q), random.randrange(q))\n"
assert s.count(old_a) == 1
s = s.replace(old_a, old_a + "        if MUT == \"slab2\":\n"
              "            a = (a1, 0, random.randrange(q))   # coord 2 carries the slab but is not shift-protected\n")
old_t = "total = 0\nfor (q, H, w) in ((307, 2, 2), (401, 2, 2), (211, 2, 1)):"
assert s.count(old_t) == 1
s = s.replace(old_t, '''def cap_only(q, w):
    # for w <= 2 the slab is a cap for ANY quadratic Q (a line with v1 != 0 meets <= w slab layers), so the
    # cap check inside run() is vacuous there; this sweep uses w >= 3 so the square_nu mutation can fail.
    nu = next(t for t in range(2, q) if not is_square(t, q))
    if MUT == "square_nu":
        nu = 4 % q
    S = [(x, y, (x * x - nu * y * y) % q) for x in range(w) for y in range(q)]
    for p in S:
        seen = set()
        for o in S:
            if o != p:
                dvec = projective(tuple((o[i] - p[i]) % q for i in range(3)), q)
                assert dvec not in seen, f"three collinear points in S (q={q}, w={w})"
                seen.add(dvec)

for (q, w) in ((31, 31), (101, 3), (101, 10), (103, 7), (127, 5)):
    cap_only(q, w)
print("cap-only sweep passed")

total = 0
for (q, H, w) in ((307, 2, 4), (401, 2, 2)):''')
old_r = "    for trial in range(2):"
assert s.count(old_r) == 1
s = s.replace(old_r, "    for trial in range(1):")
open(p, 'w').write(s)
print("edited")
