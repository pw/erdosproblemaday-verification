default(parisize, 200000000);
{
my(c1=1.0, c2=1.0, P=2*10^7, s1=0, s2=0);
forprime(p=3, P,
  r2 = #polrootsmod(x^4+2, p);
  r1 = if(p%8==1, 4, 0);
  c2 *= 1 - r2/p^2;
  c1 *= 1 - r1/p^2;
  if(p > P/2, s1 += r1; s2 += r2));
\\ tail: sum_{p>P} rho(p)/p^2 approx (avg rho = 1) * 1/(P log P)
tail = 1.0/(P*log(P));
print("c(x^4+1) ~ ", c1, " (tail factor ~ exp(-", tail, "))");
print("c(x^4+2) ~ ", c2, " (tail factor ~ exp(-", tail, "))");
print("avg rho in (P/2,P]: x^4+1 ", s1/(primepi(P)-primepi(P/2)), "  x^4+2 ", s2/(primepi(P)-primepi(P/2)));
print("observed n<=10^6: x^4+1 ", 980831/10^6, "  x^4+2 ", 756674/10^6);
}
