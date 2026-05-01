# Agents — the One Sentence Website fleet

The Webspinner approach to building a tenant site is **agentic**. A patron offers three things — *imagery*, *prose*, and *intent* — and a fleet of cooperating agents takes those three offerings and produces a deployed, governed, AI-Native site. iPhloat is the first realization of this fleet, hand-built as a working test case while the spec below was discovered by doing.

This document is the spec. Each agent below corresponds to a step the iPhloat sprint performed manually. The agents replace those manual steps for tenants 2 through one-hundred, and beyond.

## How to read this spec

Each agent is described in the same shape:

- **Purpose** — one sentence.
- **When it runs** — *build-time* (during the One Sentence Website flow that births a site), *release-time* (during quality gating), or *runtime* (in front of patrons after launch).
- **Inputs** — what the agent reads.
- **Outputs** — what the agent produces.
- **Dependencies** — other agents or services it relies on.
- **Honors** — which Webspinner UX invariants and AI Native SDLC principles the agent enforces.
- **Quality gates** — what must be true before the agent's output is accepted downstream.

The spec is deliberately implementation-agnostic. Each agent will be implemented as a service somewhere in `~/webspinner-work/`, with a tenant identity passed at runtime. The shape of the agent — its API, its responsibilities — is what this document fixes; the implementation is allowed to evolve.

## The fleet, at a glance

### Build-time fleet (runs once per site, when the site is born)

1. **The Reader** — parses the prose document into structured brand data.
2. **The Curator** — analyzes uploaded imagery and produces a visual signature.
3. **The Researcher** — pulls current credible third-party knowledge and cites it.
4. **The Stylist** — composes the CSS theme system from the brief and the imagery.
5. **The Composer** — generates page HTML for each route in the site map.
6. **The Indexer** — chunks the prose and embeds it into the tenant's WRAG corpus.
7. **The Provisioner** — wires tenant identity into vault, tunnel, and DNS.
8. **The Scaffolder** — generates the per-tenant FastAPI back-end and tests.

### Release-time fleet (runs on every change before deploy)

9. **Hagrid** — patron-voice and policy gate. Fails-closed on banned phrasing, exposed secrets, or accessibility regressions.
10. **The Auditor** — Lighthouse-style technical audit (performance, accessibility, SEO, security headers).
11. **The Retrospective** — packages what was built, presents it to the author for input, captures decisions.

### Runtime fleet (runs in front of patrons every request)

12. **The Weaver** — the chat-side loom. Converses with patrons, retrieves from WRAG, composes responses in tenant voice.
13. **The Cognitive Composer** — the right-panel renderer. Generates the single page of Cognitive Content the patron's current question warrants.
14. **The Dragon Tamer** — when an authoring patron offers new biscuits at runtime (a new product photo, a revised FAQ), this agent re-feeds the WRAG corpus and re-trains the loom for the affected surfaces.
15. **The Catalog Registrar** — at first deploy and on metadata changes, registers/updates the tenant in the `webspinner.live` site catalog so it can be featured and launched.

---

## Build-time agents

### 1. The Reader

**Purpose.** Parse the prose document(s) the patron offers into a structured brand object the rest of the fleet can act on.

**When it runs.** Build-time, first.

**Inputs.**
- `inputs/prose/*.{md,pdf,txt}` — author-provided brand documents.
- `inputs/intent.txt` — the single sentence of intent.

**Outputs.** A `BrandObject` with:
- `positioning` — who the site is for, what it competes with, where it wins.
- `voice` — tone, banned phrases, preferred phrases, vocabulary table.
- `palette` — named colors with hex values (hero, accent, background, surface, text, line).
- `type_system` — primary/fallback type families, hierarchy.
- `site_map` — list of routes with type (landing/marketing/commerce/auth/legal) and module (WebBook/Commerce/etc.).
- `pages` — for each route, the prose blocks (hero, body, pull-quotes, CTA).
- `image_manifest` — for each image referenced in the brief, the filename, aspect, and description.
- `roadmap` — phased milestones if present.
- `implementation_notes` — operational directives for the rest of the fleet.

**Dependencies.** None. The Reader is the floor.

**Honors.**
- Implementation honesty: never invent fields not present in the prose. Missing fields surface as `None`, not as plausible-sounding fabrications.
- Patron voice: extracts the banned-phrases list (the brief's "Don't use" column) and binds it to Hagrid for downstream enforcement.

**Quality gates.**
- The `BrandObject` must have at minimum: `positioning`, `voice.tone`, `palette.hero`, `site_map` (one or more routes), and one prose page block.
- Banned phrases extracted from the brief are non-empty (or explicitly empty by the brief's own statement).

### 2. The Curator

**Purpose.** Analyze the imagery the patron offers and produce a visual signature that drives the site's CSS.

**When it runs.** Build-time, after The Reader.

**Inputs.**
- `inputs/imagery/*.{png,jpg,jpeg,webp,heic}` — author-provided imagery.
- `BrandObject.palette` from The Reader (so the Curator can confirm or refine).

**Outputs.** A `VisualSignature` with:
- `dominant_colors` — top 5 colors per image, with weight.
- `palette_refinements` — proposed adjustments to The Reader's palette where imagery and brief disagree (Hagrid arbitrates).
- `image_assignments` — for each image manifest entry from The Reader, which uploaded file is the best match.
- `accessibility_metadata` — alt-text suggestions for each image (Hagrid validates).
- `aspect_ratios` — per-image, for layout decisions.

**Dependencies.** The Reader.

**Honors.**
- *Imagery is load-bearing in the build.* The Curator does not allow imagery to be ignored. Where the brief specifies an image but no upload matches, the Curator surfaces a placeholder request via The Retrospective.
- *Don't compromise design on uploaded images.* The Curator's palette refinements are honored unless the brief explicitly fixes a color that conflicts.

**Quality gates.**
- Every uploaded image is assigned to at least one manifest entry, OR surfaced as "extra/unassigned" for The Retrospective.
- Every brief manifest entry is either assigned to an upload OR queued for generation by an external image agent (out of scope for this fleet; handled by a sibling Image Generation agent that lives on `~/webspinner-app` Studio).

### 3. The Researcher

**Purpose.** Fetch current credible third-party knowledge the build needs, and cite it.

**When it runs.** Build-time, on demand from any agent that needs current facts (The Composer most often).

**Inputs.**
- A research query (e.g. "current price of Catalyst Total Protection iPhone case").
- A `BrandObject` for context (so the Researcher knows the domain).

**Outputs.** A `ResearchResult` with:
- `claim` — the one-sentence answer.
- `sources` — list of `{url, title, accessed_at}` citations the claim rests on.
- `confidence` — high/medium/low based on source agreement.
- `freshness` — how recent the sources are.

**Dependencies.** None internal. External: web search and fetch capability.

**Honors.**
- *Current knowledge with citations.* Every claim carries at least one source. Claims with zero sources are returned as `confidence: low` and tagged for The Retrospective.
- *No prior-LLM-training-as-fact.* The Researcher never returns a claim it has not just verified against a source it just read.

**Quality gates.**
- Sources reachable at fetch time (TLS valid, 200 OK).
- Citations stored alongside the page block they ground; The Composer renders them as visible links.

### 4. The Stylist

**Purpose.** Compose the site's CSS theme system from the BrandObject palette and the VisualSignature.

**When it runs.** Build-time, after The Reader and The Curator.

**Inputs.**
- `BrandObject.palette`, `BrandObject.type_system`.
- `VisualSignature.palette_refinements`, `VisualSignature.dominant_colors`.

**Outputs.** A complete `style.css` (or set of CSS files) honoring:
- CSS custom properties for every color.
- Light *and* dark themes via `@media (prefers-color-scheme: dark)` and `html[data-theme=light|dark]`.
- Responsive type scale.
- Two-panel layout primitives (chat panel + Cognitive Content panel) per the Webspinner UX invariants.
- Header / hero / value-strip / section / band / footer primitives.

**Dependencies.** The Reader, The Curator.

**Honors.**
- *Light + dark themes, switchable in real time.* The CSS variable surface guarantees both themes use the same component classes; the patron-side toggle changes only `data-theme` on `<html>`.
- *Imagery-derived CSS.* The Stylist incorporates the Curator's palette refinements as default values; brief-fixed colors override.
- *Two-panel layout.* The Stylist provides the `.chat-panel` / `.cognitive-panel` primitives even on pages that don't yet use them, so tenants 2-100 inherit the same shape.

**Quality gates.**
- WCAG 2.2 AA contrast for every foreground/background pair in both themes (Hagrid validates).
- No banned vendor names in the CSS (no `font-family: -apple-system` is fine; no `font-family: 'Anthropic Sans'` would not be).

### 5. The Composer

**Purpose.** Generate the HTML for every route in the site map, lifting prose verbatim from the BrandObject and weaving in imagery, citations, and CTAs.

**When it runs.** Build-time, after The Stylist.

**Inputs.**
- `BrandObject.pages` — page-by-page prose.
- `BrandObject.site_map` — routes to generate.
- `VisualSignature.image_assignments` — which images go where.
- `style.css` from The Stylist (for class names to use).
- `ResearchResult`s where any page block needs current third-party fact.

**Outputs.** A set of HTML files, one per route, mounted at the back-end's static root. Each file:
- Uses the patron-voice copy verbatim from the brief (no rewriting).
- References imagery via the assignments from The Curator.
- Renders citations from The Researcher inline where claims need them.
- Includes a header, footer, and the two-panel layout primitive on routes that need it.

**Dependencies.** The Reader, The Stylist, The Curator, optionally The Researcher.

**Honors.**
- *Brief is canonical.* The Composer does not paraphrase. If the brief says *"floats face-up"*, the page says *"floats face-up"* — never *"won't sink"*.
- *Single-page Cognitive Content panel.* The Composer reserves a `<div class="cognitive-panel">` slot on routes that have it; The Cognitive Composer fills it at runtime.
- *Brief content authoring order.* Per Brief §9.2: build /about → /how-it-works → /features → /insurance → / (last; synthesizes others).

**Quality gates.**
- Every route in the site map has a corresponding HTML file.
- No banned phrase from the brief's "Don't use" column appears in any generated HTML (Hagrid validates).
- Every image referenced has alt text from The Curator.
- Every citation references a source that fetched cleanly at build time.

### 6. The Indexer

**Purpose.** Chunk the prose, embed it via the existing Webspinner embeddings substrate, and persist the WRAG corpus for the tenant's loom to retrieve from at runtime.

**When it runs.** Build-time, after The Reader. Re-runs on any prose change.

**Inputs.**
- `BrandObject.pages` — the prose, page-by-page.
- `inputs/prose/*` — original documents (so citations point back to source).
- Tenant identity for scoping.

**Outputs.** A populated WRAG corpus — chunks + float32 embeddings — keyed by tenant identity. Either tenant-local SQLite (recommended for tenant #1) or centralized via `weaver-memory` (recommended once tenant #2 onboards and the corpus shape stabilizes).

**Dependencies.** The Reader. The existing embeddings substrate on Kepler.

**Honors.**
- *Drift discipline.* Tenant-local SQLite for the first tenants; extraction into shared infrastructure deferred until the third tenant reveals what is actually shared.
- *Cite-back-to-source.* Every chunk carries `source_path + heading_anchor` so The Weaver's responses can cite cleanly.

**Quality gates.**
- All chunks embedded successfully (no silent skips).
- Citations resolve at retrieval time (tested via at least one round-trip query).

### 7. The Provisioner

**Purpose.** Wire tenant identity into the platform: vault entries, tunnel ingress, DNS records, launchd plist environment.

**When it runs.** Build-time, before The Scaffolder produces the back-end.

**Inputs.**
- Tenant identity, hostname, port (assigned from a free-port allocator).
- `BrandObject.implementation_notes` for any tenant-specific config.

**Outputs.** Provisioned platform state:
- Vault entries: `{tenant}-jwt-secret`, `{tenant}-google-client-id`, `{tenant}-allowlist` (and any others the BrandObject requires).
- Tunnel ingress in `~/webspinner-work/kepler/cloudflare/tunnel.yml` for the tenant's hostname → loopback port.
- DNS record creation request (CNAME tenant-host → tunnel.cfargotunnel.com).
- launchd plist env-var contract for the back-end installer to honor.

**Dependencies.** None internal. External: vault, Cloudflare API, cloudflared.

**Honors.**
- *Vault for credentials.* Never writes secrets to disk outside the vault. The Provisioner's outputs reference vault keys, not values.
- *Blast-radius discipline.* Tunnel.yml changes are *additive only* — appended before the catch-all 404, never deleting or renaming existing entries. Validates the YAML parses before saving.
- *Multi-tenant runtime configuration.* All values flow into env vars at launchd-load time; nothing is hard-coded into source.

**Quality gates.**
- Tunnel.yml still parses as valid YAML.
- New vault entries readable by the service-caller credentials.
- DNS change request visible in Cloudflare API audit log.
- Existing tenants' tunnel ingresses unchanged.

### 8. The Scaffolder

**Purpose.** Generate the per-tenant FastAPI back-end mirroring the existing Kepler tenant template.

**When it runs.** Build-time, after The Provisioner.

**Inputs.**
- Tenant identity, hostname, port from The Provisioner.
- `BrandObject.site_map` for the route set the back-end serves.
- The existing template at `~/webspinner-work/kepler/iphloat/` (tenant #1 is the canonical reference).

**Outputs.**
- A new directory `~/webspinner-work/kepler/{tenant}/` containing `app/`, `tests/`, `requirements.txt`, `README.md`, `deploy/` (plist + install + admin-deploy scripts).
- All env-driven via `WS_TENANT_*` variables (no `iphloat` literal in shared paths).
- Auth module wired to use tenant-specific cookie name, JWT secret, allowlist, Google Client ID.
- /health, /bootstrap, /whoami, /sign-in, /auth/google, /auth/dev, /signout endpoints.
- Auth-gate middleware on patron-facing routes.
- Static mount for the front-end at `WS_TENANT_STATIC_DIR/assets`.
- pytest suite covering /health, allowlist gate, JWT integrity.

**Dependencies.** The Reader (for site map), The Provisioner.

**Honors.**
- *Drift discipline > DRY.* The Scaffolder *copies* from the canonical template, it does not refactor a shared library across tenants. Tenant 2 and tenant 3 are allowed to diverge; only the third concrete instance justifies extraction.
- *No half-finished implementations.* The Scaffolder either produces a back-end that passes its own tests OR fails the build with a clear error. No skeleton commits, no `pass` placeholders.

**Quality gates.**
- `pytest tests/` passes 100%.
- `uvicorn app.main:app` starts cleanly with the env vars The Provisioner produced.
- `curl /health` returns 200 with the expected payload shape.

---

## Release-time agents

### 9. Hagrid

**Purpose.** Patron-voice and policy gate. The patient governor at the door. Nothing reaches a patron without Hagrid's nod.

**When it runs.** Release-time, on every proposed change before it is allowed to deploy.

**Inputs.**
- Generated HTML, CSS, and any other patron-facing artifact.
- `BrandObject.voice.banned_phrases` and `BrandObject.voice.preferred_phrases`.
- The Webspinner-wide voice rules from `~/webspinner-work/PATTERNS-FOR-CLAUDE.md`.

**Outputs.** A pass/fail verdict per artifact, with reasons. On fail, returns the specific lines that violated.

**Honors.**
- *Webspinner-only branding.* Fails-closed on any vendor name leakage (LLM provider, model framework, embedding library, hardware specifics).
- *Patron-voice rules.* Banned phrases from the brief AND from PATTERNS-FOR-CLAUDE.md.
- *No half-finished implementations reach patrons.* Fails on TODO/FIXME/`coming soon` strings in patron-visible HTML.

**Quality gates.**
- Hagrid is fail-closed: anything Hagrid hasn't explicitly approved doesn't ship.
- Hagrid's verdict is logged to the per-call ledger so denials can be reviewed.

### 10. The Auditor

**Purpose.** Technical quality gate — performance, accessibility, SEO, security headers.

**When it runs.** Release-time, after Hagrid.

**Inputs.** The deployed-state preview of the site (back-end running locally with the generated front-end mounted).

**Outputs.** Lighthouse-style scores per page, plus a list of WCAG 2.2 violations. A per-page pass/fail.

**Honors.**
- *Lighthouse 95+* per Brief §9.6, on Performance, Accessibility, Best Practices, SEO.
- *WCAG 2.2 AA* minimum for accessibility.

**Quality gates.**
- Every page hits the score floor or the deploy is blocked.
- Accessibility violations are *zero* (AA), not a budget.

### 11. The Retrospective

**Purpose.** When the build needs the author's input — a missing image, a content tradeoff, a tone disagreement between brief and imagery — package what's been built, present it, take the input, iterate.

**When it runs.** Build-time *and* release-time, whenever any other agent surfaces a question for the author. Post-launch, on a cadence the author chooses (weekly, post-engineering-update, etc.).

**Inputs.**
- All artifacts produced so far.
- Open questions from other agents.

**Outputs.** A retrospective package the author reviews:
- *Done* — what's complete and ready for release.
- *Blocked* — what's waiting for the author's input, with the question framed as a single recommendation (per the *one recommendation, no questions* SDLC principle).
- *Risks* — what the build noticed but isn't blocked on.

The author's responses become the input for the next iteration.

**Honors.**
- *Iterative and interactive.* No big-bang generation; small steps, retrospectives between.
- *One recommendation, no questions.* When asking for input, the agent presents *the recommended path* and asks the author to confirm or override — never a list of options.
- *No corner-cutting.* If the easy path means a degraded site, the retrospective surfaces it as such; the author's accept/reject is captured for the audit trail.
- *Live progress.* The retrospective is built in real time as artifacts land; the author sees the package fill in as the agents work, not at the end.

**Quality gates.**
- Every blocked question carries a single recommendation.
- The author's response is captured in the per-call ledger so future iterations honor prior decisions.

---

## Runtime agents

### 12. The Weaver

**Purpose.** The chat-side loom. Listens to patron messages, retrieves from WRAG, composes responses in tenant voice with citations.

**When it runs.** Runtime, on every chat turn.

**Inputs.**
- Patron message.
- Conversation context (prior turns within the session).
- WRAG corpus for the tenant.
- Tenant voice rules from BrandObject.

**Outputs.**
- Brief response text for the chat panel.
- Optionally, a directive to The Cognitive Composer to render a fresh page in the right panel.
- Citations for every factual claim in the response.

**Dependencies.** The Indexer (corpus), the loom assignment from BrandObject (Open / Quiet / Hand).

**Honors.**
- *Brief chat.* Responses are concise; preamble forbidden.
- *Loom selection respected.* If tenant configured Quiet Loom but the loom doesn't yet support corpus-grounded tool use, The Weaver falls back to context-stuffing rather than answering ungrounded.
- *Live progress.* Streams partial responses as they're composed.
- *Citations.* Every claim carries a citation from the WRAG corpus.

**Quality gates.**
- No answer ungrounded by either retrieval or context-stuffing — failures return *"I'm gathering my thoughts on that one — ask me again?"* not a fabricated answer.

### 13. The Cognitive Composer

**Purpose.** The right-panel renderer. Receives a directive from The Weaver, generates one Cognitive Content page for the patron's current question.

**When it runs.** Runtime, on Weaver directive.

**Inputs.**
- Directive from The Weaver (what page to render, with what emphasis).
- WRAG corpus, BrandObject, current patron context (signed-in identity, scroll history if available).

**Outputs.** A single HTML page rendered into the right panel — *one page, replacing rather than stacking*.

**Honors.**
- *Single-page Cognitive Content panel.* Replaces, never stacks.
- *Adaptive content rendering* per Brief §6.2 — same source content, different rendering depending on patron context.
- *Live progress.* Renders the page in real time, surfacing each block as it composes.

**Quality gates.**
- Page composes in under 2 seconds (first paint), with full content under 5 seconds.
- Hagrid still applies: banned phrases blocked at render time too.

### 14. The Dragon Tamer

**Purpose.** When an authoring patron offers new biscuits at runtime — a new product photo, a revised page, an FAQ update — re-feed the WRAG corpus and re-train the loom for the affected surfaces.

**When it runs.** Runtime, on author-side input (new file dropped, page edited, FAQ updated).

**Inputs.**
- The new biscuit (file or text).
- The existing WRAG corpus.

**Outputs.**
- Updated chunks + embeddings in the WRAG corpus.
- Re-rendered pages where the change would affect content.
- A retrospective entry summarizing what changed and which surfaces were updated.

**Honors.**
- *Iterative and interactive.* Each biscuit is a small step; the author sees the change reflect in the live site within seconds.
- *Train Your Dragon.* The metaphor is the operational model — biscuits feed the dragon, the dragon's voice deepens, no rebuild from scratch.

**Quality gates.**
- The change is reversible — every biscuit-feed creates a corpus version the author can roll back to.

### 15. The Catalog Registrar

**Purpose.** At first deploy and on metadata changes, registers/updates the tenant in the `webspinner.live` site catalog so it can be featured and launched.

**When it runs.** Runtime — once at first deploy, then on tenant-metadata changes.

**Inputs.**
- Tenant identity, hostname, brand summary, visual signature thumbnail.
- BrandObject.positioning for the catalog blurb.

**Outputs.** A catalog row at `webspinner.live` (or wherever the catalog lives) describing the tenant for prospective patrons browsing what's available.

**Honors.**
- *Multi-tenant from the first call.* The catalog API is multi-tenant; iPhloat's first row sets the shape that tenants 2-100 follow.

**Quality gates.**
- Catalog entry round-trips: written entry is readable via catalog API.
- Catalog entry honors patron-voice rules (Hagrid validates).

---

## How the fleet runs together

For a new tenant, the flow is:

1. Patron uploads imagery and prose into Studio (or, today, drops them into `~/{tenant}/inputs/`).
2. Patron declares intent in a single sentence.
3. **The Reader** parses the prose into a `BrandObject`.
4. **The Curator** analyzes the imagery into a `VisualSignature`.
5. **The Researcher** is queried by other agents as they hit claims that need current sources.
6. **The Stylist** composes the CSS theme.
7. **The Composer** generates HTML for each route.
8. **The Indexer** populates the WRAG corpus.
9. **The Provisioner** wires vault, tunnel, DNS, plist env contract.
10. **The Scaffolder** generates the per-tenant FastAPI back-end and tests.
11. **Hagrid** reviews every artifact. **The Auditor** measures every page. **The Retrospective** surfaces anything that needs the author's input — with one recommendation each.
12. The author's responses iterate the build.
13. When all gates pass, the deploy lands. **The Catalog Registrar** registers the tenant.
14. Patrons arrive. **The Weaver** answers their chats. **The Cognitive Composer** fills the right panel. **The Dragon Tamer** feeds new biscuits as the author offers them.

## What this fleet is NOT

- Not a replacement for the author. The author is the protagonist; the fleet serves what the author meant.
- Not a one-shot generator. Iteration with retrospectives is the operational model.
- Not autonomous in production. Hagrid gates every change reaching patrons. The author retains the merge-to-main authority.
- Not vendor-locked. The loom selection is per-tenant (Open / Quiet / Hand); the fleet's APIs do not assume any particular model or framework.

## Status

iPhloat is the first test case. Every agent above has a manual analog that the iPhloat sprint performed by hand — that hand-built site is the validation set. The agents themselves are the deliverable; the next sprints will implement them, one by one, with iPhloat as the working baseline.
