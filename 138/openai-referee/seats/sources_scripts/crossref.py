import json, urllib.request, urllib.parse, time, sys
dois = ["10.1007/s11856-025-2735-0","10.1007/s00493-022-4925-2","10.1016/j.jctb.2015.09.004","10.1002/rsa.3240010307",
"10.1215/S0012-7094-62-02914-9","10.1090/S0894-0347-1988-0929498-X","10.1007/s00039-001-0332-9","10.1007/978-0-387-68361-4_9",
"10.1017/fmp.2022.12","10.4153/CMB-1968-047-7","10.1073/pnas.32.12.331","10.1017/S0080454100017726","10.1112/jlms/s1-11.4.261",
"10.1112/plms/s3-2.1.417","10.1016/S0167-5060(08)70697-6"]
out = {}
for d in dois:
    u = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="/")
    req = urllib.request.Request(u, headers={"User-Agent": "curl/8.5.0 (mailto:me@byclaude.net)"})
    try:
        m = json.load(urllib.request.urlopen(req, timeout=30))["message"]
    except Exception as e:
        print(d, "ERROR", e); continue
    out[d] = m
    dp = (m.get("published-print") or m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])[0]
    print(d, "|", (m.get("title") or [""])[0][:75], "|", (m.get("container-title") or [""])[0][:45], "|", m.get("volume"), m.get("page"), "|", dp, "|", ", ".join(a.get("family", "") for a in m.get("author", [])))
    time.sleep(0.5)
json.dump(out, open(sys.argv[1], "w"))
