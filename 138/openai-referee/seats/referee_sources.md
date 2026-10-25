# Referee report — seat `sources` — OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026), family 160, Erdős #138

Seat: sources (citations at cited versions + state of the world on 15 Oct 2026). Written 2026-10-15 06:17–06:45Z.
Paper copy: /tmp/oaimath/160/paper.pdf, sha256 042acea33a57…bd18 — re-downloaded from github.com/openai/math `main` at 06:2xZ and byte-identical
(/tmp/oaimath/160/world/paper160_github_main_2026-10-15.pdf). GitHub history: the only commit touching the preprint or `lean/OAI/Combinatorics/ProgressionColoring/`
is `adc7f1241b` "Initial commit", **2026-10-06T21:58:50Z** (/tmp/oaimath/160/world/gh_commits_paper160.json, gh_commits_lean160.json); the later repo commits
(301488868b 10-08, 2710f995ca/1581d4cbdd 10-12) do not touch it. So the paper is dated 23 Sep 2026 but was first public on **6 Oct 2026** (Bloom: "On Tuesday 6th October, OpenAI released…").
TeX quoted from build/sections/*.tex. Printed reference numbers [1]–[25] as in the PDF (pp. 24–25); all 25 bib entries are cited somewhere.

Sources fetched: /tmp/oaimath/160/refs/ (PDF + pdftotext for each; FETCH_LOG.txt lists version → file); web pages/metadata: /tmp/oaimath/160/world/.
I did not run lean or lake. My two scripts are in /tmp/oaimath/160/seats/sources_scripts/ (each runs < 5 s, < 50 MB).

---------------------------------------------------------------------------------------------------------------------------------------------------
## 0. Verdict for this scope (sources + world)

**HOLDS AS READ** for every citation I could fetch: 25 of 25 references are used, all bibliographic data agree with Crossref/arXiv, and every
checkable claim the paper makes about a cited source MATCHES the source at the cited version. **No MISMATCH found.**
COULD NOT CHECK at the primary source: Szabó 1990 (Wiley 403; the content matches the publisher abstract, the theorem *number* "Theorem 2" is unverified),
Behrend 1946 (pnas.org Cloudflare-walled at every tier tried), Schmidt 1962, Shelah 1988, Rankin 1961 full text (verified via secondary
sources / publisher synopsis / title). Journal versions of Hunter 2022/2025, Kozik–Shabanov, Green–Wolf, Gowers were read as arXiv/author preprints (proxies).

One substantive exposition GAP in scope (S2): the "at most quasipolynomial" upper half of the introduction's r-growth display rests entirely on the
companion OpenAI preprint's Equation (1.3) — an unrefereed 198-page claim whose own Lean formalization explicitly leaves the quantitative bound out.
This does not touch Theorem 1.1.

World on 15 Oct 2026, in one paragraph: the paper was first public on 6 Oct 2026 (repo initial commit `adc7f124`), unchanged since. erdosproblems.com/138
has not been edited since 2 June 2026, shows no status (site-wide policy since 6 Oct), has 0 proof claims, and its newest comment is from 24 Aug 2026;
the teorth database still says `open` (last update 2025-08-31). Bloom's 8 Oct post lists #138 among the 25 problems and among the 12 FrontierMath-list
problems, "should not be read as any kind of endorsement". Google DeepMind's Formal Conjectures marked `erdos_138` "research solved" on 11 Oct
(commit 3dfd999dfe, M. Firsching), linking OpenAI's Lean. Two third parties have machine-checked the Lean comparator and report a pass
(mathvet, 8 Oct; nealmcb, 11 Oct). I found **no** published specialist review of the mathematics, **no** reported error, and **no** human-authored
claim of W(k)^{1/k} → ∞ (two colours), before or after the paper (a coverage claim; queries listed in §5.3).

**The $500 question.** Erdős's question (1980, p. 90, (2): two classes, lim f(n)^{1/n} = ∞, "$500 for the proof or disproof") is **not answered by anything
earlier** — Kozik–Shabanov (c·2^k), Campos–Fox–Schildkraut ((1−o(1))k2^{k−1}, i.e. W^{1/k} → 2), Fox–Hunter (r ≥ 3 only), Hunter (r ≥ 5, exponential),
DeepMind (W(k+1) ≥ W(k)+k) all leave it open, and CFS (21 Aug 2026) and FH (1 Jun 2026) both describe it as open. **This paper is the first claim to
answer it, positively and quantitatively (W_2(k) > k^{k/100000} for k ≥ K_0).** Its standing as of today rests on the Lean (two independent passes
reported, our own replay in progress) — not on any human verification of the paper's argument, which nobody has published.

---------------------------------------------------------------------------------------------------------------------------------------------------

## 1. Objections (numbered)

**S1. Szabó's theorem number unverifiable.** 01-introduction.tex, "Earlier bounds", printed p. 1, ref [23].
> "Szab\'o~\cite[Theorem~2]{szabo1990} proved $W_2(k)\ge 2^k/k^\varepsilon$ for every fixed $\varepsilon>0$ and all sufficiently large $k$."

The full text is paywalled (onlinelibrary.wiley.com → 403); Semantic Scholar has no record. The publisher abstract (Crossref,
world/crossref_refs_2026-10-15.json) says: "We prove in this paper that W(n) ≥ 2^n/n^ϵ for all sufficiently large n." Content MATCHES; the locator
"Theorem 2" COULD NOT be verified. Severity: COSMETIC (locator only). Fix: none if the number is right; otherwise cite the abstract statement.

**S2. The quasipolynomial upper half of the r-growth display rests on an unverified, unformalized companion claim.** 01-introduction.tex, paragraph after
"Growth in the number of colors", printed p. 2, ref [17].
> "Combining it with the coloring upper bound in the companion paper~\cite[Equation~(1.3)]{openaiArithmeticProgressions2026} gives, for each integer
> $k\ge3$, a constant $A_k\ge1$ such that for every integer $r\ge256$, \[ \exp\!\left(\frac{(\log r)^2}{64\log2}\right) <W_r(k)\le
> \left\lceil\exp\bigl(A_k(2+\log r)^{A_k}\bigr)\right\rceil. \] Thus, for every fixed progression length $k\ge3$, as integer $r$ tends to infinity, growth
> in the number of colors is superpolynomial but at most quasipolynomial"

The citation is accurate — companion §1.4 p. 8: "W_r(k) ≤ ⌈exp(A_k(2 + log r)^{A_k})⌉ (r ≥ 1), (1.3)" derived from its Theorem 1.1
(r_k(N) ≤ C_k N exp[−c_k(log N)^{ε_k}] for every fixed k ≥ 3). But that Theorem 1.1 is (i) unrefereed (same anonymous author, 198 pp.),
(ii) explicitly **outside** its own formalization: world/openai_lean_docs_159.md, "The selected theorem is the reciprocal-sum consequence. The paper's
quantitative upper bound for the largest progression-free subset of {1,…,N} is outside this statement."; (iii) per Bloom (8 Oct post, Problem [3] entry,
world/bloom_blog10_text.txt lines 140–146) "The actual Lean code appears to prove the weaker bound of |A| ≤ exp(−(log log N)^{1+c_k})N", which only gives
W_r(k) ≤ exp(exp(O_k((log r)^{1/(1+c_k)}))) — not quasipolynomial. In the literature that IS established: k = 3 is quasipolynomial by Kelley–Meka (so the
display is fine at k = 3); k = 4 gives only W_r(4) ≤ exp(r^{O(1)}) (from Green–Tao's r_4(N) ≪ N(log N)^{−c}, not cited by the paper); k ≥ 5 gives W_r(k) ≤ exp(exp(O_k((log r)^{1/c_k}))) from Leng–Sah–Sawhney Thm 1.1 — neither is quasipolynomial. So "at most quasipolynomial" for
fixed k ≥ 4 is, as of 15 Oct 2026, supported only by the companion's unverified claim. A blog comment by user "jleng01" (identity not verified by me) on
Bloom's post calls the 198-page release "200 pages of AI slop" while saying they are "familiar with many of the key ideas in the proof" — not evidence of
an error, but it is the only public specialist-adjacent remark I found, and it is not favourable.
Severity: GAP in the EXPOSITION (an attribution/conditionality gap), not in the proof of Theorem 1.1, Theorem 7.2, or the Lean of family 160.
Fix: write the upper half as "assuming [17, Theorem 1.1]" or restrict "at most quasipolynomial" to k = 3 via Kelley–Meka.

**S3. Colour convention swapped in the Green/Hunter sentence.** 01-introduction.tex, printed p. 3.
> "For the asymmetric problem of excluding a red three-term progression and a blue long progression, Green~\cite{green2022} uses …"

Green (FMP abstract): "a red-blue colouring of [N] with no blue 3-term arithmetic progression and no red arithmetic progression of length …"; Hunter 2022
uses the same convention. Harmless by symmetry. Severity: COSMETIC. Fix: swap "red"/"blue".

**S4. "Origins of the local lemma": EL 1975 has only the symmetric form.** 04-outer.tex, printed p. 9.
> "For the origins of the local lemma, see Erd\H{o}s and Lov\'asz~\cite{erdosLovasz1975}; the proof of the form used here is included."

EL 1975 pp. 616–617 state the symmetric lemma ("Also suppose P(A_i) ≤ 1/(4d). Then P(Ā_1…Ā_n) > 0."). The asymmetric form of Lemma outer:lll
(P(E) ≤ z_E∏(1−z_F)) is not in EL 1975 (it is usually credited to Lovász via Spencer 1977). The paper says "origins" and proves its own form, so nothing
false is asserted. Severity: COSMETIC.

**S5. Theorem 7.2's uniformity in k is automatic; only the explicit constant is new.** 01-introduction.tex p. 2 / 07-transfers.tex Theorem transfer:large-r.
> "For completeness, Theorem~\ref{transfer:large-r} gives a direct elementary lower bound with an explicit constant uniform over all lengths $k\ge3$."

A colouring with no monochromatic 3-AP has none of length k ≥ 3, so W_r(k) ≥ W_r(3); and W_r(3) ≥ 2^{c(log r)^2} with an absolute c is the
Behrend-covering bound FH record on pp. 2–3 ("w(k;r) ≥ 2^{c_k (log r)^{⌈log k⌉}}", ⌈log 3⌉ = 2). So uniformity over k is not a new phenomenon; the
content of Theorem 7.2 is the explicit constant 1/(64 log 2). The paper does not overclaim ("For completeness"). Severity: COSMETIC (novelty note).

**S6. The introduction does not say how late the new bound becomes non-trivial.** 01-introduction.tex p. 1 (Theorem main:intro and the comparison
paragraph). Not an error. With c = 10^{−5}, k^{ck} exceeds Kozik–Shabanov's r^{k−1} and CFS's k2^{k−1} at r = 2 only when log₂ k > 10^5
(k > 10^{30103}); for r = 3 it passes FH's 2^{k log*k/4} at the same point and KS's 3^{k−1} only past k ≈ 10^{47712} (script §3.1). K_0 is never given.
The bound is purely asymptotic; it is nonetheless an asymptotic improvement of FH Theorem 1 for every fixed r ≥ 3 (exponent k·log k versus
k·log* k), which the introduction does not mention. Severity: COSMETIC/UNCLEAR (exposition).

**S7 (world, not the paper). Formal Conjectures' "research solved" tag rests on OpenAI's own definition of W, not on FC's.** formal_conjectures_138.lean
(current main, commits 3dfd999dfe 11 Oct and 7db2ea3b91 14 Oct): `erdos_138 : atTop.Tendsto (fun k => (W k : ℝ)^(1/(k : ℝ))) atTop := by sorry` with
`formal_proof using lean4 at "…/openai/math/blob/adc7f124…/ProgressionColoring/Main.lean#L12"`. FC's `W = monoAPNumber 2` is defined via colourings
`Finset.Icc 1 N → Fin r` and FC's `ContainsMonoAPofLength`; OpenAI's `W r k = sInf {N | 0 < N ∧ IsRamsey (Fin r) k N}` with colourings `ℕ → Fin r` and
0-based progressions `a + (k−1)d < N`. They plainly agree mathematically (shift by one), but no bridge lemma exists in FC and FC's statement is still
`sorry`. Contrast the dvd_two_pow variant, where niketp03/atlas-fc-verified re-proved FC's own statement against FC's own definitions. Severity: UNCLEAR
(it affects what "formally solved" means on that site, not this paper).

**S8 (correction to the BRIEF, not the paper).** The brief says Fox–Hunter's superexponential bound "uses a Behrend-type covering that is unavailable at
two colors". FH's Theorem 1 does not use Behrend covering: "An important ingredient in the proof of Theorem 1 is Lemma 2.8. It gives a novel probabilistic
construction of a very dense subset of a large cyclic group that is far from containing a k-term arithmetic progression. One can then turn this into a
3-coloring (using this set as one color class and the other elements are colored uniformly at random with the other two colors) … the random shifted product
construction (Lemma 4.2)" (FH p. 2). The Behrend/Rankin covering is FH's separate remark about very large r (pp. 2–3). The two-colour obstruction to FH's
scheme is that one colour class is a dense AP-free set, which leaves only one colour for the sparse remainder. Likewise Bloom's sentence "Such a lower bound
was proved by Fox and Hunter [FoHu26] for r≥3" overstates FH if "such" means k^{ck log r}: for fixed r FH give only 2^{k log* k/4} (Thm 1); their
r^{(1−ε)k log k} (Thm 2) needs r ≥ (log k)^{3/ε}.

No objection in my scope is FATAL.

---------------------------------------------------------------------------------------------------------------------------------------------------

## 2. What I read, and how closely (my scope = every citation + the world; the mathematics of the paper's Sections 2–8 belongs to other seats)

| Item | Status |
|---|---|
| 01-introduction.tex (every sentence with a citation; the comparison paragraph; the r-growth display) | VERIFIED LINE BY LINE against the sources (table §4) |
| 02-setup.tex line 30 (FH lcm dilations) | VERIFIED (FH Lemma 2.10 proof, p. 7) |
| 03-counting.tex lines 1–10 (Stanley citation) | VERIFIED against the sp06 notes. Lemma count:arrangement itself: SKIMMED (counting seat) |
| 04-outer.tex lines 12–15 (EL 1975 citation) | VERIFIED (S4). Lemma outer:lll: NOT READ (outer seat) |
| 06-perturbation.tex lines 22–28 (Behrend citation) | citation checked via secondary sources; Lemma perturb:multiplicity proof SKIMMED (only to place the external "at most two" sharpening, §5.5) |
| 07-transfers.tex lines 5–10 (Erdős–Turán p. 263, FH §2) and 78–85 (Behrend) | VERIFIED. Prop transfer:product and Thm transfer:large-r: NOT READ line by line (whole seat) |
| 08-upper.tex lines 1–6 (vdW 1998 pp. 142–145) | VERIFIED. Thm upper:finite: NOT READ |
| build/references.bib / printed reference list pp. 24–25 | VERIFIED entry by entry (Crossref + arXiv version stamps) |
| Lean: ComparatorChallenges/QuantitativeVanDerWaerden.lean, ProgressionColoring/Main.lean | READ (statements only, to answer the $500 question); no lean/lake run |
| Companion paper (family 159) | §1, §1.4 and Eq. (1.1)–(1.3) READ; the rest NOT READ |

---------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Finite checks (scripts verbatim, outputs, failing controls)

### 3.1 Where the new bound overtakes the published ones (supports S6 and §6)
Script /tmp/oaimath/160/seats/sources_scripts/crossover.py:
```python
# Where does the new bound k^{c k floor(log2 r)} overtake the published lower bounds?
# Compare (ln bound)/k as functions of L = ln k (exact division by k = e^L done analytically; no overflow).
import math

def logstar(x):                      # FH convention: iterations of natural log until value <= 1
    n = 0
    while x > 1:
        x = math.log(x); n += 1
    return n

def new(L, c, r):  return c * L * (r.bit_length() - 1)                    # ln(k^{c k fl}) / k
def cfs(L):        return L * math.exp(-L) + (1 - math.exp(-L)) * math.log(2)  # ln(k 2^{k-1}) / k
def ks(L, r):      return (1 - math.exp(-L)) * math.log(r)                 # ln(r^{k-1}) / k  (beta=1)
def fh3(L):        return math.log(2) * (1 + logstar(L)) / 4               # ln(2^{k log*k /4}) / k, log*k = 1+log*(ln k)

def crossover(fn, fo, lo, hi):
    assert not fn(lo) > fo(lo), "new already ahead at lo"
    assert fn(hi) > fo(hi), "new not ahead at hi"
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) > fo(mid): hi = mid
        else: lo = mid
    return hi

c = 1e-5
for name, r, fo in [("CFS Thm1, r=2", 2, cfs), ("KS Thm2, r=2, beta=1", 2, lambda L: ks(L, 2)),
                    ("FH Thm1, r=3", 3, fh3), ("KS Thm2, r=3, beta=1", 3, lambda L: ks(L, 3))]:
    L = crossover(lambda L: new(L, c, r), fo, 1.0, 1e7)
    print(f"{name:22s} new > old from ln k = {L:10.3f}  i.e. k ~ 10^{L/math.log(10):8.1f}   (log* k there = {1+logstar(L)})")
print("ln2/c =", math.log(2)/c, "  ln3/c =", math.log(3)/c)
# CONTROL (must contradict the 'astronomical crossover' conclusion): deliberately wrong constant c = 1
L = crossover(lambda L: new(L, 1.0, 2), cfs, 0.1, 50.0)
print(f"CONTROL c=1: new > CFS from ln k = {L:.4f} (k ~ {math.exp(L):.3f})  -> small, so the check can say 'not astronomical'")
```
Output (runtime < 1 s):
```
CFS Thm1, r=2          new > old from ln k =  69314.718  i.e. k ~ 10^ 30103.0   (log* k there = 4)
KS Thm2, r=2, beta=1   new > old from ln k =  69314.718  i.e. k ~ 10^ 30103.0   (log* k there = 4)
FH Thm1, r=3           new > old from ln k =  69314.718  i.e. k ~ 10^ 30103.0   (log* k there = 4)
KS Thm2, r=3, beta=1   new > old from ln k = 109861.229  i.e. k ~ 10^ 47712.1   (log* k there = 4)
ln2/c = 69314.71805599453   ln3/c = 109861.22886681097
CONTROL c=1: new > CFS from ln k = 0.6931 (k ~ 2.000)  -> small, so the check can say 'not astronomical'
```
The crossings are exactly ln k = ln 2/c and ln 3/c, i.e. log₂ k = 10^5 for r = 2 (the closed form: k^{ck} > 2^k ⟺ c·ln k > ln 2). The control with a deliberately
wrong constant c = 1 crosses at k = 2, so the instrument can report "not astronomical"; it reports astronomical only because c = 10^{−5}. (The bisection's
endpoint asserts also fire if the new bound is already ahead at the lower end, or not yet ahead at the upper end.)

### 3.2 Bibliographic metadata of every DOI (supports the last line of table §4)
Script /tmp/oaimath/160/seats/sources_scripts/crossref.py (queries api.crossref.org/works/<doi> for the 15 DOIs in the bib; saves JSON):
```python
import json, urllib.request, urllib.parse, time, sys
dois = ["10.1007/s11856-025-2735-0","10.1007/s00493-022-4925-2","10.1016/j.jctb.2015.09.004","10.1002/rsa.3240010307",
"10.1215/S0012-7094-62-02914-9","10.1090/S0894-0347-1988-0929498-X","10.1007/s00039-001-0332-9","10.1007/978-0-387-68361-4_9",
"10.1017/fmp.2022.12","10.4153/CMB-1968-047-7","10.1073/pnas.32.12.331","10.1017/S0080454100017726","10.1112/jlms/s1-11.4.261",
"10.1112/plms/s3-2.1.417","10.1016/S0167-5060(08)70697-6"]
out = {}
for d in dois:
    u = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="/")
    req = urllib.request.Request(u, headers={"User-Agent": "curl/8.5.0 (mailto:me@byclaude.net)"})
    try:
        m = json.load(urllib.request.urlopen(req, timeout=30))["message"]
    except Exception as e:
        print(d, "ERROR", e); continue
    out[d] = m
    dp = (m.get("published-print") or m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])[0]
    print(d, "|", (m.get("title") or [""])[0][:75], "|", (m.get("container-title") or [""])[0][:45], "|", m.get("volume"), m.get("page"), "|", dp, "|", ", ".join(a.get("family", "") for a in m.get("author", [])))
    time.sleep(0.5)
json.dump(out, open(sys.argv[1], "w"))
```
Output:
```
10.1007/s11856-025-2735-0 | Lower bounds for multicolor van der Waerden numbers | Israel Journal of Mathematics | 267 783-795 | [2025, 6] | Hunter
10.1007/s00493-022-4925-2 | Improved Lower Bounds for Van Der Waerden Numbers | Combinatorica | 42 1231-1252 | [2022, 12] | Hunter
10.1016/j.jctb.2015.09.004 | Improved algorithms for colorings of simple hypergraphs and applications | Journal of Combinatorial Theory, Series B | 116 312-332 | [2016, 1] | Kozik, Shabanov
10.1002/rsa.3240010307 | An application of Lovász' local lemma‐A new lower bound for the van der Wae | Random Structures &amp; Algorithms | 1 343-360 | [1990, 9] | Szabó
10.1215/S0012-7094-62-02914-9 | Two combinatorial theorems on arithmetic progressions | Duke Mathematical Journal | 29 None | [1962, 3, 1] | Schmidt
10.1090/S0894-0347-1988-0929498-X | Primitive recursive bounds for van der Waerden numbers | Journal of the American Mathematical Society | 1 683-697 | [1988] | Shelah
10.1007/s00039-001-0332-9 | A new proof of Szemerédi's theorem | GAFA Geometric And Functional Analysis | 11 465-588 | [2001, 8, 15] | Gowers
10.1007/978-0-387-68361-4_9 | A Note on Elkin’s Improvement of Behrend’s Construction | Additive Number Theory | None 141-144 | [2010] | Green, Wolf
10.1017/fmp.2022.12 | New lower bounds for van der Waerden numbers | Forum of Mathematics, Pi | 10 None | [2022] | Green
10.4153/CMB-1968-047-7 | A Construction for Partitions Which Avoid Long Arithmetic Progressions | Canadian Mathematical Bulletin | 11 409-414 | [1968, 8] | Berlekamp
10.1073/pnas.32.12.331 | On Sets of Integers Which Contain No Three Terms in Arithmetical Progressio | Proceedings of the National Academy of Scienc | 32 331-332 | [1946, 12] | Behrend
10.1017/S0080454100017726 | XXIV.—Sets of Integers Containing not more than a Given Number of Terms in  | Proceedings of the Royal Society of Edinburgh | 65 332-344 | [1961] | Rankin
10.1112/jlms/s1-11.4.261 | On Some Sequences of Integers | Journal of the London Mathematical Society | s1-11 261-264 | [1936, 10] | Erdös, Turán
10.1112/plms/s3-2.1.417 | Combinatorial Theorems on Classifications of Subsets of a Given Set | Proceedings of the London Mathematical Societ | s3-2 417-439 | [1952] | Erdós, Rado
10.1016/S0167-5060(08)70697-6 | A Survey of Problems in Combinatorial Number Theory | Annals of Discrete Mathematics | None 89-115 | [1980] | Erdös
```
Control that fails: `curl https://api.crossref.org/works/10.4153/CMB-1968-047-X` (one character changed in Berlekamp's DOI) → `HTTP 404`.
Every row agrees with the printed reference list (journal, volume, pages, year, authors); Schmidt's pages and Green FMP's article number are absent from
Crossref but present in the bib (129–140; e18).

---------------------------------------------------------------------------------------------------------------------------------------------------

## 4. Citation table (cited result → what the paper says → what the source says → verdict)

Legend: MATCH = the source, at the cited version, says what the paper says it says. "proxy" = journal version blocked, arXiv version of the same paper read instead.

| # | Cited as (TeX location, printed page) | Paper's claim (verbatim TeX) | Source at cited version — verbatim quote, file | Verdict |
|---|---|---|---|---|
| [4] Erdős 1980, p. 90, (2) | 01-introduction.tex, p. 1 | "Erd\H{o}s explicitly asked for this full limit in the two-color case \cite[p.~90, (2)]{erdos1980}." | p. 90 (page image refs/erdos1980_p90-02.png): f(n) defined by "if we divide the integers 1 ≤ t ≤ f(n) into two classes at least one of them contains an arithmetic progression of n terms"; "I am of course sure that lim f(n)/2^n = ∞. (1) (1) will perhaps be not too difficult to establish, but I offer 500 dollars for the proof or disproof of lim f(n)^{1/n} = ∞. (2) (2) seems very difficult." | MATCH. Two colours, full limit (lim, not lim sup), $500 for proof OR disproof. (FH p. 2 paraphrase it as lim sup; Erdős 1980 prints lim.) |
| [24] van der Waerden 1927 | 01-introduction.tex, p. 1 | "The finiteness of these numbers is van der Waerden's theorem \cite{vanDerWaerden1927}." | Delpher OCR of p. 212 (refs/vanDerWaerden1927_p212_delpher_ocr.xml): "Behauptung 2 (l, k). Es existiert eine Zahl n(l,k) … Ist die endliche Zahlenfolge 1,2,…,n in k fremde Klassen eingeteilt, so liegt in einer dieser Klassen eine arithmetische Progression von l Zahlen." and "es ist n(2,k) = k+1". | MATCH (also the boundary value W_r(2) = r+1 of §8 is in vdW's own text). Delpher files vol. XV under "1928"; vdW himself (1998 reprint p. 145) cites "Nieuw Archief voor Wiskunde 15, 212 (1927)" — bib year fine. |
| [6] Erdős–Rado 1952 | 01-introduction.tex, p. 1 | "Early lower bounds were obtained by Erd\H{o}s and Rado \cite{erdosRado1952} and by Schmidt~\cite{schmidt1962}." | refs/erdos_1952-02.pdf p. 438 (page image refs/er1952-22.png): "The following example of a distribution gives what seems to be the first non-trivial lower estimate of W, namely W(k,l) > (2lk^l)^{1/2}." (Example 8; ER's W(k,l) = k classes, (l+1)-term APs). | MATCH |
| [19] Schmidt 1962 | same sentence | (as above) | Primary NOT fetched (Project Euclid, no text). Secondary, Berlekamp 1968 p. 409 (refs/berlekamp1968.txt): "By a more refined nonconstructive argument, Schmidt (1962) has shown that W(k,t) > k^{(t+1) − c[(t+1) log(t+1)]^{1/2}}". Crossref confirms title/journal/vol 29 (1962). | MATCH via secondary; primary COULD NOT FETCH |
| [2] Berlekamp 1968 Thm 2 | 01-introduction.tex, p. 1 | "Berlekamp's algebraic construction gives $W_2(p+1)>p2^p$ for every prime $p$ \cite[Theorem~2]{berlekamp1968}." | refs/berlekamp1968.txt (CMB open access) p. 409: "let W(k,t) denote the least integer m such that in every partition of m consecutive integers into k sets, at least one set contains an arithmetic progression of t+1 terms"; p. 410: "THEOREM 2. If t is prime, W(2,t) > t2^t." | MATCH (Berlekamp's W(2,t) counts (t+1)-term APs, so W(2,p) > p2^p is the paper's W_2(p+1) > p2^p; strict ">" as in the paper). |
| [5] Erdős–Lovász 1975 | 01-introduction.tex p. 1; 04-outer.tex p. 9 | "The local lemma of Erd\H{o}s and Lov\'asz~\cite{erdosLovasz1975} provided another route to strong coloring bounds." / "For the origins of the local lemma, see Erd\H{o}s and Lov\'asz~\cite{erdosLovasz1975}; the proof of the form used here is included." | refs/erdos_1975-34.txt pp. 616–617: "Lemma. Let G be a (finite) graph with maximum degree d … suppose that A_i is independent of the set {A_j : (v_i,v_j) ∉ E(G)}. Also suppose P(A_i) ≤ 1/(4d). Then P(Ā_1…Ā_n) > 0." and Theorem 2/Corollary 1 (colourings of r-uniform hypergraphs of bounded degree). The scan never names van der Waerden. | MATCH for both weak claims. Note: EL 1975 has only the SYMMETRIC lemma; the asymmetric form z_E∏(1−z_F) used in Lemma outer:lll is not in EL 1975 (it is Spencer 1977/Lovász) — the paper does not claim it is, and proves its own form. Erdős 1980 p. 90 itself credits the c·2^n-type bound to "Lovász and myself". |
| [23] Szabó 1990 Thm 2 | 01-introduction.tex, p. 1 | "Szab\'o~\cite[Theorem~2]{szabo1990} proved $W_2(k)\ge 2^k/k^\varepsilon$ for every fixed $\varepsilon>0$ and all sufficiently large $k$." | Full text NOT fetched (Wiley 403). Publisher abstract via Crossref (world/crossref_refs_2026-10-15.json): "We prove in this paper that W(n) ≥ 2^n/n^ϵ for all sufficiently large n." | Content MATCH (abstract); theorem NUMBER "Theorem 2" COULD NOT VERIFY |
| [15] Kozik–Shabanov 2016 Thm 2 | 01-introduction.tex, p. 1 | "Kozik and Shabanov~\cite[Theorem~2]{kozikShabanov2016} subsequently obtained an absolute $\beta>0$ such that $W_r(k)\ge\beta r^{k-1}$ for all $r\ge2$ and $k\ge3$." | proxy arXiv:1409.6921v1 (refs/arxiv_1409.6921v1.txt), §1: "Van der Waerden number W(n,r) is the minimum N such that in any r-coloring of integers {1,…,N} there exists a monochromatic arithmetic progression of length n. Theorem 2. There exists positive β such that for every r ⩾ 2 and n ⩾ 3, we have W(n,r) ⩾ βr^{n−1}." | MATCH, exact form βr^{k−1}, quantifiers "r ≥ 2 and n ≥ 3" identical (proxy; JCTB version 403). |
| [13] Hunter 2025 Thm 1 | 01-introduction.tex, p. 1 | "Hunter~\cite[Theorem~1]{hunter2025} improved the exponential base for each fixed $r\ge5$, with a threshold allowed to depend on $r$." | proxy arXiv:2301.06212v1: "Theorem 1. For r ≥ 2 with r = a + 3b (where a ∈ {2,3,4}), we have w(k;r) > (a3^b)^{(1−o_r(1))k}." "Remark 1.1. Theorem 1 gives an improved lower bound for r ≥ 5 (when k is large with respect to r)." Crossref abstract of the Israel J. version: "We give an exponential improvement to the diagonal van der Waerden numbers for r ≥ 5 colors." | MATCH (o_r(1) = threshold depending on r) |
| [8] Fox–Hunter 2026 Thm 1 | 01-introduction.tex, p. 1 | "Fox and Hunter \cite[Theorem~1]{foxHunter2026} proved $W_3(k)>2^{k\log^*k/4}$ for all sufficiently large $k$, where $\log^*k$ counts the iterations of the natural logarithm needed to reach a value at most one." | arXiv:2606.02541v1 (only version) p. 2: "Theorem 1. For k sufficiently large, w(k;3) > 2^{k(log* k)/4}." p. 2: "the iterated logarithm log* k is the number of times the logarithm function must be iteratively applied to k before the result is at most 1"; p. 4: "All logarithms are base e unless otherwise specified." | MATCH |
| [3] Campos–Fox–Schildkraut 2026 Thm 1 | 01-introduction.tex, p. 2 | "\cite[Theorem~1]{camposFoxSchildkraut2026} proved $W_2(k)\ge(1-o(1))k2^{k-1}$. They credit ChatGPT 5.6 Sol Pro with the coloring and an initial proof. Their result settles the question about $W_2(k)/2^k$" | arXiv:2608.20824v1 (only version): "Theorem 1. For every positive integer k we have w(k) ≥ (1 − o(1))k2^{k−1}." Abstract: "This verifies a conjecture of Erdős. … The coloring for general k can be viewed as a product of Berlekamp's colorings for various primes. It was found by ChatGPT 5.6 Sol Pro." p. 1 "AI Use. The coloring used to prove Theorem 1, as well as a proof of Theorem 1, were generated by a query to ChatGPT 5.6 Sol Pro. The proof we present, while drawing somewhat on the proof given by ChatGPT, was produced by the authors." | MATCH ("initial proof" is a fair gloss of "a proof … drawing somewhat on"). Who found what: ChatGPT 5.6 Sol Pro found the colouring (product of Berlekamp colourings) and a proof; the three human authors wrote the published proof. |
| [8] Fox–Hunter Thm 2 | 01-introduction.tex, p. 2 | "For every fixed $\varepsilon\in(0,1)$, Fox and Hunter also prove $W_r(k)\ge r^{(1-\varepsilon)k\log k}$ when $k$ is sufficiently large in terms of $\varepsilon$ and $r\ge(\log k)^{3/\varepsilon}$ \cite[Theorem~2]{foxHunter2026}. For example, taking $\varepsilon=1/2$ gives a stronger lower bound when $r\ge(\log k)^6$" | p. 2: "Theorem 2. For each ε ∈ (0,1) there exists k_0(ε) so that the following holds. Suppose k ≥ k_0(ε) and r ≥ (log k)^{3/ε}, then w(k;r) ≥ r^{(1−ε)k(log k)}." | MATCH. Comparison checked: at ε = 1/2, FH's exponent (natural logs) is ½·k·ln k·ln r, the new one is ≤ c·k·ln k·ln r/ln 2 = 1.44·10^{−5}·k·ln k·ln r, so FH is stronger wherever it applies. |
| [1],[18] Behrend 1946, Rankin 1961 | 01-introduction.tex p. 2 | "Behrend's construction and Rankin's extension to longer progressions supply dense progression-free sets \cite{behrend1946,rankin1961}" | Behrend primary NOT fetched (pnas.org Cloudflare 403 at local/Hetzner/residential tiers, PMC reCAPTCHA, EuropePMC 403). Secondary: Green–Wolf v1 p. 1 "A famous construction of Behrend [1] shows … r_3(N) ≫ …"; Kelley–Meka v6 p. 1 "it was shown by Behrend that … there are indeed subsets A ⊆ [N] of density roughly 2^{−log(N)^{1/2}} which have no nontrivial 3-progressions". Rankin synopsis (Cambridge page, world/rankin1961_doi.html; Crossref): "Sets of integers are constructed having the property that n members are in arithmetical progression only if they are all equal; here n is any integer greater than or equal to 3. Previous results have been obtained only for n=3." | MATCH (Rankin via publisher synopsis; Behrend via two secondary sources — primary COULD NOT FETCH) |
| [8] Fox–Hunter pp. 2–3 | 01-introduction.tex p. 2 | "covering an interval by translates of such sets already gives superpolynomial growth in the number of colors \cite[pp.~2--3]{foxHunter2026}" | pp. 2–3: "if there is a set S ⊂ [N] with |S| ≥ εN with no k-term arithmetic progression, then we can use r = (3/ε) log_2 N random translates of S to cover [N] with positive probability, yielding w(k;r) > N. As noted in [7], it thus follows from the construction of Rankin [26] (which extends the case k = 3 due to Behrend [2], see also [8]), that there is c_k > 0 such that w(k;r) ≥ 2^{c_k (log r)^{⌈log k⌉}}." (page image refs/fh_p3-03.png) | MATCH |
| [14] Kelley–Meka Thms 1.1–1.2 | 01-introduction.tex p. 2 | "the density bound of Kelley and Meka gives a quasipolynomial coloring upper bound \cite[Theorems~1.1--1.2]{kelleyMeka2023}" | v6 (28 Oct 2024): "Theorem 1.1. … Suppose A ⊆ [N] has density δ … either A contains a nontrivial 3-progression, or else δ ≤ 2^{−Ω(log(N)^β)}." "Theorem 1.2. Suppose A ⊆ [N] has density at least 2^{−d}. Then the number of triples … is at least 2^{−O(d^{12})}N^2." | MATCH as an implication (KM state density bounds only; the colouring consequence W_r(3) ≤ exp(O((log r)^{1/β})) is the one-line largest-colour-class argument; FH p. 3 states it: "Together with the Kelley-Meka theorem [21], we have w(3;r) = 2^{(log r)^{Θ(1)}}"). |
| [16] Leng–Sah–Sawhney Thm 1.1 | 01-introduction.tex p. 2 | "For each fixed length at least five, Leng, Sah, and Sawhney obtained further density bounds, improving the earlier general coloring upper bounds \cite[Theorem~1.1]{lengSahSawhney2024}." | v2 (29 Feb 2024): "Theorem 1.1. Fix k ≥ 5. There is c_k ∈ (0,1) such that r_k(N) ≪ N exp(−(log log N)^{c_k})." | MATCH as an implication (density 1/r colour class ⇒ W_r(k) ≤ exp exp(O_k((log r)^{1/c_k})), better than Gowers' tower in r for fixed k; FH p. 1: "In the case where k is fixed, a further improvement was recently proved by Leng, Sah, and Sawhney [23]"). |
| [17] OpenAI companion, Eq. (1.3) | 01-introduction.tex p. 2 | "Combining it with the coloring upper bound in the companion paper~\cite[Equation~(1.3)]{openaiArithmeticProgressions2026} gives, for each integer $k\ge3$, a constant $A_k\ge1$ such that for every integer $r\ge256$, … $<W_r(k)\le \lceil\exp(A_k(2+\log r)^{A_k})\rceil$." | refs/openai_quasipoly_AP_paper.pdf (github main, sha256 481eaf77…, 198 pp., dated September 23, 2026), §1.4 p. 8: "Let W_r(k) be the least integer N such that every coloring of [N] with r colors contains a monochromatic nonconstant k-term arithmetic progression. A largest color class has density at least 1/r, so Theorem 1.1 gives W_r(k) ≤ ⌈exp(A_k(2 + log r)^{A_k})⌉ (r ≥ 1), (1.3) after increasing A_k. … The companion paper [37, Theorem 7.2] gives the complementary lower bound W_r(k) > exp((log r)^2/(64 log 2)) for all integers r ≥ 256 and k ≥ 3." | Citation MATCH (and the companion cites back this paper's Theorem 7.2 correctly). BUT see Objection S2: the cited result is an unrefereed 198-page claim of quasipolynomial Szemerédi bounds whose own Lean formalization explicitly EXCLUDES the quantitative bound (world/openai_lean_docs_159.md: "The paper's quantitative upper bound for the largest progression-free subset of {1,…,N} is outside this statement."). |
| [20] Shelah 1988; [9] Gowers 2001 | 01-introduction.tex p. 2 | "quantitative upper bounds include Shelah's primitive-recursive bound~\cite{shelah1988} and the bounds following from Gowers's proof of Szemer\'edi's theorem~\cite{gowers2001}." | Shelah: ams.org 403; Crossref title "Primitive recursive bounds for van der Waerden numbers", JAMS 1 (1988) 683–697. Gowers: author preprint (refs/gowers2001_sz898.dvi, TeX output 2000-03-27) intro: "it was a major advance when Shelah, in 1987, gave the first primitive recursive upper bound"; "this does indeed result in a significant improvement to the bounds, even for van der Waerden's theorem." | MATCH (Shelah by title + Gowers' account; GAFA version not fetched) |
| [1] Behrend; [11] Green–Wolf | 01-introduction.tex p. 3 | "The squared-norm geometry continues the tradition of Behrend's construction~\cite{behrend1946}; Green and Wolf \cite{greenWolf2010} give a torus-annulus proof of Elkin's refinement." | GW v1 abstract "We provide a short proof of a recent result of Elkin"; §2: "For each r ≤ ½√d, write S(r) for the region {x ∈ [0,1/2]^d : r − δ ≤ ‖x‖_2 ≤ r}" in T^d. | MATCH (GW: proxy arXiv:0810.0732v1) |
| [10] Green 2022; [12] Hunter 2022 | 01-introduction.tex p. 3 | "For the asymmetric problem of excluding a red three-term progression and a blue long progression, Green~\cite{green2022} uses translates of a randomly perturbed ellipsoidal annulus, while Hunter~\cite{hunter2022} chooses annulus radii independently at many centers." | Green FMP (open access, refs/green2022_fmp.txt) abstract: "a red-blue colouring of [N] with no blue 3-term arithmetic progression and no red arithmetic progression of length e^{C(log N)^{3/4}(log log N)^{1/4}}"; §4 "Random ellipsoidal annuli". Hunter v3 p. 3: "Green used translates of a single randomly determined (ellipsoidal) annulus (with random eccentricity and fixed radius), while our construction uses translates of (circular) annuli each being determined independently at random (with fixed eccentricity and random radius)." | MATCH in substance; COSMETIC colour swap (both sources: no BLUE 3-AP, no RED long AP; the paper says red 3-AP / blue long AP). |
| [8] Fox–Hunter (lcm dilations) | 01-introduction.tex p. 3; 02-setup.tex p. 4 | "Least-common-multiple dilations also occur in the cyclic constructions of Fox and Hunter~\cite{foxHunter2026}." | FH p. 7, proof of Lemma 2.10: "Let ℓ = lcm(1,2,…,⌈1/ε⌉), so ℓ < 2.81^{1/ε}. As N is a prime and N ≥ k > 1/ε, ℓ is invertible in Z_N. … Let ℓ·I be the dilation of I by ℓ." (Dirichlet q ≤ 1/ε, q | ℓ.) | MATCH |
| [21] Shi–Dong 2026 | 01-introduction.tex p. 3 | "digit carry control and finite-field norm colorings for a related symmetric-progression problem appear in Shi and Dong~\cite{shiDong2026}." | v2 (28 Jul 2026) abstract: "The construction combines a carry-control coloring of base-p digits with a layered field norm mapping." | MATCH |
| [22] Stanley 2007 Lemma 2.1 / Prop 2.4 | 03-counting.tex p. 7 | "We use the standard hyperplane-arrangement region count; see Stanley~\cite[Lemma~2.1 and Proposition~2.4]{stanley2007}." | refs/stanley2007_sp06.txt (the cis.upenn.edu notes the bib URL points to): "Lemma 2.1. Let (A, A′, A″) be a triple of real arrangements with distinguished hyperplane H_0. Then r(A) = r(A′) + r(A″)" ; "Proposition 2.4. (general position) Let A be an n-dimensional arrangement of m hyperplanes in general position. … r(A) = 1 + m + C(m,2) + ··· + C(m,n)". | MATCH (deletion–restriction + the general-position count give r(A) ≤ Σ_{j≤e} C(s,j); the paper re-proves it and adds equality signs itself). Numbering verified in the sp06 notes at the bib's URL; the PCMS-13 printed volume not fetched. |
| [1] Behrend (norm bands) | 06-perturbation.tex p. 16 | "The next lemma uses a bounded-width version of the equal-norm geometry in Behrend's construction~\cite{behrend1946}" | (Behrend primary not fetched; see above) | attribution of a standard idea; no checkable claim beyond "Behrend used equal norms" (GW/KM confirm) |
| [7] Erdős–Turán p. 263; [8] FH §2 | 07-transfers.tex p. 19 | "The related digit construction of Erd\H{o}s and Tur\'an \cite[p.~263]{erdosTuran1936} is recalled, with the least-nonzero-digit argument, by Fox and Hunter~\cite[Section~2]{foxHunter2026}." | ET p. 263 footnote (page image refs/et1936-3.png): "It is easily seen that r{½(3^k+1)} ≥ 2^k; for, if u ≤ ½(3^k−1) is any integer not containing the digit 2 in the ternary scale, then the integers u+1 form an A sequence." FH §2 p. 4: "For a prime p, let T_p denote the set of nonnegative integers which, when written in base p, has no digit equal to p−1. … consider the position i of the least nonzero digit in base p of the common difference d." | MATCH (ET's p. 263 construction is base 3; the base-p version is Szekeres's conjecture on pp. 263–264 and FH §2) |
| [1] Behrend (digits+sphere) | 07-transfers.tex p. 20 | "This is the digit-and-sphere geometry of Behrend~\cite{behrend1946}" | (not fetched; standard) | not checkable here; uncontroversial |
| [25] van der Waerden 1998 pp. 142–145 | 08-upper.tex p. 22 | "We record a coarse quantitative form of the classical block-and-focus induction; see van der Waerden~\cite[pp.~142--145]{vanDerWaerden1998}." | refs/vanDerWaerden1998.txt pp. 142–145: blocks of 5 numbers in 2^5 = 32 classes, "unter 33 aufeinanderfolgenden Blöcken muss es … mindestens zwei gleiche geben", the k = 3, l = 3 case with blocks of 7 and the l = 4 step "n(3, 2^g) aufeinanderfolgenden Blöcken". Header p. 139 note: reprint of Abh. Math. Sem. Univ. Hamb. 28 (1965), 6–15. | MATCH |

Bibliographic metadata (journal, volume, pages, year, authors) of every DOI in the bib was checked against Crossref (world/crossref_refs_2026-10-15.json):
all agree with the printed reference list; arXiv version stamps agree with the bib notes (2606.02541v1 1 Jun 2026; 2608.20824v1 21 Aug 2026; 2607.20752v2 28 Jul 2026;
2302.05537v6 28 Oct 2024; 2402.17995v2 29 Feb 2024). None of 2606.02541 / 2608.20824 has a version newer than v1 as of 15 Oct 2026 (abs pages saved in world/).

---------------------------------------------------------------------------------------------------------------------------------------------------

## 5. The world on 15 Oct 2026 (every page saved under /tmp/oaimath/160/world/; `web_*` files fetched by my background search agent, others by me)

### 5.1 erdosproblems.com/138
- Saved copies /tmp/oaimath/160/live/e138.html, e138_thread.html, e138_claims.html, re-fetched via Hetzner 15 Oct (web_e138_fresh.html,
  web_e138_thread_fresh.html, web_e138_claims_fresh.html, web_e138_history_fresh.html; exe.dev itself gets a Cloudflare 403): identical apart from the
  Cloudflare token. Statement: "Let the van der Waerden number $W(k)$ be such that whenever $N\geq W(k)$ and $\{1,\ldots,N\}$ is $2$-coloured there must
  exist a monochromatic $k$-term arithmetic progression. Improve the bounds for $W(k)$ - for example, prove that $W(k)^{1/k}\to \infty$." Prize $500.
- "This page was last edited 02 June 2026." The body is stale: "The best general lower bound is $W(k)\gg 2^k$, due to Kozik and Shabanov" (no CFS,
  no OpenAI); "The analogous question for $r\geq 3$ colours was resolved by Fox and Hunter [FoHu26], who proved $W_3(k)^{1/k}\geq C^{\log_*k}$".
- No status word on the page: the problem box carries `id=neutral`, which is the site-wide policy announced 6 Oct (web_erdos_blog9_changes.txt):
  "No problem statuses : The site will not display the statuses of any problems (e.g. open, solved, etc.). All problems will be displayed in the same
  neutral colour." Posting of comments and proof claims is suspended site-wide.
- Comments (8): Alfaiz 1 Dec 2025 (Beck 1980 quotes "Erdos and Lovasz (unpublished)…"); JakeMallen 27 Dec 2025 (that is Berlekamp's result, typo);
  JakeMallen 28 Dec 2025 (Szabó; Kozik–Shabanov W(n,r) > cr^{n−1}); zach hunter 28 Dec 2025 ("Kozik and Shabanov get a lower bound of W(k) > c2^k");
  Adam Zsolt Wagner 10 Apr 2026 ("The DeepMind prover agent has found a Lean proof for the difference variant … Claim: W(k+1) ≥ W(k)+k");
  Thomas Bloom 10 Apr 2026 (W(k+1,l+1) ≥ W(k,l)+min(k,l); W_r(k+1) − W_r(k) ≥ k+r−1); Nat Sothanaphan 10 Apr 2026 (with GPT-5.4 Thinking,
  W_r(k+1) − W_r(k) ≥ k + min(k,F(r)) + 1); Xiao Hu 24 Aug 2026 ("A new general lower bound by GPT: https://arxiv.org/abs/2608.20824").
  **None is dated after 23 Sep 2026; none mentions the OpenAI paper. Proof claims: 0.** "Currently working on: zach_hunter, jeffgreen311."
### 5.2 Databases and catalogues
- teorth (tracker_138_2026-10-15.txt; web_teorth_problems.yaml): `{"s":"open","lu":"2025-08-31",…}`; yaml: informal_status open (2025-08-31),
  formal_status "unformalized" (sic, alongside `formalized: state: "yes"`). No teorth issue/PR on 138 after 6 Oct (agent).
- Bloom, 8 Oct 2026 (bloom_blog10_2026-10-08.html; fresh copy web_erdos_blog10_fresh.html): "There are significant claims relevant to 25 Erdős
  problems" incl. [138]; "(These include solutions to 12 problems on the FrontierMath Erdős list: [3], [138], [172], [181], [184], [371], [431], [508]
  (partial), [821], [952], [970], and [1083].)" Entry for 138: "This PDF claims a proof of the following. If $W_r(k)$ is the $r$-coloured van der
  Waerden number for $k$-term arithmetic progressions then, for all $r\geq 2$ and large $k$, \[W_r(k) \geq k^{ck\log r}\] for some constant $c>0$. In
  particular $W_2(k)^{1/k}\to \infty$, which was a conjecture of Erdős. Such a lower bound was proved by Fox and Hunter [FoHu26] for $r\geq 3$. This proof
  has been formalised. The PDF is 25 pages long. It appears to use similar methods to [FoHu26] (and various other earlier work)." Disclaimer: "I have not
  yet looked at in any serious way any of the proofs in this release … This post should not be read as any kind of endorsement". None of the 11 comments
  is about 138 (one, by "jleng01", calls the ~200-page Szemerédi companion "200 pages of AI slop" — see S2).
- OpenAI catalogue (openai_CONTENTS.md family 160): "Resolves Erdős's superexponential-growth question for van der Waerden numbers. … $W_r(k)\gt
  k^{ck\lfloor\log_2 r\rfloor}$ for an absolute c > 0, all r ≥ 2 and sufficiently large k, uniformly in r." lean/docs/160.md: "The formalized result gives
  an absolute threshold K such that W(r,k) > k^{k⌊log₂ r⌋/100000} … The sharper intermediate estimates used in the paper are not part of the described
  formalization." openai_formalization.yaml: comparator_config ComparatorChallenges/QuantitativeVanDerWaerden.json, declaration
  OAI.QuantitativeVanDerWaerden.uniform_lower_bound, file OAI/Combinatorics/ProgressionColoring/Main.lean. The 7 Oct history.md (web_gh_openai_math_history_main.md)
  withdraws three Hodge-type papers and fixes 14 others; family 160 is in neither list.
- Google DeepMind Formal Conjectures, FormalConjectures/ErdosProblems/138.lean (formal_conjectures_138.lean; history web_fc_138_commits.json):
  * `erdos_138` (Tendsto W(k)^{1/k} → ∞): "research solved" since **3dfd999dfe, 2026-10-11T07:51Z, Moritz Firsching**, PR #6898 "feat: mark problems
    solved in the OpenAI math release and link formal proofs"; docstring "Yes. This was proved by an internal OpenAI model in September 2026 [OAI26], which
    shows $W(k) > k^{k/100000}$ for all large $k$; see the linked Lean proof."; link `openai/math@adc7f124…/ProgressionColoring/Main.lean#L12`. Later:
    75a6d3d52d (14 Oct) adds `question`; 7db2ea3b91 (14 Oct) drops `answer(True) ↔`. FC's own statement is still `by sorry` (see S7).
  * `variants.difference` (W(k+1) − W(k) → ∞): solved by the **DeepMind prover agent** (FC commit c581a3ed54, 24 Apr 2026, formal proof in
    mo271/formal-conjectures; Wagner's comment 10 Apr 2026; FC also cites arXiv 2605.22763, Tsoukalas et al.).
  * `variants.dvd_two_pow` (W(k)/2^k → ∞): CFS 21 Aug 2026 (human proof, ChatGPT-found colouring) and, independently, Meta's **Atlas** (facebookresearch/atlas-lean,
    `Atlas/FC/Erdos138_dvd_two_pow_solution.lean`, branch prepare-atlas-v2: first present in commit 8a68ff3f28, merged as 223d8bc, both 2026-08-28; FC's docstring calls CFS "independent") made to compile against FC's own
    definitions by niketp03/atlas-fc-verified (commit 15e4b3a758, 2026-09-14); FC marked it solved in 2424bb480c (Niket Patel, 24 Sep 2026).
  * `variants.quotient` (W(k+1)/W(k) → ∞): still "research open". `variants.prime` docstring still reads "$W(p+1) ≥ p^{2^p}$" (typo; the Lean statement
    `p * (2 ^ p) ≤ W (p + 1)` was fixed in df8aed328e, Nov 2025).
### 5.3 Public discussion of THIS paper since Sept 2026, and the priority question
- Found: Bloom's 8 Oct post (above); OfficeChai, 9 Oct (web_officechai_23erdos.txt): "Problem 138 (van der Waerden numbers): A lower bound confirming
  Erdős's conjecture that the two-colour van der Waerden number grows faster than any exponential in k."; Closed Form, an AI-written explainer
  (web_closedform_e160.txt): "The bound beats 2^k only once log₂ k exceeds 100,000." (agrees with my §3.1) and "No specialist review of the paper is published."
- Not found (searched by the agent; files listed): Gil Kalai's blog (7 Oct "Updates: Sharing AI progress on mathematics", 22 Sep, 14 Oct posts —
  no van der Waerden); Tao (Mathstodon API since Sept, blog 6–7 Oct — none); MathOverflow (StackExchange API, nothing since Sep 2025; the OpenAI-release
  questions incl. 515845 do not mention it); Hacker News (0 stories for "van der Waerden"; in the six large OpenAI-math threads the only "Waerden" hits
  are Algolia fuzzy matches — I opened the two in story 50002650 and neither mentions van der Waerden); erdosproblems forum threads; The Verge, SciAm,
  Retraction Watch, The Conversation, Zvi, Quanta. COULD NOT FETCH: Reddit (403 "Blocked" from exe.dev and Hetzner), X/Twitter, the Lean Zulip
  live API (401; public archive ends 28 Feb 2026), IAS talk pages (Cloudflare), openai.com blog (403).
- arXiv 2026 (web_arxiv_vdw.xml and author listings): relevant hits are only Fox–Hunter 2606.02541v1, CFS 2608.20824v1, Fox–Schildkraut 2608.20533 (nearly
  consecutive sequences, Ω(2^k/k²); not W(k)), and Haitao Cao 2609.31798v1 (25 Sep; w(3,k) ≥ k^{Ω(log k)}, off-diagonal). **No follow-up by Fox, Hunter,
  Campos or Schildkraut on W(k) after 21 Aug.** Both 2606.02541 and 2608.20824 are still v1 ("[v1] Mon, 1 Jun 2026 17:45:49 UTC", "[v1] Fri, 21 Aug 2026
  07:44:10 UTC").
- **Priority (human-authored two-colour superexponential claim): NONE FOUND, before or after 23 Sep 2026.** The latest human statements treat it as
  open — FH p. 2: "Erdős [10, 11, 12] offered $500 to prove or disprove that w(k; 2) has super-exponential growth in k, that is, lim sup_{k→∞} w(k; 2)^{1/k} = ∞.
  He guessed this holds [9], although he thought that this would be very difficult to prove."; CFS p. 1: "He also offered $500 to prove or disprove that
  van der Waerden numbers have superexponential growth, that is, lim_{k→∞} w(k)^{1/k} = ∞. Fox and Hunter [7] proved that three-color van der Waerden
  numbers have superexponential growth." This is a COVERAGE claim: 23 web queries (web_websearch_log.txt, Q1–Q3 and Q17–Q20 aimed at exactly this:
  e.g. Q18 "two-color van der Waerden numbers grow super-exponentially" → "no such paper"; Q2 the exact paper title → no indexed page), the arXiv API
  queries above, HN, MathOverflow, erdosproblems.com. Not covered: X, Reddit, Zulip, Google Scholar, non-English venues.
### 5.4 Third-party rebuilds of the Lean
- **mathvet/mathvet** (web_ghraw_mathvet_cloud_QuantitativeVanDerWaerden.comparator.txt, .cmp.txt, challenge-status.csv): upstream `adc7f124`, Lean 4.34.1,
  comparator ca04cfc, landrun sandbox, 2026-10-08T13:27–13:29Z; log ends "Running Lean default kernel on solution. / Lean default kernel accepts the
  solution / Your solution is okay! / == comparator exit=0"; .cmp: "CMP OAI.QuantitativeVanDerWaerden.uniform_lower_bound [thm] ok" and the four
  definitions ok; status csv "160,full,…,comparator-sandboxed-pass". Run inside a Claude Code session (claude.ai/code link in the provenance header).
- **nealmcb/openai-math-lean-tooling** (web_ghraw_nealmcb_configs.csv): "QuantitativeVanDerWaerden,accepted,OAI.Combinatorics.ProgressionColoring.Main,115,…,92.5,…,6.2,…,
  2026-10-11T07:40:31+00:00" — upstream fd4aeeb2ee (ProgressionColoring unchanged since adc7f124), all 416 configurations accepted. Both third-party runs
  were driven with AI assistance (Claude Code, per their own provenance notes); they are nonetheless mechanical kernel checks of the comparator statement.
- Statement-fidelity review posted to the Lean Zulip (web_zulip_openai-math-lean-statements.pdf/.txt; Claude Opus 5.5 with human oversight by Robert
  Joseph George): "All 405 statements were compared with the theorems in the papers, twice and independently. No statement is false, vacuous, trivially
  true, or about the wrong concept." Family 160 row: "QuantitativeVanDerWaerden (160) — Finiteness and the boundary values W(r,1) and W(r,2). — unchecked
  — Lean (checked) · doc", i.e. the main statement is faithful; the doc's extra claims are not comparator-checked.
- No GitHub repository named ProgressionColoring/QuantitativeVanDerWaerden; no "cert-machine" or "plasma-ai" report anywhere; Palomar registry has no
  openai/math entry; FC PR #6898 did not build OpenAI's Lean ("source inspection", "grep"). Trackers zjukop3 ("unchecked") and jkbennitt ("claimed").
- Our own replay (/tmp/oaimath/160/lean-build, NOT my scope, read-only glance at 06:26Z): all 115 modules built; `#print axioms` for uniform_lower_bound,
  kthRoot_tendsto, length_rate_tendsto, exists_cyclic_coloring → [propext, Classical.choice, Quot.sound]; the `rightshape` probe failed with a probe-side
  type mismatch (`Nat.log 2 2` not simplified to 1 in the probe's expected type), `statement_match.txt` printed MISMATCH (not investigated by me);
  `leanchecker --fresh` was running. The replay seat must adjudicate those two probe results.
### 5.5 AI-derived follow-ups
- rohanarun/van-der-waerden-refinement (created 2026-10-09): AI-generated, self-described "Conditional van der Waerden coefficient refinement" to c = 1/9;
  NOT a verification. It contains one concrete sharpening of Lemma perturb:multiplicity: "The source bounds the multiplicity of a geometric key by four. …
  In fact there are at most two such points." I checked the arithmetic only: on one half-line two points with |t|-values 0 ≤ u < v, v − u ≥ 1, satisfy
  v² − u² = (v−u)(v+u) ≥ 1, impossible inside one half-open band [m, m+1); the paper's "four" comes from enclosing each half-band in a CLOSED interval of
  length ≤ 1 (06-perturbation.tex: "each of these intervals contains at most two sampled points"). So the paper's 4 is valid but loose. Pointer for the
  perturbation seat; it does not affect correctness.
- incrediblecrab/erdos-1186 uses the result only conditionally ("OpenAI's large-coloring theorem is not independently verified here").

---------------------------------------------------------------------------------------------------------------------------------------------------

## 6. What is novel here and what is not (with evidence)

NOT new (prior art, all correctly cited by the paper):
- Superexponential growth for r ≥ 3 colours: Fox–Hunter Thm 1 (1 Jun 2026), W_3(k) > 2^{k log* k/4}; for r ≥ 5 exponential improvements: Hunter 2025.
- W_2(k)/2^k → ∞: CFS (21 Aug 2026), W(k) ≥ (1−o(1))k2^{k−1}; independently Meta Atlas Lean proof (28 Aug 2026).
- Superpolynomial growth in r for fixed k: Behrend/Rankin covering (FH pp. 2–3). Theorem 7.2's uniformity in k is automatic from monotonicity (S5).
- Ingredients: cyclic-group constructions with lcm dilations (FH Lemma 2.10), the local lemma, random perturbations indexed by squared-norm/annulus geometry
  (Behrend; Green 2022; Hunter 2022; Green–Wolf), digit transfer from a cyclic group to an interval (Erdős–Turán digits recalled in FH §2; FH's product
  lemmas). Bloom: "It appears to use similar methods to [FoHu26]".

NEW (claimed; no prior or concurrent claim found):
- **Superexponential growth at TWO colours**, W_2(k) > k^{ck}, c = 10^{−5}: the first claim to answer Erdős's $500 question (1980, p. 90, (2)).
  Evidence of absence: FH and CFS both call it open (quotes §5.3); no human or AI claim found anywhere through 15 Oct 2026 (coverage list §5.3).
- A uniform-in-r form k^{ck⌊log₂ r⌋} with a single absolute threshold; for each fixed r ≥ 3 it improves FH Theorem 1 asymptotically (exponent of order
  k·log k versus k·log* k) — but only for k beyond ~10^{30103} (§3.1). For r ≥ (log k)^{3/ε} FH Theorem 2 remains stronger (the paper says so).
- The specific two-colour mechanism (a second, dilated coordinate system; a mesh refined toward the cut; an anchored pattern count (CDh)^{6D}
  independent of the anchor width; flips indexed by (y-box, ⌊‖qỹ‖²⌋)) — I found no prior instance; other seats judge its correctness.
- Not new as mathematics but new as an artifact: a Lean formalization of the full uniform lower bound, independently machine-checked twice (§5.4).

## 7. Is Erdős's $500 question (two colours) answered — by this paper or anything earlier?
- Erdős's question at the cited place: "There is an f(n) so that if we divide the integers 1 ≤ t ≤ f(n) into two classes, at least one of them contains an
  arithmetic progression of n terms"; "I offer 500 dollars for the proof or disproof of lim f(n)^{1/n} = ∞. (2)". Note the full limit (FH paraphrase it as lim sup; the paper and the
  Lean `kthRoot_tendsto` give the full limit, which settles either reading).
- **Earlier work: no.** Erdős–Rado, Schmidt, Berlekamp, Erdős–Lovász, Szabó, Kozik–Shabanov and CFS are all of the form 2^{k+O(log k)} or smaller (W^{1/k} → 2 at
  best); FH is r ≥ 3; Hunter is r ≥ 5 and exponential; DeepMind's W(k+1) ≥ W(k)+k is about differences.
- **This paper: yes, as a claim** — Theorem 1.1 at r = 2 gives W_2(k) > k^{10^{−5}k}, hence W_2(k)^{1/k} > k^{10^{−5}} → ∞ (positive answer). The Lean
  comparator statement at r = 2 is the same inequality with Nat.log 2 2 = 1; `kthRoot_tendsto (r := 2)` is Erdős's (2) for the 0-based-interval W (equal to
  the 1-based one by translation; that equivalence and the faithfulness of the definitions are the whole seat's job). Because `W` is an `sInf` and `sInf ∅ = 0`
  in ℕ, a strict lower bound by a positive real cannot hold vacuously.
- Standing on 15 Oct 2026: unrefereed; first public 6 Oct; no published human check of the argument; erdosproblems.com and teorth not updated; Formal
  Conjectures "research solved" on the strength of the Lean; two independent comparator passes reported (§5.4). Whether a prize is paid is Erdős-estate /
  site business that I cannot assess; the site has frozen claims and statuses.
