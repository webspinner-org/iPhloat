# iPhloat — boot reading for Claude Code

You are in `~/iPhloat`, the codebase for the **iPhloat brand site +
storefront** — a waterproof iPhone case that floats face-up. iPhloat
is a *consumer product tenant* of the Webspinner ecosystem, and it
is **the first of 100+ tenant sites planned across the apps tier**.
Patterns you set here will be copied — drift discipline matters more
than DRY.

The Wizard's intent for this session, captured the day the repo was
seeded, lives in [`INTENT.md`](INTENT.md). **Read it first.**

## What iPhloat is

The patron-facing pitch — what the world sees on
[`README.md`](README.md) — frames iPhloat as a brand. Underneath:

- A Webspinner-ecosystem tenant, deployed Kepler-side using the
  same per-tenant pattern as `~/webspinner-work/kepler/legal/` and
  `~/webspinner-work/kepler/sovereign/`.
- **Registered on Cloudflare, served through Kepler.** The DNS zone
  for `iphloat.com` lives in Cloudflare; the runtime lives on Kepler
  (Mac Studio M4 Max), reachable from the public internet via the
  Cloudflare Tunnel (`com.webspinner.cloudflared`). It is **not a
  Cloudflare Pages site.** It is a Kepler-hosted service whose
  hostname Cloudflare resolves to the tunnel.
- A reference implementation of an *AI-Native commerce experience*
  — cart, checkout, product Q&A, customer support, all woven
  through the Webspinner stack (Studio / WebBook / Commerce / RAG /
  Loom / Wand) rather than bolted on.

## The 100+ tenants horizon

The Wizard has stated explicitly that iPhloat is the first of *over
100 sites* in the ecosystem before the build is done, with prelaunch
work happening now. That means:

- **Decisions you make here become the cookie-cutter** for tenants
  2 through ∞. Default to *boring, predictable, copy-pasteable*
  patterns. If something is interesting, isolate it so it doesn't
  contaminate the template.
- **The deploy shape must be repeatable.** A new tenant should be
  one `cookiecutter` (or scripted) operation away — not a custom
  artisanal stand-up.
- **The apps tier roadmap is the destination.** See
  `~/webspinner-work/ROADMAP.md`. Today's shape (CF DNS → CF Tunnel
  → Kepler) is the **stepping stone**; the destination is a 5-tier
  shape with a presentation server in front of Kepler and a storage
  box for LLM/RAG assets. Don't paint yourself into a corner that
  only works on Kepler.

## Source-of-truth files outside this repo

iPhloat is downstream of the Webspinner grimoire. Always read these
*first* — they will outvote any inference you make from this repo's
code:

| File | Why it's authoritative |
|---|---|
| `~/CLAUDE.md` | Project map for the whole home directory. The "Cross-repo truth" section names tapestry as the spec-of-record. |
| `~/webspinner/tapestry` | **The grimoire.** Section list: `grep -n -E '^=+$\|^[A-Z][A-Z ]{3,40}$' ~/webspinner/tapestry`. |
| `~/webspinner-work/PATTERNS-FOR-CLAUDE.md` | **The cross-repo quality guide.** UX, architecture, tone, defensive coding, deploy hygiene. *Read this before writing patron-facing code.* |
| `~/webspinner-work/ROADMAP.md` | Where the ecosystem is going — apps tier shape, multi-tenant scaling, where iPhloat lands relative to other tenants. |
| `~/webspinner-work/kepler/legal/` | Per-tenant template. The shape iPhloat's deployment will mirror. |
| `~/webspinner-work/kepler/sovereign/` | A more recent / fully-featured tenant (FastAPI + sqlite + chat + WRAG + ledger + Wards). Reference, but it has features iPhloat probably doesn't need. |
| `~/webspinner-sovereign-ai/` | The fork-evolution of the analyzer — current home of the three-loom (Open / Quiet / Hand) work + WRAG design. iPhloat may want to consume Quiet-Loom inference for product Q&A, but **it does not own the LLM stack**. |
| `~/.claude/projects/-Users-johndavidmarx-iPhloat/memory/MEMORY.md` | Auto-memory for *this* project (loads automatically when present; not yet seeded). |

## Boot checklist for a fresh session

1. **Read [`INTENT.md`](INTENT.md) end-to-end.** That's the Wizard's
   own brief. It will outvote anything inferred from code or
   filenames.
2. **Read `~/webspinner-work/PATTERNS-FOR-CLAUDE.md`.** Cross-repo
   quality guide — patron-voice rules, drift discipline, defensive
   UX, deploy hygiene, the E2E-harness rule.
3. **Skim the per-tenant template at `~/webspinner-work/kepler/legal/`**
   to understand the deploy shape iPhloat will mirror. Look at the
   directory layout, the `requirements.txt`, the `app/` module, the
   `deploy/` install script, the `tests/` setup. Don't *copy* it —
   it has features iPhloat doesn't need (the analyzer surface) and
   may be missing things iPhloat does need (commerce).
4. **Skim `~/webspinner-sovereign-ai/CLAUDE.md` + `ARCHITECTURE.md`**
   for the more modern patterns — the per-(loom, model) registry,
   the per-call ledger, the Wards. iPhloat probably doesn't need
   most of this, but the FastAPI + storage shape is the same.
5. **Confirm what's already here.** `git log --oneline` and `ls`. Don't
   assume the directory is empty just because the boot files are
   sparse.
6. **Ask the Wizard for the build brief** if INTENT.md doesn't cover
   what to build *next*. It captures intent at scaffolding-time,
   not implementation priorities.

## Hard rules (these have been earned across the ecosystem)

These rules apply to every change you propose in this repo. They
match the rules in `~/webspinner-sovereign-ai/CLAUDE.md` because
they are *ecosystem-wide* — not per-project conventions:

1. **Webspinner-only branding in patron copy.** Never name the LLM
   provider, the local-model framework, or any third party in
   patron-visible strings. The third-party LLM is "the great loom
   of the world." The local model is "Webspinner's own loom" or
   "your own loom." Technical strings (config, log lines, vendor
   names in code comments) are fine.
2. **Never `export ANTHROPIC_API_KEY` (or any provider key) in
   your shell.** Doing so makes Claude Code itself bill the user's
   Anthropic API account instead of his Code plan. Vault →
   install script → launchd plist only.
3. **No half-finished implementations.** A change either lands
   complete with tests, or it doesn't land. TODOs go in
   `BACKLOG.md`, not in code.
4. **Drift discipline > DRY.** Sibling tenants copy code rather
   than import. Two instances is generalizing prematurely; the
   third is when extraction is allowed. iPhloat is tenant #1;
   the temptation to "factor out" something for tenants 2-100
   should be resisted until you can see what tenants 2 and 3
   *actually* look like.
5. **Tests are not optional.** Every new module gets unit tests;
   every new endpoint goes through a test client. The 200+ tests
   in `~/webspinner-sovereign-ai/service/tests/` are the bar.
6. **Fix root causes, not symptoms.** Failing tests, flaky
   deploys, weird files — they're real signals. Don't
   `--no-verify`, don't add `try/except: pass`, don't rebuild a
   venv to make a Python-version mismatch go away if the
   underlying code is wrong.
7. **Curate docs in the same commit as code.** If you change the
   architecture, the architecture doc moves with it. The README
   is patron-facing and should change rarely; CLAUDE.md / INTENT.md
   / BACKLOG.md change as the work moves.

## Where to find what

| Need | Path |
|---|---|
| Patron-facing site copy | `README.md` (this repo, root) |
| Cross-repo quality guide | `~/webspinner-work/PATTERNS-FOR-CLAUDE.md` |
| Per-tenant template | `~/webspinner-work/kepler/legal/` |
| Cloudflare Tunnel config | `~/webspinner-work/kepler/cloudflared/` |
| Cloudflare API token | `wsvault --raw get webspinner-cf-token` |
| Vault CLI | `~/webspinner-work/kepler/vault/target/release/wsvault` |
| Kepler host | `Johns-Mac-Studio.local` (192.168.1.132); SSH user `johndavidmarx`; reachable via Bonjour as "John's Mac Studio" under `_ssh._tcp.local.` |
| Apps-tier destination shape | `~/webspinner-work/ROADMAP.md` |

## Status

Pre-boot. Repo seeded with the patron-facing `README.md` + Claude
boot files (CLAUDE.md, INTENT.md, BACKLOG.md). No application code
yet. The next session's first task is to take the Wizard's build
brief and turn it into a deployable Kepler tenant.
