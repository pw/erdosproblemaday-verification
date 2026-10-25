import worker from "/home/exedev/ErdosProblemADay-main/src/index.js";
const stmt = { bind() { return stmt; }, all: async () => ({ results: [] }), first: async () => null, run: async () => ({ success: true }) };
const env = { DB: { prepare: () => stmt }, RESEND_API_KEY: "" };
const r = await worker.fetch(new Request("https://erdosproblemaday.com/day/802-openai-aeks-independence-refereed"), env, {waitUntil(){},passThroughOnException(){}});
let t = await r.text();
t = t.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g,'').replace(/<\/(p|pre|li|h\d|div)>/g,'\n\n').replace(/<br\s*\/?>/g,'\n').replace(/<[^>]+>/g,'').replace(/&gt;/g,'>').replace(/&lt;/g,'<').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/[ \t]+/g,' ').replace(/\n\s*\n\s*\n+/g,'\n\n');
console.log(t);
