# Minimal raw-CDP page fetcher: open a fresh tab at URL, wait, dump text + links, close tab.
import json, sys, time, urllib.request, websocket
PORT = 9344
url = sys.argv[1]; wait = float(sys.argv[2]) if len(sys.argv) > 2 else 12
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?{url}", method="PUT")
tab = json.load(urllib.request.urlopen(req, timeout=20))
ws = None
mid = 0
def call(method, **params):
    global mid; mid += 1
    ws.send(json.dumps({"id": mid, "method": method, "params": params}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid: return m
try:
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
    time.sleep(wait)
    expr = sys.argv[3] if len(sys.argv) > 3 else "JSON.stringify({u:location.href,t:document.title,text:document.body?document.body.innerText.slice(0,20000):'',links:[...document.querySelectorAll('a')].map(a=>[a.innerText.slice(0,60),a.href]).filter(x=>/pdf|getFT|download/i.test(x[1]+x[0])).slice(0,40)})"
    r = call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
    print(r["result"]["result"].get("value"))
finally:
    try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/close/{tab['id']}", timeout=10)
    except Exception as e: print("close err", e, file=sys.stderr)
    ws and ws.close()
