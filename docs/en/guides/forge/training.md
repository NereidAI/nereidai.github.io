# Training

Training runs a real pipeline job on the cluster from a fixed dataset version
and registers the result as a new model version. It is not a mock: a trainer
container runs on CPU or GPU, emits live loss curves and logs, and uploads
artifacts into object storage on completion.

Forge schedules the work through Kubeflow Pipelines; you only fill the
training form. Two training routes share the same job machinery.

## Two training routes

| | Computer vision | LLM / VLM |
|---|---|---|
| Input dataset | COCO / YOLO / ImageNet version | LLM-SFT / sharegpt JSONL (`+ images/` for VLM) |
| Base model | YOLO / RT-DETR / timm checkpoint | Qwen / LLaMA-family pretrained model from the base-model pool |
| Trainer | Ultralytics / timm template (`train.py`) | LLaMA-Factory (NVIDIA, AMD) or native transformers + PEFT (Intel) |
| Method | Full training / fine-tuning | SFT with LoRA / QLoRA adapters (or merged checkpoint) |
| Outputs | `.pt` + `.onnx`, metrics | adapter / tokenizer / processor, `history.jsonl`, metrics |
| Accelerators | CPU, NVIDIA, AMD, Intel | NVIDIA, AMD, Intel (QLoRA), CPU fallback |

## Accelerators: one form, vendor-specific images

Forge uses an **accelerator profile** abstraction: you pick the target on the
form (only resources the cluster reports as allocatable are offered), and the
platform selects the matching trainer image variant, Kubernetes resource and
PyTorch backend:

| Vendor | K8s resource | Image suffix | Backend |
|---|---|---|---|
| NVIDIA | `nvidia.com/gpu` | `-cu` | CUDA PyTorch / LLaMA-Factory |
| AMD (RDNA) | `amd.com/gpu` | `-rocm` | ROCm / HIP, LLaMA-Factory |
| Intel Arc | `gpu.intel.com/xe` | `-xpu` | native `torch.xpu` + PEFT |
| CPU | — | default | CPU image |

Support is honestly graded and depends on your hardware:

- **Certified** — end-to-end training verified on real devices (for example
  Intel Arc is certified for CV, LLM QLoRA and SmolVLM VLM-LoRA on the
  reference node).
- **Compatible / build-only** — the image exists but CV or full E2E is not yet
  certified on that silicon.
- When the cluster has no matching device, the job cannot be scheduled there;
  pick an available accelerator or CPU rather than assuming a GPU is present.

## Create a training job

1. Open the **Training** page and choose the task type (CV detection /
   segmentation / classification, or LLM / VLM).
2. Select the dataset version (an annotation export or an LLM-SFT corpus).
3. Select a base model from the pool.
4. Set hyperparameters; the CV defaults are a safe starting point:

| Parameter | CV default | Notes |
|---|---|---|
| epochs | 100 | LLM/VLM fine-tuning typically uses 1–5 epochs |
| imgsz | 640 | Inference/training image size |
| batch | 16 | Reduce on smaller VRAM; the trainer errors clearly on OOM |
| train/val ratio | 0.8 | Forge performs the split and keeps the val set for evaluation |

5. Choose the accelerator that matches your node, then submit.

For LLM/VLM jobs the form additionally exposes the fine-tuning method
(full / LoRA / QLoRA), rank and LoRA hyperparameters; VLM jobs accept the
vision-language base model and the sharegpt + images corpus.

## While a job runs

- **Status & progress** — the job moves through queued, running, succeeded or
  failed; progress reaches 100% on success.
- **Curves** — the **Training curves** tab plots per-step/per-epoch loss and
  evaluation metrics (CV reads the trainer's results; LLM/VLM plots the
  step-level `history.jsonl`).
- **Logs** — the log view shows the real trainer pod's standard output (loss
  lines, upload confirmation), falling back to pipeline-executor logs if the
  pod has ended.
- **Artifacts** — on success the trainer uploads weights, ONNX (CV), metrics
  and tokenizer/processor files, and a model version is registered
  automatically under the job name.

Checkpoints are written during training, so an interrupted run can be resumed
from its checkpoint; a failed job can also simply be restarted.

## Bring your own trainer

When the built-in templates cannot express a workflow, a CV/PyTorch job can
use a **custom image** and/or a **custom training script**:

- `custom_image` — any private registry image with Python on `PATH`; it
  becomes the trainer container.
- `custom_script_uri` — an `s3://` or `http(s)://` URL to a Python file,
  downloaded into the container and executed as `__main__`.

The script receives the standard trainer environment (`INPUT_URI`,
`OUTPUT_DIR`, `CONFIG_JSON`, `ARTIFACT_ID`, `S3_*` credentials) and uploads
its model to `OUTPUT_DIR`. Uploading a `<artifact>.metrics.json` with
`weights_uri`/`onnx_uri` registers the version precisely; otherwise the worker
scans the output prefix and registers the best artifact (`.onnx` preferred,
then `.pt/.pth/.safetensors`). LLM/VLM jobs go through LLaMA-Factory / the XPU
trainer and do not use these selectors.

## FAQ

!!! question "Where are the curves?"
    On the job detail page, in the **Training curves** tab. They populate as
    the trainer writes them, not before the first epoch/step lands.

!!! question "The job is stuck pending?"
    The requested accelerator is not allocatable. Check cluster nodes, free
    GPU memory and device plug-ins, then resubmit on an available profile
    (including CPU for a smoke test).

!!! question "How is training data chosen?"
    You pick one immutable dataset version; Forge splits train/val at the
    ratio you set. The held-out val split is what [Evaluation](evaluation.md)
    uses by default, which avoids evaluating on training images.

!!! question "What if it is interrupted?"
    Resume from checkpoint or restart the job. Dataset and base model are
    fixed on the job, so a rerun is comparable.

## Next steps

- Compress for the edge: [Optimization](optimization.md).
- Measure quality and latency: [Evaluation](evaluation.md).
- Inspect, try and deploy the result: [Models](models.md).
