# Users

The Users module manages Exchange users in NereidHorizon: creating users, changing passwords, and managing their API keys. These are identities inside the Exchange — for example node accounts used during [node registration](node_registration.md). Console login accounts (platform administrators and partners) are managed separately under [BFF Users](bffUsers.md).

## Create a user

Required fields:

- **Username** — unique identifier, for example `alice`.
- **Password** — must be set at creation time.

Optional fields:

- **Email**
- **Admin** — whether the user is an administrator.

## Change a password

Click **Change Password** next to the username and enter the new password.

## Manage API keys

Generate a key from the user's detail view. The key is shown only once when it is created — save it immediately. Administrators can manage other users' keys. Node registration uses such a key for the node account's credentials.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Username or password missing |
| 409 | User already exists |
| 502 | Exchange unreachable |

## See also

- [BFF Users](bffUsers.md) — local console login accounts.
- [API Keys](apikeys.md) — partner API keys for the read-only Partner API.
- [Node Registration](node_registration.md)
- [Organizations](organizations.md)
