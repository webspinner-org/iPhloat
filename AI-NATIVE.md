# AI-Native — How iPhloat is Built

iPhloat is the first public showcase of the **Webspinner AI-Native approach** — the architecture that powers every site woven through Webspinner Studio. The pages you visit on iphloat.com are not static documents stamped out of a template. They are **Cognitive Content™**: web pages composed at the moment of a patron's visit from embeddings, prose, and a loom assigned to this site alone.

## What Cognitive Content Means

A traditional website is a stack of files. A Webspinner site is a stack of *understanding*. Three things go into Studio when a Webspinner site is born:

- **Imagery.** The photographs, illustrations, and brand assets that carry the site's visual voice.
- **Prose.** A document the site's owner authors with care — the substance of the brand, the tone, the things a patron must know.
- **Intent.** The site's purpose, declared plainly. What does this site exist to do?

Studio takes these three and weaves them into a corpus of embeddings — the **WRAG** — bound to a loom assigned to the site. From that union, every page on the site is rendered. Not as a fixed template waiting to be filled, but as content the loom composes in service of the patron in front of it.

## Build A Better Web — The Promise Made Visible

iPhloat is, in part, a brand site for a waterproof iPhone case. It is also the showcase implementation of what Webspinner means when it says *Build A Better Web*. Visit iphloat.com and you will find a chat window. That chat is not an afterthought bolted onto a marketing page. It is the same loom that composes the rest of the site, opened for the patron to converse with directly. Ask whether iPhloat fits an iPhone 17 Pro Max in a kayak. Ask which colorway is most visible on the surface of green lake water. Ask what happens if the case takes a hard drop on a dock. The answer is woven from the site's own corpus, in the site's own voice.

Every Webspinner site offers this experience. It is the standard, not a feature.

## How a Webspinner Site Comes Online

A Webspinner site is not deployed on the day it is authored. It moves through a deliberate sequence:

1. **Authoring.** The owner brings imagery, prose, and intent into Studio.
2. **Training.** The site is brought up under Webspinner's care. The WRAG is tuned. The assigned loom is calibrated against the corpus. The chat is exercised. This continues until the site performs at a level fit for client consumption.
3. **Quality Gating.** Webspinner runs an AI-Native CI/CD pipeline whose Quality Gates are automatic. The **Webspinner Weaver** facilitates the Release Gating process — patron-facing surfaces are checked for fitness, the chat is exercised against the corpus, coverage is verified, regressions are caught. A site that fails its gates does not move forward.
4. **Release.** Only once platform readiness is assured does a site go live. Development surfaces — preview tooling, Studio overlays, internal endpoints — are not exposed on the patron-facing site until every client-facing surface has cleared its gates.

This is a Platform Engineering discipline, AI-Native end to end. Deploy is the end of the gating, not the start of the patron's experience.

Webspinner names this discipline **AI Native SDLC**, and its day-to-day rhythm **AI Native Agile**. The build is iterative and interactive. When the author's input is needed, the loom holds a *retrospective* — it presents what has been built, takes the author's response, and iterates. The easy way out is forbidden. Progress is always visible to the author; the system never goes silent. And the loom that drives the build is sophisticated enough to do exemplary work — drawing on current credible third-party sources, with citations, rather than on stale model training alone. When a choice arises, the loom commits to a single recommendation rather than interviewing the author with a list of questions; the author is free to refine or override, but the loom takes a position.

## Sovereign AI — The Substrate

Webspinner sites do not run on the loom of the moment. They run on looms curated through the **Webspinner Sovereign AI** approaches — a deliberate, governed set of looms whose provenance, behavior, and economics are understood. The selection criteria, the local-first defaults, and the tradeoffs are documented on the Webspinner Sovereign AI app. Every Webspinner site inherits from that substrate.

## Where a Webspinner Site Can Live

A Webspinner site has two homes available to it:

- **Hosted on Webspinner.Cloud.** Most sites stay here. Hosting on Webspinner.Cloud is **$25 per year** for most sites. Additional costs may apply when a site reaches into territory that affects the underlying cost model — third-party loom access via MCP, shopping carts with credit-card adjudication, or storage and traffic volumes beyond the standard envelope. These are documented per site and never surprise the patron.
- **Extracted for the client to host elsewhere.** A Webspinner site can be **extracted** from the platform for **$5**, as a one-time operation, with no ongoing dependency on Webspinner.Cloud's WRAG or local looms. After extraction, the site is the client's to operate as they choose. This is a deliberate posture on Webspinner's part: a Webspinner site is never a hostage of the platform that birthed it.

## Webspinner.Cloud — A Private Cloud, Stewarded

Webspinner.Cloud is a **private cloud infrastructure**, owned and stewarded by the **Webspinner Foundation**. The Foundation will not sell the Cloud to a public corporation. The Cloud will not become a vehicle for shareholder extraction. It exists to serve the patrons of the sites that live on it, in accordance with the values the Foundation was constituted to uphold.

Detail on Webspinner.Cloud's surface and capabilities is forthcoming as the platform reaches public release. iPhloat is among the first sites to live on it, and its operation is part of how the Cloud earns the trust of the hundred-plus tenants still to come.

---

*iPhloat is the first public realization of the Webspinner AI-Native approach. It is also a real product sold to real patrons, who deserve the same quality from a Cognitive Content site that they deserve from any other site they spend their money on. That alignment — the promise of "Build A Better Web" meeting the obligation of "this had better work" — is the bar Webspinner has set for itself, and for every site that follows.*
