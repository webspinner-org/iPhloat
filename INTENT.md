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
