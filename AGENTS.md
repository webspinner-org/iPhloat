# How Webspinner builds the iPhloat site

The Webspinner approach to building a tenant site is **agentic**.
A brand owner offers three things — *imagery*, *prose*, and a
single sentence of *intent* — and a fleet of cooperating AI
agents takes those three offerings and produces a deployed,
governed, AI-Native site.

iPhloat is the first realization of this fleet.

This document describes the agents at the level of what each one
does for the patron and the brand. The implementation of each
agent lives in the Webspinner ecosystem and is published openly
through the Webspinner Foundation.

## The fleet, at a glance

The fleet works in three phases:

### Build-time agents — run once, when the site is born

Eight cooperating agents take a brand owner's offerings and turn
them into a site:

- **The Reader** parses the brand's prose into structured brand
  data: voice, palette, type system, page outlines, the site
  map, the bannned-phrases list.
- **The Curator** analyzes the imagery the brand provided and
  produces a visual signature — the design language the site
  will speak in.
- **The Researcher** pulls current credible third-party
  knowledge and cites it. The site speaks with authority
  rather than inventing.
- **The Stylist** composes the CSS theme system from the
  brand data and the visual signature. Light and dark themes
  are derived together.
- **The Composer** generates the page HTML for each route in
  the site map.
- **The Indexer** chunks the brand's prose and indexes it so
  the chat panel can answer questions in the brand's voice.
- **The Provisioner** wires the site's domain and hosting.
- **The Scaffolder** generates the per-tenant back-end and
  tests, so every patron-facing surface has a quality gate
  behind it before launch.

### Release-time agents — run before every deploy

Three agents stand at the gate:

- **The Voice Gate** enforces patron-voice rules. The site
  speaks in the brand's voice, never breaks character, never
  exposes implementation details to patrons. Banned phrases
  are blocked. New surfaces fail-closed if their voice drifts.
- **The Auditor** runs technical quality gates: performance,
  accessibility, SEO, security headers. Every patron-facing
  surface clears the audit before it ships.
- **The Retrospective** packages what was built, presents it
  to the brand owner, takes input, iterates. The easy way out
  is forbidden — a build does not declare itself done until
  the brand owner has seen and accepted it.

### Runtime agents — run for every patron interaction

Four agents are awake while patrons use the site:

- **The Weaver** is the chat-side loom. It converses with
  patrons, retrieves grounding from the site's knowledge
  corpus, and composes responses in the brand's voice with
  inline citations.
- **The Cognitive Composer** is the right-panel renderer. It
  generates the single page of Cognitive Content the patron's
  current question warrants. One page. One question. One
  answer.
- **The Dragon Tamer** is the live-update agent. When the
  brand owner offers new material at runtime — a new product
  photo, a revised FAQ, a fresh testimonial — the Dragon
  Tamer re-feeds the corpus and re-trains the loom for the
  affected surfaces, without taking the site down.
- **The Catalog Registrar** registers and updates the tenant
  in the public Webspinner site catalog so the brand can be
  discovered and featured.

## What the patron experiences

The patron sees a coherent site that speaks in the brand's
voice, answers questions on demand, and shows them exactly what
their current question warrants.

The patron does not see the fleet. The fleet's job is to be
invisible to the patron and auditable to the brand. The brand
owns the voice, the corpus, and the visual signature; the
Webspinner ecosystem provides the engine.

## Why this approach

A conventional commerce stack bolts AI on top of a static site.
Webspinner inverts the relationship: the site is built *by* AI,
*for* AI-fluent patrons, with governance and provenance at every
layer.

For the deeper story, see the Webspinner Foundation's public
briefings on AI-Native architecture and the Webspinner Cloud
Security Model.
