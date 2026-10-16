# Evaluation

Evaluation scores a model version against a dataset and reports real metrics, so you can decide whether a version is ready to deploy or needs another optimization round.

## Flow

1. **Create an evaluation task** — select a model (version) and a dataset.
2. **Adjust the parameters** — confidence threshold, maximum image count, and task type (suggested defaults below).
3. **Choose the data** — by default evaluation uses the val subset produced during training; any dataset version can be selected instead (converted to YOLO automatically).
4. **Review the metrics** — on completion, real metrics are shown: mAP50 / Precision / Recall / F1 / latency.

| Parameter | Suggested value |
|---|---|
| Confidence threshold | 0.25 |
| Maximum image count | 0 (all images) |

## Prerequisites

- The model must have an ONNX artifact.
- The dataset must be parseable as YOLO (handled automatically).

## FAQ

!!! question "Why is precision 0?"

    The model has not converged, or the threshold is too high so too few predictions are produced. Lower the confidence threshold and retry.

!!! question "Which data is evaluated?"

    The training val subset by default, to avoid data leakage.

## Next steps

Once the score is acceptable, deploy from the [Models](models.md) page; otherwise return to [Optimization](optimization.md) and keep tuning.
