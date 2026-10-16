# Getting Started with NereidHorizon

NereidHorizon (Horizon) is the edge distribution console for the Open Horizon management hub: a graphical console for defining services and rolling them out to fleets of edge nodes through patterns or policies. For a product-level overview see the [NereidHorizon product page](../../products/nereidhorizon.md).

This guide walks a first-time operator through the core journey: sign in, connect an edge node, define a service, deploy it with a pattern or a policy, and watch the resulting agreement and rollout.

## 1. Sign in and check the dashboard

1. Sign in to the Horizon console with your operator account.
2. On the [Dashboard](dashboard.md), confirm the Exchange version, current organization, and online node count.
3. Use Quick Actions to reach the modules in the steps below.

## 2. Register and connect an edge node

1. Prepare a machine running the `anax` agent and make sure it can reach the Exchange.
2. On the [Users](users.md) page, create the node account and generate its API key (shown only once).
3. On the node, run `hzn register` against a pattern or policy.
4. Confirm the node appears as online on the [Edge Nodes](nodes.md) page.

The full command sequence and verification steps are in [Node Registration](node_registration.md).

## 3. Define or import a service

A service definition describes the container image and its deployment settings.

- Create one on the [Services](services.md) page — name, label, version, architecture, and image are required.
- Or import an existing definition by pasting JSON or uploading a `.json` file.

Horizon signs the deployment automatically, so no manual signing is needed.

## 4. Deploy with a pattern or a policy

Choose one of the two deployment models:

- **Pattern** — a fixed set of services for a class of nodes. Create it on the [Patterns](patterns.md) page with at least one service, then register nodes to it.
- **Policy** — constraint-matched deployment for dynamic environments. Create a deployment policy on the [Deployment Policies](policies.md) page that targets a service and matches node properties.

In both cases, link the pattern or policy to an [agbot](agbots.md); the node cannot negotiate a deployment until an agbot has it linked.

## 5. Watch the agreement and rollout

1. Open [Agbots](agbots.md) and check the **Agreements** tab for the new agreement.
2. On [Edge Nodes](nodes.md), open the node's drawer and inspect the **Agreements** and **Services** tabs.
3. Watch the **Errors** tab if the rollout stalls, and confirm the result in the [Audit Log](auditlog.md), which records the `node_register` event and every hub call.

## Next steps

- [Edge Nodes](nodes.md) and [Node Registration](node_registration.md)
- [Services](services.md), [Patterns](patterns.md), [Deployment Policies](policies.md)
- [Agbots](agbots.md)
- [Management Policies](mgmtpolicies.md) for agent upgrades and lifecycle actions
- [Organizations](organizations.md), [BFF Users](bffUsers.md), [API Keys](apikeys.md) for multi-tenant setup
