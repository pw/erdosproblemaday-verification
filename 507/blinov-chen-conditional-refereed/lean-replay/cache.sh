#!/bin/bash
set -x
cd /tmp/oaimath/191b/lean/mathlib4
export PATH=$HOME/.elan/bin:$PATH
df -h / | tail -1
elan toolchain install leanprover/lean4:v4.11.0
lean --version
nice -n 19 lake exe cache get
echo "CACHE_RC=$?"
du -sh .lake
df -h / | tail -1
