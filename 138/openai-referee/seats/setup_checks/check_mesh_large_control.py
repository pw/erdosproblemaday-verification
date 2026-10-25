# CONTROL for check_mesh_large.py: identical checker (window_check imported from it), mesh built with
# m' = ceil(k R) (theta ~ 1/k: WRONG growth rate) -- MUST report violations.
# Second run (EXPECTED TO PASS): alpha replaced by alpha' = 1e-3. Lemmas mesh:width/mesh:neighbors use only
# alpha <= 1/4; the size of alpha matters only later (dichotomy:step-lattice needs alpha <= q^-D).
import importlib.util, sys, mpmath
spec = importlib.util.spec_from_file_location("cml", "/tmp/oaimath/160/seats/setup_checks/check_mesh_large.py")
src = open("/tmp/oaimath/160/seats/setup_checks/check_mesh_large.py").read()
src = src[:src.index("for k in [1025")]          # import definitions only, not the main loop
ns = {}; exec(compile(src, "cml_defs", "exec"), ns)
for k in [1025, 10**6]:
    pr = ns['params'](k)
    bad = dict(pr); bad['m'] = int(mpmath.ceil(k*pr['R'])); bad['theta'] = pr['R']/bad['m']
    res = [ns['window_check'](bad, 0, 200, 'cut'), ns['window_check'](bad, bad['m']-200, bad['m']-1, 'zero')]
    print("CONTROL wrong growth k=%d: viol=%d (must be > 0), ratio max=%s" % (k, sum(r[1] for r in res), mpmath.nstr(max(r[3] for r in res), 5)))
    alt = dict(pr); alt['alpha'] = mpmath.mpf(1)/1000; alt['R'] = mpmath.log(1 + 1/(2*alt['alpha'])); alt['m'] = int(mpmath.ceil(mpmath.mpf(k)**2*alt['R'])); alt['theta'] = alt['R']/alt['m']
    res = [ns['window_check'](alt, 0, 200, 'cut'), ns['window_check'](alt, alt['m']-200, alt['m']-1, 'zero')]
    print("alpha'=1e-3 k=%d: viol=%d (expected 0: widths/neighbours hold for ANY alpha<=1/4)" % (k, sum(r[1] for r in res)))
