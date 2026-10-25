import json,re,html,urllib.request,urllib.parse,sys
out=open('/tmp/oaimath/158/world/discussion/hn_search_2026-10-14.txt','w')
def p(*a):
    s=' '.join(str(x) for x in a); print(s); out.write(s+'\n')
since=1790000000  # 2026-09-21 approx (control: also run without filter)
for q in ['chromatic number of the plane','five-colorable','five colorable','Hadwiger-Nelson','Hadwiger Nelson','plane needs six colors','weakly measurable coloring']:
    for filt in (True, False):
        params={'query':q,'hitsPerPage':50}
        if filt: params['numericFilters']=f'created_at_i>{since}'
        url='https://hn.algolia.com/api/v1/search_by_date?'+urllib.parse.urlencode(params)
        d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'curl/8.5.0'}),timeout=30))
        p(f'=== query={q!r} since_2026-09-21={filt} nbHits={d.get("nbHits")}')
        if not filt:
            # control: show the newest 3 hits regardless of date, to prove the query matches something
            for h in d['hits'][:3]:
                p('   [control newest]', h['created_at'][:10], h.get('objectID'), (h.get('title') or '')[:60])
            continue
        for h in d['hits']:
            txt=h.get('comment_text') or h.get('story_text') or ''
            txt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',txt)))
            p('  ',h['created_at'][:16], h.get('author'), 'story' if h.get('title') else 'comment', 'id='+str(h.get('objectID')), 'story_id='+str(h.get('story_id')), '|', (h.get('title') or h.get('story_title') or '')[:70], '|', txt[:500])
