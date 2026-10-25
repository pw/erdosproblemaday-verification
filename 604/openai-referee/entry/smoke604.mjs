import worker from "/home/exedev/ErdosProblemADay-1014-1500/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const slug = "604-openai-weak-pinned-distances-refereed";
const checks = [
  ["/", 200, "Erd"],
  ["/", 200, "604"],
  [`/day/${slug}`, 200, "Katz"],
  [`/day/${slug}`, 200, "exists_pin_eventually"],
  [`/day/${slug}`, 200, "openai-referee"],
  ["/problem/604", 200, "604"],
  ["/problem/604", 200, "weak pinned"],
  ["/day/90-openai-unit-distance-power-saving-refereed", 200, "leanchecker"],
  ["/day/1083-openai-distinct-distances-refereed", 200, "7,919"],
  ["/day/181-openai-hypercube-ramsey-refereed", 200, "7,773"],
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
    if (path.startsWith("/day/604") && res.status === 200) {
      for (const ph of ["{{","[[","REPLACE_ME","TODO","still running"]) {
        if (body.includes(ph)) { console.log(`BAD placeholder leaked: ${ph}`); bad++; }
      }
    }
  } catch (e) { console.log(`BAD throw ${path}: ${e.message}`); bad++; }
}
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS");
process.exit(bad ? 1 : 0);
