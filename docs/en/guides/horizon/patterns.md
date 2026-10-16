# Patterns

A deployment pattern in NereidHorizon defines the deployment topology and version strategy for a set of services. A node registered to a pattern automatically pulls up the services the pattern contains. Use patterns when the same fixed set of services should run together on a class of nodes; for attribute-matched deployment, see [Deployment Policies](policies.md) instead.

## Create a pattern

Required fields:

- **Pattern Name** — for example `my-pattern`.
- **Label** — display name.
- **Services** — select at least one service from the checkbox list.

A description is optional. For each selected service Horizon generates the `serviceOrgid`, `serviceArch`, `serviceVersions` (default version), and `nodeHealth` entries automatically, with a default `ping_interval` of 60.

## Edit a pattern

Editing replaces all service references in the pattern. You can edit the JSON directly or select services with the checkboxes in the UI.

## Import and inspect

- **Import** — paste the pattern JSON.
- **Detail drawer** — two tabs: **Info** shows the pattern JSON, and **Node Health** shows the health of associated nodes.

## Associate the pattern with an agbot

!!! important "Required after creating a pattern"
    A pattern only reaches nodes after it is linked to an agreement bot. On the [Agbots](agbots.md) page, associate the new pattern with the corresponding agbot so nodes can negotiate it.

## Error codes

| Code | Meaning |
|---|---|
| 400 | No service selected — at least one is required |
| 409 | Pattern already exists |
| 502 | Exchange unreachable |

## See also

- [Services](services.md)
- [Deployment Policies](policies.md)
- [Agbots](agbots.md)
- [Node Registration](node_registration.md)
