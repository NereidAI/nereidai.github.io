# Sub-device

A **sub-device** is a device that cannot connect to the platform on its own and is reached through a [gateway](gateway.md). The gateway owns and manages it.

- Its device **type** is "sub-device (gateway-managed)" and it has an owning gateway.
- [Telemetry](telemetry.md), [presence](presence.md) and commands flow via the gateway's northbound connection.
- It may have at most one bound [connector](connector.md); the connector column on the device list shows its reported state.

A **direct device** is the opposite case: it authenticates and connects to the platform directly.
