# NereidEdge 入门

NereidEdge 是一个 EdgeX Foundry 应用服务，负责把现场设备桥接到 Link。它把
EdgeX 事件与读数转换为 Link 网关 MQTT 协议上的网关遥测帧，并把 EdgeX 设备名
映射为 Link 子设备。它运行在现场网关上，与 EdgeX 4.0.2 栈协同运行。

!!! tip "只需 Link 即可独立运行"
    Edge 只需要可达的 Link 消息中间件和网关凭据，运行不依赖 Sphere 或
    Horizon。Horizon 的作用是把 Edge 分发到大量站点并保持更新，并非运行期
    依赖。

## 前提条件

- 网关上已运行 EdgeX Foundry 4.0.2 栈（核心服务、NATS 消息总线与
  device service）。
- 可达的 Link MQTT 消息中间件（`tcp://` 或 `tls://`）。
- 在 Link 控制台创建的**网关凭据**：Credential ID、凭据密钥以及网关的
  Edge ID——平台侧见[网关设备接入](../link/integrate-gateway.md)，概念见
  [网关](../link/glossary/gateway.md)。
- 每台现场设备都已在 Link 中注册为绑定到该网关的子设备，因此其
  子设备 UUID 已知。

## 1. 准备平台侧

在 Link 控制台中创建网关设备、添加网关凭据，并把每台现场设备注册为绑定到
该网关的子设备。记下每个子设备 UUID；Edge 会把 EdgeX 设备名映射到这些
UUID。建议先阅读[网关设备接入](../link/integrate-gateway.md)中的握手过程
（hello、心跳与清单），再看 Edge 日志会容易得多。

## 2. 配置设备映射

编辑 EdgeX 自定义配置文件 `res/configuration.yaml` 中 `NereidEdge` 段：

```yaml
NereidEdge:
  BrokerURL: "tcp://<link-mqtt-host>:1883"
  CredentialID: "<your-cred-id>"
  CredentialSecret: "<your-cred-secret>"
  EdgeID: "<edge-instance-id>"
  DeviceMap: "edgex-device-1:<link-subdevice-uuid-1>,edgex-device-2:<link-subdevice-uuid-2>"
```

`DeviceMap` 是一组以逗号分隔的 `edgex设备名:link子设备uuid` 对应关系。生产
环境请使用 `tls://` 的中间件地址，并把凭据密钥放在密钥管理系统中，不要提交
到文件里。

## 3. 构建与运行

用 `make build-local` 构建二进制，或用 `make docker` 构建容器镜像，然后以
EdgeX 应用服务形式运行 Edge——可以裸机、Docker，或加入 EdgeX 网络的
Docker Compose。启动时 Edge 先完成 Link hello/能力协商，随后开始转发遥测。
部署模式、网络与 compose 细节见产品仓库的 `docs/deployment.md`。

## 4. 验证桥接

1. 检查 Edge 服务健康端点：访问 `59750` 端口的 `GET /api/v4/ping` 应返回
   `pong`。
2. 在 Link 控制台中，网关及其映射的子设备显示为**在线**。Edge 在子设备首次
   遥测时挂接它，并每五分钟发送一次全量设备清单。
3. 打开一个子设备，确认读数在更新——EdgeX 读数现在以映射到的 UUID 为键，
   作为 Link 遥测出现。

如果没有数据到达，请核对 DeviceMap 对应关系、EdgeX 事件是否经消息总线到达
应用服务，以及网关凭据与 Edge ID 是否通过协商。

## 下一步

- [网关设备接入](../link/integrate-gateway.md)——Edge 使用的北向契约。
- [NereidEdge 产品页](../../products/nereidedge.md)与
  [边缘分发](../../deployment/edge-delivery.md)。
- 配置、排障与协议参考位于 NereidEdge 仓库
  （[NereidAI](https://github.com/NereidAI)）。
