---
title: NereidInference
---

# NereidInference

NereidInference（简称 **NIN**）是**守在相机旁边的 AI 检查员**。它运行在现场网关上，
接过 [NereidForge](nereidforge.md) 训练好的模型，直接对现场视频和图像实时干活——检测、
分类、文字识别、人脸识别等等——再把结构化结果送回平台。视频不出厂区，毫秒级出结果，
全程不依赖云端往返。

当你遇到下面这些问题时，就该 NIN 出场了：

- "把每路相机视频都传到云端 AI 服务，又慢又贵，而且常常是合规红线——模型能不能在
  本地跑？"
- "我们的网关来自不同厂商、芯片各不相同，一套 AI 运行时能全覆盖吗？"
- "现在换个模型就是一个软件项目，能不能像投放文件一样简单？"
- "一个重模型把网关上其他任务都拖慢了，怎么保证别的检测按时完成？"
- "运维人员怎么看到 AI 到底在看什么、判得对不对？"

## NIN 能帮你做什么

### 推理在边缘，而不是遥远的机房

推理就在相机旁边的网关上完成，结果实时返回，视频无需离开现场。这正是气隙工厂、
园区与安防场景能够落地的前提。

### 一套运行时覆盖所有视觉与语言任务

同一个服务可以处理分类、目标检测、分割、姿态关键点、嵌入向量、稠密图、图生图、
OCR、CTC 文本序列以及大模型/视觉大模型的文本响应。任务之间的差异装在模型包里，
而不是靠分叉软件实现——运行时内部没有厂商 SDK，也没有写死的模型结构。

### 加模型等于投放一个包，而不是部署一套代码

模型以一个带版本的包交付，包内描述符说明输入、输出与解码规则。NIN 完成校验与
解包后，新模型即可作为一个运行任务上岗。模型包通过
[NereidHorizon](nereidhorizon.md) 或简单的受监视收件箱送达；运行时自身绝不臆造或
修补模型契约。

### 每一项检测都按时完成

每个任务按自己的节奏采样相机，最多一个在途推理，采用"丢最旧帧"策略：慢模型只会
降低自己的帧率，其他任务的延迟始终有界、队列不会堆积。单节点任务数有明确上限
（默认 64 个）。

### 不绑定你已有的芯片与模型服务器

NIN 是独立部署的模型服务器（OpenVINO Model Server、Triton、vLLM、MindIE 等）的
客户端，走两套标准协议（KServe gRPC v2 与 OpenAI 兼容 HTTP）。它可以托管自己的
OpenVINO 与 Triton 服务器，对集中式或客户自备的服务器则只做只读观察。换硬件不必
重写应用。

### 亲眼看着 AI 工作

每个任务都暴露健康计数、成功/失败累计、延迟分位数以及可读状态（已应用/降级/
失败）与最近一次错误。可选的带标注预览直接在画面上画出检测框与标签，运维人员可以
直观核对行为；预览口无认证，属于诊断用途，应通过网络策略限制访问。

## 一个模型上岗的过程

1. **交付**——Forge 构建模型包，Horizon（或本地收件箱）把它放到网关上。
2. **校验与解包**——NIN 检查描述符与校验和，把模型装入只读的活动模型根。
3. **建立任务**——相机源、模型、调度与输出方式绑定为一个 EdgeX 设备，可经平台
   下发，也可用简单配置文件完成。
4. **取帧**——RTSP、ONVIF、MJPEG 或 JPEG 源按节奏采样，每路相机的解码在任务间
   共享。
5. **推理与解码**——模型服务器返回结果，描述符选定的解码器把原始张量转换为规范的
   结构化事件。
6. **发布与预览**——事件进入 EdgeX 消息总线（可经
   [NereidEdge](nereidedge.md) 继续北上），带标注预览同步展示检测内容。

## 在套件中的位置

NIN 是模型闭环在现场的执行环节，与 Edge 并肩运行：

- **Forge → NIN：**Forge 产出模型包（当前为 ONNX 或 OpenVINO IR；其他制品格式可
  通过描述符声明）。
- **Horizon → NIN：**Horizon 把模型包分发到网关本地对象存储，NIN 监视并激活。
- **NIN ↔ 模型服务器：**OVMS、Triton、vLLM 或 MindIE 作为独立服务运行，NIN 经
  KServe gRPC v2 或 OpenAI 兼容 HTTP 作为客户端调用。
- **NIN → EdgeX / Edge：**结构化事件进入 EdgeX 总线，可沿 Edge 提供的同一套边缘
  集成通道北上 Link。

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

## 技术一览

本节面向技术评估人员；以上内容均无需机器学习背景即可阅读。

| 方面 | 说明 |
|---|---|
| 是什么 | 现场网关上、描述符驱动的媒体推理 EdgeX 设备服务 |
| 定位 | 模型闭环的现场推理运行时 |
| 取帧源 | RTSP（每 URL 一个 ffmpeg，支持 H.264/H.265）、ONVIF 相机/快照、MJPEG、JPEG |
| 推理协议 | KServe gRPC v2、OpenAI 兼容 HTTP |
| 模型服务器 | OpenVINO Model Server、Triton、vLLM、MindIE（独立部署）；受管 OVMS/Triton 加只读外部 servable |
| 模型包装 | gzip tar 包，根描述符 `nereid-model.json`，经 Horizon ESS 或受监视收件箱交付 |
| 解码器覆盖 | 检测、分类、分割、姿态、嵌入向量、稠密图、图像输出、OCR/CTC、大模型/VLM 文本、组合结果——完全由描述符选择 |
| 调度 | 每任务支持连续帧率/周期/事件/手动触发，单在途推理、丢最旧帧语义，节点默认上限 64 任务 |
| 输出 | 结构化 EdgeX 事件；可选无认证带标注 MJPEG 预览（容器口 18080，宿主 28080） |
| 服务端口 | 服务端口 59992（临时端口，待 EdgeX TSC 正式分配） |
| 技术栈 | EdgeX Foundry 4.0 上的静态 Go 二进制（`CGO_ENABLED=0`），降权 ffmpeg 子进程；linux/amd64 与 linux/arm64 镜像 |
| 许可证 | Apache-2.0 |

## 资源

- GitHub：[NereidInference](https://github.com/NereidAI/NereidInference)
- [产品总览](index.md)
- [架构总览](../architecture/overview.md)
- [边缘分发](../deployment/edge-delivery.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
