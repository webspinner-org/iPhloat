"""Take screenshots of every iPhloat page (auth-gated) for self-review.

Mints a JWT against the live back-end's signing secret, opens each
page with the cookie, snaps the viewport at desktop and mobile
widths, and writes the images to scripts/snap-out/<page>-<width>.png.

Usage:
    .venv/bin/python scripts/snap.py

Required environment (the script reads these — never bakes them in):

    IPHLOAT_DEV_SSH_HOST       hostname of the development host where
                               the iPhloat back-end runs (e.g.
                               my-dev-mac.local)
    IPHLOAT_DEV_SSH_USER       SSH user on that host
    IPHLOAT_DEV_PLIST_PATH     absolute path to the LaunchAgent plist
                               that holds the back-end's environment
                               variables on the dev host
    IPHLOAT_DEV_PLIST_KEY      key under EnvironmentVariables inside
                               the plist that holds the JWT signing
                               secret (default: WS_TENANT_JWT_SECRET)
    IPHLOAT_DEV_PYTHON         absolute path to a Python3 interpreter
                               on the dev host that has plistlib
                               (default: /usr/bin/python3)
    IPHLOAT_DEV_USER_EMAIL     email address the minted JWT will
                               authenticate as

Nothing about the operator's machine, dev host, or paths is encoded
in this script. Everything that varies between operators is read
from the environment.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright


BASE = "https://iphloat.com"
PAGES = ["/", "/how-it-works", "/features", "/insurance", "/about"]
WIDTHS = [(1280, 900), (390, 844)]  # desktop + iPhone-ish

OUT = Path(__file__).parent / "snap-out"
OUT.mkdir(exist_ok=True)


def _require_env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise SystemExit(
            f"snap.py: required environment variable not set: {name}\n"
            f"  see this script's docstring for the full list."
        )
    return value


def get_jwt_secret() -> str:
    """Pull the live JWT signing secret from the dev host's plist."""
    ssh_host = _require_env("IPHLOAT_DEV_SSH_HOST")
    ssh_user = _require_env("IPHLOAT_DEV_SSH_USER")
    plist_path = _require_env("IPHLOAT_DEV_PLIST_PATH")
    plist_key = _require_env("IPHLOAT_DEV_PLIST_KEY", "WS_TENANT_JWT_SECRET")
    python = _require_env("IPHLOAT_DEV_PYTHON", "/usr/bin/python3")

    py_oneliner = (
        "import plistlib;"
        f"p=plistlib.load(open({plist_path!r},'rb'));"
        f"print(p['EnvironmentVariables'][{plist_key!r}])"
    )
    cmd = f"{python} -c {py_oneliner!r}"
    r = subprocess.run(
        ["ssh", f"{ssh_user}@{ssh_host}", cmd],
        capture_output=True, text=True, timeout=15,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ssh failed: {r.stderr}")
    return r.stdout.strip()


def mint_jwt(secret: str, email: str | None = None, ttl: int = 3600) -> str:
    if email is None:
        email = _require_env("IPHLOAT_DEV_USER_EMAIL")

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
    """Get a CDN proxy IP for iphloat.com (avoids local DNS cache)."""
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
    print(f"using proxy IP {proxy_ip}; JWT ok ({len(jwt)} chars)")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for w, h in WIDTHS:
            ctx = await browser.new_context(viewport={"width": w, "height": h})
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
