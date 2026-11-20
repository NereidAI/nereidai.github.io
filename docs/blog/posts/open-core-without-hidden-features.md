---
title: Open core without hidden features, why we sell assurance not keys
date: 2026-11-20
authors:
  - maintainers
categories:
  - Perspectives
slug: open-core-without-hidden-features
---

# Open core without hidden features: why we sell assurance, not keys

"Open core" can mean two very different things. For some vendors it means a
gifted community edition and a second, proprietary enterprise edition whose
real value sits behind a license key. For NereidAI it means something simpler:
**one identical codebase for everyone**, with commercial revenue coming from
assurance and services around that code. This post explains the trade-offs, and
why we think the second model fits air-gapped enterprise software better.

<!-- more -->

## The hidden-feature model has a trust problem

When the interesting capabilities live in a private fork, buyers inherit three
risks:

1. **The community edition is a demo.** Its job is lead generation, not
   production, so self-hosted users constantly hit edges that only money opens.
2. **Audits stop at the source tree.** Regulated customers cannot review code
   they cannot see, yet they are asked to run it next to their most sensitive
   operational data.
3. **The vendor's incentives diverge.** Fixing a bug in the open edition
   competes with selling the closed one, so the free tier stays strategically
   awkward.

NereidAI is built for sites that treat software as a long-lived operational
dependency — factories and fleets expected to run for a decade, not a funding
cycle. Those customers need the open edition to be genuinely complete.

## What "one codebase" actually means

All seven NereidAI products are Apache-2.0, including for commercial, for-profit
production use. There is no enterprise build, no feature flag wired to a
license server, and no private repository behind the public one. The
[community versus enterprise comparison](../../community/community-vs-enterprise.md)
therefore does not describe a feature split; it describes **who operates the
software and what guarantees come with it**.

What a subscription pays for is accountability:

- contractual CVE response times with fixes backported to long-term-support
  versions, rather than best-effort fixes on the current release;
- supported multi-site rollout, HA/DR guidance, and certified hardware and
  accelerator combinations;
- compliance programs for regulated procurement, including audit-ready
  baselines;
- turnkey air-gapped delivery, private training, and a named engineer;
- signed artifacts, per-release SBOMs, and signed offline bundles.

The same capabilities are available to a self-sufficient team for free under
Apache-2.0; the subscription buys the guarantee that someone is responsible for
outcomes, not a key that unlocks hidden functions.

## Why there is no usage-based billing

Cloud SaaS prices naturally drift toward per-call, per-gigabyte, or
per-inference meters. None of those work honestly on an air-gapped platform
with no call-home channel: we have no telemetry, so we cannot meter usage — and
we do not want to.

Charging by volume would also punish exactly the behavior the platform is
designed to encourage: running more inference locally, retaining more data
on-site, and growing the fleet without a per-event tax. Subscriptions are
measured per site, with node-count bands inside a site, and a perpetual
license plus annual maintenance is available for capital-budget procurement.
The full packaging is on the [pricing and purchase page](../../community/pricing.md),
which deliberately publishes no price list — every engagement is scoped and
quoted individually.

## What this means for proofs of concept

Self-service evaluation with the community edition is free at any time. A
vendor-run private proof of concept is different: scoped work against a real
environment, on a customer's premises, is a commercial engagement. Depending on
scope it may be charged separately, bundled into a subscription, or credited
against a later agreement, and the basis is always agreed in writing before
work starts. The same page covers
[custom development](../../solutions/custom-development.md) for teams that want the
maintainers to build connectors, accelerator support, or industry adaptations.

## The commitment we are making

A single public codebase is a discipline, not a slogan. It means every bug
fix, hardening patch, and architectural improvement lands in the repository
anyone can inspect, and the vendor cannot quietly hold capabilities back. If
that model sounds obvious for infrastructure meant to be trusted in isolation,
that is the point — open core should widen the trust boundary, not move it.
