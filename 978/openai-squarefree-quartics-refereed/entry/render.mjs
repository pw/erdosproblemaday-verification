import worker from "/home/exedev/ErdosProblemADay-1022-1200/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" }; const ctx = { waitUntil() {}, passThroughOnException() {} };
const r = await worker.fetch(new Request("https://erdosproblemaday.com/day/978-openai-squarefree-quartics-refereed"), env, ctx);
let h = await r.text();
h = h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, "").replace(/<\/(p|li|h\d|div|ul|pre)>/g, "\n").replace(/<br\s*\/?>/g, "\n").replace(/<a [^>]*href="([^"]*)"[^>]*>/g, "[$1] ").replace(/<[^>]+>/g, "");
h = h.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/\n\s*\n+/g, "\n\n");
console.log(h);
