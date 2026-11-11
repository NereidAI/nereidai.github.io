---
title: 路线图
---

# 路线图

NereidAI 七个产品仓库已全部在 GitHub **开源（Apache-2.0）**，并通过合规性、开源规范与
完整性审核。当前代码以滚动**开发（dev）通道**发布：尚无带 tag 的正式版本。本页跟踪成熟度
与通向首个正式版本的路径；它是一份持续演进的计划——阶段按**门（gate）标准**进入与退出，
而非按日历。

!!! note "状态在开放环境中跟踪"
    仓库、issue 与 Discussions 均公开。当前工作可在
    [NereidAI GitHub 组织](https://github.com/NereidAI)查看；本页反映套件级视图，并在各门
    达成时更新。

## 发布通道

| 通道 | 当前能拿到什么 | 稳定性 |
|---|---|---|
| **dev（当前）** | 各仓库默认分支上的滚动源码，CI 构建的开发镜像 | 持续变动；契约仍可能变化；不承诺升级路径 |
| **首个带 tag 的正式版本（计划中）** | 各仓库语义化版本 tag、多架构镜像、SBOM、签名与签名离线包，本站补齐商用与支持文档 | 门控发布；标准达成后公布 |

商用条款、支持 SLA 与企业交付物将在首个正式版本发布时补齐文档。在此之前，请基于 dev 通道
评估与集成，并预期版本之间可能有破坏性变更。

## 成熟度门

每个产品以三种成熟度门之一发布：

| 门 | 含义 | 标准 |
|---|---|---|
| **GA** | 生产就绪 | 气隙安装已验证；API 冻结；负载/老化目标达成；文档完整；签名镜像 + SBOM |
| **Preview** | 可试用，尚不稳定 | 核心流程端到端可用；可安装；契约仍可能变化；文档不完整 |
| **Tech Preview** | 可演示的最小闭环 | 最小的端到端切片；不承诺升级或 API 稳定性 |

开源与成熟度是两件事：仓库公开本身并不意味着产品已 GA。

## 各产品所处位置

| 产品 | 门 | 当前状态 |
|---|---|---|
| Link | GA 轨道 | 单二进制功能完备（另有微服务形态）；网关线协议已实现；仓库内有自己的 GA 计划。 |
| Edge | GA 轨道 | 核心桥接与连接器治理已实现；端到端验收进行中。 |
| Sphere | Preview | 门户、对 Identity 的 OIDC 登录、网关与 SSO 票据中心均已实现并有文档。 |
| Identity | Preview | Keycloak 兼容 realm，声明式 realm/客户端预置；支持代理 IdP。 |
| Forge | Preview | 功能成熟的模型工厂：数据集、标注、CV 与 LLM/VLM 训练、优化、评估、模型库与 KServe 部署。 |
| Horizon | Preview | 管理控制台、BFF 与 partner API；边缘交换集成持续开发中。 |
| Inference | Preview | EdgeX 4.0 设备服务，含通用推理流水线、模型目录、KServe/OpenAI 后端与内置解码器集；部分相机/服务器路径已真机验证。 |

!!! warning "如实说明成熟度"
    Sphere、Identity、Forge、Horizon 与 Inference 处于 **Preview**——核心流程
    端到端可用、服务可安装，但契约仍可能变化。Link 与 Edge 在 GA 轨道上，但在
    发布门通过前不打 GA 标签。

## 通向首个正式版本的路径

每个阶段只有满足其门标准才退出；阶段内允许调整顺序。

1. **Foundation（奠基）** —— 仓库、CI 与脚手架（已完成：七个产品仓库全部公开，含许可证、
   NOTICE 与贡献文件）。
2. **Build（构建）** —— 每个产品的主要用户流程；所有跨产品契约在本阶段结束时定稿。
3. **Integration（集成）** —— 跨产品端到端测试；Link/Edge 线契约冻结；GA 轨道产品的负载与
   故障注入测试。
4. **Release candidate（候选发布）** —— 多架构镜像、SBOM、漏洞扫描、签名、签名离线包、完整
   气隙安装演练、老化测试、文档通读。
5. **Release（发布）** —— 各仓库语义化版本 GitHub Release；本站补齐商用、支持与企业文档以及
   状态徽标/等级。

凡在 Build 结束时未就绪契约、或在 RC 时仍不稳定者，移出首个正式版本，而不顺延阶段。

??? note "跨产品契约（摘要）"
    契约必须在 Build 阶段结束时定稿。

    | 契约 | 参与方 | 状态 |
    |---|---|---|
    | 网关线协议 v1（主题、帧、目录） | Link ↔ Edge | 已实现；RC 前冻结 |
    | SSO / OIDC 联邦 | Sphere ↔ Identity ↔ 各产品 | 已实现（票据模式与直接 OIDC），本站有文档 |
    | 产物交接（模型包 → rollout） | Forge → Horizon → Inference | 已定义：带 `nereid-model.json` 的 tar 包，经 Horizon ESS 运输 |
    | 边缘分发通道 | Horizon → Edge / Inference | 由 Horizon 负责 |

## 下一步

- [社区版与企业版](community-vs-enterprise.md)——哪些开源、哪些商业。
- [支持](support.md)——在哪里跟进进展、如何获得帮助。
- [开源许可](license.md)——Apache-2.0 条款。
- [平台对接](../development/api-integration.md)——如何调用产品 API。
