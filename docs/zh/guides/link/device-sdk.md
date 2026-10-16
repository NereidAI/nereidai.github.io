---
title: 设备 SDK（Go）
---

# NereidLink 设备 SDK（Go）

设备 SDK 面向从南向接入 NereidLink 的**设备与网关固件**。它是一个*轻量协议库*：
提供类型化帧、凭据、主题绑定与 MQTT/HTTP 传输辅助，不运行任何后台协程或循环，也不做
策略决策——轮询节奏、重连、hello 协商与 manifest 时机完全由固件掌控。

- **模块：** `github.com/nereidai/nereidlink/sdk/device/go`
- **独立于服务端：** 不依赖 NATS、数据库驱动或任何服务端组件。
- **参考程序：** 模块自带 `examples/simple`（直连设备）与 `examples/gateway`
  （完整网关）。

!!! info "开发者文档"
    本页是上手介绍。完整包 API、常量与可运行示例位于 NereidLink 仓库的
    `sdk/device/go/`——见 [NereidAI](https://github.com/NereidAI)。

## 安装

```bash
go get github.com/nereidai/nereidlink/sdk/device/go@latest
```

## 包结构

| 包 | 职责 |
|---|---|
| `device` | 凭据（token / id+secret / X.509）；遥测、命令、影子、属性、事件、OTA、hello/manifest/连接器/发现/探测等帧模型；主题常量 |
| `devicehttp` | HTTP 接入客户端：遥测、长轮询命令、命令响应、影子、OTA 列表 / Range 下载 / 进度 |
| `devicemqtt` | MQTT 接入客户端（Eclipse Paho）：连接、LWT、遥测、属性、事件、命令/影子/属性订阅 |
| `gateway` | 建立在 `devicemqtt` 之上的网关接口：hello、心跳/再见、子设备、manifest、批量遥测、中继命令、连接器、发现、探测、OTA、整网关操作 |

## 凭据

每个客户端都从一种凭据开始：

```go
device.Token("device-access-token")          // MQTT 用户名=token，密码为空
device.Basic("edge-001", "credential-secret") // 用户名 / 密码
device.ClientCert(tlsCert)                    // 双向 TLS（X.509）
```

设备在操作员为其创建并授予至少一个有效凭据之前无法连接——见
[凭据](credentials.md) 与 [接入直连设备](integrate-direct-device.md)。

## 直连设备走 MQTT

```go
client, _ := devicemqtt.Connect(ctx, devicemqtt.Options{
    BrokerURL:  "tcp://nereidlink.example:1883", // 或 tls://...:8883
    Credential: device.Token("device-access-token"),
    ClientID:   "sensor-001",
})
defer client.Disconnect(200)

// 下行 v1/me/cmd/<name>；应答主题 v1/me/cmdres/<id>。
_ = client.SubscribeCommands(ctx, 1, func(cmd device.Command) {
    _ = client.RespondCommand(ctx, cmd.ID, map[string]any{"ok": true}, 1)
})

_ = client.PublishTelemetry(ctx,
    device.NewFrame().SetFloat("temperature", 21.5).SetBool("online", true), 1)
```

MQTT 客户端会绕过 HTTP/SOCKS 代理，因为现场 broker 通常需要直连；除非显式关闭，
TLS 仍会校验 broker 证书。

## 直连设备走 HTTP

```go
httpClient, _ := devicehttp.New(devicehttp.Options{
    BaseURL:    "https://nereidlink.example",
    Credential: device.Token("device-access-token"),
})

_, _ = httpClient.PublishTelemetry(ctx,
    device.NewFrame().SetFloat("temperature", 21.5))

for {
    cmd, _ := httpClient.PollCommands(ctx) // 一次长轮询，由固件循环
    if cmd != nil {
        _ = httpClient.RespondCommand(ctx, cmd.ID, map[string]any{"ok": true})
    }
}
```

**帧规则：** 遥测帧是由数值、布尔、字符串组成的扁平 JSON 对象；`null` 与嵌套
对象/数组在上传前就在本地被拒绝；服务端把每个 key 转成一个 Envelope。平台从不猜测
单位——单位来自所绑定的[设备 profile](glossary/profile.md) 描述符。

## 直连设备 OTA

SDK 只负责传输字节，绝不负责烧录或校验固件——那是固件自己的职责。

```go
list, _ := httpClient.ListOTAAssignments(ctx)
for _, job := range list.Assignments {
    var f *os.File // 固件自己决定字节写到哪里
    res, _ := httpClient.DownloadOTAPackage(ctx, job.TaskID,
        devicehttp.DownloadOptions{Destination: f}) // 支持 Range 续传
    // 应用前先校验 res.SHA256（即 X-Firmware-Sha256 的值）。
    _ = httpClient.ReportOTAProgress(ctx, job.TaskID,
        device.OTAProgress{State: device.OTAStateDownloading, ProgressPct: 50, Bytes: res.Written})
}
```

由你驱动有序状态机：
`initiated → downloading → downloaded → verified → updating → updated → rebooting
→ confirmed/succeeded/failed`。操作侧见 [OTA 任务](ota-tasks.md) 与
[固件](firmware.md)。

## 网关

网关是具备网关能力的设备。它使用设备主题，并在每次连接做一次 **hello** 之后使用
`v1/gateway/*` 主题。

```go
mq, _ := devicemqtt.Connect(ctx, devicemqtt.Options{
    BrokerURL: *broker, Credential: device.Basic(id, secret),
    ClientID: edgeID, Will: devicemqtt.GoodbyeWill("transport_down"),
})
gw := gateway.Wrap(mq)

_ = gw.SubscribeConnectors(ctx, 0, func(push device.ConnectorPush) { /* 应用配置 */ })
_ = gw.SubscribeProbes(ctx, 0, func(req device.ProbeRequest) { /* 逐设备应答 */ })
_ = gw.SubscribeOTATasks(ctx, 0, func(task device.GatewayOTATask) { /* 下载 */ })

ack, err := gw.NegotiateHello(ctx, device.Hello{
    EdgeID: edgeID, AgentVersion: "2.3.1",
    Proto:  device.ProtoRange{Min: "1.0", Max: "1.4"},
    Features: device.FeatureSet{
        Required: []string{device.FeatureTelemetry, device.FeaturePresence},
    },
}, 10*time.Second)

_ = gw.ConnectDevices(ctx, []string{subDeviceUUID}, 1)
_ = gw.PublishTelemetry(ctx, device.GatewayFrame{
    DeviceID: subDeviceUUID, TS: time.Now().UnixMilli(),
    Measurements: device.NewFrame().SetFloat("temperature", 21.5),
})
// 按 ack.Limits.HeartbeatS 调 gw.Heartbeat(...)；周期性 gw.SendManifest(...)。
```

以下职责属于**固件而非 SDK**：

- **每次**重连后都要重新 hello；服务端状态会重置为未识别，ack 之前发的帧会被丢弃。
- 按协商间隔发送心跳；崩溃时 LWT 自动触发，优雅退出时主动发 `Goodbye`。
- 本地维护链路看门狗，用 `ReportLinkEpisode` 上报每次非计划断连/恢复区间；积压按
  最旧优先重放，平台去重。
- 按对齐的节奏发送全量 `Manifest`（连接器为零时也要显式带空的连接器段）。
- 按 `(spec_id, revision)` 对连接器推送去重；每次 hello 后服务端都会重发完整期望集。

另见[网关术语](glossary/gateway.md)、[接入网关](integrate-gateway.md) 与
[网关操作](gateway-operations.md)。

### 整网关操作

整网关、菜单驱动的 RPC（ping/reboot/…）与子设备命令不同。**平台不内置任何操作名**
——固件在 hello 中声明目录，且只执行自己声明过的操作：

- 在 hello **之前**订阅（`gw.SubscribeOperations`），在 `Hello.Operations` 中声明条目，
  带双语显示名、交互方式（`request-response`/`one-way`）、超时、风险级别
  （`read`/`normal`/`dangerous`）与内联 JSON Schema。
- hello ack 逐条返回 `accepted`/`reason`；单个条目被拒不会让握手失败。命名空间使用
  `diag.*` / `sys.*` / `service.*` 与 `vendor.<vendor>.*`；破坏性变更需要新 key 或
  `type_version`。
- 在 `inv.TimeoutMs` 内用 `gw.RespondOperation` 应答请求-响应操作；`secret://` 参数在
  最后一里还原为明文，切勿记录日志。

## 当前边界

SDK 跟随服务端已实现的行为，少数能力有意尚未开放：

- 边缘 → 平台对象存储的 blob 中继仍延后。
- 网关发布的域事件服务端尚未实现。
- hello 的 `resume.last_cursor` 会被接受但尚无游标重放；期望状态为全量、幂等地重发。
- 下行 MQTT 帧为 QoS 0、非保留；上行建议选 QoS 1。
