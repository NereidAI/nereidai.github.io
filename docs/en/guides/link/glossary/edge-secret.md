# Edge Secret

An **edge secret** is a credential — for example a username/password pair for a third-party system — that the platform delivers to a [gateway](gateway.md) for it to store and use. It is distinct from the device credentials that authenticate the gateway to the platform.

- The platform is the system of record: the secret is stored centrally (encrypted), and the gateway receives it with the desired-state delivery used for [connectors](connector.md).
- The gateway is only a copy: on (re)connection the full set is re-delivered, so replacing a gateway restores its secrets automatically.
- The platform never recognizes a credential protocol. A **secret type** descriptor declares the fields a secret carries as a JSON Schema; the gateway advertises it, or an operator defines it manually. Types with no descriptor fall back to an ad-hoc key/value form.
- A delivered secret may carry long-lived target selectors (such as MAC addresses); the edge alone interprets what they mean.
- A **secret binding** tracks one secret on one gateway with a monotonic revision: PENDING → DISPATCHED → APPLIED (or FAILED + reason), with withdrawal REMOVING → REMOVED. It is managed from the gateway's Secrets tab.

See the [Edge Secret Types](../edge-secret-types.md) and [Edge Secrets](../edge-secrets.md) guides.
