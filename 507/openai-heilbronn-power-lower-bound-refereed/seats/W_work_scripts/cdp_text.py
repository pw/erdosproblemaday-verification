import sys, json, time, re, urllib.request, websocket
# usage: cdp_text.py PORT URL OUTFILE [WAIT_ROUNDS] [text|html]
port, url, out = sys.argv[1], sys.argv[2], sys.argv[3]
wait = int(sys.argv[4]) if len(sys.argv) > 4 else 25
mode = sys.argv[5] if len(sys.argv) > 5 else "text"
BODY = "document.documentElement.outerHTML" if mode == "html" else "document.body.innerText"
EXPR = "document.title + '\\n@@URL ' + location.href + '\\n' + (document.body ? " + BODY + " : '')"
req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
tab = json.load(urllib.request.urlopen(req, timeout=20))
wsurl = re.sub(r"ws://[^/]+/", f"ws://127.0.0.1:{port}/", tab["webSocketDebuggerUrl"])
try:
    ws = websocket.create_connection(wsurl, timeout=60, suppress_origin=True)
    i = [0]
    def call(method, **params):
        i[0] += 1
        ws.send(json.dumps({"id": i[0], "method": method, "params": params}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == i[0]:
                return m
    call("Page.enable")
    call("Page.bringToFront")
    call("Page.navigate", url=url)
    text = ""
    for k in range(wait):
        time.sleep(2)
        r = call("Runtime.evaluate", expression=EXPR, returnByValue=True)
        text = r.get("result", {}).get("result", {}).get("value", "") or ""
        if "Just a moment" not in text[:300] and len(text) > 5000:
            time.sleep(4)
            r = call("Runtime.evaluate", expression=EXPR, returnByValue=True)
            text = r.get("result", {}).get("result", {}).get("value", "") or text
            break
    if mode == "scroll":
        js = "(function(){var els=[document.scrollingElement].concat(Array.from(document.querySelectorAll('*')).filter(e=>e.scrollHeight>e.clientHeight+50 && getComputedStyle(e).overflowY!='visible'));els.forEach(e=>{e.scrollTop+=Math.max(400,e.clientHeight*0.8)});return els.length})()"
        for k in range(60):
            call("Runtime.evaluate", expression=js, returnByValue=True)
            time.sleep(1.2)
        r = call("Runtime.evaluate", expression=EXPR, returnByValue=True)
        text = r.get("result", {}).get("result", {}).get("value", "") or text
    open(out, "w").write(text)
    print(len(text), text[:200].replace("\n", " | "))
    ws.close()
finally:
    urllib.request.urlopen(f"http://127.0.0.1:{port}/json/close/{tab['id']}", timeout=10)
