\\ Lemma 4.1 / 4.2 checks: weighted places (n_p copies of weight 1/d) and the absolute height.
default(realprecision, 60);
nrm(nf, u) = lift(Mod(numerator(u), nf.pol) / Mod(denominator(u), nf.pol));
\\ weighted sum of log|u|_v ; mode 0 = paper's normalisation,
\\ mode 1 = CONTROL (genuine |.|_p once per prime, weight 1/d), mode 2 = CONTROL (squared modulus at every embedding)
wsum(nf, u, mode) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, if(mode == 2, 2, 1) * log(abs(c[k]))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += if(mode == 1, 1, pr.e*pr.f) * (-ord/pr.e) * log(pr.p) / d);
  s
}
hplaces(nf, u) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); if(u == 0, return(0));
  c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, max(0, log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += pr.e*pr.f * max(0, (-ord/pr.e) * log(pr.p)) / d);
  s
}
habs(nf, u) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, abs(log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += pr.e*pr.f * abs((-ord/pr.e) * log(pr.p)) / d);
  s
}
\\ independent height: log Mahler measure of primitive integer minimal polynomial / degree
hmahler(nf, u) =
{
  my(f, g, r);
  u = nrm(nf, u); f = minpoly(Mod(u, nf.pol));
  g = f * denominator(content(f)); g = g / content(g); r = polroots(g);
  (log(abs(pollead(g))) + sum(k = 1, #r, max(0, log(abs(r[k]))))) / poldegree(g)
}
report(name, nf, L) =
{
  print("== ", name, "   pol = ", nf.pol, "   d_N = ", poldegree(nf.pol));
  for(k = 1, #L,
    my(u = L[k], ui = 1/L[k]);
    printf("u=%-18s sum*log|u|_v=% .1e | CTRL once/prime=% .4f CTRL sq.mod=% .4f | h_places=%.10f h_Mahler=%.10f diff=% .0e | h(1/u)-h(u)=% .0e | sum*|log|u|_v|-2h=% .0e\n",
      Str(u), wsum(nf,u,0), wsum(nf,u,1), wsum(nf,u,2), hplaces(nf,u), hmahler(nf,u),
      hplaces(nf,u)-hmahler(nf,u), hplaces(nf,ui)-hplaces(nf,u), habs(nf,u)-2*hplaces(nf,u)));
}
QI = nfinit(x^2 + 1);
report("Q(i)", QI, [1 + 2*x, 3, (1 + x)/3, 5/(2 + x), 7, (3 + 4*x)/5, 2, 1 + x, 12/(5 + 12*x), 13*x/(4 - x)]);
QS = nfinit(x^2 - 2);
report("Q(sqrt2)", QS, [1 + x, 3 + 2*x, (1 + x)/7, x/3, 5, (x - 1)/(x + 3)]);
Q8 = nfinit(x^4 + 1);
\\ in Q(zeta8): i = x^2, sqrt2 = x - x^3
report("Q(zeta8)", Q8, [1 + 2*x^2, 3, 7, (3 + 4*x^2)/5, 1 + x - x^3, 3 + 2*(x - x^3), (1 + x - x^3)/7]);
print("field independence: h(1+2i): Q(i) - Q(zeta8) = ", hplaces(QI, 1 + 2*x) - hplaces(Q8, 1 + 2*x^2), ";   h(1+sqrt2): Q(sqrt2) - Q(zeta8) = ", hplaces(QS, 1 + x) - hplaces(Q8, 1 + x - x^3));
rnd(nf) =
{
  my(d = poldegree(nf.pol), w = 0);
  while(w == 0, w = sum(k = 0, d - 1, (random(21) - 10) * x^k) / (1 + random(9)));
  w
}
{
  my(ok = 1, wa = -1e9, wm = -1e9);
  setrand(167);
  for(it = 1, 300,
    my(nf = if(it % 2, QI, Q8), a = rnd(nf), b = rnd(nf), ha, hb, m, s);
    ha = hplaces(nf, a); hb = hplaces(nf, b);
    m = hplaces(nf, a*b) - ha - hb;
    s = hplaces(nf, a + b) - ha - hb - log(2);
    wm = max(wm, m); wa = max(wa, s);
    if(m > 1e-40 || s > 1e-40, ok = 0));
  print("(4.4) 300 random pairs: max[h(uv)-h(u)-h(v)] = ", wm, "   max[h(u+v)-h(u)-h(v)-log2] = ", wa, "   all ok: ", ok);
}
print("(4.4) equality case u=v=1: h(2)-2h(1)-log2 = ", hplaces(QI, 2) - 2*hplaces(QI, 1) - log(2), ";  CONTROL without log2: h(2)-2h(1) = ", hplaces(QI, 2) - 2*hplaces(QI, 1), "  (>0: the log 2 is needed)");
{
  my(XL = [1 + 2*x^2, (3 + 4*x^2)/5, 1 + x - x^3, (1 + x - x^3)/7, 3 + 2*(x - x^3), 5/(2 + x^2), 12*x], Eh, B, r, pB, pr, c);
  Eh = sum(k = 1, #XL, hplaces(Q8, XL[k])) / #XL;
  for(j = 1, 3,
    B = [3/2, 2, 4][j]; r = [1/2, 3/10, 1/10][j]; pB = 0; pr = 0;
    for(k = 1, #XL, c = conjvec(Mod(nrm(Q8, XL[k]), Q8.pol)); for(m = 1, #c, pB += (abs(c[m]) > B); pr += (abs(c[m]) < r)));
    pB /= (#XL * 4); pr /= (#XL * 4);
    printf("(4.5) B=%.1f: P(|sX|>B)=%.4f <= Eh/logB=%.4f : %d     (4.6) r=%.2f: P(X!=0,|sX|<r)=%.4f <= Eh/log(1/r)=%.4f : %d\n",
      B, pB, Eh/log(B), pB <= Eh/log(B), r, pr, Eh/log(1/r), pr <= Eh/log(1/r)));
}
{
  my(X = 1/7, c = conjvec(Mod(1/7, QI.pol)));
  printf("CONTROL (4.6) with archimedean-only height: X=1/7, P_sigma(|sX|<1/2)=1 but arch log+ part = %.3f (bound 0 fails); true bound h(1/7)/log 2 = %.3f\n",
    sum(k = 1, 2, max(0, log(abs(c[k])))) / 2, hplaces(QI, X) / log(2));
}
