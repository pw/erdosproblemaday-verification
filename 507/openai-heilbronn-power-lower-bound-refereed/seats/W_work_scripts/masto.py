import json, sys, urllib.request, re, html
inst, acct, since, pat = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))
aid = get(f"https://{inst}/api/v1/accounts/lookup?acct={acct}")["id"]
max_id = None; n = 0; hits = 0; oldest = None
while True:
    u = f"https://{inst}/api/v1/accounts/{aid}/statuses?limit=40" + (f"&max_id={max_id}" if max_id else "")
    st = get(u)
    if not st: break
    for s in st:
        n += 1; oldest = s["created_at"]
        txt = html.unescape(re.sub("<[^>]+>", " ", s["content"]))
        if re.search(pat, txt, re.I):
            hits += 1; print(s["created_at"], s["url"], " ".join(txt.split())[:600]); print("--")
    max_id = st[-1]["id"]
    if st[-1]["created_at"] < since: break
print(f"scanned {n} statuses back to {oldest}; hits {hits}")
