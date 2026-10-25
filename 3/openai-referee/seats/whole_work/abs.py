import re,sys,html,os
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8',errors='replace').read()
    title=re.search(r'<meta name="citation_title" content="([^"]*)"',t)
    authors=re.findall(r'<meta name="citation_author" content="([^"]*)"',t)
    hist=re.search(r'<div class="submission-history">(.*?)</div>',t,re.S)
    h=re.sub(r'<[^>]+>',' ',hist.group(1)) if hist else 'NO HISTORY'
    h=re.sub(r'\s+',' ',html.unescape(h))
    jref=re.search(r'<td class="tablecell jref">(.*?)</td>',t,re.S)
    doi=re.search(r'<td class="tablecell doi">(.*?)</td>',t,re.S)
    com=re.search(r'<td class="tablecell comments[^"]*">(.*?)</td>',t,re.S)
    print('=='+os.path.basename(f))
    print(' title:',html.unescape(title.group(1)) if title else None)
    print(' authors:',[html.unescape(a) for a in authors])
    print(' hist:',h[:900])
    if jref: print(' jref:',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',jref.group(1))))
    if doi: print(' doi:',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',doi.group(1))))
    if com: print(' comments:',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',html.unescape(com.group(1))))[:300])
