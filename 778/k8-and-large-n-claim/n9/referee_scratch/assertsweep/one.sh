#!/bin/bash
# usage: one.sh <cert>  -> writes one line per option: cert|opt|orig|assert|fired
f=$1; C=$HOME/MathDyad/erdos778/cpp/check778c; A=/tmp/erdos778/referee_scratch/check778c_assert
for opt in "" "--no-cutoff"; do a=$($C $f $opt 2>/dev/null | head -1 | sed 's/\[check778c.*//'); e=$(mktemp); b=$($A $f $opt 2>$e | head -1 | sed 's/\[check778c.*//'); fired=0; grep -q ASSERT $e && fired=1; rm -f $e
  echo "$f|$opt|$fired|$([ "$a" == "$b" ] && echo same || echo DIFF)|${a:0:40}"; done
