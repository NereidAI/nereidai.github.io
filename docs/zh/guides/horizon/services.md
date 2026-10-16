# 服务

服务模块用于管理 NereidHorizon 中的服务定义。服务定义描述边缘节点运行某个工作负载所需的容器镜像、部署配置和资源限制。在此可以创建、编辑、导入和导出服务定义。

## 创建服务

在「Basic Info」面板中，以下为必填项：

| 字段 | 说明 | 示例 |
|---|---|---|
| Service Name（服务名称） | 唯一标识 | `myweather` |
| Label（标签） | 显示名称 | `My Weather Service` |
| Version（版本） | 语义化版本号 | `1.0.0` |
| Architecture（架构） | 目标架构 | `amd64`、`arm64`、`arm` |
| Image name（镜像名称） | `name:tag` 格式 | `openhorizon/example:1.0.0` |

选填项包括：服务 URL、HA 模式、共享块设备、特权模式、内存/CPU 限制、端口、健康检查、网络、存储、环境变量和密钥。

最小可用服务定义示例：

```json
{
  "label": "My Service",
  "version": "1.0.0",
  "arch": "amd64",
  "deployment": {
    "services": {
      "myorg/myservice": { "image": "myorg/myservice:1.0.0" }
    }
  }
}
```

## 编辑服务

编辑支持两种模式：JSON 编辑和 UI 表单编辑，切换标签页时两种模式自动同步。在 UI 模式下修改 deployment 后，Horizon 会自动重新签名。

## 导入与查看

- **导入（Import）**：可直接粘贴服务 JSON，或上传 `.json` 文件。
- **详情抽屉**：包含 **Info**、**Keys**、**Docker Auths** 三个标签页。Keys 管理服务公钥，Docker Auths 管理私有镜像仓库认证。

## 签名说明

Horizon 使用 RSA-PSS SHA-256 自动对 deployment 签名，无需任何手动操作。

## 错误码

| 错误码 | 含义 |
|---|---|
| 400 | JSON 格式错误，或必填字段缺失（`label`/`version`/`arch`/`image`） |
| 409 | 同名同版本的服务已存在 |
| 502 | Exchange 不可达 |

## 另请参见

- [部署模式](patterns.md)
- [部署策略](policies.md)
- [节点注册](node_registration.md)
