# Getting Started with NereidInference

NereidInference is an EdgeX Foundry 4.0 **device service** for descriptor-driven
media inference. One instance on a gateway runs any number of inference **jobs**
— one job per provisioned EdgeX device. Each job acquires frames from a camera
or image source, calls an independently deployed model server over KServe gRPC
v2 or an OpenAI-compatible HTTP API, decodes the raw tensors with the model
package descriptor, and publishes normalized structured events to the EdgeX
message bus, with an optional annotated MJPEG preview for operators.

The service is model- and silicon-neutral: it contains no vendor SDK, no
hard-coded tensor layouts and no business logic. Classification, detection,
segmentation, pose, embedding, dense-map, image-to-image and CTC-sequence
models differ only by the package descriptor and the registered decoder kind.

!!! tip "Stands alone on the EdgeX bus"
    NereidInference needs only an EdgeX 4.0 core stack and a reachable model
    server. NereidEdge is **not** a runtime dependency: Edge only bridges
    inventory, bindings and credentials when the suite-level inference
    integration is enabled. Production rollout uses NereidHorizon Open Horizon
    service definitions; this guide runs the developer Compose overlay.

## Architecture

```text
camera RTSP ──► ffmpeg child process (H.264/H.265 decode, rawvideo pipe)
MJPEG/JPEG ──► pure-Go frame source          ──► preprocess ──► KServe gRPC / OpenAI
                                                                       │
EdgeX core ◄── structured events (async) ◄── generic decoder ◄───────┘
operators  ◄── annotated MJPEG preview (local, optional)
model packages (.tar.gz with nereid-model.json) ──► inbox / ESS watcher ──► active model root
```

Key properties:

- **One ffmpeg per source URL**, reference counted and fanned out to N jobs.
  Each job samples at its own FPS with at most one in-flight inference and
  drop-oldest semantics, so a slow model only lowers that job's frame rate —
  latency stays bounded and nothing queues.
- **No CGo.** The Go binary is statically built (`CGO_ENABLED=0`); ffmpeg is a
  runtime Alpine package executed as a credential-dropped child process.
- **Local model acquisition.** The service watches an Open Horizon ESS local
  object directory and/or a plain inbox directory, validates and unpacks model
  packages into an `active/` model root shared read-only with the model server.
- **Federated credentials.** For ONVIF cameras the stream URI and secret name
  are resolved through EdgeX core-metadata/core-command/secret-store data
  registered by the ONVIF camera device service — credentials are never typed
  per job.

## Core concepts

| Concept | What it means |
|---|---|
| **Job** | An EdgeX device whose `Inference` protocol properties select source, model, schedule and output. Jobs are not provisioned by default. |
| **Manager device** | The singleton `nereid-inference` device (profile `nereid-inference-manager`) exposing service-level resources: `ModelsJSON`, `ObjectDiagnosticsJSON`, `ExternalServablesJSON`, `PipelinesJSON`. It is not a job. |
| **Device profile** | A YAML in `cmd/res/profiles/` defining the reading resources for one task family (detection, classification, pose, …). A job's `profileName` decides which readings it emits. |
| **Model package** | One gzip tar (`*.tar.gz`) with a root `nereid-model.json` descriptor and checksummed payloads. Built by NereidForge, transported by NereidHorizon, unpacked by this service. |
| **Decoder** | A tensor-shape decoder selected by the descriptor — never a vendor or task fork. The registry starts empty; no business pipeline ships in the binary. |
| **Servable** | A model instance loaded on a model server. NereidInference manages OVMS/Triton servables itself; external servers are observed read-only. |

## Prerequisites

- An EdgeX 4.0 core stack (core-keeper, core-metadata, core-command, the NATS
  message bus and device services), brought up from the official
  [edgex-compose](https://github.com/edgexfoundry/edgex-compose) project, with
  the external `edgex_edgex-network` available.
- A reachable model server — OpenVINO Model Server, Triton, vLLM or MindIE —
  deployed independently and serving at least one model. The repository's
  developer Compose also bundles OVMS and a managed Triton container.
- A frame source: an RTSP/ONVIF camera, an MJPEG/JPEG endpoint, or a `none`
  source for pipeline-only validation.
- A model package (`*.tar.gz` with a root `nereid-model.json`), produced by
  NereidForge or built following the descriptor guide in the repository.

## 1. Start the service

The repository ships a developer `docker-compose.yaml` that overlays the
official EdgeX stack on the external `edgex_edgex-network`. It adds four
pieces: the `device-inference` service itself, an OVMS init container that
renders an empty multi-model configuration, the `edgex-ovms` server, and a
managed `edgex-triton` server.

```bash
docker network create edgex_edgex-network 2>/dev/null || true
docker compose up -d device-inference
```

The local service sets `pull_policy: build`, so this ordinary `up` builds the
service from the current working tree first — no separate `make docker` or
`--build` flag is required. The published ports are `59992` (the service's
provisional EdgeX port, pending TSC assignment) and `28080` on the host, which
forwards to the container's preview port `18080`.

To build artifacts directly:

```bash
make build     # static binary at cmd/device-inference (CGO_ENABLED=0)
make test      # unit tests, golangci-lint, go vet, gofmt, Attribution gate
make image     # linux/amd64,linux/arm64 OCI archive under dist/
make docker    # native development tags plus the OCI archive
```

There is no `VERSION` file and no `latest` tag: an exact `v*` tag checkout
builds its bare SemVer, every other checkout builds the rolling `0.0.0-dev`
channel, and CI may inject `VERSION` explicitly.

### Compose volumes

| Volume / mount | Container path | Purpose |
|---|---|---|
| `model-root` | `/var/lib/nereid-inference/models` | Active model root, package catalog and runtime state |
| `ovms-runtime` | `…/models/runtime` | Server-ready repositories shared with OVMS |
| `inference-inbox` | `/var/lib/nereid-inference/inbox` | Drop directory watched for new packages |
| host ESS store (read-only) | `/var/horizon/ess-store/sync/local` | Open Horizon ESS local objects delivered by Horizon |
| `/dev/dri` | `/dev/dri` | DRM render nodes for optional VA-API decode |

## 2. Understand the configuration

Service configuration follows the standard EdgeX layout in
`cmd/res/configuration.yaml`. The product-specific section is `Inference`:

| Key | Default | Meaning |
|---|---|---|
| `DefaultEndpoint` | `edgex-ovms:9000` | KServe gRPC endpoint used by managed OVMS leases |
| `OpenAIEndpoint` | `http://edgex-vllm:8000` | Default OpenAI-compatible HTTP base URL |
| `ModelRoot` | `/var/lib/nereid-inference/models` | Active model root and persistent runtime state |
| `CoreMetadataURL` / `CoreCommandURL` | EdgeX compose hostnames | Used for ONVIF federation and manager callbacks |
| `Ess.Enabled` / `Ess.LocalDir` | `true` / ESS path | Watcher for Open Horizon local objects |
| `Inbox.Enabled` / `Inbox.Dir` | `true` / inbox path | Watcher for manually dropped packages |
| `Preview.Enabled` / `Preview.Bind` | `true` / `0.0.0.0:18080` | Unauthenticated operator preview |
| `OVMS.*` | enabled, REST `:9001` | Managed OVMS reconciler: servable add/remove and reload timeout |
| `Triton.*` | enabled | Managed Triton reconciler with explicit model-control load/unload |
| `External.Enabled` / `External.ProvisionFile` | `true` / `res/external-servables.yaml` | Read-only view of servers NereidInference cannot administrate |
| `Pipelines.ProvisionFile` | empty | Opt-in A-channel pipeline registry; empty means a blank registry |
| `Limits.MaxJobs` | `64` | Maximum concurrent jobs per node |
| `Limits.FrameTTLFactor` | `2.0` | Frame staleness bound relative to the sample interval |
| `Limits.JSONPayloadCap` | `1048576` | Maximum serialized event payload in bytes |
| `FFmpeg.VAAPIDevice` | `/dev/dri/renderD128` | Default DRM render node for `DecodeAccel: vaapi` jobs |

## 3. Provision an inference job

A job is an EdgeX device with an `Inference` protocol map. The full property
set:

| Property | Values / example | Notes |
|---|---|---|
| `SourceKind` | `rtsp` · `rtsp-udp` · `onvif-camera` · `onvif-snapshot` · `mpjpeg` · `jpeg` · `none` | Frame acquisition family |
| `SourceDevice` | `camera-01` | EdgeX name used for ONVIF URI/secret/snapshot federation |
| `SourceURL` | `http://host/snapshot.jpg` | Direct URL for `jpeg`/`mpjpeg`/`rtsp` sources |
| `StreamProfile` | `Profile_2` | Optional ONVIF Media ProfileToken, `onvif-camera` only |
| `SecretName` | `onvif-camera-01` | Optional; resolved from camera metadata when omitted |
| `FFmpegExtra` | `-fflags nobuffer …` | Optional allowlisted argv, ffmpeg sources only |
| `ModelID` / `ModelVersion` | `example-yolov8n` / `1.0.0` | Selects a catalog package for single-model jobs |
| `PipelineId` | `face-recognition-v1` | Replaces ModelID/Version for registry pipeline jobs |
| `TargetDevice` | `CPU` · `GPU` · `GPU.0` · `NPU` | OVMS binding target carried in the inference binding |
| `Endpoint` | `edgex-ovms:9000` | Optional override of the lease's family endpoint |
| `ServableID` | external servable id | External-server jobs; rejected for pipeline jobs |
| `Trigger` | `continuous` · `periodic` · `event` · `command` | How frames are sampled; `event` maps to a manual command trigger |
| `FPS` / `PeriodMs` | `5` / `5000` | Continuous rate / periodic interval |
| `MaxInferMs` | `5000` | Per-inference time bound |
| `PublishMode` | `all` · `nonempty` · `none` | `nonempty` suppresses empty-result events; `none` keeps only the GET cache |
| `DecodeAccel` / `VAAPIDevice` | `vaapi` / `renderD129` | Optional hardware decode; a missing node or driver fails the job loudly |

### Option A — development device file

Drop a YAML file into `cmd/res/devices/`; the SDK auto-loads it at startup.

```yaml
deviceList:
  - name: example-inference-01
    profileName: nereid-inference-detection
    description: Example inference job (development only)
    labels: [nereid, inference]
    protocols:
      Inference:
        SourceKind: jpeg
        SourceURL: "http://camera-host/snapshot.jpg"
        ModelID: example-model
        ModelVersion: "1.0.0"
        TargetDevice: CPU
        Endpoint: "edgex-ovms:9000"
        Trigger: periodic
        PeriodMs: "5000"
```

A camera already registered with the ONVIF camera device service needs no
copied credentials — reference it by EdgeX name:

```yaml
    protocols:
      Inference:
        SourceKind: onvif-snapshot
        SourceDevice: registered-onvif-camera
        ModelID: example-model
        ModelVersion: "1.0.0"
        TargetDevice: CPU
```

### Option B — core-metadata API

Production provisioning goes through EdgeX core-metadata (or NereidEdge when
the suite integration is enabled):

```bash
curl -fsS -X POST "http://localhost:59881/api/v3/device" \
  -H 'Content-Type: application/json' \
  --data-binary @job.json
```

## 4. Choose the device profile

Thirteen profiles ship in `cmd/res/profiles/`; the profile names the reading
resources the job emits:

| Profile | Primary readings |
|---|---|
| `nereid-inference-detection` | `DetectionJSON`, `DetectionCount`, `Top1Label`, `Top1Score`, `FrameJPEG` |
| `nereid-inference-classification` | `ProbsJSON`, `AttributesJSON`, `Top1Label`, `Top1Score` |
| `nereid-inference-segmentation` | `SegmentationJSON`, `InstanceJSON`, `SegmentCount` |
| `nereid-inference-pose` | `KeypointsJSON`, `PersonCount` |
| `nereid-inference-embeddings` | `VectorJSON` (L2-normalized) |
| `nereid-inference-regression` | `RegressionValue`, `RegressionJSON` |
| `nereid-inference-dense` | `DenseJSON`, `DenseValue`, `DepthMean` |
| `nereid-inference-image` | `ResultJPEG`, `FrameJPEG` |
| `nereid-inference-ocr` / `…-llm` | `Text`, `Confidence` |
| `nereid-inference-composite` | `CompositeJSON` (named member results) |
| `nereid-inference-pipeline` | `PipelineJSON`, `ActivePipelineVersion`, `LatestPipelineVersion` |
| `nereid-inference-manager` | Manager-only: `ModelsJSON`, `ObjectDiagnosticsJSON`, `ExternalServablesJSON`, `PipelinesJSON` |

Every job profile also carries the operational resources `State`
(`APPLIED`/`DEGRADED`/`FAILED`), `LastError`, `SuccessTotal`, `ErrorTotal`,
`P50Ms`, `P95Ms`, `InferLatencyMs` and the writable `Trigger`.

## 5. Deliver a model package

Place the package in either watched location — the inbox directory or the ESS
local object store. The service validates the checksum and descriptor, unpacks
into the read-only active model root, and registers the model in the catalog
exposed by the manager device.

- Artifact format and runtime are orthogonal: current packages declare
  `artifact.format: onnx` or `openvino-ir`; a future Triton/TensorRT package may
  declare more formats and `runtime.server.family: triton`. The catalog accepts
  the standard package; the selected runtime adapter rejects an artifact it
  cannot serve.
- For OVMS, the descriptor declares `runtime.server.family: ovms` and
  `runtime.repository_path` pointing at a repository containing either
  `<version>/model.onnx` or `<version>/model.xml` plus `model.bin`. The numeric
  repository directory (normally `1`) is OVMS-local versioning, distinct from
  the Nereid semantic model version.
- Division of labor is explicit: **Forge owns conversion and every
  model-specific parameter, Horizon only transports the package, and
  NereidInference unpacks and follows the descriptor** — it never generates,
  repairs or guesses a model contract.

## 6. Model servers and external servables

- **Managed OVMS** — the bundled server starts from an empty configuration;
  the service adds or removes one servable per active binding and target device
  and drives reloads over the OVMS REST endpoint.
- **Managed Triton** — the reconciler renders the Triton repository and drives
  explicit model-control load/unload over the HTTP Repository API, with
  configurable load and readiness timeouts.
- **External servables** — centralized or customer-provided servers that
  NereidInference cannot administrate. Declare them in
  `res/external-servables.yaml`; the merged `ExternalServablesJSON` health view
  is read-only, managed writes and `ServableID` execution against them are
  rejected.

## 7. Multi-model pipelines (optional)

The binary ships no business pipeline. The registry accepts a closed five-node
linear vocabulary — **source → infer → transform → infer → emit** — validated
by the pipeline kernel. Two opt-in onboarding channels exist:

1. **Provision file (A channel):** copy a definition next to `res/` and set
   `Inference.Pipelines.ProvisionFile`; a missing file yields an empty registry
   rather than a startup failure.
2. **Manager resource (B channel):** PUT the complete definition array through
   the `PipelinesJSON` EdgeX resource. PUT is full replacement, not a patch;
   any invalid entry rejects the whole request. Accepted tables persist under
   `ModelRoot/runtime/pipelines/pipelines.json` and survive restarts.

```bash
COMMAND=http://localhost:59882
curl -fsS "$COMMAND/api/v3/device/name/nereid-inference/PipelinesJSON" |
  jq -r '.event.readings[] | select(.resourceName == "PipelinesJSON") | .value' | jq .
```

`pipelineId` + `version` is permanently immutable, and a canonical SHA-256
history is retained even for deleted versions. The opt-in sample
`samples/pipelines/face-recognition-v1.yaml` implements a YuNet → five-point
alignment → SFace chain; provision it with profile
`nereid-inference-pipeline` and a `PipelineId` binding (never `ModelID`).

## 8. Verify a job

1. Watch the service logs for the frame source (ffmpeg for RTSP), the KServe /
   OpenAI calls and the decoder registration.
2. Fire a command-triggered job on demand:

   ```bash
   curl -fsS -X PUT \
     "$COMMAND/api/v3/device/name/example-inference-01/Trigger" \
     -H 'Content-Type: application/json' \
     --data-binary '{"Trigger":"run"}'
   ```

3. Read the cached result and health counters:

   ```bash
   curl -fsS "$COMMAND/api/v3/device/name/example-inference-01/DetectionJSON"
   curl -fsS "$COMMAND/api/v3/device/name/example-inference-01/State"
   ```

4. Subscribe to the EdgeX message bus for asynchronous events; with
   `PublishMode: nonempty`, frames whose result array is empty are suppressed.
5. Open the annotated preview at `http://<host>:28080/` to inspect boxes and
   labels overlaid on frames.

!!! warning "Preview port is diagnostics only"
    The preview server is unauthenticated. In containers it binds
    `0.0.0.0:18080` so published ports work; restrict it with host bindings,
    network policies or a reverse proxy, or set `Preview.Bind` to
    `127.0.0.1:18080`. It is not a business API.

## 9. Implementation boundaries

Implemented and live-validated: the generic pipeline, model catalog,
KServe/OpenAI backends, the built-in decoder set, the HTTP JPEG → OVMS KServe
gRPC → decoder → EdgeX event/preview path, one real RTSP H.264 camera, one
ONVIF snapshot camera, and managed Triton with ONNX Runtime on CPU.

Still open: default ONVIF `GetStreamUri`, H.265, reconnect and credential
rotation, production Horizon packages, GPU/OpenVINO-backend Triton, other-vendor
acceptance, and real NereidForge face-package validation for the sample
pipeline (its current tests use synthetic fixtures).

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| Job `State: FAILED`, `LastError: config-invalid` | The binding was rejected at admission (unknown property value, `PipelineId` mixed with `ModelID`, pipeline job with a `ServableID`). Fix the device protocol map and re-provision. |
| Job fails loudly at startup mentioning `/dev/dri` | A `vaapi` job cannot find the DRM node or VA driver. Map `/dev/dri` into the container and install `intel-media-driver` (amd64 only); there is no silent software fallback. |
| `State: FAILED` with model-not-ready, then recovery | A newest pipeline version cannot resolve; the previous active graph keeps serving. The service retries resolution every five seconds and clears the latch once the latest definition resolves. |
| Preview unreachable | Check the host port mapping (`28080→18080`) and `Preview.Enabled`; bind it to localhost if no remote operators need it. |
| ONVIF job has no stream | Confirm the camera is registered by the ONVIF camera device service and `SourceDevice` matches its EdgeX name; the service federates URI and secret rather than storing them. |
| Secrets disappear after a restart | In non-secure mode the secret store is memory-only; re-deliver secrets through EdgeX Keeper or the provisioning flow. Named secrets must never be committed to `res/`. |

## Resources

- Repository: [NereidInference](https://github.com/NereidAI/NereidInference)
- [NereidInference product page](../../products/nereidinference.md)
- [Edge getting started](../edge/getting-started.md) — the companion service
  bridging EdgeX events into Link.
- [Edge delivery](../../deployment/edge-delivery.md) — production rollout with
  NereidHorizon.
