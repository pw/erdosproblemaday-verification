import re,glob,os,sys
d=sys.argv[1]
src={}
for f in glob.glob(os.path.join(d,'*.lean')): src[os.path.basename(f)]=open(f).read()
allt='\n'.join(src.values())
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private |protected )?(?:noncomputable )?(theorem|lemma|def|abbrev)\s+([A-Za-z_][\w.\'!?₀-₉]*)',re.M)
dead=[]
for f,t in src.items():
    for m in decl.finditer(t):
        n=m.group(2); short=n.split('.')[-1]
        cnt=len(re.findall(r'(?<![\w.])'+re.escape(short)+r'(?![\w\'₀-₉])',allt))
        if cnt<=1: dead.append((f,t[:m.start()].count('\n')+1,m.group(1),n))
print(len(dead))
for x in sorted(dead): print(x)
