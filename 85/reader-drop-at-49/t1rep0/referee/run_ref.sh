#!/bin/bash
# referee independent route: our unpack7 -> zstd's LZ4 decoder -> strict RUP checker (binary, Std parse rules)
# usage: run_ref.sh <tag> <packed> <frameBytes> <cnf>
cd "$(dirname "$0")"
tag=$1; pk=$2; fb=$3; cnf=$4
ulimit -v 12000000
date -u +%FT%TZ > $tag.start
nice -n 19 src/unpack7 $pk $fb 2> $tag.unpack.err | nice -n 19 zstd -d --format=lz4 -c -q 2> $tag.zstd.err \
  | tee >(sha256sum > $tag.bin.sha256) >(wc -c > $tag.bin.bytes) \
  | nice -n 19 /usr/bin/time -f "MAXRSS_KB=%M %es" src/rupcheck $cnf > $tag.out 2> $tag.time
echo "pipestatus ${PIPESTATUS[*]}" > $tag.rc
date -u +%FT%TZ > $tag.end
