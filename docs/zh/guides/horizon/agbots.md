# 协议机器人

协议机器人（Agbot / Agreement Bot）是 Exchange 中的协商代理。在 NereidHorizon 中，它负责为边缘节点匹配服务与部署策略，并达成让工作负载真正运行的**协议（Agreement）**。节点能否部署服务，取决于 agbot 是否关联了对应的模式或策略。

## 详情抽屉

点击某个 agbot 可打开包含 4 个标签页的抽屉：

| 标签页 | 内容 |
|---|---|
| Patterns | 已关联到该 agbot 的模式 |
| Business Policies | 已关联到该 agbot 的业务策略 |
| Agreements | 当前所有协议，含状态、服务规格和关联节点 |
| Agbot Info | ID、最后心跳和公钥 |

## 关联模式或策略

1. 点击 agbot 行尾的「Link pattern」或「Link policy」。
2. 在弹出的列表中选择要绑定的模式或策略。

已关联的内容会显示在抽屉的「Patterns」和「Business Policies」标签页中，协商产生的协议显示在「Agreements」标签页中。

## 跨组织浏览

点击「Authorize」，输入 `root/root` 或具有跨组织权限的账号，即可浏览其他组织的模式与策略。IBM 组织的 agbot 会自动合并到列表中，且仅在系统组织下可见。

## 错误码

| 错误码 | 含义 |
|---|---|
| 401 | 未授权，或跨组织授权已失效 |
| 404 | 模式或策略不存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [部署模式](patterns.md)
- [部署策略](policies.md)
- [边缘节点](nodes.md)
- [节点注册](node_registration.md)
