default(parisize, 400000000);
{
countsol(th) =
  my(G, G1, Gz3, Gz4, E1, E2, R, rts, sols, cnt, e1, e2, r4, c, Phi, vals, z3v, z4v, g1);
  G = intformal(t*(t-1)*(t-z3)*(t-z4), t);
  G1 = subst(G, t, 1); Gz3 = subst(G, t, z3); Gz4 = subst(G, t, z4);
  E1 = Gz3*(th[2]-th[1]) - G1*(th[3]-th[1]);
  E2 = Gz4*(th[2]-th[1]) - G1*(th[4]-th[1]);
  R = polresultant(E1, E2, z4);
  rts = polroots(R);
  cnt = 0; sols = List();
  for(i=1, #rts,
    z3v = rts[i];
    e1 = subst(E1, z3, z3v); e2 = subst(E2, z3, z3v);
    \\ find common roots in z4 numerically
    r4 = polroots(e2);
    for(j=1, #r4,
      if(abs(subst(e1, z4, r4[j])) < 1e-15*(1+norml2(Vec(e1)))^(1/2),
        z4v = r4[j];
        \\ conditions: z3,z4 not in {0,1}, distinct, G1 != 0
        g1 = subst(subst(G1, z3, z3v), z4, z4v);
        if(abs(z3v)>1e-8 && abs(z3v-1)>1e-8 && abs(z4v)>1e-8 && abs(z4v-1)>1e-8 && abs(z3v-z4v)>1e-8 && abs(g1)>1e-8,
          c = (th[2]-th[1])/g1;
          Phi = th[1] + c*subst(subst(G, z3, z3v), z4, z4v);
          vals = [subst(Phi,t,0), subst(Phi,t,1), subst(Phi,t,z3v), subst(Phi,t,z4v)];
          if(normlp(vals - th) < 1e-10, listput(sols, [z3v, z4v]))))));
  \\ dedupe
  my(u = List());
  for(i=1,#sols, my(new=1); for(j=1,#u, if(abs(sols[i][1]-u[j][1])+abs(sols[i][2]-u[j][2])<1e-8, new=0)); if(new, listput(u, sols[i])));
  [poldegree(R), #u];
}
print("order (1,i,-1,-i): ", countsol([1, I, -1, -I]));
print("order (1,-1,i,-i): ", countsol([1, -1, I, -I]));
print("generic (0,1,3,7): ", countsol([0, 1, 3, 7]));
print("x^4+2 roots order: ", countsol([2^(1/4), I*2^(1/4), -2^(1/4), -I*2^(1/4)]));
}
