# Blind read — /day/505 entry draft (erdosproblemaday.com), before deploy
You are a hostile copy-editor + fact-checker. Read /tmp/oaimath/156/entry/entry_rendered.js (the page: title, summary, body HTML, links) and
/tmp/oaimath/156/entry/headline_rendered.js (front-page card). For EVERY factual sentence, find the file that supports it and say SUPPORTED /
WRONG / UNSUPPORTED / OVERCLAIM, quoting the sentence. Evidence (read-only):
- paper: /tmp/oaimath/156/paper.txt (render pages with pdftoppm from paper.pdf if a formula looks garbled); Lean source /tmp/oaimath/156/repo/lean/
- replay: /tmp/oaimath/156/lean-build/{driver.log,modules.tsv,steps.tsv,statement_match.txt,logs/,mut/MUTATION_RESULTS.txt,ESTIMATE.md}
- bridge: /tmp/oaimath/156/bridge/{Bridge505.lean,BridgeMut.lean,BridgeWrongShape.lean,*.log}; FC originals /tmp/oaimath/156/world/FC_*.lean
- finite step: ~/MathDyad/erdos505/{tensystem_cnf.py,check_models.py,triangle_systems.py,core_locality.py,runs/,cnf/}
- cover: ~/MathDyad/erdos505/{verify_cover.py,exact_radius.py,sample_cover.py,*.json,search_n*.log}; bundle copy ~/ErdosProblemADay-main/verification/505/borsuk-nine-refereed/cover/verify_runs.log
- seat reports: /tmp/oaimath/156/seats/seat{T_topology,F_formal,W_world}.md (+ w_dl/ downloads incl. walkup1970.txt, kalai1505.txt, acprk note /tmp/oaimath/156/world/acprk_03-borsuk.md)
- live captures: /tmp/oaimath/156/live/
Look especially for: numbers that do not match the logs (times, counts, degrees, M values); claims attributed to the wrong party; 'first'/'only'/'no one'
claims; anything the page says WE did that the files do not show; section numbers (cite the PAPER's printed numbers); overclaiming what a check proves
(e.g. what #print axioms shows, what a SAT UNSAT shows, what the bridge proves vs FC's own environment); sentences a mathematician would read as
stronger than the evidence. Also flag unclear prose. Do not edit anything; do not contact anyone; scripts under `ulimit -v 8000000`.
Output: /tmp/oaimath/156/seats/blind_read.md — a numbered list (WRONG/OVERCLAIM first), each with the quoted sentence and the fix. Reply with the counts and the top 5.
