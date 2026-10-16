---
title: 路线图
---

# 路线图

本页汇总 **v0.0.1 套件发布计划**。它是一份持续演进的计划：**日期并不固定**——阶段
按**门（gate）标准**进入与退出，而非按日历。此处反映的计划最后更新于 2026-10-11。

!!! note "状态在开放环境中跟踪"
    本页描述截至 2026-10-11 的计划。当前状态在
    [NereidAI GitHub 组织](https://github.com/NereidAI) 与 Discussions 中跟踪。

## 一段话理解 v0.0.1

v0.0.1 是 NereidAI 套件下发布的第一个可安装的边缘到云端闭环快照。每个仓库保留自己的
`VERSION`（GA 前为 `v0.0.1`；构建标识为 `v0.0.1+git<sha>.<date>`）。本页跟踪套件级
的整体视图。

## 成熟度门

每个产品以三种成熟度门之一发布：

| 门 | 含义 | 标准 |
|---|---|---|
| **GA** | 生产就绪 | 气隙安装已验证；API 冻结；负载/老化目标达成；文档完整；签名镜像 + SBOM |
| **Preview** | 可试用，尚不稳定 | 核心流程端到端可用；可安装；契约仍可能变化；文档不完整 |
| **Tech Preview** | 可演示的最小闭环 | 最小的端到端切片；不承诺升级或 API 稳定性 |

## 各产品所处位置

截至 2026-10-11 的基线状态：

| 产品 | 门 | 基线状态 |
|---|---|---|
| Link | GA | 单二进制功能完备；有自己的 GA 计划（`docs/roadmap/ga.md`）。 |
| Edge | GA | 核心桥接与连接器治理完成；端到端验收待办。 |
| Forge | Preview | 功能成熟（数据集 / 训练 / 优化 / 导出 / 模型仓库）；尚无 GA 计划。 |
| Horizon | Preview | Web UI 与 BFF 开发中；MVP 范围待冻结。 |
| Sphere | Tech Preview | 空仓库；从零构建。 |
| Mobile | Tech Preview | 仓库尚未创建；从零构建。 |
| Fleet | Tech Preview | 仅有研究文档；无提交。 |

!!! warning "如实说明：部分产品处于 Tech Preview"
    Sphere、Mobile 与 Fleet 处于 **Tech Preview**——可演示的最小
    闭环，**不承诺升级或 API 稳定性**。Forge 与 Horizon 处于
    **Preview**，契约仍可能变化。只有 Link 与 Edge 处于 **GA**。

## 五个阶段

每个阶段只有满足其门标准才退出；阶段内允许调整顺序。

1. **Foundation（奠基）** —— 新仓库、CI 与脚手架。Link 与 Edge 关闭其
   P0/P1 事项。Forge 与 Horizon 冻结 v0.0.1 范围。移动端 Taro 概念验证。
   Fleet MVP 从研究中收敛。
2. **Build（构建）** —— 每个产品的主要用户流程。所有跨产品契约在本阶段结束时定稿。
3. **Integration（集成）** —— 跨产品端到端测试；Link/Edge 线契约冻结；
   GA 产品的负载与故障注入测试。
4. **Release candidate（候选发布）** —— 多架构镜像、SBOM、漏洞扫描、签名、签名离线包、
   完整气隙安装演练、老化测试、文档通读。
5. **Release（发布）** —— 各仓库 GitHub Release；套件指南上线，附链接与状态徽标/等级。

凡在 Build 结束时未就绪契约、或在 RC 时仍不稳定者，移出 v0.0.1，而不顺延阶段。

??? note "跨产品契约（摘要）"
    契约必须在 Build 阶段结束时定稿。

    | 契约 | 参与方 | 状态 |
    |---|---|---|
    | 网关线协议 v1（主题、帧、目录） | Link ↔ Edge | 已实现；RC 前冻结 |
    | SSO / OIDC 联邦 | Sphere ↔ Keycloak ↔ 各产品 | 未开始；Sphere 先直接对接 Keycloak |
    | 只读移动端 API 子集（认证、设备、遥测、告警） | Mobile ↔ Link | 未定义 |
    | 产物交接（模型/应用包 → rollout） | Forge → Horizon | 未定义 |
    | 边缘分发通道 | Horizon → Edge | 由 Horizon 负责 |

## 社区版时间线

完整的边缘到云端社区版将于 **2026 年底前开源**；各模块逐步发布。开源的时机与各仓库
顺序在计划中仍属**待定事项**，将在候选发布前确认。

## 下一步

- [社区版与企业版](community-vs-enterprise.md) —— 哪些开源、哪些商业。
- [支持](support.md) —— 在哪里跟进进展、如何获得帮助。
- [开源许可](license.md) —— Apache-2.0 条款。
