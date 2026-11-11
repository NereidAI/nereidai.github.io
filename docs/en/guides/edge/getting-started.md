# Getting Started with NereidEdge

NereidEdge is an EdgeX Foundry **application service** (App Functions SDK Go
v4.0.2) that connects EdgeX southbound devices and companion services to
NereidLink. It converts EdgeX events and readings into Link gateway telemetry
over the MQTT gateway protocol `v1/gateway/*`, maps EdgeX device names to Link
sub-device UUIDs, and owns edge-local lifecycle management: connector
reconciliation, secret delivery, device commands, link-health tracking and —
when NereidInference is present — the neutral inference bridge.

!!! tip "Stands alone with Link"
    Edge needs only a reachable Link broker and gateway credentials. It does
    not require Sphere or Horizon to run. Horizon is how Edge is distributed
    and kept up to date across many sites, not a runtime dependency.
    NereidInference is also optional: Edge probes for it at runtime and only
    then offers the inference feature.

## Architecture

```text
EdgeX devices/services ---> EdgeX message bus ---> NereidEdge ---> NereidLink MQTT
                                                         |
                                                         +---> auxiliary MQTT brokers

NereidLink downlinks ---> NereidEdge ---> EdgeX core services / NereidInference
NereidInference state ---> NereidEdge ---> NereidLink manifest/shadow/telemetry
```

What Edge does:

- **Telemetry and presence** — converts EdgeX events/readings (including binary
  media markers) into gateway telemetry; attaches a sub-device on its first
  telemetry, withdraws presence on detach/shutdown, and sends a full device
  manifest every five minutes.
- **Governed connector lifecycle** — applies device- and node-level connector
  specs through typed handlers with schema advertisements, revision
  deduplication, ownership/conflict checks and manifest reconciliation.
  Out-of-band EdgeX device deletion is repaired on the next reconciliation.
- **Node-level MQTT export** — fans events out to independently managed
  `edge-export-mqtt` instances with resource filters, topic templates,
  auth/TLS, bounded queues and reconnect backoff.
- **Device control and health** — direction-aware commands, on-demand probes,
  per-instance health checks, the reported gateway shadow and live
  `log.level` updates.
- **Secret delivery** — stores ADR-0034 secret copies encrypted at rest,
  reconciles revisions/removals and fans ONVIF stream credentials out to
  NereidInference without placing them in connector specs or logs.
- **Inference bridge (ADR-0039)** — bridges model inventory, bindings, camera
  profiles, manager resources, binding status and detection telemetry. Edge
  never acquires packages, touches frames or calls a model server itself.

## Prerequisites

- An EdgeX Foundry 4.0.2 stack on the gateway: core-keeper, the NATS core bus,
  core-data, core-metadata, core-command and the required device services.
- A reachable Link MQTT broker (`tcp://` for plaintext, `tls://` for TLS).
- Link **gateway credentials** created in the Link console: Credential ID,
  credential secret and the gateway's Edge ID — see
  [Gateway Integration](../link/integrate-gateway.md) for the platform side and
  the [gateway concept](../link/glossary/gateway.md).
- Each field device registered in Link as a sub-device bound to the gateway, so
  its sub-device UUID is known.
- To build from source: Go 1.27.3 and (for `make verify`) golangci-lint. The
  NereidLink device SDK is an in-repo reviewed mirror under
  `third_party/nereidlink`, so no adjacent checkout or private module token is
  needed.

## 1. Prepare the platform side

In the Link console, create a gateway device, add a gateway credential, and
register each field device as a sub-device bound to that gateway. Note every
sub-device UUID — Edge maps EdgeX device names to them. Reading the
[Gateway Integration](../link/integrate-gateway.md) handshake (hello, heartbeat
and manifest) first makes Edge logs much easier to follow.

## 2. Configure NereidEdge

Edit the EdgeX custom configuration in `res/configuration.yaml` under the
`NereidEdge` section (every key has an `NEREIDEDGE_*` environment override for
container deployments):

| Key | Meaning |
|---|---|
| `BrokerURL` | Link MQTT broker, `tcp://host:1883` or `tls://host:8883`. The scheme enables TLS. |
| `CredentialID` | **Required in every auth mode, including mTLS.** MQTT CONNECT username for password auth; names the X509 credential for certificate auth. Must match an ID registered in Link. |
| `CredentialSecret` | Password/token secret; leave empty for X509 client-certificate auth. |
| `EdgeID` | Gateway identity; empty falls back to `CredentialID`. |
| `DeviceMap` | Comma-separated `edgex-name:link-uuid` pairs. Static mappings take precedence over connector-spec bindings. |
| `ForwardUnmapped` | `false` (recommended) skips telemetry from devices with no known mapping. |
| `ConnectorObserve` | `true` logs intended connector actions without mutating EdgeX metadata — useful for a first dry run. |
| `CoreCommandURL` | EdgeX core-command base URL; defaults to the Compose hostname. |
| `RootCAFile` / `RootCAPEM` | Private-CA broker pin, as a mounted file or inline PEM. |
| `ClientCertFile` + `ClientKeyFile` (or `*PEM`) | mTLS pair; both halves must use the same delivery mode. |
| `InsecureSkipVerify` | Lab brokers only — never enable in production. Pin the CA instead. |
| `ProfileWatch.Enabled` | Push device-profile add/update events as core-metadata reports them; the five-minute full scan remains as a safety net. |
| `MQTTTrace` | Verbose per-packet paho traces for transport forensics only. |

Minimal plaintext configuration:

```yaml
NereidEdge:
  BrokerURL: "tcp://<link-mqtt-host>:1883"
  CredentialID: "<your-cred-id>"
  CredentialSecret: "<your-cred-secret>"
  EdgeID: "<edge-instance-id>"
  DeviceMap: "edgex-device-1:<link-subdevice-uuid-1>,edgex-device-2:<link-subdevice-uuid-2>"
  ForwardUnmapped: false
```

### Persistent state and the secret key

Mount `/app/data` for durable state: ADR-0034 secret copies, the profile
revision ledger and the inference manager-resource ledger all live there.
Provision a stable 32-byte `Secrets.KeyFile`; with an empty key file the
service uses an ephemeral key and the platform must re-deliver every secret
after a restart.

## 3. Build and run

### Bare metal

```bash
make build-local     # binary for the current platform
make verify          # gofmt, go vet, golangci-lint, all tests, linux/amd64 build
./nereid-edge        # run from the repository root so res/ is discoverable
```

The EdgeX service key is `nereid-edge` and the default HTTP port is `59750`.
On startup Edge performs the Link hello/feature negotiation and then begins
relaying telemetry.

### Docker Compose (recommended for gateways)

The Compose file expects the external `edgex_edgex-network`, mounts `res/`
read-only, persists `/app/data` and rebuilds the native image on startup.

```bash
cp .env.example .env      # fill in broker URL and gateway credentials
make up                   # docker compose --env-file .env up -d --build
make logs
```

Use `.env.example` as the variable reference and keep credentials outside
version control. For extra overrides (`NEREID_EDGE_ID`, `NEREID_DEVICE_MAP`,
TLS mounts), copy `docker-compose.override.yaml.example` to
`docker-compose.override.yaml`. To select another operator profile:
`make up ENV_FILE=compose.k3s.env`.

### Image artifacts

```bash
make docker        # linux/amd64,linux/arm64 OCI archive under dist/images (no push)
make docker-dev    # native local ghcr.io/nereidai/nereidedge:<version> tag
```

Neither target logs in or pushes; GHCR publication happens only through the
CI workflows (`0.0.0-dev` rolling channel on every `main` push, three-tag
SemVer releases on `v*` tags, never a `latest` tag).

## 4. TLS and mTLS

Three trust models, selected purely by configuration:

| Broker certificate | Authentication | What to set |
|---|---|---|
| Public CA | id/secret | Only change `BrokerURL` to `tls://`; the image trust store verifies the server |
| Private CA | id/secret | Pin the CA PEM with `RootCAFile`/`RootCAPEM` |
| Private CA / mTLS listener | X.509 client certificate | Pin the CA **and** set `ClientCertFile`+`ClientKeyFile` (or the inline `*PEM` pair) together |

PEM delivery rules:

- Inline PEM wins when both a file path and inline text are set; prefer files,
  because environment values are seeded into core-keeper and visible via
  `docker inspect`.
- In YAML use a block scalar (`|`); in a `.env` file keep one line per PEM with
  literal `\n` separators — generate it with
  `awk 'NF {printf "%s\\n", $0}' ca.pem`. Both PKCS#8 (`BEGIN PRIVATE KEY`)
  and SEC1 (`BEGIN EC PRIVATE KEY`) key headers are accepted.
- The TLS SNI/verification name derives from the `BrokerURL` host
  automatically; there is no separate ServerName setting.
- The auxiliary `edge-export-mqtt` broker has its own `ca_cert`/`client_cert`
  connector fields and is configured separately.

## 5. Verify the bridge

1. Service health: `GET http://<host>:59750/api/v4/ping` returns `pong`.
2. In the Link console the gateway and its mapped sub-devices show **Online**.
   Edge attaches a sub-device on first telemetry and sends a full manifest
   every five minutes; heartbeats follow the interval negotiated in the hello
   ack.
3. Open a sub-device and confirm its readings update — EdgeX readings now
   appear as Link telemetry keyed by the mapped UUID.
4. Pull the diagnostic log tail through the gateway operation `sys.logs_tail`;
   the container also tees size-rotated logs onto the data volume.

If no data arrives, check the `DeviceMap` pairs, that EdgeX events reach the
application service over the message bus, and that the credential and Edge ID
pass negotiation. Planned goodbye and unplanned outages are distinguished in
the link-health episode records; subscriptions and state are replayed after a
reconnect.

## 6. The inference bridge (optional)

Everything inference-related is gated on **both** `Inference.Enabled: true`
(the static default) and a runtime existence probe: Edge calls
core-metadata `DeviceByName(nereid-inference)` before the first hello and every
30 seconds afterwards.

| Deployment shape | Detection | Behavior |
|---|---|---|
| No NereidInference installed | Manager device returns 404 | Hello carries no inference block; no `edge-inference` schema; byte-identical to firmware without the feature |
| Present, temporarily unreachable | A read fails after a prior success | Session stays negotiated; last good inventory is cached (never replaced with an empty list); shadow reports OFFLINE |
| Present, zero models | Successful read of `[]` | Explicit empty `models` segment every manifest cycle; Link hard-prunes the inventory |

When enabled, Edge bridges the model inventory (`ModelsJSON`), opaque manager
arrays via `edge-manager-resource` (GET → merge → PUT → GET with durable
replay), model and pipeline bindings through the `edge-inference` connector,
camera profiles, binding status, the runtime shadow block and optional
detection telemetry including evidence JPEGs as binary media markers.
Northbound privacy filters apply to both Link and auxiliary MQTT egress.

Key `NereidEdge.Inference` settings: `Backends` (`[kserve, openai]`, protocol
families only — never vendor names), `DeviceService` (`device-inference`),
`ManagerDevice` (`nereid-inference`), `InventoryPollS`/`ShadowPollS` (30 s) and
`BindingPollS` (10 s).

!!! warning "Production gate"
    Edge unit tests and NereidInference synthetic tests establish transport
    behavior, but the full Link → Edge → EdgeX → Inference end-to-end chain
    still depends on Link manager-resource delivery and final cross-product
    sign-off. Treat the inference bridge as a documented integration surface,
    not a production-validated one.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Startup fails: `CredentialID is required, including mTLS` | Even certificate auth needs the ID; it must match the X509 credential name registered in Link. Leave `CredentialSecret` empty in certificate mode. |
| `ClientCertPEM and ClientKeyPEM must be configured together` | Supply both halves through one delivery mode; mixing inline PEM and file paths is rejected. |
| `read NereidEdge.*File: no such file` | A PEM path points outside the container; mount the host cert directory read-only and use the in-container path. |
| `x509: certificate signed by unknown authority` | The broker CA is not pinned; set `RootCAFile`/`RootCAPEM` to the issuing CA PEM. |
| `x509: certificate is valid for ...` | Broker cert SAN does not match the `BrokerURL` hostname; use the matching hostname or reissue the certificate. |
| No telemetry forwarded | Verify `DeviceMap`, `ForwardUnmapped: false` behavior for unmapped devices, and that EdgeX events reach the bus. |
| Negotiation fails | Check `EdgeID`, credential validity and feature compatibility in the hello/ack exchange. |
| Connector shows APPLIED but the device rejects it | EdgeX multi-status (HTTP 207) can carry a per-item rejection with a nil transport error; Edge inspects every item status and reports `config-invalid` — read the item-level status code, not only the transport result. |
| Inference secrets vanish after an NI restart | NereidInference's non-secure secret store is memory-only; Edge re-posts referenced secrets on a 30 s cadence and before every job upsert. Do not rely on one manual POST. |

## Resources

- Repository: [NereidEdge](https://github.com/NereidAI/NereidEdge)
- [NereidEdge product page](../../products/nereidedge.md)
- [NereidInference getting started](../inference/getting-started.md) — the
  companion device service.
- [Gateway integration](../link/integrate-gateway.md) — the northbound
  `v1/gateway/*` contract.
- [Edge delivery](../../deployment/edge-delivery.md) — production rollout with
  NereidHorizon.
- Repository docs: `docs/deployment.md`, `docs/edge-inference.md`,
  `docs/logging.md`.
