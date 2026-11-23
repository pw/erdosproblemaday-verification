// brute.c -- brute-force relation search for small sets, lengths k = 2, 3, 4.
//
// Tails first: for every k-subset {b_1 < ... < b_k} of A, form S = 1/b_1 + ... + 1/b_k exactly as
// num/den (integers), and report a relation when S = 1/a for an integer a (den % num == 0) with
// a in A and a different from every b_i (automatically a < b_1 since S > 1/b_1).  Every relation
// 1/a = sum of k distinct reciprocals is found exactly once.  Integer arithmetic only.
//
// usage: ./brute N FILE KMAX     prints counts for k = 2..KMAX and the first 3 relations of each k.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef unsigned long long u64;
static u64 gcdu(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: %s N FILE KMAX\n", argv[0]); return 2; }
  u64 N = strtoull(argv[1], 0, 10); int KMAX = atoi(argv[3]);
  FILE *f = fopen(argv[2], "r"); if (!f) { perror(argv[2]); return 2; }
  uint8_t *in = calloc(N + 1, 1); u64 *el = malloc(sizeof(u64) * (N + 1)); int n = 0;
  char line[64];
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    u64 x = strtoull(line, 0, 10);
    if (x < 1 || x > N) { fprintf(stderr, "element %llu outside [1,%llu]\n", x, N); return 2; }
    if (!in[x]) in[x] = 1;
  }
  fclose(f);
  for (u64 x = 1; x <= N; x++) if (in[x]) el[n++] = x;   // ascending
  u64 cnt[5] = {0}; int shown[5] = {0};
  // k = 2
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
    u64 b = el[i], c = el[j], num = b + c, den = b * c;
    if (den % num) continue;
    u64 a = den / num;
    if (a <= N && in[a]) { cnt[2]++; if (shown[2]++ < 3) printf("k=2: 1/%llu = 1/%llu + 1/%llu\n", a, b, c); }
  }
  // k = 3
  if (KMAX >= 3)
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
    u64 b = el[i], c = el[j]; u64 n2 = b + c, d2 = b * c; u64 g = gcdu(n2, d2); n2 /= g; d2 /= g;
    for (int k = j + 1; k < n; k++) {
      u64 e = el[k]; u64 num = n2 * e + d2, den = d2 * e;
      if (den % num) continue;
      u64 a = den / num;
      if (a <= N && in[a]) { cnt[3]++; if (shown[3]++ < 3) printf("k=3: 1/%llu = 1/%llu + 1/%llu + 1/%llu\n", a, b, c, e); }
    }
  }
  // k = 4
  if (KMAX >= 4)
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
    u64 b = el[i], c = el[j]; u64 n2 = b + c, d2 = b * c; u64 g = gcdu(n2, d2); n2 /= g; d2 /= g;
    for (int k = j + 1; k < n; k++) {
      u64 e = el[k]; u64 n3 = n2 * e + d2, d3 = d2 * e; u64 g3 = gcdu(n3, d3); n3 /= g3; d3 /= g3;
      for (int l = k + 1; l < n; l++) {
        u64 h = el[l]; u64 num = n3 * h + d3, den = d3 * h;
        if (den % num) continue;
        u64 a = den / num;
        if (a <= N && in[a]) { cnt[4]++; if (shown[4]++ < 3) printf("k=4: 1/%llu = 1/%llu + 1/%llu + 1/%llu + 1/%llu\n", a, b, c, e, h); }
      }
    }
  }
  printf("N=%llu |A|=%d", N, n);
  for (int k = 2; k <= KMAX && k <= 4; k++) printf(" k%d=%llu", k, cnt[k]);
  printf("\n");
  return (cnt[2] + cnt[3] + cnt[4]) ? 1 : 0;
}
