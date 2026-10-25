#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$base"
python=${PYTHON:-python3}

sha256sum --quiet -c MANIFEST.sha256
echo "manifest_discrepancies=0"

work=$(mktemp -d -t c4star39-audit.XXXXXX)
cleanup() {
  find "$work" -depth -delete 2>/dev/null || true
}
trap cleanup EXIT

tar -xf provenance/upstream_commit_86a1c505.tar -C "$work"
diff -qr upstream_ro "$work"
git init --bare "$work/verify.git" >/dev/null
git -C "$work/verify.git" bundle verify "$base/provenance/upstream_history_86a1c505.bundle" >/dev/null
echo "upstream_custody_discrepancies=0"

"$python" independent_verify_f39.py >"$work/independent.log"
diff -u logs/independent_verify.log "$work/independent.log"
"$python" -O independent_verify_f39.py >"$work/independent_optimized.log"
diff -u logs/independent_verify.log "$work/independent_optimized.log"
echo "independent_exact_check=PASS"

(
  cd upstream_ro
  "$python" run_all_verifiers.py >"$work/upstream_all.log"
  "$python" validate_encoding.py >"$work/validate_encoding.log"
  "$python" validate_yconstraint.py >"$work/validate_yconstraint.log"
)
grep -Fq "ALL VERIFIERS PASSED" "$work/upstream_all.log"
grep -Fq "Conclusions: R(C4,K_{1,39}) = 46" "$work/upstream_all.log"
grep -Fq "ENCODING SOUND at full scale" "$work/validate_encoding.log"
grep -Fq "perturbed        -> False (expected False) OK" "$work/validate_yconstraint.log"
echo "upstream_supplied_verifiers=PASS"
echo "audit_reproduction=PASS"
