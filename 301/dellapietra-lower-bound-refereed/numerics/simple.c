// simple.c -- the "simple" rough-third construction for Erdos #301, written from the definitions.
//
//   heads   : a in (N/3, N/2) with least prime factor >= L   (L in {7,11,13,17,19,23})
//   top     : the FULL closed top half [ceil(N/2), N], no regularity filter
//   delete  : every head a for which 1/a = 1/b + 1/c with b < c both in the top
//   A       : top  U  (heads that were not deleted)
//
// Conflict test (route used here; the checker uses a different one):
//   1/a = 1/b + 1/c, b<c  <=>  b = a(r+s)/s, c = a(r+s)/r for coprime divisors r<s of a.
//   b >= M:=ceil(N/2)  <=>  s*(M-a) <= r*a ;   c <= N  <=>  s*a <= r*(N-a).
//   Both are upper bounds on the ratio s/r, and any divisor pair d<d' reduces to a coprime
//   pair with the same ratio, so a conflicts  <=>  the SMALLEST ratio of two consecutive
//   divisors of a satisfies both inequalities.  All integer (__int128) arithmetic.
// Relation count (optional, --rel): number of coprime divisor pairs r<s of a satisfying both
//   inequalities = number of (a,b,c) relations with head a, b<c in the top.
//
// usage: ./simple N [--rel] [--dump-set FILE --dump-L L]
// Segmented sieve over the head interval; OpenMP, honour OMP_NUM_THREADS (we use 4).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

#define NL 6
static const int LS[NL] = {7, 11, 13, 17, 19, 23};
#define MAXF 16
#define MAXOM 40
#define NPOS 5

static u64 N, M, LO, HI;      // heads a in [LO,HI]
static uint32_t *primes; static int nprimes;

static int cmpu64(const void *x, const void *y) {
  u64 a = *(const u64 *)x, b = *(const u64 *)y; return a < b ? -1 : a > b;
}
static u64 gcdu(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: %s N [--rel] [--dump-set FILE --dump-L L]\n", argv[0]); return 2; }
  N = strtoull(argv[1], 0, 10);
  int want_rel = 0; const char *dumpf = 0; int dumpL = 7;
  for (int i = 2; i < argc; i++) {
    if (!strcmp(argv[i], "--rel")) want_rel = 1;
    else if (!strcmp(argv[i], "--dump-set")) dumpf = argv[++i];
    else if (!strcmp(argv[i], "--dump-L")) dumpL = atoi(argv[++i]);
  }
  M = (N + 1) / 2;            // ceil(N/2)
  LO = N / 3 + 1;             // smallest a with 3a > N
  HI = (N - 1) / 2;           // largest a with 2a < N
  // primes up to sqrt(HI)
  u64 sq = 1; while ((sq + 1) * (sq + 1) <= HI) sq++;
  char *comp = calloc(sq + 1, 1);
  primes = malloc(sizeof(uint32_t) * (sq + 1)); nprimes = 0;
  for (u64 i = 2; i <= sq; i++) if (!comp[i]) { primes[nprimes++] = i; for (u64 j = i * i; j <= sq; j += i) comp[j] = 1; }
  free(comp);

  // tallies indexed by least prime factor class: 0..5 for lpf == 7,11,13,17,19, >=23 (lpf>=23 means 23-rough)
  u64 heads[NL] = {0}, dele[NL] = {0}, rels[NL] = {0};
  u64 posH[NPOS] = {0}, posD[NPOS] = {0};           // L=7, by position of a in (N/3,N/2)
  u64 omH[MAXOM] = {0}, omD[MAXOM] = {0};           // L=7, by Omega(a)
  u64 maxtau = 0;

  char *delmark = 0;  // for dumping: bitmap over [LO,HI] of kept dumpL-rough heads
  if (dumpf) delmark = calloc(HI - LO + 1, 1);

  const u64 SEG = 1 << 18;
  u64 nseg = (HI - LO + 1 + SEG - 1) / SEG;
  #pragma omp parallel
  {
    u64 *rem = malloc(sizeof(u64) * SEG);
    u64 *fp = malloc(sizeof(u64) * SEG * MAXF);   // u64: the last prime factor can exceed 2^32 when N >= 8.6e9
    uint8_t *fe = malloc(SEG * MAXF);
    uint8_t *nf = malloc(SEG);
    u64 *div = malloc(sizeof(u64) * 200000);
    u64 lh[NL] = {0}, ld[NL] = {0}, lr[NL] = {0}, lpH[NPOS] = {0}, lpD[NPOS] = {0}, loH[MAXOM] = {0}, loD[MAXOM] = {0};
    u64 lmaxtau = 0;
    #pragma omp for schedule(dynamic, 1)
    for (u64 sg = 0; sg < nseg; sg++) {
      u64 s0 = LO + sg * SEG, s1 = s0 + SEG - 1; if (s1 > HI) s1 = HI;
      u64 len = s1 - s0 + 1;
      for (u64 i = 0; i < len; i++) { rem[i] = s0 + i; nf[i] = 0; }
      for (int k = 0; k < nprimes; k++) {
        u64 p = primes[k];
        if (p * p > s1) break;
        u64 first = ((s0 + p - 1) / p) * p;
        for (u64 m = first; m <= s1; m += p) {
          u64 i = m - s0; uint8_t e = 0;
          while (rem[i] % p == 0) { rem[i] /= p; e++; }
          fp[i * MAXF + nf[i]] = p; fe[i * MAXF + nf[i]] = e; nf[i]++;
        }
      }
      for (u64 i = 0; i < len; i++) {
        u64 a = s0 + i;
        if (rem[i] > 1) { fp[i * MAXF + nf[i]] = rem[i]; fe[i * MAXF + nf[i]] = 1; nf[i]++; }
        u64 lpf = fp[i * MAXF];
        if (lpf < 7) continue;                // not 7-rough: never a head for L>=7
        int cls = 0; while (cls < NL - 1 && LS[cls + 1] <= lpf) cls++;
        // divisors of a
        int nd = 1; div[0] = 1; int om = 0;
        for (int f = 0; f < nf[i]; f++) {
          u64 p = fp[i * MAXF + f]; int e = fe[i * MAXF + f]; om += e;
          int cur = nd; u64 pk = 1;
          for (int t = 1; t <= e; t++) { pk *= p; for (int j = 0; j < cur; j++) div[nd++] = div[j] * pk; }
        }
        if ((u64)nd > lmaxtau) lmaxtau = nd;
        qsort(div, nd, sizeof(u64), cmpu64);
        u128 MA = M - a, NA = N - a;
        int conflict = 0;
        for (int j = 0; j + 1 < nd; j++) {
          u128 d = div[j], d2 = div[j + 1];
          if (d2 * MA <= d * (u128)a && d2 * (u128)a <= d * NA) { conflict = 1; break; }
        }
        u64 nrel = 0;
        if (want_rel && conflict) {
          for (int j = 0; j < nd; j++) for (int k = j + 1; k < nd; k++) {
            u128 r = div[j], s = div[k];
            if (s * MA > r * (u128)a || s * (u128)a > r * NA) break;  // ratio grows with k
            if (gcdu(div[j], div[k]) == 1) nrel++;
          }
        }
        lh[cls]++; if (conflict) ld[cls]++; lr[cls] += nrel;
        int pos = (int)(((6 * a - 2 * N) * (u128)NPOS) / N);
        lpH[pos]++; if (conflict) lpD[pos]++;
        loH[om]++; if (conflict) loD[om]++;
        if (delmark && lpf >= (u64)dumpL && !conflict) delmark[a - LO] = 1;
      }
    }
    #pragma omp critical
    {
      for (int c = 0; c < NL; c++) { heads[c] += lh[c]; dele[c] += ld[c]; rels[c] += lr[c]; }
      for (int c = 0; c < NPOS; c++) { posH[c] += lpH[c]; posD[c] += lpD[c]; }
      for (int c = 0; c < MAXOM; c++) { omH[c] += loH[c]; omD[c] += loD[c]; }
      if (lmaxtau > maxtau) maxtau = lmaxtau;
    }
    free(rem); free(fp); free(fe); free(nf); free(div);
  }

  u64 top = N - M + 1;
  printf("# simple construction: N=%llu  top=[%llu,%llu] (%llu elements)  heads a in [%llu,%llu]  max tau(a)=%llu\n",
         N, M, N, top, LO, HI, maxtau);
  printf("# L  rough_heads  deleted  kept_heads  |A|  2|A|-N  excess=(|A|/N-1/2)  deleted_fraction%s\n", want_rel ? "  relations" : "");
  for (int c = 0; c < NL; c++) {
    u64 H = 0, D = 0, R = 0;
    for (int c2 = c; c2 < NL; c2++) { H += heads[c2]; D += dele[c2]; R += rels[c2]; }
    u64 kept = H - D, A = top + kept;
    long long twoex = 2 * (long long)A - (long long)N;
    // excess = twoex / (2N) printed with 7 decimals, exact integer division
    long long ex7 = (long long)(((__int128)twoex * 10000000) / (2 * (__int128)N));
    u64 df6 = H ? (u64)(((u128)D * 1000000) / H) : 0;
    printf("L=%-2d %llu %llu %llu %llu %lld 0.%07lld 0.%06llu", LS[c], H, D, kept, A, twoex, ex7, df6);
    if (want_rel) printf(" %llu", R);
    printf("\n");
  }
  printf("# L=7 heads by position of a in (N/3,N/2), fifths: heads deleted kept\n");
  for (int c = 0; c < NPOS; c++) printf("pos%d %llu %llu %llu\n", c, posH[c], posD[c], posH[c] - posD[c]);
  printf("# L=7 heads by Omega(a): Omega heads deleted kept\n");
  for (int c = 0; c < MAXOM; c++) if (omH[c]) printf("Omega%d %llu %llu %llu\n", c, omH[c], omD[c], omH[c] - omD[c]);

  if (dumpf) {
    FILE *f = fopen(dumpf, "w");
    for (u64 a = LO; a <= HI; a++) if (delmark[a - LO]) fprintf(f, "%llu\n", a);
    for (u64 b = M; b <= N; b++) fprintf(f, "%llu\n", b);
    fclose(f);
  }
  return 0;
}
