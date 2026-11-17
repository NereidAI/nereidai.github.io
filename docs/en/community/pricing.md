---
title: Pricing & Purchase
---

# Pricing & Purchase

NereidAI follows an open-core model with **one codebase, no hidden features**.
All seven products are open source under Apache-2.0 and free to run in
production, including commercial use. What you can pay for is assurance,
scale governance and delivery services around that same software — plus
industry solutions built on top of it.

This page explains what is free, what is sold, how it is packaged, and how to
buy. There is no public price list: every commercial engagement is scoped and
quoted individually. For any inquiry, email
[jiekechoo@gmail.com](mailto:jiekechoo@gmail.com).

## Three ways to engage

| Layer | What it is | How you pay |
|---|---|---|
| **Community edition** | The seven Apache-2.0 repositories: the complete edge-to-cloud loop, self-deployed, community support with no SLA | Free, forever |
| **Enterprise subscription** | The same software, plus LTS releases, contractual CVE response, multi-site governance, HA/DR guidance, compliance support, turnkey delivery and a named engineer | Annual subscription, or a perpetual license plus annual maintenance |
| **Industry solutions** | NereidFactory, NereidSentinel and NereidMedical: domain products composed on top of the open platform | Per-project agreement, usually including the first-year subscription |

## What is free, and what you pay for

Because the code is identical, the difference is **not** which features exist
but who operates them and what guarantees come with them.

| Capability | Community edition | Enterprise subscription |
|---|---|---|
| All seven products, full edge-to-cloud loop | Self-service, free | Same software, vendor-supported |
| Edge connectors and NPU adapter plugins | Included | Same, with vendor-backed integration support |
| Single-site Link / Forge / Horizon | Included | Multi-site federated operation, certified hardware/accelerator combinations, supported rollout with LTS |
| Sphere + Identity multi-tenant control plane | Included, self-configured | Unified identity and cross-product governance designed and supported with the vendor |
| External IdP federation (OIDC / LDAP / SAML), SCIM | Included, self-configured | Enterprise IAM integration and automated user-lifecycle delivery |
| High availability and disaster recovery | You build and operate it | Reference architectures, HA/DR guidance and supported large-scale rollout policy |
| Audit, hardening, compliance baselines (MLPS / 等保 etc.) | Tooling included; you run the program | Compliance and audit readiness for regulated industries and SOE / multinational procurement |
| Signed artifacts and per-release SBOM | From the first tagged release | Plus signed offline bundles and enterprise supply-chain workflows |
| CVE response and fixes | Best effort, current release | Contractual response SLA with fixes backported to LTS versions |
| Air-gapped delivery, private POC, training | Self-service | Turnkey on-premises delivery, scoped private POC and knowledge transfer |
| Support channel | GitHub issues / Discussions, no SLA | 7×24 LTS support with a named engineer |

## How commercial offerings are packaged

### Subscription tiers

Enterprise subscriptions are offered in two packaged tiers; the exact
entitlements are confirmed per engagement:

- **Standard** — single-site production, LTS updates, business-hours support,
  turnkey air-gapped delivery and a scoped private POC (a vendor-run POC is a
  commercial engagement and may be chargeable depending on scope).
- **Enterprise** — multi-site federated operation, HA/DR and compliance
  support, 7×24 response with a named engineer, and supply-chain workflows
  such as signed offline bundles.

### How subscriptions are measured

- **Per site, per year** — the primary unit is a customer site (factory,
  campus or datacenter), with node-count bands inside each site so smaller
  deployments start smaller.
- **Perpetual alternative** — organizations that procure through capital
  budgets can buy a perpetual license plus an annual maintenance fee
  covering updates and SLA.
- **Industry solutions** — scoped per project under a statement of work,
  typically bundling the first year of platform subscription.

### What we deliberately do not charge for

There is **no usage-based billing**: no per-API-call, per-inference,
per-training-job or per-gigabyte charges. The platform is built for air-gapped
environments with no call-home channel, so we neither can nor want to meter
your business data. Your volume growth does not silently increase your bill.

## How to buy

1. **Email** [jiekechoo@gmail.com](mailto:jiekechoo@gmail.com) describing
   your scenario — sites, approximate device or gateway count, and the
   outcomes you need.
2. **Requirements discussion** — scope, deployment topology, compliance and
   procurement constraints.
3. **Private POC proposal** — an on-premises proof of concept where useful,
   with agreed success criteria. POCs are scoped per engagement and may be
   chargeable depending on effort and environment; the basis is stated in the
   proposal before any work starts.
4. **Quote and agreement** — tier, measurement unit (subscription or
   perpetual), delivery and support terms.
5. **Delivery and enablement** — turnkey air-gapped installation, integration
   and private training.
6. **Renewal** — LTS updates and SLA continue with the annual subscription or
   maintenance fee.

!!! note "Current stage"
    The code is open now on a rolling development channel. Commercial terms,
    SLAs and enterprise deliverables take effect with the first formally
    tagged release; inquiry and POC discussions are open in the meantime.

## Frequently asked questions

**Can I use the community edition in a commercial, for-profit deployment?**
Yes. Apache-2.0 permits commercial use, modification and redistribution. The
community edition is a complete, production-usable platform, not a crippled
trial.

**If all the code is open, what am I paying for?**
Operational assurance and accountability: contractual response times, fixes
backported to long-term-support versions, supported multi-site and HA/DR
rollout, compliance programs, turnkey offline delivery, training and a named
engineer. You buy the guarantee that someone is responsible, not a key to
hidden features.

**Do you charge by API calls, data volume or inference count?**
No. The platform runs privately with no mandatory call-home, and usage is not
metered. Charges are based on sites, service tiers and project scope.

**Is there a public price list?**
No. Requirements, site counts, hardware combinations and compliance scope vary
widely in air-gapped enterprise deployments, so each engagement is quoted
individually. Email [jiekechoo@gmail.com](mailto:jiekechoo@gmail.com) for an
estimate.

**Can we start a purchase or POC before the first formal release?**
Inquiry and POC discussions can start now; signed commercial terms and SLAs
take effect with the first tagged release.

**Is a proof of concept free?**
Not automatically. Self-service evaluation using the community edition is
free at any time. A vendor-run private POC — scoped work on your premises or
against your environment — is a commercial engagement: depending on scope it
may be charged separately, bundled into a subscription, or credited against a
later agreement. The basis is always agreed in writing beforehand.

**How do NereidFactory, NereidSentinel and NereidMedical fit in?**
They are commercial industry solutions built on top of the open platform,
each delivered under a separate project agreement. See
[Commercial Industry Solutions](../solutions/index.md).

**Can you build integrations or adaptations for us?**
Yes — vendor-run custom development (device/connector integration, multi-vendor
silicon/NPU acceleration, industry-specific adaptation) is scoped per project
under a statement of work and quoted individually. Extending the platform
yourself stays free under Apache-2.0. See
[Custom Development](../solutions/custom-development.md).

## Next steps

- [Community vs Enterprise](community-vs-enterprise.md) — the detailed capability comparison.
- [License & Support](license.md) — Apache-2.0 terms and commercial options.
- [Support](support.md) — community channels and commercial support.
- [Commercial Industry Solutions](../solutions/index.md) — domain products on top of the platform.
