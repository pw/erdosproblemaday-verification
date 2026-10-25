import re, sys, os, json
SRC = '/tmp/oaimath/191b/src/blinov-fpc/lean'
def imports(mod):
    txt = open(os.path.join(SRC, mod + '.lean')).read()
    # strip block comments /- ... -/ and line comments before scanning imports (a leading licence comment must not stop the scan)
    txt = re.sub(r'/-.*?-/', '', txt, flags=re.S)
    txt = re.sub(r'--[^\n]*', '', txt)
    out = []
    for line in txt.split('\n'):
        s = line.strip()
        if not s: continue
        m = re.match(r'import\s+(.*)', s)
        if m: out += m.group(1).split(); continue
        break   # first non-import, non-blank line ends the header
    return out
targets = sys.argv[1:]
local = {f[:-5] for f in os.listdir(SRC) if f.endswith('.lean')}
order, seen, ext = [], set(), set()
def visit(m):
    if m in seen: return
    seen.add(m)
    for i in imports(m):
        if i in local: visit(i)
        else: ext.add(i)
    order.append(m)
for t in targets: visit(t)
json.dump({'order': order, 'deps': {m: [i for i in imports(m) if i in local] for m in order}, 'external': sorted(ext)}, open('closure.json', 'w'), indent=1)
print(len(order), 'local modules;', len(ext), 'external imports:', ' '.join(sorted(ext)[:12]), '...' if len(ext) > 12 else '')
print(' '.join(order))
