import sys, re, os, json
# strip Lean comments (nested /- -/ incl. doc comments) and string/char literals
def strip(src):
    out=[]; i=0; n=len(src); depth=0
    while i<n:
        c=src[i]
        if depth>0:
            if src.startswith('/-',i): depth+=1; i+=2; out.append('  '); continue
            if src.startswith('-/',i): depth-=1; i+=2; out.append('  '); continue
            out.append('\n' if c=='\n' else ' '); i+=1; continue
        if src.startswith('/-',i): depth=1; i+=2; out.append('  '); continue
        if src.startswith('--',i):
            j=src.find('\n',i); j=n if j<0 else j
            out.append(' '*(j-i)); i=j; continue
        if c=='"':
            j=i+1
            while j<n and src[j]!='"':
                if src[j]=='\\': j+=1
                j+=1
            seg=src[i:j+1]; out.append(''.join('\n' if ch=='\n' else ' ' for ch in seg)); i=j+1; continue
        out.append(c); i+=1
    return ''.join(out)
PATS = {
 'sorry': r'\bsorry\b', 'admit': r'\badmit\b', 'axiom': r'(?<![\w.])axiom\b',
 'native_decide': r'\bnative_decide\b', 'decide_true': r'decide\s*:=\s*true', 'Decidable.decide_kernel': r'\bofReduceBool\b|\bLean\.ofReduceBool\b|\breduceBool\b',
 'implemented_by': r'\bimplemented_by\b', 'extern': r'@\[\s*extern|\bextern\b', 'unsafe': r'\bunsafe\b',
 'csimp': r'\bcsimp\b', 'opaque': r'(?<![\w.])opaque\b', 'partial': r'(?<![\w.])partial\b',
 'macro': r'(?<![\w.])macro(_rules)?\b', 'elab': r'(?<![\w.])elab(_rules)?\b', 'syntax': r'(?<![\w.])syntax\b',
 'initialize': r'(?<![\w.])(builtin_)?initialize\b', 'notation_decl': r'(?<![\w.])(notation|infix|infixl|infixr|prefix|postfix)\b',
 'set_option': r'\bset_option\b', 'skipKernelTC': r'skipKernelTC|debug\.', 'Lean.Elab/Meta import': r'^\s*(public\s+)?import\s+Lean(\.|\s|$)',
 'run_cmd': r'\brun_cmd\b|\brun_tac\b|\brun_elab\b|\brun_meta\b', '#eval': r'#eval\b', 'addDecl': r'\baddDecl\b|\baddAndCompile\b',
 'attribute_global': r'\battribute\s*\[(?!local)[^\]]*\]', 'instance_prio': r'\binstance\s*\(\s*priority', 'export': r'(?<![\w.])export\b',
 'open Lean': r'\bopen\s+(scoped\s+)?Lean\b', '#exit': r'#exit\b', 'Classical_axiom_like': r'\bClassical\.ofNonempty\b|\bClassical\.choice\b',
}
res={}; hits=[]
files=[]
for root in sys.argv[1:]:
    if os.path.isfile(root): files.append(root); continue
    for dp,dn,fn in os.walk(root):
        for f in fn:
            if f.endswith('.lean'): files.append(os.path.join(dp,f))
files.sort()
tot={k:0 for k in PATS}
for f in files:
    src=open(f,encoding='utf-8').read(); s=strip(src)
    lines=s.split('\n'); raw=src.split('\n')
    cnt={}
    for k,p in PATS.items():
        flags=re.M
        c=0
        for li,l in enumerate(lines):
            for m in re.finditer(p,l,flags):
                c+=1; hits.append((f,li+1,k,raw[li].strip()[:160]))
        if c: cnt[k]=c; tot[k]+=c
    res[f]=(len(raw),cnt)
json.dump({'files':{f:{'lines':v[0],'counts':v[1]} for f,v in res.items()},'totals':tot,'hits':hits},sys.stdout,indent=0)
