# Device profile

A **device profile** is the reusable template describing how a class of devices maps raw values to engineering values.

- A **descriptor** is one measurement-point key with unit, precision and a value transform (identity, linear, lookup table, expression, or enum).
- The platform never guesses units: a unit exists only when the descriptor declares it.
- Descriptors are versioned; re-calibration never rewrites stored history.
- A profile may bind a [rule chain](rule-chain.md); devices using it execute that chain unless they override the binding.

A profile is the *point table*; a [connector](connector.md) instance holds the per-device connection parameters. At dispatch the instance overrides are merged over the profile template.
