#!/bin/sh
# Reproduces every finite check in referee_dichotomy.md. Each line < 60 s, < 200 MB.
cd "$(dirname "$0")"
timeout 120 python3 thresholds.py 20000            > out_thresholds.txt
timeout 100 python3 affinity_check.py 7            > out_affinity.txt
timeout 100 python3 toy_model.py A 3000 1          > out_A.txt
timeout 100 python3 toy_model.py A 3000 1 --lam1   > out_A_ctrl_lam1.txt
timeout 100 python3 toy_model.py A 3000 1 --alpha 0.1 > out_A_ctrl_alpha.txt
timeout 100 python3 toy_model.py A 3000 1 --uniformV  > out_A_ctrl_uniformV.txt
timeout 100 python3 toy_model.py B 1500 2          > out_B.txt
timeout 100 python3 toy_model.py B 1500 2 --lam1   > out_B_ctrl_lam1.txt
timeout 100 python3 toy_model.py C 300 6 --longer  > out_C.txt
timeout 100 python3 toy_model.py C 150 4 --longer --vscale 1e6 > out_C_ctrl_vscale.txt
