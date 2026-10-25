# Token scan over every source file in the #431 replay closure (all_order_union.txt), comments stripped.
# Prints per-token counts with file names. Positive control: a planted file containing each token must be counted.
import re, os, sys, json
E='/tmp/oaimath/013/ext'
ROOTS={'OAI':'/tmp/oaimath/013/repo/lean','ComparatorChallenges':'/tmp/oaimath/013/repo/lean','PrimeNumberTheoremAnd':E+'/PrimeNumberTheoremAnd','StrongPNT':E+'/StrongPNT','BernoulliRegular':E+'/AINTLIB/projects/FltRegularBernoulli','Common':E+'/AINTLIB/Common'}
TOK={'sorry':r'\bsorry\b','admit':r'\badmit\b','axiom':r'(?m)^\s*(?:private\s+|protected\s+)?axiom\b','native_decide':r'\bnative_decide\b','decide_unsafe':r'Lean\.ofReduceBool|ofReduceBool','implemented_by':r'implemented_by','extern':r'@\[\s*extern|\bextern\b','unsafe':r'\bunsafe\b','opaque':r'(?m)^\s*(?:private\s+)?opaque\b','partial def':r'\bpartial\s+def\b','set_option debug/trust':r'set_option\s+(debug\.|trust)','elab/macro':r'(?m)^\s*(?:syntax|macro|elab|elab_rules|macro_rules)\b','attribute [-instance]':r'attribute\s*\[-'}
def strip(s):
    s=re.sub(r'/-.*?-/','',s,flags=re.S)  # block comments (incl. doc comments)
    s=re.sub(r'--[^\n]*','',s)
    return s
def scan(files):
    hits={k:[] for k in TOK}
    for f in files:
        s=strip(open(f).read())
        for k,r in TOK.items():
            n=len(re.findall(r,s))
            if n: hits[k].append((f,n))
    return hits
mods=[l.strip() for l in open('/tmp/oaimath/013/all_order_union.txt') if l.strip()]
files=[os.path.join(ROOTS[m.split('.')[0]],m.replace('.','/')+'.lean') for m in mods]
assert all(os.path.exists(f) for f in files), 'missing file'
# positive control
ctl='/tmp/oaimath/013/scan/control.lean'
open(ctl,'w').write('theorem t : True := by sorry\nexample : True := by admit\naxiom foo : False\nexample : 2=2 := by native_decide\n@[implemented_by x] def y := 1\n@[extern "c"] def z : Nat := 1\nunsafe def u := 1\nopaque o : Nat\npartial def p : Nat := p\nset_option debug.skipKernelTC true\nsyntax "x" : term\nattribute [-instance] foo in\n-- sorry in a comment must NOT count\n/- axiom in a block comment must not count -/\nexample := Lean.ofReduceBool\n')
c=scan([ctl])
missing=[k for k in TOK if not c[k]]
print('control: tokens not detected:', missing)
commentfalse=[k for k in ('sorry','axiom') if c[k] and c[k][0][1]!=1]
print('control: comment leakage:', commentfalse)
h=scan(files)
print('files scanned:', len(files))
for k,v in h.items():
    print(f'{k}: {sum(n for _,n in v)} in {len(v)} files', [os.path.relpath(f,'/tmp/oaimath/013') for f,_ in v[:6]])
json.dump({k:[(os.path.relpath(f,'/tmp/oaimath/013'),n) for f,n in v] for k,v in h.items()}, open('/tmp/oaimath/013/scan/hits.json','w'), indent=1)
sys.exit(1 if missing or commentfalse else 0)
