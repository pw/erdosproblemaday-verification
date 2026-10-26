import json, glob, sys, math
pat = sys.argv[1] if len(sys.argv) > 1 else 'runs/paper_*.json'
tot_adm = tot_viol = tot_ext_fail = 0; ctl = {'tau': [0, 0], 'id': [0, 0], 'lowH': [0, 0]}
print(f'{"run":<34} {"cert":>5} {"S1":>5} {"S2":>5} {"a1max":>5} {"admE>0":>6} {"viol":>4} {"extF":>4}  tauFail/tauE>0  lowH-sig/stau fail/E>0  idFail/idE>0')
for f in sorted(glob.glob(pat)):
    r = json.load(open(f))
    T = r['table']
    adm = [t for t in T if t['adm'] and t['Ep'] > 0]
    viol = [t for t in adm if not t['holds']]
    extF = [t for t in T if t['cls'] != 'ram' and not t['ext_holds']]
    tau = [t for t in T if t['cls'] == 'tau' and t['Ep'] > 0]; tauF = [t for t in tau if not t['holds']]
    low = [t for t in T if t['cls'] in ('sigma', 'sigtau') and t['p'] <= r['H'] and t['Ep'] > 0]; lowF = [t for t in low if not t['holds']]
    idd = [t for t in T if t['cls'] == 'id' and t['Ep'] > 0]; idF = [t for t in idd if not t['holds']]
    tot_adm += len(adm); tot_viol += len(viol); tot_ext_fail += len(extF)
    ctl['tau'][0] += len(tauF); ctl['tau'][1] += len(tau); ctl['lowH'][0] += len(lowF); ctl['lowH'][1] += len(low); ctl['id'][0] += len(idF); ctl['id'][1] += len(idd)
    name = f.split('/')[-1].replace('.json', '')
    print(f'{name:<34} {str(r["exact_cert"])[0]:>5} {r["S1"]:>5} {r["S2"]:>5} {r["amax"][0]:>5} {len(adm):>6} {len(viol):>4} {len(extF):>4}  {len(tauF)}/{len(tau)}  {len(lowF)}/{len(low)}  {len(idF)}/{len(idd)}'
          + ('' if r['prod_ok'] else '  NORM-PROD FAIL') + ('' if not viol else '  VIOL:' + str([(t['p'], t['Ep'], t['vp']) for t in viol])))
print(f'TOTAL admissible (p,run) pairs with E_p>0: {tot_adm}; Lemma-7 violations: {tot_viol}; extended-prediction failures: {tot_ext_fail}')
print(f'controls (fail/tested): tau-class E_p<=v_p fails {ctl["tau"]}; sigma/sigtau with p<=H fails {ctl["lowH"]}; identity class fails {ctl["id"]}')
