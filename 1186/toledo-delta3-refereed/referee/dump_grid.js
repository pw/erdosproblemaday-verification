// dump verify.js's per-grid constants for comparison
const V = require('/home/exedev/MathDyad/erdos1186/repo/instruments/delta3/verify.js');
const Q = require('/home/exedev/MathDyad/erdos1186/repo/instruments/interval/rational.js');
const fs = require('fs');
const out = {};
for (const f of process.argv.slice(2)) {
  const cert = JSON.parse(fs.readFileSync(f));
  const gd = V.gridData(cert.grid);
  out[f] = {
    grid: cert.grid,
    cells: gd.cells.map(c => ({ p: c.p, q: c.q, s: c.s, a: Q.toString(c.a), b: Q.toString(c.b), flat: c.flat })),
    full: gd.full.map(x => [x.i, x.j]),
    cut: gd.cut.map(x => [x.i, x.j, Q.toString(x.Ain), Q.toString(x.Aout)]),
    absent: gd.absent,
  };
}
fs.writeFileSync('/home/exedev/MathDyad/erdos1186/referee/verify_grids.json', JSON.stringify(out));
console.log('ok', Object.keys(out).length);
