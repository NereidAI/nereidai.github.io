# Audit Log

The Audit Log module in NereidHorizon records operations and backend calls for security auditing and troubleshooting. Two views are available: the system log and the audit log.

## System log

The system log records:

- Every API request from the front end to the backend — method, path, status code, duration, user, and organization.
- Every call the backend makes to the Exchange — method, URL, status code, and duration.
- Node registration events (`node_register`) and service startup events.

## Audit log

The audit log records only mutating operations — `POST`, `PUT`, `PATCH`, and `DELETE` — and is intended for operation audit.

## Search the logs

Filter entries by keywords such as user, path, or status code. The view is paginated for browsing long histories.

The log files live in the backend container as `system.log` and `audit.log`, written in JSON-lines format.

## Log fields

| Field | Meaning |
|---|---|
| `t` | Timestamp in ISO format |
| `type` | `api`, `exchange`, or `event` |
| `m` | HTTP method |
| `p` / `url` | Request path / Exchange URL |
| `s` | HTTP status code |
| `ms` | Duration in milliseconds |
| `u` | User (`org/username`) |
| `o` | Organization |

## See also

- [Dashboard](dashboard.md)
- [Node Registration](node_registration.md)
- [BFF Users](bffUsers.md)
