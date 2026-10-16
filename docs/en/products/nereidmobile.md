---
title: NereidMobile
---

# NereidMobile

Mobile is the operator's window into Link, delivered as a mobile
application for iOS and Android alongside a WeChat Mini Program.

!!! warning "Tech Preview"
    Mobile is at an early stage. The repository currently contains the
    mobile app and the WeChat Mini Program; treat the surface described here as
    the target rather than a finished product. The license is not yet declared.

## What it solves

- Operators need to see device telemetry and alerts away from a desktop console;
  Mobile puts that view in a phone app and a WeChat Mini Program.
- Teams in the WeChat ecosystem expect a Mini Program entry point, not only a
  native app; Mobile ships both.
- Field and on-call staff need lightweight, glanceable charts rather than a full
  operations console.
- Sign-in should follow the suite identity model rather than a separate mobile
  account.

## Core capabilities

**Mobile app**

- A single codebase targeting both iOS and Android.
- Native iOS and Android shells for platform-specific configuration.
- Static analysis and a test suite in the project's CI workflow.

**WeChat Mini Program**

- A native WeChat Mini Program developed with WeChat DevTools.
- A WeChat Mini Program AppID is required for development and release.

**Operator surface**

- Sign in through the suite identity flow, browse Link device telemetry and
  dashboards, view lightweight time-series charts, and receive alerts.

## How it fits in the suite

Mobile is a thin client: it never owns domain logic and does not replace
Link. It reads from Link and relies on the suite identity center for
sign-in.

- **Mobile → Link:** the app surfaces telemetry, dashboards, charts,
  and alerts from Link.
- **Identity:** sign-in follows the suite SSO model, so operators use the same
  identity as the desktop products. See [SSO & OIDC](../security/sso-oidc.md).
- **Product autonomy:** like the other thin layers, Mobile must not
  duplicate Link's features or business logic — it is a view onto them.
- See the [suite overview](index.md) for how the thin clients fit the closed
  loop.

!!! info "Developer documentation"
    The authoritative, detailed developer documentation for Mobile lives
    in its own repository — see [NereidAI](https://github.com/NereidAI).

## Key facts

| Aspect | Detail |
|---|---|
| Status | Tech Preview — early stage |
| What it is | The operator's window into Link |
| Form factors | iOS and Android app, plus a WeChat Mini Program |
| Positioning | Thin client in the suite; owns no domain logic |
| Stack | Flutter (Dart) app plus a native WeChat Mini Program |
| License | Pending — to be added |

## Resources

- GitHub: [NereidAI](https://github.com/NereidAI)
- [Suite overview](index.md)
- [Architecture overview](../architecture/overview.md)
- [Community vs Enterprise](../community/community-vs-enterprise.md)
