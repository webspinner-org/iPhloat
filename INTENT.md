# iPhloat — the Wizard's intent at scaffolding time

This file captures the Wizard's directive *as given*, the day this
repo's Claude boot files were seeded. It is the source of intent
for everything else. When a future implementation choice conflicts
with what's recorded here, this file outvotes inference.

Date seeded: 2026-04-30.

## Verbatim brief

The Wizard's exact words when he asked for this repo to be primed:

> "Please place in the new directory called ~/iPhloat and files
> that Claude need to boot for a new web site app that is driven by
> the Webspinner ECO System and takes full advantage of the Kepler
> backend. This webapp, as all webapps in the future will be
> registered on cloudFlare, but served through Kepler. I expect
> over 100 sites before we are done, with prelaunch work."

The patron-facing description, captured already in
[`README.md`](README.md):

> "**The iPhone case that won't sink.**
> Waterproof. Drop-proof. *It floats.*"
>
> "iPhloat is a fully waterproof iPhone case engineered to float
> face-up when dropped in water. Built for boaters, anglers,
> paddlers, surfers, kayakers, pool-side parents, dock hands, and
> anyone who has ever watched their phone disappear beneath the
> surface."

## Decoded — the load-bearing constraints

These are the constraints that flow from the brief above. If the
brief and this list ever drift apart, the brief wins.

### 1. Webspinner ecosystem tenant — not a one-off

iPhloat is **driven by the Webspinner ecosystem**, not built
alongside it. That means:

- It consumes Webspinner Studio (content authoring), WebBook (long-
  form storytelling pages), Commerce (cart/checkout), RAG (product
  Q&A + customer support), Loom (orchestration), Wand (directive
  execution). Where these modules already exist in the ecosystem,
  iPhloat *uses* them; it does not re-implement them.
- It honors the cross-repo quality guide
  (`~/webspinner-work/PATTERNS-FOR-CLAUDE.md`). Patron voice rules
  apply. The "patron / Weaver / loom / thread" vocabulary applies.
- The iPhloat *brand* lives on top — but the *engine* underneath is
  shared with every other Webspinner tenant.

### 2. Registered on Cloudflare, served through Kepler

This is the *deploy invariant* for iPhloat and for all future
tenants:

- **DNS + edge** lives in Cloudflare. The `iphloat.com` zone is a
  Cloudflare zone.
- **Runtime** lives on Kepler (Mac Studio M4 Max, hostname
  `Johns-Mac-Studio.local`). Kepler runs the FastAPI service on a
  loopback port (mirroring the per-tenant pattern at
  `~/webspinner-work/kepler/legal/` and
  `~/webspinner-work/kepler/sovereign/`).
- **The bridge** is the Cloudflare Tunnel
  (`com.webspinner.cloudflared` on Kepler). The tunnel routes
  `iphloat.com` (and any subdomain) to the loopback port.

This is **not Cloudflare Pages.** It is **not Cloudflare Workers.**
It is a Kepler-hosted FastAPI service whose hostname Cloudflare
resolves to the tunnel.

This is the same shape that `analyzer.webspinner.live`,
`sovereign.webspinner.live`, and the other live Webspinner tenants
use. iPhloat differs only in that:

- the public domain is `iphloat.com`, not a `webspinner.live`
  subdomain;
- the cart + checkout surface is a *first-class* feature
  (consumer commerce — not service B2B);
- the RAG corpus is product-centric (specs, FAQs, materials,
  warranty terms) rather than legal documents or analyzer reports.

### 3. The 100+ tenants horizon

The Wizard has stated "over 100 sites before we are done, with
prelaunch work." iPhloat is the **first** tenant of that cohort.
Two consequences:

- **Drift discipline > DRY.** Patterns established here will be
  copied. Default to *predictable, copy-pasteable* shapes. If
  iPhloat invents something interesting, isolate it so it doesn't
  become accidentally load-bearing for tenants 2–100.
- **The deploy must be repeatable.** A new tenant should be one
  scripted operation (cookiecutter, scaffold, or similar). Do not
  hand-stand each one. The first iteration is allowed to be
  artisanal so that the *second* tenant's stand-up reveals what
  to extract.
- **The apps-tier destination is documented in
  `~/webspinner-work/ROADMAP.md`.** Today's shape (CF DNS → CF
  Tunnel → Kepler) is the stepping stone. The destination is a
  five-tier shape with a presentation server in front of Kepler
  and a storage box for LLM/RAG assets. Don't paint into a corner
  that only works on Kepler.

### 4. Prelaunch work — not a v1 already in patron hands

"Prelaunch work" means: nobody is hitting `iphloat.com` yet. There
are no patron-data-loss concerns to design around. There is no
backwards-compatibility tax. The work is *greenfield-with-strong-
patterns*: greenfield because nothing is live; strong-patterns
because the ecosystem already has shape and conventions.

This matters for migration choices, schema choices, and feature-flag
choices. There is no need to gate features behind toggles or build
shims for absent code.

## What I (the seeding session) deliberately did NOT decide

- **Tech stack choices.** Whether the frontend is server-rendered
  HTML (like sovereign-ai's `index.html`), a static
  Cinzel/Cormorant template (like webbooks), or a hybrid. Likely
  the latter, but the next session should make this call explicitly.
- **Schema for the catalog.** iPhloat presumably has a small SKU
  catalog (iPhone 14 / 15 / 16 / 17 × Pro / Pro Max × colorways).
  The exact shape is a one-conversation decision; I haven't
  pre-baked it.
- **Payment processor choice.** The README implies a built-in
  cart/checkout. The actual processor (Stripe, others) is part of
  the *Webspinner Spool* design conversation that is itself
  pre-design (see `~/webspinner-sovereign-ai/BACKLOG.md` →
  "Webspinner Spool"). For iPhloat as a B2C product, Stripe is
  the obvious starting point — but the architectural decision lives
  in the Spool conversation, not here.
- **Studio module wiring.** The README enumerates Studio / WebBook
  / Commerce / RAG / Loom / Wand. Some of these are real today
  (Studio, WebBook); some are partial; some are aspirational. The
  next session should reality-check each module before writing code
  that consumes it.
- **Whether iPhloat lives at `~/iPhloat/` long-term, or migrates
  to `~/webspinner-work/kepler/iphloat/`.** The current location
  is consistent with how `~/webspinner-sovereign-ai/` lives at
  top-level even though it has a per-tenant deployment under
  `~/webspinner-work/kepler/sovereign/`. Same pattern likely
  applies here. The next session should confirm with the Wizard.

## What the next session should do first

1. **Read this file. Then re-read it after reading the cross-repo
   pointers in `CLAUDE.md`.** The intent should make more sense
   the second time.
2. **Get the Wizard's build brief.** This file captures *why*
   iPhloat exists; it does not capture *what to ship first*. Ask:
   - Is the v1 deliverable a marketing site (no commerce yet)?
   - Or a marketing site + cart + Stripe checkout?
   - Or a marketing site + Q&A RAG over product copy?
   - What's the launch date?
3. **Mirror the deploy shape.** Whatever the v1 surface is, the
   deploy shape is the same as `~/webspinner-work/kepler/legal/` —
   FastAPI on a Kepler loopback port, plist-managed, fronted by
   the CF Tunnel. Get *that* working end-to-end before you build
   features.
4. **Set up the test bar.** ~200 pytests in
   `~/webspinner-sovereign-ai/service/tests/` is the standard.
   iPhloat doesn't need that many on day one, but the *ratio* of
   code-to-tests should be the same.
5. **Update `BACKLOG.md` continuously.** Every decision the Wizard
   makes, every pattern you establish, every "we'll do this later"
   item — capture it. Future tenants will copy from here.

## Additional intent — 2026-04-30 build phase brief

The Wizard expanded the brief during the iPhloat session of
2026-04-30, ahead of any code being written. These directives
augment (and where they conflict, outvote) the seeding-time intent
above.

### What iPhloat actually prototypes

iPhloat is the first realization of the **One Sentence Website**
capability that Webspinner Studio will eventually run for every
tenant. The capability turns the three offerings — *imagery*,
*prose*, and a *single sentence of intent* — into a deployed
Webspinner tenant. iPhloat builds this capability from scratch in
Claude Code, by orchestrating the existing Kepler substrate
(embeddings, corpus, loom). What works for iPhloat will be
extracted into Studio. The Wizard will manually drop the imagery
and prose into this repo for iPhloat itself; Studio will handle
that step for tenants 2–100.

### How the build agent must behave

This is **AI Native SDLC** and **AI Native Agile** — software
discipline applied to a build run by an AI agent partnered with
a human author.

- **Sophisticated loom.** Content creation runs on a loom capable
  of exemplary work, not the cheapest available.
- **Current knowledge with citations.** The agent accesses current
  credible third-party sources and cites them. Prior LLM training
  is not sufficient.
- **One recommendation, no questions.** When a choice arises, the
  agent commits to a single recommendation. It does not interview
  the author with a list of questions.
- **Iterative and interactive.** Small steps, each tested before
  the next. No big-bang generation followed by review-and-fix.
- **Retrospective-driven author input.** When the author's input
  is needed, the build does a retrospective — presents what has
  been built so far, takes input, iterates. The easy way out is
  forbidden.
- **Live progress, no silent waits.** The author always sees what
  the agent is doing. No timers, no arbitrary gates — events,
  responses, and interrupts queue in real time and execute swiftly.
- **Imagery is load-bearing.** Uploaded imagery drives the site's
  CSS — colors, palettes, type pairings, layout-density cues. The
  build does not compromise the design by ignoring what was given.

### What every Webspinner site delivers (UX invariants)

Patron-facing UX rules every Webspinner site honors. iPhloat as
tenant #1 sets the cookie-cutter for tenants 2–100; drift on any
of these breaks the recognition that *this is a Webspinner site*.

- **Two-panel layout.** Chat panel on one side, Cognitive Content
  panel on the other (right-of-chat is the canonical placement).
- **Brief chat.** The AI is brief in the chat panel.
- **Single-page Cognitive Content.** The Cognitive Content panel
  shows one page at a time — composed for the patron's current
  question, replacing rather than stacking.
- **Event-driven.** Events originate from chat, web objects
  (buttons, menus, links), and slow server-side responses.
  Events queue in real time and execute swiftly. No timers, no
  arbitrary gates.
- **Live progress always.** The site always tells the patron what
  it is doing while it is doing it. No silent waits.
- **Light and dark themes, switchable in real time.** Reference
  the Sovereign AI app's runtime theme switch (instant, no page
  reload).
- **Imagery-derived CSS.** The patron experiences the site as
  visually coherent with the imagery the author provided.

### Architectural boundary — front-end portable, back-end Webspinner-core

A non-negotiable separation, set 2026-04-30: while iPhloat is
being built, Webspinner is also building the server-side
proprietary agents that *build* websites. The two must not
mingle.

- **Front-end (this repo, `~/iPhloat/`).** Portable. A site
  owner can extract it and host elsewhere — the $5 extraction
  promise is real. Static or near-static patron-facing UI. **No
  proprietary intelligent agents and no Spinners inside this
  repo.** The website is a consumer of services, not an
  implementer.
- **Back-end (`~/webspinner-work/`).** Where Webspinner's
  proprietary agents, Spinners, and multi-tenant services live.
  iPhloat calls these services through the existing Cloudflare
  Tunnel that fronts the rest of the ecosystem.

**Multi-tenant requirement.** Every back-end service iPhloat
relies on must be multi-tenant and configurable through runtime
parameters. No hard-coded values for tenant identity, hostname,
loom selection, database paths, port numbers, theme defaults, or
anything else that may need to change. iPhloat is tenant #1 of
100+; a literal `iphloat` in any shared code path is a defect.

**Real domain.** `iphloat.com` is a registered Cloudflare zone.
iPhloat is hosted from `iPhloat.com` directly — not a subdomain
of `webspinner.*`. The CF Tunnel maps `iphloat.com` to a Kepler
loopback port.

**Catalog membership.** All sites built by Webspinner Studio go
into a catalog that `webspinner.live` features and launches.
iPhloat enters that catalog. Whatever back-end registers a site
in the catalog must be designed multi-tenant from the first call.

**Vault for credentials.** `wsvault` is how back-end agents and
services receive the credentials they need. The standing rule
holds: never export provider keys in a shell session — Vault →
install script → launchd plist only.

**Blast-radius discipline.** Don't break code that already works.
Any service iPhloat needs added to Webspinner core is added
*additively* — new module, behind feature flags, with tests,
without disturbing existing tenants (analyzer, sovereign, legal,
weaver, weaver-memory, mlx-server-weaver, cognitive-store,
cognitive-cdn, image-engine, etc.).

### Build phase posture

- No code yet — the Wizard releases the build phase explicitly.
- When code lands, every patron-facing surface ships behind a
  feature flag. Flags flip only as each surface clears its tests
  end-to-end.
- No git commits or pushes to GitHub until the Wizard authorizes
  public exposure.
