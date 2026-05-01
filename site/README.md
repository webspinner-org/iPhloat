# site/ — the portable iPhloat front-end

Static HTML/CSS/JS for `iphloat.com`. Portable: a site owner can extract this directory and host it on any static file server. No proprietary intelligent agents inside.

## Current state

Skeleton placeholder while the One Sentence Website build agent prepares the real site from the offerings in [`../inputs/`](../inputs/). The skeleton establishes:

- A two-theme CSS variable surface (`light` / `dark`, switchable via `<html data-theme>`).
- A baseline HTML5 document the back-end mounts as the public root.

## Served by

The Webspinner-core back-end at `~/webspinner-work/kepler/iphloat/` mounts this directory as static files at the root path. Locally during development, that back-end runs on `127.0.0.1:11800`. In production, the Cloudflare Tunnel routes `iphloat.com` to that loopback port on Kepler.

## What lives here later

When the build agent runs, it will refine and extend this directory with:

- A real index page composed from the prose + imagery the author drops in `../inputs/`.
- Light/dark palettes derived from the imagery (the imagery-drives-CSS UX invariant).
- The two-panel chat + Cognitive Content layout.
- Static assets (icons, logos, optimized imagery).

Until then this remains a deliberate placeholder.
