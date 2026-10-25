import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<script.*?</script>','',s,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>','\n',t)
t=html.unescape(t)
lines=[l.strip() for l in t.split('\n') if l.strip()]
print('\n'.join(lines))
