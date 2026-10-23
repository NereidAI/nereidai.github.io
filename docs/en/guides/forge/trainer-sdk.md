---
title: Trainer SDK (Python)
---

# NereidForge Trainer SDK for Python

The Trainer SDK is for **teams that bring their own training framework** — a
detection model from another stack, a proprietary network, a classifier with
special preprocessing, an LLM/VLM fine-tuning recipe. It is the *only*
integration contract between a training component and Forge, and it is
deliberately tiny: **environment variables in, versioned artifacts out**.

- **Package:** `nereidforge-trainer` (import name `nereidforge_trainer`),
  Apache-2.0, Python ≥ 3.11, one runtime dependency (`boto3`).
- **No base class, no callbacks into the platform.** Forge never imports the
  trainer's code and the trainer never imports Forge's. Any framework, any
  library and any weights are allowed; a trainer whose upstream framework is
  not permissively licensed simply ships in its own image and repository.
- **Dogfooded:** the in-tree vision trainers (the torch trainer covering all
  vision tasks, and the PaddleX detection trainer) are built on this same SDK,
  so custom trainers get no second-class contract.

!!! info "Developer documentation"
    This page is a hands-on introduction. The package source, the full torch
    reference trainer and the capability-profile schema live in the
    NereidForge repository (`app/builders/sdk/`, `app/builders/trainer-torch/`)
    — see [NereidAI](https://github.com/NereidAI).

## When to use it

| You want to… | Use |
|---|---|
| Train with the built-in torch / PaddleX / LLM trainers and standard options | The [Training](training.md) form — no SDK needed |
| Run your own framework or training code as a Forge job | A custom trainer image built with this SDK |
| Run a one-off Python script without building an image | The `custom_script_uri` channel on a CV job (see [Training](training.md)) |
| Write a reusable, registerable trainer that appears in the Training form with its own architectures and device support | This SDK + a trainer image + capability profile |

## Install

The wheel ships with the Forge release (offline-friendly — there is no
internet dependency in the machine room):

```bash
# from the release source tree, or from any internal wheel mirror
pip install ./app/builders/sdk
```

Building a self-contained wheel for a customer image:

```bash
python -m pip wheel app/builders/sdk --no-deps -w ./wheels
# -> wheels/nereidforge_trainer-0.0.1-py3-none-any.whl
```

The package also installs the `nf-trainer` scaffolding CLI:

```bash
nf-trainer init my-detector --name acme/detector --task detection \
  --architecture acme-det --framework acme
nf-trainer validate my-detector/trainer-profile.json   # 0 ok · 1 invalid · 2 unreadable
nf-trainer profile  my-detector/trainer-profile.json   # pretty-print
```

`init` writes a ready-to-fill project into an empty directory: `train.py`,
`nf_profile.py`, `trainer_profile.py`, `trainer-profile.json`, `Dockerfile`,
`README.md`, `.gitignore`. It adds **no** framework dependency — you choose
the stack.

## The contract

### Environment variables

| Variable | Direction | Meaning |
|---|---|---|
| `INPUT_URI` | in | Dataset root: `s3://bucket/prefix…`, or a local directory in a smoke test |
| `OUTPUT_DIR` | in | Artifact destination: `s3://bucket/models/<job-id>/`, or a local directory |
| `CONFIG_JSON` | in | **Flat** training config — inline JSON or a path/URI to a JSON file |
| `ARTIFACT_ID` | in | Artifact basename (the job id); every artifact is named `<ARTIFACT_ID>.<ext>` |
| `S3_ENDPOINT` · `S3_ACCESS_KEY` · `S3_SECRET_KEY` · `S3_REGION` · `S3_BUCKET` | in | Object-store connection, injected by the platform (defaults exist for in-cluster use) |
| `NF_DEVICE` | in | Baked per vendor image: `cpu` / `cuda` / `rocm` / `xpu` |
| `NPROC` | in | Processes per node for multi-GPU `torchrun`-style launches |
| `SCRIPT` | in | Entrypoint selector: `train` (default) · `evaluate` · `export` · `catalog` · `profile` |

`CONFIG_JSON` is deliberately a flat JSON object — read it with one call and
treat unknown keys as your own hyperparameters:

```bash
export INPUT_URI=s3://nereidforge/datasets/ds-12/3/
export OUTPUT_DIR=s3://nereidforge/models/job-778/
export ARTIFACT_ID=job-778
export CONFIG_JSON='{"epochs": 50, "imgsz": 640, "batch": 16, "arch": "acme-det"}'
python train.py
```

### Output artifacts

Publish to `OUTPUT_DIR` with the artifact id as the basename:

| Object | Vision | LLM / VLM | Consumed for |
|---|---|---|---|
| `<id>.onnx` | required | — | Edge export / serving graph (opset 17; detector heads export without baked NMS) |
| `<id>.metadata.json` | required | — | Native model manifest — the only document the inference side trusts |
| `<id>.metrics.json` | required | required | Final flat metrics **plus `weights_uri` / `onnx_uri` / `manifest_uri`** — registers the version precisely |
| `<id>.pt` (or framework weights, e.g. `.pdparams`) | recommended | adapter directory | Resuming / re-export; LoRA adapters (`adapter_config.json` …) for LLM |
| `progress.json` | required | required | Live progress polled by the Forge worker (`progress_pct`, `current_epoch`, `total_epochs`) |
| `history.jsonl` | optional | typical | Per-step loss curves |

If `weights_uri` / `onnx_uri` are missing from `<id>.metrics.json`, the worker
falls back to scanning the output prefix (`.onnx` preferred, then
`.pt/.pth/.safetensors`); setting the URIs explicitly is the precise path.

### Datasets

`download_dataset(INPUT_URI)` mirrors every object under the prefix, preserving
keys, into `/data` by default. The canonical layouts are the same ones the
[Datasets](datasets.md) page describes: COCO or normalized TXT box labels
(images + per-image label files + a manifest YAML) for detection/segmentation/
pose, ImageFolder for classification, and sharegpt JSONL (+ `images/`) for
LLM/VLM. An un-split vision corpus is split deterministically at runtime using
the configured `split_ratio` (default 0.8).

## API surface

Everything is imported from the top-level package:

```python
from nereidforge_trainer import (
    read_config, write_json, Progress,
    download_dataset, publish_file, upload_file, s3_client, parse_uri, list_objects,
    build_manifest, manifest_outputs,
    resolve_augmentation, augmentation_summary,
)
```

| API | Purpose |
|---|---|
| `read_config(raw="") -> dict` | Read `CONFIG_JSON` (inline JSON or file/URI); empty → `{}` |
| `write_json(path, data)` | Atomic-ish local JSON helper |
| `Progress(output_uri, total_epochs)` | `.log(epoch, metrics)` appends to history and publishes `progress.json`; `.write(epoch, metrics, key="progress.json")` writes one record. Percentage caps at 99 until the job finalizes |
| `download_dataset(input_uri, local_root="/data")` | Mirror an `s3://` prefix (or copy a local dir) and return the local root |
| `publish_file(local_path, output_uri, name)` | Upload to `s3://…` **or copy into a local directory when `OUTPUT_DIR` is local** — the same code runs in-cluster and in a laptop smoke test. Returns the URI |
| `upload_file(...)` | Strict-S3 variant |
| `s3_client()` · `parse_uri(uri)` · `list_objects(...)` | Low-level S3 helpers wired to the injected env vars |
| `build_manifest(...)` | Build the native `<id>.metadata.json`: task, architecture, framework, input size, labels, per-task output tensor contract, preprocessing, metrics, dataset provenance, license |
| `manifest_outputs(task)` | The standard output-tensor contract for a task (`detection`, `instance_seg`, `semantic_seg`, `pose`, classification…) |
| `resolve_augmentation(cfg)` · `augmentation_summary(aug)` | Shared augmentation policy: presets `off`/`light`/`medium`/`strong` plus clamped per-knob overrides — the same knobs the UI offers |

## A minimal trainer

The whole lifecycle — config in, dataset download, progress, artifacts out:

```python
import os
from nereidforge_trainer import (
    Progress, read_config, write_json,
    download_dataset, publish_file, build_manifest,
)

cfg = read_config()
artifact_id = os.environ.get("ARTIFACT_ID", "model")
output_uri = os.environ.get("OUTPUT_DIR", "")
data_root = download_dataset(os.environ["INPUT_URI"])  # s3:// or local
epochs = int(cfg.get("epochs", 50))
labels = load_class_names(data_root)                  # your code

progress = Progress(output_uri, epochs)
for epoch in range(1, epochs + 1):
    train_one_epoch(epoch, cfg, data_root)            # your framework
    metrics = evaluate(epoch, cfg, data_root)         # {"mAP50": ..., ...}
    progress.log(epoch, metrics)                      # -> progress.json

# Framework-native checkpoint (resume / re-export)
save_checkpoint(f"/tmp/{artifact_id}.pt", labels)
weights_uri = publish_file(f"/tmp/{artifact_id}.pt", output_uri,
                           f"{artifact_id}.pt")

# Portable inference graph
export_onnx(f"/tmp/{artifact_id}.onnx")
onnx_uri = publish_file(f"/tmp/{artifact_id}.onnx", output_uri,
                        f"{artifact_id}.onnx")

# Native manifest — labels are 0-based, boxes are in model-input space
manifest = build_manifest(
    task="detection", architecture=cfg.get("arch", "custom"),
    framework="acme", input_size=int(cfg.get("imgsz", 640)),
    labels=labels, metrics=metrics,
    dataset={"version": cfg.get("dataset_version", "")},
)
manifest_path = f"/tmp/{artifact_id}.metadata.json"
write_json(manifest_path, manifest)
manifest_uri = publish_file(manifest_path, output_uri,
                            f"{artifact_id}.metadata.json")

# Final metrics document registers the model version precisely
final = {
    **metrics,
    "task": "detection",
    "architecture": cfg.get("arch", "custom"),
    "framework": "acme",
    "epochs": epochs,
    "weights_uri": weights_uri,
    "onnx_uri": onnx_uri,
    "manifest_uri": manifest_uri,
}
write_json(f"/tmp/{artifact_id}.metrics.json", final)
publish_file(f"/tmp/{artifact_id}.metrics.json", output_uri,
             f"{artifact_id}.metrics.json")
```

Console output follows one convention: plain `print(..., flush=True)` with
bracketed prefixes (`[train]`, `[data]`, `[export]`, `[evaluate]`,
`[progress]`); a user error exits with code **2**.

## Capability profile

A trainer image announces what it can do. The image carries
`/app/trainer-profile.json` and prints the same document when launched with
`SCRIPT=profile` (`python /app/nf_profile.py`). Forge stores the announcement
and renders tasks, architectures and device choices in the Training form from
it — no UI code changes per trainer.

```json
{
  "schema": "nf.trainer-profile/1",
  "name": "acme/detector",
  "framework": {"name": "acme", "version": ">=1.0"},
  "devices": ["cpu", "cuda"],
  "tier": "extended",
  "requires": ["extended.custom_trainer"],
  "tasks": [
    {
      "id": "detection",
      "label": "Object detection",
      "tier": "extended",
      "default_arch": "acme-det",
      "architectures": [
        {"id": "acme-det", "label": "Acme Detector", "size": 640,
         "params_m": 12.4, "tier": "extended", "license": "proprietary"}
      ]
    }
  ],
  "capabilities": [
    {"id": "export.onnx", "tier": "core", "entrypoint": "export"}
  ],
  "entrypoints": {
    "train": "python /app/train.py",
    "evaluate": "python /app/evaluate.py",
    "export": "python /app/export.py",
    "catalog": "python /app/catalog.py",
    "profile": "python /app/nf_profile.py"
  },
  "env": ["INPUT_URI", "OUTPUT_DIR", "CONFIG_JSON", "ARTIFACT_ID"],
  "artifacts": ["<id>.onnx", "<id>.metadata.json", "<id>.metrics.json", "<id>.pt"],
  "license": {"code": "proprietary", "weights": "per-model"}
}
```

Profile rules:

- `devices` are **per image**: `cpu`, `cuda`, `rocm`, `xpu`. Ship one image
  per supported silicon and bake `NF_DEVICE` into it; `--alias-type` style
  catch-all images are not a thing.
- Only announce tasks and architectures you actually implement;
  `default_arch` must exist in the architecture list.
- `tier` (`core` / `extended`) may be set at profile, task or architecture
  level — the most specific wins; an `extended` entry must list non-empty
  `requires` entitlement keys, checked when the job is created.
- Licenses are **recorded, not enforced**: declare the trainer code license
  and the per-model weights license; incompatible stacks stay isolated inside
  the customer's own image.
- The profile schema (`nf.trainer-profile/1`) is versioned independently from
  the SDK package version.
- The profile script must be named **`nf_profile.py`** — a file called
  `profile.py` at `/app` shadows the Python standard library.

### Register the image

An administrator registers the image under **System → Images** (category
*train*): a built-context image can announce its own profile, or the profile
JSON is pasted/uploaded against the image record. Its tasks and architectures
then appear in the Training form, and the accelerator choices offered are the
intersection of the profile's `devices` and what the cluster can allocate.

## Build and smoke-test locally

The generated `Dockerfile` installs the SDK from a pinned wheel (or a
build-arg wheel for air-gapped builds), bakes `ENV NF_DEVICE=cpu`, and
dispatches on `SCRIPT`:

```dockerfile
ARG SDK_WHEEL=
COPY ${SDK_WHEEL} /tmp/sdk.whl
RUN pip install --no-cache-dir /tmp/sdk.whl
# ...your framework and code...
ENTRYPOINT ["sh", "-c", "case \"${SCRIPT:-train}\" in \
  evaluate) exec python /app/evaluate.py;; \
  export) exec python /app/export.py;; \
  profile) exec python /app/nf_profile.py;; \
  *) exec python /app/train.py;; esac"]
```

Because `publish_file()` falls back to a local copy when `OUTPUT_DIR` is not
an `s3://` URI, the exact image can be smoke-tested on a laptop with a local
dataset:

```bash
docker run --rm \
  -v ./sample-dataset:/data:ro -v ./out:/out \
  -e INPUT_URI=/data -e OUTPUT_DIR=/out -e ARTIFACT_ID=smoke \
  -e CONFIG_JSON='{"epochs":1,"imgsz":640,"batch":4,"arch":"acme-det"}' \
  registry.example.internal/forge/acme-detector:v1
# -> ./out/smoke.onnx, smoke.metadata.json, smoke.metrics.json, progress.json
```

## Responsibilities

| The platform owns | The trainer owns |
|---|---|
| Scheduling, CPU/GPU allocation per vendor image | Reading `CONFIG_JSON` and validating its own hyperparameters |
| Dataset versioning, delivery to `INPUT_URI`, splitting | Consuming the dataset layout, the actual training loop |
| Injecting S3 credentials and endpoints | Publishing `progress.json` while the job runs |
| Progress UI, logs, job state machine | Exporting ONNX + manifest (vision) and writing final metrics |
| Registration from `<id>.metrics.json`, evaluation, optimization, deployment | Framework-native checkpoints; honest licenses in profile/manifest |

## Checkpoints and continuation

The SDK performs **no automatic resume**. A trainer saves its own checkpoint
(`<id>.pt`-style); continued/incremental training is driven through the config
key `base_weights_uri` (an `s3://` URI or a local path): materialize the
previous weights, transfer the backbone, re-initialize changed heads yourself,
and record the lineage (base URI, previous labels, added classes) in the
manifest's extra section. The optional `SCRIPT=export` entrypoint re-exports an
existing checkpoint to ONNX + manifest without training; `SCRIPT=evaluate`
writes only a metrics document.

## Current status

- SDK version **0.0.1**; the in-tree torch vision trainer (all vision tasks)
  and the PaddleX detection trainer are the first two consumers.
- LLM/VLM built-in trainers already honor the same environment-variable and
  `progress.json` / `metrics.json` conventions (adapter directory as
  `weights_uri`); SDK helper and profile coverage for LLM/VLM custom trainers
  is being aligned next.
- The `custom_script_uri` script channel is a quick-experiment path for CV
  jobs; the image + profile path described here is the supported way to
  distribute and register a reusable trainer.

## Next steps

- [Training](training.md) — how jobs, accelerators and custom images are
  selected from the UI.
- [Datasets](datasets.md) and [Annotations](annotations.md) — the layouts that
  arrive at `INPUT_URI`.
- [Models](models.md) — how the registered version is evaluated and deployed.
