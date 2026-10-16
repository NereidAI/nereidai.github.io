# Getting Started with NereidEdge

NereidEdge is an EdgeX Foundry application service that bridges field devices
into Link. It converts EdgeX events and readings into Link gateway telemetry
frames over the gateway MQTT protocol, mapping EdgeX device names to Link
sub-devices. It runs on a field gateway alongside an EdgeX 4.0.2 stack.

!!! tip "Stands alone with Link"
    Edge needs only a reachable Link broker and gateway credentials. It does not
    require Sphere or Horizon to run. Horizon is how Edge is distributed and
    kept up to date across many sites, not a runtime dependency.

## Prerequisites

- An EdgeX Foundry 4.0.2 stack running on the gateway (core services, the NATS
  message bus and device services).
- A reachable Link MQTT broker (`tcp://` or `tls://`).
- Link **gateway credentials** created in the Link console: Credential ID,
  credential secret and the gateway's Edge ID — see
  [Gateway Integration](../link/integrate-gateway.md) for the platform side and
  the [gateway concept](../link/glossary/gateway.md).
- Each field device already registered in Link as a sub-device bound to the
  gateway, so its sub-device UUID is known.

## 1. Prepare the platform side

In the Link console, create a gateway device, add a gateway credential, and
register each field device as a sub-device bound to that gateway. Note every
sub-device UUID; Edge maps EdgeX device names to them. Reading the
[Gateway Integration](../link/integrate-gateway.md) handshake (hello, heartbeat
and manifest) first makes Edge logs much easier to follow.

## 2. Configure the device map

Edit the EdgeX custom configuration file `res/configuration.yaml` under the
`NereidEdge` section:

```yaml
NereidEdge:
  BrokerURL: "tcp://<link-mqtt-host>:1883"
  CredentialID: "<your-cred-id>"
  CredentialSecret: "<your-cred-secret>"
  EdgeID: "<edge-instance-id>"
  DeviceMap: "edgex-device-1:<link-subdevice-uuid-1>,edgex-device-2:<link-subdevice-uuid-2>"
```

`DeviceMap` is a comma-separated list of `edgex-device-name:link-subdevice-uuid`
pairs. In production use a `tls://` broker URL and keep the credential secret in
a secrets manager rather than committing it to a file.

## 3. Build and run

Build the binary with `make build-local` or the container image with
`make docker`, then run Edge as an EdgeX application service — bare metal,
Docker, or Docker Compose joined to the EdgeX network. On startup Edge performs
the Link hello/feature negotiation and then begins relaying telemetry. The
deployment modes, networking and compose details live in the product
repository's `docs/deployment.md`.

## 4. Verify the bridge

1. Check the Edge service health endpoint: `GET /api/v4/ping` on port `59750`
   returns `pong`.
2. In the Link console the gateway and its mapped sub-devices show **Online**.
   Edge attaches a sub-device on its first telemetry and sends a full device
   manifest every five minutes.
3. Open a sub-device and confirm its readings update — EdgeX readings now appear
   as Link telemetry keyed by the mapped UUID.

If no data arrives, verify the DeviceMap pairs, that EdgeX events reach the
application service over the message bus, and that the gateway credential and
Edge ID pass negotiation.

## Next steps

- [Gateway Integration](../link/integrate-gateway.md) — the northbound contract
  Edge speaks.
- [NereidEdge product page](../../products/nereidedge.md) and
  [Edge delivery](../../deployment/edge-delivery.md).
- Configuration, troubleshooting and the protocol reference live in the
  NereidEdge repository ([NereidAI](https://github.com/NereidAI)).
