// Playwright (Node.js) with Fusion Proxy residential proxies.
// Each browser context gets its own sticky session: one IP per context.
//
// npm install && npx playwright install chromium
// export FUSION_USER=... FUSION_PASS=... [FUSION_COUNTRY=us]
import { chromium } from 'playwright';

const { FUSION_USER, FUSION_PASS, FUSION_COUNTRY = 'us' } = process.env;
if (!FUSION_USER || !FUSION_PASS) throw new Error('set FUSION_USER and FUSION_PASS');

const stickyProxy = (minutes = 10) => ({
  server: 'http://resi.fusionproxy.net:12286',
  username: `${FUSION_USER}-country-${FUSION_COUNTRY}-sessid-${Math.floor(Math.random() * 9e6) + 1e6}-sessTime-${minutes * 60}s`,
  password: FUSION_PASS,
});

// contexts set their own proxy; the launch value is only a placeholder
const browser = await chromium.launch({ proxy: { server: 'http://per-context' } });

for (const n of [1, 2]) {
  const context = await browser.newContext({ proxy: stickyProxy() });
  const page = await context.newPage();
  await page.goto('https://ipinfo.io/json', { timeout: 60000 });
  console.log(`context ${n}:`, (await page.locator('body').innerText()).replace(/\n/g, ' ').slice(0, 120));
  await context.close();
}

await browser.close();
