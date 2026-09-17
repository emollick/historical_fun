// Render the SVG figures to PNG at 2x with Chromium (Playwright). Run from the case folder: node code/render_figures.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const b = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}).catch(async () => chromium.launch());
  for (const name of ['fig1_leave_one_out', 'fig2_sensitivity']) {
    const svg = fs.readFileSync(path.join('figures', name + '.svg'), 'utf8');
    const p = await b.newPage({ viewport: { width: 800, height: 900 }, deviceScaleFactor: 2 });
    await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#f8f9f7"><div id="f" style="display:inline-block;padding:14px;background:#f8f9f7">' + svg + '</div></body></html>', { waitUntil: 'load' });
    await p.locator('#f').screenshot({ path: path.join('figures', name + '.png') });
    await p.close();
  }
  await b.close();
  console.log('png written');
})().catch(e => { console.error(e); process.exit(1); });
