# Independent live-source audit

Accessed 2026-08-11 UTC.

## Exact searches repeated

```text
"F(n) > n" "partition function" prime factors
"A194261" "10100"
"3153783057104074183545720448060964239"
"p(1)*p(2)*...*p(n)" "10000" prime factors
```

The search engine returned the live problem/OEIS material or unrelated uses
of partition functions. It returned no indexed occurrence of the quoted
extension witness and no public 10,100 extension. This is a dated, scoped
absence observation, not an exhaustive novelty proof.

## Records checked

* `https://www.erdosproblems.com/1106` - OPEN; zero comments; zero claimed
  proofs; no current workers; page last edited 2025-11-16.
* `https://www.erdosproblems.com/latex/1106` - statement and known asymptotic
  context agree with the rendered page.
* `https://oeis.org/A194259` - exact-count sequence; wording says the strict
  inequality after 115 "appears" to hold; linked b-file ends at 10,000.
* `https://oeis.org/A194260` - difference `F(n)-n`; positivity after 115 is
  described as an appearance; linked table is 1..10,000.
* `https://oeis.org/A194261` - smallest-new-prime sequence; linked b-file ends
  at 10,000.
* `https://pari.math.u-bordeaux.fr/dochtml/ref/Arithmetic_functions.html` -
  official documentation says `isprime` rigorously proves or disproves
  primality and contrasts it with `ispseudoprime`.

The current OEIS b-files themselves are frozen as `current_b194259_20260811.txt`
and `current_b194261_20260811.txt`; download hashes and row bounds are in
`oeis_download_audit.log`.

