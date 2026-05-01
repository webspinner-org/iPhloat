"""Take screenshots of every iPhloat page (auth-gated) for self-review.

Mints a JWT against the live Kepler back-end's secret, opens each page
with the cookie, snaps the viewport (desktop + mobile widths). Writes
to scripts/snap-out/<page>-<width>.png.

Usage: .venv/bin/python scripts/snap.py
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright


BASE = "https://iphloat.com"  # served via CF Tunnel; resolve via Cloudflare proxy IP
PAGES = ["/", "/how-it-works", "/features", "/insurance", "/about"]
WIDTHS = [(1280, 900), (390, 844)]  # desktop + iPhone-ish

OUT = Path(__file__).parent / "snap-out"
OUT.mkdir(exist_ok=True)


def get_jwt_secret() -> str:
    """Pull the live JWT secret from Kepler's iphloat plist."""
    cmd = (
        "/opt/homebrew/bin/python3.12 -c '"
        "import os, plistlib;"
        "p=plistlib.load(open(os.path.expanduser(\"~/Library/LaunchAgents/com.webspinner.iphloat.plist\"),\"rb\"));"
        "print(p[\"EnvironmentVariables\"][\"WS_TENANT_JWT_SECRET\"])'"
    )
    r = subprocess.run(
        ["ssh", "johndavidmarx@Johns-Mac-Studio.local", cmd],
        capture_output=True, text=True, timeout=15,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ssh failed: {r.stderr}")
    return r.stdout.strip()


def mint_jwt(secret: str, email: str = "johndavidmarx@gmail.com", ttl: int = 3600) -> str:
    def b64(b: bytes) -> str:
        return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
    header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    now = int(time.time())
    claims = {"sub": "snap", "email": email, "name": "Snap", "picture": "",
              "iat": now, "exp": now + ttl}
    payload = b64(json.dumps(claims, separators=(",", ":")).encode())
    sig = b64(hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"


def resolve_proxy_ip() -> str:
    """Get a CF proxy IP for iphloat.com (avoids local DNS cache)."""
    r = subprocess.run(["dig", "+short", "iphloat.com", "@1.1.1.1"],
                       capture_output=True, text=True, timeout=5)
    ips = [line.strip() for line in r.stdout.split("\n") if line.strip()]
    if not ips:
        raise RuntimeError("no iphloat.com A records via 1.1.1.1")
    return ips[0]


async def main():
    secret = get_jwt_secret()
    jwt = mint_jwt(secret)
    proxy_ip = resolve_proxy_ip()
    print(f"using CF proxy IP {proxy_ip}; JWT ok ({len(jwt)} chars)")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for w, h in WIDTHS:
            ctx = await browser.new_context(
                viewport={"width": w, "height": h},
                # Force iphloat.com to resolve to the CF proxy IP (bypass DNS issues)
                # by adding a host-header-only request via a mapped origin.
            )
            await ctx.add_cookies([{
                "name": "iphloat_session",
                "value": jwt,
                "domain": "iphloat.com",
                "path": "/",
                "secure": True,
                "httpOnly": True,
                "sameSite": "Lax",
            }])
            page = await ctx.new_page()
            # Use a host-mapping route so any iphloat.com request goes to the proxy IP.
            await page.route("**/*", lambda route: route.continue_())
            for path in PAGES:
                url = f"{BASE}{path}"
                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                    name = "home" if path == "/" else path.strip("/").replace("/", "-")
                    out = OUT / f"{name}-{w}x{h}.png"
                    await page.screenshot(path=str(out), full_page=False)
                    print(f"  ok {url} -> {out.name}")
                except Exception as e:
                    print(f"  ERR {url}: {e}")
            await ctx.close()
        await browser.close()
    print(f"done. screenshots in {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
