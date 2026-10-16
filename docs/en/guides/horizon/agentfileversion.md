# Agent File Version

The Agent File Version module in NereidHorizon manages the lists of agent software, configuration, and certificate versions. These lists guide edge nodes when they perform an agent upgrade, typically as part of an upgrade [management policy](mgmtpolicies.md).

## Edit version lists

Each list holds one version number per line, for example:

```text
2.30.0
```

The three lists are maintained separately:

- **Software Versions** — agent software versions.
- **Config Versions** — agent configuration versions.
- **Cert Versions** — agent certificate versions.

## Unsupported Exchange versions

If the connected Exchange does not support this feature, the page shows an empty state. Horizon treats the backend's `400` response as a graceful degradation, so an unsupported Agent File Version capability does not affect any other function.

## Error codes

| Code | Meaning |
|---|---|
| 400 | The current Exchange version does not support AgentFileVersion — graceful degradation, other functions are unaffected |
| 502 | Exchange unreachable |

## See also

- [Management Policies](mgmtpolicies.md)
- [Edge Nodes](nodes.md)
