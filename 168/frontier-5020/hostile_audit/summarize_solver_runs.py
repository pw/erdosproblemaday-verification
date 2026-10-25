#!/usr/bin/env python3
"""Summarize and sanity-check the independent solver reruns."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SCIP_OBJECTIVES = {
    5000: 3335,
    5001: 3335,
    5004: 3337,
    5006: 3338,
    5009: 3340,
    5011: 3341,
    5013: 3342,
    5016: 3344,
    5020: 3347,
}
FLATS = sorted(set(SCIP_OBJECTIVES) - {5000})


def match_one(pattern: str, text: str, cast):
    found = re.findall(pattern, text, flags=re.MULTILINE)
    assert len(found) == 1, (pattern, found)
    return cast(found[0])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cbc = {}
    for k in FLATS:
        path = args.runs / f"cbc_k{k}.log"
        text = path.read_text(encoding="ascii")
        assert "Result - Stopped on time limit" in text
        assert "No feasible solution found" in text
        assert "Result - Problem proven infeasible" not in text
        cbc[str(k)] = {
            "status": "UNKNOWN_TIME_LIMIT",
            "counterexample_found": False,
            "infeasibility_proved": False,
            "nodes": match_one(r"^Enumerated nodes:\s+(\d+)$", text, int),
            "iterations": match_one(r"^Total iterations:\s+(\d+)$", text, int),
            "wall_seconds": match_one(
                r"^Time \(B&C, Wallclock seconds\):\s+([0-9.]+)$", text, float
            ),
            "model_sha256": sha256(args.runs / f"flat_k{k}_counterexample.lp"),
            "log_sha256": sha256(path),
        }

    baseline_text = (args.runs / "cbc_k5000_baseline.log").read_text(encoding="ascii")
    assert "Result - Stopped on time limit" in baseline_text
    assert "MIPStart provided solution with cost 3335" in baseline_text
    cbc_baseline = {
        "status": "UNKNOWN_TIME_LIMIT",
        "verified_lower_bound": match_one(
            r"^Objective value:\s+([0-9.]+)$", baseline_text, float
        ),
        "remaining_upper_bound": match_one(
            r"^Upper bound:\s+([0-9.]+)$", baseline_text, float
        ),
        "nodes": match_one(r"^Enumerated nodes:\s+(\d+)$", baseline_text, int),
        "iterations": match_one(r"^Total iterations:\s+(\d+)$", baseline_text, int),
        "wall_seconds": match_one(
            r"^Time \(B&C, Wallclock seconds\):\s+([0-9.]+)$",
            baseline_text,
            float,
        ),
        "model_sha256": sha256(args.runs / "baseline_k5000_maximum.lp"),
        "start_sha256": sha256(args.runs / "baseline_k5000.mipstart"),
        "log_sha256": sha256(args.runs / "cbc_k5000_baseline.log"),
    }
    assert cbc_baseline["verified_lower_bound"] == 3335
    assert cbc_baseline["remaining_upper_bound"] > 3335

    scip = {}
    for k, expected in SCIP_OBJECTIVES.items():
        path = args.runs / f"independent_scip_k{k}.json"
        result = json.loads(path.read_text(encoding="ascii"))
        assert result["k"] == k and result["status"] == "optimal"
        assert result["objective"] == expected and result["dual_bound"] == expected
        assert result["gap"] == 0 and result["floating_mip"] is True
        log_path = args.runs / f"independent_scip_k{k}.log"
        log_text = log_path.read_text(encoding="ascii")
        assert "SCIP Status        : problem is solved [optimal solution found]" in log_text
        assert match_one(r"^Primal Bound\s*:\s*\+?([0-9.eE+-]+)", log_text, float) == expected
        assert match_one(r"^Dual Bound\s*:\s*\+?([0-9.eE+-]+)", log_text, float) == expected
        result["result_sha256"] = sha256(path)
        result["log_sha256"] = sha256(log_path)
        scip[str(k)] = result

    sat_text = (args.runs / "sat_unknown_probe.txt").read_text(encoding="ascii")
    assert "kissat_exit=124" in sat_text and "cadical_exit=124" in sat_text
    assert "c UNKNOWN" in sat_text
    sat = {
        "status": "UNKNOWN_TIME_LIMIT",
        "probe_seconds_each": 5,
        "versions": (args.runs / "sat_versions.txt").read_text(encoding="ascii").splitlines(),
        "probe_log_sha256": sha256(args.runs / "sat_unknown_probe.txt"),
        "note": "The CNF was not part of the frozen bundle; this probe used the matching nonfrozen working-tree CNF.",
    }

    summary = {
        "cbc": {
            "version": "Devel (unstable), build 2026-03-23",
            "arithmetic": "floating MIP",
            "baseline": cbc_baseline,
            "forced_new_counterexample_searches": cbc,
        },
        "independent_scip": {
            "version": "PySCIPOpt 6.2.1 / SCIP 10.0.2",
            "arithmetic": "floating MIP; exact mode unavailable",
            "rows": scip,
        },
        "sat_probe": sat,
    }
    args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="ascii")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
