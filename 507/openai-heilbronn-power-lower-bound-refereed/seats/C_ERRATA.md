# Erratum to C_report.md (coordinator, 2026-10-22 ~16:00Z)

C_report.md (and C_work/check7_out.txt) give log10 η = −249.498 and log10(1/(100000k)) = −250.142. These are wrong by
exactly 14: the helper `flog10` in C_work/check7_arith.py mishandles the Fraction. Two independent routes give
log10 η = −235.4982 (η = 3.1757140364…·10⁻²³⁶) and Lean exponent 7.2144283…·10⁻²³⁷:
  python3: math.log10 on the exact integer α = 45435k+16 (log10 α = 235.79919), and Decimal(2)/Decimal(α) at 50 digits;
  /tmp/oaimath/191/compute/sizes.py (a third, digit-count route).
Big O Speedrun's board independently lists OpenAI's baseline as ≈ 3.18·10⁻²³⁶. The page uses 3.18·10⁻²³⁶ and 7.2·10⁻²³⁷.
The digit counts in C's report (M 39, T 116, k 232) and every other C result are unaffected.
