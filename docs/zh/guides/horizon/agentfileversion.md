# Agent 文件版本

Agent 文件版本模块用于管理 NereidHorizon 中 Agent 的软件版本、配置版本和证书版本列表。这些列表指导边缘节点进行 Agent 升级，通常与升级类[管理策略](mgmtpolicies.md)配合使用。

## 编辑版本列表

每个列表每行填写一个版本号，例如：

```text
2.30.0
```

以下三个列表分别维护：

- **Software Versions（软件版本）**：Agent 软件版本。
- **Config Versions（配置版本）**：Agent 配置版本。
- **Cert Versions（证书版本）**：Agent 证书版本。

## Exchange 不支持该功能时

如果当前连接的 Exchange 不支持此功能，页面将显示空白状态。Horizon 将后端返回的 `400` 视为正常降级，因此 Agent 文件版本能力不可用不会影响其他任何功能。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | 当前 Exchange 版本不支持 AgentFileVersion（正常降级，不影响其他功能） |
| 502 | Exchange 不可达 |

## 另请参见

- [管理策略](mgmtpolicies.md)
- [边缘节点](nodes.md)
