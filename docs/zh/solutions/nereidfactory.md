---
title: NereidFactory
---

# NereidFactory

**智能制造：工厂运营与智能生产。**

NereidFactory 是构建在开放 NereidAI 平台**之上**的**商业行业解决方案**。它面向
制造现场——AI 需要贴近产线运行，而相关数据不应离开工厂。

!!! note "商业解决方案"
    NereidFactory 按**独立的商业协议**授权、交付与支持，不包含在 Apache-2.0
    社区版中。请见[社区版与企业版](../community/community-vs-enterprise.md)。

## 它面向的场景

制造业与私有化、边缘优先的 AIoT 平台天然契合。概括而言，该行业最棘手的压力，
正是开放平台已经为之构建的能力：

- **数据留在自有场地** —— 生产、质量与工艺数据受合规与内部制度约束，许多公有云
  方案因此不可用。
- **产线上的实时决策** —— 结果需要在作业发生处产生，而不是回传到远端数据中心。
- **异构现场硬件** —— 产线侧设备横跨众多芯片厂商（含国产路线），模型必须针对每个
  目标优化与导出，而不是逐个手调。
- **从试点到生产** —— 把有前景的演示变成日常运行，需要可复制的流水线与沉淀在组织
  内部的资产。

## 它建立在什么之上

NereidFactory 依托开放平台，而非另起炉灶。下列构件与整套件文档所述的一致：

| 平台构件 | 对工厂方案的作用 |
|---|---|
| [Forge](../products/nereidforge.md) | 模型工厂——数据集、训练、量化，以及面向产线侧目标的硬件适配导出。 |
| [Horizon](../products/nereidhorizon.md) | 离线边缘分发——把模型与应用投递到大量产线侧节点。 |
| [Edge](../products/nereidedge.md) | 网关上接入——零触碰上线与 mTLS 连接现场设备。 |
| [Link](../products/nereidlink.md) | 数据管道——设备接入、规则引擎、告警与看板。 |
| [Sphere](../products/nereidsphere.md) / [Identity](../products/nereididentity.md) | 门户、API 网关，以及整套件统一 SSO / RBAC。 |

## 这里能说——与不能说的

由于 NereidFactory 按商业方式交付，其具体功能集与范围**按项目逐一确定**。因此本页
仅在高层描述价值主张，不公布固定功能清单、价格或服务水平。

!!! info "细节按项目确定"
    适用于您环境的具体能力、集成面、交付计划与支持条款，请
    [联系我们](../community/support.md)。

## 典型行业

同样的「私有化、边缘优先」模式适用于重工制造、离散装配、流程工业与工厂运营——
凡是以产线侧推理与本地数据为前提（而非可选项）之处皆然。某个客户具体适用哪些部分，
按项目逐一确认。

## 下一步

- [NereidSentinel](nereidsentinel.md) —— 视频与图像分析
- [NereidMedical](nereidmedical.md) —— 医疗洞察
- [全部商业解决方案](index.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
