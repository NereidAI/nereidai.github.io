# 网关设备接入

本篇面向**[网关](glossary/gateway.md)/边缘节点开发者**：网关节点通过**一条** MQTT 连接接入
NereidLink，并在其后管理大量**[子设备](glossary/subdevice.md)**（Modbus/ONVIF/S7 等现场总线或本地设备
服务）。

- **传输方式：** MQTT 3.1.1 / 5.0 over TLS（mTLS 可选）。
- **载荷格式：** JSON，UTF-8。
- **官方 SDK：** Go —— `github.com/nereidai/nereidlink/sdk/device/go` 的
  `gateway` 包；完整参考程序见 `examples/gateway`。其他语言可直接按本文档的
  线协议实现。
- 平台不理解任何南向协议。平台子设备 UUID 与本地设备之间的映射完全由网关
  负责。

## 1. 平台侧前置条件

1. 网关本身在平台注册为**网关类型**设备，并拥有自己的凭据（ID+密钥、令牌或
   X.509 证书）。
2. 每台子设备都在控制台注册并**绑定到该网关**。网关只能操作绑定到自己的子
   设备；发往其他网关或未挂载子设备的帧会被丢弃。
3. 子设备的 profile 声明遥测点名称；命令必须先在该设备的命令目录中声明，才能
   下发。

## 2. 会话生命周期

状态机：`UNIDENTIFIED → NEGOTIATED → CLOSED`。

1. 建立 MQTT 连接时预先注册 LWT 到 `v1/gateway/goodbye`。
2. 订阅 hello 响应 topic（或使用 MQTT 5 Response Topic）。
3. 发布 `v1/gateway/hello`；协商必须在 10 秒内完成。
4. 只有收到成功 ack 后才能使用网关数据 topic。协商完成前发出的帧一律丢弃。
   每条连接只协商一次。

### Hello（网关 → 平台），topic `v1/gateway/hello`

```json
{
  "v": 1,
  "edge_id": "edge-001",
  "agent_version": "2.3.1",
  "proto": {"min": "1.0", "max": "1.4"},
  "features": {
    "required": ["telemetry", "presence"],
    "optional": ["ota", "shadow", "blob-relay", "command"]
  },
  "connectors": [
    {"type": "modbus", "type_version": "2.1",
     "config_schema": {"type": "object", "required": ["host"],
       "properties": {"host": {"type": "string"}, "port": {"type": "integer"}}}}
  ],
  "client_time": 1727360000123
}
```

- `features.required` 必须全部被服务端支持，否则协商失败
  （`incompatible_features`）；`features.optional` 中服务端不支持的项会被
  降级移除。可用特性：`telemetry`、`presence`、`ota`、`shadow`、
  `blob-relay`、`command`。
- `connectors[]` 可选，用于登记本网关能运行的连接器类型的**内联自包含** JSON
  Schema（draft 2020-12，不支持外部 `$ref`）。单条 schema 非法不会导致握手
  失败，其结果在 ack 中逐条回告。
- `agent_version` 是固件版本字符串，与协议版本相互独立。

### Ack（平台 → 网关），topic `v1/gateway/hello/ack`

```json
{
  "session_id": "s_...",
  "status": "ok",
  "selected": "1.4",
  "server": {"min": "1.0", "max": "2.0", "version": "nereidlink-..."},
  "features": ["telemetry", "presence", "command"],
  "limits": {"heartbeat_s": 30, "hello_timeout_s": 10,
             "upload": {"max_mb": 256, "qps": 20}},
  "time": {"server_time": 1727360000456, "offset_ms": -312, "clock_warning": false}
}
```

Ack 状态：`ok`、`auth_failed`、`incompatible_version`、
`incompatible_features`、`quota_exceeded`。心跳间隔以 `limits.heartbeat_s`
为准。每次重连后服务端状态都重置为 `UNIDENTIFIED`：必须重新 hello、重新订阅、
重新上报状态。

## 3. 在线探测：心跳、goodbye 与 LWT

- 按协商间隔向 `v1/gateway/heartbeat` 发布心跳：

```json
{"seq": 42, "client_time": 1727360060000}
```

- CONNECT 时将 `v1/gateway/goodbye` 预注册为 MQTT 遗嘱。优雅停机时显式发布
  该消息并带 `planned: true`：

```json
{"reason": "upgrade", "planned": true}
```

  broker 投递的 LWT 不带 `planned` 标志，因此崩溃停机与计划内停机可区分。
- 心跳缺失会驱动平台看门狗（`HEALTHY → SUSPECT → DOWN`），并级联导致其挂载
  子设备离线。goodbye（计划内或 LWT）会抑制可疑计时器。

### 3.1 Link episode 补发（`v1/gateway/linkhealth`）

网关本地运行 link 看门狗，每次非计划断连在重 hello 成功后补发该 episode（QoS1）：

```json
{
  "edge_id": "<网关UUID>",
  "session_id": "s_…",
  "down_at": "2026-10-10T03:12:44Z",
  "up_at": "2026-10-10T03:12:49Z",
  "reason": "transport_down"
}
```

- `edge_id` 必须与本连接的网关设备 id 一致；`down_at`/`up_at` 为 RFC3339（边缘时钟即
  ground truth），`up_at` 不得早于 `down_at`；`session_id` 可选。
- 平台会校正匹配的 lease episode，或为短于 lease 窗口的闪断记录一条已闭合、无告警的
  episode，并在 `v1/gateway/linkhealth/ack` 回 `accepted` / `duplicate` / `rejected`。
  收到三者之一即停止重传；未收到 ack（服务端瞬时错误）才重试。
- 积压补发即按时间最旧在前发 QoS1 帧，平台按 `(edge_id, down_at)` 去重。10 分钟内 ≥5 条
  未匹配 episode 会打开 flapping 告警，安静满 10 分钟后自动闭合。

## 4. 子设备 [presence](glossary/presence.md)

| Topic | 方向 | 载荷 |
|---|---|---|
| `v1/gateway/connect` | 发布 | `{"devices": ["<uuid>", ...]}` |
| `v1/gateway/disconnect` | 发布 | `{"devices": ["<uuid>", ...]}` |
| `v1/gateway/manifest` | 发布 | 每 5 分钟一次的全量状态对账 |

子设备挂载/卸载时批量上线下线。manifest 是权威的周期性全量清单，平台据此对账
desired 与 reported presence：

```json
{
  "devices": ["<uuid-1>", "<uuid-2>"],
  "connectors": [
    {"spec_id": "ci-...", "revision": 3, "config_hash": "..."}
  ],
  "missed_cycles": 0
}
```

- `connectors` 字段的存在与否有明确语义：**省略该字段**表示跳过连接器对账；
  显式发送空数组 `[]` 表示"当前零个连接器实例"。
- 每次都必须列出当前挂载的全部子设备 UUID；manifest 是全量状态，不是增量。

## 5. 子设备[遥测](glossary/telemetry.md)

向 `v1/gateway/telemetry` 发布批量数据。载荷是以子设备 UUID 为键的映射，每个
值就是直连设备上报的那种扁平标量帧，可带可选 `ts`（epoch 毫秒）：

```json
{
  "07704cf9-...": {"ts": 1728374400000, "MACAddress": "AA:BB:CC:00:11:22"},
  "089fbb69-...": {"temperature": 23.1, "online": true}
}
```

规则与直连设备完全相同：值只能是数字/布尔/字符串（不允许嵌套对象或数组）；
每个键一条存储记录；未声明键照常存储但不做描述符转换。值也可以是
`{"blob":true,...}` 标记（见直连设备集成）：媒体存入
`media/<租户>/<子设备>/...`，点变为 `blob://` 引用。

CLIENT 作用域属性走 `v1/gateway/attributes`，形状为 `{device: {key: value}}`；
SERVER/SHARED 属性推送从 `v1/gateway/attributes/push` 接收，帧为
`{"device":"...","scope":"...","data":{...}}`。每次（重）连后，网关应为每个已挂载
子设备发布一次 `v1/gateway/attributes/get`（`{"device":"...","scopes":[...],"response_topic"?}`，
`scopes` 省略即 SERVER_SCOPE+SHARED_SCOPE），并用 `v1/gateway/attributes/get/ack`
中每个 scope 的全量键值整体替换本地缓存。推送 `data` 中值为 JSON `null` 表示该键已删除，
应移除本地缓存（不要保存 null）。当前版本 SERVER_SCOPE 与 SHARED_SCOPE **都会下发给设备**
（不同于经典 ThingsBoard 中 SERVER_SCOPE 平台私有），不要假设 SERVER_SCOPE 为私有。
网关**自身**的属性走直连设备 topic：`v1/me/attributes`、`v1/me/attributes/down`、
`v1/me/attributes/get`、`v1/me/attributes/get/ack`——网关本身也是一个设备，网关整机的
运行旋钮（如日志级别、追踪开关）从这里下发，而不是 `v1/gateway/...`。

## 6. 子设备命令

命令按子设备在平台命令目录中逐一声明；网关只负责在本地总线上执行。

### 下行（平台 → 网关），topic `v1/gateway/command`

一个订阅服务所有子设备，由帧中的 `device` 字段选择目标：

```json
{
  "command_id": "01J8...",
  "device": "07704cf9-...",
  "interaction": "request-response",
  "timeliness": "realtime",
  "method": "DeviceInformation",
  "direction": "read",
  "params": {}
}
```

- `interaction`：`one-way`（无需回复）或 `request-response`（恰好一个关联
  回复）。
- `timeliness`：`realtime`（离线快速失败）或 `persistent`（平台侧排队；网关
  只会看到在线时的实时帧）。
- `method` 是命令目录中的命令名；`params` 是经目录校验、原样送达的 JSON。
- `direction`：`read` 或 `write`，表示南向操作语义（读资源 / 写资源），与
  `interaction` 正交。网关**必须严格按 `direction` 执行 GET/写操作，不得根据
  method 自行推断**；read 同样可能携带 `params`（查询参数）。`one-way` 命令
  不会带 `direction=read`。

### 上行（网关 → 平台），topic `v1/gateway/command/response`

```json
{
  "command_id": "01J8...",
  "device": "07704cf9-...",
  "data": {"manufacturer": "Acme", "model": "Cam-9", "firmware": "1.4.2"}
}
```

- `command_id` 与 `device` 原样回显；`data` 为任意 JSON。
- `one-way` 命令不发送任何回复。
- 本地执行失败时（现场总线不可达、读错误、超时），请求-响应命令**仍须回复**，
  把错误放进 `data`，例如 `{"error": "no response from field bus"}`。
  完全不回复会导致平台侧 `TIMEOUT`。
- 响应只接受来自挂载该子设备的同一网关。

Go SDK 用法：

```go
_ = gw.SubscribeCommands(ctx, 1, func(cmd device.GatewayCommand) {
    if cmd.Interaction != device.InteractionRequestResponse {
        return // 单向命令：静默执行
    }
    result := executeOnFieldBus(cmd.Device, cmd.Method, cmd.Params)
    _ = gw.RespondCommand(ctx, cmd.CommandID, cmd.Device, result, 1)
})
```

### 6.1 子设备影子（desired / reported）

影子按**设备 UUID** 存储、与传输方式无关：网关**自身**的影子走直连语义的
`v1/me/shadow/*`；网关代理的子设备影子走下面的批量网关 topic。

- 向 `v1/gateway/shadow/report` 上报一台或多台子设备的 reported。单子设备就是长度为
  1 的数组：

```json
{
  "reports": [
    {"device": "07704cf9-...", "state": {"led": "on", "brightness": 7}, "version": 3},
    {"device": "089fbb69-...", "state": {"rpm": 1200}}
  ]
}
```

  `state` 是按顶层键合并的补丁（值为 JSON `null` 时删除该键）；`version` 可选，用
  于确认刚应用的 desired 版本。逐条独立鉴权、独立入库：`device` 为空、不是 UUID 或
  未 attach、`state` 不是对象或为空时，只丢弃并审计该条，其余条目照常入库。顶层 JSON
  无法解析时整帧丢弃。

- 只需订阅一次 `v1/gateway/shadow/desired`，再按 `device` 分发。与直连通道一样，
  desired **永远是全量**而非增量——对每个具名子设备整体替换本地 desired：

```json
{"desired": [{"device": "07704cf9-...", "version": 3, "desired": {"led": "on"}}]}
```

  desired 变化时、以及子设备 ONLINE 且 `desired_version > 0` 时都会重推全量，无需按
  设备 get。

Go SDK：

```go
_ = gw.SubscribeSubdeviceShadowDesired(ctx, 1, func(frame device.GatewayShadowDesiredFrame) {
    for _, d := range frame.Desired {
        applyLocalDesired(d.Device, d.Version, d.Desired) // 全量替换
    }
})

_ = gw.ReportSubdeviceShadow(ctx, []device.GatewayShadowReport{
    device.NewGatewayShadowReportForVersion("07704cf9-...", map[string]any{"led": "on"}, 3),
}, 1)
```

## 7. 连接器生命周期（desired / reported）

连接器实例以 NereidLink 为系统记录者；网关应用 desired 状态并回报实际运行
状态。

- 只需订阅单一过滤器 `v1/gateway/connectors/#`。desired spec 从
  `v1/gateway/connectors/spec` 接收（`spec_id`、`connector_type`、
  `type_version`、`config`、`mappings`、`health_check`、`revision`），删除从
  `v1/gateway/connectors/delete` 接收。
- 每次 hello 后平台都会**幂等地重发完整 desired 集合**；按
  `(spec_id, revision)` 去重。
- 在 `v1/gateway/connectors/status` 上按状态机
  `CREATING → APPLIED / FAILED / DEGRADED` 回报，回显 `spec_id` 与
  `revision`。

### 实例存活探测（`health_check`）

绑定单个子设备的 spec 可能携带 `health_check`：

```json
{"resource": "camera_status", "interval_ms": 30000,
 "timeout_ms": 5000, "fail_threshold": 3}
```

- 每 `interval_ms` 对该子设备**读一次 `resource`**；读数**一律丢弃**，禁止写入
  telemetry/shadow/任何 Envelope 上报。
- 连续 `fail_threshold` 次失败或超时即在 `v1/gateway/disconnect` 宣告该子设备
  离线；之后首次成功探测在 `v1/gateway/connect` 宣告恢复（只发状态边沿）。
- 字段消失或 spec 删除时停止探测；该机制与 MQTT 传输层 keepalive 相互独立。

控制台侧的操作流程见帮助中心的**连接器**篇。

## 8. 可选能力

| 能力 | 下行 | 上行 | 说明 |
|---|---|---|---|
| 按需探测 | `v1/gateway/probe` | `v1/gateway/probe/response` | 按子设备做可达性测试；逐设备或用 `responses[]` 批量回报 |
| 发现 / 自动开通 | `v1/gateway/discovery/result` | `v1/gateway/discovery` | 上报扫描候选，平台将本地 ID 映射为 UUID |
| OTA | `v1/gateway/ota/task` | `v1/gateway/ota/progress` | 外部固件 URL，有序进度状态 |
| Profile 库 | — | `v1/gateway/profiles` | 上报本地设备 profile 供控制台采用 |
| 属性推送 | `v1/gateway/attributes/push`、`v1/gateway/attributes/get/ack` | `v1/gateway/attributes`、`v1/gateway/attributes/get` | SERVER/SHARED 下发 + CLIENT 上报；`null` 表示删除 |
| 设备影子 | `v1/gateway/shadow/desired` | `v1/gateway/shadow/report` | desired/reported 影子状态 |
| 网关操作 | `v1/gateway/operations/invoke` | `v1/gateway/operations/result` | 同步网关整机动作；见第 9 节 |

只在 hello 的 `features`（会话级特性）中声明实际实现的能力，其余不要发布。

## 9. 网关操作（网关整机动作）

操作是作用于网关自身的即时动作（重启、厂商维护例程），与子设备命令（第 6
节）不同。平台不内置任何操作词汇：在 hello `operations[]` 中广告本固件实现的
 catalog descriptor——操作标识名、交互方式（`request-response`/`one-way`）、超时、
 参数/结果 JSON Schema 与风险级（`read`/`normal`/`dangerous`）。

平台对每个网关的描述符**各自存储**（migration 0080）：两台网关广告相同键也互不覆盖，
调用时按**目标网关自己的副本**校验。为保持多厂商机群一致，请遵守下列命名/版本规则：

- `operations[]` 每次 hello 都是该网关当前操作的**全量集合**：后续 hello 未提交的键会被
  对账删除。不说话术的老固件应整体缺省该字段（null）；显式发送 `[]` 表示清空。
- `operation`+`type_version` 即契约：跨网关同名同版本的参数、结果、risk、interaction
  必须完全一致。
- 通用动作使用标准命名空间 `diag.*`（诊断）、`sys.*`（本机信息/维护）、`service.*`
  （托管服务）；厂商动作必须使用 `vendor.<厂商标>.*`，避免与标准键撞名。
- 破坏性契约变更必须换 `type_version`（或换新键，如 `diag.ping.v2`），因为调用帧不选版本；
  同一网关广告多个版本时调用最新一条。
- 控制台按各网关广告聚合，并在同名同版本契约不一致时标记**契约冲突**。

- 订阅 `v1/gateway/operations/invoke`。调用帧含 `id`、`operation`、`type_version`、
  `params`（已校验）与 `timeout_ms`；帧中的 `timeout_ms` 是实际生效时限——取描述符
  默认值与操作员本次下调值的较小者，并钳制在 100–60000 毫秒。在
  `v1/gateway/operations/result` 以相同 `id` 回报 `ok` 以及 `result` 或 `error`。
- 只执行本机广告过的操作；每条请求-响应调用必须在 `timeout_ms` 内回报——不回报
  平台侧记 `TIMEOUT`。单向操作不回报。
- 形如 `secret://<名称>` 的参数在最后一跳已还原为明文；禁止记录日志或持久化。
- 结果中**绝不允许包含密码**：平台不检查结果内容，脱敏由网关负责。
- 调用只在在线时发生：网关离线立即得到 NOT_CONNECTED，帧绝不排队；迟到/重复的
  结果会被丢弃。

```go
_ = gw.SubscribeOperations(ctx, 1, func(inv device.OperationInvoke) {
    out := runVendorOperation(inv.Operation, inv.Params)
    _ = gw.RespondOperation(ctx, device.OperationResult{
        ID: inv.ID, OK: true, Result: out,
    }, 1)
})
```

## 10. Topic 汇总

网关 → 平台：`v1/gateway/hello`、`heartbeat`、`goodbye`、`linkhealth`、
`connect`、`disconnect`、`manifest`、`telemetry`、`attributes`、
`shadow/report`、`command/response`、`ota/progress`、`probe/response`、
`connectors/status`、`profiles`、`discovery`、`operations/result`。

平台 → 网关：`hello/ack`、`linkhealth/ack`、`command`、`attributes/push`、
`shadow/desired`、`ota/task`、`probe`、`connectors/spec`、
`connectors/delete`、`discovery/result`、`operations/invoke`。

上行 QoS 由网关选择（建议 QoS 1）；下行帧均为 QoS 0、非 retained。

## 11. 接入检查清单

- 网关注册并具备凭据；所有子设备已注册并绑定到该网关。
- 每次（重）连后发送 hello；在 `status: ok` 之前不发布任何网关帧；特性清单与
  实际实现一致。
- CONNECT 前注册 LWT；优雅停机发计划内 goodbye；按 `limits.heartbeat_s`
  发心跳。
- 重 hello 后补发本地看门狗 episode；ack 只订阅一次；收到
  `accepted`/`duplicate`/`rejected` 即停止重传。
- 挂载变化时发 `connect`/`disconnect`；每 5 分钟发全量 manifest，正确处理
  `connectors` 字段的有无语义。
- 遥测批量以 UUID 为键，值只含扁平标量。
- 命令：一个订阅处理全部子设备；每条请求-响应命令都按 `command_id` +
  `device` 回复（失败也要回）；单向命令绝不回复。
- 连接器推送按 `(spec_id, revision)` 去重，并通过状态机回报状态。
- 影子：网关自身影子走 `v1/me/shadow/*`；子设备 reported 批量发往
  `v1/gateway/shadow/report`，只订阅一次 `v1/gateway/shadow/desired` 并按
  `device` 分发；desired 全量替换，切勿按增量合并。
- 在 hello `operations[]` 中广告操作；每条请求-响应调用都在 `timeout_ms` 内按
  `id` 回复 `operations/result`；结果中不含密码。
