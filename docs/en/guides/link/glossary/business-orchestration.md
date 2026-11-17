# Business orchestration

**Business orchestration** is NereidLink's declarative assembly of existing cameras, registered pipelines, models, external servables, companion services, rules, actions, and selective northbound outputs.

- The canvas contains asset references, scalar parameters, and subscription or trigger relationships. It accepts no scripts, expressions, user code, general DAG execution, or NereidInference per-frame pipeline topology.
- NereidLink does not execute camera frames. NereidInference owns the technical pipeline, while companion services own domain conclusions and ledgers.
- Northbound upload requires an explicit output, an existing forwarder, a field whitelist, and explicit raw EdgeX device/profile/resource selectors. Embeddings remain on the edge-local bus and cannot be whitelisted; the merged gateway filter is quiesced rather than deleted when no contributor remains.

Each [business template version](business-template-version.md) is immutable. A [business instance](business-instance.md) binds that assembly to concrete resources and is delivered through [business generations](business-generation.md) and deterministic [business expansions](business-expansion.md).

See the [Business orchestration](../business-orchestration.md) guide for the operator workflow and current integration gates.
