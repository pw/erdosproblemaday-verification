#!/bin/bash
# same cube, same binary, same options, twice: is CaDiCaL 3.0.1 deterministic on this machine?
C=$HOME/MathDyad/tools/cadical-3.0.1/build/cadical; cd $HOME/MathDyad/erdos112/kirtchakov/determinism
for k in 1 2; do rm -f f$k; mkfifo f$k; nice -n 19 $C --lrat --no-binary s21_884_1.cnf f$k > sol$k 2>&1 & p=$!; tee < f$k >(wc -c > bytes$k) | sha256sum | cut -d' ' -f1 > sha$k; wait $p; sleep 1; echo "run$k $(cat sha$k) $(cat bytes$k)"; done
