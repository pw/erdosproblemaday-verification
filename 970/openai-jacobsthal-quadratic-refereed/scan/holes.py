import re,sys,collections
files=open('files.txt').read().split()
def strip(src):
    out=[];i=0;n=len(src);depth=0
    while i<n:
        if depth>0:
            if src.startswith('/-',i): depth+=1;i+=2
            elif src.startswith('-/',i): depth-=1;i+=2
            else:
                if src[i]=='\n': out.append('\n')
                i+=1
        else:
            if src.startswith('/-',i): depth=1;i+=2
            elif src.startswith('--',i):
                j=src.find('\n',i)
                if j<0:j=n
                i=j
            elif src[i]=='"':
                # string literal
                j=i+1
                while j<n and src[j]!='"':
                    if src[j]=='\\': j+=1
                    j+=1
                out.append('""'); 
                out.append('\n'*src[i:j+1].count('\n'))
                i=j+1
            else:
                out.append(src[i]);i+=1
    return ''.join(out)
pats={
 'sorry':r'\bsorry\b','admit':r'\badmit\b','axiom':r'\baxiom\b','native_decide':r'\bnative_decide\b',
 'implemented_by':r'\bimplemented_by\b','extern':r'@\[[^\]]*\bextern\b','unsafe':r'\bunsafe\b','opaque':r'\bopaque\b',
 'skipKernelTC':r'skipKernelTC','ofReduceBool':r'ofReduceBool','decide:=true':r'decide\s*:=\s*true',
 'reduceBool':r'reduceBool','partial':r'\bpartial\b','noncomputable':r'\bnoncomputable\b',
 'sorryAx':r'sorryAx','trustCompiler':r'trustCompiler','macro/elab':r'^\s*(macro|elab|syntax|macro_rules|elab_rules|declare_syntax_cat|initialize|builtin_initialize)\b',
 'run_cmd/#eval':r'^\s*(run_cmd|#eval|run_elab|run_meta)\b',
 'attribute simp/instance globals':r'^\s*attribute\s*\[(?!local)[^\]]*instance',
 'set_option':r'\bset_option\b','unif_hint':r'unif_hint',
 'Classical.choice-skip':r'XXXX',
}
cnt={k:collections.Counter() for k in pats}
hits={k:[] for k in pats}
setopts=collections.Counter()
setopt_lines=[]
for f in files:
    src=open(f,encoding='utf8').read()
    s=strip(src)
    root=f.split('/')
    pk='OAI' if '/repo/lean/' in f else f.split('/ext/')[1].split('/')[0]
    for k,p in pats.items():
        for m in re.finditer(p,s,flags=re.M):
            cnt[k][pk]+=1
            ln=s.count('\n',0,m.start())+1
            if len(hits[k])<400: hits[k].append((f,ln,s.splitlines()[ln-1].strip()[:140]))
    for m in re.finditer(r'set_option\s+(\S+)\s+(\S+)',s):
        setopts[(m.group(1),m.group(2),pk)]+=1
for k in pats:
    tot=sum(cnt[k].values())
    print(f'{k:35s} total={tot:6d}  '+', '.join(f'{p}:{c}' for p,c in sorted(cnt[k].items())))
print()
for k in ['sorry','admit','axiom','native_decide','implemented_by','extern','unsafe','opaque','skipKernelTC','ofReduceBool','decide:=true','reduceBool','sorryAx','trustCompiler','partial','macro/elab','run_cmd/#eval','attribute simp/instance globals','unif_hint']:
    if hits[k]:
        print('==',k,len(hits[k]))
        for h in hits[k][:30]: print('  ',h[0].replace('/tmp/oaimath/021/',''),h[1],h[2])
print()
print('set_option census:')
for (o,v,pk),c in sorted(setopts.items(),key=lambda x:(x[0][0],x[0][2],x[0][1])):
    print(f'  {o} {v} [{pk}] x{c}')
