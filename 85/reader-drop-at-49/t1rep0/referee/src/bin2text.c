/* referee: binary LRAT (stdin) -> text in the seat's exact line format, to diff against unpack_lrat's text. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static int pk=-1; static int peekb(void){ if(pk<0) pk=getchar(); return pk; } static int getb(void){ int c=peekb(); pk=-1; return c; }
static long long rd(void){ uint64_t u=0; unsigned sh=0; for(;;){ int b=getb(); if(b==EOF||b==0){fprintf(stderr,"bad varint\n");exit(2);} u|=(uint64_t)(b&127)<<sh; if(!(b&128))break; sh+=7; } long long i=(long long)(u>>1); return (u&1)?-i:i; }
int main(void){ static char ob[1<<20]; setvbuf(stdout,ob,_IOFBF,sizeof ob); long long last=0,n=0;
  for(;;){ int c=getb(); if(c==EOF)break; n++;
    if(c=='a'){ long long id=rd(); last=id; printf("%lld",id); while(peekb()!=0) printf(" %lld",rd()); getb(); printf(" 0"); while(peekb()!=0) printf(" %lld",rd()); getb(); printf(" 0\n"); }
    else if(c=='d'){ printf("%lld d",last); while(peekb()!=0) printf(" %lld",rd()); getb(); printf(" 0\n"); }
    else { fprintf(stderr,"bad action byte\n"); return 2; } }
  fprintf(stderr,"bin2text actions=%lld\n",n); return 0; }
