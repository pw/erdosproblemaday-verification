#!/usr/bin/env python3
"""Public reproduction checks for the scoped Problem 1117 partial."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT / "author"
AUDIT = ROOT / "hostile_audit"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


spec = importlib.util.spec_from_file_location("audit1117", AUDIT / "verify_audit.py")
require(spec is not None and spec.loader is not None, "could not load audit verifier")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
audit.AUTHOR = AUTHOR


live = json.loads((AUTHOR / "sources" / "live_1117_20260811.json").read_text())
pages = {page["requested_url"]: page["body_text"] for page in live["pages"]}
main = pages["https://www.erdosproblems.com/1117"]
claims = pages["https://www.erdosproblems.com/forum/thread/1117/proof-claims"]
for phrase in (
    "OPEN",
    "0 claimed proofs for this problem",
    "Currently working on this problem\tNone",
    "Interested in collaborating\tNone",
    "The second question is still open",
):
    require(phrase in main, f"live snapshot missing: {phrase}")
require("No proof claims have been submitted yet." in claims, "proof claim exists")

current = audit.read_tex("arxiv_2607.09462v1_source.tar", "Erdos_finite_order_v8_arxiv.tex")
for phrase in (
    r"v_f(r)\defeq \#(\M(f)\cap\{|z|=r\})",
    r"There is an entire function \(f\in\B\), of finite order",
    r"\limsup_{r\to\infty} v_f(r)=\infty",
    r"The second part remains open",
    r"no useful control of \(v_f(r)\) away from the prescribed radii",
    r"v_f(e^{x_n})\ge 2n+1",
    r"Since \(x_n\to+\infty\)",
):
    require(phrase in current, f"2026 source quantifier missing: {phrase}")

distinct_moduli = current.find("no two points have the same modulus")
prescribed_point = current.find(r"\(z_n\in\M(f)\)", distinct_moduli)
require(distinct_moduli >= 0 and prescribed_point >= distinct_moduli,
        "Theorem 1.2 distinct-moduli scope missing")

approximate = audit.read_tex("arxiv_2208.11154v2_source.tar", "maxmod_revision3.tex")
for phrase in ("it is theoretically possible", "is uniformly bounded", "unable to conclude"):
    require(phrase in approximate, f"2024 disclaimer missing: {phrase}")

harmonic_checks = audit.verify_endpoint_harmonic()
phase_checks = audit.verify_complex_binomial_phases()
print("PASS frozen live and primary-source quantifiers")
print(f"PASS complex endpoint-harmonic identities: {harmonic_checks}")
print(f"PASS complex binomial phase counts: {phase_checks}")
print("PASS limsup-only and polynomial-scope audit")
