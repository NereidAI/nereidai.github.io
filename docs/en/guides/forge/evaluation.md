# Evaluation

Evaluation scores a model version against a labeled dataset with a real
inference pass, so you can decide whether a version is good enough to deploy —
or needs more data, retraining or a different optimization target. It also
gives the FP32-vs-quantized comparison that makes an optimization result
trustworthy rather than just faster.

## What is measured

For computer-vision models Forge reports the standard detection/classification
metrics plus end-to-end latency:

| Metric | Meaning |
|---|---|
| **mAP50** | Mean Average Precision at IoU 0.50 — the headline detection score |
| **mAP50-95** | mAP averaged over IoU 0.50–0.95 — rewards tight, accurate boxes |
| **Precision** | Of the predicted boxes, the fraction that are correct |
| **Recall** | Of the real objects, the fraction that were found |
| **F1** | Harmonic mean of precision and recall |
| **Latency** | Measured per-image inference time on the evaluation runtime |

For optimized (ONNX/int8) versions, compare against the source FP32 version:
the **accuracy drop** (for example the mAP50 delta) is the number the
[optimization](optimization.md) quality gate uses, alongside latency and size.

## Run an evaluation

1. On the **Evaluation** page, choose a model version and a dataset.
2. Set the parameters:

| Parameter | Default | Notes |
|---|---|---|
| Confidence threshold | 0.25 | Detections below it are ignored; lower it when a model under-predicts |
| Maximum images | 0 | 0 means the whole dataset; cap it for a quick check |
| Task type | from the model | Detection / segmentation / classification |

3. Submit. The dataset is converted to the layout the evaluator needs
   automatically.
4. Read the metrics table and, for an optimized version, the drop relative to
   its FP32 source.

## Which data to evaluate on

- By default evaluation uses the **val split produced at training time**. This
  prevents accidentally scoring on the training images (data leakage) and
  makes different versions directly comparable.
- You can point the job at any other dataset version instead — for example a
  newly collected field batch — to measure real-world behavior. Keep that
  dataset separate from training if you want an honest number.

## Interpreting the result

- **mAP high, latency high** → keep accuracy, deploy on stronger hardware or
  optimize more aggressively.
- **Large quantized drop** → revisit calibration data or keep FP16/FP32 for
  that target.
- **Low recall** (objects missed) → add examples of those scenes to the next
  dataset version and retrain.
- **Low precision** (false boxes) → raise the confidence threshold or add
  hard-negative images.

## Quick sanity check without a job

On the [Models](models.md) page, **Try with image** runs one uploaded image
through any version directly — drawing detected boxes (or showing
classification top-5 and timing) without creating a KServe deployment. The
Grad-CAM overlay on PyTorch versions visualizes where a detector/classifier is
looking. It is an interactive check, not a replacement for dataset-level
metrics.

## LLM / VLM versions

The benchmark metrics above are the computer-vision evaluation. For fine-tuned
LLM/VLM versions, use the training run's loss / eval-loss curves and
step-level history to confirm convergence, and validate behavior on your own
prompt/reference set with the trial-inference path before serving.

## FAQ

!!! question "Why is precision 0?"
    Either the model has not converged, or the confidence threshold is too
    high so almost no boxes survive. Lower the threshold (0.25 is the usual
    starting point) and rerun; also check that the evaluation dataset's
    classes match the model's classes.

!!! question "Which dataset is used by default?"
    The validation split generated during training, so training data is not
    reused for the score.

!!! question "The model needs an ONNX artifact?"
    Evaluation runs on the available model artifact; conversion is handled by
    the pipeline. If a version has no runnable artifact, train or upload one
    first.

## Next steps

- Accept the version and deploy it: [Models](models.md).
- Improve speed/size again: [Optimization](optimization.md).
