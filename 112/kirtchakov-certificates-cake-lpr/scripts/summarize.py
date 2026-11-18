#!/usr/bin/env python3
"""Summarise res/*.json + allcnf/sha_check.txt + allcnf/indep.txt into counts for the page. Prints JSON."""
import json, glob, os, re, sys
K = os.path.expanduser('~/MathDyad/erdos112/kirtchakov')
R = {}
for f in glob.glob(K + '/work/res/*.json'):
    r = json.load(open(f)); R[r['name']] = r
cubes = [l.split()[0] for l in open(K + '/work/cubes.txt')]
lay = lambda n: 21 if n.startswith('s21') else 22 if n.startswith('s22') else 23 if n.startswith('s23') else 24
def ok(r): return (r.get('cnf_matches_ledger') and r.get('solver_rc') == 20 and r.get('cake_verified') and r.get('solver_status') == 's UNSATISFIABLE'
                   and r.get('wall', 0) + 2 >= max(r.get('solve_secs') or 0, r.get('check_secs') or 0) and r.get('lrat_bytes', 0) > 0)
out = {'done': len(R), 'total': len(cubes)}
out['ok'] = sum(1 for r in R.values() if ok(r)); out['bad'] = sorted(n for n, r in R.items() if not ok(r))
out['identical'] = sum(1 for r in R.values() if r.get('lrat_matches_ledger')); out['not_identical'] = sorted(n for n, r in R.items() if not r.get('lrat_matches_ledger'))
for L in (21, 22, 23, 24):
    names = [n for n in cubes if lay(n) == L]
    out[f'L{L}_total'] = len(names); out[f'L{L}_ok'] = sum(1 for n in names if n in R and ok(R[n]))
out['bytes_checked'] = sum(r['lrat_bytes'] for r in R.values() if ok(r))
out['solve_cpu_h'] = round(sum((r.get('solve_secs') or 0) for r in R.values()) / 3600, 1)
out['check_cpu_h'] = round(sum((r.get('check_secs') or 0) for r in R.values()) / 3600, 1)
out['max_proof'] = max(((r['lrat_bytes'], n) for n, r in R.items()), default=None)
try:
    sc = [l.split() for l in open(K + '/allcnf/sha_check.txt')]
    out['sha_lines'] = len(sc); out['sha_match'] = sum(1 for x in sc if x[2] == 'MATCH')
except FileNotFoundError: out['sha_lines'] = 0
try:
    t = open(K + '/allcnf/indep.txt').read()
    out['indep_equal'] = len(re.findall(r' EQUAL ', t)); out['indep_diff'] = len(re.findall(r' DIFF ', t))
    out['inventory_lines'] = [l for l in t.splitlines() if l.startswith(('I3L3', 'TT4F'))]
    out['indep_done'] = 'DONE' in t
except FileNotFoundError: out['indep_equal'] = None
print(json.dumps(out, indent=1))
