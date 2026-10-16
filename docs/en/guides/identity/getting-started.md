# Getting Started with NereidIdentity

NereidIdentity is the suite-wide identity plane: the shared, replaceable single
sign-on (SSO) and access-control centre behind Sphere, Link, Horizon and Forge.
The current engine is Keycloak 26 with a dedicated PostgreSQL, using the
`nereidai` realm. The engine is an implementation detail behind a standard
OIDC/OAuth2 contract, not a portal that users open directly.

!!! tip "You rarely touch Identity directly"
    Identity is a backend service. In the default integration only Sphere speaks
    OIDC to it: users sign in through Sphere, and administrators manage accounts
    from Sphere's account console. A product deployed without the suite may
    instead register its own OIDC client.

## Prerequisites

- A deployed, reachable Identity instance (its issuer URL) and a Sphere portal
  configured against it.
- To sign in: an account in the suite realm, assigned by an administrator.
- To administer accounts: the suite **Administrator** role in Sphere.

## 1. Understand where Identity fits

- **Identity** is the single source of truth for accounts, roles and tokens.
- **Sphere** is the only mandatory OIDC relying party: it drives the browser
  login (authorization-code + PKCE) and hands identity to integrated products,
  by default through a one-time sealed ticket.
- **Products keep their own authorization.** RBAC, tenancy and feature
  permissions live inside each product; a suite identity proves who you are, and
  per-product assignment groups grant entry.

See [SSO & OIDC](../../security/sso-oidc.md) for the full model.

## 2. Sign in as a user

1. Open the Sphere portal and click **Sign in with NereidIdentity**.
2. Enter your credentials on the Identity login page, or choose a brokered
   organization provider (such as Entra ID or Okta) if one is configured.
3. You return to Sphere with a suite session and can open every product you are
   assigned to, without signing in again.

Suite users never sign in to the Keycloak administration console.

## 3. Manage users as an administrator

1. In Sphere, open the user menu and choose **Accounts**.
2. Create users, reset passwords, enable or disable accounts, and assign suite
   roles and per-product tenant/role memberships.
3. Accounts provisioned from an external identity provider are tagged as
   external and are read-only here — manage their lifecycle in that provider.

Sphere performs these operations through a service-account client against the
Identity Admin REST API, so administrators do not need the engine's master
credentials.

## 4. Operate the service

Identity ships as a container image with a Helm chart for the central
deployment and a Docker Compose stack for development. Realms, clients and the
admin service-account grant are provisioned declaratively from the Identity
repository; customer identity systems are always connected behind Identity
through identity brokering, never directly to Sphere or a product.

!!! note "Where the operational detail lives"
    Realm provisioning, client registration, brokered-IdP setup and operational
    runbooks are documented in the NereidIdentity repository
    ([NereidAI](https://github.com/NereidAI)), not in this operator guide.

## Next steps

- [SSO & OIDC](../../security/sso-oidc.md) — modes, tickets and federation.
- [RBAC](../../security/rbac.md) — suite roles and product-local authorization.
- [NereidIdentity product page](../../products/nereididentity.md).
