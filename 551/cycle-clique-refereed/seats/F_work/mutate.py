# Seat F mutation driver: each mutation = list of (old, new) exact-substring replacements on a COPY of original_checker.py.
# Every replacement must match exactly once, else the mutation is reported INVALID (a mutation that does not apply tests nothing).
import subprocess, sys, json, time, os
SRC = open('/tmp/oaimath/189/repo/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/verification/code/original_checker.py').read()
EXPECTED = open('/tmp/oaimath/189/repo/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/verification/data/expected-output.txt').read()
W = '/tmp/oaimath/189/seats/F_work/mut'
os.makedirs(W, exist_ok=True)
M = {
 # ---- control: identity (must reproduce expected output) ----
 'CONTROL': [],
 # ---- WEAKENINGS (rule deleted or weakened; sound but less powerful) ----
 'W1_no_extension_rule': [("    return out\n\ndef empty", "    return set()\n\ndef empty")],
 'W2_ext_lower_always_plus1': [("low = L+(e>=len(edges))-q", "low = L+1-q")],
 'W3_ext_upper_minus1': [("high = k+1-v-q", "high = k-v-q")],
 'W4_ext_E_empty_only': [("for mask in range(1<<len(rest)):", "for mask in range(1):")],
 'W5_ext_E_all_rest_only': [("for mask in range(1<<len(rest)):", "for mask in [(1<<len(rest))-1]:")],
 'W6_no_required_path_rule': [("            for used,x in states:\n                A[i][x].add(k-ell)\n", "            pass\n")],
 'W7_no_strengthening': [("        new = []\n", "        return 0\n        new = []\n")],
 'W8_no_d0_trials': [("for d in (0,1):", "for d in (1,):")],
 'W9_no_d1_trials': [("for d in (0,1):", "for d in (0,):")],
 'W10_no_exception_9_11': [("            if val==1 and b==c==t and k+1-n+T>=t:\n                val = 2\n", "")],
 'W11_no_size_test_triple': [("+int(c>max(k,2*t))", "")],
 'W12_u0_no_clique_pair': [("u = 1+int(b>=t)", "u = 1")],
 'W13_no_Tr_excluded_neighbours': [("T = sum(req[r]<=m for m in row)", "T = 0")],
 'W14_no_singletons': [("        W[i,-1] = 1\n", "")],
 'W15_no_radius2': [("for r in (1,2):", "for r in (1,):")],
 'W16_no_radius1or2': [("for r in (1,2):", "for r in ():")],
 'W17_no_ball_bound_growth_term': [("c = max(b,k*u+1-n+T)", "c = b")],
 'W18_no_clique_pair_rule_in_balls': [("val = max(u,1+int(c>t)+int(c>max(k,2*t)))", "val = max(u,1+int(c>max(k,2*t)))")],
 'W19_no_size_test_and_no_exception': [("+int(c>max(k,2*t))", ""), ("            if val==1 and b==c==t and k+1-n+T>=t:\n                val = 2\n", "")],
 # ---- convention variant (still sound): in-round updates applied immediately ----
 'V1_inplace_updates': [("                        new.append((i,j,d))\n", "                        new.append((i,j,d)); M[i][j].add(d); M[j][i].add(d)\n")],
 'W20_singleton_pairs_never_compatible': [("    req[0] = {0}\n", "    req[0] = {-99}\n")],
 'S9_req0_left_empty_singletons_always_compatible': [("    req[0] = {0}\n", "")],
 # ---- STRENGTHENINGS (stronger than proved = UNSOUND; should only ever exclude more) ----
 'S1_ext_drop_indicator': [("low = L+(e>=len(edges))-q", "low = L-q")],
 'S2_ext_upper_plus1': [("high = k+1-v-q", "high = k+2-v-q")],
 'S3_compat_one_less': [("req[r+s+2]<=M[i][j]", "req[max(0,r+s+1)]<=M[i][j]")],
 'S4_size_test_ge': [("int(c>max(k,2*t))", "int(c>=max(k,2*t))")],
 'S5_no_reach_test': [("                if w not in reach:\n", "                if True:\n")],
 'S6_no_degree_test': [("            if sum(z in edge for edge in E) >= 2:\n                continue\n", ""), ("if z>=w or sum(w in edge for edge in E)>=2:", "if z>=w:")],
 'S7_reqpath_plus1': [("A[i][x].add(k-ell)", "A[i][x].add(k-ell+1)")],
 'S8_u0_strict_gt_replaced_ge_tminus1': [("u = 1+int(b>=t)", "u = 1+int(b>=t-1)")],
}
only = sys.argv[1:] or list(M)
res = {}
for name in only:
    s = SRC
    ok = True
    for old, new in M[name]:
        c = s.count(old)
        if c != 1:
            ok = False; print(name, 'INVALID anchor count', c, repr(old[:50]), flush=True); break
        s = s.replace(old, new)
    if not ok:
        res[name] = 'INVALID'; continue
    if name != 'CONTROL' and s == SRC:
        res[name] = 'NOOP'; print(name, 'NOOP', flush=True); continue
    p = f'{W}/{name}.py'
    assert s.count("    print(k,*counts)") == 1
    open(p, 'w').write(s.replace("    print(k,*counts)", "    print(k,*counts, flush=True)"))
    t0 = time.time()
    lim = int(os.environ.get('MUT_TIMEOUT', '900'))
    r = subprocess.run(['bash', '-c', f'ulimit -v 8000000; exec timeout {lim} nice -n 19 python3 -I {p}'], capture_output=True, text=True)
    dt = time.time() - t0
    rows = [list(map(int, l.split())) for l in r.stdout.strip().splitlines() if l.strip()]
    z = sum(x[1] for x in rows); o1 = sum(x[2] for x in rows); o2 = sum(x[3] for x in rows)
    same = (r.stdout == EXPECTED)
    res[name] = dict(rc=r.returncode, out0=z, out1=o1, out2=o2, same_as_expected=same, secs=round(dt, 1),
                     rows=rows, stderr=r.stderr[-300:])
    print(name, 'rc', r.returncode, 'ks_done', [x[0] for x in rows], 'out0', z, 'out1', o1, 'out2', o2, 'identical' if same else 'DIFFERS', f'{dt:.0f}s', flush=True)
    json.dump(res, open(f'{W}/results_{os.getpid()}.json', 'w'), indent=1)
json.dump(res, open(f'{W}/results_last.json', 'w'), indent=1)
