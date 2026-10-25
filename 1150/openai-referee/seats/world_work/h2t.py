import sys,re,html
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<br\s*/?>','\n',t); t=re.sub(r'</(p|div|li|h\d)>','\n',t)
t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
t=re.sub(r'\n\s*\n+','\n\n',t)
print(t)
