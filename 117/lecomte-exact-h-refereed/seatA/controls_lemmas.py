"""Negative controls: mutate the per-form data so that each lemma predicate MUST fire."""
import analyze, collections
def fresh():
    st = collections.defaultdict(list); st["maxa"] = {}
    for k in ["n_L42","n_L45a","n_L45b","n_L46","n_L45w","n_L21","n_AVG","n_EQ4"]: st[k] = 0
    return st
gs = {g["id"]: g for g in analyze.parse("/tmp/p117A/controls.txt")}
E243 = gs[6]; E128 = gs[9]
# L42: pretend E243's form has rank 2 & abelian radical: a=10 != omega=7 must be flagged
g = dict(E243); f = list(g["forms"][0]); f[0] = 1; f[1] = True; g["forms"] = [f]
st = fresh(); analyze.analyze(g, st); print("L42 fires:", len(st["L42"]) > 0)
# L45a: pretend radical abelian noncentral with j=2 (needs omega >= 19 at p=3): must fire
g = dict(E243); f = list(g["forms"][0]); f[1] = True; f[2] = False; g["forms"] = [f]
st = fresh(); analyze.analyze(g, st); print("L45a fires:", len(st["L45a"]) > 0)
# L45b / L45w: pretend nonabelian radical with m=5
g = dict(E243); f = list(g["forms"][0]); f[1] = False; f[2] = False; f[3] = 5; g["forms"] = [f]
st = fresh(); analyze.analyze(g, st); print("L45b fires:", len(st["L45b"]) > 0, " L45w fires:", len(st["L45w"]) > 0)
# L46: pretend e = 2 (xi of length 2) with central radical, j=2: needs omega >= 10 > 7
g = dict(E243); f = list(g["forms"][0]); f[7] = [1, 0]; g["forms"] = [f]
st = fresh(); analyze.analyze(g, st); print("L46 fires:", len(st["L46"]) > 0)
# AVG/EQ4: pretend omega is tiny by halving -> use E128 with fake j=4? instead scale: set j huge-small: j=1 => bound C_2(2)*7/3=7 < sum widths 63
g = dict(E128); f = list(g["forms"][0]); f[0] = 1; g["forms"] = [f]
st = fresh(); analyze.analyze(g, st); print("AVG fires:", len(st["AVG"]) > 0, " EQ4 fires:", len(st["EQ4"]) > 0)
# L21: corrupt labels so fibres are mixed -> width != index somewhere
g = dict(E128); f = list(g["forms"][0]); labs = list(f[5]); labs = labs[::-1]; f[5] = labs; g["forms"] = [f]
st = fresh();
try:
    analyze.analyze(g, st); print("L21 fires:", len(st["L21"]) > 0)
except Exception as ex:
    print("L21 corrupted labels raised:", type(ex).__name__)
# L21 retry: a group of order 64 with an abelian noncentral radical; merge two fibres' labels
import random
random.seed(1)
for g in analyze.parse("/tmp/p117A/data/s64.txt"):
    fs = [f for f in (g.get("forms") or []) if f[1] and not f[2]]
    if not fs: continue
    f = list(fs[0]); labs = list(f[5]); idlab = labs[[len(r) for r in g["rows"]].index(len(g["rows"]))]
    # move one non-R coset into the R fibre label -> R "fibre" now contains a noncommuting coset
    k = next(i for i, l in enumerate(labs) if l != idlab)
    labs[k] = idlab; f[5] = labs
    g2 = dict(g); g2["forms"] = [f]
    st = fresh(); analyze.analyze(g2, st)
    print("L21/AVG with merged fibre fires:", len(st["L21"]) > 0 or len(st["AVG"]) > 0, "group", g["id"])
    break
# L21 retry 2: apply the abelian-coset formula to a NONABELIAN radical (Lemma 2.1 hypothesis false) -> must fire
for g in analyze.parse("/tmp/p117A/data/s64.txt"):
    fs = [f for f in (g.get("forms") or []) if not f[1]]
    if not fs: continue
    f = list(fs[0]); f[1] = True; f[2] = False
    g2 = dict(g); g2["forms"] = [f]
    st = fresh(); analyze.analyze(g2, st)
    if st["L21"]:
        print("L21 fires on nonabelian radical treated as abelian: True, group", g["id"], st["L21"][:2]); break
else:
    print("L21 never fired: FAIL")
