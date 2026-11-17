---
title: NereidInference
---

# NereidInference

NereidInference (**NIN**) is the **AI inspector that works next to the
camera**. It runs on the field gateway, takes the models produced by
[NereidForge](nereidforge.md), and puts them to work on live video and images
on site — detecting, classifying, reading text, recognizing faces and more —
then sends structured results into the platform. Video stays on the premises,
answers come back in milliseconds, and no cloud round-trip is involved.

NIN is what you reach for when these questions come up:

- "Sending every camera stream to a cloud AI service is too slow, too
  expensive and often forbidden — can the model run on site?"
- "We buy gateways from different vendors with different chips. Will one AI
  runtime cover them all?"
- "Upgrading a model currently means a software project. Can it just be a
  file we drop in?"
- "One heavy model is slowing everything else on the gateway. How do we keep
  the other inspections on time?"
- "How do operators see what the AI is actually looking at?"

## What NIN helps you do

### Run AI at the edge, not in a distant datacenter

Inference happens on the gateway beside the camera, so results come back in
real time and video never needs to leave the site. This is what makes
air-gapped factories, campuses and security deployments possible at all.

### One runtime for every kind of vision and language task

The same service handles classification, object detection, segmentation,
pose and keypoints, embeddings, dense maps, image-to-image, OCR, CTC text
sequences and LLM/VLM responses. Task differences live in the model package,
not in separate software forks — there is no vendor SDK and no hard-coded
model layout inside the runtime.

### Add a model by delivering a package, not deploying code

A model arrives as one versioned package containing a descriptor that
explains its inputs, outputs and decoding rules. NIN validates and unpacks
it, and the new model is available as a running job. Packages travel through
[NereidHorizon](nereidhorizon.md) or a simple watched inbox; the runtime
never invents or repairs model contracts itself.

### Keep every inspection on schedule

Each job samples its camera at its own pace with at most one inference in
flight and a drop-oldest policy: a slow model only lowers its own frame rate.
Latency for every other job stays bounded, queues do not pile up, and a
single node can run up to its configured job limit (64 by default).

### Use the chips and model servers you already have

NIN is a client of independently deployed model servers — OpenVINO Model
Server, Triton, vLLM, MindIE and similar — over two standard protocols
(KServe gRPC v2 and OpenAI-compatible HTTP). It can manage its own OpenVINO
and Triton servers, while central or customer-provided servers are observed
read-only. Switching hardware does not rewrite your application.

### Watch the AI at work

Every job exposes health counters, success/error totals, latency percentiles
and a readable state (applied, degraded, failed) with the last error. An
optional annotated preview draws boxes and labels directly on the frames, so
operators can verify behavior visually; the preview is an unauthenticated
diagnostic port and is meant to be restricted by network policy.

## A model goes to work

1. **Deliver** — Forge builds the package and Horizon (or a local inbox)
   places it on the gateway.
2. **Validate and unpack** — NIN checks the descriptor and checksums, then
   installs the model into a read-only active model root.
3. **Provision a job** — a camera source, model, schedule and output mode are
   bound together as one EdgeX device, through the platform or a simple
   configuration file.
4. **Acquire frames** — RTSP, ONVIF, MJPEG or JPEG sources are sampled, with
   per-camera decoding shared across jobs.
5. **Infer and decode** — the model server answers, and the descriptor-selected
   decoder turns raw tensors into normalized, structured events.
6. **Publish and preview** — events enter the EdgeX message bus (and can flow
   north through [NereidEdge](nereidedge.md)), while the annotated preview
   shows what was detected.

## Where NIN sits in the suite

NIN is the on-site execution step of the model loop, alongside Edge:

- **Forge → NIN:** Forge produces the model package (ONNX or OpenVINO IR
  today; other artifact formats can be declared by descriptor).
- **Horizon → NIN:** Horizon distributes packages to the gateway's local
  object store; NIN watches and activates them.
- **NIN ↔ model servers:** OVMS, Triton, vLLM or MindIE run as independent
  services; NIN is their client over KServe gRPC v2 or OpenAI-compatible HTTP.
- **NIN → EdgeX / Edge:** structured events enter the EdgeX bus and can flow
  north through the same edge integration Edge provides toward Link.

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

## Technical overview

This section is for technical evaluators; nothing above it requires a machine
learning background.

| Aspect | Detail |
|---|---|
| What it is | EdgeX device service for descriptor-driven media inference on field gateways |
| Positioning | On-site inference runtime of the model closed loop |
| Frame sources | RTSP (H.264/H.265 via per-URL ffmpeg), ONVIF camera/snapshot, MJPEG, JPEG |
| Inference protocols | KServe gRPC v2, OpenAI-compatible HTTP |
| Model servers | OpenVINO Model Server, Triton, vLLM, MindIE (independently deployed); managed OVMS/Triton plus read-only external servables |
| Model packaging | Gzip tar package with a root `nereid-model.json` descriptor, delivered via Horizon ESS or a watched inbox |
| Decoder coverage | Detection, classification, segmentation, pose, embeddings, dense maps, image output, OCR/CTC, LLM/VLM text, composites — selected purely by descriptor |
| Scheduling | Per-job FPS/periodic/event/manual triggers, one in-flight inference, drop-oldest semantics, default 64-job node limit |
| Output | Structured EdgeX events; optional unauthenticated annotated MJPEG preview (container port 18080, host 28080) |
| Service ports | 59992 service port (provisional, pending EdgeX TSC assignment) |
| Stack | Static Go binary on EdgeX Foundry 4.0 (`CGO_ENABLED=0`), credential-dropped ffmpeg child process; linux/amd64 and linux/arm64 images |
| License | Apache-2.0 |

## Resources

- GitHub: [NereidInference](https://github.com/NereidAI/NereidInference)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Edge delivery](../deployment/edge-delivery.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
