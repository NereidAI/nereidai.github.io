# ML Backend

The ML Backend is the service behind **semi-automated annotation**: when an
annotator requests pre-labeling, it predicts boxes, masks or labels on the
unlabeled tasks and writes them into the workbench as editable predictions.
People then review and correct instead of drawing every label from scratch —
this is the "machine first, human review" step of the factory's flywheel.

It implements the standard **Label Studio ML Backend protocol**, so it plugs
into the embedded Label Studio directly, and the same inference also serves
CVAT pre-annotation and the model trial feature.

## What it is — and is not

- It is a **model-agnostic routing layer**, not one fixed model. Per request
  it loads the model version the project selected and routes by family:

```
/predict
   ├── CNN (detection / segmentation / classification) ──► ONNX Runtime / Triton
  └── LLM / VLM (vision-language or text) ───────────────► vLLM-compatible OpenAI endpoint
```

- The image ships **no bundled weights**. All models live in the platform's
  S3-compatible store and are loaded on demand into bounded in-memory caches,
  so one shared service serves every model version you upload; idle memory
  stays small and unused models are evicted automatically.
- It is a backend for the **annotation workbench**, not the production
  serving path — field inference of approved models uses KServe deployments
  from the [Models](models.md) page.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health probe (the console's reachability check requires status `UP`) |
| `GET /setup` | Model information, supported labels and version |
| `POST /predict` | Batch prediction used to pre-fill annotations |
| `POST /train` | Optional trigger for interactive training |
| `POST /try/predict` | Single-image trial used by **Try with image** (boxes / top-5 / timing) |
| SAM segment route | Click-to-segment in the CVAT video editor with an uploaded `sam` model |

## Register the backend

1. On the **ML Backend** page, register the service with a name and its URL.
2. Use the **shared in-cluster service address** provided by the platform
   install. Do not invent a host name or use an external/host address: the
   workbench pod runs inside the cluster and cannot resolve host domains, and
   the shared service has no external ingress by design.
3. The console performs a real `GET /health` probe; a reachable service
   reports healthy.

The normal flow does **not** require a per-model backend: keep the shared
service, and choose the concrete model version in each annotation project's
header. A separately deployed, dedicated backend is only needed for advanced
isolation — it can be created from a registered model through the custom
backend deployment (a per-model Kubernetes Deployment + Service).

## Choose the pre-labeling model per project

In the annotation project header (both Label Studio and CVAT), select a model
and version for pre-labeling. The choice is stored on the project and applied
to batch and single-image pre-labeling:

- Only detection/segmentation models with weights are offered (SAM appears in
  the video editor separately).
- With no model selected, the semi-automated button is disabled with an
  explanatory tooltip — there is no silent built-in fallback.
- A model you just trained can be selected immediately, so each iteration
  pre-labels the next batch better.

Requests are batched to stay within the service timeout; predictions return
in input order and are mapped back to the images automatically.

## Model support

- **Detection:** RT-DETR-style single-stage detectors (PyTorch or ONNX);
  legacy detection checkpoints that cannot be loaded directly are served via
  their ONNX artifacts.
- **Segmentation:** SAM-family models for click-to-segment (upload a version
  with task type `sam`; the checkpoint must keep an official SAM-compatible
  file name).
- **Classification:** PyTorch/ONNX classifiers, top-5 output.
- **VLM/LLM:** Qwen-VL / Florence-2 style models through the vLLM route for
  label/box suggestions and text annotation.
- A detector may ship with its own default confidence threshold; the project's
  configured threshold is passed through, so tune it in the project rather
  than assuming a later filter has an effect.

## Troubleshooting

!!! question "The backend shows unreachable / unhealthy?"
    Verify the registered URL is the shared in-cluster service address from
    the install guide. A browser/host URL fails DNS from the workbench pod,
    and the old namespace address from a previous install is invalid after
    migration. `GET /health` must return status `UP`.

!!! question "Pre-labels are empty or labels do not match?"
    The selected model's classes must match the project's label schema, and
    the model version must have weights. Weak or low-confidence predictions
    (below threshold) are intentionally not inserted — lower the threshold or
    pick a stronger/newly trained model.

!!! question "A newly selected model seems ignored?"
    The service loads weights on demand and caches per artifact. After
    re-uploading weights to the **same** storage key, restart/roll the backend
    to drop the cached copy; prefer uploading a new version/key instead.

!!! question "Where are large images cached?"
    Downloaded images use a dedicated scratch directory with an LRU cap
    (separate from the weights directory); weights and media never pollute
    each other and the service logs evictions and every predict call.

## Next steps

- Use it in the workbench: [Annotations](annotations.md).
- Train a model, then loop it back as the pre-labeler: [Training](training.md).
- One-off checks of a version: [Models](models.md) → **Try with image**.
