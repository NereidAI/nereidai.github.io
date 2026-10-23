# Getting Started

NereidForge (Forge) is the privatized **model factory** of the NereidAI suite:
one production line that turns your own data into field-ready models —
prepare data, annotate, train, optimize, evaluate, register and deploy, all
running on-premises and fully offline. Data never leaves your network, and
every dataset, model version and evaluation report is retained as an
organizational asset. See the [product page](../../products/nereidforge.md)
for the full capability overview.

Forge covers **two model families** on the same production line:

| Track | Typical models | Output |
|---|---|---|
| **Computer vision (CNN)** | RT-DETR-style detectors, SAM (segmentation), timm/TorchVision (classification) | ONNX / quantized runtimes for CPU, Intel, NVIDIA, AMD |
| **LLM / VLM** | Qwen / LLaMA-family text and vision-language models | LoRA / QLoRA adapters and merged checkpoints, served via vLLM-compatible runtimes |

## The production line

```
        datasets ──► annotations ──► training ──► optimization ──► evaluation
            (versions)   (pre-label)   (CV | LLM/VLM)   (ONNX/int8)     (metrics)
                                                                        │
                                                                        ▼
                                                  model registry ──► deployment (KServe)
                                                                        │
◄──────────────────────── field data / new images feed a new round ─────┘
```

Every stage writes an immutable, versioned artifact, so any model can be
traced back to the exact dataset version and base model that produced it.

## The pages in this manual

| Stage | Page | What you do there |
|---|---|---|
| 1 | [Datasets](datasets.md) | Create datasets, upload images/ZIP or text corpora, manage immutable versions |
| 2 | [Annotations](annotations.md) | Label in Label Studio / CVAT, run ML-assisted pre-labeling, export |
| 3 | [ML Backend](mlbackend.md) | Register the pre-labeling service that predicts boxes/labels for annotators |
| 4 | [Training](training.md) | Run CV or LLM/VLM training on CPU/GPU from multiple vendors; bring your own framework via the [Trainer SDK](trainer-sdk.md) |
| 5 | [Optimization](optimization.md) | ONNX graph optimization and int8 quantization per target device |
| 6 | [Evaluation](evaluation.md) | Score mAP / Precision / Recall / F1 and latency, compare to the baseline |
| 7 | [Models](models.md) | Browse versions, try a model on an image, deploy with KServe |

## Core concepts

- **Dataset version** — every upload or annotation export is a new, immutable
  version. Training always references one fixed version, so a run is
  reproducible.
- **Base model** — a starting point from the model pool: a detection checkpoint
  (such as RT-DETR) for CV, or a pretrained LLM/VLM (for example a Qwen model)
  for fine-tuning.
- **Job** — one asynchronous pipeline run (training, optimization,
  evaluation, export). The cluster schedules CPU/GPU automatically; progress,
  logs and curves are available on the job detail page.
- **Model version** — the output registered in the model library. Trained,
  optimized and manually uploaded artifacts all become versions of one model,
  keeping their lineage and metrics.
- **Artifact storage** — images, checkpoints and reports are stored in the
  on-premises S3-compatible store (SeaweedFS); the database and message plane
  never carry the bulk bytes.

## Your first CV model (15-minute tour)

1. **Prepare data** — on the Datasets page, create a dataset (COCO/TXT) and
   upload jpg/png images or a ZIP (images at the archive root or in an
   `images/` folder). Ingestion is asynchronous; the upload becomes version 1.
2. **Annotate** — on the Annotations page, create a project (detection,
   segmentation or classification), open the embedded Label Studio workbench,
   and draw a few labels. Optionally choose a registered model in the project
   header and run **Semi-automated annotation**, then correct the suggestions.
3. **Export** — export to TXT. The export is registered as a new,
   training-ready dataset version.
4. **Train** — on the Training page, pick the exported version, a base model
   (RT-DETR-R18 is a safe start), and accept the suggested hyperparameters
   (epochs 100, imgsz 640, batch 16, train/val 0.8). Forge splits train/val
   and runs a real Kubeflow Pipelines run.
5. **Optimize** — on the Optimization page, select the trained version and a
   target device (CPU / Intel OpenVINO / NVIDIA TensorRT / AMD / Ascend). Each
   target independently runs ONNX optimization and int8 quantization and
   reports measured speedup, size and latency.
6. **Evaluate** — on the Evaluation page, score a version against the val
   subset. Review mAP50 / Precision / Recall / F1, and the `accuracy_drop` of
   a quantized version. If precision is 0, lower the confidence threshold to
   0.25 and retry.
7. **Deploy** — on the Models page, select a version, choose a serving runtime
   (OpenVINO on CPU, Triton on GPU), and create the KServe service. Forge
   creates the InferenceService and Ingress and returns the endpoint domain.

## Your first LLM / VLM

The same loop applies, with two differences:

- **Data** — create a dataset of format **LLM-SFT**: a sharegpt-style JSONL
  corpus (one conversation per line), plus an `images/` folder for VLM. Text
  projects in the annotation workbench export directly to this format.
- **Training** — choose an LLM/VLM base model. NVIDIA and AMD runs use the
  LLaMA-Factory trainer; Intel Arc uses the native transformers + PEFT route
  (LoRA/QLoRA). Pick the accelerator that matches your node on the training
  form; without a GPU the form falls back to CPU.

!!! tip "The loop repeats"
    Field data starts the next round: upload it as a new dataset version,
    annotate the gaps, retrain, optimize and re-evaluate. Every model version
    keeps its data, metrics and deployment history — the factory gets faster
    the more it runs.
