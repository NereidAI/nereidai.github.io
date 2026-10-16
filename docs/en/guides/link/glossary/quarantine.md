# Quarantine

**Quarantine** is a reversible incident-response lock on a single device. Use it when a device is suspected compromised, stolen, flooding, or behaving anomalously and must be stopped now without losing history.

Quarantine sets the device to the `QUARANTINED` [lifecycle state](lifecycle.md), evicts its [presence](presence.md) and live session, and makes further authentication fail — the device cannot reconnect, send [telemetry](telemetry.md), or receive commands while its credentials stay on record. Identity, ownership, telemetry and history are preserved, and releasing the device returns it to service without re-provisioning.

Quarantine is a lifecycle action, distinct from the [connection state](presence.md). See the [Quarantine](../quarantine.md) guide for reason codes and release procedure.
