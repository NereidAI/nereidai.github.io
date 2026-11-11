# NereidInference 快速开始

NereidInference 是一个面向描述符驱动媒体推理的 EdgeX Foundry 4.0 **设备服务**。网关上的
一个实例可运行任意数量的推理**任务（job）**——每个已预置的 EdgeX 设备对应一个任务。每个任务
从相机或图像源取帧，通过 KServe gRPC v2 或 OpenAI 兼容 HTTP API 调用独立部署的模型服务器，按
模型包描述符解码原始张量，把规范化的结构化事件发布到 EdgeX 消息总线，并可选提供带标注的
MJPEG 预览供运维查看。

本服务对模型与芯片厂商中立：不含厂商 SDK、不写死张量布局、不含业务逻辑。分类、检测、分割、
姿态、嵌入向量、稠密图、图生图与 CTC 序列模型的差异只体现在模型包描述符与注册的解码器上。

!!! tip "在 EdgeX 总线上独立运行"
    NereidInference 只需要 EdgeX 4.0 核心栈与一个可达的模型服务器。NereidEdge **不是运行时
    依赖**：只有在启用套件级推理集成时，Edge 才负责桥接目录、绑定与凭据。生产 rollout 使用
    NereidHorizon 的 Open Horizon 服务定义；本篇运行开发用 Compose 叠加层。

## 架构

```text
相机 RTSP ──► ffmpeg 子进程（H.264/H.265 解码，rawvideo 管道）
MJPEG/JPEG ──► 纯 Go 取流源             ──► 预处理 ──► KServe gRPC / OpenAI
                                                                      │
EdgeX 核心 ◄── 结构化事件（异步）◄── 通用解码器 ◄────────────────────┘
运维人员  ◄── 带标注 MJPEG 预览（本地、可选）
模型包（带 nereid-model.json 的 .tar.gz）──► 收件箱 / ESS 监视器 ──► active 模型根
```

关键特性：

- **每个取流 URL 一个 ffmpeg**，按引用计数并扇出给 N 个任务。每个任务按自己的 FPS 采样，
  最多一个在途推理，采用"丢最旧帧"语义：慢模型只会降低该任务的帧率——延迟始终有界，不会
  堆积队列。
- **无 CGo。** Go 二进制静态编译（`CGO_ENABLED=0`）；ffmpeg 是运行时 Alpine 包，以降权
  子进程执行。
- **本地模型获取。** 服务监视 Open Horizon ESS 本地对象目录和/或普通收件箱目录，校验模型包并
  解包到与模型服务器只读共享的 `active/` 模型根。
- **联邦凭据。** ONVIF 相机的流地址与密钥名通过 ONVIF 相机设备服务已注册的 EdgeX
  core-metadata/core-command/secret-store 数据解析——绝不逐任务填写凭据。

## 核心概念

| 概念 | 含义 |
|---|---|
| **任务（Job）** | 一个 EdgeX 设备，其 `Inference` 协议属性选择取流源、模型、调度与输出。任务默认不预置。 |
| **管理设备** | 单例 `nereid-inference` 设备（profile 为 `nereid-inference-manager`），暴露服务级资源：`ModelsJSON`、`ObjectDiagnosticsJSON`、`ExternalServablesJSON`、`PipelinesJSON`。它本身不是任务。 |
| **设备 profile** | `cmd/res/profiles/` 中的 YAML，为一个任务族（检测、分类、姿态……）定义 reading 资源。任务的 `profileName` 决定它发出哪些 reading。 |
| **模型包** | 一个 gzip tar（`*.tar.gz`），内含根描述符 `nereid-model.json` 与带校验和的负载。NereidForge 构建、NereidHorizon 运输、本服务解包。 |
| **解码器** | 由描述符选择的张量形状解码器——不存在厂商或任务分叉。注册表初始为空，二进制不带任何业务流水线。 |
| **Servable** | 模型服务器上加载的模型实例。NereidInference 自行管理 OVMS/Triton servable；外部服务器只做只读观察。 |

## 前提条件

- 网关上运行 EdgeX 4.0 核心栈（core-keeper、core-metadata、core-command、NATS 消息总线与
  设备服务），由官方 [edgex-compose](https://github.com/edgexfoundry/edgex-compose)
  项目启动，并存在外部网络 `edgex_edgex-network`。
- 一个可达的模型服务器——OpenVINO Model Server、Triton、vLLM 或 MindIE，独立部署且至少服务
  一个模型。仓库的开发 Compose 也自带 OVMS 与一个受管 Triton 容器。
- 一个取流源：RTSP/ONVIF 相机、MJPEG/JPEG 端点，或仅用于流水线验证的 `none` 源。
- 一个模型包（根目录带 `nereid-model.json` 的 `*.tar.gz`），由 NereidForge 生产或按仓库中的
  描述符指南构建。

## 1. 启动服务

仓库自带开发用 `docker-compose.yaml`，作为官方 EdgeX 栈在外部 `edgex_edgex-network` 上的
叠加层。它增加四个部分：`device-inference` 服务本身、一个渲染空多模型配置的 OVMS init
容器、`edgex-ovms` 服务器，以及一个受管 `edgex-triton` 服务器。

```bash
docker network create edgex_edgex-network 2>/dev/null || true
docker compose up -d device-inference
```

本地服务设置了 `pull_policy: build`，因此普通的 `up` 会先从当前工作树构建服务——无需单独的
`make docker` 或 `--build` 参数。发布端口为 `59992`（服务的临时 EdgeX 端口，待 TSC 正式
分配）与宿主 `28080`，后者转发到容器预览口 `18080`。

直接构建制品：

```bash
make build     # 静态二进制，输出到 cmd/device-inference（CGO_ENABLED=0）
make test      # 单元测试、golangci-lint、go vet、gofmt、Attribution 门
make image     # linux/amd64、linux/arm64 OCI 归档，位于 dist/
make docker    # 本地开发 tag 加 OCI 归档
```

仓库没有 `VERSION` 文件，也不存在 `latest` tag：精确的 `v*` tag 检出构建其裸 SemVer，其他
所有检出构建滚动的 `0.0.0-dev` 通道，CI 可显式注入 `VERSION`。

### Compose 卷

| 卷 / 挂载 | 容器路径 | 用途 |
|---|---|---|
| `model-root` | `/var/lib/nereid-inference/models` | active 模型根、模型包目录与运行时状态 |
| `ovms-runtime` | `…/models/runtime` | 与 OVMS 共享的服务器就绪仓库 |
| `inference-inbox` | `/var/lib/nereid-inference/inbox` | 接收新模型包的投放目录 |
| 宿主 ESS 存储（只读） | `/var/horizon/ess-store/sync/local` | Horizon 交付的 Open Horizon ESS 本地对象 |
| `/dev/dri` | `/dev/dri` | 可选 VA-API 解码所需的 DRM 渲染节点 |

## 2. 理解配置

服务配置遵循 `cmd/res/configuration.yaml` 中的标准 EdgeX 布局。产品专属段为 `Inference`：

| 键 | 默认值 | 含义 |
|---|---|---|
| `DefaultEndpoint` | `edgex-ovms:9000` | 受管 OVMS 租约使用的 KServe gRPC 端点 |
| `OpenAIEndpoint` | `http://edgex-vllm:8000` | OpenAI 兼容 HTTP 默认基址 |
| `ModelRoot` | `/var/lib/nereid-inference/models` | active 模型根与持久化运行时状态 |
| `CoreMetadataURL` / `CoreCommandURL` | EdgeX Compose 主机名 | 用于 ONVIF 联邦与管理回调 |
| `Ess.Enabled` / `Ess.LocalDir` | `true` / ESS 路径 | Open Horizon 本地对象监视器 |
| `Inbox.Enabled` / `Inbox.Dir` | `true` / inbox 路径 | 手工投放包的监视器 |
| `Preview.Enabled` / `Preview.Bind` | `true` / `0.0.0.0:18080` | 无认证运维预览 |
| `OVMS.*` | 启用，REST `:9001` | 受管 OVMS 对账器：servable 增删与重载超时 |
| `Triton.*` | 启用 | 受管 Triton 对账器，经 HTTP Repository API 显式 load/unload |
| `External.Enabled` / `External.ProvisionFile` | `true` / `res/external-servables.yaml` | 对本服务无权管理的服务器的只读视图 |
| `Pipelines.ProvisionFile` | 空 | 可选的 A 通道流水线注册表；留空即空白注册表 |
| `Limits.MaxJobs` | `64` | 每节点最大并发任务数 |
| `Limits.FrameTTLFactor` | `2.0` | 相对采样间隔的帧过期上限 |
| `Limits.JSONPayloadCap` | `1048576` | 序列化事件负载上限（字节） |
| `FFmpeg.VAAPIDevice` | `/dev/dri/renderD128` | `DecodeAccel: vaapi` 任务的默认 DRM 渲染节点 |

## 3. 预置推理任务

任务就是一个带 `Inference` 协议映射的 EdgeX 设备。完整属性集：

| 属性 | 取值 / 示例 | 说明 |
|---|---|---|
| `SourceKind` | `rtsp` · `rtsp-udp` · `onvif-camera` · `onvif-snapshot` · `mpjpeg` · `jpeg` · `none` | 取流类型 |
| `SourceDevice` | `camera-01` | 用于 ONVIF URI/密钥/快照联邦的 EdgeX 名称 |
| `SourceURL` | `http://host/snapshot.jpg` | `jpeg`/`mpjpeg`/`rtsp` 源的直连 URL |
| `StreamProfile` | `Profile_2` | 可选 ONVIF Media ProfileToken，仅 `onvif-camera` |
| `SecretName` | `onvif-camera-01` | 可选；省略时从相机元数据解析 |
| `FFmpegExtra` | `-fflags nobuffer …` | 可选白名单 argv，仅 ffmpeg 源 |
| `ModelID` / `ModelVersion` | `example-yolov8n` / `1.0.0` | 单模型任务选择目录中的包 |
| `PipelineId` | `face-recognition-v1` | 注册表流水线任务用，替代 ModelID/Version |
| `TargetDevice` | `CPU` · `GPU` · `GPU.0` · `NPU` | 推理绑定中携带的 OVMS 目标设备 |
| `Endpoint` | `edgex-ovms:9000` | 可选，覆盖租约的族端点 |
| `ServableID` | 外部 servable id | 外部服务器任务；流水线任务中会被拒绝 |
| `Trigger` | `continuous` · `periodic` · `event` · `command` | 帧采样方式；`event` 映射为手工命令触发 |
| `FPS` / `PeriodMs` | `5` / `5000` | 连续帧率 / 周期间隔 |
| `MaxInferMs` | `5000` | 单次推理时限 |
| `PublishMode` | `all` · `nonempty` · `none` | `nonempty` 抑制空结果事件；`none` 只保留 GET 缓存 |
| `DecodeAccel` / `VAAPIDevice` | `vaapi` / `renderD129` | 可选硬件解码；节点或驱动缺失时任务显式失败 |

### 方式 A——开发用设备文件

把 YAML 文件放到 `cmd/res/devices/`，SDK 启动时自动加载：

```yaml
deviceList:
  - name: example-inference-01
    profileName: nereid-inference-detection
    description: Example inference job (development only)
    labels: [nereid, inference]
    protocols:
      Inference:
        SourceKind: jpeg
        SourceURL: "http://camera-host/snapshot.jpg"
        ModelID: example-model
        ModelVersion: "1.0.0"
        TargetDevice: CPU
        Endpoint: "edgex-ovms:9000"
        Trigger: periodic
        PeriodMs: "5000"
```

已在 ONVIF 相机设备服务注册的相机无需复制凭据——按 EdgeX 名称引用即可：

```yaml
    protocols:
      Inference:
        SourceKind: onvif-snapshot
        SourceDevice: registered-onvif-camera
        ModelID: example-model
        ModelVersion: "1.0.0"
        TargetDevice: CPU
```

### 方式 B——core-metadata API

生产预置走 EdgeX core-metadata（启用套件集成时也可由 NereidEdge 代发）：

```bash
curl -fsS -X POST "http://localhost:59881/api/v3/device" \
  -H 'Content-Type: application/json' \
  --data-binary @job.json
```

## 4. 选择设备 profile

`cmd/res/profiles/` 自带十三个 profile；profile 名称决定任务发出的 reading 资源：

| Profile | 主要 reading |
|---|---|
| `nereid-inference-detection` | `DetectionJSON`、`DetectionCount`、`Top1Label`、`Top1Score`、`FrameJPEG` |
| `nereid-inference-classification` | `ProbsJSON`、`AttributesJSON`、`Top1Label`、`Top1Score` |
| `nereid-inference-segmentation` | `SegmentationJSON`、`InstanceJSON`、`SegmentCount` |
| `nereid-inference-pose` | `KeypointsJSON`、`PersonCount` |
| `nereid-inference-embeddings` | `VectorJSON`（L2 归一化） |
| `nereid-inference-regression` | `RegressionValue`、`RegressionJSON` |
| `nereid-inference-dense` | `DenseJSON`、`DenseValue`、`DepthMean` |
| `nereid-inference-image` | `ResultJPEG`、`FrameJPEG` |
| `nereid-inference-ocr` / `…-llm` | `Text`、`Confidence` |
| `nereid-inference-composite` | `CompositeJSON`（命名成员结果） |
| `nereid-inference-pipeline` | `PipelineJSON`、`ActivePipelineVersion`、`LatestPipelineVersion` |
| `nereid-inference-manager` | 仅管理：`ModelsJSON`、`ObjectDiagnosticsJSON`、`ExternalServablesJSON`、`PipelinesJSON` |

每个任务 profile 还带有运维资源 `State`（`APPLIED`/`DEGRADED`/`FAILED`）、`LastError`、
`SuccessTotal`、`ErrorTotal`、`P50Ms`、`P95Ms`、`InferLatencyMs` 与可写的 `Trigger`。

## 5. 交付模型包

把模型包放到任一受监视位置——收件箱目录或 ESS 本地对象存储。服务校验校验和与描述符，解包到
只读 active 模型根，并把模型注册到管理设备暴露的目录中。

- 制品格式与运行时正交：当前包声明 `artifact.format: onnx` 或 `openvino-ir`；未来的
  Triton/TensorRT 包可声明更多格式与 `runtime.server.family: triton`。目录接受标准包，所选
  运行时适配器会拒绝它无法服务的制品。
- 对 OVMS，描述符声明 `runtime.server.family: ovms` 与 `runtime.repository_path`，指向一个
  包含 `<version>/model.onnx` 或 `<version>/model.xml` 加 `model.bin` 的仓库。数字仓库目录
  （通常为 `1`）是 OVMS 本地版本号，与 Nereid 语义化模型版本不同。
- 分工明确：**Forge 负责转换与所有模型专属参数，Horizon 只负责运输模型包，NereidInference
  负责解包并遵循描述符**——它绝不生成、修复或臆造模型契约。

## 6. 模型服务器与外部 servable

- **受管 OVMS**——自带服务器从空配置启动；服务为每个活跃绑定与目标设备增删一个 servable，
  并经 OVMS REST 端点驱动重载。
- **受管 Triton**——对账器渲染 Triton 仓库，经 HTTP Repository API 显式执行模型 load/unload，
  加载与就绪超时均可配置。
- **外部 servable**——本服务无权管理的集中式或客户自备服务器。在
  `res/external-servables.yaml` 中声明；合并后的 `ExternalServablesJSON` 健康视图为只读，
  对其的受管写入与 `ServableID` 执行都会被拒绝。

## 7. 多模型流水线（可选）

二进制本身不带任何业务流水线。注册表只接受封闭的五节点线性词汇——
**source → infer → transform → infer → emit**——由流水线内核校验。有两种可选装载通道：

1. **预置文件（A 通道）：** 把定义复制到 `res/` 旁并设置
   `Inference.Pipelines.ProvisionFile`；文件缺失时得到空白注册表而非启动失败。
2. **管理资源（B 通道）：** 经 EdgeX 资源 `PipelinesJSON` PUT 完整定义数组。PUT 是全量替换
   而非补丁；任一非法条目都会拒绝整个请求。接受的表持久化到
   `ModelRoot/runtime/pipelines/pipelines.json`，重启后保留。

```bash
COMMAND=http://localhost:59882
curl -fsS "$COMMAND/api/v3/device/name/nereid-inference/PipelinesJSON" |
  jq -r '.event.readings[] | select(.resourceName == "PipelinesJSON") | .value' | jq .
```

`pipelineId` + `version` 永久不可变，即使删除版本也保留规范 SHA-256 历史。可选样例
`samples/pipelines/face-recognition-v1.yaml` 实现 YuNet → 五点对齐 → SFace 链；用 profile
`nereid-inference-pipeline` 与 `PipelineId` 绑定装载（绝不使用 `ModelID`）。

## 8. 验证任务

1. 观察服务日志中的取流源（RTSP 时为 ffmpeg）、KServe / OpenAI 调用与解码器注册。
2. 按需触发命令型任务：

   ```bash
   curl -fsS -X PUT \
     "$COMMAND/api/v3/device/name/example-inference-01/Trigger" \
     -H 'Content-Type: application/json' \
     --data-binary '{"Trigger":"run"}'
   ```

3. 读取缓存结果与健康计数：

   ```bash
   curl -fsS "$COMMAND/api/v3/device/name/example-inference-01/DetectionJSON"
   curl -fsS "$COMMAND/api/v3/device/name/example-inference-01/State"
   ```

4. 订阅 EdgeX 消息总线接收异步事件；`PublishMode: nonempty` 时结果数组为空的帧会被抑制。
5. 打开 `http://<宿主>:28080/` 的带标注预览，查看叠加在帧上的框与标签。

!!! warning "预览口仅用于诊断"
    预览服务器无认证。容器内绑定 `0.0.0.0:18080` 以保证端口发布可用；请用宿主绑定、网络
    策略或反向代理限制访问，或把 `Preview.Bind` 设为 `127.0.0.1:18080`。它不是业务 API。

## 9. 实现边界

已实现并真机验证：通用流水线、模型目录、KServe/OpenAI 后端、内置解码器集、HTTP JPEG →
OVMS KServe gRPC → 解码器 → EdgeX 事件/预览路径、一台真实 RTSP H.264 相机、一台 ONVIF
快照相机，以及 CPU 上带 ONNX Runtime 的受管 Triton。

仍在开放清单：默认 ONVIF `GetStreamUri`、H.265、重连与密钥轮换、生产级 Horizon 包、
GPU/OpenVINO 后端 Triton、其他厂商验收，以及样例流水线的真实 NereidForge 人脸包验证
（当前测试使用合成夹具）。

## 故障排查

| 现象 | 可能原因与处理 |
|---|---|
| 任务 `State: FAILED`，`LastError: config-invalid` | 绑定在准入时被拒（属性值非法、`PipelineId` 与 `ModelID` 混用、流水线任务带 `ServableID`）。修正设备协议映射后重新预置。 |
| 启动时提到 `/dev/dri` 后任务显式失败 | `vaapi` 任务找不到 DRM 节点或 VA 驱动。把 `/dev/dri` 映射进容器并安装 `intel-media-driver`（仅 amd64）；不存在静默软件回退。 |
| `State: FAILED` 报 model-not-ready，随后自行恢复 | 最新流水线版本无法解析；先前的活动图继续服务。服务每五秒重试解析，最新定义解析成功后清除故障锁存。 |
| 预览无法访问 | 检查宿主端口映射（`28080→18080`）与 `Preview.Enabled`；若无远程运维需求则绑定到本机。 |
| ONVIF 任务取不到流 | 确认相机已由 ONVIF 相机设备服务注册且 `SourceDevice` 与其 EdgeX 名称一致；服务联邦获取 URI 与密钥，自身不存储。 |
| 重启后密钥消失 | 非安全模式下密钥存储只在内存中；请通过 EdgeX Keeper 或预置流程重新下发。命名密钥绝不允许提交到 `res/`。 |

## 资源

- 仓库：[NereidInference](https://github.com/NereidAI/NereidInference)
- [NereidInference 产品页](../../products/nereidinference.md)
- [Edge 快速开始](../edge/getting-started.md)——把 EdgeX 事件桥接进 Link 的配套服务。
- [边缘分发](../../deployment/edge-delivery.md)——用 NereidHorizon 做生产 rollout。
