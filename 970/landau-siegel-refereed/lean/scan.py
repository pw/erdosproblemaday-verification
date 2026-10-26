# Comment-stripped textual scan of the 67-module closure for instance/notation/macro/elab and soundness escapes.
import re, sys, os
cl=[l.strip() for l in open('/tmp/oaimath/003/lean/closure_DRZB.txt') if l.strip()]
def path(m):
    if m.startswith('OAI.'): return '/tmp/oaimath/013/repo/lean/'+m.replace('.','/')+'.lean'
    if m.startswith('PrimeNumberTheoremAnd.'): return '/tmp/oaimath/013/ext/PrimeNumberTheoremAnd/'+m.replace('.','/')+'.lean'
    raise SystemExit('unknown root '+m)
def strip(src):
    # remove nested block comments /- ... -/ (incl doc comments) and line comments --, respecting string literals
    out=[];i=0;n=len(src);depth=0;instr=False
    while i<n:
        c=src[i]
        if depth==0 and not instr and c=='"':
            instr=True; out.append(c); i+=1; continue
        if instr:
            out.append(c)
            if c=='\\' and i+1<n: out.append(src[i+1]); i+=2; continue
            if c=='"': instr=False
            i+=1; continue
        if src.startswith('/-',i):
            depth+=1; i+=2; continue
        if depth>0 and src.startswith('-/',i):
            depth-=1; i+=2; continue
        if depth>0:
            out.append('\n' if c=='\n' else ' '); i+=1; continue
        if src.startswith('--',i):
            j=src.find('\n',i); j=n if j<0 else j
            out.append(' '*(j-i)); i=j; continue
        out.append(c); i+=1
    return ''.join(out)
PATS=[('instance',r'\binstance\b'),('attribute_instance',r'attribute\s*\[[^\]]*\binstance\b'),('default_instance',r'default_instance'),
('macro',r'\bmacro\b'),('macro_rules',r'\bmacro_rules\b'),('syntax',r'\bsyntax\b'),('notation',r'\bnotation\b'),
('infix',r'\binfix[lr]?\b'),('prefix',r'\bprefix\b'),('postfix',r'\bpostfix\b'),('elab',r'\belab(_rules)?\b'),('unif_hint',r'\bunif_hint\b'),
('axiom',r'\baxiom\b'),('sorry',r'\bsorry\b'),('admit',r'\badmit\b'),('opaque',r'\bopaque\b'),('implemented_by',r'implemented_by'),
('extern',r'\bextern\b'),('unsafe',r'\bunsafe\b'),('native_decide',r'native_decide'),('ofReduceBool',r'ofReduceBool'),('reduceBool',r'reduceBool'),
('decide_kernel',r'decide\s*\+\s*kernel|Decidable\.decide.*kernel|kernel\s*:=\s*true'),('debug_skipKernelTC',r'skipKernelTC'),('set_option',r'\bset_option\b'),
('local_instance_attr',r'attribute\s*\[\s*local\s+instance'),('coe_attr',r'@\[[^\]]*\bcoe\b'),('CoeFun_etc',r'\b(Coe|CoeTail|CoeHead|CoeOut|CoeFun|CoeSort|CoeDep|CoeHTCT|NatCast|IntCast|HMul|HAdd|HSub|LE|LT|Mul|Add|Sub|Neg|One|Zero|OfNat)\b\s'),
('run_cmd',r'\b(run_cmd|run_tac|run_elab|run_meta)\b'),('initialize',r'\b(initialize|builtin_initialize)\b'),('open_private',r'open\s+private'),('export',r'^\s*export\b'),
('Lean_Elab_import',r'^\s*import\s+Lean\b'),('local_notation',r'local\s+notation'),('scoped',r'\bscoped\b'),('noncomputable_instance',r'noncomputable\s+instance'),
('irreducible_def',r'irreducible_def'),('csimp',r'@\[[^\]]*csimp'),('simproc',r'\bsimproc\b'),('dsimproc',r'\bdsimproc\b'),('binop',r'binop%|binrel%|unop%'),
('instance_priority',r'instance\s*\(priority')]
hits=[]
for m in cl:
    p=path(m); s=strip(open(p).read())
    lines=s.split('\n'); raw=open(p).read().split('\n')
    for ln,(L,R) in enumerate(zip(lines,raw),1):
        for name,pat in PATS:
            if re.search(pat,L):
                hits.append((name,m,ln,R.strip()[:200]))
from collections import Counter
cnt=Counter(h[0] for h in hits)
with open('scan.txt','w') as f:
    f.write('# Comment-stripped scan of %d closure modules (closure_DRZB.txt). Counts:\n'%len(cl))
    for k,_ in PATS: f.write('%-22s %d\n'%(k,cnt.get(k,0)))
    f.write('\n# All hits (pattern | module | line | raw text)\n')
    for h in hits: f.write('%s | %s:%d | %s\n'%h)
print(open('scan.txt').read()[:3000])
