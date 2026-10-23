# 训练

训练会在集群上基于一个固定数据集版本运行真实流水线任务，并把结果注册为新的模型版本。这不是
模拟：训练器容器真实运行在 CPU 或 GPU 上，实时输出损失曲线与日志，完成后把产物上传到对象
存储。

Forge 通过 Kubeflow Pipelines 调度，你只需填写训练表单。两条训练路线共用同一套任务机制。

## 两条训练路线

| | 计算机视觉 | LLM / VLM |
|---|---|---|
| 输入数据集 | COCO / TXT / ImageNet 版本 | LLM-SFT / sharegpt JSONL（VLM 带 `images/`） |
| 基座模型 | RT-DETR / timm 权重 | 模型池中的 Qwen / LLaMA 系列预训练模型 |
| 训练器 | 内置检测 / timm 模板（`train.py`） | LLaMA-Factory（NVIDIA、AMD）或原生 transformers + PEFT（Intel） |
| 方法 | 全量训练 / 微调 | LoRA / QLoRA 适配器 SFT（或合并权重） |
| 产物 | `.pt` + `.onnx`、指标 | 适配器 / tokenizer / processor、`history.jsonl`、指标 |
| 加速器 | CPU、NVIDIA、AMD、Intel | NVIDIA、AMD、Intel（QLoRA），可回退 CPU |

## 加速器：一张表单，镜像按厂商区分

Forge 使用**加速器画像**抽象：你在表单中选择目标（只列出集群上报为可分配的资源），平台据此
选择匹配的训练器镜像变体、Kubernetes 资源与 PyTorch 后端：

| 厂商 | K8s 资源 | 镜像后缀 | 后端 |
|---|---|---|---|
| NVIDIA | `nvidia.com/gpu` | `-cu` | CUDA PyTorch / LLaMA-Factory |
| AMD（RDNA） | `amd.com/gpu` | `-rocm` | ROCm / HIP，LLaMA-Factory |
| Intel Arc | `gpu.intel.com/xe` | `-xpu` | 原生 `torch.xpu` + PEFT |
| CPU | — | 默认 | CPU 镜像 |

支持度如实分级，并取决于你的硬件：

- **Certified（认证）**——真机端到端训练通过（例如 Intel Arc 在参考节点上对 CV、LLM
  QLoRA、SmolVLM VLM-LoRA 均已认证）。
- **Compatible / build-only（兼容 / 仅构建）**——镜像存在但该芯片上的 CV 或完整端到端尚未
  认证。
- 集群没有对应设备时任务无法调度到该处；请选择可用加速器或 CPU，而不要假定一定有 GPU。

## 创建训练任务

1. 打开**训练**页，选择任务类型（CV 检测 / 分割 / 分类，或 LLM / VLM）。
2. 选择数据集版本（标注导出或 LLM-SFT 语料）。
3. 从模型池选择基座模型。
4. 设置超参；CV 默认值是稳妥起点：

| 参数 | CV 默认 | 说明 |
|---|---|---|
| epochs | 100 | LLM/VLM 微调通常 1–5 个 epoch |
| imgsz | 640 | 训练/推理图片尺寸 |
| batch | 16 | 显存不足时调小；OOM 时训练器会给出明确报错 |
| 训练/验证比例 | 0.8 | Forge 执行切分，并保留验证集供评估 |

5. 选择与节点匹配的加速器并提交。

LLM/VLM 任务表单还会暴露微调方式（全量 / LoRA / QLoRA）、秩（rank）与 LoRA 超参；VLM 任务
接收视觉语言基座模型与 sharegpt + 图片语料。

## 任务运行期间

- **状态与进度**——任务依次为排队、运行、成功、失败；成功时进度到 100%。
- **曲线**——**训练曲线** Tab 绘制逐步/逐 epoch 的损失与评估指标（CV 读取训练器结果；
  LLM/VLM 绘制逐步 `history.jsonl`）。
- **日志**——日志视图显示训练器 Pod 的真实标准输出（损失行、上传确认），Pod 结束后回退到
  流水线执行器日志。
- **产物**——成功后训练器上传权重、ONNX（CV）、指标与 tokenizer/processor 文件，并以任务名
  自动注册一个模型版本。

训练过程中会写 checkpoint，因此中断的任务可从 checkpoint 恢复；失败任务也可以直接重启。

## 自带训练器

当内置模板无法表达某个工作流时，CV/PyTorch 任务可以使用**自定义镜像**和/或**自定义训练
脚本**。如果要做一个可复用的训练器——自有框架、自有架构、出现在训练表单中、可按加速器
选择——请用[训练器 SDK（Python）](trainer-sdk.md)构建：一套极小的「环境变量进、产物出」
契约，内置训练器用的也是它。

两条扩展通道：

- `custom_image`——私有镜像仓库中的任意镜像（`PATH` 上有 Python），它成为训练器容器。
  分发可复用训练器的受支持方式，是带[能力 profile](trainer-sdk.md#能力-profile) 的 SDK 镜像。
- `custom_script_uri`——指向某个 Python 文件的 `s3://` 或 `http(s)://` URL，下载到容器后
  以 `__main__` 执行。这是快速实验通道，无需镜像，但仅限 CV。

脚本继承标准训练器环境（`INPUT_URI`、`OUTPUT_DIR`、`CONFIG_JSON`、`ARTIFACT_ID`、`S3_*`
凭据），并把模型上传到 `OUTPUT_DIR`。若同时上传带 `weights_uri`/`onnx_uri` 的
`<artifact>.metrics.json`，版本会被精确注册；否则 worker 扫描输出前缀并注册最佳产物（优先
`.onnx`，其次 `.pt/.pth/.safetensors`）。LLM/VLM 任务走 LLaMA-Factory / XPU 训练器，不使用
这些选择器。

## 常见问题

!!! question "曲线在哪里看？"
    在任务详情页的**训练曲线** Tab。曲线在训练器写入后才出现，而非第一个 epoch/step 之前。

!!! question "任务一直 pending？"
    请求的加速器不可分配。检查集群节点、空闲显存与 device plugin，然后改用可用画像（含
    CPU 冒烟测试）重新提交。

!!! question "训练数据如何确定？"
    你选定一个不可变数据集版本；Forge 按你设置的比例切分训练/验证。留出的验证切分正是
    [评估](evaluation.md)默认使用的数据，可避免在训练图片上评估。

!!! question "中断了怎么办？"
    可从 checkpoint 恢复，或重启任务。数据集与基座模型固定在任务上，因此重跑结果可比较。

## 下一步

- 为边缘压缩：[优化](optimization.md)。
- 衡量精度与延迟：[评估](evaluation.md)。
- 查看、试跑并部署结果：[模型](models.md)。
