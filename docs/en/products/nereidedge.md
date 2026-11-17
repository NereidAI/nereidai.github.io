---
title: NereidEdge
---

# NereidEdge

NereidEdge is the **field gateway's translator and night watchman**. It sits
next to your machines and cameras, understands their many protocols, and
relays their data back to [NereidLink](nereidlink.md) in one common language.
When the wide-area network is down, it keeps working locally, remembers
everything, and catches up automatically once the link returns — so nothing is
lost and nothing arrives twice.

Edge answers the questions of anyone running equipment across many sites:

- "Our PLCs, cameras and sensors all speak different protocols. Who translates?"
- "The factory's internet link goes down for hours. Do we lose data or control?"
- "We are rolling out hundreds of gateways. Can each one be installed without
  an engineer on site?"
- "How do we make sure every gateway runs the same approved configuration?"
- "What is actually happening at a remote site right now?"

## What Edge helps you do

### Speak every device's language

Edge runs on the field gateway alongside an EdgeX Foundry edge stack and
collects events and readings from southbound device services, then converts
them into the gateway telemetry format Link understands. Field device names
are mapped to the platform's sub-devices, so no per-device cloud integration is
needed.

### Keep working through network outages

Intermittent or absent WAN links are treated as the normal case, not an
emergency. Edge buffers data locally with store-and-forward queues and resumes
from a precise cursor when connectivity returns — no gaps, no duplicates.
Local control and device connections continue while the platform is
unreachable.

### Onboard gateways securely, at scale

Each gateway links to the platform over an authenticated, encrypted
connection driven by declarative configuration. A mandatory handshake
negotiates capabilities at connect time, credentials are mandatory even for
certificate-based authentication, and heartbeats follow the negotiated
schedule. Onboarding a new site becomes repeating a known-good recipe rather
than handcrafting a server.

### Heal configuration drift by itself

Connector definitions — how devices are wired into the platform — are pushed
from the center and applied, updated or removed by Edge. If someone deletes a
device out of band, the next reconciliation repairs it; platform-managed
attributes are cached locally and refreshed on every reconnect, including
deletions. New connector types arrive without changing the wire protocol.

### Report what is happening on site

Edge announces attached devices on their first telemetry, withdraws them on
shutdown, and sends a complete device manifest every five minutes plus a
runtime shadow whenever state changes. Operators in Link always know which
gateways are online and what is connected to them.

### Run on-site inference when an AI runtime is present

Edge itself never touches frames or calls a model. When NereidInference is
installed on the same gateway, Edge can additionally bridge its model
inventory, bindings and status toward the platform — and if no inference
service is present, it behaves exactly as if the feature did not exist,
byte-for-byte.

## How a gateway comes online

1. **Boot** — the Edge service, delivered and versioned by
   [NereidHorizon](nereidhorizon.md), starts on the field gateway.
2. **Handshake** — it authenticates to Link and negotiates features and
   heartbeat limits.
3. **Attach** — field devices are registered automatically as their first
   telemetry arrives.
4. **Run** — readings flow north while commands and connector definitions flow
   south; a local shadow tracks real state.
5. **Endure** — WAN outages are absorbed by local buffering.
6. **Resume** — after reconnection, missed data replays from the cursor and the
   full manifest re-syncs.
7. **Update** — Horizon rolls new service versions and policies out without a
   visit to the site.

## Where Edge sits in the suite

Edge is the southbound edge hop of the closed loop, between field devices and
Link, and it is deployed by Horizon.

- **Devices → Edge:** the edge gateway collects event and reading streams from
  southbound device services.
- **Edge → Link:** telemetry, presence, attributes and shadow flow up;
  commands and connector definitions flow down.
- **Horizon → Edge:** the distribution hop. Horizon publishes the service
  definitions and policies that run Edge on the gateway; Edge carries no
  self-update mechanism.
- **Forge:** the models and applications Edge runs on site are produced by the
  model factory and distributed through Horizon.

!!! info "Developer documentation"

    The authoritative, detailed developer documentation for Edge lives in
    its own repository — see [NereidAI](https://github.com/NereidAI/NereidEdge).

## Technical overview

This section is for technical evaluators; nothing above it requires an edge
computing background.

| Aspect | Detail |
|---|---|
| What it is | Edge agent that connects field devices to Link |
| Positioning | Southbound edge hop of the closed loop |
| Runs on | Field gateways, alongside an EdgeX Foundry 4.0.2 edge stack |
| Service identity | EdgeX application service, service key `nereid-edge`, HTTP port 59750 |
| Northbound | Bridges devices into Link over the MQTT gateway protocol (`v1/gateway/*`), plain or TLS |
| Resilience | Store-and-forward buffering with cursor-based resume; local autonomy while disconnected |
| Lifecycle | Handshake and feature negotiation, heartbeats, five-minute full manifest, device shadow and drift reconciliation |
| Connectors | Declarative, platform-pushed connector definitions with self-healing; extensible without wire-protocol changes |
| Inference | Optional ADR-0039 bridge, double-gated on a static switch and a 30-second presence probe of the inference manager device |
| Distribution | Delivered and updated by Horizon; no self-contained firmware-update mechanism |
| State | Durable state under `/app/data`, encrypted secret copies, stable 32-byte secret key file |
| Stack | Go application service built on the EdgeX App Functions SDK |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI/NereidEdge)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Air-gapped install](../deployment/air-gapped.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
