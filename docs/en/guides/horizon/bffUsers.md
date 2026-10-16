# BFF Users

The BFF Users module manages local login accounts for the NereidHorizon console — platform administrators and partners. These accounts authenticate people into the console itself; they are not Exchange users. Exchange users are managed on the [Users](users.md) page.

## Roles

| Role | Capabilities |
|---|---|
| Platform | Create and manage all BFF users, including platform administrators and partners; operate across organizations |
| Partner | Bound to one Exchange organization; after sign-in can operate only on resources inside that organization |

## Create a partner account

Every partner account must be bound to an Exchange organization (`org`). If the specified organization does not exist when the partner is created, Horizon creates it automatically.

## Password and deletion rules

- A platform account can change any user's password; a non-platform user can only change their own.
- You cannot delete the account you are currently signed in with.

## Choosing the right account type

- Use a **BFF user** for a person who signs in to the console.
- Use an [Exchange user](users.md) for an identity that exists inside the hub, such as a node account.
- Use an [API key](apikeys.md) for a system that calls the read-only Partner API without a console sign-in.

## See also

- [Users](users.md)
- [Organizations](organizations.md)
- [API Keys](apikeys.md)
