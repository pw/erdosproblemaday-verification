default(parisize, 200000000);
ep(p) = lcm(znorder(Mod(2,p)), znorder(Mod(3,p)));
{
S = Set();
for(d=1,5040, S = setunion(S, Set(factor(gcd(2^d-1,3^d-1))[,1]~)));
S = select(p->p>=5 && ep(p)<=5040, S);
print("#primes e_p<=5040: ", #S, "  largest: ", S[#S]);
n = vector(5040); for(j=1,#S, n[ep(S[j])]++);
D = vector(5040, N, sumdiv(N, d, n[d]/d));
best = vecsort(vector(5040,N,[D[N],N]), , 4);
for(j=1,10, print(best[j][2], "  ", best[j][1], "  ", best[j][1]*1.));
w = select(x->x>=1, D, 1); print("N with density>=1: ", w);
write("/tmp/evidence203/gp_set.txt", S);
}
quit;
