# ML Backend（预标注服务）

ML Backend 是 Label Studio 的模型服务，用于**半自动标注**：对未标注任务自动生成预标注框，标注员在此基础上人工修正。

## 用途

接入 ML Backend 后，预标注会作为 predictions 写入 Label Studio，并在标注工作台可见。标注员只需审核与修正，而不必从零绘制每一个框。

## 流程

1. **注册 ML Backend**：记录名称、URL、关联模型（可选）。
2. **在工作台选择**：通过“半自动标注”按钮旁的下拉选择 ML Backend（或使用默认）。
3. **执行预标注**：预标注作为 predictions 写入 Label Studio，在标注工作台可见。

## 前提条件

- ML Backend 服务需可达（集群内或已暴露）。
- 关联模型时，预标注结果与该模型的类别空间一致。

## 常见问题

!!! question "预标注标签对不上？"

    模型类别与标注配置需保持一致。

!!! question "服务不健康？"

    健康检查是对 `/health` 的真实 HTTP 探测。

## 下一步

注册模型 → 标注工作台选择 → 半自动标注 → 人工审核 → 导出训练。详见[标注](annotations.md)。
