/* Erdős #488: exact size of the divisibility-minimal core of a smooth band.
   Band A = { s in (T, L*T] : every prime factor of s is <= y },  with y < L <= q (q = next prime after y).
   Core = minimal elements of A under divisibility = { s in A : s/p <= T for every prime p | s }
        = { s in A : s / P-(s) <= T }  (P-(s) = smallest prime factor; s/p is largest when p is smallest).
   Writing s = p*t with p = P-(s):  |core| = sum_{p <= y} #{ t in (T/p, T] : all prime factors of t in [p, y] }
   (t <= T < L*T/p automatically since p <= y < L).  Exact enumeration by DFS over nondecreasing prime index.
   Also prints Psi(T) = #{ y-smooth <= T } exactly, as a cross-check against the 11-11 brackets.
   Usage: ./core y T   (y <= T < 2^63; for T < y the primes in (T, y] are omitted) */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
typedef unsigned long long u64;
static int P[400], np;
static u64 T;
static u64 dfs(int i, u64 v, u64 lo){ /* count numbers w = v * (product of primes P[j], j>=i) with lo < w <= T, w>=v */
  u64 c = (v > lo) ? 1 : 0;
  for (int j = i; j < np; j++){ unsigned __int128 w = (unsigned __int128)v * P[j]; if (w > T) break; c += dfs(j, (u64)w, lo); }
  return c; }
int main(int argc, char **argv){
  int y = atoi(argv[1]); T = strtoull(argv[2], 0, 10);
  for (int k = 2; k <= y; k++){ int pr = 1; for (int d = 2; d * d <= k; d++) if (k % d == 0){ pr = 0; break; } if (pr) P[np++] = k; }
  /* work items: (p index a, first prime index j >= a) -> numbers t = P[j]*... with smallest prime index j >= a */
  int nitems = 0; static int IA[200000], IJ[200000];
  for (int a = 0; a < np; a++) for (int j = a; j < np; j++){ IA[nitems] = a; IJ[nitems] = j; nitems++; }
  u64 *percore = calloc(np, sizeof(u64)); u64 core = 0;
  #pragma omp parallel for schedule(dynamic,1) reduction(+:core)
  for (int it = 0; it < nitems; it++){ int a = IA[it], j = IJ[it]; u64 lo = T / P[a];
    /* t in (T/p, T]: integer t > T/p  <=>  t > floor(T/p) */
    u64 c = ((u64)P[j] <= T) ? dfs(j, P[j], lo) : 0;
    #pragma omp atomic
    percore[a] += c;
    core += c; }
  /* Psi(T) exactly: 1 + sum over smallest prime index j of dfs(j, P[j], 0) */
  u64 psi = 1;
  #pragma omp parallel for schedule(dynamic,1) reduction(+:psi)
  for (int j = 0; j < np; j++) psi += dfs(j, P[j], 0);
  printf("y=%d primes=%d T=%llu core=%llu Psi(T)=%llu\n", y, np, T, core, psi);
  printf("per smallest prime p:"); for (int a = 0; a < np && a < 12; a++) printf(" %d:%llu", P[a], percore[a]); printf(" ...\n");
  return 0; }
