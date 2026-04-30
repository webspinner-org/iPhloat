# iPhloat

**The iPhone case that won't sink.**

Waterproof. Drop-proof. *It floats.*

[![Powered by Webspinner](https://img.shields.io/badge/Powered_by-Webspinner-1e3a8a)](https://webspinner.com)
[![Hosted on Webspinner.Cloud](https://img.shields.io/badge/Hosted_on-Webspinner.Cloud-0891b2)](https://webspinner.cloud)
[![Stewarded by the Webspinner Foundation](https://img.shields.io/badge/Stewarded_by-Webspinner_Foundation-7c3aed)](https://webspinner.org)

---

## About iPhloat

iPhloat is a fully waterproof iPhone case engineered to float face-up when dropped in water. Built for boaters, anglers, paddlers, surfers, kayakers, pool-side parents, dock hands, and anyone who has ever watched their phone disappear beneath the surface.

Whether you're on a lake, at the beach, in a boat, or just clumsy near a pool, iPhloat keeps your phone protected, dry, and visible on the surface.

### Features

- Fully waterproof (IP68 rated to 2m for 30 minutes)
- Positive buoyancy — floats face-up so the screen stays visible
- High-visibility marine-grade trim
- Reinforced corner impact protection
- Crystal-clear back panel preserves the iPhone's design
- MagSafe compatible
- Available for iPhone 14 / 15 / 16 / 17 Pro and Pro Max

---

## About This Repository

This repository contains the public source for the iPhloat brand presence — the marketing site, product pages, promotional content, and shopping cart — all running on the **Webspinner AI-Native Ecosystem**.

This is not a conventional e-commerce stack. Every layer, from content authoring to checkout to customer support, is woven together using Webspinner's local-first, RAG-powered architecture.

### What's in this repo

| Directory | Purpose |
|---|---|
| `/site` | Marketing site (Webspinner WebBook format) |
| `/cart` | Shopping cart and checkout (Webspinner Commerce module) |
| `/content` | Product copy, imagery, and brand assets |
| `/spinners` | Custom Spinners for product Q&A and order lookup |
| `/deploy` | Deployment manifests for Webspinner.Cloud |
| `/studio` | Webspinner Studio configuration and content schema |

---

## Powered by Webspinner

The entire iPhloat customer experience is powered by [Webspinner](https://webspinner.com), an AI-Native ecosystem for content, commerce, and customer engagement.

The site uses these Webspinner modules:

- **Webspinner Studio** — content authoring and brand management
- **Webspinner WebBook** — long-form product storytelling and landing pages
- **Webspinner Commerce** — cart, checkout, and order management
- **Webspinner RAG** — intelligent product Q&A and customer support
- **Webspinner Loom** — orchestration across the stack
- **Webspinner Wand** — directive execution for shopper-facing actions

This site demonstrates what is possible when an entire brand experience is built natively on AI from the ground up rather than bolted on after the fact.

---

## Hosted on Webspinner.Cloud

iPhloat runs on [Webspinner.Cloud](https://webspinner.cloud), Webspinner's managed hosting infrastructure for AI-Native sites and storefronts.

Webspinner.Cloud provides:

- Edge-distributed content delivery
- Built-in vector search and RAG
- Local-first data sovereignty (your data stays yours)
- Zero-ops horizontal scaling
- Native Webspinner Studio integration
- Continuous deployment from this repository

---

## Getting Started

### Run locally

```bash
git clone https://github.com/iphloat/iphloat.git
cd iphloat
webspinner studio open .
```

The Webspinner Studio CLI will boot the local site, hydrate the content from `/content`, and start the local Spinner server on `http://localhost:8088`.

### Deploy

Deployments to Webspinner.Cloud are continuous from `main`. To deploy a preview from a feature branch:

```bash
webspinner cloud deploy --preview
```

See the [Webspinner Studio documentation](https://webspinner.com/docs) for details.

---

## Contributing

iPhloat welcomes contributions from the community. Issues and pull requests should follow the conventions documented in `CONTRIBUTING.md`. All contributors agree to the Webspinner Foundation Contributor License Agreement.

---

## Ownership and License

The iPhloat brand, product, and product imagery are © iPhloat, all rights reserved.

The Webspinner platform code that powers this site is owned and stewarded by the **Webspinner Foundation** and made available under the Webspinner Foundation public license. See [LICENSE](LICENSE) for details.

The site source in this repository is provided as a reference implementation of an AI-Native commerce experience built on Webspinner.

---

## The Webspinner Ecosystem

| Domain | Purpose |
|---|---|
| [webspinner.ai](https://webspinner.ai) | Core product |
| [webspinner.com](https://webspinner.com) | Commercial entity |
| [webspinner.org](https://webspinner.org) | Webspinner Academy — free training and certification |
| [webspinner.cloud](https://webspinner.cloud) | Managed hosting infrastructure |
| [webspinner.store](https://webspinner.store) | Template and extension marketplace |
| [webspinner.app](https://webspinner.app) | App marketplace |
| [webspinner.tech](https://webspinner.tech) | Developer resources |
| [webspinner.studio](https://webspinner.studio) | Webspinner Studio (product alias) |

---

## Contact

All contact, support, press, and ordering is handled through authenticated forms on the site. We do not publish email addresses in scrapeable surfaces.

- Web: [iphloat.com](https://iphloat.com)
- Account: [iphloat.com/account](https://iphloat.com/account) — register or sign in
- Orders: [iphloat.com/order](https://iphloat.com/order) — place or track an order
- Support: [iphloat.com/support](https://iphloat.com/support) — open a support ticket
- Press: [iphloat.com/press](https://iphloat.com/press) — submit a press inquiry

---

*Built with Webspinner. Hosted on Webspinner.Cloud. Stewarded by the Webspinner Foundation.*
