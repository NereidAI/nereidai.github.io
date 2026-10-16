---
title: 适配器 SDK（Go）
---

# NereidLink 适配器 SDK（Go）

适配器 SDK 让开发者以独立项目或独立仓库的形式，为 NereidLink 增加一种**新的南向线
协议**。适配器把一种线协议翻译成平台契约；它**不拥有命令状态机，也不存储任何权威
状态**。

它与[设备 SDK](device-sdk.md) 不同：设备 SDK 用在*设备/网关固件内部*，而适配器 SDK
用于构建一个*随平台或在平台侧运行*的新接入连接器。

!!! info "开发者文档"
    本页介绍模型与生命周期。包 API 与完整参考适配器位于 NereidLink 仓库的 `sdk/`
    与 `adapters/`——见 [NereidAI](https://github.com/NereidAI)。

## 包结构

| 包 | 职责 |
|---|---|
| `sdk/adapter` | 生命周期：配置加载、注册（enrollment）、心跳、在线状态客户端、命令分发、基于请求的会话 / 邮箱中继 |
| `sdk/contract` | 稳定线契约：分发/事件主题前缀、命令状态、交互方式、生命周期 `Event` |
| `sdk/telemetry` | 遥测上行：JSON 帧 → 类型化点位 → 每点位一个 `Envelope` → JetStream 分区；stream 确保；通过可注入的 `MediaStore` 卸载二进制媒体（`blob://` 引用） |
| `sdk/registry` | 用于设备认证的 Registry gRPC 客户端 |
| `sdk/profile` | 可选的 profile 描述符解析（PostgreSQL 支撑、带缓存）与原始值到工程值的转换 |
| `sdk/partition` | 上行使用的不可变分区拓扑 |
| `sdk/scriptruntime` | 表达式描述符使用的 JavaScript 运行时 |
| `api/gen/nereidlink/v1` | 生成的 protobuf 消息类型 |

SDK **不依赖服务端的 `internal/` 目录树**。SDK 包的破坏性变更遵循语义化版本；内部包
随时可能变化。

## 适配器生命周期

1. 加载共享配置并连接 NATS（Core + JetStream）。
2. 可选地用 `telemetry.EnsureStreams` 确保遥测 stream。
3. 用模块类型、ingress ID 与版本调用 `adapter.Enroll(...)`。
4. 启动在线状态（`Run`）并订阅命令分发。
5. 把协议流量翻译成 `telemetry.Publish` 调用；把分发下来的命令翻译成协议写入；通过
   命令处理器应答。当协议携带二进制负载时，针对你的存储实现 `telemetry.MediaStore`，
   并传入 `telemetry.WithMediaStore(...)`；帧的 `data` 字段保持 base64，已发布点位以
   `blob://<key>` 引用对象。
6. 优雅关闭时断开会话、让心跳停止。

`adapters/template` 提供带注释的完整骨架；内置的 CoAP 适配器（`adapters/coap`）是
完整参考实现。

## 新建外部项目

```bash
mkdir myadapter && cd myadapter
go mod init github.com/example/myadapter
go get github.com/nereidai/nereidlink@v0.0.1
```

把 `adapters/template/main.go` 复制为你的 `main.go`。只需要上面列出的 SDK 包——外部
模块绝不允许 import `internal/`（Go 本身也会禁止）。

## 共享配置

```yaml
core:
  nats_url: nats://127.0.0.1:4222
  nats_user: module
  nats_password: module-password
  registry_grpc: 127.0.0.1:19090
  registry_token: dev-module-token
  management_url: http://127.0.0.1:8080
  postgres_dsn: ""            # 可选；启用描述符解析
module:
  enrollment_token: my-enrollment-token
  heartbeat_interval: 10s
```

协议特有配置由适配器自己负责：用一个额外的包装结构体解析同一个 YAML 文件。

## 契约不变量

- API 响应中的数组始终是 `[]`，绝不为 `null`。
- 平台从不臆造语义（例如单位）——语义只来自用户定义的描述符。
- 处理平面逻辑不要放进连接平面；业务逻辑不要放进适配器：规则由租户在平台中定义。

## 下一步

- [设备 SDK（Go）](device-sdk.md)——把客户端嵌入设备/网关固件。
- [接入网关](integrate-gateway.md) 与[连接器术语](glossary/connector.md)——适配器如何
  呈现为可在控制台管理的连接器。
