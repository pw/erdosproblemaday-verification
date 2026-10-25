import worker from "/home/exedev/ErdosProblemADay-1014-1200/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const S = "/day/341-queneau-variant-not-periodic-either";
const checks = [
  ["/", 200, "341-queneau-variant-not-periodic-either"],
  ["/", 200, "QUENEAU"],
  [S, 200, "77 replaced by 56"],
  [S, 200, "<em>Y</em><sub>0</sub> ⊕ <em>Y</em><sub>0</sub>"],
  [S, 200, "1,224,510"],
  [S, 200, "period 117"],
  [S, 200, "Lemma 3 (the gates)"],
  [S, 200, "verification/341/queneau-variant-56-for-77"],
  ["/problem/341", 200, "341-queneau-variant-not-periodic-either"],
  ["/day/341-li-disproof-refereed", 200, "Follow-up, 14 October"],
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
const src = readFileSync("/home/exedev/ErdosProblemADay-1014-1200/src/index.js", "utf8");
const ph = (src.match(/⟨[A-Z_0-9]+⟩|REFEREE_SENTENCE|GREEDY_SENTENCE/g) || []);
if (ph.length) { console.log("BAD placeholders left: " + [...new Set(ph)].join(" ")); bad++; }
console.log(bad ? `SMOKE FAIL (${bad})` : "SMOKE PASS"); process.exit(bad ? 1 : 0);
