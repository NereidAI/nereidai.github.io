# Services

The Services module manages service definitions in NereidHorizon. A service definition describes the container image, deployment configuration, and resource limits that an edge node needs to run a workload. You can create, edit, import, and export definitions here.

## Create a service

In the **Basic Info** panel, the following fields are required:

| Field | Description | Example |
|---|---|---|
| Service Name | Unique identifier | `myweather` |
| Label | Display name | `My Weather Service` |
| Version | Semantic version | `1.0.0` |
| Architecture | Target architecture | `amd64`, `arm64`, `arm` |
| Image name | Container image in `name:tag` form | `openhorizon/example:1.0.0` |

Optional settings include the service URL, HA mode, shared block device, privileged mode, memory/CPU limits, ports, health check, network, storage, environment variables, and secrets.

A minimal service definition looks like this:

```json
{
  "label": "My Service",
  "version": "1.0.0",
  "arch": "amd64",
  "deployment": {
    "services": {
      "myorg/myservice": { "image": "myorg/myservice:1.0.0" }
    }
  }
}
```

## Edit a service

Editing offers two modes: a JSON editor and a UI form. The two are synchronized automatically when you switch tabs. When you change the deployment in UI mode, Horizon re-signs the deployment automatically.

## Import and inspect

- **Import** — paste service JSON directly or upload a `.json` file.
- **Detail drawer** — three tabs: **Info**, **Keys**, and **Docker Auths**. Keys manages the service public key; Docker Auths manages credentials for private registries.

## Signing

Horizon signs the deployment automatically with RSA-PSS SHA-256, so there is no manual signing step.

## Error codes

| Code | Meaning |
|---|---|
| 400 | Malformed JSON, or a required field is missing (`label`/`version`/`arch`/`image`) |
| 409 | A service with the same name and version already exists |
| 502 | Exchange unreachable |

## See also

- [Patterns](patterns.md)
- [Deployment Policies](policies.md)
- [Node Registration](node_registration.md)
