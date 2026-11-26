"""Load the certificate pickles with a RESTRICTED unpickler (only the four numpy
globals seen in the opcode listing) and check what the audit script does NOT:
  - every hypothesis factor uses a bound that is actually a hypothesis of Prop 9.3
  - the total configuration degree of every multiplier is <= 7 (else the
    7-vertex expansion silently drops terms)
"""
import pickle, re, sys, collections
import numpy as np

ALLOWED = {('numpy._core.multiarray', '_reconstruct'), ('numpy', 'ndarray'),
           ('numpy', 'dtype'), ('numpy._core.multiarray', 'scalar')}


class R(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked global {module}.{name}")


def load(p):
    with open(p, 'rb') as f:
        return R(f).load()


def factors_of(expr):
    if expr == '1':
        return []
    out = []
    for tok in expr.split('*'):
        m = re.fullmatch(r"D\(([\d, ]*)\)>=(-?\d+)", tok)
        if m:
            S = tuple(int(v) for v in re.findall(r"\d+", m.group(1)))
            out.append(('ge', len(S), int(m.group(2)), 1)); continue
        m = re.fullmatch(r"deg(\d+)<=(-?\d+)", tok)
        if m:
            out.append(('le', 1, int(m.group(2)), 1)); continue
        m = re.fullmatch(r"int\[D\(([\d, ]*)\),(-?\d+)\]", tok)
        if m:
            S = tuple(int(v) for v in re.findall(r"\d+", m.group(1)))
            out.append(('int', len(S), int(m.group(2)), 2)); continue
        raise ValueError(tok)
    return out


for p in sys.argv[1:]:
    c = load(p)
    print("==", p.split('/')[-1])
    print("  keys:", sorted(c.keys()))
    print("  args:", c.get('args'))
    print("  s, N, nu:", c['s'], c['N'], c['nu'])
    n = len(c['w'])
    toks = collections.Counter()
    maxdeg = 0
    over = []
    kinds = collections.Counter()
    specials = []
    for i in range(n):
        sup = c['support'][i]
        if sup[0] == 'psd':
            nm = c['psd_names'][i]
            mo = re.fullmatch(r"r(\d+)s(\d+):(mono(\d+)|pair )x\[(.*)\]", nm)
            r = int(mo.group(1))
            vdeg = 2 if mo.group(3).startswith('pair') else int(mo.group(4))
            fs = factors_of(mo.group(5))
            deg = r + 2 * vdeg + sum(f[3] for f in fs)
            kinds['psd ' + ('pair' if vdeg == 2 and mo.group(3).startswith('pair') else f'mono{vdeg}')] += 1
        else:
            nm = c['lin_names'][i]
            mo = re.fullmatch(r"r(\d+)s(\d+):(.*)", nm)
            if not mo:
                specials.append(nm)
                kinds['special'] += 1
                continue
            r = int(mo.group(1))
            fs = factors_of(mo.group(3))
            deg = r + sum(f[3] for f in fs)
            kinds['lin'] += 1
        for f in fs:
            toks[(f[0], f[1], f[2])] += 1
        maxdeg = max(maxdeg, deg)
        if deg > 7:
            over.append((nm, deg))
    print("  multipliers:", n, dict(kinds))
    print("  specials:", specials)
    print("  distinct factor (kind,|S|,bound): counts:", dict(sorted(toks.items())))
    print("  max configuration degree:", maxdeg, " items over 7:", over[:5], len(over))
    print("  min weight w, min scale:", float(np.min(c['w'])), float(np.min(c['scale'])))
