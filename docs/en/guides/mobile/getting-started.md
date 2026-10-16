# Getting Started with NereidMobile

!!! warning "Tech Preview"
    Mobile is at an early stage. The repository currently contains the Flutter
    app and the native WeChat Mini Program; the operator surface described here
    is the target, and the license is not yet declared. Treat it as a preview
    rather than a finished release.

NereidMobile is the operator's window into Link: a Flutter application for iOS
and Android built from one Dart codebase, alongside a native WeChat Mini
Program. It is a thin client — it owns no domain logic, reads telemetry,
dashboards, charts and alerts from Link, and relies on Identity for sign-in.

## Prerequisites

- A reachable Link instance with devices already sending telemetry; Mobile has
  nothing to show on an empty platform.
- The suite identity flow available (Identity through Sphere SSO) and an account
  with access to the Link tenant. When Link runs standalone without the suite,
  Mobile's SSO entry does not apply — see
  [Standalone by default](../../products/index.md#standalone-by-default).
- The app installed on a phone, or the Mini Program opened in WeChat. Building
  or releasing the Mini Program additionally requires a WeChat Mini Program
  AppID.

## 1. Sign in

Open the app or the Mini Program and complete the suite sign-in flow — the same
identity you use for the desktop products. There is no separate mobile account.
Background on the flow: [SSO & OIDC](../../security/sso-oidc.md).

## 2. Browse devices and telemetry

After sign-in you see your Link devices and their live connection state. Open a
device to view its latest telemetry and dashboards. This is the same data Link
collects, laid out for a phone rather than the full operations console.

## 3. View time-series charts

Open a measurement to view a lightweight time-series chart for at-a-glance
analysis while on the move. Mobile is intentionally a glanceable field view, not
a replacement for the desktop dashboards.

## 4. Receive alerts

Link alerts are delivered to the phone, so field and on-call staff can react
away from the console. Alert rules and escalation remain configured inside Link.

## Trying the builds (developers)

The app is a standard Flutter project: run `flutter pub get` then
`flutter run` inside `app/`. The Mini Program is imported into WeChat DevTools
from the `miniapp/` directory with your AppID. Toolchain prerequisites
(Flutter SDK, Xcode for iOS, Android SDK, WeChat DevTools) and build commands
are documented in the NereidMobile repository ([NereidAI](https://github.com/NereidAI)).

## Next steps

- [NereidMobile product page](../../products/nereidmobile.md).
- [Link Overview](../link/overview.md) — the dashboards Mobile mirrors.
- [Link Getting Started](../link/getting-started.md) — get telemetry flowing
  first.
