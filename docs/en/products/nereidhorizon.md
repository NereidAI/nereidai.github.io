---
title: NereidHorizon
---

# NereidHorizon

Horizon is the operations console for the Open Horizon Management Hub:
the place where the suite defines, signs, and rolls out the edge services,
patterns, and policies that deliver Edge — and the applications and models
built by Forge — to fleets of remote edge nodes.

## What it solves

- Managing Open Horizon edge resources (nodes, services, patterns, policies,
  AgBots, HA groups) by hand against the management hub's raw APIs is slow and
  error-prone; Horizon gives operators one graphical console.
- Open Horizon requires every service deployment configuration to be signed;
  Horizon signs it automatically, so operators never handle signing
  material per service.
- Third parties and sub-organizations need access to edge resources without
  sharing the hub-level credentials; Horizon issues organization-scoped,
  read-only API keys instead.
- Regulated environments need a tamper-evident record of every action against
  the hub; Horizon keeps an append-only audit trail.
- Deployment often happens in air-gapped networks where the console cannot reach
  the internet; Horizon is delivered for offline installation.

## Core capabilities

**Hub resource management**

- Manage edge nodes, service definitions, deployment patterns, deployment
  policies, management policies, Agreement Bots (AgBots), organizations, and
  hub users from one interface.
- High-availability (HA) node groups: configure, manage, and monitor groups,
  memberships, and network configuration.
- Browse public services and patterns across organizations.
- Import services, patterns, and policies from JSON, with interactive handling
  of template variables.

**Deployment and rollout**

- Sign service deployment configurations automatically on create and update.
- Follow assignments through, from services and patterns to the nodes that run
  them, and manage node-side environment variables in place.

**Access and identity**

- Two-layer authentication: local console accounts plus a single, system-level
  connection to the hub shared by all operations.
- Role-based access: a cross-organization administrator role and an
  organization-bound partner role.
- Single sign-on through the suite identity center (Sphere /
  Identity) or a direct OIDC provider.
- Organization-scoped, read-only API keys for third-party integration.

**Operations and security**

- Server-side sessions with credentials encrypted at rest.
- Append-only audit log of every console and API-key action, including the
  actual hub endpoint reached.
- Hardened TLS and security response headers.
- Offline, air-gapped installation from prebuilt images.

## How it fits in the suite

Horizon occupies the distribution hop of the closed loop. Forge
produces versioned models and applications; Horizon publishes them —
together with Edge itself — as Open Horizon service definitions, patterns,
and policies, and the hub's agents roll them out to field nodes. Edge then
runs on those nodes and feeds data back to Link.

- **Forge → Horizon:** versioned artifacts become distributable
  services.
- **Horizon → Edge:** policy-driven rollout of the edge runtime and
  the workloads it hosts. See the [edge delivery guide](../deployment/edge-delivery.md).
- **Sphere / Identity:** in a full suite deployment, operators sign
  in once through Sphere and reach Horizon from the common portal.
  See [SSO & OIDC](../security/sso-oidc.md).
- **Standalone:** Horizon can also run on its own as the hub console.

!!! info "Developer documentation"
    The authoritative, detailed developer documentation for Horizon lives
    in its own repository — see [NereidAI](https://github.com/NereidAI).

## Key facts

| Aspect | Detail |
|---|---|
| What it is | Web operations console for the Open Horizon Management Hub |
| Positioning | Distribution and deployment hop of the closed loop |
| Access model | Single sign-on; cross-organization admin and organization-bound partner roles; read-only partner API keys |
| Deployment | Standalone, or as part of the suite; installs in air-gapped networks |
| Stack | React + Vite front end over an Express / Node.js Backend-For-Frontend, PostgreSQL |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Air-gapped install](../deployment/air-gapped.md)
- [SSO & OIDC](../security/sso-oidc.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
