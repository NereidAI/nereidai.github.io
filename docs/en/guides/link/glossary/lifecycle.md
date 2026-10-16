# Lifecycle state

A device's **lifecycle state** is its operational status, as opposed to its live connection state.

- `ACTIVE` — in service; the default device-list view shows only active devices.
- `QUARANTINED` — reversibly locked by [quarantine](quarantine.md).
- Decommissioned/archived states are **tombstones**: devices are never physically deleted, so history and identity remain auditable.

Lifecycle is independent of [presence](presence.md): an active device may be offline, and connectivity says nothing about whether the device is in service.
