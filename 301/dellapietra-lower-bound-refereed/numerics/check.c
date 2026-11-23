// check.c -- independent k=2 relation-freeness check of an arbitrary set A subset [1,N].
//
// Route: for EVERY element a of A (no assumption about where heads live), enumerate every
// divisor d of a^2 with d < a (so b < c), put b = a + d, c = a + a^2/d, and report a relation
// when b <= N, c <= N, b in A and c in A.  This is the identity (b-a)(c-a) = a^2, which lists
// every solution of 1/a = 1/b + 1/c with a < b < c exactly once.  Membership is a bitmap of
// the set read from the file.  Integer arithmetic only (a^2 < 2^64 for a <= 4e9).
//
// Every element is tried as a head (no use of a < N/2), so nothing about the construction is assumed.
// usage: ./check N FILE   (FILE = one integer per line; '#' lines ignored)
// prints: |A|, number of relations found, the first 5 relations.  exit 0 = none, 1 = found, 2 = error
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned long long u64;

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: %s N FILE\n", argv[0]); return 2; }
  u64 N = strtoull(argv[1], 0, 10);
  FILE *f = fopen(argv[2], "r"); if (!f) { perror(argv[2]); return 2; }
  uint8_t *in = calloc(N + 1, 1);
  char line[64]; u64 sz = 0;
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    u64 x = strtoull(line, 0, 10);
    if (x < 1 || x > N) { fprintf(stderr, "element %llu outside [1,%llu]\n", x, N); return 2; }
    if (!in[x]) { in[x] = 1; sz++; }
  }
  fclose(f);
  // smallest prime factor table up to N
  uint32_t *spf = calloc(N + 1, sizeof(uint32_t));
  for (u64 i = 2; i <= N; i++) if (!spf[i]) for (u64 j = i; j <= N; j += i) if (!spf[j]) spf[j] = i;
  u64 found = 0; int shown = 0;
  static u64 div[1 << 20];
  for (u64 a = 1; a <= N; a++) {
    if (!in[a]) continue;
    // divisors of a^2
    int nd = 1; div[0] = 1; u64 x = a;
    while (x > 1) {
      u64 p = spf[x]; int e = 0; while (x % p == 0) { x /= p; e++; }
      int cur = nd; u64 pk = 1;
      for (int t = 1; t <= 2 * e; t++) { pk *= p; for (int j = 0; j < cur; j++) div[nd++] = div[j] * pk; }
    }
    u64 a2 = a * a;
    for (int j = 0; j < nd; j++) {
      u64 d = div[j];
      if (d >= a) continue;
      u64 b = a + d, c = a + a2 / d;
      if (b > N || c > N) continue;
      if (in[b] && in[c]) {
        found++;
        if (shown < 5) { printf("relation 1/%llu = 1/%llu + 1/%llu\n", a, b, c); shown++; }
      }
    }
  }
  printf("N=%llu |A|=%llu k2_relations_found=%llu\n", N, sz, found);
  return found ? 1 : 0;
}
