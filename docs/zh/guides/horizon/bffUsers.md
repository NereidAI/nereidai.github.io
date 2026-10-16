# BFF 用户

BFF 用户模块用于管理 NereidHorizon 控制台的本地登录账号——平台管理员和合作方。这些账号用于人员登录控制台本身，并非 Exchange 用户。Exchange 用户请在[用户](users.md)页面管理。

## 角色

| 角色 | 能力 |
|---|---|
| 平台（Platform） | 创建和管理所有 BFF 用户（含平台管理员和合作方），可跨组织操作 |
| 合作方（Partner） | 必须绑定一个 Exchange 组织，登录后只能操作该组织内的资源 |

## 创建合作方账号

每个合作方账号都必须绑定一个 Exchange 组织（org）。创建合作方时，如果指定的 Exchange 组织尚不存在，Horizon 会自动创建。

## 密码与删除限制

- 平台账号可以修改任意用户的密码；非平台用户只能修改自己的密码。
- 无法删除当前登录的账号本身。

## 如何选择账号类型

- 人员登录控制台，使用 **BFF 用户**。
- 管理中心内部的身份（例如节点账号），使用 [Exchange 用户](users.md)。
- 外部系统不登录控制台、直接调用只读 Partner API，使用 [API 密钥](apikeys.md)。

## 另请参见

- [用户](users.md)
- [组织](organizations.md)
- [API 密钥](apikeys.md)
