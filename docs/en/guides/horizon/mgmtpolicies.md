# Management Policies

A management policy (NMP) in NereidHorizon handles node upgrade and lifecycle management — for example agent upgrades and node configuration push. Management policies target nodes by constraint, and the result of their execution is visible on each node's **Mgmt Status** tab.

## Create a management policy

Required fields:

- **Policy Name**
- **Label**
- **Type** — `upgrade` or `lifecycle`.

Optional fields:

- **Constraints** — select the target nodes.
- **Properties** — payload of the policy. For an agent upgrade, supply an `agentUpgradePolicy`, for example:

```json
{ "type": "agent", "version": "2.30.0" }
```

## Edit and import

- **Edit** — updating the policy issues a PUT that replaces its configuration.
- **Import** — paste the management policy JSON.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Unsupported type, or a required field is missing |
| 409 | Policy already exists |
| 502 | Exchange unreachable |

## See also

- [Edge Nodes](nodes.md) — the **Mgmt Status** tab shows policy execution state.
- [Agent File Version](agentfileversion.md) — version lists that guide agent upgrades.
- [Deployment Policies](policies.md)
