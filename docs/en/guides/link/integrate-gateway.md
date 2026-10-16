# Gateway Integration

This guide explains how to integrate a **[gateway](glossary/gateway.md) / edge node** — one process
that connects to NereidLink over a single MQTT connection and manages many
**[sub-devices](glossary/subdevice.md)** behind it (Modbus/ONVIF/S7 field buses,
local device services, and so on). It is written for gateway developers.

- **Transport:** MQTT 3.1.1 / 5.0 over TLS (mTLS optional).
- **Payloads:** JSON, UTF-8.
- **Official SDK:** Go — `github.com/nereidai/nereidlink/sdk/device/go`,
  package `gateway`. A complete reference program is in
  `examples/gateway`. Other languages can implement the wire contract in
  this document directly.
- The platform does not understand any south-side protocol. Mapping between
  platform sub-device UUIDs and local devices is entirely the gateway's job.

## 1. Prerequisites on the platform

1. The gateway itself is registered as a device of type **gateway**, with its
   own credential (ID + secret, token, or X.509 certificate).
2. Each sub-device is registered in the console and **bound to this
   gateway**. A gateway can only operate sub-devices bound to it; frames for
   a foreign or un-attached sub-device are dropped.
3. Sub-device profiles declare the telemetry point names; commands must be
   declared in the per-device command catalog before they can be dispatched.

## 2. Session lifecycle

State machine: `UNIDENTIFIED → NEGOTIATED → CLOSED`.

1. Establish the MQTT connection; pre-register the LWT on
   `v1/gateway/goodbye`.
2. Subscribe the hello-ack topic (or use the MQTT 5 Response Topic).
3. Publish `v1/gateway/hello`; negotiation must finish within 10 seconds.
4. Only after a successful ack may gateway data topics be used. Frames sent
   before the ack are discarded. Exactly one hello happens per connection.

### Hello (gateway → platform), topic `v1/gateway/hello`

```json
{
  "v": 1,
  "edge_id": "edge-001",
  "agent_version": "2.3.1",
  "proto": {"min": "1.0", "max": "1.4"},
  "features": {
    "required": ["telemetry", "presence"],
    "optional": ["ota", "shadow", "blob-relay", "command"]
  },
  "connectors": [
    {"type": "modbus", "type_version": "2.1",
     "config_schema": {"type": "object", "required": ["host"],
       "properties": {"host": {"type": "string"}, "port": {"type": "integer"}}}}
  ],
  "client_time": 1727360000123
}
```

- `features.required` must all be supported by the server or negotiation
  fails (`incompatible_features`); `features.optional` are downgraded away
  when unsupported. Available features: `telemetry`, `presence`, `ota`,
  `shadow`, `blob-relay`, `command`.
- `connectors[]` optionally registers inline, self-contained JSON Schemas
  (draft 2020-12; no external `$ref`) for the connector types this gateway
  can run. An invalid schema never fails the handshake; its result is
  reported per entry in the ack.
- `agent_version` is your build string and is independent of the protocol
  version.

### Ack (platform → gateway), topic `v1/gateway/hello/ack`

```json
{
  "session_id": "s_...",
  "status": "ok",
  "selected": "1.4",
  "server": {"min": "1.0", "max": "2.0", "version": "nereidlink-..."},
  "features": ["telemetry", "presence", "command"],
  "limits": {"heartbeat_s": 30, "hello_timeout_s": 10,
             "upload": {"max_mb": 256, "qps": 20}},
  "time": {"server_time": 1727360000456, "offset_ms": -312, "clock_warning": false}
}
```

Ack statuses: `ok`, `auth_failed`, `incompatible_version`,
`incompatible_features`, `quota_exceeded`. Use `limits.heartbeat_s` for the
heartbeat cadence. After every reconnect the server state resets to
`UNIDENTIFIED`: re-run hello, re-subscribe, and re-announce state.

## 3. Liveness: heartbeat, goodbye and LWT

- Publish a heartbeat to `v1/gateway/heartbeat` at the negotiated interval:

```json
{"seq": 42, "client_time": 1727360060000}
```

- Pre-register `v1/gateway/goodbye` as the MQTT will at CONNECT time. On
  graceful shutdown publish it explicitly with `planned: true`:

```json
{"reason": "upgrade", "planned": true}
```

  The broker-delivered LWT has no `planned` flag, so a crash is
  distinguishable from planned downtime.
- Missed heartbeats drive the platform watchdog (`HEALTHY → SUSPECT → DOWN`)
  and cascade attached sub-devices offline. A goodbye (planned or LWT)
  suppresses the suspicion timer.

### 3.1 Link episode reports (`v1/gateway/linkhealth`)

Run a local link watchdog in the gateway and report each unplanned
down/up episode after re-hello succeeds (QoS1):

```json
{
  "edge_id": "<gateway-uuid>",
  "session_id": "s_…",
  "down_at": "2026-10-10T03:12:44Z",
  "up_at": "2026-10-10T03:12:49Z",
  "reason": "transport_down"
}
```

- `edge_id` must equal this connection's gateway id; `down_at`/`up_at` are
  RFC3339 (the edge clock is the ground truth) and `up_at` must not precede
  `down_at`; `session_id` is optional.
- The platform corrects the matching lease episode or records a closed
  alarm-free episode for flaps shorter than the lease window, and answers on
  `v1/gateway/linkhealth/ack`: `accepted` / `duplicate` / `rejected`. Stop
  retrying on any of the three; no ack (transient server error) means retry.
- Backlog replay is just oldest-first QoS1 frames; de-duplication is by
  `(edge_id, down_at)`. Five unmatched episodes in 10 minutes raise a
  flapping alarm, auto-cleared after a quiet 10-minute window.

## 4. Sub-device [presence](glossary/presence.md)

| Topic | Direction | Payload |
|---|---|---|
| `v1/gateway/connect` | publish | `{"devices": ["<uuid>", ...]}` |
| `v1/gateway/disconnect` | publish | `{"devices": ["<uuid>", ...]}` |
| `v1/gateway/manifest` | publish | Full-state reconciliation, every 5 minutes |

Announce sub-devices in batches when they attach/detach. The manifest is the
authoritative periodic full list; the platform reconciles desired vs
reported presence from it:

```json
{
  "devices": ["<uuid-1>", "<uuid-2>"],
  "connectors": [
    {"spec_id": "ci-...", "revision": 3, "config_hash": "..."}
  ],
  "missed_cycles": 0
}
```

- `connectors` semantics matter: **omit the field** to skip connector
  reconciliation; send an explicit empty array `[]` to report "zero
  connectors applied".
- Include all currently attached sub-device UUIDs every time; the manifest
  is full-state, not a delta.

## 5. Sub-device [telemetry](glossary/telemetry.md)

Publish batches to `v1/gateway/telemetry`. The payload is a map keyed by
sub-device UUID; each value is the same flat scalar frame as a direct device
reports, with an optional `ts` (epoch milliseconds):

```json
{
  "07704cf9-...": {"ts": 1728374400000, "MACAddress": "AA:BB:CC:00:11:22"},
  "089fbb69-...": {"temperature": 23.1, "online": true}
}
```

Rules are identical to direct devices: values must be numbers/booleans/
strings (no nested objects or arrays); one storage record per key; unknown
keys are stored without descriptor conversion. A value may also be a
`{"blob":true,...}` marker (see direct-device integration): the media is
stored under `media/<tenant>/<sub-device>/...` and the point becomes a
`blob://` reference.

CLIENT-scope attributes use `v1/gateway/attributes` with
`{device: {key: value}}`; SERVER/SHARED pushes arrive on
`v1/gateway/attributes/push` as `{"device":"...","scope":"...","data":{...}}`.
After every (re)connect the gateway should publish
`v1/gateway/attributes/get` (`{"device":"...","scopes":[...],"response_topic"?}`,
omitted `scopes` means SERVER_SCOPE+SHARED_SCOPE) for each attached sub-device
and replace its cache from the full per-scope set in
`v1/gateway/attributes/get/ack`. A JSON `null` value in a push `data` map means
that key was deleted; drop it locally (do not store null). In the current
version both SERVER_SCOPE and SHARED_SCOPE are delivered to the device (unlike
classic ThingsBoard, where SERVER_SCOPE is server-private); do not assume
SERVER_SCOPE is private. The gateway's **own** attributes use the direct-device
topics `v1/me/attributes`, `v1/me/attributes/down`, `v1/me/attributes/get` and
`v1/me/attributes/get/ack` — the gateway is itself a device, and whole-gateway
runtime knobs (for example log level or trace switches) are delivered there,
not under `v1/gateway/...`.

## 6. Commands to sub-devices

Commands are declared per sub-device in the platform command catalog; the
gateway merely executes them against its local bus.

### Downlink (platform → gateway), topic `v1/gateway/command`

One subscription serves every sub-device; the `device` field selects the
target:

```json
{
  "command_id": "01J8...",
  "device": "07704cf9-...",
  "interaction": "request-response",
  "timeliness": "realtime",
  "method": "DeviceInformation",
  "direction": "read",
  "params": {}
}
```

- `interaction`: `one-way` (no reply expected) or `request-response`
  (exactly one correlated reply).
- `timeliness`: `realtime` (fails fast when offline) or `persistent`
  (queued server-side; the gateway only ever sees live frames).
- `method` is the catalog command name; `params` is the catalog-validated
  JSON delivered verbatim.
- `direction`: `read` or `write`, the south-side operation (read a resource
  vs. write a resource), orthogonal to `interaction`. The gateway MUST
  perform the GET/write exactly as directed and MUST NOT infer direction
  from the method name; a read may carry `params` (query arguments).
  `one-way` frames never carry `direction=read`.

### Uplink (gateway → platform), topic `v1/gateway/command/response`

```json
{
  "command_id": "01J8...",
  "device": "07704cf9-...",
  "data": {"manufacturer": "Acme", "model": "Cam-9", "firmware": "1.4.2"}
}
```

- Echo `command_id` and `device` unchanged; `data` is arbitrary JSON.
- For `one-way` commands send nothing.
- On local failure (device not reachable on the field bus, read error,
  timeout), still answer request-response commands with the error inside
  `data`, for example `{"error": "no response from field bus"}`. Not
  answering at all causes a platform-side `TIMEOUT`.
- A response is accepted only from the gateway that attached the named
  sub-device.

Go SDK:

```go
_ = gw.SubscribeCommands(ctx, 1, func(cmd device.GatewayCommand) {
    if cmd.Interaction != device.InteractionRequestResponse {
        return // one-way: execute silently
    }
    result := executeOnFieldBus(cmd.Device, cmd.Method, cmd.Params)
    _ = gw.RespondCommand(ctx, cmd.CommandID, cmd.Device, result, 1)
})
```

### 6.1 Sub-device shadow (desired / reported)

A shadow is stored per **device UUID**, independent of transport: the
gateway's **own** shadow is direct-device traffic on `v1/me/shadow/*`; the
shadow of a sub-device it proxies uses the batched gateway topics below.

- Report one or more sub-devices' reported state on
  `v1/gateway/shadow/report`. A single sub-device is a length-one batch:

```json
{
  "reports": [
    {"device": "07704cf9-...", "state": {"led": "on", "brightness": 7}, "version": 3},
    {"device": "089fbb69-...", "state": {"rpm": 1200}}
  ]
}
```

  `state` is a per-top-level-key patch (a JSON `null` value deletes the key);
  `version` optionally acknowledges the desired version just applied. Entries
  are authorized and stored independently: an empty `device`, a non-UUID or
  not-attached device, or a non-object/empty `state` causes that entry alone
  to be dropped and audited — the rest of the batch still persists. A frame
  whose top-level JSON cannot be parsed is dropped wholesale.

- Subscribe once to `v1/gateway/shadow/desired`; demux each entry by
  `device`. Like the direct channel, desired is **always full-state**, not a
  delta — replace each named sub-device's local desired map wholesale:

```json
{"desired": [{"device": "07704cf9-...", "version": 3, "desired": {"led": "on"}}]}
```

  Desired is re-pushed in full when it changes and once when a sub-device
  becomes ONLINE with `desired_version > 0`, so no per-device get is needed.

Go SDK:

```go
_ = gw.SubscribeSubdeviceShadowDesired(ctx, 1, func(frame device.GatewayShadowDesiredFrame) {
    for _, d := range frame.Desired {
        applyLocalDesired(d.Device, d.Version, d.Desired) // full replace
    }
})

_ = gw.ReportSubdeviceShadow(ctx, []device.GatewayShadowReport{
    device.NewGatewayShadowReportForVersion("07704cf9-...", map[string]any{"led": "on"}, 3),
}, 1)
```

## 7. Connector lifecycle (desired / reported)

NereidLink is the system of record for connector instances; the gateway
applies desired state and reports what it actually runs.

- Subscribe the single filter `v1/gateway/connectors/#`. Desired specs
  arrive on `v1/gateway/connectors/spec`
  (`spec_id`, `connector_type`, `type_version`, `config`, `mappings`,
  `health_check`, `revision`), removals on `v1/gateway/connectors/delete`.
- After every hello the **full desired set is re-sent idempotently**;
  de-duplicate by `(spec_id, revision)`.
- Report state on `v1/gateway/connectors/status` using the state machine
  `CREATING → APPLIED / FAILED / DEGRADED`, echoing `spec_id` and
  `revision`.

### Instance liveness probe (`health_check`)

A spec bound to one sub-device may carry `health_check`:

```json
{"resource": "camera_status", "interval_ms": 30000,
 "timeout_ms": 5000, "fail_threshold": 3}
```

- Every `interval_ms`, READ `resource` once for that sub-device and
  **discard the value**: never emit telemetry, shadow updates or any
  Envelope uplink from a probe.
- After `fail_threshold` consecutive failures/timeouts, assert the
  sub-device offline on `v1/gateway/disconnect`; the first successful
  probe afterwards asserts it back online on `v1/gateway/connect`
  (send state edges only).
- Stop probing when the field disappears or the spec is deleted; the
  probe is independent of the MQTT transport keepalive.

The console-side workflow is documented in the **Connectors** help topic.

## 8. Optional capabilities

| Capability | Downlink | Uplink | Notes |
|---|---|---|---|
| On-demand probe | `v1/gateway/probe` | `v1/gateway/probe/response` | Reachability test per sub-device; answer per device or one `responses[]` batch |
| Discovery / auto-provisioning | `v1/gateway/discovery/result` | `v1/gateway/discovery` | Report scan candidates; platform maps local IDs to UUIDs |
| OTA | `v1/gateway/ota/task` | `v1/gateway/ota/progress` | External firmware URL; ordered progress states |
| Profiles library | — | `v1/gateway/profiles` | Report local device profiles for adoption in the console |
| Attribute push | `v1/gateway/attributes/push`, `v1/gateway/attributes/get/ack` | `v1/gateway/attributes`, `v1/gateway/attributes/get` | SERVER/SHARED delivered + CLIENT reported; `null` deletes; see section 5 |
| Shadow | `v1/gateway/shadow/desired` | `v1/gateway/shadow/report` | Desired/reported device shadow |
| Gateway operations | `v1/gateway/operations/invoke` | `v1/gateway/operations/result` | Synchronous whole-gateway actions; see section 9 |

Advertise only what you implement in the hello `features` list (for the
session-level features) and simply do not publish the rest.

## 9. Gateway operations (whole-gateway actions)

Operations are immediate actions on the gateway itself (reboot, vendor
maintenance routines), distinct from sub-device commands (section 6). The
platform ships no operation vocabulary: advertise the operations your
build implements as catalog descriptors in hello `operations[]` — operation
key, interaction (`request-response`/`one-way`), timeout, parameter/result
JSON Schemas and risk (`read`/`normal`/`dangerous`).

The platform stores each gateway's descriptors **separately** (migration
0080); two gateways advertising the same key never overwrite each other, and
an invocation is validated against the TARGET gateway's own descriptor. Keep
these naming/version rules so a multi-vendor fleet stays consistent:

- `operations[]` is the gateway's **full current set** on every hello: keys
  absent from a later hello are reconciled away. Omit the field entirely
  (null) on firmware that does not speak operations; sending `[]` clears the
  set.
- `operation` + `type_version` is the contract: same key and version across
  gateways MUST have identical params, result, risk and interaction.
- Use standard namespaces for common actions — `diag.*` (diagnostics),
  `sys.*` (host info/maintenance), `service.*` (managed services); vendor
  actions MUST use `vendor.<vendor>.*` so they cannot collide.
- A breaking contract change needs a new `type_version` (or a new key, e.g.
  `diag.ping.v2`) since invoke frames do not select a version; when one
  gateway advertises several versions the newest one is invoked.
- The console aggregates the keys across gateways and flags a **contract
  conflict** when same-key advertisers disagree on risk/timeout/schema.

- Subscribe `v1/gateway/operations/invoke`. Invoke frames carry
  `id`, `operation`, `type_version`, `params` (already validated) and
  `timeout_ms`; the frame value is the effective bound — the smaller of the
  descriptor default and any operator per-call override, clamped to
  100–60000 ms. Reply on `v1/gateway/operations/result` with the same `id`,
  `ok`, and `result` or `error`.
- Execute only operations you advertised; answer every request-response
  invoke within `timeout_ms` — no reply means a platform-side `TIMEOUT`.
  For one-way operations send nothing.
- A parameter value of the form `secret://<name>` arrives already resolved
  to plaintext at the last mile; never log or persist it.
- Results MUST NOT contain passwords: the platform does not inspect result
  content, so redaction is the gateway's responsibility.
- Invocation is live-only: an offline gateway gets NOT_CONNECTED immediately
  and frames are never queued. Late/duplicate results are dropped.

```go
_ = gw.SubscribeOperations(ctx, 1, func(inv device.OperationInvoke) {
    out := runVendorOperation(inv.Operation, inv.Params)
    _ = gw.RespondOperation(ctx, device.OperationResult{
        ID: inv.ID, OK: true, Result: out,
    }, 1)
})
```

## 10. Topic summary

Gateway → platform: `v1/gateway/hello`, `heartbeat`, `goodbye`,
`linkhealth`, `connect`, `disconnect`, `manifest`, `telemetry`,
`attributes`, `shadow/report`, `command/response`, `ota/progress`,
`probe/response`, `connectors/status`, `profiles`, `discovery`,
`operations/result`.

Platform → gateway: `hello/ack`, `linkhealth/ack`, `command`,
`attributes/push`, `shadow/desired`, `ota/task`, `probe`,
`connectors/spec`, `connectors/delete`, `discovery/result`,
`operations/invoke`.

Uplink QoS is the gateway's choice (QoS 1 recommended); downlink frames are
QoS 0 and non-retained.

## 11. Integration checklist

- Gateway registered with a credential; all sub-devices registered and
  bound to it.
- Hello sent after every (re)connect; no gateway frames published before
  `status: ok`; feature list matches what the build implements.
- LWT registered before CONNECT; planned goodbye on graceful shutdown;
  heartbeats at `limits.heartbeat_s`.
- Local link watchdog episodes reported after re-hello; ack subscription
  registered once; stop retrying on `accepted`/`duplicate`/`rejected`.
- `connect`/`disconnect` on attachment changes; full-state manifest every 5
  minutes with correct `connectors` presence semantics.
- Telemetry batches keyed by UUID, flat scalar values only.
- Commands: one subscription for all sub-devices; answer every
  request-response command by `command_id` + `device`, including failures;
  never answer one-way commands.
- Connector pushes de-duplicated by `(spec_id, revision)`; status reported
  through the state machine.
- Shadow: gateway's own shadow on `v1/me/shadow/*`; sub-device reports batched
  to `v1/gateway/shadow/report` and one `v1/gateway/shadow/desired`
  subscription demuxed by `device`; replace full desired, never patch it.
- Operations advertised in hello `operations[]`; every request-response
  invoke answered on `operations/result` by `id` within `timeout_ms`;
  results contain no passwords.
