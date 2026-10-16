# Optimization

Optimization compiles and quantizes a trained model for one or more target devices. Each target produces an independent task; artifacts are registered as new model versions with real benchmark metrics.

## Flow

1. **Create an optimization task** — select a source model (version) and one or more target devices.
2. **Multiple targets** — you can select several devices (CPU / OpenVINO / NVIDIA, etc.); each target generates an independent task.
3. **Automatic processing** — the platform performs ONNX graph optimization plus int8 quantization. Artifacts land in SeaweedFS and are registered as a new model version carrying a target suffix.
4. **Compare and select** — optimized versions carry real metrics such as speedup and size reduction; compare them in the model library when choosing a version.

## Prerequisites

- The source model must have an ONNX artifact (an `.onnx` produced by training or uploaded manually).
- Targets such as NVIDIA/TensorRT require the matching hardware/toolchain. When the cluster has no such hardware, the task is marked pending.

## FAQ

!!! question "Where does the speedup figure come from?"

    A real benchmark run by `optimize.py` with ONNX Runtime — not an estimate.

!!! question "How do I use an optimized model?"

    Optimized versions are registered under the source model and can be deployed or evaluated.

## Next steps

- Verify the optimized version's accuracy (`accuracy_drop`) on the [Evaluation](evaluation.md) page.
- Or deploy it from the [Models](models.md) page.
