"""Positive and negative controls for analyze.py"""
import analyze, collections
expect = {1: ("S3", 4, 4), 2: ("A4", 5, 5), 3: ("D8", 3, 3), 4: ("E27", 4, 4), 5: ("E125", 6, 6),
          6: ("E243", 7, 10), 7: ("E243b", 7, 10), 8: ("E32p", 5, 5), 9: ("E128p", 7, 9), 10: ("UT3F4", 5, 5)}
ok = True
for g in analyze.parse("/tmp/p117A/controls.txt"):
    st = collections.defaultdict(list); st["maxa"] = {}
    for k in ["n_L42","n_L45a","n_L45b","n_L46","n_L45w","n_L21","n_AVG","n_EQ4"]: st[k] = 0
    r = analyze.analyze(g, st)
    name, om, a = expect[g["id"]]
    good = (r["omega"], r["a"]) == (om, a)
    ok &= good
    viol = {k: len(st[k]) for k in ["G1","G2","L42","L45a","L45b","L45w","L21","L46","AVG","EQ4"] if st.get(k)}
    print(f"{name:6s} z={r['z']:4d} omega={r['omega']} a={r['a']} expected ({om},{a}) {'OK' if good else 'MISMATCH'}  violations={viol}")
# negative control 1: a wrong profile T'(n)=n must be flagged on E243 (a=10>7)
orig = analyze.T
analyze.T = lambda n: n if n >= 3 else 1
st = collections.defaultdict(list); st["maxa"] = {}
for k in ["n_L42","n_L45a","n_L45b","n_L46","n_L45w","n_L21","n_AVG","n_EQ4"]: st[k] = 0
for g in analyze.parse("/tmp/p117A/controls.txt"):
    analyze.analyze(g, st, deep=False)
print("negative control (profile T'(n)=n): flagged", st["G1"])
assert any(x[0][1] in (6, 7) for x in st["G1"])
analyze.T = orig
# negative control 2: corrupt E243 data so that two noncommuting cosets are declared commuting -> omega/a change
for g in analyze.parse("/tmp/p117A/controls.txt"):
    if g["id"] == 6:
        rows = g["rows"]
        # make coset 2 commute with everything (would make it central-like) -> must violate assertion of unique centre
        try:
            rows2 = [list(r) for r in rows]; rows2[1] = list(range(1, len(rows) + 1))
            g2 = dict(g); g2["rows"] = rows2; g2["forms"] = []
            analyze.analyze(g2, st, deep=False); print("negative control 2: NOT caught")
        except AssertionError:
            print("negative control 2: corrupted data rejected (two central cosets) OK")
print("ALL CONTROLS", "PASS" if ok else "FAIL")
