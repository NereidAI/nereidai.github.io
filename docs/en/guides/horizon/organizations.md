# Organizations

An organization is the top-level isolation unit in the Exchange. In NereidHorizon each organization owns its own services, patterns, nodes, and related resources, so operations performed inside one organization do not affect the others.

## Create an organization

Required fields:

- **Org ID** — unique identifier.
- **Label** — display name.

Optional fields:

- Description.
- Node count limit.
- Heartbeat interval.

## Permissions

- **Hub Admin** users can create and delete organizations.
- The system organization (**IBM**) has a global view across the hub.

When you create partner accounts under [BFF Users](bffUsers.md), a partner bound to an organization can only operate on resources within that organization.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Org ID missing |
| 409 | Organization already exists |
| 502 | Exchange unreachable |

## See also

- [BFF Users](bffUsers.md)
- [Catalog](catalog.md)
- [Edge Nodes](nodes.md)
