# Node Registration

Edge nodes — machines running the `anax` agent — register with the Exchange through the `hzn` command line. After registration they pull their pattern or policy, negotiate an agreement, and deploy services. This guide follows that flow and shows where to verify each step in NereidHorizon.

## Phase 1: Prepare the node

1. Install the `anax` agent, for example with `apt install horizon`, or run `anax` in Docker.
2. Confirm the node can reach the Exchange URL over the network.
3. Generate an API key for the node account on the [Users](users.md) page. The key is shown only once.

## Phase 2: Register the node

On the node, run:

```bash
hzn exchange user create -u <org>/<user>:<apikey> -o <exchange-url>
```

Then register with a pattern or a policy:

```bash
hzn register -o <exchange-url> -u <org>/<user>:<apikey> \
  --name <node-name> \
  -p <org>/<pattern-name>    # or --policy <policy-file>
```

Use `-p <org>/<pattern-name>` for pattern deployment, or `--policy <policy-file>` for policy-based deployment.

## Phase 3: Negotiation and deployment

1. The node sends a **proposal** to an agbot.
2. The agbot matches a linked pattern or policy and returns an **agreement**.
3. The node pulls the service image and starts the container.
4. The node continues to report a **heartbeat**.

Make sure the pattern or policy is linked to an agbot on the [Agbots](agbots.md) page; otherwise the negotiation cannot succeed.

## Phase 4: Verify in the UI

- The node appears in the [Edge Nodes](nodes.md) list with status **Online**.
- The node detail's **Services** and **Agreements** tabs show the deployed services and agreements.
- The [Audit Log](auditlog.md) records a `node_register` event.

## Common errors

| Symptom | Likely cause and action |
|---|---|
| Node does not appear | Check the API key, network reachability to the Exchange, and node time synchronization |
| Agreement timeout (reason 201) | Usually the node cannot persist state, for example an `anax.db` permission problem |
| After a pattern change | Re-register: `hzn unregister -f && hzn register ...` |

## See also

- [Edge Nodes](nodes.md)
- [Patterns](patterns.md)
- [Deployment Policies](policies.md)
- [Agbots](agbots.md)
- [Users](users.md)
