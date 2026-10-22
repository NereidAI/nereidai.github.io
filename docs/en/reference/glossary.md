---
title: Glossary
---

# Glossary

Terms used across the suite and this site. Product **short names** and
**abbreviations** (NS, NF, NFL, …) are listed on
[Naming & abbreviations](naming.md).

## Suite & products

| Term | Meaning |
|---|---|
| **NereidAI** | The platform / suite and the GitHub organization; never abbreviated. |
| **Suite** | The eight products used together; each product still works on its own. |
| **Product suite** | Two thin suite services (Sphere, Identity) plus six domain products. |
| **Thin layer** | A component that only federates others — portal / SSO / gateway / event glue — and holds no domain logic. Applies to Sphere and Mobile. |
| **Standalone deployment** | Running a single product without the suite layer. It has its own login and data and does not depend on the other products. |
| **Domain product** | A product that owns a full domain end to end — Link, Forge, Horizon, Edge, Fleet, Mobile. |
| **Commercial solution** | An industry offering (NereidFactory, NereidSentinel, NereidMedical) built on the open platform and licensed separately. |

## Identity & access

| Term | Meaning |
|---|---|
| **SSO** | Single sign-on: sign in once, reach every integrated product. |
| **Identity (NI)** | The identity plane; the single source of truth for users, currently a Keycloak realm (`nereidai`) behind a replaceable OIDC engine. |
| **OIDC** | OpenID Connect; the identity protocol Sphere speaks to Identity. |
| **PKCE** | Proof Key for Code Exchange; used with the OAuth/OIDC authorization-code flow. |
| **Ticket (sealed ticket)** | In the default `ns` SSO mode, a short-lived, single-use, audience-bound token Sphere issues and a product exchanges server-to-server for the verified identity. |
| **`ns` / `oidc` mode** | The two product SSO integration modes: ticket handoff (default) or a product acting as its own direct OIDC client. Sphere and the product must agree on the mode. |
| **Break-glass (local) account** | A local bcrypt account in Sphere used only for emergencies when the identity plane is unreachable; never the production default. |
| **RBAC** | Role-based access control. Permissions decide *what* you may do; data scope (tenant / customer / group) decides *which* data you may reach. Stays inside each product. |
| **Tenant** | An isolated customer/partition inside a multi-tenant product. |
| **IdP** | Identity provider (a customer directory). External OIDC / LDAP / SAML IdPs are always connected behind Identity via brokering. |
| **Identity brokering** | Federating an external IdP behind Identity, so Sphere and products always see the same issuer and claims. |
| **Service account** | An OAuth2 client-credentials machine identity, separate from human users. |
| **mTLS** | Mutual TLS; both sides present certificates. Used for service-to-service and device-to-platform links. |

## Security posture & delivery

| Term | Meaning |
|---|---|
| **Air-gapped** | Installed and run with no internet access; all images and dependencies come from an offline bundle / internal mirror. |
| **Call-home** | A mandatory outbound connection to the vendor. NereidAI has none at runtime. |
| **SBOM** | Software Bill of Materials; a per-release inventory of components. |
| **CVE** | A publicly disclosed security vulnerability; enterprise contracts add a response SLA and backported fixes. |
| **LTS** | Long-term support with backported fixes, offered commercially. |
| **Private registry** | An internal container image registry (e.g. Harbor) used instead of public ones. |
| **Helm / chart** | The Kubernetes packaging used to deploy the products. |
| **Store-and-forward** | Edge buffering that keeps telemetry locally during a WAN outage and replays it when the link returns, without losing data. |
| **OTA** | Over-the-air delivery of Edge itself, applications, models, or firmware to remote nodes. |
| **Rollout** | Distributing an artifact to a set of nodes according to a policy (batches, percentage, canary). |
| **Bandwidth-aware delivery** | Delivery that adapts to constrained / intermittent links (resumable, chunked transfers). |
| **Agreement / agbot** | Open Horizon concepts: an *agreement* is a node's commitment to run a service; an *agbot* negotiates and maintains agreements. |

## Link (IoT) domain

| Term | Meaning |
|---|---|
| **Telemetry** | Time-series data a device reports — sensor readings and other numeric or discrete samples. |
| **Measurement point** | One named signal (key); its meaning, unit and transform come from the bound device profile. The platform never invents units. |
| **Device profile** | A reusable template describing how a class of devices maps raw values to engineering values. |
| **Descriptor** | One measurement-point definition with unit, precision and a value transform (identity, linear, lookup, expression, enum). |
| **Device** | A registered, credential-bearing entity that can connect; the platform never physically deletes one. |
| **Gateway** | A device that mediates between the platform and devices that cannot connect directly; one northbound link, many southbound devices. |
| **Sub-device** | A device reached and owned through a gateway. |
| **Standalone device** | A device that connects to the platform directly (MQTT / HTTP / CoAP). |
| **Connector** | A protocol-connector *instance* running on a gateway and managed through the platform; gateway-level or bound to one sub-device. |
| **Edge secret** | A third-party credential the platform delivers to a gateway to store and use, distinct from the gateway's own platform credentials. |
| **Credential** | What authenticates a device: TOKEN, PASSWORD, JWT, or X.509. |
| **Presence** | The real-time view of whether a device is connected: online, offline, or unknown. |
| **Lifecycle state** | A device's operational status (e.g. active, quarantined, decommissioned), distinct from live connection state. |
| **Quarantine** | A reversible incident-response lock that disconnects a device and blocks auth while preserving its identity and history. |
| **Device shadow** | Two independent documents per device: *desired* (target state) and *reported* (last state the device sent). |
| **Attribute** | Relatively static metadata in one of three scopes: client, server, or shared. |
| **Rule chain** | A versioned graph of rule nodes that routes messages and runs tenant-defined logic; the platform itself carries no business logic. |
| **Command** | A remote operation sent to a device/gateway; one-way or request-response, read or write, gated by a command catalog. |
| **Probe** | An on-demand, one-shot reachability check of a sub-device through its gateway; returns answered + RTT, never stored as telemetry. |
| **Health check** | A periodic connector read that is discarded; used by the gateway to mark a sub-device reachable/unreachable. |
| **Alarm** | A triggered condition with a lifecycle (active → acknowledged → cleared) and optional escalation. |
| **Escalation chain** | Ordered, delayed notification steps and target roles for an unhandled alarm. |
| **Forwarder** | An async side output that pushes data to an external system over a pluggable channel. |
| **DLQ** | Dead-letter queue where messages that failed processing can be inspected. |
| **Firmware** | A device software package delivered via OTA with staged status and structured result codes. |
| **WebSocket push** | The single connection over which all live updates are delivered server-side; polling is not used. |
| **NATS** | The message backbone (Core / JetStream / KV); the only service-to-service channel inside Link. |
| **TimescaleDB** | The time-series extension on PostgreSQL used for telemetry. |

## Forge (model factory) domain

| Term | Meaning |
|---|---|
| **Dataset** | A versioned collection of images/data in an annotation format (e.g. COCO / TXT). |
| **Annotation / labeling** | Marking data (bounding boxes, masks, …), with optional VLM-assisted pre-labeling. |
| **Training / fine-tuning** | Producing or adapting a model on a dataset via a Kubeflow pipeline. |
| **Optimization / quantization** | Reducing a model's size/latency (e.g. NNCF, OpenVINO, TensorRT) without retraining from scratch. |
| **Export** | Producing an artifact for a target hardware/runtime. |
| **Multi-silicon / NPU** | The range of GPU/NPU vendors supported; vendor toolchains stay isolated inside Forge pipeline images. |
| **Evaluation** | Assessing model quality / benchmarking, producing dashboard metrics. |
| **Model registry** | The versioned store of produced models and metadata. |
| **Artifact** | A produced, versioned package (model or application) handed to Horizon for rollout. |
| **Kubeflow Pipelines** | The workflow engine that runs Forge training/optimization/evaluation. |

## Edge & fleet

| Term | Meaning |
|---|---|
| **EdgeX Foundry** | The open edge framework Edge is built on (an EdgeX application service), tracked upstream rather than forked. |
| **Zero-touch onboarding** | A field gateway comes up and registers securely with no manual per-device setup. |
| **Local autonomy** | The edge keeps operating and enforcing local logic while the platform link is down. |
| **Field gateway** | The on-site hardware running Edge and connectors to field devices. |
| **AMR** | Autonomous mobile robot; one class of robot Fleet schedules. |
| **Teleoperation** | A human driving a robot remotely; low-latency LAN path. |
| **WeChat Mini Program** | One of Mobile's two targets, alongside the mobile app. |

## Releases & open source

| Term | Meaning |
|---|---|
| **GA** | General availability; production-ready gate (frozen API, docs, signed images + SBOM). |
| **Preview** | Tryable but not stable; core flows work, contracts may change. |
| **Tech Preview** | Minimal demoable slice; no stability or upgrade promise. |
| **VERSION** | The per-repository file that is the single source for release and image tags. |
| **Conventional Commits** | Commit message convention (`feat:`, `fix:`, `docs:`, …). |
| **DCO** | Developer Certificate of Origin; commits are signed off with `git commit -s`. |
