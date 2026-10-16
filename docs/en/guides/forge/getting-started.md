# Getting started

NereidForge (Forge) is the privatized **model factory** of the NereidAI suite — one production line that turns business images into field-ready models: prepare a dataset, annotate, train, optimize and quantize, evaluate, then register and deploy — all running on-premises and fully offline. See the [product page](../../products/nereidforge.md) for the full capability overview.

This guide walks one model through its first run in the factory.

## The journey at a glance

| Step | Page | What happens |
|---|---|---|
| 1. Prepare data | [Datasets](datasets.md) | Create a dataset, upload images or a ZIP, get a versioned dataset |
| 2. Annotate | [Annotations](annotations.md) · [ML Backend](mlbackend.md) | Label images, optionally with model pre-labeling, then export YOLO |
| 3. Train | [Training](training.md) | Pick dataset version + base model + hyperparameters, run the KFP pipeline |
| 4. Optimize | [Optimization](optimization.md) | ONNX graph optimization + int8 quantization for target devices |
| 5. Evaluate | [Evaluation](evaluation.md) | Score mAP50 / Precision / Recall / F1 / latency |
| 6. Register & deploy | [Models](models.md) | Pick a version, configure runtime, create the KServe service |

## 1. Prepare the dataset

On the Datasets page, create a dataset (COCO / YOLO) and upload jpg / jpeg / png images or a ZIP — images may sit at the archive root or in an `images/` folder. The ZIP is extracted and ingested asynchronously, and every upload creates a new retained version.

## 2. Annotate

Create an annotation project on the Annotations page and label images in the embedded Label Studio workbench (detection / segmentation / classification). To speed the work up, run semi-automated annotation from an ML Backend registered on the ML Backend page. When done, export to YOLO — the export becomes a new, training-ready dataset.

## 3. Train

On the Training page, select the dataset version, a base model (YOLOv8n suggested), and hyperparameters (epochs 100, imgsz 640, batch 16, train/val ratio 0.8 suggested). The cluster matches CPU/GPU automatically and runs a real KFP pipeline. On completion the model is registered automatically and training curves are available.

## 4. Optimize and quantize

On the Optimization page, select the source model and one or more target devices (CPU / OpenVINO / NVIDIA …). Each target independently runs ONNX graph optimization and int8 quantization, lands its artifact in SeaweedFS, and registers as a new version with real speedup and size-reduction metrics. A target without the matching hardware stays pending.

## 5. Evaluate

On the Evaluation page, score a version — by default against the training val subset, to avoid data leakage. Review mAP50 / Precision / Recall / F1 / latency, and check `accuracy_drop` for optimized versions. If precision comes back 0, lower the confidence threshold (0.25 suggested) and retry.

## 6. Register and deploy

Trained and optimized versions all live in the model library on the Models page, where the version table lets you compare target devices and speedup. Select a version, configure the runtime (OpenVINO for CPU, Triton reserved for GPU), GPU, and domain, and Forge creates the KServe service and Ingress. The deployment response returns the endpoint domain.

!!! tip "The loop repeats"

    Field data can start a new round: upload it as a new dataset version, annotate the gaps, retrain, and re-evaluate. Every model version keeps its data, metrics, and deployment history.
