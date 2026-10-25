import worker from "/home/exedev/ErdosProblemADay-1813/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const S = "/day/160-shidong-itabe-upper-bounds-refereed";
const checks = [
  ["/", 200, "Erd"],
  ["/", 200, "160-shidong-itabe-upper-bounds-refereed"],
  [S, 200, "27<em>p</em>"],
  [S, 200, "Classical.choice, Quot.sound"],
  [S, 200, "4 ≤ <em>N</em> ≤ 12"],
  [S, 200, "2607.20752"],
  [S, 200, "v0.2.1-review-candidate"],
  ["/problem/160", 200, "160-shidong-itabe-upper-bounds-refereed"],
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
import { readFileSync } from "node:fs";
const src = readFileSync("/home/exedev/ErdosProblemADay-1813/src/index.js", "utf8");
const ph = (src.match(/⟨[A-Z_0-9]+⟩/g) || []);
if (ph.length) { console.log("BAD placeholders left: " + [...new Set(ph)].join(" ")); bad++; }
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS"); process.exit(bad ? 1 : 0);
