# Lemma 5.2: verify the explicit r-1 cycle uses only step-1 / step-4 chords and covers {1..r-1}.
def seq(r):
    if r == 7:
        return [1,5,6,2,3,4,1]
    return list(range(1, r-5)) + [r-2, r-1] + [r-5, r-4, r-3] + [1]
bad = 0
for r in range(7, 401):
    s = seq(r)
    gen = list(range(1, r-5)) + [r-2, r-1] + [r-5, r-4, r-3] + [1]
    if r == 7: assert gen == s, (gen, s)
    body = s[:-1]
    assert s[0] == s[-1] == 1
    if sorted(body) != list(range(1, r)) :
        bad += 1; print("cover fail", r); continue
    for u, w in zip(s, s[1:]):
        dd = (w - u) % r
        if dd not in (1, r-1, 4, r-4):
            bad += 1; print("chord fail", r, u, w, dd)
print("Lemma 5.2 construction checked r=7..400, failures:", bad)
