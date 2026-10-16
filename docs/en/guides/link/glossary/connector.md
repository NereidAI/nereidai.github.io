# Connector

A **connector** is a protocol-connector *instance* running on a [gateway](gateway.md) and managed through the platform. It is the concrete realization of a connector type on one gateway.

- A connector is either **gateway-level** (not bound to a device) or bound to exactly one managed [sub-device](subdevice.md).
- The platform is the system of record: you declare a **desired spec** `{connector_type, type_version, config, mappings}`, and the gateway reports the state it actually applied (`CREATED`, `DISPATCHED`, `APPLIED`, `DEGRADED`, `FAILED`).
- A connector's `config` and `mappings` are interpreted only by the edge; the platform never understands protocol details.

The bound [device profile](profile.md) supplies the reusable point table; instance overrides are merged over it at dispatch. [Health checks](health-check.md) (`health_check`) are available only on connectors bound to a device.

See the [Connectors](../connectors.md) page guide for full operations.
