// rebuild the inner P exactly as verify.js does (using its exported pieces), report provePSD details, dump P
const V = require('/home/exedev/MathDyad/erdos1186/repo/instruments/delta3/verify.js');
const Q = require('/home/exedev/MathDyad/erdos1186/repo/instruments/interval/rational.js');
const { provePSD } = require('/home/exedev/MathDyad/erdos1186/repo/instruments/delta3/psd.js');
const fs = require('fs');
const cert = JSON.parse(fs.readFileSync('/home/exedev/MathDyad/erdos1186/repo/certs/delta3/inner-r20-g24_4_8.json'));
const gd = V.gridData(cert.grid); const n = gd.n;
const r = (a, b) => Q.R(BigInt(a), BigInt(b === undefined ? 1 : b));
const rat = s => { const [a, b] = s.split('/'); return Q.R(BigInt(a), BigInt(b || 1)); };
const ONE = r(1), ZERO = r(0);
const Y = i => ({ k: ZERO, y: [[i, ONE]], m: ZERO }), O = i => ({ k: ONE, y: [[i, r(-1)]], m: ZERO });
const rin = rat(cert.rin);
const MR = { k: rin, y: [], m: r(-1) }, M0 = { k: ZERO, y: [], m: ONE };
const p = new V.Poly(gd.w);
V.addL(p, gd, 'inner');
for (const [key, v] of Object.entries(cert.lam)) { const [i, j] = key.split(',').map(Number); p.addProduct(Q.neg(rat(v)), Y(i), O(j)); }
cert.nu.forEach((v, j) => p.addProduct(Q.neg(rat(v)), Y(j), MR));
p.addProduct(Q.neg(rat(cert.kap)), M0, MR);
for (const [key, v] of Object.entries(cert.N)) { const [i, j] = key.split(',').map(Number); p.addProduct(Q.neg(Q.mul(rat(v), r(i === j ? 1 : 2))), Y(i), Y(j)); }
cert.c.forEach((v, i) => p.addProduct(Q.neg(rat(v)), Y(i)));
p.finish();
console.log('const', Q.toString(p.k), 'nonzero linear', p.g.filter(v => Q.sign(v)).length);
const P = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => p.quad(i, j)));
const res = provePSD(P);
console.log(JSON.stringify({ verdict: res.verdict, method: res.method, tauExp: res.tauExp, minMargin: res.minMargin ? Q.toDouble(res.minMargin) : null, minMarginSign: res.minMargin ? Q.sign(res.minMargin) : null, dropped: res.dropped }));
fs.writeFileSync('/home/exedev/MathDyad/erdos1186/referee/inner_P.json', JSON.stringify(P.map(row => row.map(Q.toString))));
// multiplier stats
const lamv = Object.values(cert.lam).map(rat); const Nv = Object.values(cert.N).map(rat);
console.log('lam count', lamv.length, 'N count', Nv.length, 'kap', cert.kap, 'nu nonzero', cert.nu.filter(x => x !== '0').length, 'c nonzero', cert.c.filter(x => x !== '0').length);
