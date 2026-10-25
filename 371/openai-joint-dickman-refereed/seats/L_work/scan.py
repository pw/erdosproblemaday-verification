import re, os, sys, collections
base='/tmp/oaimath/012'
files=[]
for l in open(base+'/oai_files.txt'):
    l=l.strip()
    if l: files.append(os.path.join(base,'src/oai',l))
for m in open(base+'/seats/L_work/L_nonoai_modules.txt'):
    m=m.strip()
    if not m: continue
    if m.startswith('PrimeNumberTheoremAnd'): p=base+'/src/pnt/'+m.replace('.','/')+'.lean'
    elif m.startswith('StrongPNT'): p=base+'/src/strongpnt/'+m.replace('.','/')+'.lean'
    elif m.startswith('Architect'): p='/tmp/oaimath/024/architect/'+m.replace('.','/')+'.lean'
    else: print('UNMAPPED',m); continue
    files.append(p)
missing=[f for f in files if not os.path.exists(f)]
print('files',len(files),'missing',len(missing),missing[:5])
pats={
 'sorry':r'\bsorry\b','admit':r'\badmit\b','axiom':r'^\s*(private\s+|protected\s+)?axiom\b',
 'native_decide':r'native_decide','implemented_by':r'implemented_by','extern':r'@\[\s*extern|\bextern\b',
 'unsafe':r'\bunsafe\b','csimp':r'csimp','skipKernelTC':r'skipKernelTC','debug.':r'set_option\s+debug\.',
 'opaque':r'^\s*(private\s+)?opaque\b','decide:=true':r'decide\s*:=\s*true','Lean.ofReduceBool':r'ofReduceBool',
 'trustCompiler':r'trustCompiler','macro_rules/elab':r'^\s*(macro_rules|elab_rules|elab|macro)\b',
 'run_cmd/#eval':r'^\s*(run_cmd|run_tac|#eval)\b','maxRecDepth':r'maxRecDepth','maxHeartbeats':r'maxHeartbeats',
 'partial def':r'\bpartial\s+def\b','initialize':r'^\s*(builtin_)?initialize\b','attribute[instance]low':r'xxxxxx',
 'Classical.choice-axiom-decl':r'axiom\s+Classical','set_option pp':r'set_option\s+pp',
}
cnt=collections.Counter(); hits=collections.defaultdict(list)
for f in files:
    if not os.path.exists(f): continue
    txt=open(f,encoding='utf-8').read()
    # strip block comments and line comments for code-level hits
    code=re.sub(r'/-.*?-/','',txt,flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    for k,p in pats.items():
        ms=re.findall(p,code,flags=re.M)
        if ms:
            cnt[k]+=len(ms); hits[k].append((f.replace(base+'/',''),len(ms)))
for k in pats:
    print(f'{k:28s} {cnt[k]:6d}', '' if not hits[k] else hits[k][:8])
