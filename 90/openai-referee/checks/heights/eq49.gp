\\ (4.9): 2 E h(d_e/d_e') = E sum* |n_e - n_e'| = 2 int pi(1-pi)  (<= 2S), on a toy edge-jump law in Q(i).
default(realprecision, 50);
nf = nfinit(x^2 + 1); d = 2;
nrm(u) = lift(Mod(numerator(u), nf.pol) / Mod(denominator(u), nf.pol));
hpl(u) =
{
  my(c, s, fa, pr);
  u = nrm(u); if(u == 0, return(0));
  c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, max(0, log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; s += pr.e*pr.f * max(0, -fa[k,2]/pr.e * log(pr.p)) / d);
  s
}
J = [1 + 2*x, (3 + 4*x)/5, 2, 1/(1 + x), 7*x/(2 - x), 3, (1 - x)/5, 11 + 0*x];
J = vector(#J, k, nrm(J[k])); m = #J;
\\ places: 2 embeddings (weight 1/2 each) + primes dividing some d_e (weight e*f/2)
P = []; { for(k = 1, m, my(fa = idealfactor(nf, J[k])); for(j = 1, #fa~, my(pr = fa[j,1], new = 1);
      for(i = 1, #P, if(P[i].p == pr.p && idealval(nf, pr.gen[2], P[i]) > 0 && P[i].e == pr.e && P[i].f == pr.f && idealhnf(nf, P[i]) == idealhnf(nf, pr), new = 0));
      if(new, P = concat(P, [pr])))); }
\\ n_e(v) table
nv(k, v) = if(v <= 2, -log(abs(conjvec(Mod(J[k], nf.pol))[v])), my(pr = P[v - 2]); idealval(nf, J[k], pr) * log(pr.p) / pr.e);
wt(v) = if(v <= 2, 1/d, my(pr = P[v - 2]); pr.e*pr.f/d);
\\ exact integral of pi(1-pi) over s, pi(s) = #{n_e > s}/m, piecewise constant between sorted values
ipi(vals) = { my(sv = vecsort(vals), tot = 0, cnt); for(j = 1, #sv - 1, cnt = #select(t -> t > sv[j], sv); tot += (cnt/m)*(1 - cnt/m)*(sv[j+1] - sv[j])); tot };
ifm(vals) = { my(sv = vecsort(vals), tot = 0, cnt); for(j = 1, #sv - 1, cnt = #select(t -> t > sv[j], sv); tot += min(cnt/m, 1 - cnt/m)*(sv[j+1] - sv[j])); tot };
{
  my(nV = 2 + #P, lhs, mid, rhs, S);
  lhs = 2 * sum(a = 1, m, sum(b = 1, m, hpl(J[a]/J[b]))) / m^2;
  mid = sum(a = 1, m, sum(b = 1, m, sum(v = 1, nV, wt(v) * abs(nv(a, v) - nv(b, v))))) / m^2;
  rhs = 2 * sum(v = 1, nV, wt(v) * ipi(vector(m, k, nv(k, v))));
  S = sum(v = 1, nV, wt(v) * ifm(vector(m, k, nv(k, v))));
  print("primes used: ", vector(#P, i, [P[i].p, P[i].e, P[i].f]));
  print("2E h(d/d')            = ", lhs);
  print("E sum*|n_e - n_e'|     = ", mid);
  print("2 int pi(1-pi)        = ", rhs);
  print("2S                    = ", 2*S, "   (4.9) chain holds: ", abs(lhs-mid) < 1e-30 && abs(mid-rhs) < 1e-30 && rhs <= 2*S + 1e-30);
  print("CONTROL: 2 int min(pi,1-pi) = 2S differs from 2E h: ", 2*S - lhs, "  (the equality is with pi(1-pi), only an inequality with f)");
}
