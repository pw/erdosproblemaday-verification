\\ Independent PARI/GP check of the explicit 111-integer obstruction file.

left = 133858454292;
right = 133858454404;
certificate = readvec("gap_133858454292_133858454404.cert");

if (#certificate != right-left-1, error("wrong certificate length"));
{
for (i = 1, #certificate,
  row = certificate[i];
  n = row[1]; p = row[2]; e = row[3];
  if (n != left+i, error("nonconsecutive certificate row at index ", i));
  if (!isprime(p), error("witness is composite at n=", n));
  if (p % 4 != 3, error("witness is not 3 mod 4 at n=", n));
  if (e % 2 != 1, error("witness exponent is even at n=", n));
  if (valuation(n, p) != e, error("wrong exact valuation at n=", n));
);
}

if (49986^2 + 362436^2 != left, error("left endpoint representation failed"));
if (35298^2 + 364160^2 != right, error("right endpoint representation failed"));

{
print("PARI_CERTIFICATE_PASS rows=", #certificate,
      " endpoints=", left, ",", right, " gap=", right-left);
}
