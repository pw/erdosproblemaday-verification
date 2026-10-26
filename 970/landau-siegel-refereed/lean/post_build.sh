#!/bin/bash
# Seat D: after the closure build ends, run the bridge, the mutants, the audit negative control, then leanchecker --fresh.
D=/tmp/oaimath/003/seats/D_work; cd $D
log(){ echo "[$(date -u +%FT%TZ)] $*" >> $D/logs/post_build.log; }
while ! grep -q '^closure_build ' $D/steps.tsv 2>/dev/null; do sleep 20; done
log "closure: $(grep '^closure_build ' $D/steps.tsv)"
grep -q '^closure_build 0 67/67' $D/steps.tsv || { log "BUILD NOT COMPLETE - stopping"; exit 1; }
./runlean.sh env_bridge.sh logs/Bridge.log Bridge.lean out/SeatD003/Bridge; echo "bridge $?" >> steps.tsv; log "bridge rc=$?"
for m in beta_le_two no_log drop_ne_one re_not_im LSeries drop_primitive; do
  ./runlean.sh env_bridge.sh logs/BridgeMut_$m.log BridgeMut_$m.lean; echo "mut_$m $?" >> steps.tsv; log "mut_$m done"
done
./runlean.sh env_bridge.sh logs/AuditNegControl.log AuditNegControl.lean; echo "auditneg $?" >> steps.tsv
source env_bridge.sh
cd $D/bridge
nice -n 19 leanchecker --fresh SeatD003.NoSuchModule > $D/logs/leanchecker_missing_control.log 2>&1; echo "leanchecker_missing_control $?" >> $D/steps.tsv
log "leanchecker fresh start"
$D/rsscap.sh 14000000 7200 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' nice -n 19 leanchecker --fresh SeatD003.Bridge > $D/logs/leanchecker_fresh.log 2>&1; rc=$?
echo "leanchecker_fresh $rc" >> $D/steps.tsv; log "leanchecker fresh rc=$rc"
log DONE
