# 部署模式

部署模式（Pattern）在 NereidHorizon 中定义一组服务的部署拓扑与版本策略。注册到某个模式的节点会自动拉起该模式包含的服务。当一类节点需要运行同一套固定服务集合时使用模式；需要按属性匹配部署时请改用[部署策略](policies.md)。

## 创建模式

必填项：

- **Pattern Name（模式名称）**：例如 `my-pattern`。
- **Label（标签）**：显示名称。
- **服务选择**：从复选框列表中至少选择一个服务。

描述为选填项。对每个选中的服务，Horizon 会自动生成 `serviceOrgid`、`serviceArch`、`serviceVersions`（默认版本）和 `nodeHealth`（默认 `ping_interval=60`）。

## 编辑模式

编辑模式会替换其中所有服务引用。可以直接编辑 JSON，也可以通过界面复选框选择服务。

## 导入与查看

- **导入（Import）**：粘贴模式 JSON。
- **详情抽屉**：包含两个标签页，**Info** 展示模式 JSON，**Node Health** 展示关联节点的健康状态。

## 将模式关联到协议机器人

!!! important "创建模式后的必要操作"
    模式只有在关联到协议机器人之后才能到达节点。请在[协议机器人](agbots.md)页面将新模式绑定到对应的 agbot，节点才能协商到该模式。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | 未选择服务（至少需要一个） |
| 409 | 模式已存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [服务](services.md)
- [部署策略](policies.md)
- [协议机器人](agbots.md)
- [节点注册](node_registration.md)
