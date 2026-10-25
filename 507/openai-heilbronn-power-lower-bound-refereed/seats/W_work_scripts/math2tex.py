import re, sys, html
t = open(sys.argv[1]).read()
# replace each <math ...>...</math> with its alttext or TeX annotation
def rep(m):
    s = m.group(0)
    a = re.search(r'alttext="([^"]*)"', s)
    if a: return ' $' + html.unescape(a.group(1)) + '$ '
    b = re.search(r'<annotation[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>', s, re.S)
    if b: return ' $' + html.unescape(b.group(1)) + '$ '
    return ' [MATH:' + ' '.join(re.sub('<[^>]+>', ' ', s).split()) + '] '
t = re.sub(r'<math\b.*?</math>', rep, t, flags=re.S)
t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
t = re.sub(r'<(p|h[1-6]|div|li|section)\b[^>]*>', '\n', t)
t = re.sub(r'<[^>]+>', '', t)
t = html.unescape(t)
t = re.sub(r'[ \t]+', ' ', t)
t = re.sub(r'\n\s*\n+', '\n\n', t)
print(t)
