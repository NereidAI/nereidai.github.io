---
title: NereidInference
---

# NereidInference

NereidInference（Inference，**NIN**）是套件的边缘推理运行时：一个运行在现场网关上的
EdgeX Foundry **设备服务**，从相机与图像源取流，调用基于标准的模型服务器，并把规范化的
结构化事件发布回 EdgeX 消息总线。它把 Forge 生产、Horizon 分发的模型变成现场实时推理——
而不让网关绑定任何模型格式、芯片厂商或厂商 SDK。

## 解决什么问题

- 模型工厂训练出的模型必须在靠近相机的廉价现场网关上运行；把视频回传云数据中心太慢，在
  气隙站点更是不可能。
- 一个现场可能混用多种相机（RTSP、ONVIF、MJPEG）与多种模型服务器（OpenVINO、Triton、
  vLLM、MindIE）；手工集成每种组合无法规模化。
- 现场团队需要一个中立运行时：新模型应以"包"的形式到达，而不是新代码；一个慢模型绝不能
  拖垮同一网关上的其他任务。

## 核心能力

**描述符驱动的媒体推理**

- 每个节点一个服务实例，可运行任意数量的推理**任务（job）**（每个已预置设备一个）；一个
  任务绑定一个取流源、一个模型包、一个调度策略与输出选项。
- 模型与芯片中立：不含厂商 SDK、不写死张量布局、不含业务逻辑。分类、检测、分割、姿态/关键
  点、嵌入向量、稠密图、图生图与 CTC 序列模型的差异只体现在模型包描述符与注册的解码器上。
- 讲两种标准推理协议：**KServe gRPC v2** 与 **OpenAI 兼容 HTTP**，对接独立部署的模型服务器
  （OpenVINO Model Server、Triton、vLLM、MindIE……）。

**边缘取流**

- 取流源：RTSP（每 URL 一个 ffmpeg 子进程，支持 H.264/H.265 解码）、ONVIF 相机与 ONVIF
  快照、MJPEG 与 JPEG（纯 Go 取流源）。
- 每个任务按自己的 FPS 采样，最多一个在途推理，采用"丢最旧帧"语义：慢模型只会降低该任务的
  帧率——延迟始终有界，不会堆积队列。
- ONVIF 流地址与密钥从 ONVIF 相机设备服务已注册的 EdgeX
  core-metadata/core-command/secret-store 数据中联邦获取，无需逐任务填写。

**通用解码与事件**

- 一组张量形状解码器由模型包描述符选择，而非按厂商或任务分叉：YOLO 风格 anchor/row 检测器、
  YuNet 人脸检测、分类器、回归器、语义/实例分割、关键点、嵌入、稠密图、图像张量、CTC 序列、
  复合解码器，以及面向 OpenAI 对话/VLM 响应的文本透传。
- 结果作为规范化结构化事件发布到 EdgeX 消息总线，并可选提供本地带标注的 MJPEG 预览供运维
  查看。

**本地模型获取**

- 分发单元是一个 gzip tar 包（`*.tar.gz`），内含根描述符 `nereid-model.json` 与带校验和的
  负载。服务监视 Open Horizon ESS 本地对象目录和/或收件箱目录，校验并解包到与模型服务器只读
  共享的 active 模型根目录。
- 分工明确：**Forge 负责模型转换与所有模型专属参数，Horizon 只负责运输模型包，Inference
  负责解包并遵循描述符**——它绝不生成、修复或臆造模型契约。

**运维**

- 纯 Go、静态编译（`CGO_ENABLED=0`）；ffmpeg 以降权子进程运行。多架构 OCI 镜像
  （`linux/amd64`、`linux/arm64`）。
- 遵循 EdgeX 4.0 约定与设备服务配置布局；预览端口是无认证的运维诊断口，应通过网络策略
  限制访问。

## 在套件中的位置

Inference 是模型闭环的现场执行环节，与 Edge 并列：

- **Forge → Inference：** Forge 生产模型包（当前为 ONNX 或 OpenVINO IR；其他制品格式可由
  描述符声明）。
- **Horizon → Inference：** Horizon 把模型包分发到网关的 Open Horizon ESS 本地对象存储；
  Inference 监视并激活。
- **Inference ↔ 模型服务器：** OVMS、Triton、vLLM 或 MindIE 作为独立服务运行；Inference
  通过 KServe gRPC v2 或 OpenAI 兼容 HTTP 作为其客户端。
- **Inference → EdgeX / Edge：** 结构化事件进入 EdgeX 总线，可经 Edge 提供的同一边缘集成
  向北流向 Link。

!!! info "开发者文档"
    完整配置、描述符参考、解码器目录与预置 API 位于 NereidInference 仓库——见
    [NereidInference](https://github.com/NereidAI/NereidInference)。

## 状态

NereidInference 已按 **Apache-2.0 开源**，基于 EdgeX 4.0.2 构建。与套件其他部分一样，
当前以滚动开发通道交付——源码加 CI 构建镜像，尚无带 tag 的正式版本。通用流水线、模型
目录、KServe/OpenAI 后端与内置解码器集均已实现；HTTP JPEG → OVMS KServe gRPC 路径、
一台真实 RTSP H.264 相机、一台 ONVIF 快照相机，以及 CPU 上带 ONNX Runtime 的托管
Triton 已通过真机验证。部分能力（默认 ONVIF `GetStreamUri`、H.265、重连与密钥轮换、
生产级 Horizon 包、GPU/OpenVINO 后端 Triton、其他厂商验收）仍在开放清单；适用于整套件的
发布门见[路线图](../community/roadmap.md)。

## 关键事实

| 维度 | 说明 |
|---|---|
| 是什么 | 现场网关上描述符驱动的媒体推理 EdgeX 设备服务 |
| 定位 | 模型闭环的现场推理运行时 |
| 取流源 | RTSP、ONVIF 相机/快照、MJPEG、JPEG |
| 推理协议 | KServe gRPC v2、OpenAI 兼容 HTTP |
| 模型服务器 | OpenVINO Model Server、Triton、vLLM、MindIE（独立部署） |
| 模型包装 | 带 `nereid-model.json` 描述符的 tar 包，经 Horizon ESS/收件箱交付 |
| 输出 | 结构化 EdgeX 事件；可选带标注 MJPEG 预览 |
| 技术栈 | EdgeX Foundry 4.0 上的静态 Go 二进制、ffmpeg 子进程；amd64/arm64 |
| 许可证 | Apache-2.0 |

## 资源

- GitHub：[NereidInference](https://github.com/NereidAI/NereidInference)
- [套件总览](index.md)
- [架构总览](../architecture/overview.md)
- [边缘分发](../deployment/edge-delivery.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
