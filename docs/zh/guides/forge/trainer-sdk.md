---
title: 训练器 SDK（Python）
---

# NereidForge 训练器 SDK（Python）

训练器 SDK 面向**自带训练框架的团队**——来自其他技术栈的检测模型、专有网络、
带特殊预处理的分类器、LLM/VLM 微调配方。它是训练组件与 Forge 之间**唯一**的
集成契约，而且刻意做得很小：**环境变量进，版本化产物出**。

- **包：** `nereidforge-trainer`（导入名 `nereidforge_trainer`），
  Apache-2.0，Python ≥ 3.11，运行时仅依赖 `boto3`。
- **没有基类，也没有回调平台的接口。** Forge 不导入训练器代码，训练器也不导入
  Forge 代码。可以使用任意框架、任意库、任意权重；上游框架许可证不宽松的训练器，
  放在自己的镜像与仓库里交付即可。
- **内置训练器同样基于它**（dogfooding）：内置视觉训练器（覆盖全部视觉任务的
  torch 训练器、PaddleX 检测训练器）都建立在这套 SDK 上，客户训练器不会得到
  一份二等契约。

!!! info "开发者文档"
    本页是上手介绍。包源码、完整的 torch 参考训练器与能力 profile 结构位于
    NereidForge 仓库（`app/builders/sdk/`、`app/builders/trainer-torch/`）
    ——见 [NereidAI](https://github.com/NereidAI)。

## 什么时候用

| 你想…… | 用 |
|---|---|
| 用内置 torch / PaddleX / LLM 训练器和标准选项训练 | 直接用[训练](training.md)表单，无需 SDK |
| 让自己的框架或训练代码作为 Forge 任务运行 | 用本 SDK 构建自定义训练器镜像 |
| 不构建镜像，临时跑一个 Python 脚本 | CV 任务的 `custom_script_uri` 通道（见[训练](training.md)） |
| 写一个可复用、可注册、带自有架构与设备支持并出现在训练表单中的训练器 | 本 SDK + 训练器镜像 + 能力 profile |

## 安装

wheel 随 Forge 版本发布一起交付（适合离线环境，机房内无需互联网）：

```bash
# 从发布源码树，或任意内部 wheel 镜像
pip install ./app/builders/sdk
```

为客户镜像构建自包含 wheel：

```bash
python -m pip wheel app/builders/sdk --no-deps -w ./wheels
# -> wheels/nereidforge_trainer-0.0.1-py3-none-any.whl
```

安装后还会得到脚手架 CLI `nf-trainer`：

```bash
nf-trainer init my-detector --name acme/detector --task detection \
  --architecture acme-det --framework acme
nf-trainer validate my-detector/trainer-profile.json   # 0 合法 · 1 非法 · 2 不可读
nf-trainer profile  my-detector/trainer-profile.json   # 美化输出
```

`init` 会在一个空目录中生成可直接填写的工程：`train.py`、`nf_profile.py`、
`trainer_profile.py`、`trainer-profile.json`、`Dockerfile`、`README.md`、
`.gitignore`。它**不**添加任何框架依赖——技术栈由你选择。

## 契约

### 环境变量

| 变量 | 方向 | 含义 |
|---|---|---|
| `INPUT_URI` | 入 | 数据集根：`s3://bucket/prefix…`；冒烟测试时可为本地目录 |
| `OUTPUT_DIR` | 入 | 产物目标：`s3://bucket/models/<job-id>/`，或本地目录 |
| `CONFIG_JSON` | 入 | **扁平**训练配置——内联 JSON，或 JSON 文件的路径/URI |
| `ARTIFACT_ID` | 入 | 产物基名（即任务 ID）；所有产物命名为 `<ARTIFACT_ID>.<ext>` |
| `S3_ENDPOINT` · `S3_ACCESS_KEY` · `S3_SECRET_KEY` · `S3_REGION` · `S3_BUCKET` | 入 | 对象存储连接信息，由平台注入（集群内使用有默认值） |
| `NF_DEVICE` | 入 | 按厂商镜像烘焙：`cpu` / `cuda` / `rocm` / `xpu` |
| `NPROC` | 入 | 多 GPU `torchrun` 式启动时每节点进程数 |
| `SCRIPT` | 入 | 入口选择：`train`（默认）· `evaluate` · `export` · `catalog` · `profile` |

`CONFIG_JSON` 刻意是一个扁平 JSON 对象——一次调用读入，未知键当作你自己的
超参：

```bash
export INPUT_URI=s3://nereidforge/datasets/ds-12/3/
export OUTPUT_DIR=s3://nereidforge/models/job-778/
export ARTIFACT_ID=job-778
export CONFIG_JSON='{"epochs": 50, "imgsz": 640, "batch": 16, "arch": "acme-det"}'
python train.py
```

### 输出产物

以产物 ID 为基名发布到 `OUTPUT_DIR`：

| 对象 | 视觉 | LLM / VLM | 被用于 |
|---|---|---|---|
| `<id>.onnx` | 必需 | — | 边缘导出 / 服务图（opset 17；检测头导出时不烘焙 NMS） |
| `<id>.metadata.json` | 必需 | — | 原生模型 manifest——推理侧唯一信任的文档 |
| `<id>.metrics.json` | 必需 | 必需 | 扁平最终指标，**外加 `weights_uri` / `onnx_uri` / `manifest_uri`**——精确注册版本 |
| `<id>.pt`（或框架权重，如 `.pdparams`） | 建议 | 适配器目录 | 恢复 / 重新导出；LLM 为 LoRA 适配器（`adapter_config.json` …） |
| `progress.json` | 必需 | 必需 | Forge worker 轮询的实时进度（`progress_pct`、`current_epoch`、`total_epochs`） |
| `history.jsonl` | 可选 | 常用 | 逐步损失曲线 |

若 `<id>.metrics.json` 缺少 `weights_uri` / `onnx_uri`，worker 会退化为扫描
输出前缀（优先 `.onnx`，其次 `.pt/.pth/.safetensors`）；显式给出 URI 才是精确
注册路径。

### 数据集

`download_dataset(INPUT_URI)` 默认把前缀下的所有对象按键名原样镜像到 `/data`。
规范布局与[数据集](datasets.md)页一致：检测/分割/姿态用 COCO 或归一化 TXT 框
标签（图片 + 每图一个标签文件 + 清单 YAML），分类用 ImageFolder，LLM/VLM 用
sharegpt JSONL（加 `images/`）。未切分的视觉语料会在运行时按配置的
`split_ratio`（默认 0.8）做确定性切分。

## API 一览

所有内容都从顶层包导入：

```python
from nereidforge_trainer import (
    read_config, write_json, Progress,
    download_dataset, publish_file, upload_file, s3_client, parse_uri, list_objects,
    build_manifest, manifest_outputs,
    resolve_augmentation, augmentation_summary,
)
```

| API | 用途 |
|---|---|
| `read_config(raw="") -> dict` | 读取 `CONFIG_JSON`（内联 JSON 或文件/URI）；为空时返回 `{}` |
| `write_json(path, data)` | 本地 JSON 写入辅助 |
| `Progress(output_uri, total_epochs)` | `.log(epoch, metrics)` 追加 history 并发布 `progress.json`；`.write(epoch, metrics, key="progress.json")` 写单条记录。任务收尾前百分比封顶 99 |
| `download_dataset(input_uri, local_root="/data")` | 镜像 `s3://` 前缀（或复制本地目录），返回本地根 |
| `publish_file(local_path, output_uri, name)` | 上传到 `s3://…`；**`OUTPUT_DIR` 为本地目录时则复制进该目录**——同一份代码既能跑在集群里，也能在笔记本冒烟。返回 URI |
| `upload_file(...)` | 严格 S3 版本 |
| `s3_client()` · `parse_uri(uri)` · `list_objects(...)` | 按注入环境变量接线的底层 S3 辅助 |
| `build_manifest(...)` | 构建原生 `<id>.metadata.json`：任务、架构、框架、输入尺寸、标签、逐任务输出张量契约、预处理、指标、数据血缘、许可证 |
| `manifest_outputs(task)` | 某任务的标准输出张量契约（`detection`、`instance_seg`、`semantic_seg`、`pose`、分类……） |
| `resolve_augmentation(cfg)` · `augmentation_summary(aug)` | 共享增强策略：预设 `off`/`light`/`medium`/`strong` 加带钳制的逐项覆盖——与界面上的旋钮一致 |

## 最小训练器

完整生命周期——读配置、下载数据、报进度、产出物：

```python
import os
from nereidforge_trainer import (
    Progress, read_config, write_json,
    download_dataset, publish_file, build_manifest,
)

cfg = read_config()
artifact_id = os.environ.get("ARTIFACT_ID", "model")
output_uri = os.environ.get("OUTPUT_DIR", "")
data_root = download_dataset(os.environ["INPUT_URI"])  # s3:// 或本地目录
epochs = int(cfg.get("epochs", 50))
labels = load_class_names(data_root)                  # 你自己的代码

progress = Progress(output_uri, epochs)
for epoch in range(1, epochs + 1):
    train_one_epoch(epoch, cfg, data_root)            # 你的框架
    metrics = evaluate(epoch, cfg, data_root)         # {"mAP50": ..., ...}
    progress.log(epoch, metrics)                      # -> progress.json

# 框架原生 checkpoint（恢复 / 重新导出）
save_checkpoint(f"/tmp/{artifact_id}.pt", labels)
weights_uri = publish_file(f"/tmp/{artifact_id}.pt", output_uri,
                           f"{artifact_id}.pt")

# 可移植推理图
export_onnx(f"/tmp/{artifact_id}.onnx")
onnx_uri = publish_file(f"/tmp/{artifact_id}.onnx", output_uri,
                        f"{artifact_id}.onnx")

# 原生 manifest——标签从 0 开始，框坐标在模型输入空间
manifest = build_manifest(
    task="detection", architecture=cfg.get("arch", "custom"),
    framework="acme", input_size=int(cfg.get("imgsz", 640)),
    labels=labels, metrics=metrics,
    dataset={"version": cfg.get("dataset_version", "")},
)
manifest_path = f"/tmp/{artifact_id}.metadata.json"
write_json(manifest_path, manifest)
manifest_uri = publish_file(manifest_path, output_uri,
                            f"{artifact_id}.metadata.json")

# 最终指标文档，精确注册模型版本
final = {
    **metrics,
    "task": "detection",
    "architecture": cfg.get("arch", "custom"),
    "framework": "acme",
    "epochs": epochs,
    "weights_uri": weights_uri,
    "onnx_uri": onnx_uri,
    "manifest_uri": manifest_uri,
}
write_json(f"/tmp/{artifact_id}.metrics.json", final)
publish_file(f"/tmp/{artifact_id}.metrics.json", output_uri,
             f"{artifact_id}.metrics.json")
```

控制台输出遵循统一约定：普通 `print(..., flush=True)` 加方括号前缀
（`[train]`、`[data]`、`[export]`、`[evaluate]`、`[progress]`）；用户错误以
退出码 **2** 结束。

## 能力 profile

训练器镜像要声明自己能做什么。镜像携带 `/app/trainer-profile.json`，并在以
`SCRIPT=profile`（`python /app/nf_profile.py`）启动时打印同一份文档。Forge
保存该声明，并据此在训练表单中渲染任务、架构与设备选项——每个训练器无需改动
界面代码。

```json
{
  "schema": "nf.trainer-profile/1",
  "name": "acme/detector",
  "framework": {"name": "acme", "version": ">=1.0"},
  "devices": ["cpu", "cuda"],
  "tier": "extended",
  "requires": ["extended.custom_trainer"],
  "tasks": [
    {
      "id": "detection",
      "label": "目标检测",
      "tier": "extended",
      "default_arch": "acme-det",
      "architectures": [
        {"id": "acme-det", "label": "Acme 检测器", "size": 640,
         "params_m": 12.4, "tier": "extended", "license": "proprietary"}
      ]
    }
  ],
  "capabilities": [
    {"id": "export.onnx", "tier": "core", "entrypoint": "export"}
  ],
  "entrypoints": {
    "train": "python /app/train.py",
    "evaluate": "python /app/evaluate.py",
    "export": "python /app/export.py",
    "catalog": "python /app/catalog.py",
    "profile": "python /app/nf_profile.py"
  },
  "env": ["INPUT_URI", "OUTPUT_DIR", "CONFIG_JSON", "ARTIFACT_ID"],
  "artifacts": ["<id>.onnx", "<id>.metadata.json", "<id>.metrics.json", "<id>.pt"],
  "license": {"code": "proprietary", "weights": "per-model"}
}
```

Profile 规则：

- `devices` **按镜像划分**：`cpu`、`cuda`、`rocm`、`xpu`。每种支持的芯片发一个
  镜像并烘焙 `NF_DEVICE`；不存在"万能"镜像。
- 只声明真正实现的任务与架构；`default_arch` 必须在架构列表中。
- `tier`（`core` / `extended`）可设在 profile、任务或架构层级——越具体越优先；
  `extended` 条目必须列出非空的 `requires` 授权键，创建任务时检查。
- 许可证**只记录、不强制**：声明训练器代码许可证与逐模型权重许可证；不兼容的
  技术栈隔离在客户自己的镜像中。
- Profile 结构（`nf.trainer-profile/1`）独立于 SDK 包版本另行版本化。
- Profile 脚本必须命名为 **`nf_profile.py`**——`/app` 下放一个 `profile.py`
  会遮蔽 Python 标准库。

### 注册镜像

管理员在 **系统 → 镜像** 注册镜像（类别 *train*）：构建上下文中的镜像可以自行
声明 profile，也可以对着镜像记录粘贴/上传 profile JSON。之后它的任务与架构会
出现在训练表单中，可选加速器则是 profile 的 `devices` 与集群可分配资源的交集。

## 本地构建与冒烟

生成的 `Dockerfile` 从固定 wheel 安装 SDK（离线构建时可通过构建参数传入
wheel），烘焙 `ENV NF_DEVICE=cpu`，并按 `SCRIPT` 分发：

```dockerfile
ARG SDK_WHEEL=
COPY ${SDK_WHEEL} /tmp/sdk.whl
RUN pip install --no-cache-dir /tmp/sdk.whl
# ...你的框架与代码...
ENTRYPOINT ["sh", "-c", "case \"${SCRIPT:-train}\" in \
  evaluate) exec python /app/evaluate.py;; \
  export) exec python /app/export.py;; \
  profile) exec python /app/nf_profile.py;; \
  *) exec python /app/train.py;; esac"]
```

因为 `publish_file()` 在 `OUTPUT_DIR` 不是 `s3://` URI 时会退化为本地复制，
同一个镜像可以直接在笔记本上用本地数据集冒烟：

```bash
docker run --rm \
  -v ./sample-dataset:/data:ro -v ./out:/out \
  -e INPUT_URI=/data -e OUTPUT_DIR=/out -e ARTIFACT_ID=smoke \
  -e CONFIG_JSON='{"epochs":1,"imgsz":640,"batch":4,"arch":"acme-det"}' \
  registry.example.internal/forge/acme-detector:v1
# -> ./out/smoke.onnx、smoke.metadata.json、smoke.metrics.json、progress.json
```

## 职责边界

| 平台负责 | 训练器负责 |
|---|---|
| 调度、按厂商镜像分配 CPU/GPU | 读取 `CONFIG_JSON` 并校验自己的超参 |
| 数据集版本化、投递到 `INPUT_URI`、切分 | 消费数据集布局、真正的训练循环 |
| 注入 S3 凭据与端点 | 运行期间持续发布 `progress.json` |
| 进度界面、日志、任务状态机 | 导出 ONNX + manifest（视觉）并写最终指标 |
| 依据 `<id>.metrics.json` 注册、评估、优化、部署 | 框架原生 checkpoint；在 profile/manifest 中如实标注许可证 |

## Checkpoint 与续训

SDK **不做自动恢复**。训练器自行保存 checkpoint（`<id>.pt` 式）；继续/增量
训练通过配置键 `base_weights_uri`（`s3://` URI 或本地路径）驱动：自行物化历史
权重、迁移骨干、重新初始化变化的检测头，并把血缘（基权重 URI、历史标签、新增
类别）记入 manifest 的扩展字段。可选的 `SCRIPT=export` 入口把已有 checkpoint
重新导出为 ONNX + manifest，无需训练；`SCRIPT=evaluate` 只写指标文档。

## 当前状态

- SDK 版本 **0.0.1**；内置 torch 视觉训练器（全部视觉任务）与 PaddleX 检测
  训练器是前两个消费者。
- LLM/VLM 内置训练器已经遵循同一套环境变量与 `progress.json` /
  `metrics.json` 约定（适配器目录作为 `weights_uri`）；面向 LLM/VLM 自定义
  训练器的 SDK 辅助与 profile 覆盖正在对齐中。
- `custom_script_uri` 脚本通道是 CV 任务的快速实验路径；本页描述的「镜像 +
  profile」才是分发和注册可复用训练器的受支持方式。

## 下一步

- [训练](training.md)——界面上如何选择任务、加速器与自定义镜像。
- [数据集](datasets.md)与[标注](annotations.md)——到达 `INPUT_URI` 的布局。
- [模型](models.md)——注册出的版本如何评估与部署。
