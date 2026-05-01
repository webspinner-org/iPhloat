# iPhloat — repository orientation

This repository contains the public source of the iPhloat brand
site — the marketing pages, the chat panel, the Cognitive Content
surfaces, and the patron-facing storefront — all running on the
Webspinner AI-Native ecosystem.

## What iPhloat is

A fully waterproof iPhone case engineered to float face-up when
dropped in water. Designed for boaters, anglers, paddlers,
surfers, kayakers, pool-side parents, dock hands, and anyone who
has ever watched their phone disappear beneath the surface. See
[`README.md`](README.md) for the patron-facing product story.

## What this site demonstrates

iPhloat is the first realization of the Webspinner *One Sentence
Website* capability — the ability to take three offerings from
a brand owner (imagery, prose, and a single sentence of intent)
and produce a deployed, governed, AI-Native site. The same
capability will produce sites for many tenants over time;
iPhloat is the public reference implementation.

## Where to read more

- [`README.md`](README.md) — what iPhloat the product is.
- [`AI-NATIVE.md`](AI-NATIVE.md) — what AI-Native means in
  practice and what it changes for patrons.
- [`HOW-WEBSPINNER-WORKS.md`](HOW-WEBSPINNER-WORKS.md) — the
  Webspinner ecosystem explained in plain language.
- [`AGENTS.md`](AGENTS.md) — the agent fleet that builds and
  runs Webspinner sites, described at the level of what each
  agent does for the patron.
- [`INTENT.md`](INTENT.md) — the product and site intent.

## Hard rules for any change in this repo

1. **Brand voice is consistent.** Patron-facing copy speaks in
   the iPhloat brand's voice. Where the patron experience
   references the AI behind the site, the language is
   Webspinner-native: "the loom," "the patron," "the Cognitive
   Content," "the brand's voice."
2. **Tests are not optional.** Every patron-facing surface
   ships behind tests that exercise it end-to-end.
3. **Curate docs alongside code.** When the architecture moves,
   the patron-facing docs in this repository move with it.
4. **No hard-coded tenant identity.** Tenant identity is a
   runtime parameter; nothing in shared code paths assumes
   "iPhloat" as a literal value.
