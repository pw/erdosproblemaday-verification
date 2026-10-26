import json, glob, math, sys
c0 = 1/(4*97**2); C0 = 192
print(f'{"run":<26} {"M":>4} {"U":>6} {"S1":>6} {"S2":>6} {"S2/S1":>6} {"H*S2/S1":>7} {"maxw":>5} {"96H^(2/3)U":>10} {"c0MH^(2/3)U":>11} {"C0MH^(-1/3)U":>12}  H<=N')
for f in sorted(glob.glob(sys.argv[1])):
    r = json.load(open(f)); M, U, H, N = r['M'], r['U'], r['H'], r['N']
    lo = c0*M*H**(2/3)*U; hi = C0*M*H**(-1/3)*U; wb = 96*H**(2/3)*U
    name = f.split('/')[-1].replace('.json', '').replace('paper_', '')
    print(f'{name:<26} {M:>4} {U:>6.2f} {r["S1"]:>6} {r["S2"]:>6} {r["S2"]/r["S1"]:>6.3f} {H*r["S2"]/r["S1"]:>7.2f} {r["maxweight"]:>5} {wb:>10.0f} {lo:>11.2f} {hi:>12.0f}  {H<=N}'
          + ('' if (r['S1'] >= lo and r['S2'] <= hi and r['maxweight'] <= wb) else '  <-- stated inequality FAILS'))
