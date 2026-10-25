import fs from 'fs';
const src=fs.readFileSync(process.argv[2],'utf8');
let obj;
try { obj = (new Function('return ('+src.trim().replace(/,\s*$/,'')+')'))(); } catch(e){ console.log("PARSE FAIL",e.message); process.exit(1); }
console.log("parsed OK; keys:",Object.keys(obj).join(","));
const b=obj.body;
console.log("body length",b.length,"backticks in body:",(b.match(/`/g)||[]).length,"'${' in body:",b.includes('${'));
// tag balance
const tags=[...b.matchAll(/<\/?([a-zA-Z0-9]+)[^>]*>/g)];
const stack=[];const errs=[];
for(const m of tags){const t=m[1].toLowerCase(); if(['br','hr','img'].includes(t)) continue;
 if(m[0].startsWith('</')){ if(stack.length&&stack[stack.length-1]===t) stack.pop(); else errs.push(`unexpected </${t}> at ${m.index} (open: ${stack.slice(-3)})`);} else stack.push(t);}
console.log("tag errors:",errs.length,errs.slice(0,5),"unclosed:",stack);
const counts={};for(const m of tags){const k=m[0].startsWith('</')?'/'+m[1]:m[1];counts[k]=(counts[k]||0)+1}
console.log(counts);
for (const f of ['title','summary']) { console.log(f,"len",obj[f].length, "smart quotes:", /[‘’“”]/.test(obj[f])); }
console.log("body smart quotes:",(b.match(/[‘’“”]/g)||[]).length, "straight dq in body:", (b.match(/"/g)||[]).length);
console.log("stray < or & :", [...b.matchAll(/&(?![a-zA-Z#0-9]+;)/g)].length, [...b.matchAll(/<(?![a-zA-Z\/!])/g)].map(m=>b.slice(m.index-30,m.index+30)));
for(const l of obj.links){ try{ new URL(l.url); console.log("URL ok",l.url);}catch(e){console.log("BAD URL",l.url)} }
console.log("title has html:", /<[a-z]/.test(obj.title));
