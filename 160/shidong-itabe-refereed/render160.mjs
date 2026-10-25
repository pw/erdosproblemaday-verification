import worker from "/home/exedev/ErdosProblemADay-1813/src/index.js";
import { writeFileSync } from "node:fs";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" }; const ctx = { waitUntil() {}, passThroughOnException() {} };
for (const p of ["/day/160-shidong-itabe-upper-bounds-refereed", "/", "/problem/160"]) {
  const res = await worker.fetch(new Request("https://erdosproblemaday.com" + p), env, ctx);
  const name = p === "/" ? "render_home.html" : "render" + p.replace(/\//g, "_") + ".html";
  writeFileSync("/tmp/erdos160/entry/" + name, await res.text());
  console.log(p, res.status);
}
// plain-text version of the entry for the blind reader
import { readFileSync } from "node:fs";
const h = readFileSync("/tmp/erdos160/entry/render_day_160-shidong-itabe-upper-bounds-refereed.html", "utf8");
const t = h.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "").replace(/<\/p>/g, "\n\n").replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/\n{3,}/g, "\n\n");
writeFileSync("/tmp/erdos160/entry/render_160.txt", t); console.log("txt", t.length);
