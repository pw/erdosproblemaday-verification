# Seat W — world, priority, prior art
Read /tmp/oaimath/191b/seats/BRIEF_common.md first. Your report: /tmp/oaimath/191b/seats/W_report.md; work dir W_work/.
You are not refereeing the math; you are establishing what the world already knows, so our page says exactly what is ours.

1. Has ANYONE checked, refereed, refuted or replicated Blinov's (1/145,278,430 of 13 Oct; 1/50,893,237 of 15 Oct;
   earlier checkpoints) or Chen's (2/100,866,719, 19 Oct) Heilbronn claims? Look at: both repos' issues/PRs/discussions
   (gh api); bigospeedrun.com/other/heilbronn-triangle and its board/race pages (curl with a browser UA); erdosproblems.com
   #507 page, forum thread and proof-claims tab — exe.dev is 403'd there, so fetch through the Hetzner box:
   ssh -i ~/.ssh/hetzner_prod deploy@100.103.211.37 'curl -s -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36" https://www.erdosproblems.com/forum/thread/507'
   (and /507, /forum/thread/507/proof-claims). Also arXiv listings (math.CO/math.MG, Oct 2026) for any Heilbronn
   lower-bound preprint after 6 Oct; any OpenAI update to the family-191 preprint (gh api repos/openai/math/commits).
   Our own earlier page: https://erdosproblemaday.com/day/507-openai-heilbronn-power-lower-bound-refereed (read it).
2. The BOS Heilbronn board: every ranked entry with date, author, claimed η and evidence level, as of now. Anything
   newer than Chen? Any later Blinov checkpoint (check all branches: gh api repos/littleBro/heilbronn-triangle-bounds/branches,
   and commits after 15 Oct)?
3. Who are the authors / systems: Blinov discloses "OpenAI Codex assistance"; Chen's "Euler" (github.com/canghaimeng/Euler)
   — what is it, is it an AI system, what do they disclose? Quote, don't characterise.
4. Lean: is there ANY formalization of an every-n Heilbronn lower bound at Blinov's or Chen's exponent, or of the
   tagged-moment lemma beyond Blinov's own lean/ dir? Search GitHub code by several names (HeilbronnTriangle,
   heilbronn, Problem355, reserved_packing, tagged_small_residue_moment, "50893237", "100866719").
5. Prior art for the ingredients, so we credit correctly: (a) Conner–Gesmundo–Landsberg–Ventura arXiv:1909.04785
   Theorem 4.1 — what exactly does it state (field, the root u, rank 18 for det⊗det?), (b) the slab simplification of
   OpenAI's cap — is it anywhere earlier (e.g. an earlier Blinov checkpoint date)?, (c) Salem–Spencer {0,1}-in-base-3 sets.
6. Known 3-AP-free sets at this size: what is the smallest X for which [0,X] is known to contain a 3-term-AP-free set
   of 2,921 integers? (Literature on lower bounds for r_3(N) around N = 1–2·10⁵: Gasarch–Glenn–Kruskal, Dybizbański,
   OEIS A003002/A065825 and related, any record tables.) This bears on whether Blinov's k is improvable by packing alone.
Search by every name a thing goes by (a namespace, a challenge name, an author handle, a number). A search that
finds nothing is a statement about your queries — list them.
