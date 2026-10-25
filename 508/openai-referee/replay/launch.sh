#!/bin/bash
L=/tmp/oaimath/158/lean-build
nohup setsid nice -n 19 bash $L/build.sh > $L/driver.log 2>&1 &
echo $! > $L/driver.pid; echo "launched pid $(cat $L/driver.pid) at $(date -u +%FT%TZ)"
