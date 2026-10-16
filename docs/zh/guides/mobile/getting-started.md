# NereidMobile 入门

!!! warning "技术预览（Tech Preview）"
    Mobile 处于早期阶段。当前仓库包含 Flutter App 与原生微信小程序；此处描述
    的运维界面是目标形态，许可证也尚未声明。请把它视为预览，而非已完成的
    发布版本。

NereidMobile 是运维人员观察 Link 的移动窗口：一套 Dart 代码同时面向 iOS 与
Android 的 Flutter 应用，加上一个原生微信小程序。它是轻量客户端——不拥有
领域逻辑，只从 Link 读取遥测、看板、图表与告警，并依赖 Identity 完成登录。

## 前提条件

- 一个可达、且已有设备上报遥测的 Link 实例；空平台上 Mobile 无内容可展示。
- 套件身份流程可用（经 Sphere SSO 使用 Identity），且账号具备该 Link 租户的
  访问权限。当 Link 脱离套件独立运行时，Mobile 的 SSO 入口不适用——参见
  [默认可独立](../../products/index.md#standalone-by-default)。
- 手机上已安装 App，或已在微信中打开小程序。构建或发布小程序还需要微信小程序
  AppID。

## 1. 登录

打开 App 或小程序，完成套件登录流程——与桌面产品使用同一身份，不需要单独的
移动端账号。流程背景见 [SSO 与 OIDC](../../security/sso-oidc.md)。

## 2. 浏览设备与遥测

登录后可看到你的 Link 设备及其实时连接状态。打开设备即可查看最新遥测与看板。
这些就是 Link 采集的同一份数据，只是按手机而非完整运维控制台的方式呈现。

## 3. 查看时序图表

打开某个测点可查看轻量时序图表，便于在外移动时一眼分析。Mobile 刻意定位为
可快速浏览的现场视图，并不替代桌面看板。

## 4. 接收告警

Link 告警会推送到手机，现场与值班人员离开控制台后也能及时响应。告警规则与
升级策略仍在 Link 内部配置。

## 尝试构建（开发者）

App 是标准 Flutter 项目：在 `app/` 目录中执行 `flutter pub get` 后运行
`flutter run`。小程序则在微信开发者工具中导入 `miniapp/` 目录并填入 AppID。
工具链前提（Flutter SDK、iOS 所需的 Xcode、Android SDK、微信开发者工具）与
构建命令记录在 NereidMobile 仓库
（[NereidAI](https://github.com/NereidAI)）。

## 下一步

- [NereidMobile 产品页](../../products/nereidmobile.md)。
- [Link 总览](../link/overview.md)——Mobile 所呈现的看板。
- [Link 入门](../link/getting-started.md)——先让遥测流动起来。
