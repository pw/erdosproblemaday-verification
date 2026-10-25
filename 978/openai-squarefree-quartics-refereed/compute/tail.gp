\\ Large-prime tail of Proposition 1.4 for d = 4, k = 2: n <= N with p^2 | f(n) for some prime p > n (full factorisation).
tail(f, N) = { my(L = List()); for(n = 1, N, my(v = subst(f, x, n), F = factor(v));
   for(i = 1, #F~, if(F[i,2] >= 2 && F[i,1] > n, listput(L, [n, F[i,1], F[i,2]])))); Vec(L) };
N = 100000;
t1 = tail(x^4 + 2, N); print("x^4+2, n<=", N, ": ", #t1, " inputs with p^2 | f(n), p > n: ", t1);
t2 = tail(x^4 + 1, N); print("x^4+1, n<=", N, ": ", #t2, " inputs with p^2 | f(n), p > n: ", t2);
quit;
