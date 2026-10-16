---
title: Community vs Enterprise
---

# Community vs Enterprise

The community edition covers the complete edge-to-cloud loop and can be used in
production on its own. Enterprise capabilities cover the procurement, operations,
and compliance needs of large organizations.

The table below reproduces the capability comparison from the NereidAI project
overview.

| Capability | Community | Enterprise value |
|---|---|---|
| Edge connectors & NPU adapter plugins | ✓ | Same capabilities, with vendor-backed integration support |
| Link / Forge / Horizon, single-site | ✓ | Multi-site scale — federated operation across many sites, certified hardware/accelerator combinations, and vendor-supported rollout with LTS |
| Sphere + Identity multi-tenant control plane | — | Unified identity and cross-product governance — one login, one portal, consistent tenants and policies across the suite |
| Identity external IdP federation (OIDC / LDAP / SAML) and SCIM provisioning | — | Enterprise IAM integration — connect to an existing directory and automate user lifecycle management |
| High availability, disaster recovery, large-scale rollout policy | — | Scale and resilience — fleet-wide rollouts with HA/DR for sites that cannot tolerate downtime |
| Audit, hardening, compliance baselines (等保 / MLPS etc.) | — | Compliance and audit readiness for regulated industries and SOE / multinational procurement |
| Signed release artifacts and per-release SBOM | ✓ | Plus signed offline bundles and enterprise supply-chain workflows |
| CVE response SLA and backported fixes | — | Contractual response commitment with fixes backported to LTS versions |
| Air-gapped delivery, private POC, training | self-service | Turnkey delivery and knowledge transfer on the customer's premises |
| Support | GitHub issues / Discussions (community only, no SLA) | 7×24 LTS with a named engineer |

## How to read this table

- A **✓** in the Community column means the capability is available in the
  Apache-2.0 community edition; a **—** means it is a commercial capability.
- "Community" is not a crippled edition. The community edition is a complete,
  production-usable edge-to-cloud loop. Enterprise value is about **scale,
  governance, and assurance** — running many sites, meeting procurement and audit
  requirements, and getting contractual commitments.
- The **self-service** entry for air-gapped delivery means the community edition
  supports it, while commercial terms add turnkey delivery and knowledge transfer.

## Security & delivery posture

The same posture work that underpins the community edition also determines what is
planned or commercial. From the project overview:

| Capability | Status |
|---|---|
| Air-gapped / offline installation (full image bundles, no internet required) | Available |
| No mandatory call-home; data stays inside the customer perimeter | Available |
| mTLS service-to-service and device-to-platform links | Available |
| Unified SSO and centralized RBAC across all suite products (Identity) | Available |
| Signed release artifacts and per-release SBOM | Planned |
| Enterprise SLA on CVE response and backported fixes | Commercial contract |
| Compliance baselines (e.g. 等保 2.0) and local-OS / accelerator certifications | Per-engagement roadmap |

## Next steps

- [License & Support](license.md) — Apache-2.0 and commercial options.
- [Roadmap](roadmap.md) — maturity gates and phases.
- [Commercial Industry Solutions](../solutions/index.md).
