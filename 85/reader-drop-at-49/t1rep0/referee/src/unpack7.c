/* referee: 7-bit unpack (LSB-first, per unpackOrderFortyNineSevenBit) streamed to stdout; stops at frameBytes. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: unpack7 packed frameBytes\n");return 2;}
  FILE*f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
  unsigned long long want=strtoull(argv[2],0,10), got=0; uint64_t acc=0; unsigned bits=0;
  static uint8_t in[1<<20], out[1<<20]; size_t n, on=0;
  while(got<want && (n=fread(in,1,sizeof in,f))>0){
    for(size_t i=0;i<n && got<want;i++){
      if(in[i]&0x80){fprintf(stderr,"high bit set at input byte\n");return 2;}
      acc|=(uint64_t)in[i]<<bits; bits+=7;
      if(bits>=8){ out[on++]=acc&0xff; acc>>=8; bits-=8; got++; if(on==sizeof out){fwrite(out,1,on,stdout);on=0;} }
    }
  }
  if(on) fwrite(out,1,on,stdout);
  if(got!=want){fprintf(stderr,"short: %llu of %llu\n",got,want);return 2;}
  fprintf(stderr,"unpack7: %llu frame bytes\n",got); return 0;
}
