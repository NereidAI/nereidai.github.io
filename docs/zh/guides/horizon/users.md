# 用户

用户模块用于管理 NereidHorizon 中的 Exchange 用户：创建用户、修改密码以及管理其 API 密钥。这些是 Exchange 内部的身份，例如[节点注册](node_registration.md)时使用的节点账号。控制台登录账号（平台管理员和合作方）请在 [BFF 用户](bffUsers.md)中单独管理。

## 创建用户

必填项：

- **Username（用户名）**：唯一标识，例如 `alice`。
- **Password（密码）**：创建时必须设置。

选填项：

- **Email（邮箱）**
- **Admin（管理员）**：是否为管理员。

## 修改密码

点击用户名旁的「Change Password」按钮，输入新密码。

## 管理 API 密钥

在用户详情中生成密钥。密钥仅在创建时显示一次，请立即保存。管理员可以管理其他用户的密钥。节点注册时，节点账号正是使用这样的密钥作为凭证。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | 用户名或密码缺失 |
| 409 | 用户已存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [BFF 用户](bffUsers.md)：本地控制台登录账号。
- [API 密钥](apikeys.md)：用于只读 Partner API 的合作方密钥。
- [节点注册](node_registration.md)
- [组织](organizations.md)
