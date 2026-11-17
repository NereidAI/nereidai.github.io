# Business instance

A **business instance** is a tenant-owned deployment draft and lifecycle resource created from a [business template version](business-template-version.md). It retains the complete template snapshot and holds its own parameter values, concrete asset bindings, assembly, and validation state.

Later template releases never rewrite an existing instance, and editing an instance never publishes a template version. Gateway and camera selectors use authoritative NereidLink resources: a camera is chosen from the devices managed by the selected gateway, and changing or clearing that gateway clears the camera selection. Drafts may retain placeholders, but deployment requires the real assets demanded by the assembly.

Each saved desired change is tracked as a [business generation](business-generation.md) with a durable [business expansion](business-expansion.md). Deployment preflights all destinations; monitoring reads actual health. Undeploy removes only resources owned by the instance and leaves shared models, pipeline registrations, companions, and forwarders intact.

Use the [Business orchestration](../business-orchestration.md) guide to create, edit, deploy, monitor, roll back, undeploy, and delete instances.
