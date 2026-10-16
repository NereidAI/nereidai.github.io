---
title: Security
---

# Security

Security and operability are first-class concerns in NereidAI, not bolt-ons. The
platform is designed to run with no internet access and to keep every byte inside
the customer perimeter.

## Posture

| Capability | Status |
|---|---|
| Air-gapped / offline installation (full image bundles, no internet required) | Available |
| No mandatory call-home; data stays inside the customer perimeter | Available |
| mTLS service-to-service and device-to-platform links | Available |
| Unified SSO and centralized RBAC across all suite products (Identity) | Available |
| Signed release artifacts and per-release SBOM | Planned |
| Enterprise SLA on CVE response and backported fixes | Commercial contract |
| Compliance baselines (e.g. 等保 2.0) and local-OS / accelerator certifications | Per-engagement roadmap |

## Defense in depth

The suite layers several independent controls rather than relying on a single
gate:

- **Network isolation.** Products run with no runtime internet dependency and no
  mandatory call-home; a privatized build pulls only from internal mirrors and a
  private registry. See [Air-Gapped Install](../deployment/air-gapped.md).
- **Transport integrity.** Service-to-service and device-to-platform traffic is
  protected with mTLS. Field links between edge gateways and the platform use
  outbound-only mTLS with store-and-forward buffering.
- **Identity.** A single suite-wide identity plane is the source
  of truth; the portal never stores users. See [SSO & OIDC](sso-oidc.md).
- **Authorization.** Access is default-deny: identity proves *who* you are, and
  product-local RBAC decides *what* you can do and *which rows* you can reach. See
  [RBAC](rbac.md).
- **Secrets and data at rest.** Tenant secrets and stored credentials are
  encrypted at rest under a key kept outside the database; plaintext is restored
  only where it is truly needed.
- **Integrity and provenance.** Audit records form an append-only, tamper-evident
  chain; deployments published to the field are signed. Signed release artifacts
  and a per-release SBOM are on the roadmap.

!!! note "Zero trust between services"
    Products never reach into one another's data stores. Products communicate over
    their documented APIs and a message backbone, and the suite layer carries no
    domain logic — so there is no shared database that would widen the blast
    radius.

## Identity and access

Two suite services own the security plane, and both are optional for a
single-product deployment:

- **Identity** — the suite authentication and identity center: single
  sign-on across every product, OIDC / LDAP / SAML federation, coarse suite roles,
  token issuance, and tenant-aware access governance. The identity engine is
  replaceable: any OIDC/OAuth2-compliant engine that satisfies the published
  contract can take its place.
- **Sphere** — the suite portal and the **only** component that speaks OIDC
  to the identity plane. It hands verified identity to products and never sees or
  stores their passwords.

A detailed walkthrough of the two product integration modes is in
[SSO & OIDC](sso-oidc.md); the role and tenant model is in [RBAC](rbac.md).

## Product-level controls

Domain products contribute their own hardened controls on top of the suite
baseline, for example:

- a **built-in certificate authority** issuing device certificates, with mTLS and
  certificate-revocation checks for device authentication;
- **multi-factor authentication** with recovery codes, login lockout, and
  per-session revocation;
- **step-up confirmation** for dangerous operations, with machine identities
  refused;
- **device quarantine** on credential compromise or anomalous traffic, preserving
  identity and time-series data.

!!! info "Operations documentation"
    Deployment hardening checklists and operational security detail live in each
    product repository: [github.com/NereidAI](https://github.com/NereidAI).

## Related

- [SSO & OIDC](sso-oidc.md) — the suite single sign-on model.
- [RBAC](rbac.md) — role-based access control and tenant scope.
- [Air-Gapped Install](../deployment/air-gapped.md) — the offline posture.
