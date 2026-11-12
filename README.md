<p align="center">
  <a href="https://fusionproxy.net/?utm_source=github&utm_medium=playwright-proxy">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/FusionProxies/.github/main/assets/logo-on-dark.png">
      <img src="https://raw.githubusercontent.com/FusionProxies/.github/main/assets/logo-on-light.png" alt="Fusion Proxy" height="52">
    </picture>
  </a>
</p>

# Playwright with residential proxies

How to use [Fusion Proxy](https://fusionproxy.net/?utm_source=github&utm_medium=playwright-proxy) residential proxies in Playwright, in Python and Node.js: authenticated proxy, country targeting, and one sticky IP per browser context.

## Why one session per context

A page loads dozens of resources. On the rotating port every new connection can get a different IP, and many sites treat a page whose requests come from several IPs as suspicious. The examples give every browser context its own sticky session (`-sessid-` and `-sessTime-` in the username), so all pages in a context share one residential IP and a new context gets a new one.

## Setup

```bash
export FUSION_USER="your_username"
export FUSION_PASS="your_password"
export FUSION_COUNTRY="us"   # optional, two-letter country code
```

Your username and password are in the [dashboard](https://dashboard.fusionproxy.net/?utm_source=github&utm_medium=playwright-proxy).

### Python

```bash
cd python
pip install -r requirements.txt
playwright install chromium
python example.py
```

### Node.js

```bash
cd node
npm install
npx playwright install chromium
node example.mjs
```

Each script opens two contexts and prints the exit IP each one got.

## The proxy settings

```python
context = browser.new_context(proxy={
    "server": "http://resi.fusionproxy.net:12286",
    "username": f"{USER}-country-us-sessid-4821937-sessTime-600s",
    "password": PASS,
})
```

| Username part | Meaning |
|---|---|
| `-country-us` | Exit country (two-letter ISO code). Add `-state-` and `-city-` codes from the endpoint generator for narrower targeting |
| `-sessid-4821937` | Session ID. The same ID keeps the same IP; a new ID gets a new IP |
| `-sessTime-600s` | How long the session holds its IP, 1 to 120 minutes, in seconds |

All options are explained in the [endpoint generator guide](https://fusionproxy.net/guides/endpoint-generator?utm_source=github&utm_medium=playwright-proxy).

## Notes

- Use the HTTP endpoint (`resi.fusionproxy.net:12286`) in browsers. Chromium does not support SOCKS5 proxies with a username and password.
- The launch call sets a placeholder proxy (`http://per-context`). Some Chromium builds need a launch-level proxy before per-context proxies work; every context then sets its real proxy.
- A residential IP belongs to a real device and can change before the session ends if the device goes offline. Handle navigation errors with a retry in a new context.

## More

- [Code examples in 8 languages](https://github.com/FusionProxies/fusionproxy)
- [Puppeteer version](https://github.com/FusionProxies/puppeteer-proxy)
- [Residential proxies](https://fusionproxy.net/proxies/residential?utm_source=github&utm_medium=playwright-proxy) · [Pricing](https://fusionproxy.net/pricing?utm_source=github&utm_medium=playwright-proxy) · [Free trial](https://fusionproxy.net/free-trial?utm_source=github&utm_medium=playwright-proxy)

## License

MIT, see [LICENSE](LICENSE).
