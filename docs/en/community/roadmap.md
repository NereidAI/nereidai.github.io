---
title: Roadmap
---

# Roadmap

This page summarizes the **v0.0.1 suite release plan**. It is a living plan:
**dates are not fixed** — phases are entered and exited by **gate criteria**, not by
the calendar. The plan reflected here was last updated 2026-10-11.

!!! note "Status is tracked in the open"
    This page describes the plan as of 2026-10-11. Current status is tracked in the
    [NereidAI GitHub organization](https://github.com/NereidAI) and in Discussions.

## v0.0.1 in one paragraph

v0.0.1 is the first installable snapshot of the edge-to-cloud loop published under
the NereidAI suite. Each repository keeps its own `VERSION` (`v0.0.1` until GA;
build identity `v0.0.1+git<sha>.<date>`). This page tracks the suite-level view.

## Maturity gates

Each product ships at one of three maturity gates:

| Gate | Meaning | Criteria |
|---|---|---|
| **GA** | Production-ready | Air-gapped install verified; API frozen; load/burn-in targets met; docs complete; signed images + SBOM |
| **Preview** | Tryable, not stable | Core flows work end to end; installable; contracts may still change; partial docs |
| **Tech Preview** | Demoable minimal loop | Smallest end-to-end slice; no upgrade or API stability promise |

## Where each product stands

Baseline state as of 2026-10-11:

| Product | Gate | Baseline state |
|---|---|---|
| Link | GA | Feature-complete single binary; its own GA plan exists (`docs/roadmap/ga.md`). |
| Edge | GA | Core bridge and connector governance done; E2E acceptance pending. |
| Forge | Preview | Functionally mature (dataset / train / optimize / export / registry); no GA plan yet. |
| Horizon | Preview | Web UI and BFF under development; MVP scope to be frozen. |
| Sphere | Tech Preview | Empty repository; built from zero. |
| Mobile | Tech Preview | Repository not created; built from zero. |
| Fleet | Tech Preview | Research docs only; no commits. |

!!! warning "Be honest: some products are Tech Preview"
    Sphere, Mobile, and Fleet are at **Tech Preview** — a demoable
    minimal loop with **no upgrade or API stability promise**. Forge and
    Horizon are at **Preview**, so their contracts may still change. Only
    Link and Edge are at **GA**.

## The five phases

Exit each phase only when its gate is met; reordering within a phase is allowed.

1. **Foundation** — Repos, CI, and scaffolding for new products. Link and
   Edge close their P0/P1 items. Forge and Horizon freeze v0.0.1
   scope. Mobile Taro proof-of-concept. Fleet MVP converged from research.
2. **Build** — Main user flows in every product. All cross-product contracts are
   finalized by the end of this phase.
3. **Integration** — Cross-product end-to-end testing; Link/Edge
   wire-contract freeze; load and fault-injection tests for GA products.
4. **Release candidate** — Multi-arch images, SBOM, vulnerability scan, signatures,
   signed offline bundles, full air-gapped install rehearsal, burn-in, docs pass.
5. **Release** — Per-repository GitHub releases; the suite guide goes live with links
   and status badges/levels.

Anything not contract-ready by the end of Build, or not stable by RC, is moved out of
v0.0.1 rather than delaying the phase.

??? note "Cross-product contracts (summary)"
    Contracts must be finalized by the end of the Build phase.

    | Contract | Parties | Status |
    |---|---|---|
    | Gateway wire protocol v1 (topics, frames, catalogs) | Link ↔ Edge | Implemented; freezes before RC |
    | SSO / OIDC federation | Sphere ↔ Keycloak ↔ products | Not started; Sphere integrates Keycloak directly first |
    | Read-only mobile API subset (auth, devices, telemetry, alerts) | Mobile ↔ Link | Not defined |
    | Artifact hand-off (model/app packages → rollout) | Forge → Horizon | Not defined |
    | Edge distribution channel | Horizon → Edge | Horizon is the owner |

## Community edition timing

The community edition of the full edge-to-cloud loop will be **open-sourced by the
end of 2026**; individual modules are released progressively. Open-source timing and
per-repository order remain **open decisions** in the plan and are confirmed before
the release candidate.

## Next steps

- [Community vs Enterprise](community-vs-enterprise.md) — what is open vs commercial.
- [Support](support.md) — where to follow progress and get help.
- [License](license.md) — the Apache-2.0 terms.
