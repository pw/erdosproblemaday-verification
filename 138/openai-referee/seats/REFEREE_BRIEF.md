# Hostile referee brief — OpenAI preprint "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026, 25 pp), family 160, Erdős problem #138 ($500)

ONE paper, anonymous author ("OpenAI"), github.com/openai/math `preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/paper.pdf`
(sha256 042acea3…, /tmp/oaimath/160/paper.sha256). Local copies: /tmp/oaimath/160/paper.pdf (PDF page = printed page), /tmp/oaimath/160/paper.txt
(pdftotext -layout; displayed math is MANGLED), and — USE THESE — the paper's own LaTeX source, clean:
/tmp/oaimath/604/lean-build/repo/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/{01-introduction,02-setup,03-counting,04-outer,05-dichotomy,06-perturbation,07-transfers,08-upper}.tex
(+ build/references.bib, build/figures/norm-band.tex). Quote from the TeX; cite by the TeX \label (e.g. count:local) AND the printed lemma number/page.
A Lean 4 formalization EXISTS and is catalogued: /tmp/oaimath/604/lean-build/repo/lean/OAI/Combinatorics/ProgressionColoring/ (115 files, 14,837 lines; Main.lean proves
`OAI.QuantitativeVanDerWaerden.uniform_lower_bound` = the comparator's statement, /tmp/oaimath/604/lean-build/repo/lean/ComparatorChallenges/QuantitativeVanDerWaerden.lean,
plus kthRoot_tendsto, exists_uniform_lower_bound, length_rate_tendsto). Our kernel replay is running in /tmp/oaimath/160/lean-build (steps.tsv) — do NOT run lean/lake
yourselves (memory guard on this box); read the Lean sources as text if your scope needs them.

THEOREM 1.1 (main:intro, p. 1). There is an absolute integer K_0 such that for every integer k ≥ K_0 and every integer r ≥ 2, W_r(k) > k^{ck⌊log₂ r⌋}, c = 10^{−5}.
Hence lim_k W_r(k)^{1/k} = ∞ for each fixed r ≥ 2. W_r(k) = least N such that every map [N] → [r] is constant on some a, a+d, …, a+(k−1)d with a,d ≥ 1, a+(k−1)d ≤ N.

WHY THIS MATTERS. erdosproblems.com/138 ($500; saved at /tmp/oaimath/160/live/e138.html, thread e138_thread.html, proof-claims tab EMPTY, last edited 2 June 2026):
"Improve the bounds for W(k) — for example, prove that W(k)^{1/k} → ∞." Page's best general lower bound: Kozik–Shabanov W(k) ≫ 2^k; Berlekamp W(p+1) ≥ p·2^p (p prime);
Fox–Hunter [FoHu26 = arXiv 2606.02541] resolved r ≥ 3: W_3(k) > 2^{k log* k / 4}. Erdős's $500 is explicitly for W(k)^{1/k} → ∞. Since the page's last edit:
Campos–Fox–Schildkraut arXiv 2608.20824 (21 Aug 2026, 5 pp; coloring found by ChatGPT 5.6 Sol Pro) proved W(k) ≥ (1−o(1))k·2^{k−1}, which settles W(k)/2^k → ∞
(the page's other question) but NOT the k-th-root question. THIS paper claims the k-th-root question for every r ≥ 2 including r = 2, with an explicit exponent.
Bloom's 8 Oct 2026 post lists #138 among the 25 problems the OpenAI release touches and among 12 on the FrontierMath Erdős list. Google DeepMind's Formal Conjectures
already marks `erdos_138` "research solved" on this Lean (saved: /tmp/oaimath/160/world/formal_conjectures_138.lean). The teorth community database still says open.

ARCHITECTURE (read 01-introduction.tex "The construction and its quantitative ingredient" first whatever your scope).
§2 (02-setup.tex): c = 10^{−5}, δ = 1/10, γ = 1/100, D = ⌈k^{1/10}⌉, M = ⌈k^{1/2}⌉, h_0 = D², p = k^{−1/20}, H = k^{−2}, η = 1/(1000D); dilation
λ = ∏_{ℓ ≤ h_0 prime} ℓ^{⌊log(2M)/log ℓ⌋} (Lemma setup:dilation: log λ ≤ h_0 log(2M); for 1 ≤ h ≤ 2M every prime-power divisor of h with prime ≤ h_0 divides λ, so
s = h/gcd(h, λt) is 1 or > h_0); Lemma setup:prime: a prime P ∈ (k, 2k²] (central binomial); q = least power of P ≥ k^{ck/D} (so k^{ck/D} ≤ q ≤ 2k²k^{ck/D}),
N = q^D, G = ℤ/Nℤ, gcd(λ,q) = 1; H_x = H/λ, α = q^{−(D+1)}; coordinates x_i(n) = n/q^i mod 1, y_i(n) = λx_i(n), representatives x̂ ∈ [0,1)^D, ỹ ∈ [−1/2,1/2)^D,
ρ(Y) = dist_T(Y, 1/2); partition U = intervals of width H_x (exact, H_x^{−1} = k²λ integral); partition V of [−1/2,1/2) geometric toward the cut ±1/2 with
R = log(1 + 1/(2α)), m = ⌈k²R⌉, a_ℓ = α(e^{ℓR/m} − 1); labels 𝓛 = U^D × V^D, L(n). Lemma mesh:width: ¼H(ρ(Y)+α) ≤ |I| ≤ 2H(ρ(Y)+α) ≤ 2H for Y ∈ Ī, |V| = 2m = O(k³ log k).
Lemma mesh:neighbors: with w = |I| and N(I) = {Y : dist(Y, Ī) ≤ w}, every J meeting N(I) has |J| ≥ w/16 and N(I) holds ≤ 49 endpoints. V_η truncation (* when ρ < η);
Lemma mesh:truncated: on an arc of length ≤ 4H, V_η has ≤ 16004D breakpoints.
§3 (03-counting.tex): Lemma count:arrangement (sign vectors incl. equality of s affine hyperplanes in ℝ^e: ≤ (e+1)²(s+1)^e); Lemma count:global: log T_glob = O(D(log k + log λ))
= O(k^{3/10} log k) = o(M); Definition count:eligible (h_0 < h ≤ 2M, t ∈ {0..h−1}^D, s_i = h/gcd(h, λt_i), stationary s_i = 1 / rotating s_i > h_0; paths
X_z = x + (z/h)(t+u), Y_z = y + (z/h)(λt+v); regular position = ρ(Y_{z,i}) ≥ η in every rotating coordinate; eligible = (i) ≥ h/2 regular positions with pairwise distinct
full labels, (ii) |u_i| ≤ H_x, |v_i| ≤ H in rotating coords, (iii) |v_i| ≤ |V(Y_{z,i})| in every stationary coordinate at every regular z); Lemma count:local: the number of
(t, eligible pattern containing a given label β) pairs is ≤ (CDh)^{6D}, C absolute, INDEPENDENT OF THE ANCHOR INTERVAL'S WIDTH (the stationary drift bound is relative to width).
§4 (04-outer.tex): Lemma outer:lll (finite asymmetric local lemma, proved); Prop outer:coloring: a map c_*: 𝓛 → {0,1} with (i) in every cyclic progression with ≥ δk light
positions (light = label multiplicity ≤ k/M) each bit is on ≥ ¼ of the light positions, (ii) in every eligible recorded pattern each bit is on ≥ ¼ of its regular positions.
Proof: first family = rows (≥ ⌊L_0/w_max⌋ ≥ δM − 1 distinct labels each) of every light-position word, ≤ kT_glob events; second family = one event per (eligible pattern, h, t);
tails P(E) ≤ 2e^{−l(E)/8} via cosh; weights z_E = e^{−l(E)/32}; first-family total weight kT_glob e^{−(δM−1)/32} = o(1); second-family weight per label
Σ_{h>D²}(CDh)^{6D}e^{−h/64} = o(1); incident weight ≤ 1/500; criterion exp(−(1/32 + 2/500)l) ≥ 2e^{−l/8} for l ≥ 100.
§5 (05-dichotomy.tex): Lemma dichotomy:affinity (representatives in one box of widths ≤ 2H, 2kH < 1 ⇒ Z_j = A + jB on J); Lemma dichotomy:drift (closest return of a
heavy label: 1 ≤ h ≤ 2M, |u_i| ≤ H_x/(m_*−1) ≤ 2MH_x/k, |v_i| ≤ 4MH/k, v = λu as reals); Lemma dichotomy:path (t with x(n_j) = x(n_0) + (j/h)(t+u),
y(n_j) = y(n_0) + (j/h)(λt+v); gcd(t_1..t_D,h) = 1; incongruent indices mod h have distinct full labels); Lemma dichotomy:heavy-width (|v_i| ≤ (2M/k)|V(y_i(n_{j_*}))| at
every heavy index); Theorem dichotomy:main: every progression has (i) ≥ γk of each outer bit or (ii) ỹ(n_j) = A + jB for ALL j. Short periods h ≤ h_0: h | λ so the y-step is
w = v/h with k|w_i| ≤ 4MH/h < ½ and w_i ∈ q^{−i}ℤ (so w_i ≠ 0 ⇒ |w_i| ≥ α); a cut crossing would force every V-width below |w_i| and all labels distinct — contradiction ⇒ (ii).
Longer periods h_0 < h ≤ 2M: full blocks of length h are eligible patterns when they contain a heavy index (regular fraction ≥ 1 − D(4η + 1/h_0) > ½; distinct labels by
dichotomy:path; (iii) via mesh:neighbors + heavy-width with 2M/k ≤ 1/16), so Prop outer (ii) gives ≥ h/8 of each bit per such block; blocks without a heavy index are all light;
k − h − δk ≥ (4/5)k positions covered ⇒ ≥ k/10 ≥ γk of each bit ⇒ (i).
§6 (06-perturbation.tex): keys κ(n) = ((V(y_i(n)))_i, ⌊‖qỹ(n)‖²⌋); Lemma perturb:multiplicity: a key occurs ≤ 4 times on any progression (same V-box ⇒ affine lift by
dichotomy:affinity; separation ‖qỹ(n_j) − qỹ(n_{j'})‖ ≥ 1 via the coordinate a+1 where λ(n_j − n_{j'}) = q^a u, q ∤ u; a norm band meets each half of a line in length ≤ 1).
Lemma perturb:signatures: T_aff ≤ C T_glob (k(Dq²+2))³, log = o(pk) (the ⌊f(n_j)⌋ word of an affine progression is a quadratic θ_0 + θ_1 j + θ_2 j² compared with ≤ k(B_*+1)
integers, arrangement in ℝ³). Theorem perturb:cyclic: C(n) = c_0(n) + E_{κ(n)} mod 2 with independent Bernoulli(p) E_κ; rich case R_k ≤ 2q^{2D}p^{γk/4} =
exp((2c − γ/80)k log k + o(k log k)), 2c − γ/80 = −21/200000 < 0; affine case A_k ≤ 2T_aff(1−p)^{k/4} = exp(−pk/4 + o(pk)); dichotomy covers everything ⇒ a coloring of ℤ/q^Dℤ
with no monochromatic nonzero-step k-progression, q^D ≥ k^{ck}.
§7 (07-transfers.tex): Prop transfer:product (digit product: a cyclic coloring of ℤ/Nℤ with no mono k-AP of nonzero step gives W_{2^m}(k) > N^m, hence
W_r(k) > N^{⌊log₂ r⌋}); proof of Theorem 1.1; Theorem transfer:large-r (W_r(k) > exp((log r)²/(64 log 2)) for r ≥ 256, k ≥ 3, Behrend digits + squared norm);
Corollary transfer:limits. §8/Appendix (08-upper.tex): elementary finite upper bound F(r,k) and the boundary values W_r(1) = 1, W_r(2) = r + 1, W_1(k) = k.

WHERE THE PROOF GOES BEYOND THE STATE OF THE ART (test these hardest). The best previous r = 2 bound is exponential (Kozik–Shabanov c·2^k; CFS26 k2^{k−1}); Fox–Hunter's
superexponential bound needs r ≥ 3 and uses a Behrend-type covering that is unavailable at two colors. So the new content is precisely the two-color cyclic construction of §2–§6,
and the whole weight sits on: (a) Lemma count:local's (CDh)^{6D} being independent of the anchor width AND of q, λ (otherwise the second-family LLL weights do not sum to o(1));
(b) the dichotomy actually covering every progression — in particular the SHORT-period case (the step-lattice argument w_i ∈ q^{−i}ℤ and |w_i| ≥ α, and the claim that a cut
crossing forces every V-width in that coordinate below |w_i|) and the LONGER-period case (regular fraction, eligibility (iii) at every regular position of a block containing a
heavy index — is Lemma heavy-width applied at the right index; is dist_T(y_i(n_j), y_i(n_{j_*})) ≤ |v_i| right when the block's own u,v come from a DIFFERENT heavy label than j_*'s);
(c) Lemma perturb:multiplicity's separation (3-point argument on a closed interval of length ≤ 1; the half-line split at the nearest point; keys whose V-box is a product of
half-open intervals vs the affinity lemma's box); (d) the two probability unions: are the events "monochromatic with target b" exactly the prescriptions claimed, is the affine
count T_aff really over SIGNATURES (same literal keys) so that identical signatures define identical events, and is the rich case's "≥ γk/4 distinct keys" right when a key
may carry BOTH outer colors on the same progression; (e) every "for sufficiently large k" inequality — list each one in your scope with the inequality it needs
(e.g. h_0 < 2M < k; 4MH/h < ½; 2H(k+1)|w_i| < |w_i|; 4MH/k < η; D(4η + 1/h_0) < ½; 2M/k ≤ 1/16; 6D log(CDh)/h ≤ 6 log(CD³)/D; l(E) ≥ 100; p < ½; 2c − γ/80 < 0;
log T_aff = o(pk) with log q = O(k^{9/10} log k) vs pk = k^{19/20}) and say whether it holds for all large k with the stated parameters — a single reversed inequality
in this chain is FATAL for the paper (the Lean, if it compiles, is unaffected); (f) the LLL: the dependency graph "share a label variable" vs the independence hypothesis of
Lemma outer:lll; whether the first-family row events are functions of the ξ_β only (the word fixes light/heavy); whether Σ_{F∈Γ(E)} z_F ≤ l(E)/500 follows from the per-label
incident weight; (g) Lemma dichotomy:path's gcd argument (the convex-combination step needs the representative box to be a product of HALF-OPEN intervals and j'+h/e < k)
and the "incongruent ⇒ distinct labels" step (only the FIRST system is used — is 1/h − k|u_i|/h > H_x right); (h) the digit product (07): the identity
⌊(a+jd)/N^i⌋ = ⌊a/N^i⌋ + je, the reduction mod N, "translation by one", and that the cyclic theorem forbids progressions for EVERY d ≠ 0 incl. wrapping ones.
Also (i) QUANTIFIERS: K_0 is claimed absolute and uniform in r — check that no threshold in §2–§6 depends on r (it should not; r enters only in §7) and that the
"sufficiently large k" thresholds are finite in number; (j) PROVE-TOO-MUCH: the method gives q^D ≥ k^{ck} with c = 10^{−5} — could the same argument give k^{k} or more
(does any step genuinely cap c; which inequality is tight); the paper says nothing about W(k) ≥ k^{(1−o(1))k}; does it CLAIM more than it proves anywhere (abstract, intro,
Corollary transfer:limits' infimum over integer r including the k-threshold ordering).

Classic holes to hunt: a quantifier/parameter fixed after it is used; "clearly"/"it follows"/"similarly"/"the same argument" at a hard step (count them in your scope and
check each); an inequality used in the wrong direction; a probability called exact that is approximate; an o(1) that depends on the progression; a limit taken before a sup;
a lemma applied outside its hypotheses (box widths ≤ 2H, 2kH < 1, regular vs heavy indices, h ≤ 2M vs h > h_0, p ≤ ½); half-open vs closed intervals at a mesh endpoint
or the cut; natural-number subtraction and 0-based vs 1-based conventions between the paper and the Lean.

OUTPUT — write /tmp/oaimath/160/seats/referee_<YOURTAG>.md containing:
- Objections, numbered. Each: location (section / lemma \label / equation / printed page), the quoted sentence(s) VERBATIM (from the TeX), what is wrong or unverifiable,
  severity FATAL / GAP / UNCLEAR / COSMETIC, what would fix it. For FATAL/GAP say whether it is a gap in the PROOF or in the EXPOSITION (the Lean, if it compiles,
  settles the THEOREM regardless — your job on the paper is the human-readable proof).
- For each lemma/proposition/equation in your scope: VERIFIED LINE BY LINE / SKIMMED / NOT READ. This distinction is the deliverable.
- Any finite check you ran: the script VERBATIM, its output, and a control that FAILS (a deliberately wrong input the check rejects). Python is fine; keep every run under
  a minute and under 1 GB (the box carries live solvers); never run lean/lake. Exact rational arithmetic (fractions) where the claim is an identity.
- Citation table for your scope (if any): cited result → what the paper claims it says → what the source actually says (quote) → MATCH / MISMATCH / COULD NOT FETCH.
  Fetch primary sources with curl/pdftotext (arXiv current version) or WebFetch; bib is in build/references.bib.
- Verdict for your scope: HOLDS AS READ / GAP AT <location> / COULD NOT CHECK <what, why>.
Be concrete, quote, no "the authors should clarify". A machine wrote this; it will not be clarifying. Finish with a ≤400-word summary in your final message (the file is
the full report).
