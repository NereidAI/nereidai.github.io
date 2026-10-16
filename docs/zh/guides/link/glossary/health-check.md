# 健康检查

**健康检查**（`health_check`）是绑定设备的[连接器](connector.md)上的可选探测规约。网关周期性读一个资源并**丢弃读数**——探测绝不产生[遥测](telemetry.md)或[设备影子](shadow.md)数据。

- 字段：`resource`、`interval_ms`（默认 30000）、`timeout_ms`（默认 5000，必须短于间隔）、`fail_threshold`（默认 3）。
- 在线/离线的边沿判定归网关：它根据连续探测结果标记可达性。

健康检查只在连接器绑定[子设备](subdevice.md)时有意义；网关级连接器没有单一可探测的资源属主。
