# iPhloat backlog

Living list of iPhloat work items. Closed items kept with a **DONE**
marker + the tag they shipped under so the history is walkable from
this file alone.

## Status

Pre-boot. Repo seeded with patron-facing `README.md` + Claude boot
files. **No application code yet.** The next Claude Code session
will pick up the Wizard's build brief and turn it into a deployable
Kepler tenant.

## Queued — Wizard owes a call before code lands

These are the open architectural calls listed in `INTENT.md` that
need to be settled before serious implementation. Pulling them up
here so the next session sees them at a glance:

- **v1 surface scope.** Marketing site only? Marketing + Q&A RAG?
  Marketing + cart + Stripe checkout? The README implies all of the
  above; the launch ordering is the Wizard's call.
- **Frontend shape.** Server-rendered HTML (sovereign-ai's pattern,
  ~5000 lines of `index.html`)? Static-bound webbook template
  (Cinzel/Cormorant candlelight)? Hybrid? Likely hybrid, but the
  call should be explicit.
- **Catalog schema.** iPhone 14 / 15 / 16 / 17 × Pro / Pro Max ×
  colorways. Storage shape (sqlite + structured JSON, dedicated
  table per dimension, etc.) deferred to the build conversation.
- **Payment processor choice.** Stripe is the obvious starting
  point but is intertwined with the Webspinner Spool pre-design
  conversation (see `~/webspinner-sovereign-ai/BACKLOG.md` →
  "Webspinner Spool"). iPhloat is B2C consumer commerce — its
  needs may diverge from the Spool's prepaid-wallet model.
- **Long-term repo location.** `~/iPhloat/` (top-level, like
  `~/webspinner-sovereign-ai/`) or `~/webspinner-work/kepler/iphloat/`
  (alongside other tenants)? Sovereign-ai went top-level. Same
  pattern likely. Confirm with the Wizard.

## Queued — first session after the build brief

The minimum viable iPhloat tenant on Kepler:

- **Scaffold the FastAPI tenant** mirroring
  `~/webspinner-work/kepler/legal/` — `app/`, `requirements.txt`,
  `tests/`, `deploy/`. Pick a free loopback port (the existing
  catalog is in `~/webspinner-sovereign-ai/service/tests/test_main.py`
  '_pick_free_port' helper if you need it).
- **Wire the Cloudflare Tunnel route** for `iphloat.com` →
  `http://127.0.0.1:<port>` in the cloudflared config on Kepler.
- **First plist + installer** — `com.webspinner.iphloat` launchd
  agent, modeled on `com.webspinner.sovereign.plist`. Install
  script reads `WEBSPINNER_LIVE_JWT_SECRET` (or whatever auth shape
  iPhloat needs — may not need it for unauthenticated marketing
  pages).
- **First green test suite.** Even a single "GET / returns 200"
  pytest establishes the bar.

## Queued — patron-visible features

To be sequenced once the build brief lands:

- Marketing landing page — Cinzel/Cormorant candlelight or a
  product-photography-led layout? Wizard call.
- Product photography + 3D viewer (the README mentions "crystal-
  clear back panel preserves the iPhone's design" — the visual
  becomes load-bearing for trust).
- Catalog browse → variant select → cart.
- Checkout (deferred until processor decision).
- Account / order tracking (`iphloat.com/account`,
  `iphloat.com/order`).
- Support form (`iphloat.com/support`) backed by Webspinner RAG
  over product corpus.
- Press inquiry form (`iphloat.com/press`).

## Queued — ecosystem hygiene

- **Multi-tenant deploy template.** iPhloat is tenant #1 of 100+.
  Once iPhloat is live and stable, *immediately* extract the deploy
  shape into a cookiecutter or scripted scaffold so tenant #2
  takes hours, not days. Hold off until iPhloat is real — premature
  extraction would template the wrong thing (drift discipline > DRY).
- **Apps-tier migration plan.** Today's shape (CF Tunnel → Kepler)
  is the stepping stone. The destination per
  `~/webspinner-work/ROADMAP.md` is a five-tier shape (presentation
  server in front, storage box behind). When iPhloat moves, what
  has to move with it (DB? assets? plist?). Capture the boundary.

## Recently shipped

- **DONE** `repo-seed` (2026-04-30) — `README.md` (patron-facing)
  + `CLAUDE.md` (Claude boot reading) + `INTENT.md` (Wizard's
  brief at scaffolding time) + `BACKLOG.md` (this file) +
  `.gitignore`. Git initialized; ready for the first build session.
