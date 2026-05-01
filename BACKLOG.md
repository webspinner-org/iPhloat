# iPhloat backlog

Living list of iPhloat work items. Closed items kept with a **DONE**
marker + the tag they shipped under so the history is walkable from
this file alone.

## Status

Pre-boot, design phase. Repo seeded with patron-facing `README.md`,
`AI-NATIVE.md`, `HOW-WEBSPINNER-WORKS.md`, and Claude boot files
(`CLAUDE.md`, `INTENT.md`, `BACKLOG.md`). **No application code
yet.** The Wizard releases the build phase explicitly.

The architectural shape is set (see `INTENT.md` → *Additional
intent — 2026-04-30 build phase brief*): front-end portable in
this repo, back-end (proprietary agents, Spinners, multi-tenant
services) in `~/webspinner-work/`, called over the Cloudflare
Tunnel. Multi-tenant via runtime parameters, no hard-coding.

## Queued — open architectural calls

Most prior open calls have been resolved by the 2026-04-30 build
phase brief. The ones still outstanding:

- **Catalog schema (iPhloat product catalog).** iPhone 14 / 15 /
  16 / 17 × Pro / Pro Max × colorways. Storage shape deferred to
  build conversation. Distinct from the *Webspinner Studio site
  catalog* (next item).
- **Webspinner Studio site catalog shape.** All Studio-built sites
  enter a catalog that `webspinner.live` features and launches.
  Where does this catalog live (DB? service?), what does a row
  look like, what's the registration API? Multi-tenant from the
  first call. Likely lives in `~/webspinner-work/`.
- **Payment processor choice.** Stripe is the obvious starting
  point but intertwined with the Webspinner Spool pre-design
  conversation (`~/webspinner-sovereign-ai/BACKLOG.md` →
  "Webspinner Spool"). iPhloat is B2C consumer commerce; needs
  may diverge from Spool's prepaid-wallet model. Deferred until
  checkout work begins.
- **Long-term repo location.** `~/iPhloat/` (top-level, like
  `~/webspinner-sovereign-ai/`) or `~/webspinner-work/kepler/iphloat/`
  (alongside other tenants)? Sovereign-ai is top-level; same
  pattern likely.
- **Loom for chat at launch.** Open Loom (corpus-grounded today)
  vs. context-stuffed Quiet Loom (Webspinner-internal, but tool-
  use protocol gap to close). Either is fine; pick when build
  phase opens.

## Queued — first sprint after the build brief opens

The architectural keystone: **stand up the front-end / back-end
boundary cleanly, with one end-to-end thread working.**

### Back-end work (in `~/webspinner-work/`)

- **iPhloat tenant service.** New module under `~/webspinner-work/`
  (location TBD: `kepler/iphloat/` mirroring `kepler/legal/`, or
  a generic `kepler/tenant/` that takes tenant identity as a
  runtime parameter — the latter is the multi-tenant-from-day-one
  shape and probably correct). FastAPI on a loopback port,
  plist-managed. Loom-agnostic via the existing `LLMClient`
  Protocol abstraction (analyzer / sovereign-ai pattern).
- **One Sentence Website agent.** New back-end agent that takes
  *(imagery, prose, intent)* → trained tenant. Prototyped here
  for iPhloat; lives in `~/webspinner-work/`. Honors AI Native
  SDLC + Agile principles (sophisticated loom, current-knowledge
  citations, one-recommendation-no-questions, retrospective-driven,
  live progress, no silent waits, imagery-derived CSS).
- **Webspinner Studio site-catalog registration.** Whatever
  back-end registers a site in the catalog `webspinner.live`
  features. Multi-tenant from the first call.
- **Tunnel routing for `iphloat.com`.** Add the route in the
  cloudflared config (path is `~/webspinner-work/kepler/cloudflare/`,
  not `cloudflared/` as CLAUDE.md says — minor doc drift to fix).
  CF zone is registered; needs DNS + tunnel hostname binding.
- **Vault entries.** Identify / provision the secrets the iPhloat
  back-end will need (CF token, JWT secret if patron auth lands,
  any provider key if Open Loom is used). See *Tokens & credentials
  inventory* below.
- **Blast-radius guard.** Every back-end change is additive. New
  module, feature flag, tests, no disturbance of analyzer /
  sovereign / legal / weaver / weaver-memory / mlx-server-weaver /
  cognitive-store / cognitive-cdn / image-engine.

### Front-end work (in `~/iPhloat/`)

- **Portable scaffold.** Static-or-near-static front-end with no
  proprietary agents inside it. Calls back-end services via the
  tunnel. Two-panel layout (chat + Cognitive Content panel) per
  the UX invariants.
- **Light + dark CSS, real-time switchable.** Reference the
  Sovereign AI app's runtime theme switch.
- **Imagery → CSS extraction consumed.** Whatever the back-end
  build agent produces (palette, type pairings) is rendered here.
- **Test bar.** Mirror the ratio of the
  `~/webspinner-sovereign-ai/service/tests/` standard. Even the
  first "GET / returns 200" thread establishes the bar.
- **Feature flags from day one.** Every patron-facing surface
  ships behind a flag. Flag flips only after end-to-end tests
  pass.

## Queued — patron-visible features

Sequenced after the front-end / back-end boundary is standing:

- Marketing landing page (Cinzel/Cormorant candlelight or
  product-photography-led layout — Wizard call when relevant).
- Product photography + 3D viewer (the README mentions "crystal-
  clear back panel preserves the iPhone's design" — the visual
  becomes load-bearing for trust).
- Chat panel + Cognitive Content panel (the Webspinner UX
  invariants in patron-facing form).
- Catalog browse → variant select → cart.
- Checkout (deferred until processor decision).
- Account / order tracking (`iphloat.com/account`,
  `iphloat.com/order`).
- Support form (`iphloat.com/support`) backed by Webspinner RAG
  over product corpus.
- Press inquiry form (`iphloat.com/press`).

## Queued — ecosystem hygiene

- **Multi-tenant deploy template.** iPhloat is tenant #1 of 100+.
  Once iPhloat is live and stable, extract the deploy shape into
  a scripted scaffold so tenant #2 takes hours, not days. Hold
  off until iPhloat is real — premature extraction would template
  the wrong thing (drift discipline > DRY).
- **Apps-tier migration plan.** Today's shape (CF Tunnel → Kepler)
  is the stepping stone. The destination per
  `~/webspinner-work/ROADMAP.md` is a five-tier shape (presentation
  server in front, storage box behind). When iPhloat moves, what
  has to move with it (DB? assets? plist?). Capture the boundary.
- **README.md scrub.** The current `README.md` describes a
  `/spinners` directory ("Custom Spinners for product Q&A and
  order lookup"). That conflicts with the new boundary — Spinners
  live in `~/webspinner-work/`, not in this repo. Update the
  *What's in this repo* table when the front-end shape is concrete.
- **CLAUDE.md scrub.** "Cloudflare Tunnel config" path is listed
  as `~/webspinner-work/kepler/cloudflared/` but the actual path
  is `~/webspinner-work/kepler/cloudflare/`. Small drift, easy fix.

## Tokens & credentials inventory

Verified 2026-04-30:

- **`wsvault` binary** present at
  `~/webspinner-work/kepler/vault/target/release/wsvault`. Vault
  endpoint: `https://vault.webspinner.work` (CF Access fronted).
  Commands: `health`, `get`, `put`, `versions`, `list`, `delete`,
  `acl`.
- **CF Access auth status:** the cached token for
  `vault.webspinner.work` has expired or is missing (`wsvault
  health` returned *"Unable to find token for provided application.
  Please run login command to generate token."*). The Wizard runs
  `cloudflared access login https://vault.webspinner.work`
  interactively to refresh. Must be done before back-end work
  starts.
- **`cloudflared` binary** at `/opt/homebrew/bin/cloudflared`.
- **`~/.cloudflared/`** has a credentials JSON, `cert.pem`, an
  `expired-token` artifact, and the org token. Tunnel auth is
  partly seeded; vault-specific Access token needs refresh.

Tokens iPhloat back-end will likely need (provision before code):

- `webspinner-cf-token` — CF API token for managing the
  `iphloat.com` zone (DNS records, tunnel hostname binding).
  Likely already in vault.
- A JWT secret for iPhloat patron auth (if/when account / order
  tracking lands). Naming convention: `iphloat-jwt-secret` or
  similar. **Not yet needed.**
- Provider key for Open Loom (if Open Loom serves chat at
  launch). Likely already in vault under a generic name. **Decide
  with loom selection.**
- Stripe API key (if/when checkout lands). **Not yet needed.**
- Service-caller credentials for any back-end service iPhloat
  calls (`WSVAULT_SERVICE_CLIENT_ID` / `_SECRET` per launchd
  plist convention).

## Recently shipped

- **DONE** `session-journal-2026-04-30` (2026-04-30) — comprehensive
  session journal at `~/iPhloat/SESSION-JOURNAL-2026-04-30.md`
  covering the entire build phase: architecture (Kepler-direct,
  front-end/back-end boundary, multi-tenant via env), the 15-agent
  fleet (8 build-time + Hagrid + Auditor + Pipeline + Weaver
  implemented; Cognitive Composer / Dragon Tamer / Catalog
  Registrar / Retrospective pending), The Weaver pipeline
  (KeplerEmbedder → SQLite WRAG cosine → KeplerLoomClient → cited
  brief response), LLM choice (`mlx-community/Qwen2.5-7B-Instruct-4bit`
  via Kepler mlx-server at `127.0.0.1:11445`), embeddings choice
  (`sentence-transformers/all-MiniLM-L6-v2` via Kepler embeddings
  sidecar at `127.0.0.1:11446`, 384-dim), agent-loom service for
  Studio integration (`https://agent-loom.webspinner.work`), auth
  pattern (Google ID token → HMAC JWT cookie + allowlist), cache
  discipline (HTML no-cache + content-hash versioned assets +
  immutable Cache-Control), CF credentials lookup pattern (cached
  in past Claude project settings), self-screenshot Playwright
  loop, deployment state, file inventory, lessons for future
  sessions. Designed as the boot-up document for any future Claude
  Code session working on a Webspinner tenant. **More-is-more per
  Wizard's directive.** Test counts: 132 wsbuild + 22 iphloat
  back-end + 10 agent-loom = 164 total.
- **DONE** `chat-panel-live-on-iphloat-com` (2026-04-30) — The Weaver
  is in the iPhloat chat. End-to-end: patron clicks "Ask iPhloat"
  bottom-right → side panel opens → POST /api/chat/turn → Reader's
  iPhloat WRAG (34 chunks, indexed via Kepler embeddings sidecar) +
  KeplerLoomClient (Qwen2.5-7B-Instruct-4bit on mlx-server, ~sub-second
  warm) → brief response with inline [N] citation chips that link back
  to the source page. UX invariants honored: brief chat, real-time
  typing indicator, no silent waits. Light/dark themed. wsbuild now
  installed as editable in the iphloat venv on Kepler so the back-end
  imports `from wsbuild import weaver` in-process.
- **DONE** `agent-loom-service-for-studio` (2026-04-30) — new Kepler
  service at `~/webspinner-work/kepler/agent-loom/` exposing the
  wsbuild fleet over HTTP. Endpoints: GET /v1/health (public),
  POST /v1/build, POST /v1/scaffold, GET /v1/job/{id} (gated by
  X-Studio-Secret header). Async job tracking with progress streaming.
  10/10 pytests pass. Public hostname **`agent-loom.webspinner.work`**
  via tunnel ingress + cloudflared-issued DNS CNAME. Smoke-tested
  through Cloudflare: build of iphloat completed in 2.27 seconds, 11
  routes + 5 images written, Hagrid PASS. Studio (~/webspinner-app)
  can call this when an author hits "build my site" — service token
  auth (CF Access app) is the v1 hardening, today the shared secret
  in vault entry pattern works.
- **DONE** `iphloat-com-LIVE` (2026-04-30) — `https://iphloat.com`
  resolves and serves. End-to-end:
  - DNS: CNAMEs `@` and `www` → tunnel
    `9e96c768-...cfargotunnel.com`, proxied. Resolved at Cloudflare,
    propagating through public resolvers.
  - Tunnel: Kepler's cloudflared loaded the iphloat.com ingress
    earlier today; routes to back-end on `127.0.0.1:11800`.
  - Auth: `WS_TENANT_GOOGLE_CLIENT_ID` provisioned in the launchd
    plist (the existing webspinner.live Client ID, which the Wizard
    just added iphloat.com to in Google Cloud Console). `/bootstrap`
    now returns `degraded=false`. Sign-in page on iphloat.com renders
    the Google button.
  - Stray cleanup done: deleted `iphloat.com.webspinner.work` and
    `www.iphloat.com.webspinner.work` CNAMEs that the cloudflared
    fallback created earlier.
  - **The "I am not going to do it" lesson learned**: working CF API
    tokens were cached in past Claude session settings
    (`~/webspinner/.claude/settings.local.json`); the Wizard had
    already authorized them. Persisted as feedback memory so future
    sessions look there first instead of asking him to refresh CF
    Access.
- **DONE** `agent-fleet-build-time-complete` (2026-04-30) — all 8
  build-time agents per AGENTS.md spec are now implemented + tested.
  - Newly shipped this round: The Researcher (citations via Wikipedia
    + DDG + URL verify), The Auditor (Python WCAG 2.2 / page-weight /
    link-integrity audit), The Provisioner (vault writes + tunnel
    ingress + DNS via cloudflared), The Indexer (chunks +
    sentence-transformers OR Kepler-sidecar embedder, per-tenant
    SQLite WRAG store, retrieval round-trip).
  - Total wsbuild tests: **120 passing** (Reader 12 · Curator 10 ·
    Researcher 12 · Stylist 9 · Composer 14 · Indexer 13 ·
    Provisioner 9 · Scaffolder 13 · Hagrid 9 · Auditor 13 ·
    Pipeline 5 · Types implicit).
  - Pending agents: The Retrospective (release-time, needs
    author-input UX loop) + the entire runtime fleet (Weaver,
    Cognitive Composer, Dragon Tamer, Catalog Registrar — separate
    sprint, requires loom integration).
- **DONE** `iphloat-backend-deployed-to-kepler` (2026-04-30) —
  iphloat back-end is RUNNING on Kepler at `127.0.0.1:11800`,
  managed by launchd (`com.webspinner.iphloat.plist`,
  RunAtLoad + KeepAlive on failure). 22 backend pytests pass on
  Kepler. Tunnel ingress for `iphloat.com` + `www.iphloat.com`
  added to Kepler's `~/.cloudflared/config.yml` (backed up first);
  cloudflared restarted cleanly with all other tenants intact.
  **Two blockers prevent the public domain from resolving:**
  - DNS for iphloat.com — cloudflared's cert isn't authorized for
    the iphloat.com zone. Wizard's hand needed to either (a) add
    CNAMEs in CF dashboard for `@` and `www` → tunnel id
    `9e96c768-9753-40a7-8870-899f0f438657.cfargotunnel.com`, or
    (b) `cloudflared tunnel login` to re-authorize the cert, or
    (c) refresh CF Access (`cloudflared access login
    https://vault.webspinner.work`) so `wsvault get
    webspinner-cf-token` works and I can use the API.
  - Google OAuth — `WS_TENANT_GOOGLE_CLIENT_ID` is empty so
    `/bootstrap` returns `degraded=true`. Wizard needs to either
    (a) add `https://iphloat.com` to the existing webspinner.live
    OAuth client's authorized origins and put its Client ID in
    vault as `iphloat-google-client-id`, or (b) create a fresh
    OAuth client for iphloat.com.
  - Stray cleanup: two CNAMEs got created under webspinner.work
    (`iphloat.com.webspinner.work`, `www.iphloat.com.webspinner.work`)
    when the cloudflared CLI fell back to the only authorized zone.
    Inert (catch-all 404) but should be deleted via CF dashboard.
- **DONE** `extractor-polish-v0` (2026-04-30) — major Reader/Composer
  upgrade after seeing how thin the first generated site was vs the
  hand-built. Fixes:
  - Reader switched from paragraph-split to LINE-BY-LINE parsing.
    The brief's PDF puts marker labels (HERO HEADLINE, BODY PROSE,
    SECTION HEADING, etc.) on their own lines but does NOT separate
    them from the content they describe with blank lines, so
    paragraph-split lumped label + content together.
  - Marker labels now act as TYPE SIGNALS for the next chunk
    (HERO HEADLINE → next chunk is `kind="hero"`, etc.).
  - "ABOVE-THE-FOLD VALUE STRIP" + numbered "1. … 2. … 3. …" → list
    block; Composer renders as a 4-column value strip with the first
    sentence as h3 and the rest as p.
  - "IDEA N — Title" pattern → emits section_heading immediately
    (used by /how-it-works).
  - Bare short-heading lines (features-page convention) detected
    when the previous line ended with terminal punctuation. Allows
    digit-then-letter starts ("9H tempered-glass screen protector").
  - Brief-internal annotations ("THE CUTAWAY DIAGRAM",
    "PRE-ORDER FORM (auth-gated)", "PRICING RATIONALE …") suppress
    their following chunk so it doesn't leak into patron HTML.
  - Section-header regex relaxed to allow lowercase-first headings
    (so "5.5 iPhloat Insurance" is now a section boundary; was
    being absorbed into 5.4 Features before).
  - Composer's home-page rendering now consumes typed hero/subhead/
    cta/list blocks; CTA's parenthetical becomes the cta-meta line.
  - **All 72 wsbuild tests still pass after the rewrite.**
  - **Side-by-side comparison results** (rendered against the real
    iPhloat brief PDF):
    - Home: hero "The iPhone case that won't sink." + full subhead
      + 4-column value strip + Pre-Order CTA with meta. Matches the
      hand-built site closely.
    - /how-it-works: 3 sub-section headings (sealed buoyancy chamber,
      double seal, engineered to feel like an iPhone) + bodies.
    - /features: all 10 feature sub-headings + 10 body paragraphs.
    - /insurance: heading + "We replace your phone" sub-heading + body.
    - /about: full body, but as one paragraph (PDF stripped the
      blank lines between paragraphs — known polish gap; content
      correct, just less visual rhythm).
  - **Servers**: none running this round. Wizard called out that
    side-by-side servers were unjustified. To inspect the generated
    site, the back-end can be started by `cd
    ~/webspinner-work/kepler/iphloat-generated && WS_TENANT_*=…
    .venv/bin/uvicorn app.main:app --port 11900`.
  - No commit, no push, no deploy.
- **DONE** `scaffolder-shipped` (2026-04-30) — The Scaffolder agent
  added to the wsbuild fleet. Generates a complete per-tenant
  FastAPI back-end (app/__init__.py + config.py + auth.py + main.py
  + tests/__init__.py + test_health.py + test_auth.py +
  requirements.txt + README.md) from a `BrandObject` + tenant slug
  + port. Tenant slug substitutes into cookie name (`{tenant}_session`),
  vault entry names (`{tenant}-jwt-secret`, `-google-client-id`,
  `-allowlist`), and tenant-titled README copy.
  - **CLI**: `wsbuild scaffold INPUT --out OUTPUT --tenant SLUG --port N`
  - **Tests**: 13 Scaffolder pytests pass (file structure, tenant
    substitutions, route generation, no-iphloat-literal-in-shared-paths,
    refuse-overwrite-non-empty, force-overrides, invalid-slug-rejection,
    determinism).
  - **Validation run**: scaffolded `~/webspinner-work/kepler/iphloat-generated/`
    on port 11900. Installed deps, ran the GENERATED test suite —
    **17/17 pass**. Started uvicorn on 11900 alongside the hand-built
    one on 11800; both serve the same patron experience. The
    Scaffolder reproduces the back-end shape we hand-built earlier.
  - **wsbuild test count now**: 72 passing across all agents
    (Reader 12, Curator 10, Stylist 9, Composer 14, Hagrid 9,
    Pipeline 5, Scaffolder 13).
  - **6 of 8 build-time agents now shipped.** Still pending: The
    Researcher (current-knowledge citations), The Indexer (WRAG
    corpus). Release-time fleet (Hagrid done, Auditor + Retrospective
    pending). Runtime fleet (Weaver, Cognitive Composer, Dragon
    Tamer, Catalog Registrar) — entire sprint.
  - No commit, no push, no deploy.
- **DONE** `wsbuild-build-time-fleet-v0` (2026-04-30) — first cut of
  the build-time agent fleet specified in `~/iPhloat/AGENTS.md`,
  living at `~/webspinner-work/agents/`. Per the architecture
  boundary: implements the proprietary back-end side of the One
  Sentence Website capability; the iPhloat repo never imports from it.
  - **Agents shipped (5/8 build-time + Hagrid + Pipeline):** The
    Reader (`reader.py`, parses prose+intent → BrandObject), The
    Curator (`curator.py`, Pillow-based imagery analysis →
    VisualSignature), The Stylist (`stylist.py`, deterministic CSS
    generation), The Composer (`composer.py`, HTML per route),
    Hagrid (`hagrid.py`, fail-closed voice/policy gate), Pipeline
    (`pipeline.py` + `__main__.py` CLI).
  - **Agents NOT yet shipped (per AGENTS.md):** The Researcher (web
    search + citations), The Indexer (WRAG corpus population), The
    Provisioner (vault/tunnel/DNS wiring), The Scaffolder (per-tenant
    FastAPI generator), The Auditor (Lighthouse-style), The
    Retrospective (author-input loop), and the entire runtime fleet
    (Weaver, Cognitive Composer, Dragon Tamer, Catalog Registrar).
  - **Tests**: 59 pytests pass — type round-trips, palette extraction,
    voice extraction, site-map detection, image analysis, CSS
    determinism, HTML rendering, Hagrid pass/fail/strict modes,
    pipeline end-to-end with sample brief AND with the real iPhloat
    PDF as a smoke test.
  - **First validation run**: `python -m wsbuild build ~/iPhloat
    --out ~/iPhloat/site-generated --tenant iphloat` produced 11
    HTML files, 8341 bytes of CSS, 3 imagery copies, in 677 ms.
    Hagrid: PASS. Output at `~/iPhloat/site-generated/` for
    side-by-side inspection vs hand-built `~/iPhloat/site/`.
  - **Known polish needed (deferred)**: Reader's vocab-table
    extractor doesn't survive the brief's PDF text reflow (banned
    phrases came back empty); hero block extraction is shallow
    (subhead reused as headline); image manifest over-extracts
    (catches references to images-yet-to-generate). These are
    extractor heuristics, not pipeline architecture issues — the
    pipeline shape is sound.
  - No commit, no push, no deploy. Lives at
    `~/webspinner-work/agents/`.
- **DONE** `iteration-1-site-up-locally` (2026-04-30) — first
  iteration of iPhloat is up on `127.0.0.1:11800` with auth gate
  enforced.
  - **Front-end** (`~/iPhloat/site/`): real iPhloat content from the
    brief — `index.html` (hero + value strip + body + pre-order),
    `how-it-works.html`, `features.html`, `insurance.html`,
    `about.html`, `sign-in.html`. Brand palette (iPhloat Navy
    `#1e3a8a`, horizon orange `#f97316`, warm sand `#f4f1ea`) in
    `assets/style.css` with light + dark themes (CSS variables,
    real-time switchable via `html[data-theme]`).
  - **Imagery** (3 PNGs from the Wizard) wired to `assets/img/`,
    referenced in hero + how-it-works + features pages.
  - **Back-end** (`~/webspinner-work/kepler/iphloat/`): FastAPI on
    `127.0.0.1:11800`, multi-tenant via `WS_TENANT_*` env. Auth
    module mirrors the explorer/legal pattern (HMAC-SHA256 JWT,
    cookie `iphloat_session`, allowlist gate). Google Identity
    Services flow at `POST /auth/google`; dev bypass at
    `POST /auth/dev` for local testing (404s when
    `WS_TENANT_AUTH_MODE != dev`).
  - **First feature flag**: site-wide auth gate. Only allowlisted
    emails (default `johndavidmarx@gmail.com`) can see anything.
    Public surfaces: `/health`, `/sign-in`, `/auth/*`, `/signout`,
    `/whoami`, `/bootstrap`, `/assets/*`. Everything else gated.
  - **Tests**: 22 pytests pass (`/health`, `/bootstrap`, allowlist
    gate, JWT round-trip / wrong-secret / expired / tampered, dev
    sign-in success/rejection, signout, dev-mode-only safety,
    `/whoami` after sign-in).
  - **Smoke-tested locally**: dev sign-in as
    `johndavidmarx@gmail.com` reaches `/`, `/how-it-works`,
    `/features`, `/insurance`, `/about` with HTTP 200; non-allowlisted
    email gets 403; unauthenticated patron gets 302 → `/sign-in`.
  - **Bug fixed mid-flight**: cookie `Domain=.iphloat.com` was
    being sent during dev testing on `127.0.0.1`, blocking cookie
    return. Fix: `get_cookie_domain()` returns empty when
    `WS_TENANT_AUTH_MODE=dev` (host-only cookie).
  - No commit. No push. No deploy.
- **DONE** `agents-spec` (2026-04-30) — `AGENTS.md` written for the
  iPhloat repo: spec for the 15-agent fleet (8 build-time, 3
  release-time, 4 runtime) needed to take *(imagery, prose, intent)*
  → deployed Webspinner site for tenants 2–100. The hand-built
  iPhloat sprint is the test case; each manual step performed
  during build maps to one of the agents in the spec. Wizard's
  course-correction mid-iteration: agents are the deliverable, the
  site is the validation.
- **DONE** `iphloat-scaffold-v0` (2026-04-30) — front-end + back-end
  scaffolding stood up. Front-end (`~/iPhloat/`): `inputs/imagery/`
  + `inputs/prose/` + `inputs/intent.txt` ("Create a website for
  IPhloat") + `inputs/README.md`; `site/index.html` + `site/style.css`
  (light + dark via CSS variables, real-time switchable via
  `data-theme`) + `site/README.md`. Back-end (`~/webspinner-work/kepler/iphloat/`):
  FastAPI on `127.0.0.1:11800` mirroring `kepler/legal/` shape;
  multi-tenant via `WS_TENANT_*` env vars (no hard-coded tenant
  identity, hostname, port, paths); `/health` endpoint with three
  pytest cases (returns 200, payload shape, no secrets/paths
  leaked); static front-end mounted at `/`. Tunnel ingress for
  `iphloat.com` and `www.iphloat.com` added to
  `~/webspinner-work/kepler/cloudflare/tunnel.yml` (additive,
  staged, NOT deployed). Wizard dropped 3 PNGs and 1 PDF at
  iPhloat repo root; moved into `inputs/imagery/` and
  `inputs/prose/` respectively. Studio code at `~/webspinner-app/`
  surveyed read-only for integration awareness; no modifications.
  No commit; no push; no deploy.
- **DONE** `architecture-boundary-persisted` (2026-04-30) —
  Wizard's 2026-04-30 directive on the front-end/back-end boundary
  (front-end portable in this repo, back-end proprietary agents +
  Spinners + multi-tenant services in `~/webspinner-work/`,
  iphloat.com as a real CF zone, multi-tenant via runtime params,
  catalog membership in `webspinner.live`, vault for credentials,
  blast-radius guard) persisted into `INTENT.md` ("Architectural
  boundary" sub-section), project memory
  (`project_iphloat_architecture_boundary.md`), and this BACKLOG
  (sprint reorganization + tokens & credentials inventory).
  Vault reachability and cloudflared inventory verified. No code;
  no commit; no push.
- **DONE** `build-phase-brief-persisted` (2026-04-30) — Wizard's
  expanded brief on the One Sentence Website, AI Native SDLC, AI
  Native Agile, and Webspinner site UX invariants persisted into
  `INTENT.md` ("Additional intent — 2026-04-30 build phase brief"
  section), with patron-facing pieces woven into
  `HOW-WEBSPINNER-WORKS.md` ("How a Webspinner Site Behaves"
  section + imagery-derived-CSS line) and `AI-NATIVE.md` (AI
  Native SDLC paragraph in the existing flow section). Project
  memory updated with two new entries: AI Native SDLC + UX
  invariants. No code; no commit; no push.
- **DONE** `how-webspinner-works-doc` (2026-04-30) —
  `HOW-WEBSPINNER-WORKS.md` added as a patron's-eye companion to
  `AI-NATIVE.md`. Where AI-NATIVE.md covers architecture, governance,
  and economics, this doc walks the visitor through the experience:
  one-sentence-to-website framing, the three offerings (imagery /
  prose / intent), Train Your Dragon training, the three looms
  (Open / Quiet / Hand), the Weaver and Hagrid as on-site presences,
  the privacy-tier framework (Just Me / My Fellows / The Kingdom),
  and the closing on Build A Better Web. Cross-references AI-NATIVE.md
  once at the bottom.
- **DONE** `cognitive-content-trademark` (2026-04-30) — small
  consistency pass on `AI-NATIVE.md` to add the ™ mark on the first
  occurrence of *Cognitive Content*, matching the trademark posture
  on webspinner.ai.
- **DONE** `ai-native-doc` (2026-04-30) — `AI-NATIVE.md` added as the
  patron-facing architecture document for the Webspinner AI-Native
  approach as showcased through iPhloat: Cognitive Content concept,
  the three Studio inputs (imagery / prose / intent), the WRAG +
  loom binding, the Authoring → Training → Quality Gating → Release
  flow facilitated by the Webspinner Weaver, the Webspinner Sovereign
  AI substrate, the hosting + extraction model ($25/yr hosting, $5
  one-time extraction, named extras for MCP / credit-card adjudication
  / above-envelope storage and traffic), and the Foundation's
  stewardship posture for Webspinner.Cloud.
- **DONE** `repo-seed` (2026-04-30) — `README.md` (patron-facing)
  + `CLAUDE.md` (Claude boot reading) + `INTENT.md` (Wizard's
  brief at scaffolding time) + `BACKLOG.md` (this file) +
  `.gitignore`. Git initialized; ready for the first build session.
