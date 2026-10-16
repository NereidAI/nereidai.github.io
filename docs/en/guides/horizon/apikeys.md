# API Keys

API keys in NereidHorizon let partners read their own organization's data through the read-only Partner API (`GET /api/v1/{org}/...`) without signing in to the console. Use a key when another system needs to pull service, pattern, policy, or node information from your organization programmatically.

## Key format and storage

- Keys use the `nk_live_<random>` or `nk_test_<random>` format.
- Horizon stores only the SHA-256 hash of each key. The plaintext key is shown exactly once, when the key is created.

## Who can manage keys

| Role | Can |
|---|---|
| Partner | Create and revoke keys for the partner's own organization only; no access to other organizations |
| Platform | Create and delete keys for any organization |

## Create a key

1. Open the API Keys page.
2. Provide a **label** describing the key's purpose.
3. Set an **expiry in days**, or choose for the key never to expire.
4. Copy the plaintext key from the creation dialog immediately.

## Revoke or delete a key

A revoked key becomes invalid immediately; calls made with it to the Partner API return 401. Delete a key to remove it entirely.

!!! danger "Handle the secret carefully"
    The plaintext key is displayed only once in the creation dialog. Copy and save it immediately, and revoke it at once if it is ever leaked.

## See also

- [BFF Users](bffUsers.md) — console login accounts and roles.
- [Users](users.md) — Exchange users and their keys.
- [Audit Log](auditlog.md)
