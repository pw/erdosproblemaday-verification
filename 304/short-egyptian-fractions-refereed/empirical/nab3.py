src=open('nab.py').read().split('B=int(sys.argv[1])')[0]
ns={}; exec(src,ns); N=ns['N']
first={}
for b in range(2,740):
    x=N(b-1,b)
    if x not in first: first[x]=b
print('first b with N(b-1,b)=k:',first)
