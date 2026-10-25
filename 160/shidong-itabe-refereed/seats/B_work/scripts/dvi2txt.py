import sys
data=open(sys.argv[1],'rb').read()
i=0; out=[]
def u(n):
    global i
    v=int.from_bytes(data[i:i+n],'big'); i+=n; return v
def s(n):
    global i
    v=int.from_bytes(data[i:i+n],'big',signed=True); i+=n; return v
h=0; stack=[]; w=x=y=z=0; v=0; lastv=None; line=[]; lasth=None
fonts={}; cur=None
def emit(c):
    global lasth
    line.append(c)
while i < len(data):
    op=data[i]; i+=1
    if op<=127:
        if lasth is not None and h-lasth>150000: line.append(' ')
        line.append(chr(op) if 32<=op<127 else '?'); h+=0; lasth=h+300000  # approx width
        h+=300000
    elif 128<=op<=131: c=u(op-127); line.append('?'); h+=300000
    elif op==132: s(4); s(4)
    elif 133<=op<=136: u(op-132)
    elif op==137: s(4); s(4)
    elif op==138: pass
    elif op==139:
        i+=44; h=v=w=x=y=z=0; stack=[]; out.append('\n\f\n')
    elif op==140: out.append(''.join(line)); line=[]
    elif op==141: stack.append((h,v,w,x,y,z))
    elif op==142: h,v,w,x,y,z=stack.pop()
    elif 143<=op<=146: d=s(op-142); h+=d; 
    elif op==147: h+=w
    elif 148<=op<=151: w=s(op-147); h+=w
    elif op==152: h+=x
    elif 153<=op<=156: x=s(op-152); h+=x
    elif 157<=op<=160: d=s(op-156); v+=d
    elif op==161: v+=y
    elif 162<=op<=165: y=s(op-161); v+=y
    elif op==166: v+=z
    elif 167<=op<=170: z=s(op-166); v+=z
    elif 171<=op<=234: cur=op-171
    elif 235<=op<=238: cur=u(op-234)
    elif 239<=op<=242: k=u(op-238); i+=k
    elif 243<=op<=246: u(op-242); i+=12; a=data[i]; l=data[i+1]; i+=2+a+l
    elif op==247: i+=1+12; k=data[i]; i+=1+k
    elif op==248: break
    else: break
    if lastv is None: lastv=v
    if v-lastv>200000 or v<lastv-200000:
        line.append('\n'); lastv=v; lasth=None
print(''.join(out))
