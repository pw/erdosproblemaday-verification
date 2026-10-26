export HOME=/tmp/oai-math/lean-build/home ELAN_HOME=/tmp/oai-math/lean-build/home/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="/tmp/oai-math/lean-build/home/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
M=/tmp/erdos0300/lean/mathlib4/.lake
export LEAN_PATH=$M/build/lib/lean:$(ls -d $M/packages/*/.lake/build/lib/lean | tr '\n' ':')
