import worker from "/home/exedev/ErdosProblemADay-1015-0000/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const S = "/day/341-the-last-seed-in-12-through-1e8";
const checks = [
  ["/", 200, "341-the-last-seed-in-12-through-1e8"],
  ["/", 200, "THE LAST SEED IN [12]"],
  [S, 200, "{1, 4, 8, 10, 11, 12}"],
  [S, 200, "3a045efe"],
  [S, 200, "27,875"],
  [S, 200, "UNSAT"],
  [S, 200, "verification/341/seed-e-through-1e8"],
  ["/problem/341", 200, "341-the-last-seed-in-12-through-1e8"],
  ["/day/341-li-disproof-refereed", 200, "Follow-up, 15 October"],
  ["/day/341-queneau-variant-not-periodic-either", 200, "Follow-up, 15 October"],
  ["/report/341", 200, "4094"],
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
const src = readFileSync("/home/exedev/ErdosProblemADay-1015-0000/src/index.js", "utf8");
const ph = (src.match(/⟨[A-Z_0-9]+⟩/g) || []);
if (ph.length) { console.log("BAD placeholders left: " + [...new Set(ph)].join(" ")); bad++; }
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS"); process.exit(bad ? 1 : 0);
