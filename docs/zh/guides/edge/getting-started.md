# NereidEdge 快速开始

NereidEdge 是一个 EdgeX Foundry **应用服务**（App Functions SDK Go v4.0.2），把 EdgeX 南向设备与
配套服务接入 NereidLink。它把 EdgeX 事件与 reading 经 MQTT 网关协议 `v1/gateway/*` 转换为
Link 网关遥测，把 EdgeX 设备名映射为 Link 子设备 UUID，并负责边缘本地生命周期管理：连接器
对账、密钥投递、设备命令、链路健康跟踪，以及——当 NereidInference 存在时——中立的推理桥接。

!!! tip "与 Link 配合即可独立运行"
    Edge 只需要一个可达的 Link broker 与网关凭据，不需要 Sphere 或 Horizon 即可运行。Horizon
    是在大量站点间分发并持续更新 Edge 的手段，而非运行时依赖。NereidInference 同样是可选的：
    Edge 在运行时探测到它之后才会提供推理能力。

## 架构

```text
EdgeX 设备/服务 ---> EdgeX 消息总线 ---> NereidEdge ---> NereidLink MQTT
                                                    |
                                                    +---> 辅助 MQTT broker

NereidLink 下行 ---> NereidEdge ---> EdgeX 核心服务 / NereidInference
NereidInference 状态 ---> NereidEdge ---> NereidLink manifest/shadow/遥测
```

Edge 的职责：

- **遥测与在线状态**——把 EdgeX 事件/reading（含二进制媒体标记）转换为网关遥测；子设备在
  首次遥测时上线，在分离/关停时撤销在线状态；每五分钟发送一次完整设备 manifest。
- **受治理的连接器生命周期**——通过带类型的处理器应用设备级与节点级连接器规格，具备 schema
  广告、修订去重、属主/冲突检查与 manifest 对账。带外删除的 EdgeX 设备会在下一轮对账中修复。
- **节点级 MQTT 导出**——把事件从默认流水线扇出到独立管理的 `edge-export-mqtt` 实例，支持
  资源过滤、主题模板、认证/TLS、有界队列与重连退避。
- **设备控制与健康**——方向感知命令、按需探针、逐实例健康检查、上报的网关 shadow 与在线
  `log.level` 更新。
- **密钥投递**——静态加密存储 ADR-0034 密钥副本，对账修订与删除，把 ONVIF 流密钥扇出给
  NereidInference，且绝不写入连接器规格或日志。
- **推理桥接（ADR-0039）**——桥接模型目录、绑定、相机 profile、管理器资源、绑定状态与检测
  遥测。Edge 自身绝不获取模型包、不接触帧、也不调用模型服务器。

## 前提条件

- 网关上的 EdgeX Foundry 4.0.2 栈：core-keeper、NATS 核心总线、core-data、core-metadata、
  core-command 与所需设备服务。
- 可达的 Link MQTT broker（明文用 `tcp://`，TLS 用 `tls://`）。
- 在 Link 控制台创建的 **网关凭据**：Credential ID、凭据密钥与网关 Edge ID——平台侧见
  [网关接入](../link/integrate-gateway.md)，概念见[网关](../link/glossary/gateway.md)。
- 每个现场设备已在 Link 中注册为绑定到该网关的子设备，已知其子设备 UUID。
- 从源码构建需要 Go 1.27.3；运行 `make verify` 还需 golangci-lint。NereidLink 设备 SDK 以
  仓内审阅镜像形式位于 `third_party/nereidlink`，无需相邻检出或私有模块令牌。

## 1. 准备平台侧

在 Link 控制台创建网关设备、添加网关凭据，并把每个现场设备注册为绑定到该网关的子设备。记录
所有子设备 UUID——Edge 会把 EdgeX 设备名映射到它们。先阅读
[网关接入](../link/integrate-gateway.md) 中的握手流程（hello、heartbeat、manifest），后续看
Edge 日志会顺畅很多。

## 2. 配置 NereidEdge

编辑 `res/configuration.yaml` 中 EdgeX 自定义配置的 `NereidEdge` 段（容器部署时每个键都有
`NEREIDEDGE_*` 环境变量覆盖）：

| 键 | 含义 |
|---|---|
| `BrokerURL` | Link MQTT broker，`tcp://host:1883` 或 `tls://host:8883`。scheme 决定是否启用 TLS。 |
| `CredentialID` | **任何认证模式（含 mTLS）下都必填。** 密码认证时是 MQTT CONNECT 用户名；证书认证时命名 X509 凭据。必须与 Link 中已注册的 ID 一致。 |
| `CredentialSecret` | 密码/令牌密钥；X509 客户端证书认证时留空。 |
| `EdgeID` | 网关身份；留空时回退到 `CredentialID`。 |
| `DeviceMap` | 逗号分隔的 `edgex名称:link-uuid` 对。静态映射优先于连接器规格绑定。 |
| `ForwardUnmapped` | `false`（推荐）跳过无已知映射设备的遥测。 |
| `ConnectorObserve` | `true` 时只记录计划的连接器动作、不修改 EdgeX 元数据——适合首次演练。 |
| `CoreCommandURL` | EdgeX core-command 基址；默认取 Compose 主机名。 |
| `RootCAFile` / `RootCAPEM` | 私有 CA broker 固定，分别用挂载文件或内联 PEM。 |
| `ClientCertFile` + `ClientKeyFile`（或 `*PEM`） | mTLS 证书对；两半必须使用同一种交付方式。 |
| `InsecureSkipVerify` | 仅限实验室 broker——生产环境绝不启用，应改为固定 CA。 |
| `ProfileWatch.Enabled` | core-metadata 一报告设备 profile 增改就推送事件；五分钟全量扫描仍作为兜底。 |
| `MQTTTrace` | 逐包 paho 详细跟踪，仅用于传输取证。 |

最小明文配置：

```yaml
NereidEdge:
  BrokerURL: "tcp://<link-mqtt-host>:1883"
  CredentialID: "<your-cred-id>"
  CredentialSecret: "<your-cred-secret>"
  EdgeID: "<edge-instance-id>"
  DeviceMap: "edgex-device-1:<link-subdevice-uuid-1>,edgex-device-2:<link-subdevice-uuid-2>"
  ForwardUnmapped: false
```

### 持久化状态与密钥

挂载 `/app/data` 以持久化状态：ADR-0034 密钥副本、profile 修订台账与推理管理器资源台账都位于
此。请提供稳定的 32 字节 `Secrets.KeyFile`；密钥文件为空时使用临时密钥，重启后平台必须重新
下发全部密钥。

## 3. 构建与运行

### 裸机

```bash
make build-local     # 当前平台二进制
make verify          # gofmt、go vet、golangci-lint、全部测试、linux/amd64 构建
./nereid-edge        # 从仓库根目录运行，以便发现 res/
```

EdgeX 服务键为 `nereid-edge`，默认 HTTP 端口 `59750`。启动时 Edge 执行 Link hello/特性协商，
随后开始中继遥测。

### Docker Compose（网关推荐）

Compose 文件要求外部网络 `edgex_edgex-network`，以只读方式挂载 `res/`、持久化 `/app/data`，
并在启动时重建本地镜像。

```bash
cp .env.example .env      # 填写 broker URL 与网关凭据
make up                   # 即 docker compose --env-file .env up -d --build
make logs
```

以 `.env.example` 作为变量参考，凭据始终放在版本控制之外。需要额外覆盖（`NEREID_EDGE_ID`、
`NEREID_DEVICE_MAP`、TLS 挂载）时，把 `docker-compose.override.yaml.example` 复制为
`docker-compose.override.yaml`。选择其他运维档案：
`make up ENV_FILE=compose.k3s.env`。

### 镜像制品

```bash
make docker        # linux/amd64、linux/arm64 OCI 归档，位于 dist/images（不推送）
make docker-dev    # 本地原生 ghcr.io/nereidai/nereidedge:<version> tag
```

两个目标都不登录、不推送；GHCR 发布只由 CI 工作流完成（每次推 `main` 发布滚动 `0.0.0-dev`
通道，`v*` tag 发布三 tag SemVer 版本，绝不打 `latest`）。

## 4. TLS 与 mTLS

三种信任模型，完全由配置选择：

| Broker 证书 | 认证方式 | 需要设置 |
|---|---|---|
| 公共 CA | id/secret | 只需把 `BrokerURL` 改为 `tls://`；镜像信任库负责校验 |
| 私有 CA | id/secret | 用 `RootCAFile`/`RootCAPEM` 固定 CA PEM |
| 私有 CA / mTLS 监听器 | X.509 客户端证书 | 固定 CA，**并且**成对设置 `ClientCertFile`+`ClientKeyFile`（或内联 `*PEM`） |

PEM 交付规则：

- 文件路径与内联文本同时存在时内联 PEM 优先；优先用文件，因为环境值会被种入 core-keeper 且
  可通过 `docker inspect` 看到。
- YAML 中用块标量（`|`）；`.env` 文件中每个 PEM 写成一行、以字面量 `\n` 分隔——可用
  `awk 'NF {printf "%s\\n", $0}' ca.pem` 生成。PKCS#8（`BEGIN PRIVATE KEY`）与
  SEC1（`BEGIN EC PRIVATE KEY`）密钥头均受支持。
- TLS SNI/校验名自动从 `BrokerURL` 主机推导，没有单独的 ServerName 配置。
- 辅助 `edge-export-mqtt` broker 有自己的 `ca_cert`/`client_cert` 连接器字段，需单独配置。

## 5. 验证桥接

1. 服务健康：`GET http://<宿主>:59750/api/v4/ping` 返回 `pong`。
2. Link 控制台中网关及其映射的子设备显示**在线**。子设备在首次遥测时上线，Edge 每五分钟发送
   一次完整 manifest；heartbeat 间隔按 hello ack 协商结果执行。
3. 打开一个子设备确认 reading 在更新——EdgeX reading 现在以映射后的 UUID 为键出现在 Link
   遥测中。
4. 通过网关操作 `sys.logs_tail` 拉取诊断日志尾部；容器同时把按大小轮转的日志写到数据卷。

若无数据到达，检查 `DeviceMap` 对、EdgeX 事件是否经消息总线到达应用服务，以及凭据与 Edge ID
是否通过协商。计划内 goodbye 与非计划断连会在链路健康事件记录中区分；重连后自动重放订阅与
状态。

## 6. 推理桥接（可选）

所有推理相关能力同时受两个门控：`Inference.Enabled: true`（静态默认值）**与**运行时存在性
探测——Edge 在首次 hello 前及之后每 30 秒调用 core-metadata
`DeviceByName(nereid-inference)`。

| 部署形态 | 探测结果 | 行为 |
|---|---|---|
| 未安装 NereidInference | 管理设备返回 404 | hello 不带推理块；无 `edge-inference` schema；与无此特性的固件字节级一致 |
| 已安装但暂时不可达 | 曾成功读取后本次失败 | 会话保持协商；缓存上一份良好目录（绝不替换为空列表）；shadow 上报 OFFLINE |
| 已安装且零模型 | 成功读到 `[]` | 每个 manifest 周期显式发送空 `models` 段；Link 硬剪枝目录 |

启用后，Edge 桥接模型目录（`ModelsJSON`）、经 `edge-manager-resource` 传递的不透明管理器数组
（GET → 合并 → PUT → GET，带持久重放）、经 `edge-inference` 连接器下发的模型与流水线绑定、
相机 profile、绑定状态、运行时 shadow 块，以及可选检测遥测（含以二进制媒体标记承载的证据
JPEG）。北向隐私过滤对 Link 与辅助 MQTT 出口同时生效。

`NereidEdge.Inference` 关键设置：`Backends`（`[kserve, openai]`，只写协议族——绝不写厂商名）、
`DeviceService`（`device-inference`）、`ManagerDevice`（`nereid-inference`）、
`InventoryPollS`/`ShadowPollS`（30 秒）与 `BindingPollS`（10 秒）。

!!! warning "生产门"
    Edge 单元测试与 NereidInference 合成测试只建立了传输行为，完整的
    Link → Edge → EdgeX → Inference 端到端链路仍取决于 Link 管理器资源交付与最终跨产品签收。
    请把推理桥接视为已文档化的集成面，而非已通过生产验证的链路。

## 故障排查

| 现象 | 原因与处理 |
|---|---|
| 启动失败：`CredentialID is required, including mTLS` | 证书认证也必须提供 ID，且须与 Link 中注册的 X509 凭据名一致。证书模式下 `CredentialSecret` 留空。 |
| `ClientCertPEM and ClientKeyPEM must be configured together` | 证书/密钥必须以同一种交付方式成对提供；混用内联 PEM 与文件路径会被拒绝。 |
| `read NereidEdge.*File: no such file` | PEM 路径指向容器外；只读挂载宿主证书目录并使用容器内路径。 |
| `x509: certificate signed by unknown authority` | 未固定 broker CA；把 `RootCAFile`/`RootCAPEM` 设为签发 CA 的 PEM。 |
| `x509: certificate is valid for ...` | broker 证书 SAN 与 `BrokerURL` 主机名不匹配；改用匹配主机名或重新签发证书。 |
| 遥测未转发 | 检查 `DeviceMap`、未映射设备在 `ForwardUnmapped: false` 下的行为，以及 EdgeX 事件是否到达总线。 |
| 协商失败 | 检查 hello/ack 交换中的 `EdgeID`、凭据有效性与特性兼容性。 |
| 连接器显示 APPLIED 但设备拒绝 | EdgeX 多状态（HTTP 207）可能携带逐项拒绝而传输错误为 nil；Edge 会检查每个条目状态并上报 `config-invalid`——要看条目级状态码，不能只看传输结果。 |
| NI 重启后推理密钥消失 | NereidInference 非安全密钥存储只在内存中；Edge 每 30 秒并在每次任务 upsert 前重新下发引用到的密钥，不要依赖一次性手工 POST。 |

## 资源

- 仓库：[NereidEdge](https://github.com/NereidAI/NereidEdge)
- [NereidEdge 产品页](../../products/nereidedge.md)
- [NereidInference 快速开始](../inference/getting-started.md)——配套的设备服务。
- [网关接入](../link/integrate-gateway.md)——北向 `v1/gateway/*` 契约。
- [边缘分发](../../deployment/edge-delivery.md)——用 NereidHorizon 做生产 rollout。
- 仓库内文档：`docs/deployment.md`、`docs/edge-inference.md`、`docs/logging.md`。
