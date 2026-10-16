---
title: Cross-Product Contracts
---

# Cross-Product Contracts

Products are autonomous, so the only things that bind the suite are explicit
contracts. These are kept small, versioned, and vendor-neutral; a change to one
is a suite-level event, not a local refactor.

## The contracts

| Contract | Parties | What it fixes |
|---|---|---|
| **Gateway wire protocol v1** | Link ↔ Edge | Topics, frames, and catalogs for the southbound gateway link (`v1/gateway/*`): telemetry, attributes, shadow, commands, discovery, OTA. Implemented; frozen before a release candidate. |
| **SSO / OIDC federation** | Sphere ↔ Identity ↔ products | How a browser session becomes a product session: either ticket handoff or a direct OIDC client. See [SSO & OIDC](../security/sso-oidc.md). |
| **Read-only mobile API subset** | Mobile ↔ Link | The narrow read surface a mobile client needs: auth, devices, telemetry, alerts. |
| **Artifact hand-off** | Forge → Horizon | How produced model / application packages become rollout-ready artifacts. |
| **Edge distribution channel** | Horizon → Edge | How Edge itself, apps, and models are delivered and updated. The edge OTA channel is owned by Horizon, not by Edge. |

!!! info "Contract status"
    Contracts are finalized before a release candidate; anything not contract-ready
    is moved out of the release rather than shipped half-defined. Individual
    statuses are tracked in the suite development plan.

## Contract rules

These apply to every contract above and to each product's public API:

- **OpenAPI is the spec.** APIs are described with OpenAPI 3.1, and the spec moves
  in the same change as the code. Specs are validated (they must parse) as part of
  the contract; Sphere and Link both ship an embedded, offline Swagger
  UI so an air-gapped operator can read the contract without a CDN.
- **Empty arrays are `[]`, never `null`.** Clients may rely on the shape.
- **No invented semantics.** The platform never guesses meaning — e.g. units come
  only from user-defined descriptors.
- **Neutral by construction.** Contracts stay protocol-, stack-, and vendor-agnostic.
  No generic interface hard-depends on a specific edge stack or silicon vendor;
  vendor specifics stay inside Forge.
- **Migrations are explicit and reversible.** Schema changes ship as numbered,
  paired up/down migrations — never auto-mutated at startup.
- **i18n moves together.** No hardcoded user-facing strings; new keys land in both
  locales in the same change.

## Repositories

Each product is an independent repository under the NereidAI organization; a
contract change touches the contract document and every affected implementation in
one coordinated change.

- [Product suite overview](../products/index.md)
- [Architecture overview](overview.md)
