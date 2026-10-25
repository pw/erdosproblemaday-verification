/* unpack_lrat.c — our own decoder (erdos cron seat, 2026-10-20) for the authors'
 * "packed.lz4p7" LRAT certificates, written from the Lean definitions in
 * Proofs/Erdos85OrderFortyNineLratCertificateBase.lean (7-bit unpack -> LZ4 frame ->
 * binary LRAT) and Std's binary LRAT parser; emits TEXT LRAT on stdout for
 * drat-trim's lrat-check.  Fails loudly (exit 2) on any size/format mismatch.
 *
 *   unpack_lrat <packed> <frameBytes> <binaryBytes> [--mutate K] > proof.lrat
 *
 * --mutate K : negative control — drop the FIRST hint of the K-th addition
 *              (1-based) that has >= 2 hints; a sound checker must then reject.
 * --mutate-last-empty : negative control on the DECISIVE step — drop the LAST hint
 *              of the final empty-clause addition (drat-trim lrat-check wrongly
 *              accepts this; a sound checker must reject).
 * --binary   : emit binary LRAT (Std / drat-trim binary encoding) instead of text.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static void die(const char *m) { fprintf(stderr, "unpack_lrat: %s\n", m); exit(2); }

static uint8_t *slurp(const char *p, size_t *n) {
  FILE *f = fopen(p, "rb"); if (!f) die("open packed");
  fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  uint8_t *b = malloc(sz); if (!b) die("malloc packed");
  if (fread(b, 1, sz, f) != (size_t)sz) die("read packed");
  fclose(f); *n = sz; return b;
}

static uint32_t rd32(const uint8_t *d) { return d[0] | d[1] << 8 | d[2] << 16 | (uint32_t)d[3] << 24; }

int main(int argc, char **argv) {
  if (argc < 4) die("usage: unpack_lrat packed frameBytes binaryBytes [--mutate K]");
  size_t frameBytes = strtoull(argv[2], 0, 10), binBytes = strtoull(argv[3], 0, 10);
  long mutateK = 0; int mutLastEmpty = 0, binary = 0;
  for (int a = 4; a < argc; a++) {
    if (!strcmp(argv[a], "--mutate") && a + 1 < argc) mutateK = atol(argv[++a]);
    else if (!strcmp(argv[a], "--mutate-last-empty")) mutLastEmpty = 1;
    else if (!strcmp(argv[a], "--binary")) binary = 1;
    else die("unknown option");
  }
  size_t np; uint8_t *packed = slurp(argv[1], &np);
  /* 7-bit unpack, LSB first (unpackOrderFortyNineSevenBit) */
  uint8_t *frame = malloc(frameBytes); if (!frame) die("malloc frame");
  size_t fo = 0; uint64_t acc = 0; unsigned bits = 0;
  for (size_t i = 0; i < np && fo < frameBytes; i++) {
    if (packed[i] & 0x80) die("packed byte has high bit set (not 7-bit text)");
    acc |= (uint64_t)packed[i] << bits; bits += 7;
    if (bits >= 8) { frame[fo++] = acc & 0xff; acc >>= 8; bits -= 8; }
  }
  if (fo != frameBytes) die("7-bit unpack produced fewer bytes than frameBytes");
  free(packed);
  fprintf(stderr, "unpacked frame %zu bytes\n", fo);
  /* LZ4 frame */
  if (frameBytes < 7 || rd32(frame) != 0x184D2204) die("bad LZ4 magic");
  uint8_t flg = frame[4];
  if ((flg & 0xC0) != 0x40 || (flg & 0x02)) die("bad LZ4 FLG");
  int bcs = flg & 0x10, csz = flg & 0x08, ccs = flg & 0x04, dict = flg & 0x01;
  size_t pos = 4 + 2 + (csz ? 8 : 0) + (dict ? 4 : 0) + 1;
  uint8_t *out = malloc(binBytes); if (!out) die("malloc out");
  size_t on = 0;
  for (;;) {
    if (pos + 4 > frameBytes) die("truncated block size");
    uint32_t raw = rd32(frame + pos); pos += 4;
    if (raw == 0) { if (pos + (ccs ? 4 : 0) != frameBytes) die("trailing bytes after end mark"); break; }
    size_t bsz = raw & 0x7fffffff;
    if (pos + bsz > frameBytes) die("block overruns frame");
    if (raw & 0x80000000) {
      if (on + bsz > binBytes) die("uncompressed block overruns output");
      memcpy(out + on, frame + pos, bsz); on += bsz;
    } else {
      size_t p = pos, stop = pos + bsz;
      while (p < stop) {
        uint8_t tok = frame[p++]; size_t ll = tok >> 4;
        if (ll == 15) { uint8_t b; do { if (p >= stop) die("lit len"); b = frame[p++]; ll += b; } while (b == 255); }
        if (p + ll > stop || on + ll > binBytes) die("literal overrun");
        memcpy(out + on, frame + p, ll); on += ll; p += ll;
        if (p == stop) break;
        if (p + 2 > stop) die("offset overrun");
        size_t off = frame[p] | frame[p + 1] << 8; p += 2;
        size_t ml = (tok & 15);
        if (ml == 15) { uint8_t b; ml = 19; do { if (p >= stop) die("match len"); b = frame[p++]; ml += b; } while (b == 255); }
        else ml += 4;
        if (off == 0 || off > on || on + ml > binBytes) die("bad match");
        for (size_t k = 0; k < ml; k++) { out[on] = out[on - off]; on++; }
      }
    }
    pos += bsz + (bcs ? 4 : 0);
  }
  free(frame);
  if (on != binBytes) die("decoded size != binaryBytes");
  fprintf(stderr, "decoded binary LRAT %zu bytes\n", on);
  /* locate the LAST empty-clause addition (for --mutate-last-empty) */
  size_t lastEmptyPos = (size_t)-1;
  if (mutLastEmpty) {
    size_t q = 0;
    while (q < on) {
      size_t start = q; uint8_t c = out[q++];
      if (c != 'a' && c != 'd') die("scan: expected a or d");
      int nfields = (c == 'a') ? 3 : 1; /* a: id, lits..0, hints..0 ; d: ids..0 */
      if (c == 'a') {
        while (out[q] & 128) q++; q++;            /* id */
        int nl = 0; while (out[q] != 0) { while (out[q] & 128) q++; q++; nl++; } q++;
        while (out[q] != 0) { while (out[q] & 128) q++; q++; } q++;
        if (nl == 0) lastEmptyPos = start;
      } else { while (out[q] != 0) { while (out[q] & 128) q++; q++; } q++; }
      (void)nfields;
    }
    if (lastEmptyPos == (size_t)-1) die("no empty-clause addition found");
  }
  size_t q = 0; long long lastid = 0, nadd = 0, ndel = 0, nempty = 0, nrat = 0, addk = 0;
  char *buf = malloc(1 << 22); size_t bl = 0;
#define FLUSH() do { fwrite(buf, 1, bl, stdout); bl = 0; } while (0)
#define PUT(...) do { bl += sprintf(buf + bl, __VA_ARGS__); if (bl > (1 << 22) - 256) FLUSH(); } while (0)
#define PUTB(ch) do { buf[bl++] = (char)(ch); if (bl > (1 << 22) - 256) FLUSH(); } while (0)
#define PUTV(x) do { long long _x = (x); uint64_t _u = _x < 0 ? (((uint64_t)(-_x)) << 1) | 1 : ((uint64_t)_x) << 1; \
      while (_u >= 128) { PUTB((_u & 127) | 128); _u >>= 7; } PUTB(_u); } while (0)
  while (q < on) {
    size_t recStart = q;
    uint8_t c = out[q++];
    #define RDLIT(dst) do { uint64_t u = 0; unsigned sh = 0; for (;;) { if (q >= on) die("eof in lit"); uint8_t b = out[q++]; if (b == 0 && sh == 0) die("zero byte in lit"); u |= (uint64_t)(b & 127) << sh; if (!(b & 128)) break; sh += 7; if (sh > 63) die("lit too long"); } dst = (u & 1) ? -(long long)(u >> 1) : (long long)(u >> 1); } while (0)
    if (c == 'a') {
      long long id; RDLIT(id); if (id <= 0) die("non-positive id");
      if (binary) { PUTB('a'); PUTV(id); } else PUT("%lld", id);
      lastid = id; nadd++;
      int nl = 0;
      while (out[q] != 0) { long long l; RDLIT(l); if (binary) PUTV(l); else PUT(" %lld", l); nl++; }
      q++; if (binary) PUTB(0); else PUT(" 0");
      if (nl == 0) nempty++;
      int wantdrop = 0, dropLast = (mutLastEmpty && recStart == lastEmptyPos), cnt = 0;
      { size_t q2 = q; while (out[q2] != 0) { while (out[q2] & 128) q2++; q2++; cnt++; } }
      if (mutateK && cnt >= 2) { addk++; if (addk == mutateK) wantdrop = 1; }
      int dropped = 0, israt = 0, idx = 0;
      while (out[q] != 0) { long long h; RDLIT(h); idx++; if (h < 0) israt = 1;
        if (wantdrop && !dropped) { dropped = 1; fprintf(stderr, "MUTATION: dropped first hint %lld of clause id %lld\n", h, id); continue; }
        if (dropLast && idx == cnt) { fprintf(stderr, "MUTATION: dropped LAST hint %lld (of %d) of the final empty clause id %lld\n", h, cnt, id); continue; }
        if (binary) PUTV(h); else PUT(" %lld", h); }
      q++; if (binary) PUTB(0); else PUT(" 0\n");
      if (israt) nrat++;
    } else if (c == 'd') {
      if (binary) PUTB('d'); else PUT("%lld d", lastid);
      while (out[q] != 0) { long long h; RDLIT(h); if (h <= 0) die("bad deletion id"); if (binary) PUTV(h); else PUT(" %lld", h); }
      q++; if (binary) PUTB(0); else PUT(" 0\n"); ndel++;
    } else die("expected a or d");
  }
  FLUSH();
  fprintf(stderr, "actions: add=%lld del=%lld total=%lld empty_adds=%lld rat_adds=%lld last_id=%lld\n",
          nadd, ndel, nadd + ndel, nempty, nrat, lastid);
  return 0;
}
