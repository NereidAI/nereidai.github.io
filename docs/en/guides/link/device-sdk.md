---
title: Device SDK (Go)
---

# NereidLink Device SDK for Go

The Device SDK is for **device and gateway firmware** that connects to NereidLink
from the southbound side. It is a *thin protocol library*: typed frames,
credentials, topic bindings, and MQTT/HTTP transport helpers. It runs no
background goroutines or loops and makes no policy decisions — your firmware keeps
full control of poll cadence, reconnection, hello negotiation, and manifest timing.

- **Module:** `github.com/nereidai/nereidlink/sdk/device/go`
- **Independent of the server:** it does not pull NATS, database drivers, or any
  other server dependency.
- **Reference programs:** `examples/simple` (a direct device) and
  `examples/gateway` (a full gateway) ship in the module.

!!! info "Developer documentation"
    This page is a hands-on introduction. The full package API, constants, and
    runnable examples live in the NereidLink repository under
    `sdk/device/go/` — see [NereidAI](https://github.com/NereidAI).

## Install

```bash
go get github.com/nereidai/nereidlink/sdk/device/go@latest
```

## Packages

| Package | Purpose |
|---|---|
| `device` | Credentials (token / id+secret / X.509); frame models for telemetry, commands, shadow, attributes, events, OTA, hello/manifest/connector/discovery/probe; topic constants |
| `devicehttp` | HTTP ingress client: telemetry, long-poll commands, command response, shadow, OTA list / range download / progress |
| `devicemqtt` | MQTT ingress client (Eclipse Paho): connect, LWT, telemetry, attributes, events, command/shadow/attribute subscriptions |
| `gateway` | The gateway surface on top of `devicemqtt`: hello, heartbeat/goodbye, sub-devices, manifest, batched telemetry, relayed commands, connectors, discovery, probe, OTA, whole-gateway operations |

## Credentials

Every client starts from one credential:

```go
device.Token("device-access-token")        // MQTT username = token, empty password
device.Basic("edge-001", "credential-secret") // username / password
device.ClientCert(tlsCert)                 // mutual TLS (X.509)
```

A device cannot connect until an operator has created it and granted it at least
one valid credential — see [Credentials](credentials.md) and
[Integrate a direct device](integrate-direct-device.md).

## Direct device over MQTT

```go
client, _ := devicemqtt.Connect(ctx, devicemqtt.Options{
    BrokerURL:  "tcp://nereidlink.example:1883", // or tls://...:8883
    Credential: device.Token("device-access-token"),
    ClientID:   "sensor-001",
})
defer client.Disconnect(200)

// Downlink v1/me/cmd/<name>; reply on v1/me/cmdres/<id>.
_ = client.SubscribeCommands(ctx, 1, func(cmd device.Command) {
    _ = client.RespondCommand(ctx, cmd.ID, map[string]any{"ok": true}, 1)
})

_ = client.PublishTelemetry(ctx,
    device.NewFrame().SetFloat("temperature", 21.5).SetBool("online", true), 1)
```

The MQTT client bypasses HTTP/SOCKS proxies because field brokers are reached
directly; TLS still verifies the broker certificate unless you explicitly opt out.

## Direct device over HTTP

```go
httpClient, _ := devicehttp.New(devicehttp.Options{
    BaseURL:    "https://nereidlink.example",
    Credential: device.Token("device-access-token"),
})

_, _ = httpClient.PublishTelemetry(ctx,
    device.NewFrame().SetFloat("temperature", 21.5))

for {
    cmd, _ := httpClient.PollCommands(ctx) // one long poll; firmware loops
    if cmd != nil {
        _ = httpClient.RespondCommand(ctx, cmd.ID, map[string]any{"ok": true})
    }
}
```

**Frame rule:** a telemetry frame is a flat JSON object of numbers, booleans, and
strings. `null` and nested objects/arrays are rejected locally before upload; the
server turns each key into one Envelope. Units are never guessed — they come from
the bound [device profile](glossary/profile.md) descriptors.

## OTA on a direct device

The SDK streams bytes but never flashes or verifies firmware — that is the
firmware's job.

```go
list, _ := httpClient.ListOTAAssignments(ctx)
for _, job := range list.Assignments {
    var f *os.File // firmware decides where bytes go
    res, _ := httpClient.DownloadOTAPackage(ctx, job.TaskID,
        devicehttp.DownloadOptions{Destination: f}) // Range resume supported
    // Verify res.SHA256 (the X-Firmware-Sha256 value) before applying.
    _ = httpClient.ReportOTAProgress(ctx, job.TaskID,
        device.OTAProgress{State: device.OTAStateDownloading, ProgressPct: 50, Bytes: res.Written})
}
```

Drive the ordered state machine yourself:
`initiated → downloading → downloaded → verified → updating → updated → rebooting
→ confirmed/succeeded/failed`. See [OTA tasks](ota-tasks.md) and
[Firmware](firmware.md) for the operator side.

## Gateways

A gateway is a device with the gateway capability. It uses the device topics and,
after one **hello** per connection, the `v1/gateway/*` topics.

```go
mq, _ := devicemqtt.Connect(ctx, devicemqtt.Options{
    BrokerURL: *broker, Credential: device.Basic(id, secret),
    ClientID: edgeID, Will: devicemqtt.GoodbyeWill("transport_down"),
})
gw := gateway.Wrap(mq)

_ = gw.SubscribeConnectors(ctx, 0, func(push device.ConnectorPush) { /* apply */ })
_ = gw.SubscribeProbes(ctx, 0, func(req device.ProbeRequest) { /* answer per device */ })
_ = gw.SubscribeOTATasks(ctx, 0, func(task device.GatewayOTATask) { /* download */ })

ack, err := gw.NegotiateHello(ctx, device.Hello{
    EdgeID: edgeID, AgentVersion: "2.3.1",
    Proto:  device.ProtoRange{Min: "1.0", Max: "1.4"},
    Features: device.FeatureSet{
        Required: []string{device.FeatureTelemetry, device.FeaturePresence},
    },
}, 10*time.Second)

_ = gw.ConnectDevices(ctx, []string{subDeviceUUID}, 1)
_ = gw.PublishTelemetry(ctx, device.GatewayFrame{
    DeviceID: subDeviceUUID, TS: time.Now().UnixMilli(),
    Measurements: device.NewFrame().SetFloat("temperature", 21.5),
})
// gw.Heartbeat(...) on ack.Limits.HeartbeatS; gw.SendManifest(...) periodically.
```

The firmware — not the SDK — owns these responsibilities:

- Re-run hello after **every** reconnect; server state resets to unidentified and
  frames sent before the ack are discarded.
- Heartbeat on the negotiated interval; the LWT fires on crash, and a planned
  `Goodbye` is sent on graceful shutdown.
- Run a local link watchdog and report each unplanned down/up interval with
  `ReportLinkEpisode`; backlog replay is oldest-first, the platform de-duplicates.
- Send a full-state `Manifest` at the aligned cadence (explicitly include an empty
  connectors segment when reporting zero connectors).
- De-duplicate connector pushes by `(spec_id, revision)`; the full desired set is
  re-sent after every hello.

See the [gateway glossary](glossary/gateway.md),
[Integrate a gateway](integrate-gateway.md), and [Gateway operations](gateway-operations.md).

### Whole-gateway operations

Whole-gateway, menu-driven RPC (ping/reboot/…) is distinct from sub-device
commands. **The platform ships no operation names** — firmware advertises a
catalog in hello and executes only what it advertised:

- Subscribe **before** hello (`gw.SubscribeOperations`), advertise entries in
  `Hello.Operations` with bilingual display names, interaction
  (`request-response`/`one-way`), timeout, risk (`read`/`normal`/`dangerous`), and
  inline JSON schemas.
- The hello ack reports `accepted`/`reason` per entry; one bad entry never fails
  the handshake. Use namespaces `diag.*` / `sys.*` / `service.*` and
  `vendor.<vendor>.*`; a breaking change needs a new key or `type_version`.
- Answer request-response invocations within `inv.TimeoutMs` with
  `gw.RespondOperation`; `secret://` parameters arrive as plaintext at the last mile
  and must never be logged.

## Current gaps

The SDK tracks implemented server behavior; a few edges are intentionally not yet
exposed:

- Edge → platform object-storage blob relay is deferred.
- Gateway-published domain events are not implemented server-side.
- Hello `resume.last_cursor` is accepted but no cursor replay exists; desired state
  is full-state and idempotently re-driven.
- Downlink MQTT frames are QoS 0, non-retained; choose QoS 1 for uplink.
