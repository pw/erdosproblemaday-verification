import re,os,sys,glob
d=sys.argv[1]
decl=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private |protected )?(?:noncomputable )?(theorem|lemma|def|abbrev|instance|structure|class|inductive)\s+([^\s(:{\[]+)?')
rows=[];kinds={}
for f in sorted(glob.glob(os.path.join(d,'*.lean'))):
    L=open(f).read().split('\n')
    starts=[]
    for i,l in enumerate(L):
        m=decl.match(l)
        if m: starts.append((i,m.group(1),m.group(2) or '?'))
    for j,(i,k,n) in enumerate(starts):
        end=starts[j+1][0] if j+1<len(starts) else len(L)
        # trim trailing 'end' lines
        rows.append((end-i,os.path.basename(f),i+1,k,n))
        kinds[k]=kinds.get(k,0)+1
rows.sort(reverse=True)
print('kinds',kinds,'total decls',len(rows))
for r in rows[:15]: print(r)
