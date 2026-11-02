# Host (erdos seat) notes — #1188 submission 8gfcew (Pedro Martins), 2026-11-02

Source: Zenodo 10.5281/zenodo.23427851 (v2 of concept 23406126, 16 Oct 2026; v1 15 Oct same size), 34 pp,
sha256 64039de93e248ef0ae2862a107c568c10a787b432e4272c7100144c65fe69d0d. Fetched from Zenodo on 2026-11-02.
The "accompanying verification supplement" (Section 8) is NOT in the Zenodo record (one PDF only; pdfdetach shows
only a C2PA "Content Credentials" attachment).

## Read line by line by the host (independent of the seats)
- Lemma 2.1, 2.3, Construction 3.1 / Prop 3.2 (covering, distinct moduli via top/cof, private integers incl. the
  B_{iota(q)} exclusion via v_j(z) = v), proof of Thm 1.2 (injectivity: top(n)=p picks out A_{p,u}, u = residue mod p,
  sigma_p(u) = n/p). HOLDS.
- Thm 1.3 local lemma (CRT lift z' ≡ r mod p^e, z' ≡ z mod L'; a class in A_p would force r ≡ a_A mod p^{v_p}), Cor 1.4
  (floor(x/p) < p multiples), Thm 1.5 (map S_x -> residue or *). HOLDS. The upper bound is elementary.
- Construction 4.2 / Prop 4.3 (I-part / I-free part decomposition of moduli; covering by walking the tree with z mod c;
  private integer gets z ≡ r_lambda mod e_lambda added; leaves split at the last common node). HOLDS.
- Prop 4.7 (single splitters c in (x^{1/5}, x^{1/4}], levels p in (2x^{2/5}, P)): pools P_{p,c} = I-free sigma <= x/(pc)
  are < p so divide M_F(p); sum_c f_{p,c} <= 2x^{4/5}/p < p-1; N_{p,c} >= y/20 since y >= sqrt2 c and 1-S_I > 0.77;
  injectivity from (modulus -> p,c,sigma; residue -> u,v); Mertens sums give lambda(lambda - 3/20) log x.
  kappa_1 = (1-lambda) lambda (lambda - 3/20) = 0.012679 recomputed. HOLDS.
  => log F(x) >= (0.01267 + o(1)) x log x by a fully elementary argument, so log F(x) = Theta(x log x) is established
     independently of the deeper Theorem 4.8 (which only improves the constant to 0.0672).

## Host computations (mine/)
- explicit.py: Prop 7.2 finite range checked for EVERY integer 2..400,000 (paper needs < 81,796): 0 violations, max
  (Upsilon - (1-log2) n log n)/n = 0.5418 at n = 50 (allowance 1.5). Control Upsilon(12) = hand value.
  Prop 7.1 finite range 40 <= x < e^20, step function tested at the sup of each step: 0 violations, min margin
  (Lambda - RHS)/x = 0.0604 near x = 928.
- examples.py: Examples 3.3, 4.4, 4.5 built FROM THE CONSTRUCTION RULES (sigma = u-th smallest admissible divisor, iota by
  position, tau as printed), exact count-array check over Z/L. Controls: classical system accepted; +3 mod 8 rejected
  (not minimal); minus 7 mod 12 rejected (not covering). Ex 4.4: 40 classes, max modulus 330, minimal covering; printed
  split residues reproduced; ALL 6720 padding injections give minimal distinct coverings, 6720 distinct systems.
  Ex 4.5: 40 classes, max 2310, printed 11 split residues reproduced; all 120 orderings of the I-part-35 group pass.
