# 节点注册

边缘节点（运行 `anax` agent 的机器）通过 `hzn` 命令行注册到 Exchange，随后拉取所属模式或策略、协商协议并部署服务。本指南按阶段介绍这一流程，并说明在 NereidHorizon 中如何验证每个步骤。

## 阶段一：节点准备

1. 安装 `anax` agent，例如通过 `apt install horizon`，或在 Docker 中运行 `anax`。
2. 确认节点在网络上可以访问 Exchange URL。
3. 在[用户](users.md)页面为节点账号生成 API 密钥（仅显示一次）。

## 阶段二：注册节点

在节点上执行：

```bash
hzn exchange user create -u <org>/<user>:<apikey> -o <exchange-url>
```

随后使用模式或策略进行注册：

```bash
hzn register -o <exchange-url> -u <org>/<user>:<apikey> \
  --name <node-name> \
  -p <org>/<pattern-name>    # 或 --policy <policy-file>
```

模式部署使用 `-p <org>/<pattern-name>`；基于策略的部署使用 `--policy <policy-file>`。

## 阶段三：协商与部署

1. 节点向协议机器人发送**提案（Proposal）**。
2. 协议机器人匹配到已关联的模式或策略后返回**协议（Agreement）**。
3. 节点拉取服务镜像并启动容器。
4. 节点持续上报**心跳（Heartbeat）**。

请务必在[协议机器人](agbots.md)页面将模式或策略关联到 agbot，否则协商无法成功。

## 阶段四：在界面中验证

- 节点出现在[边缘节点](nodes.md)列表中，状态为「在线（Online）」。
- 节点详情的「Services」和「Agreements」标签页显示已部署的服务与协议。
- [审计日志](auditlog.md)会记录 `node_register` 事件。

## 常见错误

| 现象 | 可能原因与处理 |
|---|---|
| 节点不出现 | 检查 API 密钥、到 Exchange 的网络连通性以及节点时间是否同步 |
| 协议超时（reason 201） | 通常是节点无法持久化状态，例如 `anax.db` 权限问题 |
| 修改模式后 | 重新注册：`hzn unregister -f && hzn register ...` |

## 另请参见

- [边缘节点](nodes.md)
- [部署模式](patterns.md)
- [部署策略](policies.md)
- [协议机器人](agbots.md)
- [用户](users.md)
