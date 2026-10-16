# Agbots

An agbot (agreement bot) is the Exchange negotiation agent in NereidHorizon. It matches services and deployment policies to edge nodes and forms the **agreements** that cause workloads to run. Whether a node can deploy a service depends on whether an agbot has the matching pattern or policy linked.

## The detail drawer

Clicking an agbot opens a drawer with four tabs:

| Tab | Contents |
|---|---|
| Patterns | Patterns linked to this agbot |
| Business Policies | Business policies linked to this agbot |
| Agreements | Current agreements with status, service specs, and associated node |
| Agbot Info | ID, last heartbeat, and public key |

## Link a pattern or policy

1. Click **Link pattern** or **Link policy** at the end of the agbot's row.
2. Choose the pattern or policy from the popup list.

Linked items appear in the drawer's **Patterns** and **Business Policies** tabs, and resulting agreements appear under **Agreements**.

## Browse other organizations

Click **Authorize** and provide `root/root` credentials, or an account with cross-organization permissions, to browse patterns and policies in other organizations. Agbots from the IBM organization are merged into the list automatically; they are visible only in the system organization.

## Error codes

| Code | Meaning |
|---|---|
| 401 | Unauthorized, or cross-organization authorization has expired |
| 404 | Pattern or policy not found |
| 502 | Exchange unreachable |

## See also

- [Patterns](patterns.md)
- [Deployment Policies](policies.md)
- [Edge Nodes](nodes.md)
- [Node Registration](node_registration.md)
