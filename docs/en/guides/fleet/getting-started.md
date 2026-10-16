# Getting Started with NereidFleet

!!! warning "Tech Preview — design stage"
    Fleet is at an early design stage (v0.1 draft). The repository currently
    holds design documents, research and proposed architecture decisions rather
    than a runnable product; there is no operator console to install yet. This
    guide describes the intended first-run path and today's simulation proof of
    concept, not a finished workflow.

NereidFleet is the planned management, control and collaboration platform for
embodied-AI robot fleets — wheeled AMRs, quadruped, humanoid and balancing
robots. It will provide a robot roster with live status, multi-robot task
dispatch and traffic coordination, teleoperation and emergency stop, built on
an open stack: ROS 2, Eclipse Zenoh, Open-RMF and EdgeX Foundry.

## What it will do

- **Management** — asset ledger, fleet grouping, edge-node management, maps,
  permissions and audit.
- **Control** — single-robot teleoperation, emergency stop, safety-mode
  switching, and real-time state and telemetry.
- **Collaboration** — multi-robot task orchestration, traffic control, conflict
  resolution and cross-robot cooperation.

## Current state

There is nothing for operators to deploy in the Tech Preview. The project
follows a simulation-first, hardware-second route, and the engineering
milestones are:

1. **Phase 0 — simulation (no hardware):** bring up the validated Free Fleet
   multi-robot example with Open-RMF and a Zenoh ROS 2 DDS bridge, and verify
   task dispatch and traffic negotiation end to end.
2. **Phase 1 — wheeled-robot PoC:** adapt one wheeled AMR (the first target
   platform), put at least two robots on one Zenoh bus, and stand up a minimal
   roster/task/telemetry API and web UI.
3. **Phase 2 — edge and northbound:** connect EdgeX, research VDA5050 over
   MQTT for cloud-master scenarios, and extend to quadruped and humanoid
   robots.

The recommended environment for the simulation phase is Ubuntu 24.04 with
ROS 2 Jazzy, the Cyclone DDS RMW, Zenoh 1.5 or newer, and Open-RMF. Closed-loop
integration with the Edge → Forge → Horizon → Link pipeline is future work.

!!! danger "Safety stays on the vehicle"
    A platform emergency stop is never the only stop path. Every robot must keep
    a vehicle-side hardware E-stop or independent safety loop that can halt it
    during a network or bus failure.

## Stay informed

- [NereidFleet product page](../../products/nereidfleet.md) — target design and
  key facts.
- [Roadmap](../../community/roadmap.md) — maturity across the suite.
- The research reports, feasibility study and proposed ADRs live in the
  NereidFleet repository ([NereidAI](https://github.com/NereidAI)); check it for
  current scope before planning any integration.
