---
title: NereidInference
---

# NereidInference

NereidInference (Inference, **NIN**) is the edge inference runtime of the
suite: an EdgeX Foundry **device service** that runs on a field gateway,
acquires frames from cameras and image sources, calls standards-based model
servers, and publishes normalized structured events back onto the EdgeX
message bus. It turns the models produced by Forge and delivered by Horizon
into live, on-site inference — without binding the gateway to any model
format, chip vendor or vendor SDK.

## What it solves

- Models trained in the factory must run on inexpensive field gateways, close
  to the cameras; round-tripping video to a cloud datacenter is too slow and
  often impossible on air-gapped sites.
- A site may mix cameras (RTSP, ONVIF, MJPEG) and model servers (OpenVINO,
  Triton, vLLM, MindIE); integrating each combination by hand does not scale.
- Field teams need one neutral runtime: new models should arrive as packages,
  not as new code, and a slow model must never stall the other jobs on the
  same gateway.

## Core capabilities

**Descriptor-driven media inference**

- One service instance per node runs any number of inference **jobs** (one per
  provisioned device); a job binds a frame source, a model package, a schedule
  and output options.
- Model and silicon neutral: no vendor SDK, no hard-coded tensor layouts, no
  business logic. Classification, detection, segmentation, pose/keypoint,
  embedding, dense-map, image-to-image and CTC-sequence models differ only by
  their package descriptor and registered decoder.
- Talks two standard inference protocols: **KServe gRPC v2** and
  **OpenAI-compatible HTTP**, against independently deployed model servers
  (OpenVINO Model Server, Triton, vLLM, MindIE, …).

**Frame acquisition at the edge**

- Sources: RTSP (via a per-URL ffmpeg child process, H.264/H.265 decode),
  ONVIF camera and ONVIF snapshot, MJPEG and JPEG (a pure-Go frame source).
- Each job samples at its own FPS with at most one in-flight inference and
  drop-oldest semantics: a slow model only lowers that job's frame rate —
  latency stays bounded and nothing queues.
- ONVIF stream URIs and secrets are federated from EdgeX
  core-metadata/core-command/secret-store data registered by the ONVIF camera
  device service, rather than typed per job.

**Generic decoding and events**

- A family of tensor-shape decoders is selected by the model package
  descriptor, never by a vendor or task fork: YOLO-style anchor and row
  detectors, YuNet face detection, classifiers, regressors, semantic/instance
  segmentation, keypoints, embeddings, dense maps, image tensors, CTC
  sequences, composites, and passthrough text for OpenAI chat/VLM responses.
- Results are published as normalized structured events on the EdgeX message
  bus, with an optional local annotated MJPEG preview for operators.

**Local model acquisition**

- The distributable unit is one gzip tar package (`*.tar.gz`) carrying a root
  `nereid-model.json` descriptor and checksummed payloads. The service watches
  an Open Horizon ESS local object directory and/or an inbox directory,
  validates and unpacks packages into a read-only active model root shared
  with the model server.
- Division of labor is explicit: **Forge owns model conversion and all
  model-specific parameters, Horizon only transports the package, and
  Inference unpacks it and follows the descriptor** — it never generates,
  repairs or guesses a model contract.

**Operations**

- Pure Go, statically built (`CGO_ENABLED=0`); ffmpeg runs as a
  credential-dropped child process. Multi-arch OCI images (`linux/amd64`,
  `linux/arm64`).
- Follows EdgeX 4.0 conventions and the device-service configuration layout;
  the preview port is an unauthenticated operator diagnostic and is meant to
  be restricted by network policy.

## How it fits in the suite

Inference is the on-site execution step of the model loop, alongside Edge:

- **Forge → Inference:** Forge produces the model package (ONNX or OpenVINO IR
  today; other artifact formats can be declared by descriptor).
- **Horizon → Inference:** Horizon distributes packages to the gateway's
  Open Horizon ESS local object store; Inference watches and activates them.
- **Inference ↔ model servers:** OVMS, Triton, vLLM or MindIE run as
  independent services; Inference is their client over KServe gRPC v2 or
  OpenAI-compatible HTTP.
- **Inference → EdgeX / Edge:** structured events enter the EdgeX bus and can
  flow north through the same edge integration Edge provides toward Link.

!!! info "Developer documentation"
    The full configuration, descriptor reference, decoder catalog and
    provisioning API live in the NereidInference repository — see
    [NereidInference](https://github.com/NereidAI/NereidInference).

## Status

NereidInference is **open source under Apache-2.0** and built on EdgeX 4.0.2.
Like the rest of the suite it currently ships on the rolling development
channel — source and CI-built images, with no tagged release yet. The generic
pipeline, model catalog, KServe/OpenAI backends and the built-in decoder set
are implemented, and live validation has passed for the HTTP JPEG to OVMS
KServe gRPC path, a real RTSP H.264 camera, an ONVIF snapshot camera, and CPU
Triton with ONNX Runtime. Some capabilities (default ONVIF `GetStreamUri`,
H.265, reconnect and credential rotation, production Horizon packages,
GPU/OpenVINO-backend Triton, other-vendor acceptance) remain open; the
[roadmap](../community/roadmap.md) tracks the release gates that apply to the
whole suite.

## Key facts

| Aspect | Detail |
|---|---|
| What it is | EdgeX device service for descriptor-driven media inference on field gateways |
| Positioning | On-site inference runtime of the model closed loop |
| Frame sources | RTSP, ONVIF camera/snapshot, MJPEG, JPEG |
| Inference protocols | KServe gRPC v2, OpenAI-compatible HTTP |
| Model servers | OpenVINO Model Server, Triton, vLLM, MindIE (independently deployed) |
| Model packaging | Tar package with `nereid-model.json` descriptor, delivered via Horizon ESS/inbox |
| Output | Structured EdgeX events; optional annotated MJPEG preview |
| Stack | Static Go binary on EdgeX Foundry 4.0, ffmpeg child process; amd64/arm64 |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidInference](https://github.com/NereidAI/NereidInference)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
