import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const ctx = { waitUntil() {}, passThroughOnException() {} };
const res = await worker.fetch(new Request("https://erdosproblemaday.com/day/341-li-disproof-refereed"), env, ctx);
let b = await res.text();
b = b.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "").replace(/<br\s*\/?>/g, "\n").replace(/<\/p>/g, "\n\n").replace(/<[^>]+>/g, "");
b = b.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/[ \t]+/g, " ").replace(/\n{3,}/g, "\n\n");
console.log(res.status); process.stdout.write(b);
