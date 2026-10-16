# Getting Started with NereidLink

NereidLink is the privatized IoT data pipeline of the suite: multi-protocol
device access, a unified message backbone, a rule engine, alerting and
real-time dashboards. It ships as one codebase in two forms — an all-in-one
binary or Kubernetes microservices. This guide is the operator's first-run
path from an empty tenant to live telemetry on the Overview.

!!! tip "Runs standalone"
    Link is a complete product on its own. You do not need Sphere, Identity or
    any other product to connect devices and see data. Suite single sign-on and
    the portal only apply when Sphere is deployed as the entry point — see
    [Standalone by default](../../products/index.md#standalone-by-default).

## Prerequisites

- A running Link instance (the all-in-one binary or a Kubernetes deployment)
  and the URL of its console.
- A console account with permission to manage profiles, devices and
  credentials — a Link-local account on a standalone install, or a suite
  account with a Link role when Sphere is present.
- Something to connect: a device that speaks MQTT/HTTP directly, or a
  [gateway](glossary/gateway.md) such as Edge that fronts field sub-devices.

## 1. Sign in

Open the Link console. On a standalone deployment you sign in with Link's own
account; when the suite is used, you typically enter Link from the Sphere
portal without a second login. Either way the console experience is the same.

## 2. Create a device profile

A [device profile](glossary/profile.md) groups measurement descriptors — point
names, value types, units and optional transforms. A profile is optional
(values are still stored without one), but creating one first means units and
engineering values are correct from the very first frame.

1. Open **Profiles** and click **Create profile**.
2. Give it a name and, if relevant, a protocol family such as `modbus`.
3. Add one descriptor per measurement key the device publishes.

See [Device Profiles](profiles.md) for the full descriptor and transform
options.

## 3. Register a device

1. Open **Devices** and click **Create device**.
2. The **canonical name** (`dev-xxxx`, or `gw-xxxx` for a gateway) is generated
   for you and stays the stable device identity.
3. Select the profile you created (optional) and set a human-friendly alias if
   you like.
4. For a gateway deployment, create the parent as type **gateway**, then create
   each field device as a sub-device bound to that gateway. See
   [Devices](devices.md).

## 4. Add a credential

A device cannot connect until it holds at least one valid credential. Open the
device's **Credentials** tab and add one: `TOKEN` for a simple shared secret,
`PASSWORD`, `JWT`, or `X509` for an mTLS client certificate.

!!! note "Copy the secret now"
    A newly created secret is shown exactly once and cannot be recovered
    afterwards. Copy it to a secure store before leaving the page. See
    [Device Credentials](credentials.md).

## 5. Connect the device

Choose the path that matches the device:

- **Direct device** — firmware speaks MQTT (primary) or HTTPS long-polling
  itself. Point it at the Link broker with the credential and publish flat
  telemetry frames. See [Direct Device Integration](integrate-direct-device.md).
- **Gateway with sub-devices** — one process holds a single MQTT connection and
  relays many field devices behind it. Register and bind the sub-devices first,
  then run the gateway. See [Gateway Integration](integrate-gateway.md); Edge is
  the ready-made EdgeX-based gateway for this path.

## 6. See live telemetry

Return to the **Overview**. The device turns **Online** on its first
presence/telemetry, the **Telemetry 1h** card climbs, and the throughput panel
updates live over WebSocket — there is no polling. Open the device to inspect
its latest readings and charts.

## Next steps

- [Overview](overview.md) — KPI cards and live panels.
- [Dashboards](dashboards.md), [rule chains](rule-chains.md) and
  [alarms](alarms.md) — visualize, process and alert on the data.
- [NereidLink product page](../../products/nereidlink.md) and the
  [suite glossary](../../reference/glossary.md).
