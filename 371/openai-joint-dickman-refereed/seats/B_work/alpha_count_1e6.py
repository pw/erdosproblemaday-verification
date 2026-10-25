# exact-integer recount (seat B) of #{2<=n<=X : P(n+1) > P(n)*n^(k/20)}  <=>  P(n+1)^20 > P(n)^20 * n^k, and the mirror
X=10**6; M=X+2
lpf=list(range(M+1))  # largest prime factor via ascending-prime overwrite
lpf=[1]*(M+1)
isp=bytearray([1])*(M+1); isp[0]=isp[1]=0
for p in range(2,M+1):
    if isp[p]:
        for q in range(p*p,M+1,p): isp[q]=0
        for q in range(p,M+1,p): lpf[q]=p
res={}
for k in (1,2,4,6,10):
    up=dn=tie=0
    for n in range(2,X+1):
        a=lpf[n]; b=lpf[n+1]; a20=a**20; b20=b**20; nk=n**k
        if b20>a20*nk: up+=1
        elif b20==a20*nk: tie+=1
        if a20>b20*nk: dn+=1
    print(f"alpha={k/20:.2f} up={up} up/X={up/X:.4f} up/(X-1)={up/(X-1):.4f} mirror={dn} mirror/X={dn/X:.4f} exact_ties={tie}")
