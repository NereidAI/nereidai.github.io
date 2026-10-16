# NereidIdentity 入门

NereidIdentity 是套件级身份平面：Sphere、Link、Horizon 与 Forge 背后共享的、
可替换的单点登录（SSO）与访问控制中心。当前引擎为 Keycloak 26 配独立
PostgreSQL，使用 `nereidai` 领域（realm）。引擎只是标准 OIDC/OAuth2 契约
背后的实现细节，并非用户直接打开的门户。

!!! tip "通常不需要直接接触 Identity"
    Identity 是后端服务。默认集成中只有 Sphere 与它说 OIDC：用户经 Sphere
    登录，管理员在 Sphere 的账号控制台管理账号。脱离套件独立部署的产品，
    也可以注册自己的 OIDC 客户端。

## 前提条件

- 已部署且可达的 Identity 实例（其 issuer 地址），以及一个指向它配置的
  Sphere 门户。
- 登录所需：管理员在套件领域中分配的账号。
- 管理账号所需：Sphere 中的套件**管理员**角色。

## 1. 理解 Identity 的位置

- **Identity** 是账号、角色与令牌的唯一事实来源。
- **Sphere** 是唯一强制的 OIDC 依赖方：它驱动浏览器登录（授权码 + PKCE），
  并默认通过一次性密封票据把身份移交给已集成产品。
- **授权留在产品内部。** RBAC、租户与功能权限都在各产品内部；套件身份证明
  你是谁，而按产品的授权用户组决定能否进入产品。

完整模型见 [SSO 与 OIDC](../../security/sso-oidc.md)。

## 2. 作为用户登录

1. 打开 Sphere 门户，点击**使用 NereidIdentity 登录**。
2. 在 Identity 登录页输入凭据；若配置了代理的组织身份提供商（如 Entra ID 或
   Okta），也可选择对应提供商登录。
3. 返回 Sphere 后即获得套件会话，可以不再登录直接打开所有已授权产品。

套件用户永远不需要登录 Keycloak 管理控制台。

## 3. 作为管理员管理用户

1. 在 Sphere 中打开用户菜单，选择**账号**。
2. 创建用户、重置密码、启用或停用账号，分配套件角色以及各产品的租户/角色
   成员关系。
3. 由外部身份提供商提供的账号带有外部标记，在此只读——其生命周期请在对应
   提供商中管理。

Sphere 通过服务账号客户端调用 Identity Admin REST API 完成这些操作，因此
管理员不需要掌握引擎的主控凭据。

## 4. 服务运维

Identity 以容器镜像交付，中心部署用 Helm chart，本地开发用 Docker Compose
栈。领域、客户端与管理员服务账号授权在 Identity 仓库中声明式预置；客户身份
系统始终通过身份代理接到 Identity 之后，绝不直接连到 Sphere 或产品。

!!! note "运维细节在哪里"
    领域预置、客户端注册、外部 IdP 代理配置与运维手册都记录在 NereidIdentity
    仓库（[NereidAI](https://github.com/NereidAI)），不在本运维指南中。

## 下一步

- [SSO 与 OIDC](../../security/sso-oidc.md)——模式、票据与联邦。
- [RBAC](../../security/rbac.md)——套件角色与产品本地授权。
- [NereidIdentity 产品页](../../products/nereididentity.md)。
