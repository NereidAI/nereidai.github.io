# Deployment Policies

A deployment policy (business policy) in NereidHorizon is an automatic service-deployment rule based on properties and constraints. Policies suit flexible deployments that do not depend on a fixed pattern: the agbot matches the policy against each eligible node instead of the node joining a fixed service set.

## Create a policy

Required fields:

- **Policy Name**
- **Label**
- **Target Service** — the URL of the service to deploy.

Optional fields:

- **Properties** — characteristics describing the service.
- **Constraints** — matching rules, for example `openhorizon.allowPrivileged == true`.
- **Service Org**, **Service Arch**, and the **service version range**.

## Import a policy

Paste the policy JSON into the importer. The JSON must include the `businessPolicy` wrapper.

## Policy versus pattern

A pattern is a fixed set of services: every node registered to the pattern runs the same set. A policy is constraint-matched deployment, which fits dynamic environments where different nodes run a service depending on their attributes. After creating a policy, link it to an agbot on the [Agbots](agbots.md) page so it can be negotiated.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Missing target service, or invalid constraint format |
| 409 | Policy already exists |
| 502 | Exchange unreachable |

## See also

- [Patterns](patterns.md)
- [Services](services.md)
- [Agbots](agbots.md)
- [Edge Nodes](nodes.md)
