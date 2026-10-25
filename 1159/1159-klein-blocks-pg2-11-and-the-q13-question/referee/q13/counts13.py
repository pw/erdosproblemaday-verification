# Count bound for a blocking set S of PG(2,q) with every line meeting S in 1..C points.
# t_i = #lines meeting S in i points. sum t_i = q^2+q+1; sum i t_i = k(q+1); sum i(i-1) t_i = k(k-1).
# sum (i-1)(C-i) t_i >= 0  <=>  -(k^2+qk) + (C+1)k(q+1) - C(q^2+q+1) >= 0.
import sys
q,C=13,4
N=q*q+q+1
ok=[k for k in range(1,N+1) if -(k*k+q*k)+(C+1)*k*(q+1)-C*N>=0]
print('analytic: k^2 -',(C+1)*(q+1)-q,'k +',C*N,'<= 0 ; feasible k range',min(ok),max(ok))
# brute force: does a nonnegative integer (t1..t4) exist for each k?  (finer than the quadratic)
feas=[]
for k in range(1,N+1):
    A=k*(q+1); B=k*(k-1); found=False
    # unknowns t1..t4 >=0: t1+t2+t3+t4=N; t1+2t2+3t3+4t4=A; 2t2+6t3+12t4=B
    for t4 in range(0,N+1):
        for t3 in range(0,N+1-t4):
            r=B-6*t3-12*t4
            if r<0: break
            if r%2: continue
            t2=r//2; t1=N-t2-t3-t4
            if t1<0: continue
            if t1+2*t2+3*t3+4*t4==A: found=True; break
        if found: break
    if found: feas.append(k)
print('integer-feasible k:',min(feas),'..',max(feas),'(count',len(feas),') contiguous:',feas==list(range(min(feas),max(feas)+1)))
# pencil floor at P0 for cube (c1,c2): |S| <= 1 + c1 + (q-1)*c2 (L0 tangent contributes 0)
for c1 in range(1,4):
    for c2 in range(1,c1+1):
        print(f'cube ({c1},{c2}): max |S| = 1+{c1}+{q-1}*{c2} = {1+c1+(q-1)*c2}', 'UNSAT by size floor 20' if 1+c1+(q-1)*c2<20 else '')
