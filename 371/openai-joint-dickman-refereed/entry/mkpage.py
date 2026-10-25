import html
t = open('fc_issue_title.txt').read().strip(); b = open('fc_issue_body.md').read().strip()
style = open('/home/exedev/Handoff/reports/erdos304-fc-issue-2026-10-21.html').read().split('<style>')[1].split('</style>')[0]
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Erdős #371 — Formal Conjectures issue draft (22 Oct 2026)</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{style}</style></head><body><h1>Erdős #371 — one Formal Conjectures issue, stage only</h1>
<div class="sub">Staged 22 Oct 2026 by the 09:00Z erdos seat (finishing the 06:00Z seat’s #371 work) after the kernel replay, the bridge and leanchecker --fresh (rc 0). <b>Nothing has been posted.</b> Open it (as you, or from a byclaude account) at <a href="https://github.com/google-deepmind/formal-conjectures/issues/new">github.com/google-deepmind/formal-conjectures/issues/new</a>.</div>
<div class="warn">⚠ Before posting: BUNDLE_URL must be public — github.com/pw/ErdosProblemADay.com is PRIVATE; make it public or paste verification/371/openai-joint-dickman-refereed/bridge/Bridge371.lean into a gist and use that URL. Note FC’s own merge commit 3dfd999 (PR #6898) listed “Erdős 371 (density over Icc 2 ⌊X⌋ vs Iio b)” as a transport not in the linked proof, so the issue answers a note they wrote; it also proposes a 928.lean (FC has none) with a proof. Interactive posted eight FC items from byclaude this morning with gists — same shape works here if you prefer.</div>
<div class="section"><h2>Title</h2><span class="field-label">Title</span><textarea id="title" rows="2" readonly>{html.escape(t)}</textarea><div class="copybar"><button class="copy" onclick="cp('title',this)">Copy title</button></div></div>
<div class="section"><h2>Body (markdown)</h2><span class="field-label">Body</span><textarea id="body" rows="34" readonly>{html.escape(b)}</textarea><div class="copybar"><button class="copy" onclick="cp('body',this)">Copy body</button></div></div>
<script>function cp(id,btn){{const t=document.getElementById(id);navigator.clipboard.writeText(t.value).then(()=>{{btn.textContent='Copied';btn.classList.add('copied');setTimeout(()=>{{btn.textContent=btn.id;btn.classList.remove('copied')}},1500)}})}}</script>
</body></html>'''
open('/home/exedev/Handoff/reports/erdos371-fc-issue-2026-10-22.html', 'w').write(page); print('written', len(page))
