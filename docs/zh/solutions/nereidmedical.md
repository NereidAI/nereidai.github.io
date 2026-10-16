---
title: NereidMedical
---

# NereidMedical

**Empower Healing with Intelligent Insights.**

NereidMedical 是构建在开放 NereidAI 平台**之上**、面向**医疗洞察**的
**商业行业解决方案**。

!!! note "商业解决方案"
    NereidMedical 按**独立的商业协议**授权、交付与支持，不包含在 Apache-2.0
    社区版中。请见[社区版与企业版](../community/community-vs-enterprise.md)。

!!! warning "非临床或监管声明"
    本页为高层商业概览，不构成医疗建议，也**不作任何监管、认证或临床性能声明**。
    适用要求与范围按项目逐一约定。

## 思路

医疗与生命科学环境集中体现了塑造整个平台的那些压力：数据高度敏感、强烈期望其留在
组织内部、以及需要及时而非在云端批量处理的洞察。NereidMedical 把这一点当作平台问题
来处理——在边缘采集数据，在私有化模型工厂中构建与优化模型，离线分发，并在数据产生
处附近推理，且不强制依赖云端。

## 它建立在什么之上

医疗洞察类解决方案复用与整套件相同的平台构件：

| 平台构件 | 对医疗洞察方案的作用 |
|---|---|
| [Edge](../products/nereidedge.md) | 本地数据采集，具备零触碰上线与 mTLS。 |
| [Forge](../products/nereidforge.md) | 模型工厂——数据集、训练、优化与硬件适配导出。 |
| [Horizon](../products/nereidhorizon.md) | 把模型与应用离线分发到远程节点。 |
| [Link](../products/nereidlink.md) | 设备接入、统一消息、规则引擎、告警与看板。 |
| [Sphere](../products/nereidsphere.md) / [Identity](../products/nereididentity.md) | 门户、API 网关，以及整套件统一 SSO / RBAC。 |

## 这里能说——与不能说的

由于 NereidMedical 按商业方式交付，其具体功能集与范围**按项目逐一确定**。本页仅在
高层描述价值主张，不公布固定功能清单、价格或服务水平。

!!! info "细节按项目确定"
    适用于您环境的具体能力、集成面、交付计划与支持条款，请
    [联系我们](../community/support.md)。

## 下一步

- [NereidFactory](nereidfactory.md) —— 智能制造
- [NereidSentinel](nereidsentinel.md) —— 视频与图像分析
- [全部商业解决方案](index.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
