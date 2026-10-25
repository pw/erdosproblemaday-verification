#!/bin/bash
cd ~/MathDyad/erdos85/h1k; ulimit -v 6000000
for a in "$@"; do echo "## $a"; timeout 700 ~/.venv/bin/python h1cube2.py $a 2>&1 | tail -2; done
