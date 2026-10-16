# 管理策略

管理策略（Management Policy / NMP）用于 NereidHorizon 中的节点升级与生命周期管理，例如 Agent 升级和节点配置下发。管理策略通过约束选择目标节点，其执行结果可以在节点详情的「Mgmt Status」标签页中查看。

## 创建管理策略

必填项：

- **Policy Name（策略名称）**
- **Label（标签）**
- **Type（类型）**：`upgrade`（升级）或 `lifecycle`（生命周期）。

选填项：

- **Constraints（约束）**：匹配目标节点。
- **Properties（属性）**：策略内容。进行 Agent 升级时填写 `agentUpgradePolicy`，例如：

```json
{ "type": "agent", "version": "2.30.0" }
```

## 编辑与导入

- **编辑**：更新策略时通过 PUT 请求替换其配置。
- **导入（Import）**：粘贴管理策略 JSON。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | 类型不支持，或必填字段缺失 |
| 409 | 策略已存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [边缘节点](nodes.md)：「Mgmt Status」标签页展示策略执行状态。
- [Agent 文件版本](agentfileversion.md)：指导 Agent 升级的版本列表。
- [部署策略](policies.md)
