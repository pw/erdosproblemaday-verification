import re,sys,os,collections,json
def strip(text):
    # remove nested block comments /- -/ (incl doc comments), line comments, string literals
    out=[];i=0;n=len(text);depth=0
    res=[]
    while i<n:
        if text.startswith('/-',i):
            depth+=1;i+=2;continue
        if depth>0:
            if text.startswith('-/',i): depth-=1;i+=2;continue
            res.append('\n' if text[i]=='\n' else ' ');i+=1;continue
        if text.startswith('--',i):
            j=text.find('\n',i); j=n if j<0 else j
            res.append(' '*(j-i)); i=j; continue
        if text[i]=='"':
            j=i+1
            while j<n and text[j]!='"':
                if text[j]=='\\': j+=1
                j+=1
            res.append('"'+' '*(j-i-1)+'"'); i=j+1; continue
        res.append(text[i]); i+=1
    return ''.join(res)
PATS=[
 ('sorry',r'\bsorry\b'),('admit',r'\badmit\b'),('axiom-decl',r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+)?axiom\b'),
 ('native_decide',r'\bnative_decide\b'),('ofReduceBool',r'ofReduceBool|reduceBool'),('implemented_by',r'implemented_by'),
 ('extern',r'@\[\s*extern|\bextern\b'),('unsafe',r'\bunsafe\b'),('opaque',r'^\s*(?:private\s+)?opaque\b'),('partial',r'\bpartial\s+def\b'),
 ('csimp',r'csimp'),('set_option',r'\bset_option\b'),('skipKernelTC',r'skipKernelTC|debug\.'),('import Lean',r'^\s*(?:public\s+)?import\s+Lean\b'),
 ('elab',r'^\s*(?:@\[[^\]]*\]\s*)?(?:local\s+|scoped\s+)?elab(?:_rules)?\b'),('macro',r'^\s*(?:@\[[^\]]*\]\s*)?(?:local\s+|scoped\s+)?macro(?:_rules)?\b'),('syntax',r'^\s*(?:local\s+|scoped\s+)?syntax\b'),
 ('notation',r'^\s*(?:local\s+|scoped\s+)?(?:notation|infix|infixl|infixr|prefix|postfix)\b'),
 ('run_cmd/#eval',r'\brun_cmd\b|\brun_tac\b|#eval|\binitialize\b|builtin_initialize'),('addDecl',r'addDecl|Kernel\.|Environment\.add|unsafeCast|ofExcept'),
 ('decide',r'\bdecide\b'),('instance-dist',r'instance[^\n:]*:[^\n]*(?:Dist|MetricSpace|PseudoMetricSpace|Norm\b|NormedAddCommGroup|InnerProductSpace|EuclideanSpace)'),
 ('Classical.choice-axiom-name',r'\baxiom\b'),
]
def scan(files,root):
    hits=collections.defaultdict(list)
    for f in files:
        t=open(f,encoding='utf-8',errors='replace').read()
        s=strip(t).split('\n'); raw=t.split('\n')
        for k,p in PATS:
            rx=re.compile(p)
            for i,l in enumerate(s):
                if rx.search(l): hits[k].append((os.path.relpath(f,root),i+1,raw[i].strip()[:160] if i<len(raw) else ''))
    return hits
if __name__=='__main__':
    root=sys.argv[1]; files=[]
    for dp,dn,fn in os.walk(root):
        if '.git' in dp: continue
        for x in fn:
            if x.endswith('.lean'): files.append(os.path.join(dp,x))
    h=scan(sorted(files),root)
    print('files',len(files))
    for k,_ in PATS: print(f'{k:28s} {len(h[k])}')
    json.dump(h,open(sys.argv[2],'w'),indent=0)
