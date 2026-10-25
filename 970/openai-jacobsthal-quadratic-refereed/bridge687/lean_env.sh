L=/tmp/oaimath/021/lean-build; H=/tmp/oaimath/166/lean-build/home
export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=/tmp/oaimath/021/b687/out:/tmp/oaimath/021/bridge/out:$(cat $L/lean_path.txt)
