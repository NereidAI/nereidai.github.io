---
title: RBAC
---

# RBAC

NereidAI separates **identity** from **authorization**. The suite identity plane
proves who a user is; each product decides what that user may do. This page
describes the role-based access control model at the level the suite shares.

## Identity vs. authorization

- **The suite supplies identity**: a stable subject, email, display name, and a
  small, coarse set of suite roles (`user`, `operator`, `admin`).
- **Each product owns authorization**: its roles, its permission model, and its
  data scopes are entirely product-local. Products do **not** invent new suite
  role names; they map the coarse suite roles onto their own fine-grained
  permissions.

The identity plane also stores **per-user, per-product tenant and role
assignments** as realm groups shaped `/nereid{product}/{tenant}/{role}`. Products
filter these groups by their own `nereid{product}` prefix — so one account can hold
different tenants and roles in different products.

## Default-deny product access

Access is default-deny and gated at the suite entry point:

- A user with **no assignment group for a product cannot enter it**. Having an
  account only enables signing in to the portal and receiving assignments.
- **Realm administrators** are the exception: they implicitly administer every
  product, so a fresh deployment's bootstrap admin is never locked out.
- **Removing the last assignment** for a product revokes access on the next login,
  because products reconcile their memberships from the groups on every login.
- Products enforce the same boundary on their own callback: they consume only
  their own groups and refuse to issue a session when none is present.

!!! note "Not every account is a product grant"
    The `operator` suite role grants access to the portal's account console but is
    **not** automatically a product grant — operators still need a product group to
    enter a product.

## Tenant-aware access

Multi-tenancy is a product concept, not a cluster boundary. Each product maps the
tenant segment of an assignment group onto its own tenancy model, so access is
scoped to the tenants (and, in some products, the orgs) a user is assigned to. The
identity plane intentionally invents no tenant semantics of its own.

For example, Horizon binds users to Open Horizon **organizations** through
its roles: a cross-org **platform** role, and a **partner** role bound to one org
(with several partner assignments becoming switchable orgs). Other products use
their own tenant shapes — the pattern is the same, the vocabulary is product-local.

## Permission points vs. data scope

A product's RBAC typically answers two separate questions, and enforcing both is
what makes the model sound:

| Question | Decided by | Example |
|---|---|---|
| *What* may this caller do? | **Permission points** attached to a role | create a device, run a command, edit a rule |
| *Which rows* may they reach? | **Data scopes** (tenant / customer / group) | only devices in their assigned group |

Link is a good illustration: permissions decide what a caller can do, while
data scopes decide which rows they can reach, enforced in the store layer on both
reads and writes. This prevents a role that *can* read devices from reaching
devices outside its scope, and it applies to real-time push as well — a restricted
member's wildcard subscription is materialized server-side to the set of devices
they are allowed to see, so pushed frames never cross tenants or exceed
authorization.

## Audit

Authorization decisions and the actions they permit are recorded. Link's
audit log is an **append-only, tamper-evident hash chain** — each entry is linked
to the previous one and anchored with daily seals, enabling online verification
and tamper detection. The distribution console keeps its own append-only audit
trail covering console and API activity, attributing each action to a user or an
API key.

## Account governance

The portal's account console manages identities against the identity plane with a
service-account client: create, enable/disable, reset password, and assign suite
roles. Accounts federated from a brokered customer IdP are shown **read-only** in
the console — their lifecycle (password, MFA, lockout, deprovisioning) is owned by
the customer's identity system.

!!! note "No universal role list"
    The suite shares only the coarse roles above. The concrete role lists —
    tenant admins, engineers, read-only users, platform/partner operators, and so
    on — are defined **per product** and documented with that product.

!!! info "Operations documentation"
    Product-specific role definitions, permission tables, and audit retention
    settings live in each product repository:
    [github.com/NereidAI](https://github.com/NereidAI).

## Related

- [SSO & OIDC](sso-oidc.md) — how identity reaches products.
- [Security overview](index.md) — the full posture.
