# Deployment License

The deployment license is an offline, vendor-signed file that caps what this
platform may host. It is signed with Ed25519; the platform verifies the
signature against its configured public key and never trusts the file's
contents on its own.

## Install a license

Choose the vendor `.json` file (or paste its contents) and install. The file
carries a base64 payload and its detached Ed25519 signature. Installing
replaces the current license immediately; the same file is accepted by the
`nereidlink license` command line, so a deployment can be licensed without a
running console. A license that fails signature verification is rejected and the
current license is kept.

## Fields

- **Status** — Installed, or Not installed.
- **Customer** — the licensed customer.
- **Tenant limit / Current tenants** — how many tenants may exist. Unlimited
  means no cap.
- **Issued at / Expires at** — the validity window.
- **Features** — the licensed feature set; empty means no feature restriction.

## Read-only degradation

When the license is missing, expired, over the tenant or device cap, or the
rollback clock detects tampering, the deployment degrades to **read-only**
instead of stopping:

- no new tenants and no new devices can be created;
- no new device connections are accepted;
- existing devices keep reporting, and existing data stays readable and
  queryable.

A banner on this page shows when the deployment is currently read-only. Import
a valid license to restore full operation; nothing has to be recreated.