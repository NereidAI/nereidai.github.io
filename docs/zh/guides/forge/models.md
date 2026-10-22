# 模型

模型库是工厂中心的注册中心：每个训练、优化或导入的版本都带血缘、指标与部署历史汇聚于此。在
此页面你可以横向对比版本、用图片快速试跑，并把模型发布为在线推理服务。

## 模型与版本

- 一个**模型**聚合同一解决方案的多个版本；一个**版本**是一份不可变产物。
- 版本有三种来源：
  1. **训练**——成功后自动注册（CV 为权重 + ONNX；LLM/VLM 为适配器/tokenizer）。
  2. **优化**——以 `{source-version}-onnx-{dtype}` 之名注册到源模型下，带目标设备、加速比、
     体积与精度下降指标。
  3. **手动上传**——导入 `.pt` / `.pth` / `.onnx` / `.safetensors`（及相关权重），框架按
     后缀推断。
- 每个版本保存框架（`pytorch` / `onnx` / …）、任务（检测 / 分割 / 分类 / llm / vlm）、来源
  任务、指标与产物 URI。

## 对比与选型

版本表展示任务、框架、目标设备，以及优化版本的实测加速比/体积。当存在多个 int8 目标时，按你
需要的延迟/精度点选择，而不是按名字挑选。在优化版本通过评估前，同时保留 FP32 源版本与量化
版本。

## 用图片试跑某个版本

部署前，可在版本行使用**用图片试跑**：

- 上传一张图片并设置置信度阈值；Forge 通过共享 ML Backend 用**该确切版本**推理——**无需
  KServe 部署**。
- 检测画出带标签与分数的框；分类返回 top-5；并报告推理耗时。
- PyTorch（`.pt`）版本额外支持 **Grad-CAM** 热力图，显示驱动预测的区域（ONNX 无梯度，开关
  不可用）。
- 无法直接加载的旧版检测权重，会透明地经其同名 ONNX 产物提供服务（界面会标记）；
  原始 `.pt` 绝不被修改。

## 用 KServe 部署

1. 选择版本并打开**部署**。
2. 选择**服务运行时**。列表来自集群中安装的 KServe `ClusterServingRuntime` 定义——例如
   **OpenVINO**（CPU，已验证的默认项）或 **NVIDIA Triton**（GPU）；当集群提供 vLLM 兼容运行
   时，LLM/VLM 也会出现对应项。
3. 按表单需要选择加速器/域名并确认。
4. Forge 提交流水线，创建 KServe **InferenceService** 与 **Ingress**，随后把服务名、运行时、
   域名记录到版本上。

端点默认遵循 `<model>-<version>.inference.<platform-domain>`；请让该域名的 DNS 指向集群
Ingress。部署是异步的（通常 1–3 分钟）——部署列表自动刷新，直接根据 KServe 显示部署中 /
就绪 / 失败状态。

**下线（Undeploy）**会删除 InferenceService 与 Ingress；模型版本与产物仍保留在库中，随时可
重新部署。

## 前提条件

- 手动导入需提供受支持的权重/ONNX 文件。
- 所选运行时必须以 `ClusterServingRuntime` 存在，GPU/NPU 运行时还需节点上有对应设备。
- 部署域名必须能在 DNS 解析到集群 Ingress 地址。
- KServe 及其服务账号 / Ingress 绑定由集群运维在平台安装时预置。

## 常见问题

!!! question "部署后如何访问模型？"
    部署响应与部署列表会显示端点域名。Ingress 自动创建，只需让 DNS 指向集群 Ingress IP。

!!! question "选 OpenVINO 还是 Triton？"
    CPU 推理用 OpenVINO（端到端已验证）；NVIDIA GPU 服务用 Triton。LLM/VLM 使用集群安装的
    vLLM 兼容运行时。运行时要与模型实际运行位置匹配。

!!! question "试跑可以但部署失败？"
    试跑走共享 ML Backend，不需要 KServe；部署还额外需要匹配的服务运行时、节点资源与 DNS。先
    检查部署状态/信息与集群预置情况。

## 下一步

- 使用并集成端点；之后用现场数据重训——循环从[数据集](datasets.md)重新开始。
- 用[优化](optimization.md)与[评估](evaluation.md)继续打磨已部署模型。
