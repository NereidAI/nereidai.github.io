# 部署策略

部署策略（Business Policy）是 NereidHorizon 中基于属性和约束的自动服务部署规则。策略适用于不依赖固定模式的灵活部署：由协议机器人将策略与符合条件的节点进行匹配，而不是让节点加入一个固定的服务集合。

## 创建策略

必填项：

- **Policy Name（策略名称）**
- **Label（标签）**
- **Target Service（目标服务）**：要部署的服务 URL。

选填项：

- **Properties（属性）**：描述服务的特征。
- **Constraints（约束）**：匹配规则，例如 `openhorizon.allowPrivileged == true`。
- **Service Org（服务组织）**、**Service Arch（服务架构）**以及服务版本范围。

## 导入策略

将策略 JSON 粘贴到导入器中，JSON 必须包含 `businessPolicy` 包裹层。

## 策略与模式的区别

模式是「固定服务集合」：注册到该模式的每个节点运行同一组服务。策略是「按约束匹配」的部署，更适合动态环境——不同节点根据自身属性决定是否运行某个服务。创建策略后，需在[协议机器人](agbots.md)页面将其关联到 agbot，才能被协商。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | 缺少目标服务，或约束格式错误 |
| 409 | 策略已存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [部署模式](patterns.md)
- [服务](services.md)
- [协议机器人](agbots.md)
- [边缘节点](nodes.md)
