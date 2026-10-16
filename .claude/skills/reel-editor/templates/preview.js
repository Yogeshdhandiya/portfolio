// Quick overlay check without a full render: node preview.js page.html out.png t1 t2 ... (tiles frames over grey)
const { chromium } = require('/opt/node-tools/node_modules/playwright-core');
const path = require('path');
(async () => {
  const [page_, out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' in process.env ? undefined : undefined });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(page_)); await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: 'body{background:#5a6270 !important}' });
  const shots = [];
  for (const t of ts) { await p.evaluate(t => window.__seek(t), +t); await p.waitForTimeout(60); shots.push(await p.screenshot({ type: 'png' })); }
  await b.close();
  const fs = require('fs'); shots.forEach((s, i) => fs.writeFileSync(out.replace('.png', `_${i}.png`), s));
})();
