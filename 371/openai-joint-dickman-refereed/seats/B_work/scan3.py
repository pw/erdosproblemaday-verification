import re,collections
base='/tmp/oaimath/012/src/pnt/'
files=['PrimeNumberTheoremAnd/Sobolev.lean','PrimeNumberTheoremAnd/SmoothExistence.lean','PrimeNumberTheoremAnd/Mathlib/Analysis/Asymptotics/Asymptotics.lean']
pats={'sorry':r'\bsorry\b','admit':r'\badmit\b','axiom':r'^\s*(private\s+|protected\s+)?axiom\b','native_decide':r'native_decide','implemented_by':r'implemented_by','extern':r'@\[\s*extern|\bextern\b','unsafe':r'\bunsafe\b','csimp':r'csimp','skipKernelTC':r'skipKernelTC','debug.':r'set_option\s+debug\.','opaque':r'^\s*(private\s+)?opaque\b','ofReduceBool':r'ofReduceBool','trustCompiler':r'trustCompiler','macro/elab':r'^\s*(macro_rules|elab_rules|elab|macro|syntax)\b','run_cmd/#eval':r'^\s*(run_cmd|run_tac|#eval)\b','partial def':r'\bpartial\s+def\b','initialize':r'^\s*(builtin_)?initialize\b'}
for f in files:
    txt=open(base+f,encoding='utf-8').read(); raw=txt
    code=re.sub(r'/-.*?-/','',txt,flags=re.S); code=re.sub(r'--[^\n]*','',code)
    hits={k:len(re.findall(p,code,flags=re.M)) for k,p in pats.items()}
    rawhits={k:len(re.findall(p,raw,flags=re.M)) for k,p in pats.items()}
    print(f, len(raw.splitlines()), {k:v for k,v in hits.items() if v}, 'raw:',{k:v for k,v in rawhits.items() if v})
