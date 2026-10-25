\\ Exact local densities rho_f(p^2) by brute force mod p^2 for p < 2000; rho_f(p) = #roots mod p beyond (p unramified, odd => simple roots lift uniquely).
\\ c_f = prod_p (1 - rho(p^2)/p^2), truncated at P = 2e7; tail bound sum_{p>P} 4/p^2 < 4/(P log P).
default(parisize, 200000000);
rho2(f, p) = { my(q = p^2, c = 0); for(a = 0, q-1, if(subst(f, x, a) % q == 0, c++)); c };
euler(f, P) = { my(s = 0., d = poldisc(f)); forprime(p = 2, P, my(r);
   if(p < 2000 || d % p == 0, r = rho2(f, p), r = #polrootsmod(f, p));
   s += log(1 - r/p^2)); exp(s) };
\p 30
f1 = x^4 + 2; f2 = x^4 + 1;
print("rho(4), rho(9), rho(p^2) small for x^4+2: ", vector(8, i, rho2(f1, prime(i))));
print("rho for x^4+1: ", vector(8, i, rho2(f2, prime(i))));
P = 2*10^7;
print("c(x^4+2) truncated at 2e7 = ", euler(f1, P), "  tail bound ", 4./(P*log(P)));
print("c(x^4+1) truncated at 2e7 = ", euler(f2, P));
\\ direct count by full factorisation (independent of any sieve)
cnt(f, N) = { my(c = 0); for(n = 1, N, if(issquarefree(subst(f, x, n)), c++)); c };
N = 200000;
c1 = cnt(f1, N); c2 = cnt(f2, N);
print("N=", N, "  #sqfree x^4+2: ", c1, "  ratio ", c1/N*1.);
print("N=", N, "  #sqfree x^4+1: ", c2, "  ratio ", c2/N*1.);
quit;
