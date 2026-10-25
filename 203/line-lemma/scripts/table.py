#!/usr/bin/env python3
"""Derive the results table from the JSONL files (numbers on the page come from here, never typed)."""
import json, glob, os
from fractions import Fraction as F
D = os.path.join(os.path.dirname(os.path.abspath(__file__)))
rows = {}
for f in sorted((g for g in glob.glob(os.path.join(D, 'll_*.jsonl')) if os.path.basename(g)[3:-6].isdigit()), key=lambda s: int(os.path.basename(s)[3:-6])):
    N = int(os.path.basename(f)[3:-6]); rs = [json.loads(l) for l in open(f)]
    rr = os.path.join(D, f'll_{N}_rerun.jsonl')
    if os.path.exists(rr):
        rer = {tuple(r['dir']): r for r in (json.loads(l) for l in open(rr)) if 'cpsat' in r}
        rs = [rer.get(tuple(r.get('dir',[])), r) for r in rs] + [r for d,r in rer.items() if d not in {tuple(x.get('dir',[])) for x in rs}]
    done = [r for r in rs if 'cpsat' in r and r['cpsat'].get('V') is not None]
    sk = [r for r in rs if 'skipped' in r]
    opt = [r for r in done if r['cpsat']['status'] == 'OPTIMAL']
    # a direction excludes when the PROVEN upper bound on max-min is < 1 (OPTIMAL with V < 1, or a bound < 1 at the time limit)
    pass
    feas = {}
    for ff in (os.path.join(D, f'feas_{N}.jsonl'), os.path.join(D, f'feas_{N}_undecided.jsonl')):
        if os.path.exists(ff):
            for l in open(ff):
                r = json.loads(l)
                if 'feas' in r:
                    prev = feas.get(tuple(r['dir']))
                    # keep an INFEASIBLE verdict if any run produced one
                    if prev is None or (prev.get('cpsat_status') != 'INFEASIBLE' and prev.get('milp_status') != 2): feas[tuple(r['dir'])] = r['feas']
    # a direction counts as excluding if EITHER the max-min bound < 1 OR the feasibility model is INFEASIBLE (either solver)
    for r in done:
        fz = feas.get(tuple(r['dir']))
        if fz and (fz.get('cpsat_status') == 'INFEASIBLE' or fz.get('milp_status') == 2):
            r['feas_infeasible'] = True
    excl = [r for r in done if F(r['cpsat']['bound']) < 1 or r.get('feas_infeasible')]
    feas_rows = [r for r in done if F(r['cpsat']['V']) >= 1]
    und = [r for r in done if F(r['cpsat']['V']) < 1 <= F(r['cpsat']['bound']) and not r.get('feas_infeasible')]
    best = min(excl, key=lambda r: F(r['cpsat']['bound'])) if excl else None
    worst = max(excl, key=lambda r: F(r['cpsat']['bound'])) if excl else None
    milp = {}
    mf = os.path.join(D, f'milp_{N}.jsonl')
    if os.path.exists(mf):
        for l in open(mf):
            r = json.loads(l); milp[tuple(r['dir'])] = r
    rows[N] = dict(N=N, density=done[0]['density'] if done else None, density_f=done[0]['density_f'] if done else None,
                   ndirs=len(done), nopt=len(opt), nskip=len(sk), nexcl=len(excl), nfeas=len(feas), nund=len(und),
                   best=best, worst=worst, feas=feas_rows, und=und, milp=milp, feasm=feas)
print("| N | pool density Σ1/e_p | directions run (exact modulus unless noted) | excluding directions | min V (direction) | max V among excluding | feasible directions (V ≥ 1) | undecided | MILP agrees | feasibility model: CP-SAT INFEASIBLE / HiGHS INFEASIBLE / dirs |")
print("|---|---|---|---|---|---|---|---|---|---|")
for N, r in rows.items():
    if r['ndirs'] == 0: print(f"| {N} | — | 0 | | | | | | |"); continue
    b = r['best']; w = r['worst']
    def vs(x):
        c = x['cpsat']; 
        if c['status'] == 'OPTIMAL': return f"{c['V']} = {float(F(c['V'])):.4f} ({x['dir'][0]},{x['dir'][1]})"
        return f"≤ {c['bound']} = {float(F(c['bound'])):.4f}, best found {float(F(c['V'])):.4f} ({x['dir'][0]},{x['dir'][1]})"
    bs = vs(b) if b else "—"; ws = vs(w) if w else "—"
    fs = ", ".join(f"({x['dir'][0]},{x['dir'][1]}) {float(F(x['cpsat']['V'])):.4f}{'' if x['cpsat']['status']=='OPTIMAL' else '≥'}" for x in r['feas']) or "none"
    us = ", ".join(f"({x['dir'][0]},{x['dir'][1]}) best {float(F(x['cpsat']['V'])):.4f} bound {float(F(x['cpsat']['bound'])):.4f}" for x in r['und']) or "none"
    ms = "—"
    if r['milp']:
        ag = [m.get('milp',{}).get('agrees_cpsat') for m in r['milp'].values()]
        ms = f"{sum(1 for a in ag if a)}/{len(ag)}"
    fm = r['feasm']; fcs = "—"
    if fm:
        fcs = f"{sum(1 for v in fm.values() if v.get('cpsat_status')=='INFEASIBLE')} / {sum(1 for v in fm.values() if v.get('milp_status')==2)} / {len(fm)}"
    print(f"| {N} | {r['density']} = {r['density_f']:.4f} | {r['ndirs']} ({r['nopt']} optimal, {r['nskip']} skipped) | {r['nexcl']} | {bs} | {ws} | {fs} | {us} | {ms} | {fcs} |")
print()
tor = sorted(glob.glob(os.path.join(D, 'torus_*.jsonl')))
if tor:
    print("Coarse-torus runs:")
    for f in tor:
        for l in open(f):
            r = json.loads(l)
            if 'feas' in r: print(f"- {r['label']} T={r['T']}: feasibility {r['feas']['status']} ({r['feas']['wall']:.0f} s) → {r['verdict']}")
            else:
                c = r['cpsat']; print(f"- {r['label']} T={r['T']}: {c['status']} V={c['V']} bound={c['bound']} ({c['wall']:.0f} s) → {r['verdict']}")
