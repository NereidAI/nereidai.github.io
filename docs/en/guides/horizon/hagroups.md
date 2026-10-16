# HA Groups

An HA (high-availability) group in NereidHorizon organizes multiple edge nodes into a high-availability cluster so that services can be deployed redundantly across the group. Use HA groups when a workload must keep running even if one member node is lost.

## Create an HA group

1. Open the HA Groups page and start a new group.
2. Enter a unique **group name** — this is required.
3. Optionally add a description and choose member nodes.

## Edit membership

In the edit view, add nodes to the group or remove existing members. Each node can belong to only one HA group, so a node already in another group cannot be added until it is removed there.

## Delete an HA group

Remove all member nodes first; a group that still has members cannot be deleted.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Group name missing or invalid |
| 409 | A group with that name already exists |
| 502 | Exchange unreachable |

## See also

- [Edge Nodes](nodes.md)
- [Services](services.md)
