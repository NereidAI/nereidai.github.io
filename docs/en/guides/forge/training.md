# Training

Training runs a real Kubeflow Pipelines (KFP) job from a dataset version and registers the result as a new model version in the model library.

## Flow

1. **Create a training task** — select a dataset (version), a base model, and hyperparameters.
2. **Fill the structured form** — suggested defaults are listed below.
3. **Start the run** — Forge automatically splits train/val and runs the KFP pipeline (real training).
4. **Get the result** — on completion the model version is registered to the model library automatically, and training curves are generated.

| Parameter | Suggested value |
|---|---|
| Base model | YOLOv8n |
| epochs | 100 |
| imgsz | 640 |
| batch | 16 |
| train/val ratio | 0.8 |

## Prerequisites

- The dataset must be in YOLO format. An annotation export satisfies this automatically; for raw COCO, `data.yaml` is generated automatically.
- Training resources (CPU/GPU) are matched automatically by the cluster; without a GPU, CPU is used.

## FAQ

!!! question "Where are the curves?"

    The **Training curves** tab on the task detail page.

!!! question "What if the run is interrupted?"

    Failed tasks can be restarted; resume-from-checkpoint is supported for recovering from a checkpoint.

## Next steps

When training finishes, optimize the model on the [Optimization](optimization.md) page, verify its accuracy on the [Evaluation](evaluation.md) page, or deploy it from the [Models](models.md) page.
