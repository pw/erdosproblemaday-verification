import json,sys,os
for f in sorted(sys.argv[1:]):
    try:
        m=json.load(open(f))['message']
    except Exception as e:
        print(os.path.basename(f),'PARSE FAIL',open(f).read()[:100]);continue
    au='; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in m.get('author',[]))
    dp=m.get('published-print',m.get('issued',{})).get('date-parts',[[None]])[0]
    po=m.get('published-online',{}).get('date-parts',[[None]])[0]
    iss=m.get('issued',{}).get('date-parts',[[None]])[0]
    print(os.path.basename(f)[:-5],'|',(m.get('title') or [''])[0][:110],'|',au,'|',(m.get('container-title') or [''])[0],'| vol',m.get('volume'),'iss',m.get('issue'),'pp',m.get('page'),'art',m.get('article-number'),'| print',dp,'online',po,'issued',iss)
