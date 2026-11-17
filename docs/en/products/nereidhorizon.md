---
title: NereidHorizon
---

# NereidHorizon

NereidHorizon is the **delivery depot for your edge fleet**. In one console you
define what software and models should run on which remote sites, and the
platform rolls it out to hundreds or thousands of gateways automatically —
including sites that are completely offline. It is the graphical operations
console for an Open Horizon management hub, so operators never touch raw
hub APIs.

Horizon is built for teams facing these realities:

- "We have gateways in hundreds of locations, and updating them by hand is no
  longer survivable."
- "Many of those sites are air-gapped — there is no internet path to push to."
- "Every deployment needs to be signed, but we cannot hand signing keys to
  every operator."
- "Partners and sub-organizations need limited access without sharing our
  central credentials."
- "Auditors ask who changed what, when, on which node."

## What Horizon helps you do

### Roll software out to an entire fleet from one screen

Manage edge nodes, service definitions, deployment patterns and policies,
management policies, agreement bots, organizations and users in a single
graphical console. Assign a service or pattern and follow it through to the
exact nodes running it, with node-side environment variables editable in
place.

### Deliver to sites that have no internet

Horizon itself is installable fully offline from prebuilt images, and the hub's
agents on remote nodes reconcile toward the declared state autonomously.
Air-gapped sites receive the same policy-driven rollout as connected ones,
just on the local network's schedule.

### Never think about signing keys

Open Horizon requires every service deployment configuration to be signed.
Horizon signs automatically on create and update, so operators work with
normal forms while the cryptographic requirement is satisfied behind the
scenes.

### Give partners access without giving away the keys

Third parties and sub-organizations get organization-scoped, read-only API
keys instead of hub-level credentials. Two built-in roles separate a
cross-organization administrator from an organization-bound partner, and
single sign-on works through [Sphere](nereidsphere.md) /
[Identity](nereididentity.md) or a direct OIDC provider.

### Answer any audit question

Every console and API-key action is recorded in an append-only audit log,
including the actual hub endpoint reached. Server-side sessions keep
credentials encrypted at rest, and hardened TLS plus security response
headers protect the console itself.

### Keep mission-critical sites available

High-availability node groups let you organize, monitor and configure
redundant edge nodes together, including their network settings. Service,
pattern and policy definitions can be imported from JSON with interactive
template variables, and public services can be browsed across organizations.

## From a built model to a thousand sites

1. **Receive the artifact** — models and applications built by
   [NereidForge](nereidforge.md) arrive as versioned packages.
2. **Define the service** — operators describe what should run, on which
   patterns or policies, in the console; JSON import is available for
   repeatable definitions.
3. **Sign automatically** — Horizon signs the deployment configuration on
   save.
4. **Assign and roll out** — the hub's agreement bots negotiate with eligible
   edge nodes, including offline nodes when they next contact the hub.
5. **Observe and reconcile** — follow assignments through to running nodes;
   drift is corrected autonomously.
6. **Hand off to the edge** — [NereidEdge](nereidedge.md) and
   [NereidInference](nereidinference.md) now run on the gateways and begin
   feeding data back to [Link](nereidlink.md).

## Where Horizon sits in the suite

Horizon occupies the distribution hop of the closed loop. Forge produces
versioned models and applications; Horizon publishes them — together with Edge
itself — as Open Horizon service definitions, patterns and policies, and the
hub's agents roll them out to field nodes. Edge then runs on those nodes and
feeds data back to Link.

- **Forge → Horizon:** versioned artifacts become distributable services.
- **Horizon → Edge:** policy-driven rollout of the edge runtime and the
  workloads it hosts. See the [edge delivery guide](../deployment/edge-delivery.md).
- **Sphere / Identity:** in a full suite deployment, operators sign in once
  through Sphere and reach Horizon from the common portal.
  See [SSO & OIDC](../security/sso-oidc.md).
- **Standalone:** Horizon can also run on its own as the hub console.

!!! info "Developer documentation"
    The authoritative, detailed developer documentation for Horizon lives
    in its own repository — see [NereidAI](https://github.com/NereidAI/NereidHorizon).

## Technical overview

This section is for technical evaluators; nothing above it requires edge
operations experience.

| Aspect | Detail |
|---|---|
| What it is | Web operations console for the Open Horizon Management Hub |
| Positioning | Distribution and deployment hop of the closed loop |
| Managed resources | Nodes, services, patterns, deployment and management policies, agreement bots, HA groups, organizations, hub users |
| Signing | Automatic signing of service deployment configurations on create and update |
| Access model | SSO via Sphere/Identity or direct OIDC; cross-organization admin and organization-bound partner roles; read-only partner API keys |
| Audit | Append-only log of every console and API-key action, including the hub endpoint reached |
| High availability | HA node groups with membership and network configuration management |
| Security | Server-side sessions with credentials encrypted at rest, hardened TLS and security headers |
| Offline operation | Air-gapped installation from prebuilt images; autonomous agent reconciliation at disconnected sites |
| Deployment | Standalone, or as part of the suite |
| Stack | React + Vite front end over an Express / Node.js Backend-For-Frontend, PostgreSQL |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI/NereidHorizon)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Air-gapped install](../deployment/air-gapped.md)
- [SSO & OIDC](../security/sso-oidc.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
