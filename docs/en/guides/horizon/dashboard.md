# Dashboard

The Dashboard is the default landing page after you sign in to NereidHorizon. It gives an at-a-glance view of the overall system status so you can confirm the hub is healthy and jump straight into daily operations. Horizon renders all Dashboard data from the Exchange API and refreshes it automatically every 30 seconds.

## What the page shows

- **System Info card** — Exchange version, BFF service start time and uptime, current organization, and online node count.
- **Quick Actions** — card-style shortcuts that take you directly to functional modules such as services, patterns, and nodes.
- **Recent Node Activity** — the edge nodes that most recently reported a heartbeat, sorted by last heartbeat time with the newest first.

## How to use it

1. After sign-in, confirm the **System Info** card shows the expected Exchange version and your current organization.
2. Check the **online node count** to see whether the fleet is connected.
3. Review **Recent Node Activity** to spot nodes that have stopped reporting.
4. Use **Quick Actions** to open the module you need instead of navigating the sidebar.

## Troubleshooting

!!! warning "Connection failed"
    If the Dashboard shows a connection failure, verify that the Exchange URL is correct, that the network from Horizon to the Exchange is reachable, and that your login credentials are valid.

## See also

- [Edge Nodes](nodes.md)
- [Node Registration](node_registration.md)
- [Audit Log](auditlog.md)
