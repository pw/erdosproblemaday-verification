# Independent audit bundle for Erdos 222

Disposition: **PASS** for the bounded exact frontier claim in
`AUDIT_VERDICT.md`.

Key cold evidence:

- `full_scan_0_200b_width73456789.out`: fresh combined scan with a new chunk
  width, proving the frontier directly through 200 billion.
- `verify_full_scan.log`: exact scan-field and count-aggregation checks.
- `scanner_harness.log`: both scanners versus an SPF-factorisation classifier
  across boundary and randomized partition cases.
- `regenerated_gap_133858454292_133858454404.cert`: independent PARI
  regeneration, byte-identical to the author certificate.
- `certificate_regeneration_audit.log`: regeneration result.
- `oeis_refetch.log` and `live_page_refetch_keylines.txt`: current-scope checks.
- `author_manifest_check.log`: integrity check of the untouched author bundle.

Two output-only robustness issues outside the claimed represented-endpoint
regime are disclosed in the verdict.  They do not affect the result.
