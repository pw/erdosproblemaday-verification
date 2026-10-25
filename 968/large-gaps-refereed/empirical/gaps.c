// #968 empirical table (erdosproblemaday.com, 2026-10-21). Segmented sieve of Eratosthenes up to LIMIT; for each consecutive prime
// pair (p_n, p_{n+1}) records: increase  p_n/n < p_{n+1}/(n+1)  [exact: (n+1)*p_n < n*p_{n+1} in 128-bit], and gap > C*log(p_n)
// for C in CS[]. Prints cumulative counts at checkpoints N = 10^k and 2.5*10^k, 5*10^k (n ≤ N), and writes the first 10,000
// increase-primes to oeis_check.txt (to be diffed against OEIS A387591's b-file).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef unsigned long long u64;
static const double CS[] = {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0};
#define NC 8
int main(int argc, char **argv) {
  u64 LIMIT = strtoull(argv[1], 0, 10);
  u64 sq = (u64)sqrt((double)LIMIT) + 2;
  char *small = calloc(sq + 1, 1); u64 *sp = malloc(sizeof(u64) * (sq + 1)); u64 nsp = 0;
  for (u64 i = 2; i <= sq; i++) if (!small[i]) { sp[nsp++] = i; for (u64 j = i * i; j <= sq; j += i) small[j] = 1; }
  const u64 SEG = 1 << 22; char *seg = malloc(SEG);
  u64 n = 0, prev = 0, inc = 0, big[NC] = {0}, maxgap = 0;
  static const u64 CK[] = {1000ULL,2500ULL,5000ULL,10000ULL,25000ULL,50000ULL,100000ULL,250000ULL,500000ULL,1000000ULL,2500000ULL,5000000ULL,10000000ULL,25000000ULL,50000000ULL,100000000ULL,250000000ULL,500000000ULL,1000000000ULL,2500000000ULL,5000000000ULL,0}; int ci = 0; u64 next_ck = CK[0];
  FILE *oe = fopen("oeis_check.txt", "w"); u64 oe_n = 0;
  for (u64 lo = 0; lo <= LIMIT; lo += SEG) {
    u64 hi = lo + SEG - 1; if (hi > LIMIT) hi = LIMIT;
    memset(seg, 0, SEG);
    for (u64 k = 0; k < nsp; k++) { u64 p = sp[k]; if (p * p > hi) break;
      u64 st = (lo + p - 1) / p * p; if (st < p * p) st = p * p; for (u64 j = st; j <= hi; j += p) seg[j - lo] = 1; }
    for (u64 x = (lo < 2 ? 2 : lo); x <= hi; x++) if (!seg[x - lo]) {
      // x is prime number n+1; pair (prev = p_n, x = p_{n+1})
      if (n >= 1) {
        unsigned __int128 a = (unsigned __int128)(n + 1) * prev, b = (unsigned __int128)n * x;
        int isinc = a < b; inc += isinc;
        if (isinc && oe_n < 10000) { fprintf(oe, "%llu %llu\n", ++oe_n, prev); }
        u64 g = x - prev; if (g > maxgap) maxgap = g; double lp = log((double)prev);
        for (int c = 0; c < NC; c++) if ((double)g > CS[c] * lp) big[c]++;
        if (n == next_ck) {
          printf("N=%llu p_N=%llu inc=%llu frac_inc=%.6f", n, prev, inc, (double)inc / n);
          for (int c = 0; c < NC; c++) printf(" gt%.1f=%.6f", CS[c], (double)big[c] / n);
          printf(" maxgap=%llu\n", maxgap); fflush(stdout);
          next_ck = CK[++ci]; if (!next_ck) next_ck = ~0ULL;
        }
      }
      n++; prev = x;
    }
  }
  fclose(oe);
  printf("END n_primes=%llu last_p=%llu inc=%llu frac_inc=%.6f", n, prev, inc, (double)inc / (n - 1));
  for (int c = 0; c < NC; c++) printf(" gt%.1f=%.6f", CS[c], (double)big[c] / (n - 1)); printf(" maxgap=%llu\n", maxgap);
  return 0;
}
