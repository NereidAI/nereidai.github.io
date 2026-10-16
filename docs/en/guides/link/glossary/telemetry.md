# Telemetry

**Telemetry** is time-series data a device reports — sensor readings and other numeric or discrete samples.

- A **measurement point** (measurement key) is one named signal; its meaning, unit and transform come from the bound [device profile](profile.md) descriptors. The platform never invents units.
- Samples are addressable by device, point key and time, and power dashboards, charts and rules.

Telemetry is observed data; the [device shadow](shadow.md) holds current/desired state, and attributes hold relatively static metadata.
