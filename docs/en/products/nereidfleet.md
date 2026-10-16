---
title: NereidFleet
---

# NereidFleet

Fleet is a management, control, and collaboration platform for embodied-AI
robot fleets — wheeled, quadruped, humanoid, and balancing robots — built on an
open stack of ROS 2, Eclipse Zenoh, Open-RMF, and EdgeX Foundry.

!!! warning "Tech Preview"
    Fleet is at an early design stage (v0.1 draft). The repository is
    currently design documents and research; the implementation follows the
    phased PoC route below. Treat these capabilities as the target design, not
    shipped features.

## What it solves

- Closed fleet platforms lock operators into one vendor and one robot shape;
  Fleet aims to unify management, control, and collaboration over an open
  stack instead.
- Heterogeneous robots (wheeled AMRs, quadrupeds, humanoids, balancing vehicles)
  expose different control surfaces; Fleet abstracts them behind a single
  unified fleet, robot, task, and capability model.
- Mixing real-time control with platform traffic is a source of jitter and
  fragility; Fleet separates the real-time control domain from the
  management and telemetry domain.
- Sites lose connectivity; edge autonomy must let robots and the edge tier keep
  operating safely while the platform is unreachable.
- Adopting a platform must not force replacing vehicle-side middleware;
  Fleet bridges existing ROS 2 robots rather than intruding on them.

## Core capabilities

**Management**

- Asset ledger, fleet grouping, and edge-node management.
- Maps, permissions, and audit.

**Control**

- Single-robot teleoperation and emergency stop.
- Safety-mode switching.
- Real-time state and telemetry.

**Collaboration**

- Multi-robot task orchestration.
- Traffic control and conflict resolution.
- Cross-robot cooperation.

**Architecture approach**

- Data/control separation: vehicle-local control loops stay in the real-time
  domain for low latency and safety, while platform observation, management, and
  tasks ride on a separate data bus across network segments.
- Heterogeneous abstraction: a fleet-adapter layer hides locomotion differences
  behind the unified model.
- Bridge, not invade: existing ROS 2 robots join the platform rather than having
  their middleware replaced.
- Edge autonomy and heterogeneous sensor intake through EdgeX Foundry.
- An industry northbound protocol (VDA5050 over MQTT) is under pre-research for
  cloud-master scenarios.

## How it fits in the suite

Fleet lives in the site/field plane of the suite, alongside Edge and
the robots themselves, on the local LAN rather than in the central platform.

- **Fleet → robots:** the platform schedules tasks and issues telecommands,
  while robots report state and telemetry back to the platform.
- **Open-RMF:** owns global task allocation, traffic negotiation, and resource
  conflict resolution.
- **EdgeX Foundry:** owns heterogeneous sensor access and edge autonomy, the same
  edge framework Edge builds on.
- **Closed-loop integration is future:** Fleet is not yet wired into the
  Edge → Forge → Horizon → Link loop; it is an early
  stage addition to the suite. See the [suite overview](index.md).

!!! info "Developer documentation"
    The authoritative, detailed developer documentation for Fleet lives in
    its own repository — see [NereidAI](https://github.com/NereidAI).

## Key facts

| Aspect | Detail |
|---|---|
| Status | Tech Preview — early design stage (v0.1 draft) |
| What it is | Management, control, and collaboration platform for robot fleets |
| Robot types | Wheeled AMRs, quadrupeds, humanoids, balancing robots |
| Positioning | Site/field plane of the suite, on the local LAN |
| First target | Wheeled AMR — simulation first, then hardware |
| Safety | Requires a vehicle-side hardware E-stop; platform E-stop is secondary |
| Stack | Open stack: ROS 2, Eclipse Zenoh, Open-RMF, EdgeX Foundry |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
