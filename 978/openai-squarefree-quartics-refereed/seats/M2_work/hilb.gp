default(parisize, 1000000000);
p = 2^61-1;
rnd() = Mod(random(p-1)+1, p);
\\ list of exponent vectors of total degree D in n vars
expo(n, D) = { my(L=List()); forvec(v=vector(n,i,[0,D]), if(vecsum(v)==D, listput(L, v))); Vec(L); }
expole(n, D) = { my(L=List()); forvec(v=vector(n,i,[0,D]), if(vecsum(v)<=D, listput(L, v))); Vec(L); }
mon(x, e) = prod(i=1,#e, x[i]^e[i]);
\\ Hilbert series coefficient for bigraded CI: gens bidegrees list G, d vars each block
hscoef(d, G, A, B) = {
  my(s=0, m=#G);
  forvec(S=vector(m,i,[0,1]),
    my(a=A, b=B); for(i=1,m, if(S[i], a-=G[i][1]; b-=G[i][2]));
    if(a>=0 && b>=0, s += (-1)^vecsum(S) * binomial(a+d-1,d-1)*binomial(b+d-1,d-1)));
  s;
}
\\ points on bicone (d,k) with thetas th; optional constraint F solver
bicone_pt(d,k,th) = { my(a=vector(d,i,rnd()), N=rnd(), L=rnd()); [a, vector(d,i,(N-th[i]*L)/a[i]^k)]; }
evalrank(pts, ea, eb) = {
  my(M = matrix(#pts, #ea*#eb));
  for(r=1,#pts, my(c=0, pa=vector(#ea,i,mon(pts[r][1],ea[i])), pb=vector(#eb,j,mon(pts[r][2],eb[j])));
    for(i=1,#ea, for(j=1,#eb, c++; M[r,c] = pa[i]*pb[j])));
  matrank(M);
}
{
\\ Lemma 5.1 checks
foreach([], dt,
  my(d=dt[1], th=dt[2], k=d-2);
  foreach(if(d==4, [[2,1],[4,2],[6,3],[3,3],[8,2],[2,4]], [[4,2],[3,3],[5,1]]), AB,
    my(A=AB[1], B=AB[2], ea=expo(d,A), eb=expo(d,B), npts=#ea*#eb+20, pts, r, h);
    pts = vector(npts, i, bicone_pt(d,k,th));
    r = evalrank(pts, ea, eb);
    h = hscoef(d, vector(d-2,i,[k,1]), A, B);
    print("bicone d=",d," (A,B)=",AB," evalrank=",r," CIseries=",h, if(r==h," OK"," MISMATCH"))));
}
thF=[1,2,3,5];
ptF() = my(a=vector(4,i,rnd()), L=rnd(), N); N = thF[1]*L - a[1]^3*L/a[2]^3; [a, vector(4,i,(N-thF[i]*L)/a[i]^2)];
{
my(d=4,k=2);
foreach([[3,1],[5,2],[6,3],[4,3],[8,2]], AB,
  my(A=AB[1], B=AB[2], ea=expo(d,A), eb=expo(d,B), pts, r, h);
  pts = vector(#ea*#eb+20, i, ptF());
  r = evalrank(pts, ea, eb);
  h = hscoef(d, [[2,1],[2,1],[3,1]], A, B);
  print("cut F d=4 (A,B)=",AB," evalrank=",r," CIseries=",h, if(r==h," OK"," MISMATCH")));
\\ same with naive (unsaturated) bidegree (5,1) for comparison
foreach([[5,2],[6,3]], AB, print("  naive (5,1) series at ",AB,": ", hscoef(d, [[2,1],[2,1],[5,1]], AB[1], AB[2])));
}
