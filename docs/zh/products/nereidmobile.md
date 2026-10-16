---
title: NereidMobile
---

# NereidMobile

Mobile 是 Link 的移动窗口，以面向 iOS 与 Android 的移动应用，加上一个
微信小程序交付。

!!! warning "技术预览（Tech Preview）"
    Mobile 处于早期阶段。当前仓库包含移动应用与微信小程序；此处描述的能力为
    目标形态，而非已完成产品。许可证尚未声明。

## 它解决什么问题

- 运维人员需要离开桌面控制台后仍能看到设备遥测与告警；Mobile 把这一视图放进
  手机 App 与微信小程序。
- 处于微信生态的团队期望有小程序入口，而不仅是原生 App；Mobile 一并交付两者。
- 现场与值班人员需要轻量、可一眼看清的图表，而非完整的运维控制台。
- 登录应遵循套件统一身份模型，而不是另建一套移动端账号。

## 核心能力

**移动应用**

- 一套代码同时面向 iOS 与 Android。
- 原生 iOS 与 Android 外壳，用于平台相关配置。
- 项目的 CI 流程中执行静态分析与测试套件。

**微信小程序**

- 以微信开发者工具开发的原生微信小程序。
- 开发与发布需要微信小程序 AppID。

**运维视图**

- 经套件身份流程登录，浏览 Link 的设备遥测与看板，查看轻量时序图表并接收告警。

## 在套件中的位置

Mobile 是轻量客户端：它不拥有领域逻辑，也不替代 Link。它从 Link 读取
数据，并依赖套件身份中心完成登录。

- **Mobile → Link**：App 呈现来自 Link 的遥测、看板、图表与告警。
- **身份**：登录遵循套件 SSO 模型，运维人员与桌面产品使用同一身份。参见
  [SSO 与 OIDC](../security/sso-oidc.md)。
- **产品自治**：与其他轻量层一样，Mobile 不得复制 Link 的功能或业务逻辑
  ——它只是这些能力的视图。
- 关于各轻量客户端在闭环中的位置，参见 [套件总览](index.md)。

!!! info "开发者文档"
    本产品的权威、详细开发者文档位于其自有仓库——见
    [NereidAI](https://github.com/NereidAI)。

## 关键事实

| 方面 | 说明 |
|---|---|
| 状态 | 技术预览——早期阶段 |
| 产品定位 | Link 的运维移动窗口 |
| 形态 | iOS 与 Android App，加上微信小程序 |
| 在套件中的位置 | 套件中的轻量客户端，不拥有领域逻辑 |
| 技术栈 | Flutter（Dart）App 加上原生微信小程序 |
| 许可证 | 待补充 |

## 资源

- GitHub：[NereidAI](https://github.com/NereidAI)
- [套件总览](index.md)
- [架构总览](../architecture/overview.md)
- [社区版与企业版](../community/community-vs-enterprise.md)
