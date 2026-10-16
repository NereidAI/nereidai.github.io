---
title: NereidEdge
---

# NereidEdge

Edge is the edge agent that connects field devices to Link; it runs
on field gateways and is delivered and kept current by Horizon.

## What it solves

- Field devices and sensors speak many southbound protocols; Edge brings
  them into Link without per-device cloud integration.
- Edge sites sit behind flaky or absent WAN links; local buffering and autonomy
  keep data and control working while the platform is unreachable.
- Onboarding large numbers of gateways must be repeatable and secure; gateways
  link to Link over a secure connection driven by declarative
  configuration from the platform.
- Keeping the edge runtime and its configuration consistent across a fleet is an
  operations problem; Horizon owns distribution and update, while
  Edge reconciles its declared state.
- Operators need visibility of gateways and their attached devices; Edge
  reports presence, device state, and a periodic manifest.

## Core capabilities

**Device integration**

- Telemetry bridge: turns field events and readings into Link's gateway
  telemetry.
- Device mapping: relates field device names to Link sub-devices.
- Lifecycle management: attaches devices on first telemetry, detaches them on
  shutdown, and sends a full device manifest at a regular interval.
- Runs alongside an EdgeX Foundry edge stack on the gateway.

**Gateway behaviour**

- Mandatory handshake and feature negotiation at connect time.
- Periodic heartbeat, aligned with the limits agreed during negotiation.
- Platform-managed device attributes cached locally and refreshed on every
  reconnect, with deletions honoured.
- Device shadow: reports the gateway's real runtime state on connect and on
  change.
- Gateway-level settings applied live from the platform.

**Declarative connectors**

- Connector definitions are pushed by the platform; Edge applies, updates,
  and deletes them, reports status, and self-heals removed devices.
- New connector types are added without changing the platform or the wire
  protocol; a node-level export connector is on the roadmap.

**Resilience**

- Secure MQTT transport to Link over plain or TLS connections.
- Designed for disconnected operation: store-and-forward buffering and
  cursor-based resume so an intermittent WAN does not lose data.
- Health and observability built in.

## How it fits in the suite

Edge is the southbound edge hop of the closed loop, between the field
devices and Link, and it is deployed by Horizon.

- **Devices → Edge:** the edge gateway collects event and reading streams
  from southbound device services.
- **Edge → Link:** telemetry, presence, attributes, and shadow flow
  up; commands and connector definitions flow down.
- **Horizon → Edge:** the distribution hop. Horizon publishes
  the service definitions and policies that run Edge on the gateway;
  Edge does not carry its own firmware-update mechanism.
- **Forge:** the models and applications Edge runs on site are
  produced by the model factory and distributed through Horizon.

!!! info "Developer documentation"
    The authoritative, detailed developer documentation for Edge lives in
    its own repository — see [NereidAI](https://github.com/NereidAI).

## Key facts

| Aspect | Detail |
|---|---|
| What it is | Edge agent that connects field devices to Link |
| Positioning | Southbound edge hop of the closed loop |
| Runs on | Field gateways, alongside an EdgeX Foundry edge stack |
| Northbound | Bridges devices into Link over an MQTT gateway protocol |
| Distribution | Delivered and updated by Horizon |
| Stack | Go application service built on EdgeX Foundry |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Air-gapped install](../deployment/air-gapped.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
