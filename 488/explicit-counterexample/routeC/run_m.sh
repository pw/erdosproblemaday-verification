#!/bin/bash
export OMP_NUM_THREADS=6
R=$1; tag=$2
run(){ name=$1; shift; bash -c "ulimit -v 12000000; exec timeout 3000 nice -n 10 ./e488m $*" > log_m_${tag}_${name}.txt 2>&1; }
run t1_y401_W52761 401 409 $R 12589254117941 52761
run t2_y251_2p56 251 256 $R 72057594037927936 22616
run t3_y251_2p48 251 256 $R 281474976710656 24415
run t4_y401_1.5e13 401 409 $R 15000000000000 52761
