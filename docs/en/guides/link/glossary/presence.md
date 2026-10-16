# Presence

**Presence** is the platform's real-time view of whether a device is currently connected: online, offline, or unknown.

- A **presence boundary** is an online/offline transition event (connect, disconnect, session eviction).
- **Connection state** is derived from the latest boundary; *unknown* means the device has never produced one.
- **Last activity** is the newer of the latest [telemetry](telemetry.md) and the latest presence boundary, shown when hovering the connection badge.

Presence answers "is it connected now"; [lifecycle state](lifecycle.md) answers "what operational status is it in" (active, quarantined, decommissioned). The two are independent.

For a passive sub-device, presence does not prove field-bus reachability: it can stay online after the device itself drops off. An on-demand [probe](probe.md) verifies that end-to-end.
