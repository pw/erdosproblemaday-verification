import worker from "/home/exedev/ErdosProblemADay-1014-0300/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "120-openai-geometric-similarity-refereed";
const checks = [
  ["/", 200, "Erd"],
  ["/", 200, "KERNEL REPLAY GREEN"],
  [`/day/${slug}`, 200, "Green's Problem 94"],
  [`/day/${slug}`, 200, "statement_match.txt"],
  [`/day/${slug}`, 200, "HOLDS AS READ"],
  [`/day/${slug}`, 200, "openai-referee"],
  ["/problem/120", 200, "120"],
  ["/day/188-cmxz-6330-refereed-and-finite-certificates", 200, "6330"],
  ["/progress", 200, ""],
  ["/board", 200, "open"],
  ["/day/no-such-slug-xyz", 404, ""],
];
let bad = 0;
for (const [path, want, needle] of checks) {
  try {
    const res = await worker.fetch(new Request("https://erdosproblemaday.com" + path), env, ctx);
    const body = await res.text();
    const ok = res.status === want && (needle === "" || body.includes(needle));
    console.log(`${ok ? "ok " : "BAD"} ${res.status} ${path} ${body.length}B${needle ? ` needle=${body.includes(needle)}` : ""}`);
    if (!ok) bad++;
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
