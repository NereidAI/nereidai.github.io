# 二进制媒体与 S3 存储

遥测并不只限于数值：设备可以把**二进制媒体——相机图片、巡检照片、扫描文档**——与测量值
一起上报。二进制字节绝不进入数据库或消息总线。NereidLink 会把它们流式写入
**S3 兼容对象存储**（MinIO、SeaweedFS、AWS S3……），遥测点位中只保留一个轻量的
`blob://` 引用。

**MQTT 与 HTTP 两种方式都支持**，直连设备与网关下的子设备均适用。

!!! info "开发者文档"
    本页介绍设备侧契约与运维侧配置。存储实现位于 NereidLink 仓库的
    `internal/blob/` 与 `internal/ingesthttp/media.go`——见
    [NereidAI](https://github.com/NereidAI)。

## 工作原理

```
设备 / 网关                              NereidLink                         S3 兼容存储
      |                                     |                                       |
      |  遥测帧（标量 + 媒体）               |                                       |
      |-----------------------------------> |                                       |
      |                                     |  校验大小 / 内容类型                   |
      |                                     |  流式写入字节（PUT object）           |
      |                                     |-------------------------------------->|
      |                                     |            对象 key                    |
      |                                     |<--------------------------------------|
      |                                     |  点位 v_string = blob://<key>         |
      |             202 accepted            |  （PostgreSQL / 时序只存引用）        |
      |<----------------------------------- |                                       |
```

对象 key 始终由平台生成，并按归属方隔离：

```
media/<租户-id>/<设备-id>/<uuid>
```

时序行与每个 Envelope 只携带字符串
`blob://media/<tenant>/<device>/<uuid>`，绝不携带字节本身。读侧消费方识别
`blob://` 协议头，按需将其换成短时有效的签名下载 URL。

## 方式一：把媒体包裹进遥测帧（MQTT 或 HTTP）

在"扁平帧"中，唯一被接受的结构化字段形态是**二进制媒体标记（media marker）**。
文件负载采用 base64 编码（标准或 URL-safe 字母表，有无填充均可）：

```json
{
  "temperature": 21.5,
  "online": true,
  "snapshot": {
    "blob": true,
    "content_type": "image/jpeg",
    "filename": "inspection-01.jpg",
    "data": "/9j/4AAQSkZJRgABAQ..."
  }
}
```

标量测量与媒体字段可以自由混在同一帧里。每个媒体字段变成一个字符串型点位
（`blob://…`）；其他字段照常处理。

### marker 字段规范

这是遥测帧中**唯一**被接受的结构化对象——`null`、数组及其他任何嵌套对象都会被拒绝。
其线格式是稳定、面向设备契约的版本化规范：

| 字段 | 必填 | 规范 |
|---|---|---|
| `blob` | 是 | 必须为布尔值 `true`。`false` 或其他值都会拒绝该字段，避免无关对象被误判为媒体。 |
| `data` | 是 | 文件字节的 **base64 编码**——标准或 URL-safe 字母表、有无填充均可。**不接受**明文：`"HELLO WORLD."` 必须写成 `"SEVMTE8gV09STGQu"`；空数据被拒绝。 |
| `content_type` | 否 | 字节的 MIME 类型。省略或传 `""` 时平台从内容嗅探类型（平台不猜测*单位*，但会存储/检测媒体类型）。 |
| `filename` | 否 | 原始文件名，仅用于展示，不影响存储对象键。 |

同一负载可接受的编码形式：`SEVMTE8gV09STGQu`、`SEVMTE8gV09STGQ`、
`SEVMTE8gV09STGQ_`（URL-safe）。

!!! warning "两条硬规则"
    1. `data` **只能是 base64**——绝不能放明文或 URL。要引用外部文件，请上传字节；
       对象 key 由平台拥有与生成。
    2. 字节**绝不内联**进时序行或 Envelope。未配置 blob 后端时，marker 会被直接拒绝，
       而不是退化为内联存储。

### 走 MQTT

把该帧发布到设备遥测主题——与标量遥测完全相同的路径：

```
PUBLISH v1/me/telemetry   （QoS 0 或 1）
```

网关以同样的方式中继子设备媒体：放在批量帧 `v1/gateway/telemetry` 中逐设备的
values 映射里，与该子设备的标量并列。

使用 Go 设备 SDK 时，`Frame.Set` 只接受标量；请用普通 map 构造 marker，再通过
`PublishRaw` 发布：

```go
marker := map[string]any{
    "blob": true, "content_type": "image/jpeg",
    "filename": "inspection-01.jpg", "data": base64Img,
}
frame, _ := json.Marshal(map[string]any{
    "temperature": 21.5,
    "snapshot":    marker,
})
_ = client.PublishRaw(ctx, device.TopicTelemetry, frame, 1)
```

!!! tip "MQTT 报文大小"
    base64 会使体积膨胀约三分之一。请让 MQTT 帧同时小于 broker 的最大报文限制与平台的
    单对象上限（默认 10 MiB）。大文件建议使用下面的 HTTP 原始上传，直接流式传输字节、
    无需 base64。

### 走 HTTP

同一份 JSON 文档可携带设备凭据提交到 `POST /v1/me/telemetry`。

## 方式二：HTTP 原始二进制上传

对于较大的文件，或为避免 base64 开销，可直接流式上传原始字节：

```http
POST /v1/me/blob?key=snapshot HTTP/1.1
Authorization: <设备凭据>
Content-Type: image/jpeg

<binary body>
```

请求体被直接流式写入对象存储（不会整体缓冲到内存），随后平台发布一个引用该对象的遥测
点位。`key` 查询参数为测量键名（默认 `blob`；仅允许字母、数字、`_`、`.`、`-`）；
**对象 key 由服务端生成**。

`202 Accepted`：

```json
{
  "published": 1,
  "key": "media/tenant-a/dev-1/8f3c2d0e-...",
  "uri": "blob://media/tenant-a/dev-1/8f3c2d0e-...",
  "size": 48213
}
```

如果对象已存储但遥测点位发布失败，对象会被一并删除——不会产生孤儿文件。

## 接受的文件类型与大小

| 策略 | 默认值 | 配置项 |
|---|---|---|
| 单个媒体对象上限 | 10 MiB | `blob.media_max_bytes` |
| 接受的内容类型 | `image/*` | `blob.media_allowed_types` |
| 下载 URL 有效期 | 15 分钟 | `blob.presign_ttl` |

```yaml
blob:
  media_max_bytes: 20971520          # 20 MiB
  media_allowed_types:
    - image/                         # 所有图片
    - application/pdf                # PDF 文档
    - application/msword
    - application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

白名单条目以 `/` 结尾时按类型前缀匹配（`image/`），其余按精确值匹配（如
`application/pdf`）。要接收**文档**，需如上扩展平台配置。`Content-Type` 为空时也会被
接受，读取时再做嗅探，而不是在上传时猜测类型。固件包共用同一对象存储，但使用独立且大得
多的上传上限。

### 存储后端

- **S3 兼容**（生产默认）：MinIO、SeaweedFS、AWS S3——标准 SigV4 path-style 访问，
  单一 region 与 bucket。上传走集群内端点；签名下载 URL 则嵌入外部可达的
  `public_endpoint`。
- **本地文件系统**：面向没有对象服务的小型或气隙部署；平台自行提供文件服务（含 HTTP
  Range），并签发 HMAC 下载链接。

未配置任何 blob 后端时，媒体端点返回 `503 BLOB_UNAVAILABLE`，媒体标记字段会被拒绝。

### 错误码

| 响应 | 触发条件 |
|---|---|
| `413 BLOB_TOO_LARGE` | 超过 `media_max_bytes`（HTTP 上传时传输途中即被截断）。 |
| `415 BLOB_TYPE_REJECTED` | `Content-Type` 不在 `media_allowed_types` 白名单（HTTP 在读取 body 前就拒绝）。 |
| `503 BLOB_UNAVAILABLE` | 未配置 blob 后端。 |
| `502 BLOB_STORE_FAILED` / `BLOB_PUBLISH_FAILED` | 对象存储或遥测发布失败；发布失败时已存对象会被删除。 |

## 读回媒体

- **归属设备自身**通过 `GET /v1/me/blob?key=<完整对象键>` 下载自己的对象（支持
  HTTP Range、ETag 与条件请求）。只服务 key 中编码为当前已认证设备的对象——设备无法靠
  猜测 key 读取他者对象。
- **控制台与 API 用户**通过租户 REST 端点把 `blob://` 值换成短时 URL：

  ```
  GET /v1/tenants/{tenantId}/blob/sign?key=media/<tenant>/<device>/<uuid>
  ```

  返回短时预签名 URL（`url`、`size`、`content_type`）——可以是 S3 预签名 URL 或
  HMAC 签名的 `/v1/blobs/get` 链接，有效期为配置的 `presign_ttl`（默认 15 分钟）。
  key 必须属于路径中的租户，且调用方需具备设备读取权限——其他租户的合法 key 会被拒绝，
  引用无法被利用为跨租户访问。

  控制台按类型渲染换回的媒体：图片显示缩略图、视频用播放器、文本/JSON/XML 用文本查看器
  （内联显示前 256 KiB），其余类型则作为下载。

## 相关链接

- [直连设备接入](integrate-direct-device.md)、[网关接入](integrate-gateway.md)
- [遥测术语](glossary/telemetry.md)、[连接器术语](glossary/connector.md)
- [设备 SDK（Go）](device-sdk.md)——MQTT/HTTP 客户端与帧
- 平台 REST 与设备端点的完整契约见内嵌 OpenAPI 文档 `/api/docs`。
