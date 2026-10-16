# Getting Started with NereidSphere

NereidSphere is the thin suite layer: one portal, a single sign-on (SSO) entry
point and a unified API gateway, with no product business logic of its own.
This guide walks an operator through the first run — open the portal, sign in,
enter an integrated product, manage accounts, and sign out.

!!! tip "Optional, not required"
    Every product works standalone with its own login. Sphere and Identity only
    come into play when you want one portal and one login across the suite. Edge
    is never a central portal entry — it runs independently at each edge site.

## Prerequisites

- A deployed Sphere instance and its portal URL.
- In the default OIDC mode, a reachable Identity service and an account assigned
  to you in the suite realm by an administrator.
- One or more integrated products (Forge, Horizon, Link) reachable from your
  browser.

## 1. Open the portal and sign in

1. Browse to the Sphere portal; unauthenticated visitors land on the login page.
2. In the default OIDC mode, click **Sign in with NereidIdentity**. Your browser
   is redirected to Identity over the authorization-code + PKCE flow; enter your
   organization credentials there. Sphere never sees the password.
3. On return, Sphere establishes the encrypted `ns_session` cookie and opens the
   portal. On an emergency `auth.mode=local` deployment, use the explicitly
   labeled **Emergency access** form instead.

Full flow and error messages: [Signing In](sso-login.md).

## 2. Take the portal tour

The product grid lists the integrated products in closed-loop order —
Forge → Horizon → Link — and your display name and suite roles are shown after
login. See [NereidSphere Overview](portal-overview.md).

## 3. Jump into a product

1. Click a product card; the portal always enters through
   `/auth/enter/{product}`.
2. In the default ticket mode (`ns`), Sphere mints a 30-second, single-use,
   audience-bound sealed ticket; the product exchanges it server to server for
   your verified identity and opens its own session — no second login.
3. In direct-OIDC mode (`oidc`), the product is itself an Identity client and
   entry is seamless through the existing SSO session.

See [Opening Products with SSO](product-sso.md). Only exact, configured product
origins are accepted as post-login redirects, which prevents open redirects.

## 4. Manage accounts (administrators)

Open the user menu → **Accounts** (available in OIDC mode only). Administrators
create accounts, reset passwords, enable or disable users, assign
`User`/`Operator`/`Administrator` suite roles, and set each account's
per-product tenant and role. Operators have read-only access; accounts
federated from an external provider are read-only here and must be managed in
that provider. Sphere never uses the identity engine's own master console. See
[Account Management](admin-users.md).

## 5. Sign out

Open the user menu in the header (top-right avatar) and choose **Sign out**.
Sphere clears the session cookie and, in OIDC mode, continues to the Identity
logout page before returning to the portal. Products that established their own
local sessions may require a separate logout. See
[Session and Logout](session-and-logout.md).

## Troubleshooting

Login loops, rejected redirects and appearing signed out on every request are
usually a Sphere/product mode mismatch, an unregistered redirect origin, or
cookies being blocked. Start with [Troubleshooting](troubleshooting.md).

## Next steps

- [SSO & OIDC](../../security/sso-oidc.md) — the two integration modes.
- [NereidSphere product page](../../products/nereidsphere.md).
