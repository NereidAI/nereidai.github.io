# Business generation

A **business generation** is one numbered desired revision of a [business instance](business-instance.md). It is not a [business template version](business-template-version.md): one immutable template version can produce many instances, and each instance has its own generation history.

- `generation` identifies the latest saved desired assembly and parameters. Updates send `expected_generation`; a stale editor receives a conflict instead of overwriting another operator's changes.
- `pending_generation` identifies the deployment or rollback target being applied, which can differ from the latest desired generation.
- `active_generation` identifies the generation confirmed by health read-back. A failed or still-pending rollout does not displace the last active generation.

Every generation retains a deterministic [business expansion](business-expansion.md) and its applied-resource mapping. Rollback re-applies a retained generation through the same preflight and resource-owner path.
