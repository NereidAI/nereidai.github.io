# Models

The model library is where every model version is registered, compared, and deployed. Trained models land here automatically; external weights can be uploaded manually.

## Flow

1. **Register a model** — training registers the result automatically; you can also upload manually (`.pt` / `.onnx`).
2. **Manage versions** — each model has multiple versions; optimized versions record their target device and speedup.
3. **Compare and select** — the version table shows target device and speedup so you can pick the best version.
4. **Deploy** — select a version, then configure the runtime (OpenVINO/Triton), GPU, and domain name. Forge automatically creates a KServe service and an Ingress.

## Prerequisites

- Manual upload requires a model file such as `.pt` / `.onnx` / `.tflite`.
- The deployment domain must resolve in DNS. By default `<model>-<version>.inference.<platform-domain>` is generated.

## FAQ

!!! question "How do I reach a deployed model?"

    The deployment response returns the domain name; the Ingress is created automatically and DNS points to the cluster IP.

!!! question "Which runtime should I choose?"

    OpenVINO (CPU, verified) or Triton (reserved for GPU scenarios).

## Next steps

Use the inference endpoint after deployment, or continue optimizing and evaluating other versions: [Optimization](optimization.md) · [Evaluation](evaluation.md).

**First run?** Follow the end-to-end [Getting started](getting-started.md) walkthrough.
