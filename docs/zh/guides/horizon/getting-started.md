# NereidHorizon 快速开始

NereidHorizon（简称 Horizon）是面向 Open Horizon 管理中心的边缘分发控制台：通过图形化界面定义服务，并以模式或策略将服务发布到大规模边缘节点。产品层面的介绍参见 [NereidHorizon 产品页](../../products/nereidhorizon.md)。

本指南带领首次使用的运维人员走通核心流程：登录 → 注册并接入边缘节点 → 定义或导入服务 → 通过模式或策略部署 → 查看协议与发布状态。

## 1. 登录并查看仪表盘

1. 使用运维账号登录 Horizon 控制台。
2. 在[仪表盘](dashboard.md)上确认 Exchange 版本、当前组织和在线节点数。
3. 通过快速操作进入后续步骤所需的模块。

## 2. 注册并接入边缘节点

1. 准备一台运行 `anax` agent 的机器，确保它可以访问 Exchange。
2. 在[用户](users.md)页面创建节点账号并为其生成 API 密钥（仅显示一次）。
3. 在节点上通过 `hzn register` 按模式或策略完成注册。
4. 在[边缘节点](nodes.md)页面确认该节点显示为在线。

完整命令顺序与验证步骤见[节点注册](node_registration.md)。

## 3. 定义或导入服务

服务定义描述容器镜像及其部署配置。

- 在[服务](services.md)页面创建：名称、标签、版本、架构和镜像为必填项。
- 或通过粘贴 JSON、上传 `.json` 文件导入已有定义。

Horizon 会自动对 deployment 签名，无需手动操作。

## 4. 通过模式或策略部署

两种部署模型二选一：

- **模式（Pattern）**：面向一类节点的固定服务集合。在[部署模式](patterns.md)页面创建（至少选择一个服务），然后将节点注册到该模式。
- **策略（Policy）**：面向动态环境、按约束匹配部署。在[部署策略](policies.md)页面创建策略，指定目标服务并匹配节点属性。

无论哪种方式，都必须将模式或策略关联到[协议机器人](agbots.md)；在 agbot 关联之前，节点无法协商到部署。

## 5. 查看协议与发布状态

1. 打开[协议机器人](agbots.md)，在「Agreements」标签页查看新达成的协议。
2. 在[边缘节点](nodes.md)打开节点抽屉，查看「Agreements」和「Services」标签页。
3. 如果发布停滞，查看「Errors」标签页，并在[审计日志](auditlog.md)中确认结果——日志会记录 `node_register` 事件以及每一次对管理中心的调用。

## 后续阅读

- [边缘节点](nodes.md)与[节点注册](node_registration.md)
- [服务](services.md)、[部署模式](patterns.md)、[部署策略](policies.md)
- [协议机器人](agbots.md)
- Agent 升级与生命周期操作：[管理策略](mgmtpolicies.md)
- 多租户配置：[组织](organizations.md)、[BFF 用户](bffUsers.md)、[API 密钥](apikeys.md)
