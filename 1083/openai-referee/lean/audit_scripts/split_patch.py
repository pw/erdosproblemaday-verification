import re,sys,os
src=sys.argv[1]; out=sys.argv[2]
txt=open(src,encoding='utf-8',errors='replace').read()
parts=re.split(r'^(?=diff --git )',txt,flags=re.M)
for p in parts:
    m=re.match(r'diff --git a/(\S+) b/(\S+)',p)
    if not m: continue
    path=m.group(2)
    new='new file mode' in p.split('\n@@')[0]
    # collect added lines for new files
    if new:
        lines=[]
        for l in p.split('\n'):
            if l.startswith('+++') : continue
            if l.startswith('+'): lines.append(l[1:])
        dest=os.path.join(out,path)
        os.makedirs(os.path.dirname(dest),exist_ok=True)
        open(dest,'w').write('\n'.join(lines)+'\n')
    add=sum(1 for l in p.split('\n') if l.startswith('+') and not l.startswith('+++'))
    rem=sum(1 for l in p.split('\n') if l.startswith('-') and not l.startswith('---'))
    print(('NEW ' if new else 'MOD '),path,'+%d -%d'%(add,rem))
