# Referee report — seat `world` — citations, numerics, and the world (family 076, sib1 "Asymptotically minimal maxima of real Littlewood polynomials", 23 Sept 2026)
Seat started 2026-10-12 (~09:2xZ). Status: COMPLETE — verdict at the bottom.

## Scope read (pages)
sib1 pp. 25–26 (bibliography) + every in-text use of each reference (pp. 1–24); Appendix A pp. 23–24 (computations only).

## Method
(1) For each bibliography entry: does it exist (arXiv abs / DOI / publisher page), and does the cited locator say what sib1 uses it for —
quoted from the pre-fetched PDF text where available, else fetched, else COULD NOT FETCH.
(2) Numerics in /tmp/oaimath/076/seats/world_work/ (nice -n 19 python3): brute-force m_N, N ≤ 20; Erdélyi bound check; App. A computations.
(3) World: web search for expert reactions, tracker / Formal Conjectures status, openai/math issues, independent Lean builds.

## Findings (running)

### W1 — Erdős 1957 Problem 22 is the COMPLEX-unimodular question (= erdosproblems #230), not the real-sign one (#1150). EXPOSITION (citation placement)
sib1 p.2 ll.5–8: "Erdős's original question allowed complex unimodular coefficients and was refuted in that class by Kahane; the
restriction to real signs is the question addressed here [12, Problem 22]; see also [17] and [15, Problems 4.13 and 4.31]."
Source fetched: Erdős, "Some unsolved problems", Michigan Math. J. 4 (1957) 291–300, scan from the Rényi Erdős archive
(users.renyi.hu/~p_erdos/1957-13.pdf; world_work/erdos57/), p. 297, read from the rendered page image:
  "22. If P(z) = Σ_1^n a_k z^k, where |a_k| = 1 for all k, then max_{|z|=1} |P(z)| ≥ √n, by Parseval's Theorem. Does there exist a
   universal constant c > 0 such that, for n ≥ 2, the maximum is at least (1 + c)√n? I have an unpublished proof that if
   P(θ) = Σ_{k=1}^n ε_k cos kθ (ε_k = ±1), then max_{0<θ<2π} |P(θ)| > (1 + c)√(n/2)."
So Problem 22 ASKS the unimodular question; its only ±1 content is a claimed (unpublished) theorem about COSINE polynomials
normalised by √(n/2) — not the question m_N ≥ 1+c. erdosproblems.com/230 (fetched today via a non-blocked egress) lists exactly this
source, "#230: [Er57,p.297][Er61,p.248][Ha74][Er80h,p.385]", states the unimodular problem, and records "The answer is no ... Kahane
[Ka80]". erdosproblems.com/1150 cites "[Ha74,4.31][Va99,2.36]" and does NOT cite Er57. ⇒ DanielChin's 04 Feb 2026 remark in the #1150
thread ("problem 22 in [Er57] ... reads like [230]") is CORRECT. As a source for "Erdős's original question" [12, Problem 22] is right;
as a source for "the restriction to real signs" (the reading the sentence's punctuation invites) it is wrong — the real-sign question's
locators are [15] Problems 4.13/4.31 (see W2). Not a mathematical issue; no effect on any proof.
Side remark (no conflict): Erdős's claimed cosine bound max|Σε_k cos kθ| > (1+c)√(n/2) is compatible with Theorem 1.1, since
|Re P| ≤ |P| ≤ (1+η)√N only bounds the cosine sum by ≈ √2·√(N/2).

### W2 — Hayman–Lingham Problems 4.13 and 4.31 (arXiv:1809.07200v2 = current version, 21 Sep 2018) say what sib1 uses them for. OK
Problem 4.13 (p. 75 of the book PDF): "It is known that there exists a polynomial P(z) = Σ_{k=1}^n ε_k z^k, ε_k = ∓1 for which
max_{|z|=1}|P(z)| < C_1√n. (4.2) (See Clunie [158]). Is it necessarily true that C_1 > 1 + A if (4.2) holds, where A is a positive
absolute constant?" Update 4.13: "No progress on this problem has been reported to us."
Problem 4.31 (pp. 81–82): "Erdös and Newman conjectured that if f(z) = Σ_{k=0}^n a_k z^k, |a_k| = 1, 0 ≤ k ≤ n, (4.5) then there is an
absolute constant c such that max_{|z|=1}|f(z)| > (1+c)n^{1/2}. (4.6) The weaker form of our conjecture stated that (4.6) holds if we
assume a_k = ±1 (Problem 4.13). ... However, (4.6) was disproved by Kahane (no citation). ... It would be worthwhile to determine if
(4.6) holds for a_k = ±1 and for a_{n_k} = ±1. (P. Erdös and D. Newman)". Update 4.31: "No progress ... reported to us."
⇒ sib1 p.2 "The distinction between the unimodular and real-sign questions is also explicit in [15, Problem 4.31]" — accurate; 4.13 is
precisely the real-sign question (length n, z^1..z^n; Theorem 1.1's "length N" matches). erdosproblems #1150 also cites [Ha74,4.31].

### W3 — Numerics: exhaustive m_N for N ≤ 20 (world_work/mN_bruteforce.py → mN_output.txt; cross-check mN_crosscheck.py → mN_crosscheck_output.txt). Consistent with the paper; no claim of the paper is numerical. OK
Method (rigorous up to float rounding): all 2^(N−1) vectors with ε_0=+1; |P|² is a real trig polynomial of degree n=N−1, so a grid of
M points gives grid-max g with g² ≥ ‖P‖²_∞(1 − n²π²/(2M²)) (Taylor at the maximiser + Bernstein twice); stage 1 (M=1024) discards
every vector whose grid-max exceeds U = min g/√(1−r); survivors get a 2^16 grid + golden-section refinement. Independent cross-check:
direct Horner evaluation of every reported minimiser on 2^20 points (agrees to 1e-9), and for N ≤ 14 all 2^N vectors with no symmetry
reduction on a separate full-circle grid (agrees).
  N:      1      2      3      4      5      6      7      8      9     10
  m_N: 1.0000 1.4142 1.2910 1.3303 1.3416 1.4329 1.1730 1.2887 1.3726 1.3862
  N:     11     12     13     14     15     16     17     18     19     20
  m_N: 1.1464 1.2808 1.2739 1.2883 1.2910 1.3085 1.3265 1.2901 1.2830 1.3258
(min ‖P‖_∞ exactly 2, √5, 3, 5 at N = 2, 3, 5, 15; full brackets and a minimising sign word per N in mN_output.txt.)
Printed tables compared:
 • Odlyzko, "Search for ultraflat polynomials with plus and minus one coefficients" (Connections in Discrete Mathematics, CUP 2018;
   author preprint revised 18 May 2017, www-users.cse.umn.edu/~odlyzko/doc/ultraflat.pdf, fetched): his M_n = min max|F|/√(n+1) over
   degree n is our m_{n+1}. Exhaustive for n ≤ 52. His "online tables" are not at the URL he gives any more (home page has no such
   link; COULD NOT FETCH the tables), so the comparison is against his Fig. 1 (n = 10..50) read off the rendered page: M_10 ≈ 1.145,
   M_11 ≈ 1.28, M_12 ≈ 1.275, M_13 ≈ 1.29, M_14 ≈ 1.29, M_15 ≈ 1.31, M_16 ≈ 1.325, M_17 ≈ 1.29, M_18 ≈ 1.28, M_19 ≈ 1.325 — matches
   our m_11..m_20 to plot resolution.
 • Georgiev–Gómez-Serrano–Tao–Wagner, arXiv:2511.02864v3 (= current, 22 Dec 2025), §6.13 Problem 6.28, Figure 16 (right) is the only
   place their numbers appear (a plot, degrees 10–89, NOT tabulated; the text says "for n ≤ 100"). Read off the zoomed render:
   degree 10 ≈ 1.32, 11 ≈ 1.10, 12 ≈ 1.23, 13 ≈ 1.23, 14 ≈ 1.245, 15 ≈ 1.25, 16 ≈ 1.27, 17 ≈ 1.29, 18 ≈ 1.255, 19 ≈ 1.25, 20 ≈ 1.29;
   rising to ≈ 1.35–1.41 at degrees 55–89; no value below 1.097 anywhere. ⚠ At degrees 11–19 these plotted values lie BELOW the exhaustive
   minimum (e.g. degree 11: plotted ≈ 1.10 vs exhaustive 1.2808 by us and ≈ 1.28 by Odlyzko). So Figure 16's small-degree points cannot be
   true sup norms — consistent with their stated evaluator (max over a mesh {e^{2πik/K}} with a misprinted "K = 6, 7", which under-reads
   the max). This is a defect of [14], not of sib1; sib1 only says "their computations do not give an asymptotic theorem" (p.3), which
   is true. Their text also quotes Odlyzko's extrapolated limits "lim C+ ≈ 1.27, lim C− ≈ 0.64, lim C^w ≈ 0.79".
EXPOSITION (scholarly omission, sib1 p.3 / bibliography): sib1 never cites Odlyzko [Od18], the exhaustive search (n ≤ 52, plus
skew-symmetric to n = 104) whose stated conclusion is "The computations reported here suggest that M ≈ 1.27 ... These conjectures imply
that ultraflat polynomials in U_n do not exist" and "Fig. 1 shows M_n converging rapidly". Theorem 1.1 says M = 1, so it falsifies that
numerically-based conjecture and implies the observed plateau ≈1.27–1.33 for n ≤ 100 is pre-asymptotic. That is not a contradiction
(sib1 p.2: "no useful convergence rate ... is asserted"), but it is the strongest published evidence pointing the other way and the
paper should engage with it. Erdélyi (2608.00744, p.2) likewise records "It is a common belief that the analogous Erdős conjecture for
L_n is true". Our N ≤ 20 data show no decrease toward 1 either (m_N ∈ [1.146, 1.433]); they cannot bear on a limit statement.

### W4 — Erdélyi bound check. OK
2608.00744v1 (current) Theorem 2.1 verbatim: "We have max_{t∈R} |P_n(e^{it})|² ≥ n + 1 + (1/38) n^{1/3} for every polynomial P_n ∈ L_n"
with L_n = degree-n (n+1 coefficients) ±1 polynomials. In length N this is N + (N−1)^{1/3}/38 — sib1 p.3's transcription is exact.
Against the exhaustive minima (appA_and_erdelyi_output.txt) it holds for every N ≤ 20 with large slack (N=20: 35.15 vs 20.07; N=1
equality 1=1). Erdélyi's abstract says "an Erdős problem dating back to 1957" and his p.2 attributes "(Problem 22 in [Er57])" to the
UNIMODULAR class K_n and says "For the more restricted class L_n the analogous Erdős conjecture is unsettled to this date" — agrees with W1.

### W5 — Appendix A computations (appA_and_erdelyi_check.py → appA_and_erdelyi_output.txt). All three are CORRECT. OK
 (a) A.1 Dirichlet kernel: |D_q(t)| ≤ 1/sin(πd) off (−d,d) (|t| ∈ [d,1/2]); |D_q| ≥ 2q/π on |t| ≤ 1/(2q) (sin(πq|t|) ≥ 2q|t|,
     sin(π|t|) ≤ π|t|); hence ∫_{T\E}|D_q|^α ≤ sin(πd)^{−α}, ∫_T|D_q|^α ≥ (2/π)^α q^{α−1}, ratio → 0 for α > 1, so B_α(E) = 1.
     Re-derived by hand; numerically both printed bounds hold and ∫_E/∫_T → 1 for d ∈ {0.05,0.2,0.45}, α ∈ {1.5,2,4}, q up to 1000
     (e.g. d=0.05, α=2: 0.775, 0.980, 0.998 at q = 10, 100, 1000). D_q ∈ I (E_0 = {0,…,q−1}). Note the claim is only for α > 1
     (at α = 1 the ratio does not tend to 1); the contrary paper's use is α = 2p ≥ 4, so fine.
 (b) A.2: the PDF (rendered p.24) has a_j = 2^{j²}, NOT 2^j as the seat prompt paraphrased. With 2^{j²}: exact rational arithmetic
     confirms for n = 1..40 that Σ_{j<n}a_j²/a_n² ≤ (n−1)2^{−4n+2} ≤ 1, S_n ≤ 2a_n² ≤ (2/n²)Σj²a_j² (so (46) holds with K = 2),
     Σ_{j<n}a_j/a_n ≤ (n−1)2^{−2n+1}; measured max_{|z|=1} | |P|/√S_n − 1 | = 1.3e−1, 3.5e−2, 8.1e−3, 4.9e−4 at n = 2, 3, 4, 6 → 0.
     (With the paraphrase 2^j, (46) with K = 2 still holds but |P(1)|/√S_n → √3, so the example would fail; the paper's 2^{j²} is
     the right one.) Whether (46) is exactly [9]'s hypothesis is seat `reduce`'s scope.
 (c) A.2 identity: P = 1+z, z = 1, z′ = i: |P(z) − P(z′)| = |1 − i| = √2, while σ·2 + τ·√2 ∈ {±3.414, ±0.586}; none equals √2. Correct.
 (d) A (p.23) endpoint remark: flipping one sign changes P by exactly 2z^k, so two flips cost ≤ 4, i.e. ≤ 4/√N normalised. Correct.

### W6 — Bibliography audit, entry by entry (existence = Crossref DOI metadata / arXiv abs page fetched today; content = source text read)
Every one of the 23 entries EXISTS with the printed venue/volume/pages/year (Crossref: [1] 10.1007/s00373-005-0628-x GC 21(4) 377–384
2005 ✓; [3] 10.4007/annals.2020.192.3.6 Ann. 192(3) 977–1004 ✓; [4] 10.1007/bf02579452 Comb. 1(4) 319–325 ✓; [5] 10.4171/jems/163 JEMS
11(3) 627–703 ✓; [7] 10.1016/s0304-3975(98)00121-2 TCS 209(1–2) 377–387 ✓; [12] 10.1307/mmj/1028997963 MMJ 4 ✓; [13]
10.1016/s0195-6698(85)80045-7 EJC 6(4) 317–326 ✓; [16] 10.1016/j.aim.2013.03.015 AiM 241 127–136 ✓; [17] 10.1112/blms/12.5.321 BLMS 12(5)
321–342 ✓; [18] 10.1112/jlms/s1-41.1.367 JLMS s1-41 367–376 ✓; [19] 10.1137/130929400 SICOMP 44(5) 1573–1582 ✓; [21]
10.1016/0097-3165(89)90074-5 JCTA 51(1) 24–42 ✓; [22] 10.1090/s0002-9939-1959-0116184-5 PAMS 10 855–859 ✓; [23]
10.1090/s0002-9947-1985-0784009-0 TAMS 289(2) 679–706 ✓). arXiv versions cited are the CURRENT versions in every case (abs pages fetched
today): 0707.3023v2, 1203.5747v2, 1609.03435v2, 1809.07200v2, 1909.08777v1, 2504.21499v1, 2509.04212v1, 2608.00744v1, 2511.02864v3.
In particular el Abdalaoui has posted NO new version of 2504.21499 / 2509.04212 / 1609.03435 since his 16 Aug 2026 forum promise that
comments "will be taken into account in the next version".
Locator-by-locator (what sib1 uses it for → what the source says):
 [2] Balister Thm 1 (1909.08777v1, read): "|P_{<n}(z)| ≤ √(6n−2) − 1 for all n ≥ 1 and |z| = 1", P_{<n} = first n Rudin–Shapiro terms,
     sharp at n = (2·4^k+1)/3, z = 1. sib1 p.2 (rendered) "the all-length bound √(6N−2) − 1 for its initial segments" ✓.
 [3] BBMST Thm 1.1 (1907.09464v1, the only arXiv version): "There exist constants Δ > δ > 0 such that, for all n ⩾ 2, there exists a
     Littlewood polynomial P(z) of degree n with δ√n ⩽ |P(z)| ⩽ Δ√n for all z ∈ C with |z| = 1." Annals landing page
     (annals.math.princeton.edu/2020/192-3/p06, fetched): abstract states the identical theorem; received 22 Jul 2019, revised 16 Sep
     2020. The Annals body is paywalled — COULD NOT FETCH, so whether "[3, Sections 4–5]" (p.18) matches the PUBLISHED section numbers is
     unverified; in arXiv v1 §4 "Minimising Discrepancy" states the partial-colouring lemma as "Lovett and Meka [34, Theorem 4]" and §5
     "The odd sine polynomial" uses it to choose ε_k — what sib1 says. Minor: sib1 cites the Annals version but reads arXiv numbering.
 [5] Bombieri–Bourgain (EMS Press open-access PDF fetched, 10.4171-jems-163.pdf): §2 "First steps for Theorems 2 and 3" = smoothed
     quadratic phase Φ(x)=(x²−x)/2 "As in Littlewood [17]" + Poisson summation; Eq. (2.2) is the quadratic Fourier-inversion identity
     ∫χ_α(y)e(n(ξ_h−y)²/2)dy = e(1/8)n^{-1/2}χ_α(ξ_h) + e(1/8)n^{-1/2}∫χ̂_α(y)e(ξ_h y)(e(−y²/2n)−1)dy; §7 "The Fourier coefficients of P1"
     (Poisson summation); §8 "The Körner correction". sib1 pp.2, 10, 15 locators ✓ all four.
 [7] Downarowicz–Lacroix (author manuscript, refs/downarowicz_lacroix): Def. 2 "The merit factor of A is 1/(2M_A)", M_A = Σ|Φ_A(n)|²,
     Φ_A(n) = (1/a)Σ A(k)A(k+n) ⇒ a²/(2ΣC_u²) = sib1's F(A) ✓; Lemma 0 "2M_A = ‖P_A‖_4^4 − 1" ✓; manuscript p.3: "the hypothesis on
     boundedness is called the Turyn's conjecture, or, equivalently, the Erdös L4-norm conjecture" ✓; Thm 2: "There exist binary words with
     arbitrarily large merit factors if and only if there exists a binary Morse flow (X,S,µ) such that the Fourier transform of the spectral
     measure µ_f of the 'zero coordinate function' belongs to ℓ². In particular, the spectrum of (X,S,µ) is then simple and not purely
     singular." Unique ergodicity is in the proof ("Fact 1"). sib1 p.3 paraphrase ✓ (hypotheses at point of use: seat `round`).
 [11] Erdélyi Thm 2.1 ✓ (W4). [12] Erdős 1957 Problem 22 — see W1 (EXPOSITION). [14] Georgiev et al — see W3.
 [15] Hayman–Lingham 4.13/4.31 ✓ (W2).
 [16] Jedwab–Katz–Schmidt (arXiv:1205.0260v2 = accepted version, fetched): Thm 1.1 "There is a sequence h_1, h_2, … of Littlewood
     polynomials with deg(h_n) → ∞ and ‖h_n‖_4/‖h_n‖_2 → c^{1/4} as n → ∞, where c < 22/19 is the smallest root of 27x³ − 498x² + 1164x
     − 722"; Cor. 3.2 is the matching lower bound/equality case for the generalized Fekete family. Merit factor = 1/(c−1); computed:
     c = 1.157677431123647…, 1/(c−1) = 6.342061719763943… (also the largest root of 29x³ − 249x² + 417x − 27) — sib1's "6.342061…" ✓.
     "improving the previous proven value 6" ✓ (JKS intro: Høholdt–Jensen 1988, ratio (7/6)^{1/4} ⇒ merit factor 6). Note: [14] prints
     this constant as "6.340261…" — a digit transposition in Georgiev et al., not in sib1. JKS intro also calls Problem 22 the unimodular
     conjecture ("[13, Problem 22] ... for all non-constant polynomials f whose coefficients have absolute value 1") — agrees with W1.
 [17] Kahane 1980 — paywalled (Wiley), not fetched; the cited content ("Kahane obtained ultraflatness", unimodular class) is corroborated
     by four independent secondary sources read today (erdosproblems #230; Erdélyi 2608.00744 p.2; Hayman–Lingham 4.31; BB09 intro).
 [18] Littlewood 1966 — paywalled, not fetched; "Littlewood used quadratic phases" corroborated by BB09 §2 ("As in Littlewood [17], we
     choose Φ(x) = (x²−x)/2").
 [19] Lovett–Meka arXiv v2 Thm 4 (read): "Main Partial Coloring Lemma ... Σ_j exp(−c_j²/16) ≤ n/16 ... finds a point x ∈ [−1,1]^n
     such that (i) |⟨x − x_0, v_j⟩| ≤ c_j‖v_j‖_2 (ii) |x_i| ≥ 1 − δ for at least n/2 indices". It gives |x_i| ≥ 1−δ, NOT exact signs;
     sib1 p.18 handles this explicitly ("Letting η tend to zero and taking a convergent subsequence ... closed under limits") ✓.
 [20] OpenAI companion: exists in github.com/openai/math/preprints/A-smooth-three-torus-diffeomorphism-with-simple-Lebesgue-spectrum-
     September-23-2026/paper.pdf (dir listed today; unchanged since the repo's initial commit adc7f124); text (refs/oai_companion20, fetched
     by another seat) Thm 1.1: "There exist a C∞ volume-preserving diffeomorphism T : T³ → T³ and a real function f ∈ L²_0(T³, µ) such
     that {f ∘ T^n : n ∈ Z} is an orthonormal basis of L²_0(T³, µ)." — matches sib1 p.23's description ✓ (an unrefereed OpenAI preprint).
 [22] Rudin 1959 Thm I — COULD NOT FETCH (ams.org Cloudflare challenge from exe.dev and from Hetzner; residential proxy returned 407;
     seat `reduce` also failed, refs/rudin1959/NOTE.txt). The claimed content (|P|²+|Q|² = 2N at N = 2^k ⇒ ‖P‖_∞ ≤ √(2N)) is a one-line
     identity; checked numerically instead: our exhaustive m_N ≤ √2 at N = 2, 4, 8, 16 (1.414, 1.330, 1.289, 1.309) as it must be.
     History "obtained earlier by Shapiro and independently by Rudin" agrees with Balister p.1 and BBMST §3.
 [1], [4], [13], [21], [23]: existence ✓; content at point of use is seats `construct` (Alon–Yuster Lemma 2.1, fetched by them as the
     author PDF) and `round` (Beck/Spencer). Attributions ("near-perfect-packing lineage of Frankl and Rödl", "partial-coloring method of Beck
     and Spencer") are standard and agree with BBMST §4 ("partial colouring lemma of Spencer [44] (whose proof ... was based on a technique of
     Beck [2])").
Verdict on (1): no citation says something other than what it is used for, except the [12, Problem 22] placement (W1, EXPOSITION) and the
omission of Odlyzko (W3, EXPOSITION). Paper copies on disk are byte-identical to the repo blobs (git hash-object: sib1 c92e8a48…, sib2
e5c191c4…, family e5c95210… = the blob SHAs in openai/math main today).

### W7 — The world (as of 2026-10-12). A helper seat ran the search; every query/URL tried is logged in world_work/world_search.md
(raw downloads in world_work/raw/). I re-checked the load-bearing items against the raw files myself (marked ✔).
 • erdosproblems.com/1150 (fetched via Hetzner; exe.dev gets a Cloudflare 403): unchanged, "This page was last edited 23 January 2026",
   NO status shown — but since Bloom's 6 Oct post "Changes" (forum/thread/blog:9) the site shows no status for ANY problem ("The site will
   not display the statuses of any problems") and has frozen comments/proof claims, so the absence says nothing. The #1150 thread is
   text-identical to the saved copy; newest comment el Abdalaoui 16 Aug 2026; proof claims: none. /history/1150 shows only the current version.
 • Bloom, "Erdős problems in the OpenAI proofs", 8 Oct 2026 (forum/thread/blog:10) ✔: lists [1150] "Ultraflat Littlewood polynomial":
   "This PDF claims a proof of the following. For every ε>0, and for all large N, there are signs ε_i ∈ {−1,1} such that |Σ_{0≤k<N} ε_k z^k|
   < (1+ε)√N for all z with |z|=1. In other words there exist 'ultraflat' polynomials. The weaker bound of ≪√N was proved by [BBMST20]."
   with the post-wide disclaimer "I have not yet looked at in any serious way any of the proofs ... nor ... checked myself that the
   formalisation compiles ... This post should not be read as any kind of endorsement". None of its 9 comments concerns 1150. (Note: Bloom
   calls the ONE-sided bound "ultraflat" and links the 16-page two-sided PDF, while the formalisation he links is sib1's one-sided theorem.)
 • Formal Conjectures — STATUS CHANGED ✔ (refs/fc_1150/1150.lean and world_work/raw/fc_1150.lean agree): ErdosProblems/1150.lean now
   `@[category research solved, AMS 12 30, formal_proof using lean4 at "…openai/math/blob/adc7f124…/lean/OAI/Analysis/Littlewood/Main.lean#L187"]`
   with `answer(False)` and docstring "No. This was disproved by an internal OpenAI model in September 2026 [OAI26a]". Commit 3dfd999dfe,
   2026-10-11, PR #6898 (Moritz Firsching; approved by Paul-Lez). The PR's own checks: build, link resolution, grep for `sorry`, config
   inspection; Firsching: "#print axioms, Comparator" NOT executed; reviewer notes flag "Erdős 1150 (length vs degree)" as a transport not in
   the linked proof. (That transport is trivial: FC states degree n with √n; OAI gives length N = n+1 with (1+η)√(n+1); take η = c/2 and n
   large.) Open FC issue #6986 / PR #6991 (anxkhn) adds Theorem 1.1 separately "not two-sided uniform ultraflatness", no proof link
   ("The external proof was not built locally").
 • openai/math: has_issues=false, has_discussions=false — there is NO issue tracker to search; only PR #1 (OpenAI's own 8 Oct sync).
   history.md (7 Oct): 3 withdrawals (Weil classes / Kuga–Satake / Hodge for K3 products) + 14 revisions — none in family 076 (✔ I read
   history.md). All 076 preprint dirs and all lean/OAI/Analysis/Littlewood files have exactly one commit, adc7f124 (✔ `gh api commits?path=`).
   CONTENTS.md's 076 headline claims two-sided "(1+o(1))√N uniformly on the entire unit circle ... ultraflat, including at the real
   endpoints"; lean/docs/076.md scopes the formalisation to the one-sided max bound + finite-exponent flatness — i.e. the two-sided headline
   is NOT what is formalised (irrelevant to #1150, which needs only the one-sided bound).
 • Independent MACHINE checks of the Lean (not human review): carlostoledo1891/cert-machine ✔ (corpus/openai-math/kernel-runs/38017370880/
   AsymptoticallyMinimalLittlewood.json: "okay": true, "Lean default kernel accepts the solution", "nanoda kernel accepts the solution",
   Lean 4.34.1, "Build completed successfully (8947 jobs)", exported axioms propext/Quot.sound/Classical.choice, pinned to openai/math
   fd4aeeb2, run 2026-10-10; its own caveat "It does not mean the paper's claim is proved" and Comparator's AF_UNIX sandbox guard "is NOT
   applied" on GitHub runners). plasma-ai/erdos (erdosproblems.ai): claims it built the module, printed axioms (propext, Classical.choice,
   Quot.sound), matched the comparator fingerprint, recorded 2026-10-07; "Not reviewed: no outside reviewer or independent acceptance of the
   result is recorded" (who/what ran it — human or AI — not stated). Not registered on Palomar (Bloom's stated source for linking Lean).
 • Human expert reactions specific to 076 — found three, none a verification: Gil Kalai blog 7 Oct ✔ ("The new manuscript announces
   polynomials with N such coefficients whose modulus is (1+o(1))√N uniformly on the entire unit circle, answering that stronger question");
   MathOverflow answer 515866 by mathworker21, 2026-10-09 01:08Z ✔ ("I, and I think many others, thought there would be no ultraflat
   Littlewood polynomial."); Bloom 8 Oct (above). NO reaction found from Tao (blog + all Mathstodon posts since 3 Sep), Erdélyi,
   el Abdalaoui, Balister, Sahasrabudhe, Jedwab, Katz, Schmidt. No arXiv paper or new version reacting (el Abdalaoui's three preprints
   and Erdélyi's 2608.00744 all un-revised). HN: no story/comment mentioning Littlewood/ultraflat/Turyn since 23 Sep. Wikipedia "Littlewood
   polynomial" (edited 12 Oct) still says the ±1 problem "remains open in the peer-reviewed literature". One AI-generated derivative
   (jeff-kline/ultraflat-littlewood-rate, 10 Oct: explicit N₀ ≥ exp(exp(exp(10^12 log²(2/ε)))) for the two-sided paper; "No human expert
   has reviewed them").
 • COULD NOT FETCH / blind spots: Bluesky and Reddit APIs (403 from exe.dev and Hetzner), Lean Zulip (login; public archive stale at
   Feb 2026), nytimes.com, openai.com, Scott Aaronson's blog (429); X recent-search reaches only ~5–12 Oct. "No reaction found" is a claim
   about the places listed in world_search.md, not about the world.
 • Timeline: sib1 is dated 23 Sep 2026, but the openai/math repo was created 2026-10-06T21:47Z and Bloom dates the release "Tuesday 6th
   October"; no public trace of the manuscript before 6 Oct was found.

## External inputs checked (source · version · exact statement vs use) — summary; details and quotes in W1–W7
| ref | version read | statement vs use |
|---|---|---|
| [2] Balister | arXiv 1909.08777v1 (only) | Thm 1 √(6n−2)−1, all n ≥ 1 — matches p.2 |
| [3] BBMST | arXiv 1907.09464v1 + Annals abstract page | Thm 1.1 identical in both; Annals body (section numbers for "[3, §§4–5]") not fetched |
| [5] Bombieri–Bourgain | JEMS 11 (2009) open-access PDF | §2, Eq. (2.2), §7, §8 — all four locators match |
| [7] Downarowicz–Lacroix | author manuscript (refs/) | Def 2, Lemma 0, p.3 Turyn/Erdős L⁴, Thm 2 — match p.3 |
| [11] Erdélyi | arXiv 2608.00744v1 (only) | Thm 2.1 = N + (N−1)^{1/3}/38 in length N — exact |
| [12] Erdős 1957 | Rényi-archive scan, p.297 | Problem 22 is the UNIMODULAR question (= #230); W1 |
| [14] Georgiev et al. | arXiv 2511.02864v3 (current) | §6.13 Problem 6.28 + Fig. 16 (plot only; small-degree points below the true minimum — their defect) |
| [15] Hayman–Lingham | arXiv 1809.07200v2 (current) | Problems 4.13 (real-sign question) and 4.31 (Erdős–Newman, ±1 variant explicit) — match |
| [16] Jedwab–Katz–Schmidt | arXiv 1205.0260v2 | Thm 1.1 / Cor 3.2; 1/(c−1) = 6.342061719… recomputed — match |
| [19] Lovett–Meka | arXiv 1203.5747v2 (current) | Thm 4 gives |x_i| ≥ 1−δ; sib1 p.18 takes the limit explicitly — fine |
| [20] OpenAI companion | openai/math preprint (unchanged since adc7f124) | Thm 1.1 matches p.23 description |
| [8],[9],[10] el Abdalaoui | arXiv current versions (v2, v1, v1) | existence/versions only; content vs App. A is seat `reduce` |
| [1],[4],[13],[17],[18],[21],[22],[23] | Crossref metadata only | exist as printed; content not read by me (Alon–Yuster read by seat `construct`) |
| Odlyzko 2018 (NOT cited) | author preprint 18 May 2017 | exhaustive n ≤ 52, conjectures M ≈ 1.27 — contradicted by Thm 1.1 asymptotically; W3 |

## What I skimmed / did not check
- Did NOT read: Kahane 1980, Littlewood 1966, Rudin 1959 (COULD NOT FETCH — ams.org bot wall from two egresses, proxy 407), Pippenger–Spencer
  1989, Frankl–Rödl 1985, Beck 1981, Spencer 1985 (paywalled; existence via Crossref only), the Annals typeset BBMST, Odlyzko's online
  tables (dead link). Hypotheses-at-point-of-use of Alon–Yuster, Lovett–Meka, Downarowicz–Lacroix, Bonami–Révész and the el Abdalaoui
  preprints are other seats' scopes; I checked only that the cited locators exist and say what sib1 attributes to them.
- Did NOT run any Lean (per brief); the kernel results quoted in W7 are third-party records, read not reproduced.
- Numerics are N ≤ 20 only; they are a sanity check on definitions and on the Erdélyi bound, and cannot bear on a limit theorem.
- World search: Bluesky, Reddit, Lean Zulip, NYT, openai.com, Aaronson's blog unreachable; X only ~5–12 Oct.
- Did not read §§3–6, 8 of sib1 for mathematics (other seats).

## Verdict
HOLDS AS READ IN SCOPE — no citation is misused in a way that affects any proof; all 23 entries exist; App. A's three computations and
the Erdélyi transcription are correct; exhaustive m_N (N ≤ 20) agree with Odlyzko. Two EXPOSITION items: [12, Problem 22] is the
unimodular question (= erdosproblems #230), not the real-sign one (W1); Odlyzko's exhaustive data/conjecture M ≈ 1.27, the main published
evidence against the theorem, is not cited or discussed (W3). World: no human expert has verified or refuted 076; erdosproblems.com
shows no status for any problem (site policy since 6 Oct); Formal Conjectures flipped erdos_1150 to `research solved`/`answer(False)` on
11 Oct on source inspection only; two outside machine kernel checks (cert-machine, plasma-ai) accept `main`; no 076 file revised or withdrawn.

Status: COMPLETE (2026-10-12).
