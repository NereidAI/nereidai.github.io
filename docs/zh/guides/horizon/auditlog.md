# 审计日志

审计日志模块记录 NereidHorizon 中的系统操作与后端调用，用于安全审计和问题排查。模块提供两种视图：系统日志和审计日志。

## 系统日志（System Log）

系统日志记录：

- 所有前端发往后端的 API 请求：方法、路径、状态码、耗时、用户和组织。
- 所有后端发往 Exchange 的调用：方法、URL、状态码和耗时。
- 节点注册事件（`node_register`）和服务启动事件。

## 审计日志（Audit Log）

审计日志仅记录变更类操作——`POST`、`PUT`、`PATCH` 和 `DELETE`，用于操作审计。

## 搜索日志

可按用户、路径、状态码等关键词过滤记录，并支持分页浏览较长的历史。

日志文件位于后端容器内，文件名为 `system.log` 和 `audit.log`，采用 JSON 行（JSON-lines）格式。

## 日志字段说明

| 字段 | 含义 |
|---|---|
| `t` | 时间戳（ISO 格式） |
| `type` | `api`、`exchange` 或 `event` |
| `m` | HTTP 方法 |
| `p` / `url` | 请求路径 / Exchange URL |
| `s` | HTTP 状态码 |
| `ms` | 耗时（毫秒） |
| `u` | 用户（`org/username`） |
| `o` | 组织 |

## 另请参见

- [仪表盘](dashboard.md)
- [节点注册](node_registration.md)
- [BFF 用户](bffUsers.md)
