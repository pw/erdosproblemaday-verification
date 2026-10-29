#!/bin/bash
# usage: flip_one.sh POS  -> prints "POS count c0 c1 firstexample"
W=/home/exedev/MathDyad/subs-1029/531/submitted/k5_w1513.txt
out=$(/tmp/ref531/chkB "$W" 5 1 "$1")
tot=$(echo "$out" | sed -n 's/.*mono_total=\([0-9]*\).*/\1/p')
ex=$(echo "$out" | grep '^MONO' | head -1)
echo "$1 $tot | $ex"
