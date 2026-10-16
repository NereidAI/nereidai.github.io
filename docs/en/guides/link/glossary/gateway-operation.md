# Gateway Operation

A **gateway operation** is an immediate, whole-gateway action requested on demand — for example rebooting the gateway or triggering a vendor-defined maintenance routine. It is distinct from a [connector](connector.md) desired spec (long-lived configuration) and from commands sent to a managed [sub-device](subdevice.md) (ADR-0012).

- The platform has no built-in operation vocabulary. Every operation is a **descriptor**: key, interaction (request-response/one-way), timeout, parameter/result JSON Schemas and risk level (`read`/`normal`/`dangerous`).
- Descriptors come from a gateway's hello advertisement, are defined privately by a tenant, or are a private clone of an advertised descriptor. A tenant may disable any operation.
- Invocation of a `dangerous` operation requires a fresh [step-up](edge-secret.md) TOTP challenge. Parameters may reference edge secrets and are resolved at the last mile.

See the [Gateway Operations](../gateway-operations.md) page guide.
