# #203 entry: blind consistency read (2026-10-12)

**Scope.** I checked `/tmp/seat1200/entry203.js` (title, summary, body, links) against the `~/MathDyad/erdos203/` files, `/tmp/evidence203/REPORT.md` and `/tmp/erdos203_forum.html`. Nothing in the source directory was modified. My own check scripts and outputs are in `/tmp/seat1200/chk/` (`pools.py`, `front.py`, `wit.py`, `gap.py`, `js.mjs`, `cpsat_S4S5_rerun.log`).

**Severity scale.**
- **HIGH:** fix before going live — the statement is false or overclaims, or the page is visibly broken.
- **MED:** misleading, or stronger than the files support.
- **LOW:** wording, or a true claim with no saved artifact.

## Issues

1. **HIGH: the title renders its HTML tags as literal text.**
   - Phrase: `Σ 1/e<sub>p</sub>` in `title`.
   - Source: the site prints titles through `escapeHtml(e.title)` in `<h1>` (src/index.js:8769), in the home cards (8568) and in `<title>`. No existing entry title contains HTML (0 of the titles in index.js).
   - Effect: readers will see the literal text `<sub>p</sub>`.
   - **Fix:** write `Σ 1/eₚ` (U+209A) or `Σ 1/e_p` in the title.

2. **HIGH: the Filaseta–Finch–Kozek DOI points to a different paper.**
   - Phrase: `https://doi.org/10.1016/j.jnt.2007.09.003`.
   - Source: Crossref resolves that DOI to Homma, *"On the discrepancy of uniformly distributed roots of quadratic congruences"*, JNT 128 (2008) 500–508.
   - The FFK paper is **10.1016/j.jnt.2008.02.004** (JNT 128 (2008) 1916–1940).
   - **Fix:** replace the URL with `https://doi.org/10.1016/j.jnt.2008.02.004`.

3. **HIGH: "every covering has Σ 1/e_p ≥ 1.16625" overclaims.**
   - Where it appears:
     - title: "none with Σ 1/e_p below 1.166";
     - summary: "every covering has Σ 1/e_p ≥ 1.16625";
     - Theorem B: "every covering system for #203 has Σ 1/e_p ≥ 1.16625";
     - "What is ours": "a lower bound Σ 1/e_p ≥ 1.16625 on any covering that exists".
   - What the inequality gives: union(P) ≤ U(P∩B) + Σ_{P∖B} 1/e_p. That yields Σ_{p∈P} 1/e_p ≥ 1 + loss(P ∩ S7). This equals 1.16625 only when P contains **all seven** of 5, 7, 11, 13, 17, 19, 31.
   - A covering that avoids some of the seven gets only the subset's loss, from `subsets_S7.json`: e.g. {7,11,13,17,19,31} loss 0.0696, {5,19} loss 0. One that avoids all seven gets bare Σ ≥ 1.
   - The README makes the same overclaim ("So any covering system for #203 has Σ 1/e_p ≥ 1.16625"), so it originates there.
   - **The period exclusions are not affected.** They go through the pool density, which is monotone (U(P∩B) ≤ U(pool∩B), Σ_{P∖B} ≤ Σ_{pool∖B}).
   - **Fix:** use "every covering that uses all of 5, 7, 11, 13, 17, 19 and 31 has Σ 1/e_p ≥ 1.16625". Equivalently, "a covering whose period is a multiple of 720 needs pool density ≥ 1.16625". The title needs a matching change, e.g. "…and every covering through the seven smallest usable primes wastes 0.166".

4. **HIGH: "every covering … wastes a twenty-fourth" overclaims in the same way.**
   - Where it appears: the title, the slug ("every covering system wastes a twenty-fourth"), and the summary ("so every covering needs Σ 1/e_p ≥ 25/24").
   - Source: Theorem A, which the body states correctly ("any covering system **containing 5 and 7**"). A covering without 5 or without 7 is not forced to waste 1/24.
   - **Fix:**
     - title/slug: "every covering through 5 and 7 wastes a twenty-fourth";
     - summary: "so every covering that uses 5 and 7 needs Σ 1/e_p ≥ 25/24".
   - The ≤ 5040 exclusion still holds as written, because a covering at 5040 that drops 5 or 7 has Σ ≤ 143/140 − 1/6 < 1.

5. **HIGH: "period above 65,520" is not supported.**
   - Phrase (summary): "…and period above 65,520 (every N ≤ 30,000 excluded one by one)".
   - Source: `frontier.out` says "N values with data: 30012 ; contiguous from 1 to 30000". The only N above 30,000 with data are 30240, 40320, 45360, 50400, 55440, 60480, 65520, 110880, 166320, 221760, 332640 and 720720.
   - Every other period in (30000, 65520] is unscanned, e.g. 31680, 36960, 39600, 47520, 63360.
   - Context, not a fix:
     - The judgment seat is computing some of these in `/tmp/ref203`: 36960 = 1.0300, 39600 = 1.0662, 47520 = 1.0634, none in the bundle.
     - Using the known primes, my lower bounds for the gap all sit at a union bound ≤ 0.90 (`chk/gap.py`), so the claim is very likely true. It is still not computed.
   - **Fix:** either "period above 30,000 (and not 30240, 40320, 45360, 50400, 55440, 60480 or 65520)", or extend the scan through 65,520 before making the claim.

6. **MED: "three independent implementations" overclaims for the seven-prime block.**
   - Phrase: "The block maxima are (d) computer-assisted by three independent implementations".
   - What the logs show, by block:

     | Block | Max | Implementations with a saved log |
     |---|---|---|
     | S4 | 1765 | C, Python-bigint (`bigint.log`), evidence seat, CP-SAT* |
     | S5 | 30580 | C, Python-bigint, evidence seat, CP-SAT* |
     | S6 | 294900 | C (`S6.log`), numpy (`np_S6.log`), bigint |
     | **S7** | **303336** | **C only** (`S7.log`) |

   - *The CP-SAT runs for S4/S5 have no log in the directory. I re-ran `cpsat_maxcover.py`: S4 OPTIMAL 1765 (1.5 s), S5 OPTIMAL 30580 (38.6 s). The log is `chk/cpsat_S4S5_rerun.log`; add it to the bundle.
   - The **S7 value and all 128 entries of `subsets_S7.json`** (built by `subsets.py` → `./maxunion`) come from the C tool alone: `np_S7.log`, `cpsat_S6.log` and `cpsat_S7.log` are 0 bytes. S7 carries the headline 0.16625.
   - I re-counted the S7 witness (0 1 1 0 0 1 0) literally in numpy: 303336 ✓. So the value is attained; only its *maximality* rests on one implementation.
   - **Fix:** say "S4–S6 agree across the C, numpy and Python-integer brute forces (CP-SAT also proves S4 and S5 optimal); the seven-prime maximum and the 128-subset table are from the C brute force alone, with its per-coset count check and a literal numpy re-count of the witness".
   - Also: `bundle.sh` will ship the two **empty** `cpsat_S6.log` and `cpsat_S7.log`. Drop them or label them "not completed".

7. **MED: the Theorem C parenthetical has the direction backwards.**
   - Phrase: "(unconstrained: 0.568866 — the free sets gain less than the residue condition costs)".
   - Source: max_d U_d = 0.586296 > 0.568866, so the net change is **+0.0174**. At d = 720 the free sets add density 0.2000 (`fixed_720.bin`: 103680/518400), and the union still rises from 0.568866 to 0.586296. The free sets therefore gain *more* than the residue condition costs. The README has the same sentence.
   - **Fix:** "(no free sets, no residue condition: 0.568866 — the free sets bring up to 0.20 of density, but the residue condition takes back all but 0.017 of it)".

8. **MED: "the first pools this block does not exclude" overclaims.**
   - Phrase: "The first pools this block does not exclude are 110880 (1.1777), …".
   - Source: no period between 65,520 and 110,880 was computed, so "first" is not established.
   - **Fix:** "Of the larger periods we computed, the block leaves open 110880 (1.1777), 166320 (1.1913), 221760 (1.1826), 332640 (1.2064) and 720720 (99 primes, 1.2490)." The densities themselves are ✓.

9. **MED: "would already decide the periods up to 332640" overclaims.**
   - Source: an 8-prime loss ≥ 0.2064 would exclude the four computed pools 110880, 166320, 221760 and 332640 (all divisible by 36, so 37 is in each). It would say nothing about the unscanned periods in between.
   - **Fix:** "would already exclude the computed pools 110880, 166320, 221760 and 332640 if its loss reaches 0.21". 0.21 > 0.2064 ✓.

10. **MED: the judgment seat's report does not exist yet.**
    - Phrase: "…both read the bundle before this went up; their reports are in it." The link label also says "both referee reports".
    - Source: there is no `referee_judgment.md` in `~/MathDyad/erdos203/`. `bundle.sh` copies it with `2>/dev/null || true`, so it would be skipped silently. The judgment seat is still writing files in `/tmp/ref203` (12:42).
    - The evidence seat also did not "read the bundle". Its report says it recomputed from scratch, read only the README and forum, and touched nothing under `erdos203/`.
    - **Fix:**
      - do not publish until `referee_judgment.md` is in the bundle, and make `bundle.sh` fail when it is missing;
      - reword to "a separately briefed evidence seat recomputed … from scratch and compared with our README; a hostile referee with tools (Opus) read the bundle; both reports are in it".

11. **MED: "Both say, correctly, that none of this is a proof" is wrong for AnimishSharma.**
    - Source: AnimishSharma's comment explicitly lists "Proved: the subgroup formula…" and "Proved: the density necessary condition…". The page itself says he "proved the density condition" two lines earlier.
    - **Fix:** "Neither claims to prove nonexistence."

12. **LOW: the veljjanoski quotation drops a parenthetical without marking it.**
    - Phrase: "the chains that make 1D Sierpiński coverings work have no analogue here".
    - Source (15 Sep 2026 comment): "The chains that make 1D Sierpiński coverings work ($2 \mid 4 \mid 8 \mid \cdots \mid 64$) have no analogue here."
    - **Fix:** "…coverings work (2 | 4 | 8 | ⋯ | 64) have no analogue here", or mark the cut with "[…]".

13. **LOW: "falls short by 0.003, as do 60480 (1.0633) and 65520 (1.1035)" reads as if all three miss by 0.003.**
    - Source: 55440 misses by 0.003209 ✓. 60480 misses by 0.1029 and 65520 by 0.0627.
    - **Fix:** "…falls short by 0.003; 60480 (1.0633) and 65520 (1.1035) fall further short".

14. **LOW: "the six smallest primes" is literally 2, 3, 5, 7, 11, 13.**
    - Phrase: "for N₀ divisible by 720 the six smallest primes have exactly one admissible coset each".
    - Source: `algsweep` d = 720 allowed = [1,1,1,1,1,1] ✓. I checked from the definition (2^k3^ℓ ≡ −1): the cosets are {2},{3},{5},{6},{8},{9}, matching the witness.
    - **Fix:** "the six block primes 5–19".

15. **LOW: "(sub-blocks computed for the periods lacking 17 or 19)" leaves out 11.**
    - Source: there are also sweeps for blocks lacking 11: `algsweep_5_7_13`, `_5_7_13_19` and `_5_7_13_17_19`.
    - **Fix:** "lacking 11, 17 or 19".

16. **LOW: code gap in the sub-block sweeps; the result is unchanged.**
    - This is not page text. Sub-blocks without 11 have LCM 12, 36 or 144, so `algsweep.py` never builds the free set 5ℤ². `frontier.py`'s allowance starts at q = 7. For periods with 12 | N and 5 ∤ N, the perfect-power bound therefore omits up to 1/25.
    - I re-ran the frontier with +0.04 credited to those blocks (`chk/front.py`). **No N ≤ 30,000 flips.** The worst perfect-power margin is still 0.98497 at N = 25200, which uses the full S6 block.
    - **Fix:** credit 1/25 when 5 ∤ LCM in `frontier.py`, or add a sentence to the README.

17. **LOW: Lemma 1 leaves out the free sets.**
    - Phrase: "…certify compositeness… then the cosets cover all of ℤ²: their union is invariant under the lattice ∩ L_p".
    - Source (README): "the cosets C_p … **together with the free sets** cover all of ℤ²", invariant under ∩L_p ∩ (periods of the free sets).
    - **Fix:** add "together with the free sets", and include the free sets' periods in the invariance lattice.

18. **LOW: the all-N scan is described with a method it did not use.**
    - Phrase: "factoring that number (split along the cyclotomic pairs…, with the product… checked equal to the gcd)… We did this for every N ≤ 30,000". The Labels paragraph says the same: "the all-N scan… with a completeness certificate (the product… equals the gcd)".
    - Source: `scanN.py` factors G with plain sympy `factorint` and checks each factor with `isprime`. It does no cyclotomic split and no explicit product check. That is equivalent in substance (the factorisation multiplies to G); the description is just inaccurate.
    - Data ✓:
      - 30,000 rows, contiguous 1..30000, all `complete`;
      - matches the evidence seat's exact densities on all 5040 N ≤ 5040 (0 mismatches);
      - matches the pool JSONs at every overlapping N.
    - **Fix:** "the listed pools carry the product certificate; the all-N scan fully factors each gcd (every factor proven prime)".

19. **LOW: the second-route e_p check has no artifact.**
    - Phrase: "e_p was recomputed by a second route (sympy's multiplicative orders) for the whole 5040 pool".
    - Source: no log or script in `erdos203/`; `pool.py` brute-forces e_p.
    - I re-ran it for **all 20 pool JSONs** with sympy `n_order` (`chk/pools.py`): 0 e_p mismatches, every (u,v) lattice spot-checked against 2^k3^ℓ ≡ 1, and every completeness certificate true.
    - **Fix:** add a log to the bundle (`chk/pools.py` will do).

20. **LOW: the numpy re-count of the forced configuration has no artifact.**
    - Phrase: "re-counted in numpy for the fully forced configuration (303936/518400, equal)".
    - Source: no log. My numpy re-count (`chk/wit.py`) gives 303936 ✓, and `fixed_720.bin` is bit-identical to 3ℤ² ∪ 5ℤ² ∪ {k≡2, ℓ≡0 (4)} (103680 points).
    - **Fix:** add the log.

21. **LOW: two raw `<` characters in the body.**
    - "143/140 < 25/24" and "lcm < 5040".
    - They render, but are invalid HTML. **Fix:** `&lt;`.

22. **LOW: the bundled README has the wrong threshold.**
    - The README says the perfect-power threshold is 1.08066. `frontier.out` and the exact value give **1.080623**: 1 − 0.0511363 − 303936/518400 + 517/720.
    - The page's "1.0806" is ✓.
    - **Fix:** correct the README to 1.08062.

23. **LOW / UNSUPPORTED: the FFK conjecture attribution cannot be checked from the given sources.**
    - Phrase: "Filaseta, Finch and Kozek conjecture there is no other kind".
    - The thread (TerenceTao, 19 Oct 2025) supports only "it is believed that all Sierpinski numbers either come from covering systems, or are perfect powers", without naming FFK.
    - **Fix:** confirm against the FFK paper (correct DOI in item 2) or soften to "it is believed".

24. **LOW (precision): "Theorem A alone rules out every covering system with period dividing 5040".**
    - For a covering that omits 5 or 7, the exclusion comes from the density condition (≤ 143/140 − 1/6 < 1), not from Theorem A.
    - **Fix:** "Theorem A plus the density condition".

## Checked and OK (computed, not trusted)

- **e_35 and Theorem A:**
  - ord₃₅ 2 = 12;
  - powers of 2 mod 35 are 1, 2, 4, 8, 16, 32, 29, 23, 11, 22, 9, 18 exactly, and 3 is not among them;
  - e₃₅ = 24 = 4·6 (also e₉₁ = 72, e₁₄₃ = 60).
- **Transversal pairs:** 271 of 465, recomputed from scratch via |⟨2,3⟩ mod pq| = e_p·e_q (194 non-transversal). `pairs_5040.json` agrees.
- **Pool densities:**
  - 143/140 = 1.021429 < 25/24;
  - 5040 = 31 primes; 55440 = 55 primes, 21493/18480 = 1.163041; 720720 = 99 primes, 1.248958 → 1.2490;
  - 10080 1.0319, 20160 1.0367, 40320 1.0411 (all < 1.04167);
  - 60480 1.0633, 65520 1.1035, 110880 1.1777, 166320 1.1913, 221760 1.1826, 332640 1.2064.
  - All 20 pools are complete by certificate.
- **The scan:** 30,000 rows, all `complete`. The only N < 5040 runners-up are 3960 = 0.933081 and 3600 = 0.930278. The max density for N ≤ 30,000 is 1.0656 (25200).
- **Block maxima:**
  - {5,7} 54/144 = 9/24;
  - S4 1765/3600, loss 0.109722;
  - S5 30580/57600, loss 0.131597;
  - S6 294900/518400, loss 0.149190;
  - S7 303336/518400, loss **0.166250** exactly (86184/518400 = 133/800);
  - S7 configs = 6,220,800 on T = 720;
  - `subsets_S7.json` has 128 keys.
- **Derived numbers:**
  - 1.16625 − 1.163041 = 0.003209;
  - 85.5%: U(S7) + 143/140 − Σ_S7 = 0.855179.
- **Frontier (re-run independently):**
  - Pure: every N ≤ 30,000 excluded (worst 0.9177 at 27720); 55440 (0.9968), 60480 and 65520 excluded.
  - Perfect power: every N ≤ 30,000 excluded (worst 0.9850). 30240, 40320, 45360, 50400 (0.9960) and 60480 excluded; 55440 (1.0824) and 65520 (1.0229) not.
- **Theorem C numbers:**
  - 0.586296 = 303936/518400 (d = 15 and others, and d = 720);
  - unconstrained 0.568866;
  - Σ_{q≥7} 1/q² = 0.0511363 (via P(2) and by a direct sieve to 10⁷);
  - threshold 1.080623 → "1.0806" ✓;
  - 30 values of d = gcd(N₀, 720).
- **Item 8:** the page does not claim CP-SAT proved S6 ✓. The CP-SAT optima for S4 and S5 are true (re-run).
- **"303936/518400":** ✓.
- **Forum:**
  - Comments (15), with 15 signatures in the saved HTML.
  - Signatures follow their comments: AnimishSharma 07:36 21 Jun 2026 = the "I have been studying the r = 2 case" comment; veljjanoski 09:43 15 Sep 2026 = the "computational attempt" comment.
  - 71.7% at 5040 (31 primes) and 76.0% at 55440 (55 primes) ✓; "only 77 pairs are nested" supports "almost never nested".
  - AnimishSharma's "lcm < 5040 … p ≤ 50,000,000" ✓.
  - veljjanoski's 31/1.021, 55/1.163 and 99/1.249 (repo README) agree.
  - The page makes no "15 comments read" claim; the README's claim is supported.
- **Links:** all URLs are well-formed. The bundle URL path `verification/203/covering-forced-loss` matches `bundle.sh`. The forum URL format matches site convention. The problem-page source "[ErGr80, p. 27]" ✓.
- **JS/HTML:**
  - the object parses in node;
  - 0 backticks and 0 `${` in the body;
  - no smart quotes;
  - all tags balanced (p 8, strong 15, em 166, sup 26, sub 56, a 1);
  - `status: "partial"` is a valid STATUS key;
  - no existing #203 entry or slug collision.

## Count by severity

| Severity | Count | Items |
|---|---|---|
| HIGH | 5 | 1 title tags, 2 wrong DOI, 3 the ≥ 1.16625 overclaim, 4 the "every covering wastes 1/24" overclaim, 5 "period above 65,520" |
| MED | 6 | 6 three implementations for S7, 7 backwards parenthetical, 8 "first pools", 9 "up to 332640", 10 missing judgment report / "both read the bundle", 11 "none of this is a proof" |
| LOW | 13 | 12–24 |
