# Business expansion

A **business expansion** is the deterministic `nereidlink.business-expansion/v1` document generated for one [business generation](business-generation.md). It translates the business assembly into closed declarative artifacts: model-distribution requests, pipeline and external-servable registrations, inference connector bindings, companion subscriptions, rule chains, explicit northbound channels, and one gateway-level northbound filter singleton per affected gateway.

Artifact dependencies describe delivery order, not a runtime frame-processing graph. Identical inputs produce byte-identical artifacts and the same SHA-256 digest; stable artifact keys and retained resource mappings make retries and rollback deterministic.

**Preview expansion** inspects the exact saved generation without claiming that its artifacts are deployed. Deployment still requires complete validation and destination preflight, and missing external contracts or capabilities remain blocking findings. Existing resource owners apply the artifacts; NereidLink does not create a second connector transport or a general DAG executor.

See [Business orchestration](../business-orchestration.md) and the [gateway integration](../integrate-gateway.md) guide for ownership and delivery boundaries.
