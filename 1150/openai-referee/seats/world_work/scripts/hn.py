import json,html,re,sys
d=json.load(open(sys.argv[1]))
print('nbHits',d.get('nbHits'))
for h in d['hits'][:40]:
    t=h.get('title') or h.get('story_title')
    c=re.sub(r'<[^>]+>',' ',html.unescape(h.get('comment_text') or ''))
    print(h['created_at'][:16],h.get('objectID'),'story',h.get('story_id'),h.get('points'),'|',t,'|',(h.get('url') or '')[:80],'|',c[:200].replace('\n',' '))
