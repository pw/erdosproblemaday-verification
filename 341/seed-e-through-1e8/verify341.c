// verify341.c — from-scratch check of the defining recurrence on a WINDOW [X, X+w) of a computed Dickson/Queneau
// greedy set. Reads <elems.u32> (uint32 LE, increasing), rebuilds S as a bitset, and decides "x in S+S" for every x
// in the window by iterating over ELEMENTS s <= (X+w)/2 and OR-ing the slice S[X-s, X+w-s) (unaligned 64-bit reads)
// into a window accumulator — the generator iterates over positions t and shifts the whole prefix; this iterates
// over summands and reads the suffix slice. Asserts for every x in the window with x > maxseed: x in S <=> x not in sums.
// usage: verify341 elems.u32 distinct maxseed X w [flipbit]   (flipbit: XOR membership of one position = negative control)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t *S; static long WS;
static inline uint64_t rd(long bit){ // 64 bits of S starting at absolute bit position `bit` (may be unaligned), zero beyond
  long wi=bit>>6; int sh=bit&63; uint64_t lo=(wi<WS)?S[wi]:0, hi=(wi+1<WS)?S[wi+1]:0;
  return sh? (lo>>sh)|(hi<<(64-sh)) : lo; }
#define GETB(B,i) ((B[(i)>>6]>>((i)&63))&1ULL)
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: verify341 elems.u32 distinct maxseed X w [flipbit]\n");return 2;}
  const char*fn=argv[1]; int distinct=atoi(argv[2]); long M=atol(argv[3]); long X=atol(argv[4]); long w=atol(argv[5]);
  long flip=(argc>6)?atol(argv[6]):-1;
  FILE*f=fopen(fn,"rb"); if(!f){perror("open");return 2;} fseek(f,0,SEEK_END); long ne=ftell(f)/4; fseek(f,0,SEEK_SET);
  uint32_t*el=malloc(4*ne); if(fread(el,4,ne,f)!=(size_t)ne){fprintf(stderr,"short read\n");return 2;} fclose(f);
  long top=el[ne-1]; if(X+w-1>top){fprintf(stderr,"window beyond data (top=%ld)\n",top);return 2;}
  WS=top/64+2; S=calloc(WS,8);
  for(long i=0;i<ne;i++){ if(i&&el[i]<=el[i-1]){fprintf(stderr,"not increasing at %ld\n",i);return 2;} S[el[i]>>6]|=1ULL<<(el[i]&63); }
  if(flip>=0) S[flip>>6]^=1ULL<<(flip&63);
  long WW=w/64+2; uint64_t*V=calloc(WW,8);
  long half=(X+w-1)/2;
  // summands: every s in S with s <= half (use the bitset so a flipped-in position counts too)
  for(long s=1;s<=half;s++){ if(!GETB(S,s)) continue;
    long t0=X-s; if(t0<s) t0=s; if(distinct&&t0==s) t0=s+1; long t1=X+w-s; if(t0>=t1) continue;
    long j0=s+t0-X;                       // window bit for t0
    for(long t=t0, j=j0; t<t1; t+=64, j+=64){ uint64_t m=rd(t); long rem=t1-t; if(rem<64) m&=(rem==64)?~0ULL:((1ULL<<rem)-1);
      int sh=j&63; long wi=j>>6; V[wi]|=m<<sh; if(sh && wi+1<WW) V[wi+1]|=m>>(64-sh); }
  }
  long viol=0,inS=0,first[5]; int nf=0;
  for(long x=X;x<X+w;x++){ if(x<=M) continue; int in=GETB(S,x), sum=GETB(V,x-X); inS+=in; if(in==sum){ if(nf<5) first[nf++]=x; viol++; } }
  printf("window [%ld,%ld) elems=%ld inS=%ld violations=%ld",X,X+w,ne,inS,viol); for(int i=0;i<nf;i++) printf(" %ld",first[i]); printf("\n");
  return viol?1:0;
}
