/* Three copies of W (INF = 0) whose Z13-orbit sets cover >= 97 of the 99 orbits.  Case analysis (see NOTES):
   (alpha) some two of the three orbit-sets are disjoint  -> enumerate disjoint pairs (33,33) and (33,32), scan the third;
   (beta)  three 33-sets pairwise meeting in one and the same orbit (union 97).
   Output: TRIPLE lines with union size and the three role vectors.                                            */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>
typedef unsigned __int128 u128;
typedef struct { u128 mask; uint8_t role[13]; uint8_t d; uint8_t pad[2]; } rec_t;
#define PC(a,b) (__builtin_popcountll(a)+__builtin_popcountll(b))
int main(void){
    FILE*f=fopen("z13_d31.bin","rb"); fseek(f,0,SEEK_END); long n=ftell(f)/sizeof(rec_t); rewind(f);
    rec_t *A=malloc(n*sizeof(rec_t)); if(fread(A,sizeof(rec_t),n,f)!=(size_t)n) return 1; fclose(f);
    /* sort indices by d descending: 33s first, then 32s, then 31s; pack masks */
    long *ord=malloc(n*sizeof(long)), k=0, n33,n32;
    for(int d=33;d>=31;d--){ for(long i=0;i<n;i++) if(A[i].d==d) ord[k++]=i; if(d==33) n33=k; if(d==32) n32=k-n33; }
    uint64_t *lo=malloc(n*8),*hi=malloc(n*8); for(long i=0;i<n;i++){ lo[i]=(uint64_t)A[ord[i]].mask; hi[i]=(uint64_t)(A[ord[i]].mask>>64); }
    const uint64_t FL=~0ULL, FH=(1ULL<<35)-1;
    fprintf(stderr,"n=%ld n33=%ld n32=%ld\n",n,n33,n32);
    long pa=0,pb=0,pc_=0,sols=0;
    #pragma omp parallel for schedule(dynamic,32) reduction(+:pa,pb,pc_,sols)
    for(long a=0;a<n33;a++){
        uint64_t l1=lo[a],h1=hi[a];
        /* (alpha-1) disjoint (33,33), b>a ; third any index != a,b with |R \ m3| <= 2, R has 33 orbits */
        for(long b=a+1;b<n33;b++){ if((l1&lo[b])|(h1&hi[b])) continue; pa++;
            uint64_t rl=FL&~(l1|lo[b]), rh=FH&~(h1|hi[b]);
            for(long c=0;c<n;c++){ if(c==a||c==b) continue; if(PC(rl&~lo[c],rh&~hi[c])<=2){ sols++;
                #pragma omp critical
                { printf("TRIPLE alpha33 union %d |",99-PC(rl&~lo[c],rh&~hi[c])); long T[3]={a,b,c}; for(int t=0;t<3;t++){ for(int q=0;q<13;q++) printf(" %d",A[ord[T[t]]].role[q]); printf(" |"); } printf("\n"); fflush(stdout);} } } }
        /* (alpha-2) disjoint (33,32); third from d>=32 (index < n33+n32), != a,b, with |R \ m3| <= 2, R has 34 orbits */
        for(long b=n33;b<n33+n32;b++){ if((l1&lo[b])|(h1&hi[b])) continue; pb++;
            uint64_t rl=FL&~(l1|lo[b]), rh=FH&~(h1|hi[b]);
            for(long c=0;c<n33+n32;c++){ if(c==a||c==b) continue; if(PC(rl&~lo[c],rh&~hi[c])<=2){ sols++;
                #pragma omp critical
                { printf("TRIPLE alpha32 union %d |",99-PC(rl&~lo[c],rh&~hi[c])); long T[3]={a,b,c}; for(int t=0;t<3;t++){ for(int q=0;q<13;q++) printf(" %d",A[ord[T[t]]].role[q]); printf(" |"); } printf("\n"); fflush(stdout);} } } }
        /* (beta) 33,33,33 pairwise overlap exactly one common orbit */
        for(long b=a+1;b<n33;b++){ uint64_t cl=l1&lo[b], ch=h1&hi[b]; if(PC(cl,ch)!=1) continue; pc_++;
            uint64_t ul=l1|lo[b], uh=h1|hi[b];
            for(long c=b+1;c<n33;c++){ uint64_t il=ul&lo[c], ih=uh&hi[c]; if(il==cl && ih==ch){ sols++;
                #pragma omp critical
                { printf("TRIPLE beta union 97 |"); long T[3]={a,b,c}; for(int t=0;t<3;t++){ for(int q=0;q<13;q++) printf(" %d",A[ord[T[t]]].role[q]); printf(" |"); } printf("\n"); fflush(stdout);} } } }
    }
    fprintf(stderr,"disjoint (33,33) pairs %ld ; disjoint (33,32) pairs %ld ; (33,33) pairs with overlap 1: %ld ; triples with union >= 97: %ld\n",pa,pb,pc_,sols);
    return 0;
}
