default(parisize, 1000000000);
p = 2^61-1;
rnd() = Mod(random(p-1)+1, p);
monsw(h, U, V, N) = { my(L=List()); forvec(v=vector(2*h,i,[0,N]), my(w=U*vecsum(v[1..h])+V*vecsum(v[h+1..2*h])); if(w<=N, listput(L,v))); Vec(L); }
mon(x, e) = prod(i=1,#e, x[i]^e[i]);
rk(pts, E) = { my(M=matrix(#pts,#E)); for(r=1,#pts, for(c=1,#E, M[r,c]=mon(pts[r],E[c]))); matrank(M); }
series_cum(h, U, V, Q, Ee, N) = { my(s = (1-x^Q)^(h-1)*(1-x^Ee)/((1-x)*(1-x^U)^h*(1-x^V)^h) + O(x^(N+1))); polcoef(s, N); }
th = [Mod(1,p), Mod(2,p), Mod(3,p), Mod(5,p)];
k = 2;
\\ Ex1: h=2, F1 = a2 (n - th1) + a1^3 ; D = U+V
ptE1() = my(a1=rnd(), a2=rnd(), n); n = th[1] - a1^3/a2; [a1, a2, (n-th[1])/a1^2, (n-th[2])/a2^2];
\\ Ex2: h=2, F1 = a1 a2 - n ; D = 2U+V
ptE2() = my(a1=rnd(), a2=rnd(), n); n = a1*a2; [a1, a2, (n-th[1])/a1^2, (n-th[2])/a2^2];
\\ Ex3: h=3, F1 = a3 (n-th1)(n-th2) + a1^2 a2 ; D = 2U+2V
ptE3() = my(a1=rnd(), a2=rnd(), n=rnd(), a3); a3 = -a1^2*a2/((n-th[1])*(n-th[2])); [a1,a2,a3,(n-th[1])/a1^2,(n-th[2])/a2^2,(n-th[3])/a3^2];
{
foreach([[1,1],[1,2],[2,1],[2,3],[3,2]], UV,
  my(U=UV[1], V=UV[2]);
  foreach([[2, ptE1, U+V, 3*U+V, "E1"], [2, ptE2, 2*U+V, 2*U+V, "E2"], [3, ptE3, 2*U+2*V, 5*U+2*V, "E3"]], ex,
    my(h=ex[1], f=ex[2], D=ex[3], naive=ex[4], Nmax = if(h==2, 12, 7), bad=0, out=List());
    if(h==3 && max(U,V)>1, Nmax = 10);
    if(h==2 && max(U,V)>1, Nmax = 18);
    for(N=1, Nmax,
      my(E=monsw(h,U,V,N), pts=vector(#E+15,i,f()), r=rk(pts,E), s=series_cum(h,U,V,k*U+V,D,N), sn=series_cum(h,U,V,k*U+V,naive,N));
      listput(out, [N, r, s, sn]); if(r!=s, bad++));
    print(ex[5], " U,V=", UV, " D=", D, " mismatches=", bad, "  last [N,evalrank,series(D),series(naive)]=", out[#out])));
}
