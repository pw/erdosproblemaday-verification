default(parisize, 100000000);
a = eval(getenv("A")); b = eval(getenv("B")); w = eval(getenv("W"));
{
sq = 0; big = List(); mid = 0;
for(n = a, b,
  v = n^4 + w;
  f = factor(v);
  issq = 1;
  for(j = 1, #f~,
    if(f[j,2] >= 2,
      issq = 0;
      if(f[j,1] > n, listput(big, [n, f[j,1], f[j,2]]));
      if(f[j,1] > sqrtint(n) && f[j,1] <= n, mid++)));
  sq += issq);
print("RANGE ", a, " ", b, " W ", w, " SQF ", sq, " MID ", mid, " BIG ", #big);
for(i = 1, #big, print("BIGHIT ", big[i]));
}
