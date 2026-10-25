import os,re,sys
root=sys.argv[1]
files={}
for d,_,fs in os.walk(os.path.join(root,'Erdos128')):
    for f in fs:
        if f.endswith('.lean'):
            p=os.path.join(d,f); mod=os.path.relpath(p,root)[:-5].replace('/','.')
            files[mod]=p
imp={}
ext=set()
for m,p in files.items():
    s=open(p).read()
    ims=re.findall(r'^\s*(?:public\s+)?import\s+([A-Za-z0-9_.]+)',s,re.M)
    imp[m]=ims
seen=set(); stack=['Erdos128.ModuloBCL']
while stack:
    m=stack.pop()
    if m in seen: continue
    seen.add(m)
    for i in imp.get(m,[]):
        if i in files: stack.append(i)
        else: ext.add(i)
print('total Erdos128 files',len(files))
print('transitive closure of ModuloBCL (incl itself)',len(seen))
print('not reached:',sorted(set(files)-seen))
print('external imports:',sorted(ext))
