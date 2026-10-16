# Edge Nodes

The Edge Nodes module is where you manage the edge nodes registered to the hub in NereidHorizon. From this page you can view and search nodes, set a deployment pattern, edit node policy, and inspect agreements, errors, and management status. For how nodes first join the hub, see [Node Registration](node_registration.md).

## Step 1: View nodes

The table lists every node with its ID, name, type, architecture, memory, deployment method, number of deployed services, privileged flag, last heartbeat, and status. The list supports search (by name, type, pattern, or architecture) and pagination.

## Step 2: Set a pattern

1. Click **Set Pattern** at the end of the node's row.
2. Choose a deployment pattern from the dropdown. Pattern names use the `org/patternname` format.
3. Leave the selection empty to clear the pattern and deploy the node by policy instead.

!!! note "Authorizing a pattern change"
    Changing the pattern of a registered node requires `root/root` authorization — click **Authorize** and enter the root password. After the change you must re-register the node for it to take effect; Horizon generates the command for you.

## Step 3: View details

Click **View** to open the detail drawer, which has five tabs:

| Tab | Contents |
|---|---|
| Info | Basic information and the editable node policy |
| Services | Registered and deployed services with their agreement IDs |
| Agreements | All agreements currently reached for the node |
| Errors | Node error history |
| Mgmt Status | Execution status of management policies (NMP) |

## Step 4: Edit node policy

- System properties under `openhorizon.*` are read-only.
- Add custom **Properties** as `Name=Value` pairs, for example `gpu=true`.
- Add **Constraints**, one per line, for example `openhorizon.allowPrivileged == true`.
- The **allowPrivileged** switch controls whether privileged containers are allowed; changes take effect automatically after about 60 seconds.

## Error codes

| Code | Meaning | Action |
|---|---|---|
| 401 | Unauthorized | Re-login or provide root authorization |
| 400 | Bad request | Fix invalid parameters, such as an incorrectly formatted pattern |
| 502 | Exchange connection failed | Check the Exchange URL and network |

## See also

- [Node Registration](node_registration.md)
- [Patterns](patterns.md)
- [Deployment Policies](policies.md)
- [Agbots](agbots.md)
