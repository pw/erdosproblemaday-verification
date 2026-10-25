#!/bin/bash
L=/tmp/oaimath/012/lean-build
cd $L && python3 drive.py 5 > drive2.out 2>&1
bash $L/post.sh
