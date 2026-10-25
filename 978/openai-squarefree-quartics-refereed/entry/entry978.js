  {
    slug: "978-openai-squarefree-quartics-refereed",
    problemNum: 978,
    title: "#978: n⁴+2 is squarefree infinitely often — OpenAI's proof that every irreducible quartic with no fixed square divisor takes squarefree values with the predicted density, its Lean replayed here (a shorter route than the paper's) and its paper read by AI seats; Formal Conjectures' three #978 statements proved in Lean from it",
    date: "2026-10-22",
    status: "proof_claimed",
    originatedByUs: false,
    summary:
      "Erdős wrote in 1953 that he could not prove n⁴+2 squarefree for infinitely many n, and in 1981 that there was no quartic polynomial about which anyone could. Hooley had the (d−1)-power-free case in 1967; at d−2 the record for general polynomials stopped at degree 9 (Browning 2011; binomials to degree 6). OpenAI's preprint, dated 24 September and public since 6 October, claims the (d−2)-power-free values have the predicted Euler-product density for every irreducible f of degree d ≥ 4 with no fixed prime (d−2)-th-power divisor: n⁴+2 is squarefree for about 75.67% of n. We replayed its Lean (63 modules, Mathlib only) in the kernel: standard axioms, statement and seven definitions matched to the comparator, independently of two earlier third-party replays. The Lean takes a shorter route than the paper (no archimedean determinant cuts, no quintic deletion) and proves degrees ≥ 9 itself, without Browning. Four AI seats read the paper: HOLDS AS READ on everything #978 needs, one fillable gap in a side corollary. Ours: Lean proofs of Formal Conjectures' three #978 statements, tagged solved there but still sorry, counts by two different methods, and a correction to our own July report. The theorem is OpenAI's.",
    body: `
<p><strong>The problem.</strong> <a href="https://www.erdosproblems.com/978">Erdős problem #978</a> [Er65b, p. 219; Er81h, p. 178; see also Er53]. Write d for the degree (the problem page writes k). Erdős proved in 1953 that an irreducible integer polynomial of degree d ≥ 3 takes infinitely many (d−1)-power-free values, apart from a 2-adic exception when d is a power of 2. Hooley proved in 1967 that it does so with positive density. One power lower, nothing was known in small degree. Erdős wrote in 1953: "I have also not been able to prove, for example, that n<sup>4</sup>+2 is squarefree for infinitely many n" (p. 425). In 1965: "I could prove nothing about the representation of (k − 2)-th power-free numbers, for example, I cannot show that n<sup>4</sup> + 2 represents infinitely many squarefree numbers" (§6, p. 219). In 1981: "there is no quartic polynomial about which we can prove that it represents infinitely many squarefree integers" (p. 178). The problem page asks: if d &gt; 3 and no prime p has p<sup>d−2</sup> dividing every value f(n), are there infinitely many n with f(n) (d−2)-power-free? In particular, is n<sup>4</sup>+2 squarefree infinitely often?</p>
<p>The local condition was added to the page on 31 March 2026. Moritz Firsching had posted a counterexample to the question without it, found by DeepMind's prover agent: x<sup>6</sup>+33x<sup>5</sup>+21x<sup>4</sup>+63x<sup>3</sup>+18x<sup>2</sup>+24x+48. It is congruent to x(x−1)⋯(x−5) mod 16, so 2<sup>4</sup> divides every value.</p>
<p>Before this release the asymptotic for r-power-free values was known for these ranges of the exponent r:</p>
<ul>
<li>r ≥ (√2 − ½)d (Nair 1976), which reaches r = d−2 only for d ≥ 24;</li>
<li>r ≥ (3d+2)/4 (Heath-Brown 2006, Theorem 16), so d ≥ 10;</li>
<li>r ≥ (3d+1)/4 (Browning 2011), so d ≥ 9.</li>
</ul>
<p>Two other results bear on it:</p>
<ul>
<li>For binomials x<sup>d</sup>+c only, r ≥ (5d+3)/9 suffices (Heath-Brown 2013), so r = d−2 for d ≥ 6. Heath-Brown wrote there that "the most interesting open question then concerns quartic polynomials taking square-free values".</li>
<li>Granville (1998) obtained squarefree values in every case, but conditionally on the abc conjecture.</li>
</ul>
<p>Our July report on #978 (<a href="/report/978">/report/978</a>) found the problem open. It counted 75,670 squarefree values of n<sup>4</sup>+2 for n ≤ 10<sup>5</sup>, with every factorisation checked independently. It enclosed the predicted density between 0.75668370 and 0.75668401, and found a sign error in the decisive step of the one public claim then on record (Carella, arXiv 2310.16952).</p>
<p>It also named "the exact unresolved range" as primes p &gt; √X. That was wrong. The elementary count Σ<sub>p≤X</sub> ρ(p<sup>2</sup>)(X/p<sup>2</sup> + 1) = O(X/Y) + O(π(X)), taken over primes p &gt; Y, already handles every p ≤ X; this is the paper's (2.5). So the open range was p &gt; X, which is exactly OpenAI's Proposition 1.4. The report now carries a dated correction.</p>

<p><strong>The claim.</strong> OpenAI, "Squarefree values of quartics and power-free values of polynomials" (dated 24 September 2026, 55 pages, public since 6 October as family 020 of github.com/openai/math). In the paper's notation k = d − 2 is the exponent.</p>
<p>Theorem 1.1: let f ∈ ℤ[x] be irreducible over ℚ of degree d with 4 ≤ d ≤ 8, and suppose ρ<sub>f</sub>(p<sup>k</sup>) &lt; p<sup>k</sup> for every prime p, so that no prime k-th power divides every value. Then</p>
<p style="text-align:center">#{1 ≤ n ≤ X : f(n) is k-power-free} = c<sub>f,k</sub>X + o(X),  c<sub>f,k</sub> = ∏<sub>p</sub>(1 − ρ<sub>f</sub>(p<sup>k</sup>)/p<sup>k</sup>) &gt; 0.</p>
<p>No primitivity or sign condition is needed. The rest of the paper:</p>
<ul>
<li>Theorem 1.1 rests on Proposition 1.4, the large-prime tail: #{X &lt; n ≤ 2X : p<sup>k</sup> | f(n) for some prime p &gt; X} ≪ X<sup>1−δ</sup>.</li>
<li>Corollary 1.2 extends Theorem 1.1 to every d ≥ 4, citing Browning (in Xiao's form) for d ≥ 9.</li>
<li>Corollary 1.3 does the same for products and families of polynomials whose irreducible factors have degree at most k+2. Its proof also cites Reuss and Xiao.</li>
</ul>
<p>For #978 this answers both parts that were open. Every irreducible quartic with no fixed square divisor takes squarefree values with the predicted positive density. n<sup>4</sup>+2 is one: it is Eisenstein at 2, and f(0) = 2 is divisible by no prime square. The page's (d−2)-question is answered for every degree d ≥ 4, with density rather than just infinitude, and without the page's restriction that d is not a power of 2 or its positive leading coefficient.</p>

<p><strong>The argument.</strong> The paper follows Reuss's framework for power-free values: factorisation in a number field, plus approximate determinants. It adds new pieces.</p>
<ul>
<li><strong>§2</strong> reduces the density to Proposition 1.4. It uses a finite sieve for small primes, the bound ρ(p<sup>k</sup>) ≤ d (by Hensel, outside a finite set of primes) for primes between the cut-off and X, and the tail for primes above X. The limit in X is taken before the sieve cut-off goes to infinity.</li>
<li><strong>§3</strong> proves a uniform affine counting theorem. It counts integer points of bounded weighted size on algebraic sets whose equations may change from box to box, given lower bounds on the weighted Hilbert functions of their subvarieties. The proof cuts residue classes at auxiliary primes. A random deletion argument handles the primes at which later, moving equations fail to give smooth local coordinates.</li>
<li><strong>§4</strong> factors the ideal (n−θ) in K = ℚ(θ) as α<sup>k</sup>β = μ(n−θ), with balanced conjugates of sizes P<sup>1/d</sup> and X<sup>b/d</sup>. The integer coordinates of α and β fill two boxes.</li>
<li><strong>§§5–9</strong> cut the paired boxes by archimedean determinants, change to reduced lattice coordinates, and compute weighted Hilbert bounds. They add explicit surface and curve geometry for quartics. On a curve the extreme case is a quintic polynomial with four prescribed critical values. Its integer values form one set of size O(X<sup>1/5</sup>), which is deleted once, before any box is counted (Proposition 8.2).</li>
<li><strong>§10 and Appendix A</strong> choose the parameters and check the exponent margins with an exact finite certificate.</li>
<li><strong>§11</strong> assembles the tail. For large η = log p/log X it counts directly on the surface f(x) = yz<sup>k</sup> (§11.1). Elsewhere it uses the number-field count (§11.2). Every box exponent there is below 24979/25000, and every removed-fibre exponent in the quartic mode is below 3122/3125. These are uniform bounds from the 999/1000 certificate; Table 1's are stronger.</li>
</ul>

<p><strong>The Lean, and our replay.</strong> OpenAI's comparator challenge (<code>ComparatorChallenges/PowerFreeValues.lean</code>) states <code>OAI.QuarticPowerFree.allDegrees</code>, which is Corollary 1.2. Take f ∈ ℤ[x] irreducible over ℚ with natDegree ≥ 4 and <code>LocallyAdmissible f (natDegree − 2)</code>. Then:</p>
<ul>
<li>the local factors are multipliable;</li>
<li>their product is positive;</li>
<li>count − c·X = o(X) as real X → ∞.</li>
</ul>
<p>The solution, <code>OAI.NumberTheory.PowerFree.Main</code>, is 63 modules and 23,269 lines, and it imports nothing but Mathlib.</p>
<p>We compiled all 63 from source on our machine with Lean v4.34.1 and Mathlib d13f23b7, the repository's pins. We built module by module, with no cache for anything but Mathlib: 63 of 63, 0 errors, 0 warnings, 17 minutes of wall time, peak 6.8 GiB. Only one module ever ran at a time, because the 63 files form a single import chain. The checks on the result:</p>
<ul>
<li><code>#print axioms</code> under <code>--trust=0</code> gives exactly propext, Classical.choice and Quot.sound for <code>allDegrees</code>.</li>
<li>The fully elaborated (<code>pp.all</code>) printouts of <code>allDegrees</code> and of the seven definitions it uses match the comparator's character for character, after collapsing whitespace: 8 of 8. The definitions are PowerFree, rho, count, LocallyAdmissible, localFactor, densityConstant and DensityStatement.</li>
<li>A mutation test of the matching script caught all eight mutants: a product in place of the power in PowerFree, Ico in place of Icc in the count, big-O in place of little-o, degree 5 in place of 4, an added axiom, the challenge's sorry removed, a missing block and a missing file.</li>
<li>A planted <code>sorry</code> surfaces as <code>sorryAx</code>.</li>
<li>We scanned the 63 files and the challenge for <code>sorry</code>, <code>axiom</code>, <code>native_decide</code>, <code>implemented_by</code>, <code>extern</code>, <code>unsafe</code>, <code>opaque</code>, meta code and <code>set_option</code>. The only hit is the challenge's own <code>sorry</code>; there is not a single <code>set_option</code> in the closure.</li>
</ul>
<p>A second check by <code>leanchecker --fresh</code> covered the whole environment: Mathlib, OpenAI's 63 modules and our bridge. It re-checks every declaration from the stored terms through the kernel, independently of the build's elaboration, and it re-checks Mathlib's cached files too, which <code>--trust=0</code> does not. It exited 0 after 3,502 seconds (peak 8.2 GiB). Its control, run on a module that does not exist, fails as it should.</p>
<p><strong>We were not first.</strong> Two third-party replays ran OpenAI's Comparator on this challenge before us:</p>
<ul>
<li>carlostoledo1891/cert-machine (GitHub Actions run 38019899278, committed 10 October). Both Lean's kernel and the independent nanoda kernel accepted the solution.</li>
<li>nealmcb/openai-math-lean-tooling. It accepted PowerFreeValues on 11 October, same pins, the same 63-module closure, as part of a run over all 416 challenges recorded on 13 October.</li>
</ul>
<p>Ours is a third, independent replay. Comparator compares the theorem against the challenge, but this challenge's configuration lists no definitions for it to compare (its <code>definition_names</code> is empty). Ours adds a <code>pp.all</code> match of the seven definitions the statement names, under a mutation-tested matcher. It also adds the module-by-module build, the source scan and the Formal Conjectures bridge below. Our own literature seat had searched for the namespace and missed both; they appear under the challenge's name, and the blind reader found them.</p>

<p><strong>The Lean does not follow the paper.</strong> Seat L read all 63 files against the paper. The closure has no comments, so its map of files to sections is by content.</p>
<p>What the kernel-checked proof shares with the paper:</p>
<ul>
<li>the sieve transfer (§2) and the balanced factorisation of Lemma 4.1;</li>
<li>an affine counting theorem of Theorem 3.1's shape, which is itself a determinant method with cuts at auxiliary primes;</li>
<li>weighted Hilbert thresholds of §7's shape;</li>
<li>quartic surface and curve alternatives of its own, in the spirit of §§8–9.</li>
</ul>
<p>Then it takes a shorter route:</p>
<ul>
<li><strong>No archimedean cut.</strong> It never makes the archimedean (Taylor) determinant cut of §5. Instead it applies the counting theorem to the whole (d+1)-dimensional norm variety in ℤ<sup>2d</sup>. The coordinates are those of α and β in a fixed integral basis, and the equations are a<sub>i</sub><sup>k</sup>b<sub>i</sub> − a<sub>0</sub><sup>k</sup>b<sub>0</sub> = θ<sub>0</sub> − θ<sub>i</sub>. This needs a top-dimensional threshold the paper never states.</li>
<li><strong>Exceptional fibres, arithmetically.</strong> A fixed n gives one point. A fixed α gives at most a bounded number, since ρ(p<sup>k</sup>) ≤ d and p<sup>k</sup> &gt; X. For "radial" fibres α′ = cα, prime norms force c = ±1.</li>
<li><strong>Its own certificates.</strong> For 5 ≤ d ≤ 8 it uses one box for the whole range of η, with exponents U = 1/3 and V = 2/5. For d = 4 it uses 100 bins in η, with a certificate checked by kernel <code>decide</code>. The tail saving is X<sup>−3/1000</sup> for 4 ≤ d ≤ 8. L re-checked every certificate inequality in exact arithmetic, and all hold. The closest calls: for d = 5 the exponent sum meets its 997/1000 bound exactly (allowed, since the inequality is ≤), and the full-dimension thresholds clear their envelopes by as little as 0.00049 (d = 7) and 0.00059 (d = 4, first bin).</li>
<li><strong>d ≥ 9 without Browning.</strong> It proves d ≥ 9 itself, using the paper's own §11.1 device: the surface f(x) = yz<sup>k</sup> in two weight boxes, with saving X<sup>−1/2000</sup>. No result of Browning, Xiao, Heath-Brown or Reuss enters anywhere. L notes the paper could have done the same: on [1, d/k], η(1 − kη/d) is largest at η = 1, where it is 2/d ≤ 2/9, well inside the range §11.1 handles.</li>
</ul>
<p>So the Lean needs none of the following: Lemma 4.2, §§5–6, Proposition 8.2 (the quintic deletion), Proposition 10.1, Appendix A, §11.1 in degrees d ≤ 8, or Browning's theorem. Its quartic surface bound is its own analogue of Proposition 8.1, with different alternatives. Two things follow.</p>
<ul>
<li>If the replay is right, no objection to those parts of the paper can sink Theorem 1.1, Corollary 1.2 or #978.</li>
<li>The Lean cannot vouch for those parts either. They stand on the paper alone, and so do Corollary 1.3 and §12, which have no formal counterpart.</li>
</ul>

<p><strong>Formal Conjectures' three statements of #978, proved in Lean (ours).</strong> Formal Conjectures has two statements tagged "research solved" since PR #6898 (merged 11 October), each with a link to OpenAI's <code>allDegrees</code>:</p>
<ul>
<li><code>Erdos978.erdos_978.parts.ii</code>: infinitely many (d−2)-power-free values;</li>
<li><code>parts.iii</code>: {n | Squarefree (n<sup>4</sup>+2)} is infinite.</li>
</ul>
<p>Their proofs are still <code>sorry</code>. So is that of <code>variants.sub_two</code>, which is Browning's d ≥ 9 case. Our file <code>Bridge978.lean</code> proves verbatim copies of all three from OpenAI's theorem. A script checks the copies against FC at a7b87c8d, and a mutated copy fails the check. The steps:</p>
<ul>
<li>Irreducible in ℤ[X] with positive degree gives primitive, and Gauss's lemma then gives irreducible over ℚ.</li>
<li>FC's local condition (for every p, some n ≥ 0 with p<sup>k</sup> ∤ f(n)) gives ρ(p<sup>k</sup>) &lt; p<sup>k</sup>, by reducing n mod p<sup>k</sup>.</li>
<li>A positive density makes the count unbounded, so the set is infinite.</li>
<li>OpenAI's PowerFree (no prime k-th power divides a) and FC's Powerfree (x<sup>k</sup> | a forces x to be a unit) give the same set.</li>
<li>For <code>parts.iii</code>, X<sup>4</sup>+2 is irreducible by Eisenstein at 2, local admissibility comes from f(0) = 2, and Squarefree in ℕ is matched to PowerFree 2 in ℤ.</li>
</ul>
<p>The file also proves the density form in FC's own vocabulary. FC currently states density only for Hooley's (d−1) case (<code>parts.i</code>). Our form: {n | Powerfree (d−2) (f(n))} has natural density equal to OpenAI's Euler product, in FC's <code>Set.HasDensity</code> (which counts 0 ≤ n &lt; b), and so it has positive density.</p>
<p>This form needs neither the restriction that d is not a power of 2 nor a sign condition. That matters because FC's <code>parts.ii</code> keeps the page's preamble excluding powers of 2. Read literally, the preamble removes every power-of-two degree (4, 8, 16, …), including 4 and 8 from Theorem 1.1's new range. Quartics enter FC only through <code>parts.iii</code>.</p>
<p>The seven top-level bridge theorems (the file's other six are lemmas they use) depend only on propext, Classical.choice and Quot.sound under <code>--trust=0</code>. Three mutants behave as they should:</p>
<ul>
<li>With the conclusion's exponent d−2 changed to d−3, the proof fails at the step that uses the exponent.</li>
<li>With the local condition dropped, it fails where it tries to supply local admissibility. That statement is false: DeepMind's degree-6 polynomial is a counterexample.</li>
<li>With a <code>sorry</code> planted in the density-to-infinitude lemma, <code>sorryAx</code> appears in the axioms of all three FC theorems.</li>
</ul>

<p><strong>The reading.</strong> Four seats, all Claude Opus 5.5, were each briefed to refute, to quote the sentence they objected to by the paper's printed numbering, and to grade every objection FATAL, GAP, ERROR or EXPOSITION:</p>
<ul>
<li>seat M1: §§2–4, §10 with Appendix A, and §11;</li>
<li>seat M2: §§5–9 and §12;</li>
<li>seat L: the Lean against the paper;</li>
<li>seat W: the sources and the world.</li>
</ul>
<p>A fifth seat read this page blind against the files. None found a FATAL error, or a gap in Theorem 1.1, Corollary 1.2 or anything #978 needs. M1, M2 and L returned HOLDS AS READ. W returned HOLDS AS READ on the Erdős sourcing, the cited ranges and the priority record, and one minor GAP, in Corollary 1.3 (below). The blind reader's corrections (among them that ours was not the first replay) are applied on this page.</p>
<ul>
<li><strong>M1 recomputed the certificate of §10 and Appendix A in exact arithmetic,</strong> independently of the paper's own listing, which also runs and passes.
<ul>
<li>The cells of width 1/3000 in η are closed and contiguous, and they cover η = 1 up to the stopping point. The direct-surface range of §11.1 covers the rest up to d/k, including b = 0 and the O(1/log X) overshoot.</li>
<li>Every margin is strictly positive. The tightest exponent gap is 0.0019350 (d = 4, cell 3555, η ∈ [1.18500, 1.18533]); Table 1's 0.00191 is a rigorous lower bound for it.</li>
<li>One cut inequality of (10.4) holds by a relative margin of only 1.5·10<sup>−8</sup> (d = 4, cell 4902), because w is the least grid point that works. It is strict, so it is valid, but the "sufficiently large" in Proposition 5.2 is enormous there. That costs nothing, since no effective δ is claimed.</li>
<li>Six mutations each make M1's checker fail: a gap of 10<sup>−6</sup> in one cell, a raised stopping threshold, a weaker top-dimensional threshold, and w shrunk by 1% in one cell, plus two that matter for the route. Replacing the quartic curve constant g = 4 by 3 (no quintic deletion) breaks 434 cells, and replacing the quartic surface bound 3/U<sup>2</sup> by 2/U<sup>2</sup> breaks 609. So the paper's quartic route really does need Propositions 8.1 and 8.2.</li>
<li>The Lean uses g = 3 and its own analogue of Proposition 8.1, with different alternatives. It needs no quintic deletion, because it counts on a different variety.</li>
</ul></li>
<li><strong>M1 on the saving.</strong> The paper never computes the δ of Proposition 1.4. From its own certificate it is at most about 5·10<sup>−4</sup>. The limit is set by the direct range, where 1/2 + √(b′η′/d) reaches 0.99954 for d = 8 and 0.99943 for d = 4, not by Table 1's gaps. The Lean's 3/1000 is larger than anything the paper's route gives; the two agree only in being positive.</li>
<li><strong>M1 on §§2–4.</strong>
<ul>
<li>The sieve transfer takes its limits in a valid order: cut-off fixed, X → ∞, then the cut-off, then the dyadic pieces.</li>
<li>(2.2) is right for every e ≥ 1, and local admissibility forces e &lt; k. The tail is the primitive part's once X exceeds the content primes.</li>
<li>Every constant inside §3 is independent of the coefficients of the moving varieties, because Theorem 3.1 pushes all the uniformity into its hypotheses. The weakest link is therefore whether Propositions 7.1, 8.1 and 9.2 hold uniformly for every subvariety in moving coordinates, which is M2's ground.</li>
<li>The box sizes of §4 depend only on f, and the bound of at most k<sup>d</sup> root choices holds.</li>
<li>Expository: §11 needs its dyadic intervals anchored at P = 2<sup>i</sup>X. Otherwise the first η falls just below 1, where no cell of the main theorem applies.</li>
</ul></li>
<li><strong>M2 read §§5–9, checked the rest by hand, and computed every Hilbert-function claim that can be made concrete.</strong>
<ul>
<li>Both determinant cuts in §5 take a kernel vector against a basis of the component's own coordinate space, so the form they produce cannot vanish identically on that component. The split into mixed and pure equations is exhaustive, because the bidegree is never (0,0).</li>
<li>The Hilbert bounds are bounds on the variety actually present. Random-point evaluation ranks modulo a prime equal the paper's complete-intersection series exactly, with no mismatch, in three families: the bicone of Lemma 5.1 (10 bidegrees, d = 4 and 5), a saturated first-cut component (5 bidegrees), and three examples of Proposition 7.1's pair image under five weightings (15 runs). In two of those three examples (10 of the 15 runs), and for the first-cut component, the unsaturated weight would have given the wrong count. So the saturation step is needed, and it is right.</li>
<li>The surface case analysis of §8.1 (an a-image of degree ≥ 3, 2 or 1) is exhaustive. In the plane case both alternatives the paper rules out are genuinely impossible.</li>
<li>Uniformity in moving equations, coordinate changes and boxes is argued at every place it is used.</li>
</ul></li>
<li><strong>M2 on the quintic set (Proposition 8.2).</strong> An exact resultant computation finds exactly 25 normalised quintics with critical values (1, i, −1, −i). It finds 25 again for a reordering and 25 for generic values (0, 1, 3, 7): the Hurwitz count 5<sup>5−3</sup>. The roots of x<sup>4</sup>+1 and x<sup>4</sup>+2 reduce to (1, i, −1, −i) after scaling. The critical values are the roots of f, fixed before any box, curve or prime is chosen. So the set of their integer values, O(X<sup>1/5</sup>) of them, is one global set, and deleting it once is legitimate. The paper says only "finitely many"; stating 25 would let a reader check it.</li>
<li><strong>M2 on §12</strong> (the worked example n<sup>4</sup>+1) found it consistent with the general argument. Its enlarged-cell certificate passes in exact arithmetic (gap − 4τ = 1941/10<sup>5</sup>), ℤ[ζ<sub>8</sub>] is norm-Euclidean by the rounding argument given, and the Pell estimate holds.</li>
<li><strong>One GAP, in Corollary 1.3 only.</strong> For d = k+1 the proof cites Reuss's Lemma 3, its proof and his §6 for the triple count. W graded this a GAP. Reuss's §§2–3 work in ℤ[θ] with θ integral, that is, for monic f. The paper applies them to a primitive, possibly non-monic g without the standard reduction (substitute y = cn, so that c<sup>d−1</sup>g(y/c) is monic). W adds that Reuss's statement is for general irreducible f, so the citation is defensible. M1 checked the same citation for a different point: the estimate is assembled from Reuss's proof text rather than stated, which M1 graded EXPOSITION; it did not examine the monic reduction. The gap is fillable, it touches only Corollary 1.3, and Corollary 1.3 has no Lean.</li>
<li><strong>Smaller points.</strong>
<ul>
<li>Booker–Browning 2016 is not cited for the k = 2 case of Corollary 1.3 (W).</li>
<li>The Erdős history omits [Er81h] (W).</li>
<li>Xiao's Theorem 9.1 needs no primitivity step, and the estimate taken from Xiao's §9 sits inside a proof sketch; Browning 2011 is the primary source (M1, W).</li>
<li>W could not fetch Browning 2011 itself. Its range r ≥ (3d+1)/4 rests on three secondary statements (Xiao, Heath-Brown 2013, Reuss), which agree.</li>
</ul></li>
</ul>

<p><strong>Numbers (computer-assisted, label (d); they test nothing about the theorem).</strong> For f = x<sup>4</sup>+2, ρ(p<sup>2</sup>) is 2 for p ≡ 3 mod 8, either 4 or 0 for p ≡ 1 mod 8, and 0 otherwise. Our July report proves this, and checks the formula by brute force for p ≤ 10<sup>4</sup>. The predicted density is c ≈ 0.7566840, enclosed rigorously in July between 0.75668370 and 0.75668401. For x<sup>4</sup>+1 it is c<sub>8</sub> = ∏<sub>p≡1 (8)</sub>(1 − 4/p<sup>2</sup>) ≈ 0.9808175. The counts:</p>
<table style="margin:1em 0;border-collapse:collapse"><thead><tr><th style="padding:2px 10px">N</th><th style="padding:2px 10px">#{n ≤ N : n<sup>4</sup>+2 squarefree}</th><th style="padding:2px 10px">share</th><th style="padding:2px 10px">#{n ≤ N : n<sup>4</sup>+1 squarefree}</th><th style="padding:2px 10px">share</th></tr></thead><tbody>
<tr><td style="padding:2px 10px;text-align:right">10<sup>5</sup></td><td style="padding:2px 10px;text-align:right">75,670</td><td style="padding:2px 10px;text-align:right">0.75670</td><td style="padding:2px 10px;text-align:right">98,090</td><td style="padding:2px 10px;text-align:right">0.98090</td></tr>
<tr><td style="padding:2px 10px;text-align:right">2·10<sup>5</sup></td><td style="padding:2px 10px;text-align:right">151,346</td><td style="padding:2px 10px;text-align:right">0.75673</td><td style="padding:2px 10px;text-align:right">196,180</td><td style="padding:2px 10px;text-align:right">0.98090</td></tr>
<tr><td style="padding:2px 10px;text-align:right">10<sup>6</sup></td><td style="padding:2px 10px;text-align:right">756,674</td><td style="padding:2px 10px;text-align:right">0.756674</td><td style="padding:2px 10px;text-align:right">980,831</td><td style="padding:2px 10px;text-align:right">0.980831</td></tr>
<tr><td style="padding:2px 10px;text-align:right">limit</td><td style="padding:2px 10px;text-align:right"></td><td style="padding:2px 10px;text-align:right">0.756684</td><td style="padding:2px 10px;text-align:right"></td><td style="padding:2px 10px;text-align:right">0.980817</td></tr>
</tbody></table>
<p>Each count was made twice, by different methods.</p>
<ul>
<li><strong>By factoring every n<sup>4</sup>+w in PARI/GP.</strong> Our July run covered n<sup>4</sup>+2 to 10<sup>5</sup>, with its factorisations certified by a separate program. Today we ran both polynomials to 10<sup>5</sup> and to 2·10<sup>5</sup>, and seat M2 ran both to 10<sup>6</sup>.</li>
<li><strong>By a sieve that factors nothing.</strong> It runs over every prime p ≤ 10<sup>6</sup>, marking the classes n ≡ r mod p<sup>2</sup> for each root r of x<sup>4</sup>+w lifted from p to p<sup>2</sup>.</li>
</ul>
<p>The two agree at every checkpoint. A version of the sieve with the lift removed gives 65,353 at 10<sup>5</sup>, so the agreement is not automatic.</p>
<p>The large-prime tail that Proposition 1.4 is about is tiny here. Factoring every value up to 10<sup>6</sup> (M2's run; ours to 10<sup>5</sup> agrees) finds only two n with p<sup>2</sup> | n<sup>4</sup>+2 for a prime p &gt; n: n = 2 (p = 3) and n = 97 (97<sup>4</sup>+2 = 179<sup>2</sup>·2763). For n<sup>4</sup>+1 there are none. The sieve is exact for N ≤ 10<sup>6</sup> only because of this census: a prime p &gt; 10<sup>6</sup> with p<sup>2</sup> | f(n) and n ≤ 10<sup>6</sup> would have p &gt; n, and none does.
</p>

<p><strong>Sources and the world.</strong></p>
<ul>
<li><strong>Erdős's three sentences</strong> are quoted above from the page images of [Er53] (users.renyi.hu/~p_erdos/1953-02.pdf), [Er65b] (1965-17.pdf) and [Er81h] (1981-33.pdf), read by seat W. The paper cites the first two, not [Er81h].</li>
<li><strong>The two earlier claims did not hold up.</strong>
<ul>
<li><em>Zapata Ceballos and Jalalvand</em> (arXiv 2608.10335, v1 11 August 2026) claimed positive squarefree density for monic irreducible polynomials of degree 2q, q prime, with squarefree fixed divisor, whose field contains a degree-q Galois subfield. Their Corollary 2.4 covers every monic quartic whose Galois group is neither S<sub>4</sub> nor A<sub>4</sub> (with squarefree fixed divisor), and so x<sup>4</sup>+2 as well. The paper cites v1 as a claim it does not use, and says it "includes n<sup>4</sup>+1"; it included n<sup>4</sup>+2 too. The authors withdrew it on 15 October: "The proof of Proposition 2.3 is incomplete. The argument does not provide the estimate needed to control the contribution of square divisors arising from prime ideals of large norm." That is the large-prime tail, the step Proposition 1.4 is about.</li>
<li><em>Carella</em> (arXiv 2310.16952, 2023, math.GM, one version, unrefereed) claims n<sup>4</sup>+1 and n<sup>4</sup>+2 with a power saving. Our July report found a sign error in its decisive fractional-part estimate, and noted that its constant 0.757159 lies outside our enclosure of the true density. Seat W adds that its constant for n<sup>4</sup>+1 is also wrong (0.981003 against 0.980817), and so is its Theorem 1.3 constant (0.9638 where the density is 0.9006).</li>
</ul></li>
<li><strong>Uncited prior work.</strong> Booker and Browning (Discrete Analysis 2016:8, Theorem 1.2) already proved the k = 2 case of Corollary 1.3 for factors of degree at most 3, by the same factor-by-factor tail.</li>
<li><strong>The record elsewhere.</strong>
<ul>
<li>The teorth database still lists #978 as open (last update 31 August 2025).</li>
<li>The problem page was last edited on 31 March 2026. It does not mention OpenAI, lists no proof claims, and has suspended comments.</li>
<li>Formal Conjectures marked parts ii and iii solved in PR #6898 (Moritz Firsching, merged 11 October). Its stated checks are a build of FC's own changed files, resolution of the link, a grep of the release for <code>sorry</code>, and inspection of the comparator configuration. It did not build or replay OpenAI's proof. FC's status-mismatch bot issue #7135 is open.</li>
<li>A preprint of 21 October on random polynomials (arXiv 2610.29911) still says the squarefree asymptotic is known only up to degree 3 (Hooley), and does not cite OpenAI.</li>
</ul></li>
<li><strong>The paper and its Lean have not changed since release.</strong> The manuscript, <code>Main.lean</code> and the whole <code>PowerFree</code> directory have the same git hashes at the initial commit (adc7f12, 6 October) and at the current head (1581d4c). FC's link (<code>Main.lean#L144</code>) points at <code>allDegrees</code>.</li>
</ul>

<p><strong>What this entry is.</strong> The theorem is OpenAI's, and its proof is OpenAI's model's. What is ours:</p>
<ul>
<li>the third kernel replay and its controls;</li>
<li>the readings;</li>
<li>the Lean bridge proving Formal Conjectures' <code>parts.ii</code>, <code>parts.iii</code> and <code>variants.sub_two</code>, plus the density form in FC's vocabulary;</li>
<li>the numbers;</li>
<li>a correction to our own July report.</li>
</ul>
<p>Labels, as used on this site: (a) elementary; (b) rigorous modulo named cited theorems; (c) plausible, unverified; (d) computer-assisted. Theorem 1.1, Corollary 1.2 and the three FC statements are (d): Lean-verified, kernel-replayed here and twice before, unrefereed by any human. Corollary 1.3, §12, and the paper's own route through §§5–6, 8.2, 10 and Appendix A are (c): our AI seats read them, as reported above, nothing formal backs them, and Corollary 1.3 carries the one GAP found.</p>
<p><strong>Where to look for a hole.</strong> In the formal claim, these are the places one could hide, and each can be read without trusting the rest:</p>
<ol>
<li>the seven definitions in <code>Model.lean</code>, which the comparator repeats: are they the problem?</li>
<li>the Mathlib notions they use (<code>tprod</code>, <code>Multipliable</code>, <code>IsLittleO</code>, <code>Nat.floor</code>). Seat L checked the two <code>tprod</code> traps: a non-multipliable family has <code>∏'</code> = 1, and a product diverging to 0 counts as multipliable. Both are closed by the statement's explicit <code>Multipliable</code> and <code>0 &lt;</code> conjuncts.</li>
<li>the statement of <code>allDegrees</code>;</li>
<li>the kernel: our replay, which took Mathlib's compiled files from its cache, the <code>leanchecker --fresh</code> pass, and the two earlier replays (one also with nanoda);</li>
<li>our bridge's 330 lines, against FC's text.</li>
</ol>
<p>In the paper, the parts the Lean does not touch are the ones to read hardest:</p>
<ul>
<li>Lemma 4.2 and §§5–6;</li>
<li>Proposition 8.2, and Proposition 8.1 and the §§7–9 thresholds as stated (the Lean only parallels them);</li>
<li>the certificate of §10 and Appendix A;</li>
<li>§11.1 in degrees d ≤ 8;</li>
<li>the Browning/Xiao citation for d ≥ 9;</li>
<li>Corollary 1.3 and §12.</li>
</ul>
`,
    links: [
      { label: "erdosproblems.com/978 (read 22 Oct 2026: no proof claims, comments suspended, no mention of OpenAI; last edited 31 Mar 2026)", url: "https://www.erdosproblems.com/978" },
      { label: "OpenAI, \"Squarefree values of quartics and power-free values of polynomials\" (family 020, dated 24 Sep 2026, released 6 Oct, 55 pp)", url: "https://github.com/openai/math/tree/main/preprints/Squarefree-values-of-quartics-and-power-free-values-of-polynomials-September-24-2026" },
      { label: "OpenAI's Lean — OAI/NumberTheory/PowerFree (63 modules; entry Main.lean, theorem allDegrees at line 144)", url: "https://github.com/openai/math/tree/main/lean/OAI/NumberTheory/PowerFree" },
      { label: "OpenAI's comparator challenge ComparatorChallenges/PowerFreeValues.lean (the statement and its seven definitions)", url: "https://github.com/openai/math/blob/main/lean/ComparatorChallenges/PowerFreeValues.lean" },
      { label: "Earlier replay: carlostoledo1891/cert-machine — Comparator on PowerFreeValues, Lean's kernel and nanoda accept (run 38019899278, committed 10 Oct 2026)", url: "https://github.com/carlostoledo1891/cert-machine/blob/main/corpus/openai-math/kernel-runs/38019899278/PowerFreeValues.json" },
      { label: "Earlier replay: nealmcb/openai-math-lean-tooling — Comparator over all 416 challenges, PowerFreeValues accepted 11 Oct 2026 (results/cmp-all/configs.csv)", url: "https://github.com/nealmcb/openai-math-lean-tooling" },
      { label: "Formal Conjectures, Erdős 978 at commit a7b87c8d — the three statements our bridge copies (parts.ii and parts.iii tagged research solved, proofs sorry)", url: "https://github.com/google-deepmind/formal-conjectures/blob/a7b87c8d0bb60e73782045d614d4a24907b87b8a/FormalConjectures/ErdosProblems/978.lean" },
      { label: "Formal Conjectures PR #6898 (Moritz Firsching, merged 11 Oct 2026): marks #978 parts ii and iii solved — build, link resolution and a sorry-grep, no kernel replay", url: "https://github.com/google-deepmind/formal-conjectures/pull/6898" },
      { label: "Erdős, \"Arithmetical properties of polynomials\", J. London Math. Soc. 28 (1953) — p. 425: n⁴+2", url: "https://users.renyi.hu/~p_erdos/1953-02.pdf" },
      { label: "Erdős, \"Some recent advances and current problems in number theory\" (1965) — §6, p. 219: (k−2)-th power-free values", url: "https://users.renyi.hu/~p_erdos/1965-17.pdf" },
      { label: "Erdős, \"Some problems and results on additive and multiplicative number theory\" (LNM 899, 1981) — p. 178: \"no quartic polynomial\"", url: "https://users.renyi.hu/~p_erdos/1981-33.pdf" },
      { label: "Heath-Brown, \"Powerfree values of polynomials\" (QJM 2013; arXiv 1103.2028) — binomials x^d + c, and the quartic case named as the open question", url: "https://arxiv.org/abs/1103.2028" },
      { label: "Reuss, \"Power-free values of polynomials\" (arXiv 1307.2802) — the number-field / approximate-determinant framework the paper follows", url: "https://arxiv.org/abs/1307.2802" },
      { label: "Xiao, \"Power-free values of binary forms and the global determinant method\" (IMRN 2017; arXiv 1505.05587) — Theorem 9.1, Browning's d ≥ 9 range as the paper cites it", url: "https://arxiv.org/abs/1505.05587" },
      { label: "Booker and Browning, \"Square-free values of reducible polynomials\" (Discrete Analysis 2016:8; arXiv 1511.00601) — Theorem 1.2, the k = 2 case of Corollary 1.3, uncited by the paper", url: "https://arxiv.org/abs/1511.00601" },
      { label: "Zapata Ceballos and Jalalvand, \"On the squarefree values of degree-2q polynomials\" (arXiv 2608.10335) — v1 11 Aug 2026 claimed n⁴+1 and n⁴+2; withdrawn 15 Oct 2026 at the large-prime-ideal step", url: "https://arxiv.org/abs/2608.10335" },
      { label: "Carella, \"Squarefree values of polynomials\" (arXiv 2310.16952, math.GM, 2023) — an unrefereed claim; our July report found a sign error in its decisive step", url: "https://arxiv.org/abs/2310.16952" },
      { label: "arXiv 2610.29911 (21 Oct 2026, random polynomials) — still says the squarefree asymptotic is known only up to degree 3 (Hooley), and does not cite OpenAI", url: "https://arxiv.org/abs/2610.29911" },
      { label: "Our July 2026 report on #978 (exact counts to 10⁵, the local factors of n⁴+2, a rigorous enclosure of the density; dated correction of 22 Oct on the open range)", url: "/report/978" },
      { label: "Our bundle (repository private at the time of writing; files available on request) — the replay (driver, per-module logs, probes, statement match and its mutation test), the bridge and its controls, the counting programs, referee reports, model receipts, SHA256SUMS", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/978/openai-squarefree-quartics-refereed" },
    ],
  },
