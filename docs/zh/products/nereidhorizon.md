---
title: NereidHorizon
---

# NereidHorizon

Horizon 是 Open Horizon 管理中枢（Management Hub）的运维控制台：套件在这里
定义、签名并 rollout 那些把 Edge（以及 Forge 产出的应用与模型）投递到
大量远程边缘节点的边缘服务、模式（pattern）与策略。

## 它解决什么问题

- 直接对着管理中枢的原始 API 手工维护 Open Horizon 边缘资源（节点、服务、模式、
  策略、AgBot、HA 组）既慢又易错；Horizon 为运维人员提供一个图形化控制台。
- Open Horizon 要求每个服务部署配置都带签名；Horizon 自动完成签名，运维人员
  无需逐个服务处理签名材料。
- 第三方与下级组织需要访问边缘资源，又不能共享中枢级凭据；Horizon 改以绑定
  组织的只读 API Key 交付权限。
- 受监管环境需要针对中枢的可追溯操作记录；Horizon 保留只追加的审计轨迹。
- 部署常发生在无法访问互联网的气隙网络中；Horizon 支持离线安装交付。

## 核心能力

**中枢资源管理**

- 在一个界面中管理边缘节点、服务定义、部署模式、部署策略、管理策略、协议机器人
  （AgBot）、组织与中枢用户。
- 高可用（HA）节点组：配置、管理与监控分组、成员关系与网络配置。
- 跨组织浏览公共的服务与模式。
- 从 JSON 导入服务、模式与策略，并交互式处理其中的模板变量。

**部署与 rollout**

- 在创建与更新时自动为服务部署配置签名。
- 从服务、模式一路跟踪到实际运行它们的节点，并可就地管理节点侧的环境变量。

**访问与身份**

- 双层认证：本地控制台账号 + 一套供所有操作共享的系统级中枢连接。
- 基于角色的访问：一个跨组织的管理员角色，以及一个绑定组织的合作方角色。
- 经套件身份中心（Sphere / Identity）或直接对接 OIDC 提供方的单点登录。
- 面向第三方集成、绑定组织的只读 API Key。

**运维与安全**

- 服务端会话，凭据加密落库。
- 只追加的审计日志，记录每一次控制台与 API Key 操作，含实际访问到的中枢端点。
- 加固的 TLS 与安全响应头。
- 基于预构建镜像的离线、气隙安装。

## 在套件中的位置

Horizon 处于闭环中的“分发”一环。Forge 产出带版本的应用与模型；
Horizon 把它们连同 Edge 本身发布为 Open Horizon 的服务定义、模式与策略，
由中枢的 agent 将这些投递到现场节点。Edge 随后在这些节点上运行，并把数据回传给
Link。

- **Forge → Horizon**：带版本的产物转化为可分发的服务。
- **Horizon → Edge**：策略化 rollout 边缘运行时及其承载的工作负载。参见
  [边缘分发](../deployment/edge-delivery.md)。
- **Sphere / Identity**：在完整套件部署中，运维人员经 Sphere 一次
  登录，并从统一门户进入 Horizon。参见 [SSO 与 OIDC](../security/sso-oidc.md)。
- **独立部署**：Horizon 也可单独作为中枢控制台运行。

!!! info "开发者文档"
    本产品的权威、详细开发者文档位于其自有仓库——见
    [NereidAI](https://github.com/NereidAI)。

## 关键事实

| 方面 | 说明 |
|---|---|
| 产品定位 | Open Horizon 管理中枢的 Web 运维控制台 |
| 在套件中的位置 | 闭环中的“分发与部署”一环 |
| 访问模型 | 单点登录；跨组织管理员与绑定组织的合作方角色；只读合作方 API Key |
| 部署形态 | 可独立部署，也可作为套件一部分；支持气隙网络安装 |
| 技术栈 | React + Vite 前端，Express / Node.js 的 BFF，PostgreSQL |
| 许可证 | Apache-2.0 |

## 资源

- GitHub：[NereidAI](https://github.com/NereidAI)
- [套件总览](index.md)
- [架构总览](../architecture/overview.md)
- [边缘分发](../deployment/edge-delivery.md)
- [气隙安装](../deployment/air-gapped.md)
- [SSO 与 OIDC](../security/sso-oidc.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
