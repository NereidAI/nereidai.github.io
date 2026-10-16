---
title: 贡献指南
---

# 贡献指南

NereidAI 以 **Apache License 2.0** 开源，开发分散在
[NereidAI GitHub 组织](https://github.com/NereidAI)下的一组独立仓库中。本页从
较高层面说明如何参与；**权威细节以各仓库为准**。

!!! info "开发者文档"
    贡献规则、确切命令与评审要求均由各仓库自行维护。请从
    [NereidAI 组织](https://github.com/NereidAI) 进入，先阅读该仓库自己的贡献指南
    与作业规则。

## 在哪里参与

每个产品都是独立仓库，拥有自己的 issue 跟踪。请使用拥有你所改动领域的那个
产品仓库——在错误的仓库里修改，并不构成去别处修改的理由。

| 仓库（GitHub 组织内） | 负责 |
|---|---|
| `Sphere` | 门户、统一 API 网关、跨产品事件粘合。 |
| `Identity` | 套件 SSO / 身份联邦。 |
| `Link` | IoT 管道：设备接入、规则、告警、看板。 |
| `Forge` | 模型工厂：数据集、训练、导出、模型仓库。 |
| `Horizon` | 边缘分发与 rollout。 |
| `Edge` | 现场网关上的南向边缘接入。 |
| `Fleet` | 机器人集群管理。 |
| `Mobile` | 移动 App 与微信小程序。 |

讨论通过 GitHub issues 与 Discussions 进行——这就是社区支持渠道。企业相关问题
见[社区与支持](../community/support.md)。

## 贡献流程

1. **选定负责的仓库**，阅读其 `README`、贡献指南与作业规则。
2. 较大的改动前先**提交或找到对应 issue**，在公开场合确认范围。
3. **建分支、实现并验证**，使用*该仓库自己的* format / lint / type-check /
   test / build 命令——切勿编造项目并不存在的脚本。
4. **发起 pull request**，附上清晰说明；保持每次改动聚焦、易于评审。

!!! note "一次改动，一个仓库"
    在任一仓库的工作中，兄弟仓库都视为只读。跨仓库修复会作为协同改动交给负责的
    仓库，而不是顺手在别处改掉。

## 提交与署名规范

- **Conventional Commits。** 用类型前缀书写提交信息，如 `feat:`、`fix:`、
  `chore:` 或 `docs:`。
- **DCO 署名。** 每个提交都带 `Signed-off-by` 行；使用 `git commit -s`。

    ```bash
    git commit -s
    ```

- **一个已验证的里程碑一个提交。** 只暂存预期文件，并在某个阶段验证通过后再
  提交，而不是攒成一大坨。

## 许可证头

每个手写源文件（Go、Python、TS/TSX、SQL、项目自撰的 YAML、proto、shell）都必须
以项目头开头，并使用该语言的注释语法：

```text
// Copyright (C) 2026 YIQISOFT
// SPDX-License-Identifier: Apache-2.0
```

!!! warning "Vendored 代码不同"
    Vendored / 第三方子树遵循**上游**约定——上游许可证头、格式与工作流。不要在那里
    添加或还原头信息。头规则只适用于手写的 NereidAI 代码。

## 完成前先验证

绝不以“已成功编辑”收尾——要以“已验证”收尾。运行负责仓库的格式化、lint、
类型检查、测试与构建，并修复每一处失败。注意前端打包器构建本身不做类型检查，
需另外运行项目的类型检查器。清理你自己创建的测试进程与临时文件。确切命令见
该仓库。

## 版本与契约

- 仓库级的 `VERSION` 文件是**发布的事实来源**，也是派生镜像标签的来源；未经明确
  要求不要修改。
- 当公共 API、请求/响应结构、WebSocket 帧或线契约发生变化时，在同一改动内更新
  规范与受影响的文档。

## 下一步

- [快速开始](getting-started.md) —— 在套件中定位方向。
- [代码规范](conventions.md) —— 共享的编码规范。
- [跨产品契约](../architecture/contracts.md) —— 套件约定的内容。
