# Models

The model library is the registry at the center of the factory: every trained,
optimized or imported version lands here with its lineage, metrics and
deployment history. From this page you compare versions, sanity-check a model
on an image, and publish it as a live inference service.

## Model and versions

- A **model** groups versions of the same solution; a **version** is one
  immutable artifact.
- Versions arrive three ways:
  1. **Training** — registered automatically on success (weights + ONNX for
     CV; adapters/tokenizer for LLM/VLM).
  2. **Optimization** — registered under the source model as
     `{source-version}-onnx-{dtype}`, carrying target device, speedup, size
     and accuracy-drop metrics.
  3. **Manual upload** — import `.pt` / `.pth` / `.onnx` / `.safetensors`
     (and related checkpoints); the framework is inferred from the suffix.
- Each version stores its framework (`pytorch` / `onnx` / …), task
  (detection / segmentation / classification / llm / vlm), source job,
  metrics and artifact URIs.

## Compare and select

The version table shows task, framework, target device and the measured
speedup/size for optimized versions. When several int8 targets exist, pick by
the latency/accuracy point you need rather than by name. Keep both the FP32
source and the quantized versions until the optimized one passes evaluation.

## Try a version on an image

Before deploying, use **Try with image** on a version row:

- Upload one image and set a confidence threshold; Forge runs it through the
  shared ML Backend using that exact version — **no KServe deployment needed**.
- Detection draws boxes with labels and scores; classification returns the
  top-5; elapsed inference time is reported.
- PyTorch (`.pt`) versions additionally support a **Grad-CAM** heatmap that
  shows the regions driving the prediction (ONNX has no gradients, so the
  toggle is unavailable there).
- Legacy detection checkpoints that cannot be loaded directly are served
  transparently via their sibling ONNX artifact (the UI marks this); the
  original `.pt` is never modified.

## Deploy with KServe

1. Select a version and open **Deploy**.
2. Choose a **serving runtime**. The list comes from the KServe
   `ClusterServingRuntime` definitions installed in the cluster — for example
   **OpenVINO** (CPU, the validated default) or **NVIDIA Triton** (GPU);
   vLLM-compatible runtimes for LLM/VLM appear when the cluster provides them.
3. Choose the accelerator/domain as the form requires and confirm.
4. Forge submits a pipeline that creates the KServe **InferenceService** and
   an **Ingress**, then records the service name, runtime and domain on the
   version.

By default the endpoint follows
`<model>-<version>.inference.<platform-domain>`; point DNS for that domain at
the cluster ingress. Deployments are asynchronous (typically 1–3 minutes) —
the Deployments list refreshes automatically and shows deploying / ready /
failed state straight from KServe.

**Undeploy** removes the InferenceService and Ingress; the model versions and
artifacts remain in the library and can be redeployed at any time.

## Prerequisites

- For manual import, provide a supported checkpoint/ONNX file.
- The runtime you choose must exist as a `ClusterServingRuntime`, and GPU/NPU
  runtimes need the corresponding device available on a node.
- The deployment domain must resolve in DNS to the cluster ingress address.
- KServe and its service account / ingress bindings are provisioned by
  cluster operations as part of the platform install.

## FAQ

!!! question "How do I reach a deployed model?"
    The deployment response and the Deployments list show the endpoint domain.
    The Ingress is created automatically; DNS just needs to point at the
    cluster ingress IP.

!!! question "OpenVINO or Triton?"
    OpenVINO for CPU inference (validated end-to-end); Triton for NVIDIA GPU
    serving. For LLM/VLM use the vLLM-compatible runtime installed on the
    cluster. Pick the runtime that matches where the model will actually run.

!!! question "Try works but deployment fails?"
    Trial uses the shared ML Backend and does not need KServe; deployment
    additionally requires a matching serving runtime, node resources and DNS.
    Check the deployment state/message and cluster provisioning first.

## Next steps

- Serve and integrate the endpoint; retrain later from field data — the loop
  starts again at [Datasets](datasets.md).
- Improve a deployed model with [Optimization](optimization.md) and
  [Evaluation](evaluation.md).
