---
title: Adapter SDK (Go)
---

# NereidLink Adapter SDK for Go

The Adapter SDK lets developers add a **new southbound wire protocol** to
NereidLink as a separate project or repository. An adapter translates one wire
protocol into platform contracts; it owns **no command state machine and stores
no authoritative state**.

This is different from the [Device SDK](device-sdk.md): the Device SDK is used
*inside device/gateway firmware*, while the Adapter SDK is used to build a new
ingress connector that runs *with or alongside the platform*.

!!! info "Developer documentation"
    This page introduces the model and lifecycle. The package API and the
    complete reference adapters live in the NereidLink repository under
    `sdk/` and `adapters/` — see [NereidAI](https://github.com/NereidAI).

## Packages

| Package | Purpose |
|---|---|
| `sdk/adapter` | Lifecycle: config loading, enrollment, heartbeats, presence client, command dispatcher, request-based sessions / mailbox relay |
| `sdk/contract` | Stable wire contract: dispatch/event subject prefixes, command statuses, interaction modes, lifecycle `Event` |
| `sdk/telemetry` | Telemetry uplink: JSON frame → typed points → one `Envelope` per point → JetStream partition; stream ensuring; binary media offload via an injectable `MediaStore` (`blob://` references) |
| `sdk/registry` | Registry gRPC client for device authentication |
| `sdk/profile` | Optional profile-descriptor resolution (PostgreSQL-backed, cached) and raw-to-engineering conversion |
| `sdk/partition` | Immutable partition topology used by the uplink |
| `sdk/scriptruntime` | JavaScript runtime used by expression descriptors |
| `api/gen/nereidlink/v1` | Generated protobuf message types |

The SDK has **no dependency on the server's `internal/` tree**. Breaking changes
to SDK packages follow semantic versioning; internal packages may change at any
time.

## Adapter lifecycle

1. Load the shared config and connect to NATS (Core + JetStream).
2. Optionally ensure telemetry streams with `telemetry.EnsureStreams`.
3. `adapter.Enroll(...)` with the module type, ingress ID, and version.
4. Start presence (`Run`) and subscribe to command dispatch.
5. Translate protocol traffic into `telemetry.Publish` calls; translate
   dispatched commands into protocol writes; reply through the command handler.
   When the protocol carries binary payloads, implement `telemetry.MediaStore`
   against your storage and pass `telemetry.WithMediaStore(...)`; frame `data`
   fields stay base64 and published points reference the object as `blob://<key>`.
6. On graceful shutdown, disconnect sessions and let heartbeats stop.

A complete annotated skeleton is provided by `adapters/template`; the built-in
CoAP adapter (`adapters/coap`) is a full reference implementation.

## Starting an external project

```bash
mkdir myadapter && cd myadapter
go mod init github.com/example/myadapter
go get github.com/nereidai/nereidlink@v0.0.1
```

Copy `adapters/template/main.go` as your `main.go`. Only the SDK packages listed
above are needed — never import `internal/` from an external module (Go forbids
it).

## Shared configuration

```yaml
core:
  nats_url: nats://127.0.0.1:4222
  nats_user: module
  nats_password: module-password
  registry_grpc: 127.0.0.1:19090
  registry_token: dev-module-token
  management_url: http://127.0.0.1:8080
  postgres_dsn: ""            # optional; enables descriptor resolution
module:
  enrollment_token: my-enrollment-token
  heartbeat_interval: 10s
```

Protocol-specific configuration is the adapter's responsibility: parse the same
YAML file with an additional wrapper struct.

## Contract invariants

- Arrays in API responses are always `[]`, never `null`.
- The platform never invents semantics (for example units) — they come only from
  user-defined descriptors.
- Keep processing-plane logic off the connection plane, and keep business logic
  out of the adapter: tenants define rules in the platform.

## Next steps

- [Device SDK (Go)](device-sdk.md) — embed the client in device/gateway firmware.
- [Integrate a gateway](integrate-gateway.md) and the
  [connector glossary](glossary/connector.md) — how adapters surface as
  connectors managed from the console.
