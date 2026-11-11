---
title: Roadmap
---

# Roadmap

All seven NereidAI product repositories are **open source on GitHub under
Apache-2.0**, having passed compliance, open-source standard and completeness
review. The code is currently published on a rolling **development (dev)
channel**: there is no tagged release yet. This page tracks maturity and the
path to the first formal release; it is a living plan — phases are entered and
exited by **gate criteria**, not by the calendar.

!!! note "Status is tracked in the open"
    The repositories, issue trackers and Discussions are public. Current work is
    visible in the [NereidAI GitHub organization](https://github.com/NereidAI);
    this page reflects the suite-level view and is updated as gates are met.

## Release channels

| Channel | What you get today | Stability |
|---|---|---|
| **dev (current)** | Rolling source on each repository's default branch, CI-built development images | Moving target; contracts may still change; no upgrade promise |
| **First tagged release (planned)** | Per-repository semantic-version tags, multi-arch images, SBOM, signatures and signed offline bundles, with the commercial and support documentation completed on this site | Gate-controlled; announced when the criteria below pass |

Commercial terms, support SLAs and enterprise deliverables will be documented
when the first formal release is published. Until then, evaluate and integrate
against the dev channel, expecting breaking changes between revisions.

## Maturity gates

Each product ships at one of three maturity gates:

| Gate | Meaning | Criteria |
|---|---|---|
| **GA** | Production-ready | Air-gapped install verified; API frozen; load/burn-in targets met; docs complete; signed images + SBOM |
| **Preview** | Tryable, not stable | Core flows work end to end; installable; contracts may still change; partial docs |
| **Tech Preview** | Demoable minimal loop | Smallest end-to-end slice; no upgrade or API stability promise |

Open-sourcing and maturity are different things: a public repository does not
by itself make a product GA.

## Where each product stands

| Product | Gate | Current state |
|---|---|---|
| Link | GA-track | Feature-complete single binary (and microservices form); gateway wire protocol implemented; own GA plan in its repository. |
| Edge | GA-track | Core bridge and connector governance implemented; end-to-end acceptance in progress. |
| Sphere | Preview | Portal, OIDC login against Identity, gateway and SSO ticket hub implemented and documented. |
| Identity | Preview | Keycloak-compatible realm with declarative realm/client provisioning; brokered IdP support. |
| Forge | Preview | Functionally mature model factory: datasets, annotation, CV and LLM/VLM training, optimization, evaluation, registry and KServe deployment. |
| Horizon | Preview | Management console, BFF and partner API; edge exchange integration under continued development. |
| Inference | Preview | EdgeX 4.0 device service with the generic inference pipeline, model catalog, KServe/OpenAI backends and built-in decoder set; selected camera/server paths live-validated. |

!!! warning "Be honest about maturity"
    Sphere, Identity, Forge, Horizon and Inference are **Preview** — core flows
    work end to end and the services are installable, but contracts may still
    change. Link and Edge are on the GA track but are not tagged GA until the
    release gates pass.

## The path to the first tagged release

Exit each phase only when its gate is met; reordering within a phase is allowed.

1. **Foundation** — Repositories, CI and scaffolding (done: all seven
   product repositories are public with license, notice and contribution files).
2. **Build** — Main user flows in every product; all cross-product contracts
   finalized by the end of this phase.
3. **Integration** — Cross-product end-to-end testing; Link/Edge wire-contract
   freeze; load and fault-injection tests for GA-track products.
4. **Release candidate** — Multi-arch images, SBOM, vulnerability scan,
   signatures, signed offline bundles, full air-gapped install rehearsal,
   burn-in, docs pass.
5. **Release** — Per-repository semantic-version GitHub releases; this site
   adds the commercial, support and enterprise documentation and status
   badges/levels.

Anything not contract-ready by the end of Build, or not stable by RC, is moved
out of the first release rather than delaying the phase.

??? note "Cross-product contracts (summary)"
    Contracts must be finalized by the end of the Build phase.

    | Contract | Parties | Status |
    |---|---|---|
    | Gateway wire protocol v1 (topics, frames, catalogs) | Link ↔ Edge | Implemented; freezes before RC |
    | SSO / OIDC federation | Sphere ↔ Identity ↔ products | Implemented (ticket mode and direct OIDC); documented on this site |
    | Artifact hand-off (model packages → rollout) | Forge → Horizon → Inference | Defined: tar package with `nereid-model.json`, transported via Horizon ESS |
    | Edge distribution channel | Horizon → Edge / Inference | Horizon is the owner |

## Next steps

- [Community vs Enterprise](community-vs-enterprise.md) — what is open vs commercial.
- [Support](support.md) — where to follow progress and get help.
- [License](license.md) — the Apache-2.0 terms.
- [Platform integration](../development/api-integration.md) — how to call the product APIs.
