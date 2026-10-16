---
title: NereidFactory
---

# NereidFactory

**Smart manufacturing: factory operations and intelligent production.**

NereidFactory is a **commercial industry solution** built on top of the open
NereidAI platform. It targets the manufacturing floor, where AI has to run close to
the line and the data involved should not leave the plant.

!!! note "Commercial solution"
    NereidFactory is licensed, delivered, and supported under a **separate
    commercial agreement**. It is not part of the Apache-2.0 community edition. See
    [Community vs Enterprise](../community/community-vs-enterprise.md).

## Where it plays

Manufacturing is a natural fit for a private, edge-first AIoT platform. Stated
generically, the industry's hardest pressures are the ones the open platform is
already built for:

- **Data that stays on the premises** — production, quality, and process data are
  subject to compliance and internal policy, which rules out many public-cloud
  offerings.
- **Real-time decisions on the line** — results need to be produced where the work
  happens, rather than round-tripped to a distant data center.
- **Heterogeneous field hardware** — line-side devices span many silicon vendors,
  including domestic options, so models have to be optimized and exported for each
  target instead of hand-tuned per project.
- **From pilot to production** — turning a promising demo into daily operation needs
  repeatable pipelines and assets that stay with the organization.

## What it builds on

NereidFactory stands on the open platform rather than restating it. The building
blocks below are the same ones documented for the whole suite:

| Platform building block | Role for a factory solution |
|---|---|
| [Forge](../products/nereidforge.md) | Model factory — datasets, training, quantization, and hardware-targeted export for line-side targets. |
| [Horizon](../products/nereidhorizon.md) | Offline edge distribution — rollout of models and apps to large numbers of line-side nodes. |
| [Edge](../products/nereidedge.md) | On-gateway integration — connects field devices with zero-touch onboarding and mTLS. |
| [Link](../products/nereidlink.md) | Data pipeline — device access, rule engine, alerting, and dashboards. |
| [Sphere](../products/nereidsphere.md) / [Identity](../products/nereididentity.md) | Portal, API gateway, and unified SSO / RBAC across the suite. |

## What we can — and cannot — say here

Because NereidFactory is delivered commercially, its concrete feature set and scope
are **defined per engagement**. This page therefore describes the value proposition
at a high level only; it does not publish a fixed feature list, pricing, or service
levels.

!!! info "Details are per engagement"
    For the specific capabilities, integration surface, delivery plan, and support
    terms that apply to your environment, please
    [reach out](../community/support.md).

## Typical industries

The same private, edge-first pattern applies across heavy manufacturing, discrete
assembly, process industries, and plant operations — anywhere line-side inference
and on-premises data are requirements rather than options. Which parts apply to a
given customer is confirmed per engagement.

## Next steps

- [NereidSentinel](nereidsentinel.md) — video & image analytics
- [NereidMedical](nereidmedical.md) — medical insights
- [All commercial solutions](index.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
