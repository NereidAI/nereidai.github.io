---
title: Edge model inventory and camera inference bindings, explained
date: 2026-11-20
authors:
  - maintainers
categories:
  - Engineering
slug: edge-model-inventory-explained
---

# Edge model inventory and camera inference bindings, explained

Once a fleet of gateways starts running AI locally, a deceptively simple
question becomes hard to answer: **which models are actually on which box, and
are they healthy?** NereidLink's Edge models feature answers that question
without the platform ever touching a model file. This post walks through how it
works, based on the [Edge models guide](../../guides/link/edge-models.md).

<!-- more -->

## A control plane that never holds the models

The Edge models tab appears on a gateway only when its firmware negotiates the
`inference` capability during the hello handshake. From that point on, the
gateway reports the AI models physically present on its storage.

The boundary is deliberate: NereidLink never stores, proxies, or transfers
model bytes. It keeps only the **inventory the gateway reports**, renders it,
and raises alarms when a model or the inference runtime is unhealthy. The
actual artifacts travel through the model factory and edge distribution path —
[NereidForge](../../products/nereidforge.md) builds and optimizes them,
[NereidHorizon](../../products/nereidhorizon.md) delivers them, and
[NereidInference](../../products/nereidinference.md) serves them at the edge.

## Three independent status planes

Model health is reported on three planes that fail independently, so an
operator can tell what is actually wrong:

1. **Inference runtime** — the serving process itself (for example a
   KServe/OpenAI-compatible runtime), read from the gateway's device shadow as
   `ONLINE`, `DEGRADED`, or `OFFLINE`. If no health report arrives within three
   probe intervals, the card shows Unknown/stale rather than guessing. It also
   surfaces ready-versus-total model counts, active bindings, and last reported
   latency.
2. **Model inventory** — every model the gateway last reported, each with its
   own lifecycle state: `EXTRACTING`, `VALIDATING`, `READY`, `FAILED`, or
   `REMOVED`.
3. **Bindings** — the `edge-inference` connector instances on the gateway and
   their applied state (`APPLIED`, `DEGRADED`, `FAILED`).

A failed binding does not imply a failed model, and a degraded runtime does not
invalidate the inventory; the separate planes keep those stories apart.

## Inventory semantics: full replacement, with a safety net

Each gateway manifest carries a full `models` segment, and every report is a
**complete replacement**: models missing from a new list are removed, and an
explicit empty list means the gateway currently holds zero models. Older
firmware that does not send the segment leaves the stored inventory untouched.

Rows carry the facts an operator needs without interpretation — model id,
semantic version, build revision, task family (such as `detection`), the
post-processing family (such as `yolov8`), the concrete model-server family
when the firmware knows it (`ovms`, `triton`, `external`) plus the wire
protocol family underneath it, and the model's class labels shown verbatim.

Two stale conditions keep an inventory honest: if manifests stop entirely, or
if a gateway that previously reported models keeps sending manifests without
the `models` segment for more than fifteen minutes, lingering rows are tagged
**Stale** rather than deleted, and a stale model cannot be selected for a new
binding.

## From a camera and a model to a running binding

The **Bind inference** wizard turns one camera and one `READY` model into a
detection binding in a single action, enabled only when at least one healthy
model exists. The design choices underneath the wizard encode a lot of field
experience:

- **Three acquisition modes.** Snapshot JPEG for lightweight periodic checks;
  an RTSP video stream resolved locally from ONVIF registration, with the
  stream profile picker and credentials that never leave the gateway; and a
  direct-URL mode for non-ONVIF cameras, where transport, URL, and a named
  edge secret are supplied explicitly. A bad feed is rejected —
  `config-invalid` at apply time, `source-no-frame` at runtime — never silently
  swapped for another source.
- **Triggers match the workload.** On-demand inference with an idle guard,
  periodic inference every configured interval, or continuous inference at a
  steady frame rate for video streams.
- **Target device is a hard requirement.** CPU, a specific GPU index, NPU, or
  an accelerator composite form can be selected, and the edge must report
  `target-device-unavailable` rather than silently falling back to CPU.
  Hardware decoding through VA-API follows the same rule: no driver, no
  automatic software fallback.
- **Evidence is optional and explicit.** Annotated evidence JPEGs can be
  attached to every result event or switched off to save uplink bandwidth, and
  custom ffmpeg arguments are restricted to a small allowlist.

Every binding creates a virtual output sub-device whose identity is the
camera, profile, and exact model id/version, so the same camera can run
multiple model versions in parallel while a rebind deterministically reuses
the existing output device.

## Alarms close the loop

The platform raises deduplicated alarms that auto-clear on recovery:
`GATEWAY_MODEL_FAILED` per failed model, `GATEWAY_MODEL_STALE` while a lease or
the models segment goes quiet, `GATEWAY_INFERENCE_RUNTIME` for offline or
silent runtimes, and the generic connector alarms for degraded or failed
bindings. Inventory reads require only the `connector:read` permission, and the
API returns an empty list — never a null — for a gateway with no models.

The full field-level reference, including every binding option and alarm
condition, lives in the [Edge models guide](../../guides/link/edge-models.md), and
the broader device lifecycle is covered in the
[NereidLink product overview](../../products/nereidlink.md).
