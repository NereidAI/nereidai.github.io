---
title: Introducing NereidAI, an open, air-gapped edge-AIoT platform
date: 2026-11-20
authors:
  - maintainers
categories:
  - Product updates
slug: introducing-nereidai
---

# Introducing NereidAI, an open, air-gapped edge-AIoT platform

Most AIoT platforms assume a reliable cloud connection, a willingness to ship
operational data off-site, and a single preferred silicon vendor. The sites that
need edge intelligence most — factories, campuses, hospitals, regulated
infrastructure — often cannot accept any of those assumptions. NereidAI exists to
close the device-to-intelligence loop **without** making them.

<!-- more -->

## The problem NereidAI starts from

Edge AI projects tend to stall in the same three places:

1. **Integration debt piles up at the edge.** Every device speaks its own
   protocol, every gateway vendor ships a different SDK, and point-to-point
   integrations multiply with every new line or site.
2. **Models never reach the edge cleanly.** Training happens in one place,
   quantization and hardware targeting somewhere else, and distribution to
   hundreds of remote nodes is a manual, untracked ritual.
3. **Connectivity and data residency are non-negotiable.** The network is
   air-gapped or intermittent, telemetry must stay on the premises, and the
   security team will not approve a mandatory call-home channel.

NereidAI treats all three as platform problems rather than per-project
custom work.

## One suite, one closed loop

The suite is seven Apache-2.0 products that compose into a single edge-to-cloud
loop:

- **NereidEdge** adapts southbound devices and companion services through
  connectors, with zero-touch onboarding and mTLS links.
- **NereidLink** is the privatized data pipeline: multi-protocol device access,
  a rule engine, alerting, dashboards, and gateway lifecycle management.
- **NereidForge** is the multi-silicon model factory — datasets, training,
  evaluation, quantization, and hardware-targeted export.
- **NereidHorizon** distributes models, applications, and firmware to large
  fleets of remote nodes, fully offline.
- **NereidInference** serves the optimized models close to cameras and sensors.
- **NereidSphere** and **NereidIdentity** provide the portal, API gateway,
  unified SSO, RBAC, and federation with the identity systems you already run.

Each product is useful on its own; together they form a loop where edge
telemetry feeds back into training, and new models travel the same proven path
back to the edge. You can read the full picture on the
[suite overview](../../products/index.md) and the
[architecture overview](../../architecture/overview.md).

## Private by design, not by configuration

Privacy here is an architectural property rather than a policy checkbox:

- the platform runs fully air-gapped, with **no mandatory call-home channel**
  and no telemetry that leaves the site;
- every link uses mTLS, every user authenticates once through standard
  OIDC/SAML, and authorization is expressed through a small, stable role model;
- model and data storage stays inside the customer's environment, including on
  S3-compatible object storage operated on-premises;
- multi-vendor silicon is supported through adapter layers, so choosing an
  accelerator never means locking into a single vendor's stack.

The [air-gapped installation guide](../../deployment/air-gapped.md) describes how a
site that never touches the public internet gets signed artifacts, offline
bundles, and a supported rollout.

## Open source, in the open

All seven repositories are published under Apache-2.0 on the
[NereidAI organization](https://github.com/NereidAI) and run on a rolling
development channel today. The community edition covers the complete loop and
is production-usable on its own; the first formally tagged release will add
signed images, per-release SBOMs, and offline bundles through the gates tracked
on the [roadmap](../../community/roadmap.md).

Commercial engagements — enterprise subscriptions, turnkey delivery, and
industry solutions — wrap assurance and services around the *same* codebase,
never a hidden enterprise fork. The next post explains why that distinction
matters: [open core without hidden features](open-core-without-hidden-features.md).

If you are evaluating an edge-AIoT platform for a site where the cloud cannot
reach, start with the [product suite](../../products/index.md) and clone any
repository that looks useful.
