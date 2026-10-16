# Optimization

A trained model is usually too large or too slow for a field device.
Optimization compiles the model to ONNX, applies graph optimization and
**int8 quantization** for a chosen target silicon, and benchmarks the result
on that target — so you trade a controlled, measured accuracy drop for
latency, throughput and storage gains.

Each **(source version × target device)** combination is an independent job
and produces its own model version. Selecting several targets fans out into
several runs in one submission.

## Target devices

Targets are vendor-first: selecting a vendor maps to the runtime/export path
the optimizer uses.

| Selection | Optimizer target | Typical runtime in the field |
|---|---|---|
| CPU | `cpu` | ONNX Runtime (CPU) |
| Intel | `openvino` | OpenVINO |
| NVIDIA | `tensorrt` | TensorRT / Triton |
| AMD | `onnx-rocm` | ONNX Runtime (ROCm) |
| Huawei Ascend | `ascend` | Ascend runtime |

Legacy values (`cpu`, `openvino`, `tensorrt`, …) are accepted as-is. A target
whose toolchain or hardware is absent from the cluster stays pending rather
than failing silently — run it on a node that has that accelerator.

## What the pipeline does

1. Take the source version's ONNX artifact (training emits one; a manually
   uploaded `.onnx` works too).
2. Run ONNX graph optimization for the target.
3. Quantize weights/activations to int8 with a calibration set.
4. Benchmark source vs. optimized with ONNX Runtime on the target — this is a
   **real measurement**, not an estimate.
5. Register the result as a new version with measured metrics and a gate
   verdict.

The optimized artifact lands in object storage (SeaweedFS) and is registered
under the source model with a name like
`{source-version}-onnx-{dtype-suffix}`, so every optimized version keeps its
lineage to the trained model.

## Metrics and quality gates

Each optimized version records:

- **Speedup** — optimized vs. source latency on the same target.
- **Size reduction** — artifact bytes before vs. after.
- **Latency** — measured inference latency (the optimization sweep can search
  parameter combinations, minimizing latency subject to a hard mAP-drop
  bound).
- **Accuracy drop** — evaluation metrics of the quantized model against the
  FP32 source (for example `mAP50` delta).

The gate separates what must never regress from what an operator may accept:

- **Hard gate** — task-accuracy drop and numerical safety (NaN/Inf). A failed
  hard gate blocks automatic registration.
- **Soft gate** — performance targets such as latency/throughput; a miss is
  flagged (YELLOW) and can be reviewed and manually released with the gate
  recorded, rather than hidden.

Always confirm the int8 model's accuracy on the [Evaluation](evaluation.md)
page before deploying it; quantization is hardware- and data-dependent.

## Prerequisites

- The source version must have an **ONNX artifact**. Train it in Forge (the CV
  trainer exports ONNX) or upload an `.onnx` manually to the model library.
- The matching hardware/toolchain for GPU/NPU targets must exist in the
  cluster; otherwise the task stays pending.
- Use a representative calibration set — quantization quality follows the data
  it calibrates on.

## FAQ

!!! question "Where does the speedup number come from?"
    From a real benchmark (`optimize.py` via ONNX Runtime) comparing the
    source and optimized models on the target, not from a table of estimates.

!!! question "Can I optimize for several chips at once?"
    Yes — select multiple targets in one task; Forge creates one independent
    job and one output version per target, then compares them in the model
    library.

!!! question "The int8 model lost too much accuracy."
    Re-run with a more representative calibration set; if the drop still
    exceeds the gate, keep the FP32/FP16 version for that target or choose a
    less aggressive path. Review `accuracy_drop` in evaluation.

!!! question "Does this optimize LLM/VLM models?"
    This page describes the CV ONNX/int8 line. LLM/VLM serving efficiency is
    handled primarily through LoRA/QLoRA adapters at [training](training.md)
    time and the chosen serving runtime; a single-page CV quantizer is not
    applied to large language checkpoints.

## Next steps

- Verify the optimized version: [Evaluation](evaluation.md).
- Pick the winning target and deploy: [Models](models.md).
