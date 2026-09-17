const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const FIG = path.join(__dirname, '..', 'figures');
(async () => {
  const browser = await chromium.launch();
  for (const name of ['fig1_night_by_source','fig2_shares_by_prior']) {
    const svg = fs.readFileSync(path.join(FIG, `${name}.svg`),'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const w = +m[1], h = +m[2];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.screenshot({ path: path.join(FIG, `${name}.png`), clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
    console.log('rendered', name, w, h);
  }
  await browser.close();
})();
