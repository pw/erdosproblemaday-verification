import re, os, sys
R='/tmp/oaimath/013/repo/lean'
def mods(f): return [l.strip() for l in open(f) if l.strip().startswith('OAI.')]
C=set(mods('/tmp/oaimath/013/closure_OAI.NumberTheory.Ostmann.Complete.txt'))
M=set(mods('/tmp/oaimath/013/closure_OAI.NumberTheory.Ostmann.Main.txt'))
decl=re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s:({\[]+)')
def names(m):
    p=os.path.join(R,m.replace('.','/')+'.lean'); out={}
    ns=[]
    src=re.sub(r'/-.*?-/','',open(p).read(),flags=re.S)
    for line in src.split('\n'):
        line=re.sub(r'--.*','',line)
        mm=re.match(r'^\s*namespace\s+(\S+)',line)
        if mm: ns.append(mm.group(1)); continue
        mm=re.match(r'^\s*end\s+(\S+)\s*$',line)
        if mm and ns and ns[-1]==mm.group(1): ns.pop(); continue
        mm=decl.match(line)
        if mm and mm.group(1)!='instance' and 'private' not in line.split(mm.group(1))[0]:
            n=mm.group(2)
            full=n[len('_root_.'):] if n.startswith('_root_.') else '.'.join(ns+[n])
            out[full]=(mm.group(1),line.strip()[:120])
    return out
Conly=C-M; Monly=M-C
nc={}; 
for m in Conly:
    for k,v in names(m).items(): nc.setdefault(k,[]).append((m,v))
nm={}
for m in Monly:
    for k,v in names(m).items(): nm.setdefault(k,[]).append((m,v))
both=sorted(set(nc)&set(nm))
print('C-only decls',len(nc),'M-only decls',len(nm),'same full name in both',len(both))
for k in both[:25]: print(k, '| C:',nc[k][0][0].split('Ostmann.')[-1], '| M:',nm[k][0][0].split('Ostmann.')[-1], '|', nc[k][0][1][0])
