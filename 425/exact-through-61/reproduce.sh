#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
python3 base_erdos425_wave9i_verify.py
python3 verify_425_through_61.py
python3 audit_425_witnesses.py
python3 audit_425_logic.py
gzip -t replay_control_n50/upper_n50_F26.drat.gz
sha256sum -c SHA256SUMS
