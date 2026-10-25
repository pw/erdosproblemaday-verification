default(parisize, 200000000);
ep(p) = lcm(znorder(Mod(2,p)), znorder(Mod(3,p)));
pool(N) = {my(g=gcd(2^N-1,3^N-1), f=factor(g)[,1]~); select(p->p>=5, f)};
{
for(i=1,3, N=[720,5040,55440][i];
  P = pool(N);
  s = sum(j=1,#P, 1/ep(P[j]));
  \\ independent direct sieve up to 10^7
  Q = List(); forprime(p=5, 10^7, if(Mod(2,p)^N==1 && Mod(3,p)^N==1, listput(Q,p)));
  print("N=",N," #pool=",#P," sum=",s," | sieve<=1e7 count=",#Q, " same set below 1e7: ", Vec(Q)==select(p->p<=10^7,P));
);
}
quit;
