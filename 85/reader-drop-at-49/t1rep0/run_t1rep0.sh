#!/bin/bash
# External LRAT check of the authors' h7_t1_rep0 certificate (14,332,419 actions) against the CNF
# rendered from their Lean definition (EmitT1Rep0.lean, same_as_lean_cnf=true). Our decoder + drat-trim lrat-check.
cd "$(dirname "$0")"
D=/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/strata-lrat
L=$HOME/.local/bin/lrat-check
date -u +%FT%TZ > t1rep0.start
sha256sum $D/h7_t1_rep0.packed.lz4p7 > t1rep0.packed.sha256
( ulimit -v 8000000; exec nice -n 19 ./unpack_lrat $D/h7_t1_rep0.packed.lz4p7 1405625860 2680553030 2> unpack_t1r0.err ) \
 | ( ulimit -v 24000000; exec nice -n 19 /usr/bin/time -f "MAXRSS_KB=%M %es" $L h7_t1_rep0.cnf > lratcheck_t1r0.out 2> lratcheck_t1r0.time )
echo "pipestatus ${PIPESTATUS[*]}" > t1rep0.rc
date -u +%FT%TZ > t1rep0.end
